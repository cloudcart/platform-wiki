---
type: feature
nav_path: "Marketing → Discounts → Code PRO → Generator"
route_name: discounts-code_pro-generator
route_path: /admin/marketing-new/discounts/code-pro/:id/generator
aliases: ["Code PRO generator", "Bulk code generator", "Codes generation", "Генериране на кодове", "Генератор на кодове"]
tags: [marketing, discounts, coupons, code-pro, bulk-generation]
plan_gates: ["discount-code-pro", "discount-code-pro-generator"]
created: 2026-05-23
updated: 2026-06-10
source_count: 5
---

# Code PRO bulk generator

## Purpose

The **Code PRO generator** creates many [[marketing-discounts-code-pro]] codes at once **under a single Code PRO discount**, with **shared discount terms** across the entire batch. Instead of clicking through the per-code form 500 times for an influencer campaign, the merchant defines the terms once (conditions, date window, customer groups, region, max-uses, per-customer cap, stacking flags) and the generator emits 500 codes with auto-generated strings — each as its own redeemable Code PRO row.

The generator produces strings in one of **two modes**:

- **Range** — sequential numeric range (e.g., `1000` to `1999` → 1,000 codes named `1000`, `1001`, ..., `1999`). Predictable, easy-to-track codes.
- **Random** — randomly composed alphanumeric / numeric strings of a chosen length (or random length 6-18 if not specified). Unpredictable codes that can't be guessed.

The generator is **plan-gated** on the `discount-code-pro-generator` feature value, which caps the batch size (default 5,000 codes per request on plans that enable it).

## Where to find it

From the [[marketing-discounts-code-pro]] list inside any Code PRO discount, click "Generate codes" (the toolbar button labelled with a list icon — `fa-list`). The breadcrumb reads "Marketing → Discounts → Code PRO → Generator". The route name is `discounts-code_pro-generator`, the path is `/admin/marketing-new/discounts/code-pro/:id/generator`.

The generator is **the only way to produce more than a few Code PRO codes efficiently** — the per-code form ([[code-pro-form]]) creates one code per save.

## Sub-pages (in this cluster)

This feature is split into 6 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[code-pro-generator-form-layout]] — the on-screen settings boxes (General, Code, Registered users, Customer groups, Regions, Date range, Discount limits, Conditions); the Range/Random sub-block; post-save 1.5 s redirect.
- [[code-pro-generator-modes]] — what Range vs Random do once submitted; the two pipelines; generator strategies for alpha / numeric / mixed; the numeric-only soft cap; the leading-zero gotcha.
- [[code-pro-generator-fields]] — full field reference: generator-type / code-shape fields (`code.generator_type`, `code.from`, `code.to`, `code.limit`, `code.length`, `code.structure[]`) + shared per-code fields applied to every row.
- [[code-pro-generator-validation]] — client-side date gate; server-side validators; verbatim error messages including *"Number of codes may not be greater than:max"*, *"You can generate maximum:max promo codes"*, *"Some of the codes have already been created"*.
- [[code-pro-generator-business-rules]] — plan-gate cascade; cap derivation from `discount-code-pro-generator` feature value; all-or-nothing transactional save; identical-terms guarantee; no audit log.
- [[code-pro-generator-api]] — JSON-API v2 `POST /generate`; same pipeline as the admin form **but hard-capped at 5,000 codes per request regardless of plan feature value**.

## What the merchant can do here

- Choose between **Range** and **Random** modes (see [[code-pro-generator-modes]]).
- Define batch-wide discount terms (conditions, date window, customer groups, region, max-uses, per-customer cap, stacking flags) — see [[code-pro-generator-fields]].
- Save once — every code is generated, persisted under a single transaction, and the merchant lands back on the codes list 1.5 seconds later.
- Re-run the generator multiple times if the campaign needs more codes than the plan cap allows.
- Export the resulting batch via [[marketing-discounts-code-pro-export]].

## Settings & fields

