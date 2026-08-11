---
type: feature
nav_path: "Marketing → Discounts → Code PRO codes"
route_name: discounts-code_pro-list
route_path: /admin/marketing-new/discounts/code-pro/:id
aliases: ["Discount code PRO", "Code PRO codes", "Code PRO management", "Multi-code campaign", "Промо кодове ПРО", "Управление на кодове"]
tags: [marketing, discounts, coupons, code-pro, multi-code-campaigns]
plan_gates: ["discount-code-pro", "discount-code-pro-generator"]
created: 2026-05-23
updated: 2026-06-10
source_count: 6
---

# Code PRO codes (multi-code campaign management)

## Purpose

The **Code PRO codes** page is the management surface for codes that belong to a **Discount code (PRO)** discount — the discount type for **multi-code campaigns where every code carries its own discount terms**. Unlike Container codes (parent defines the terms, all codes share them) or Promo codes (one code per discount), a Code PRO discount holds **a collection of independently-configured codes** under a single campaign umbrella. Each child code has its own discount terms (`flat` / `percent` / `shipping`), date window, usage limits, customer-group restriction, region, active flag, and stacking flags.

Use Code PRO for an influencer / partner campaign: `INFLUENCER1` gives 15% off, `INFLUENCER2` gives 20% off, `STAFF2026` gives 25% off — each with its own cap and date window — all rolled up under one parent for reporting.

This hub is the navigation pivot; the detail lives on the six aspect pages below.

## Where to find it

From the [[marketing-discounts]] list, click the "Codes management (N)" link on any **Code PRO** discount row. The breadcrumb reads "Marketing → Discounts → Code PRO codes". The modern Vue route is `/admin/marketing-new/discounts/code-pro/:id` (the legacy URL `/admin/discounts/code-pro/{discount_id}` still works).

Sub-screens hang off this list:

| Sub-screen | Route name (Vue) | Route path |
|------------|------------------|------------|
| Create a code | `discounts-code_pro-create` | `/admin/marketing-new/discounts/code-pro/:id/create` |
| Edit a code | `discounts-code_pro-edit` | `/admin/marketing-new/discounts/code-pro/:id/:codeId` |
| Bulk-generate codes | `discounts-code_pro-generator` | `/admin/marketing-new/discounts/code-pro/:id/generator` |
| Export the codes to CSV | (toolbar anchor, no route) | `GET /admin/api/core/discounts/code-pro/{id}/export` |

The generator and exporter are sibling pages: [[marketing-discounts-code-pro-generator]] and [[marketing-discounts-code-pro-export]].

## Sub-pages (in this cluster)

This feature is split into 6 aspect pages. Drill into the aspect that matches the question.

- [[code-pro-overview]] — what makes Code PRO different from Promo / Container, store-wide code uniqueness, the `discount-code-pro` plan-gate, and the type-picker entry surface.
- [[code-pro-form]] — the six form blocks, conditions array row builder, per-target sliding sub-forms (`all`, `order_over`, `product`, `category`, `vendor`, `selection`, `category_vendor`), Allow-price sub-form.
- [[code-pro-fields]] — citation-level field reference: backend keys, defaults, validation strings, listing columns.
- [[code-pro-business-rules]] — non-obvious admin behaviours: per-code active flag independence, deletes-and-recreates save transaction, save-flow sequence, barcode mode, stacking flags, bulk operations.
- [[code-pro-checkout]] — runtime active-scope filter, case-insensitive lookup, single-Code-PRO-per-cart replacement semantics, and the `uses` counter recompute that runs as a background task about 10 seconds after a counted status change.
- [[code-pro-endpoints-api]] — admin-panel endpoints under `/admin/api/core/discounts/code-pro/`, JSON-API v2 surface, the 5,000-codes-per-request hard cap on bulk-generate.

## What the merchant can do here

From the list view:

- See every code with columns **name**, **code**, **active** toggle, **uses** counter, **max_uses** (∞ if NULL), **date period**, **targets count**.
- **+ Add code** — opens the single-code form (see [[code-pro-form]]).
- **Bulk-generate codes** — opens [[marketing-discounts-code-pro-generator]].
- **Export to CSV** — downloads all codes via [[marketing-discounts-code-pro-export]].
- Edit any code by clicking its row.
- Toggle a code `active` / `inactive` inline (inactive codes are rejected at checkout).
- Bulk-toggle status and bulk-delete via the table action bar.

Filters: `active`, `time_used`, `uses_left`, `start_date`, `date_end`.

The merchant **cannot** reuse a code string anywhere in `discounts_code_pro.code` store-wide (*"Discount code is exists"* — `code_pro.validation.code.unique`), save without `date_start` (*"Data is required"* — `code_pro.validation.date_start.required`), save without at least one condition (*"Conditions are required"* — `code_pro.validation.condition.required`), save an `order_over` condition without an amount (*"Amount is required"* — `code_pro.validation.condition.order_over.required_if`), or save a condition with `value < 0.01`. The `customer_groups_target` ("All groups") and `all_regions` toggles must be ON unless an explicit list / zone is picked. Full reference on [[code-pro-fields]].

