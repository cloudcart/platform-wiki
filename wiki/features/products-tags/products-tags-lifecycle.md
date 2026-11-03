---
type: feature
nav_path: "Products → Tags → Lifecycle & validation"
route_name: products.tags
route_path: /admin/products/products/edit/:id (Tags section)
aliases: ["Product tag lifecycle", "Tag auto-create", "firstOrCreate tags", "Tag validation", "Tag lowercase", "Tag caps", "100 tags per product", "191 chars"]
tags: [products, tags, classification, taxonomy, validation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 8
---

# Product Tags — lifecycle & validation

> Part of [[products-tags]]. See the hub for the other aspects (assignment, data model, consumers + API).

## Purpose

This aspect documents **how a product tag is born, validated, and never auto-pruned** — the on-save auto-create resolver, lowercasing, wildcard sanitization, the per-product caps, concurrency / deadlock recovery during bulk imports, and the absence of an auto-prune step. The merchant-facing trigger (typing into the picker) is on [[products-tags-assignment]]; what gets stored is on [[products-tags-data-model]].

## Where to find it

This lifecycle runs invisibly whenever a product is saved with tag strings — from the product editor's Tags aside ([[products-tags-assignment]]), from a [[products-products]] bulk-tag action, from bulk imports ([[apps-csv-import]] / [[apps-xml-sync]]), or from a JSON-API v2 product PATCH ([[products-tags-consumers-api]]). There is no screen the merchant visits for it.

## What the merchant can do here

- Type a brand-new tag name and have it created automatically on save — no "create the tag first" step.
- Rely on case-insensitive de-duplication so "Summer 2026", "SUMMER 2026", and "summer 2026" all resolve to one tag.

What the merchant **cannot** rely on: automatic clean-up of unused tags (orphan tags persist — see Business rules).

## Settings & fields

There are no merchant-editable settings for the lifecycle. The relevant **server-side validation rules** (platform-wide, NOT plan-gated) are:

| Rule | Limit / behaviour |
|------|-------------------|
| Tag string length | ≤ **191 characters** per tag. |
| Tags per product | ≤ **100 tags** per product (hard ceiling; exceeding returns a validation error). |
| `url_handle` length | ≤ **191 characters**. |
| Uniqueness | Enforced on the `tag` column. |
| Wildcard-only tags | A tag whose **entire value** is just `%` or just `_` is dropped. |

## Business rules

### Tag names are auto-lowercased on save

When the merchant types a new tag name and confirms, the platform lowercases the text before saving. So "Summer 2026", "SUMMER 2026", and "summer 2026" all resolve to the same tag — the stored canonical value is "summer 2026". This prevents accidental near-duplicates from case variations during bulk imports or quick typing. Spaces, accents, and punctuation are preserved as-is.

### Uniqueness, length, and skipped characters

The Tag form-request validation caps the tag value at 191 characters and enforces uniqueness on the `tag` column. When tags are batch-added via the product save flow:

- Each tag is trimmed of leading/trailing whitespace, and duplicates within the same product are de-duplicated.
- A tag whose **entire value** is just `%` or just `_` is dropped (these single-character wildcard strings are reserved for SQL LIKE matching). Tags that merely **contain** `%` or `_` are kept intact — e.g. "50%-off" is stored as "50%-off" (the characters are NOT stripped from inside the tag).
- A hard ceiling of **100 tags per product** is enforced server-side; exceeding it returns a validation error.
- Each tag string itself must be ≤ 191 characters.

### Auto-creation on product save (`firstOrCreate`)

When a product is saved with a new tag string, the platform's tag-resolver:

1. Trims each tag and de-duplicates within the product.
2. Drops any tag whose entire value is just `%` or just `_` (wildcard-only tags); tags that merely contain those characters are kept.
3. Lowercases each tag name, then calls a `firstOrCreate` per lowercased tag name, so a missing tag is created on the fly.
4. Caches the resolved tag in-memory for the rest of the save batch (to avoid re-resolving the same tag many times during bulk imports).

The resolver tolerates concurrent inserts: if two parallel product-save jobs try to create the same tag, the second falls back to a shared-lock SELECT to load the row the first inserted. This auto-create runs **identically** on JSON-API v2 product PATCHes (see [[products-tags-consumers-api]]).

### Stale-tag recovery on deadlock

If a tag row is rolled back by a database deadlock during a bulk product import (but its ID is still cached in memory), the platform detects the resulting foreign-key violation and re-resolves the tag by name, re-inserts it, and retries the product-to-tag link. The merchant doesn't see this — it's transparent recovery during heavy CSV/XML imports.

### No auto-prune of unused tags

The backend does **NOT** auto-delete tags when their product count drops to 0. Orphan tags persist until the merchant (or an admin endpoint) deletes them explicitly. (An earlier version of this wiki claimed the platform "may auto-prune" — that is incorrect.)

### Re-indexing on tag rename

When a tag is renamed via the admin API, the listing engine does **NOT** have a dedicated tag-rename patch job (unlike vendors and brand-models). Products reference tags via the join table, so storefront filter labels update naturally on the next index refresh, but there is no immediate batch re-index triggered specifically by a tag rename.

## Related

- [[products-tags]] — hub.
- [[products-tags-assignment]] — the picker that triggers this lifecycle (referenced inline above).
- [[apps-csv-import]] — bulk import path that exercises the deadlock-recovery branch.
- [[apps-xml-sync]] — feed sync path that writes tags via the same resolver.

## Open questions

- Whether any UI or scheduled job offers orphan-tag clean-up (currently none found; verify).