The hub does not duplicate the field reference — see [[code-pro-generator-fields]] for the full table of generator-type / code-shape fields (`code.generator_type`, `code.from`, `code.to`, `code.limit`, `code.length`, `code.structure[]`) and shared per-code fields (`active`, `code_apply`, `apply_regular_price`, `only_customer`, `geo_zone_id`, `max_uses`, `maxused_user`, `date_start`, `date_end`, `condition[]`, `customer_groups[]`, `customer_groups_target`, `all_regions`, `no_expire`, `barcode_prefix`). For the on-screen layout that groups these fields into settings boxes see [[code-pro-generator-form-layout]].

## What the merchant CANNOT do here

The most-common rejection cases (see [[code-pro-generator-validation]] for the full message catalogue):

- Generate more than the `discount-code-pro-generator` plan-feature cap.
- Use a `range` where `to ≤ from`.
- Use a `range` whose total count exceeds the plan cap (validator rejects before allocation).
- Use `random` mode with no `code.structure` selected.
- Use `random` numeric-only with a `limit` larger than what `length` digits can fit.
- Re-use code strings that already exist (range mode rejects whole batch; random mode retries internally).
- Use a `length` outside 6-18.

## Business rules (one-line summaries — full detail in aspects)

- **Plan-gate cascade**: `discount-code-pro` (boolean parent) must be on; `discount-code-pro-generator` (numeric) caps per-request size — default 5,000 — see [[code-pro-generator-business-rules]].
- **Identical terms across the batch**: every code shares conditions, customer groups, region, dates, limits, stacking flags — only the `code` string differs — see [[code-pro-generator-business-rules]].
- **All-or-nothing transaction**: the merchant gets a full batch or no batch — never a partial one — see [[code-pro-generator-business-rules]].
- **No audit log** for batch generation (verify) — see [[code-pro-generator-business-rules]].
- **Range mode loses leading zeros** — see [[code-pro-generator-modes]] for the workaround (use Random + numeric structure).
- **Same `marketing.discounts` permission** as the rest of the Discounts engine.

## Plan gates

| Mapping | Shape | What it controls |
|---|---|---|
| `discount-code-pro` | Boolean (parent on/off) | The parent Code PRO discount type must be unlocked — otherwise the generator route is unreachable. |
| `discount-code-pro-generator` | Numeric (max codes per single batch) | Caps `code.limit` (random) or `(to - from + 1)` (range). Default cap **5000 per request**. |

The admin-panel generator honours the higher plan-feature value; the JSON-API v2 endpoint is **hard-capped at 5,000** regardless — see [[code-pro-generator-api]] for the divergence.

## Programmatic access

The same bulk-generation pipeline is exposed via JSON-API v2 — see [[code-pro-generator-api]] for the divergence (hard 5,000 cap) and [[api-discount-codes-pro]] for the resource Schema.

## Related

- [[marketing-discounts]] — parent feature.
- [[marketing-discounts-code-pro]] — per-code create / edit / list (codes generated here appear there).
- [[marketing-discounts-code-pro-export]] — export the generated batch to CSV for distribution.
- [[marketing-discounts-codes]] — Container codes' simpler bulk generator (hard 1,000-per-batch cap, no prefix / length / structure controls).
- [[code-pro-form]] — per-code form sharing the conditions sub-component.
- [[code-pro-overview]] — Code PRO discount type overview.
- [[code-pro-business-rules]] — Code PRO discount-level business rules.
- [[code-pro-endpoints-api]] — endpoint catalogue including the `POST /generate` action.
- [[api-discount-codes-pro]] — JSON-API v2 resource.
- [[discount]] — entity page for the parent Code PRO discount.
- [[discount-code]] — entity page for each generated code.
- [[customers-custom-groups]] — customer groups applied per batch.
- [[geo-zone]] — region applied per batch.
- [[products-smart-collections]] — selections used by `setting=selection` conditions.
- [[settings-statuses]] — `discounts_used_statuses` setting determines which statuses count uses on generated codes.
- [[plan-gates]] / [[plan-vs-feature-pack]] / [[plan-features]] — plan-gating model.

## Open questions

None — all previously-flagged items resolved or distributed to sub-pages.