## Settings & fields

Each per-code form carries: **Active** (`active`), **Code** (`code`, required, max 20 chars, `alpha_num`, unique on `discounts_code_pro.code`), **Barcode mode** (`code_prefix` + `code_format` ∈ {`ean13`, `ean8`, null} + `barcode_prefix`), **Stacking flags** (`code_apply`, `apply_regular_price`), **Guest restriction** (`only_customer`), **Date window** (`date_start` required + `date_end`, nullable if `no_expire` ON), **Usage limits** (`max_uses` and `maxused_user`, each 1–100,000 or unlimited), **Customer groups** (`customer_groups[]` + `customer_groups_target` toggle), **Region** (`geo_zone_id` + `all_regions` toggle), **Name** (`name`, optional, falls back to `code`), and a **Conditions array** (`condition[]`, up to 5 rows of `type` / `value` / `setting` + per-target records + `allow_price`). The citation-level reference — defaults, validation strings, listing columns — is on [[code-pro-fields]]; the form-block layout and per-target sub-forms are on [[code-pro-form]].

Plan-feature keys: **`discount-code-pro`** (gates creating the parent campaign) and **`discount-code-pro-generator`** (the admin-panel bulk-generate batch-size cap). See [[code-pro-overview]] + [[code-pro-endpoints-api]].

## Business rules

Cluster-wide rules that span multiple aspects:

- **Each code is its own mini-campaign.** The parent is just an organizational umbrella; every discount term lives per-child-code. See [[code-pro-overview]].
- **Store-wide code uniqueness.** `discounts_code_pro.code` is unique across the entire store; two Code PRO campaigns cannot share a code string. See [[code-pro-overview]].
- **Per-code active flag is independent.** A child code is redeemable only when BOTH parent and child are `active = 1`. See [[code-pro-business-rules]].
- **Conditions deleted-and-recreated on save.** Every save drops all `targets` and `customer_groups` join rows then re-inserts from the payload — external integrations must re-look-up by `code_id`. See [[code-pro-business-rules]].
- **Uses counter recomputes async on counted statuses.** Orders contribute to `uses` only on the store's `discounts_used_statuses` (default `paid` / `completed` / `fulfilled` — see [[settings-statuses]]); cancels / refunds free the code back up. See [[code-pro-checkout]].
- **Checkout active-scope** combines parent active, child active, date window, `max_uses > uses`, customer-group match, and `geo_zone_id` match. Any failure yields a generic "invalid code" message. See [[code-pro-checkout]].
- **One Code PRO code per cart.** Typing a second replaces the first; combining codes requires Container codes ([[marketing-discounts-codes]]). Lookup is **case-insensitive** (`summer25` / `SUMMER25` match). See [[code-pro-checkout]].
- **JSON-API v2 triggers the same side-effects** as the admin save — same transaction, uniqueness constraint, recompute, and audit-log entry (source `api2`). Bulk-generate has a hard cap of **5,000 codes per request** on the API regardless of `discount-code-pro-generator`; only the admin-panel generator honours higher plan values. See [[code-pro-endpoints-api]].
- **Plan-gating.** Creating a parent requires `discount-code-pro = 1`; without it the type-picker opens the upgrade modal (*"To create a discount code, you need to upgrade your plan."*). Once a parent exists, attaching children has no per-code plan limit.
- **Permission.** All admin endpoints are protected by the `marketing.discounts` permission.

## Related

- [[marketing-discounts]] — parent feature; Code PRO discount type lives there.
- [[marketing-discounts-code-pro-generator]] — sibling page — bulk-create many codes at once with prefix / suffix / range / random controls.
- [[marketing-discounts-code-pro-export]] — sibling page — CSV export of the entire codes list with conditions.
- [[marketing-discounts-codes]] — Container codes (identical-terms mass-generated single-use coupons).
- [[discount]] — entity page for the parent Code PRO campaign.
- [[customers-custom-groups]] — customer groups referenced by `customer_groups[]`.
- [[geo-zone]] — geo zones referenced by `geo_zone_id`.
- [[products-smart-collections]] — selections used by `setting=selection` condition.
- [[products-categories]] — categories used by `setting=category` / `category_vendor`.
- [[products-vendors]] — vendors used by `setting=vendor` / `category_vendor`.
- [[settings-statuses]] — `discounts_used_statuses` setting determines which statuses count toward `uses`.
- [[settings-hooks]] — `discount.updated` event fires on the parent campaign on per-code CRUD.
- [[marketing-campaigns]] — campaigns can substitute dynamic Code PRO codes via the `{triggered_dynamic_discount}` replacement (gated on `discount-code-pro`).
- [[marketing-segments]] — segment conditions can reference Code PRO usage (also `discount-code-pro` gated).
- [[api-discount-codes-pro]] — JSON-API v2 resource for individual Code PRO codes.
- [[api-discounts]] — JSON-API v2 resource for the parent campaign (with `type=code-pro`).
- [[cart-vs-order-lifecycle]] — where the checkout active-scope evaluation runs.
- [[json-api-v2]] — authentication, rate-limit, same-side-effects principle.

## Open questions

No outstanding questions.
