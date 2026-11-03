---
type: feature
nav_path: "Products → Smart Collections → Async evaluation"
route_name: selections
route_path: /admin/products/smart-collections
aliases: ["Smart Collections evaluation", "Smart Collections regeneration", "Selection executing flag", "Selection Pending Finished status", "Smart Collections async", "Smart Collections background jobs"]
tags: [products, collections, selections, async, jobs, status, regeneration]
plan_gates: ["product_collections"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[products-smart-collections]]. See the hub for the other aspects (list view, editor, rule builder, rule types, storefront side-effects, rules and limits).

# Smart Collections — async evaluation

## Purpose

The mechanism that turns rule definitions into a concrete product list. When the merchant saves a collection, edits a product that might affect membership, or changes a linked discount, the platform queues a background regeneration job that walks the catalogue, applies the rules, and writes the resolved set into the collection's cached `products` field. Until the job finishes the collection shows **Pending** on the list; once finished it flips to **Finished**. This page documents the three trigger sources, the flag mechanics, the recovery path for stuck-Pending collections, and why the storefront can serve a stale list for a brief window after Save.

## Where to find it

The async status is surfaced on the [[smart-collections-list-view]] under the **Status** column. The flag itself (`executing`) lives on the selection record — see [[smart-collections-editor]] for the full 11-field shape.

The merchant has no settings page that exposes the regeneration internals; the entry points are the Save button on the editor, product edits anywhere in [[products-products]], and discount edits in the Discounts feature.

## What the merchant can do here

The merchant cannot trigger or cancel a regeneration job directly — it runs automatically. What they can do is:

- **Watch the Status badge** on [[smart-collections-list-view]] flip from Pending to Finished.
- **Wait** for Finished before linking a discount to the collection — discounts attached to a still-evaluating collection may not apply to the right product set until the job finishes.
- **Recover from stuck Pending** by re-saving the collection (re-fires the regeneration job) when the badge remains Pending after several minutes.

## Settings & fields

### The `executing` boolean is the badge mechanism

The "Pending vs Finished" badge is driven by a boolean flag — Pending = `executing = 1`, Finished = `executing = 0`. The flag is set to `1` on every Save and flipped back to `0` only when the regeneration job completes successfully.

### The `products` field caches the resolved list

After regeneration, the resolved product list is stored on the selection record itself (the `products` field). The storefront category-render does not re-evaluate conditions on every page load — it reads the cached list. This is why a brief stale window can exist immediately after Save: the cached list still reflects the previous rule set until the job finishes.

### `last_generated_at` records the completion timestamp

When a regeneration finishes, the timestamp is written to `last_generated_at`. The list view does not currently surface this field directly — it's diagnostic, useful when investigating why the storefront shows stale data. (verify whether the field appears anywhere in the admin UI)

## Business rules

### Three event sources trigger regeneration

The platform regenerates a collection's product list whenever any of these happen:

1. **The collection itself changes** — name save, rule add / edit / delete, URL handle change. This is the most direct trigger and fires on every Save from the [[smart-collections-editor]].
2. **A product changes** in a way that could affect membership — category change, price change, vendor change, tag change, property-value change, new / digital / sale / featured flag change, or product create / delete. Every collection that could possibly match the changed product is re-evaluated. For very large catalogues with many smart collections, a bulk import can queue many regeneration jobs at once — see [[smart-collections-storefront-side-effects]] for the search re-index pressure.
3. **A linked discount changes** — discount activation / deactivation or scope change. Collections referenced by the discount's scope are re-evaluated to keep the discount-aware view consistent.

### Job completion time scales with catalogue size

For typical catalogues, regeneration finishes in seconds. Large catalogues with many cross-references can take a few minutes — the Pending badge stays until the job finishes. The merchant should not panic about a Pending badge that lingers under five minutes; beyond that, suspect a stuck job.

### Stuck-Pending recovery procedure

If a job fails (e.g., transient DB error), the collection can stay Pending — the flag never flips back to 0. The recovery procedure:

1. Refresh the [[smart-collections-list-view]] page.
2. If the collection is still Pending after a few minutes, re-open the collection in the editor and Save it again — this re-fires the regeneration job. No edit is required; just clicking Save is enough.
3. If still Pending after the re-save settles, escalate — there may be an underlying queue-worker outage.

### Don't link discounts to Pending collections

A common operational pattern: the merchant creates a discount in the Discounts feature scoped to a collection. If the collection is still Pending when the discount is created, the discount may not apply to the right product set until the regeneration finishes — and the discount's own re-evaluation may not pick up the eventual final set. The safe path is: wait for Finished, then link the discount.

### Per-row `sort_order` does not affect membership

Rule rows persist with a `sort_order` value (see [[smart-collections-rule-builder]]). Because all rules are AND-combined, the evaluation result is independent of row order — `sort_order` exists for UI / API forward-compat but has no behavioural effect on the regenerated product list.

### Save flips Pending even for non-rule edits

Editing only the SEO title or description (no rule change) still re-fires the regeneration job — the platform does not currently dirty-check which fields changed before queuing the job. The cost of a no-op regeneration is small; the Pending flicker is the merchant-visible cost.

### The job runs once per regeneration trigger, not per row

A collection with 10 rules and 100,000 candidate products runs a single regeneration job — not one job per row. The job walks the catalogue once with all rules applied. This is why catalogue size, not rule count, dominates job duration.

## Related

- [[products-smart-collections]] — hub.
- [[smart-collections-list-view]] — where the Status badge is surfaced.
- [[smart-collections-editor]] — the Save that flips Pending.
- [[smart-collections-rule-builder]] — where rule edits originate from.
- [[smart-collections-storefront-side-effects]] — the search re-index + storefront cache flush that fire alongside regeneration.
- [[products-products]] — product edits that may trigger collection regeneration.
- [[background-queue-inventory]] — adjacent background-queue patterns; useful context for jobs / queue troubleshooting.

## Open questions

- (verify) Whether `last_generated_at` is surfaced anywhere in the admin UI (diagnostic value only).
- (verify) The exact dirty-check policy on Save — does the platform skip regeneration when only SEO fields changed, or always re-fire?
