---
type: feature
nav_path: "Marketing → Discounts"
route_name: discounts-list
route_path: /admin/marketing-new/discounts
aliases: ["Discounts", "Promo codes", "Coupons", "Coupon codes", "Sales", "Promotions", "Промо кодове", "Отстъпки", "Купони"]
tags: [marketing, discounts, coupons, promo-codes, promotions]
plan_gates: ["total_discounts", "discount_global", "discount_fixed", "discount_coupon", "discount_quantity", "discount_banner", "discount-code-pro", "discount-code-pro-generator"]
created: 2026-05-21
updated: 2026-06-10
source_count: 8
---
# Discounts

## Purpose

The **Discounts** page is the merchant's main promotions toolbox — a catalogue of discount **types** (the **+ Add discount** modal offers 10 cards) that cover virtually every promotion model an online store needs. Compared to the more flexible [[apps-cart-rules]] (composable trigger + action engine), Discounts are simpler **single-condition** rules — one type, one target, one threshold — but cover the most common 80 % of merchant promotions: holiday sales, customer rewards, inventory liquidation, volume incentives, and flash sales.

This page is the **hub** for the entire Discounts area. Each discount **type** has its own per-type detail page (with create-form fields, save-time validation, and a worked example). Cross-cutting topics that apply to every type — lifecycle, eligibility, storefront display, audit trail, known issues — have their own aspect pages inside `marketing-discounts/`.

## Where to find it

**Sidebar → Marketing → Discounts.** The breadcrumb reads "Marketing → Discounts". The route is `/admin/marketing-new/discounts` (modern Vue UI). The legacy URL `/admin/discounts/` still works and continues to drive the same backend, but the modern Vue listing is the default merchant experience (toggled via the `marketing-discounts` cookie — set to `old` to fall back).

## What the merchant can do here

From the list view:

- See every discount with name, type, code, date window, uses-count, max-uses limit, and active status.
- **+ Add discount** — opens the **type-picker modal** with 10 cards (listed below). Picking a card opens the matching create form. Only the **Discount code** (PRO) card is plan-gated — on a plan without it, choosing it shows an upgrade panel (*"This feature is not enabled for your plan. To access it, please upgrade your plan."*); the other cards are always selectable.
- Toggle a discount **active / inactive** with the row switch (rate-limited — see [[discounts-lifecycle]]).
- Bulk-toggle status or bulk-delete via the table action bar.
- Filter / sort by type, code, date window, uses, active state, etc.
- Drill into per-type sub-pages — Code management ([[marketing-discounts-code-pro]]), Container codes ([[marketing-discounts-codes]]), per-product overrides ([[marketing-discounts-products]]).
- See **"Last update"** badge on freshly-saved discounts during background regeneration — see [[discounts-storefront-display]].

Things the merchant CANNOT do:

- Activate two Countdown discounts at once (single-instance rule — see [[discounts-known-issues]]).
- Stack a promo code on already-discounted items by default — see the `code_apply` toggle on [[discounts-eligibility]].
- Tie two Quantity discounts to the same product — see [[discounts-known-issues]].
- Reactivate within 10 minutes of the prior toggle — see [[discounts-lifecycle]].
- See "who changed this discount and when" — there is no internal audit log; see [[discounts-audit-trail]].

## Sub-pages — per-type details

The **+ Add discount** modal offers **10 cards, in this order**. The first opens a separate engine, the last two are visual-only and managed under Products; the rest are the discount **types**, each with its own page (create-form fields, validation, worked example, storefront rendering):

- **Cart rules** — opens [[apps-cart-rules]] (a separate multi-condition engine, not a discount type).
- **Global discount** — an always-on, no-code discount. One "Discount type" select chooses the flavour: [[marketing-discounts-flat]] (fixed amount off, -10 EUR), [[marketing-discounts-percent]] (percentage off, -15 %), or [[marketing-discounts-shipping]] (Free shipping).
- **Discount with promo code** — the same flat / percent discount, applied only when the customer enters a code (the single-`code` variant on [[marketing-discounts-flat]] / [[marketing-discounts-percent]]).
- **Discount with multiple promo codes - Container** — a parent discount that owns many child promo codes (for mail-outs); the child codes are listed on [[marketing-discounts-codes]].
- **Fixed discount** — a fixed replacement price per product / variant (MSRP override): [[marketing-discounts-fixed]] + per-product table [[marketing-discounts-products]].
- **Quantity discount** — buy-more-pay-less unit-price tiers on ONE product (max 12 tiers): [[marketing-discounts-quantity]].
- **Countdown discount** — flash sale + timer + confetti / fireworks / parade effect; only ONE per store: [[marketing-discounts-countdown]].
- **Discount code** (PRO) — multi-code campaign where each code carries its own terms; the only plan-gated card: [[marketing-discounts-code-pro]] (+ [[marketing-discounts-code-pro-generator]], [[marketing-discounts-code-pro-export]]).
- **Label Discount** — a text label on products (visual only, not a price cut), managed under Products → Product labels: [[products-banners-labels]].
- **Visual Label/Image** — a sticker / image badge over products (visual only): [[products-banners-labels]].

## Sub-pages — cross-cutting aspects

Behaviour that applies uniformly across every discount type:

- [[discounts-lifecycle]] — `active`, date window, "No expiration", hourly auto-disable, 10-minute activation cooldown, "Latest update" badge, counted statuses.
- [[discounts-eligibility]] — customer-group / geo-zone / guest gating, `maxused_user`, `code_apply` stacking, `apply_regular_price`, `force_save`, resolution order.
- [[discounts-storefront-display]] — per-product attachment regen, cache invalidation, strikethrough, MSRP, countdown timer / popup, smart-collection refresh.
- [[discounts-audit-trail]] — webhooks, per-order discount rows, `uses` mechanics, no internal audit log.
- [[discounts-known-issues]] — Countdown single-instance, 10 000-combination cap, strict-greater rules, MSRP "Save X" gotcha, code-lookup order, JSON-API 5-type allowlist + HTTP 403, older-wiki corrections.

## Sub-screens (routes)

| Label | Route name | Route path |
|-------|------------|------------|
| Discounts list | `discounts-list` | `/admin/marketing-new/discounts` |
| Create | `discounts-create` | `/admin/marketing-new/discounts/create/:type` |
| Edit | `discounts-edit` | `/admin/marketing-new/discounts/edit/:id` |
| Fixed-discount products | `discounts-products` | `/admin/marketing-new/discounts/products/:id` |
| Code PRO codes list | `discounts-code_pro-list` | `/admin/marketing-new/discounts/code-pro/:id` |
| Code PRO bulk generator | `discounts-code_pro-generator` | `/admin/marketing-new/discounts/code-pro/:id/generator` |
| Code PRO create / edit code | `discounts-code_pro-create` / `-edit` | `/admin/marketing-new/discounts/code-pro/:id/create` (or `/:codeId`) |
| Container codes list | `discounts-codes_list` | `/admin/marketing-new/discounts/codes` |

The backend API is namespaced under `admin.api.discounts.*` — CRUD + sub-routes for `products/{id}` (Fixed), `code-pro/{id}` (PRO), and `codes` (Container).

> **⚙️ Backend — CloudCart staff only (internal; not a merchant-facing answer).**
> Modern Vue create/update endpoints (under prefix `admin/api/core/discounts`): create = `POST /{type?}` (`admin.api.discounts.store`), update = `PATCH /{id}/{type?}` (`admin.api.discounts.update`), show = `GET /{id}` (`admin.api.discounts.show`); `type` ∈ `code|container|fixed|quantity|countdown|code-pro`. Fixed products live under `products/{discount_id}`: list `GET /`, get `GET /{product_id}`, create `POST /`, **update `POST /{product_id}`**, status `POST status`, delete `DELETE /`. Container codes under `codes`: index/store/delete + `change-status`. The store/update controller methods (the platform code) call the platform code / the platform code — **not** the legacy the platform code path. So on the modern SPA **all** validation is the request layer (the request validator/the request validator); the model-layer `_validateType` (and its error strings) is dead code for the SPA.

## Settings & fields

The hub does not introduce new fields directly. Field-level documentation lives on the per-type pages (for type-specific fields) and the cross-cutting aspect pages:

- Scheduling fields (`date_start`, `date_end`, `max_uses`, timer switches) → [[discounts-lifecycle]].
- Eligibility / stacking fields (`customer_groups[]`, `geo_zone_id`, `only_customer`, `maxused_user`, `code_apply`, `apply_regular_price`, `force_save`) → [[discounts-eligibility]].
- Display fields (`color`, `text_color`, `discount_amount_type_in_label`, `hide_discount_price`, `msrp`, `position`, `countdown_popup_effect`) → [[discounts-storefront-display]].
- Targeting fields (`type`, `type_value`, `settings`, `order_over`, `products[]`, `product_categories[]`, `vendors[]`, `selections[]`) → the per-type page.
- Code / barcode fields (`code`, `code_format`, `code_prefix`, `barcode_prefix`) → the per-type page (code variants) and [[marketing-discounts-code-pro]].

## Business rules

All cross-cutting rules live on the aspect pages:

- **Active = `active=yes` AND in date window AND `max_uses > uses`** → [[discounts-lifecycle]].
- **Customer-group / region / guest gating; `code_apply` stacking; ONE `order_over` winner; Cart Rules run AFTER Discounts** → [[discounts-eligibility]].
- **Per-product attachment regen + cache invalidation + MSRP "Save X" display + countdown rendering** → [[discounts-storefront-display]].
- **`discount.created` / `discount.updated` / `discount.deleted` webhooks; no internal audit log** → [[discounts-audit-trail]].
- **Validation edge cases (Countdown single-instance, target combinatorial cap, strict-greater `order_over`, code-lookup order, JSON-API 5-type allowlist + HTTP 403)** → [[discounts-known-issues]].

## Plan gates

Plan limits on discounts are enforced as **usage quotas** — each counter caps how many discounts of a kind a store may have, surfaced as the "used / limit" figure in the panel (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

- `total_discounts` — aggregate cap across all discounts.
- `discount_global` — no-code Flat / Percent / Shipping (counts only no-code discounts with stacking off).
- `discount_coupon` — code-based discounts (Promo, Container, PRO child codes).
- `discount_fixed` — Fixed per-product discounts.
- `discount_quantity` — Quantity discounts.
- `discount_multi_coupon` — Container parents.
- `discount_banner` / `discount_labels` — visual Banner / Label (see [[products-banners-labels]]).
- `discount-code-pro` (boolean) — whether Code PRO is available at all.
- `discount-code-pro-generator` (numeric) — max codes per bulk-generator run.

Of these, only **Code PRO** is enforced as a hard gate at create time in the modern panel: choosing the **Discount code** (PRO) card on a plan without it returns **HTTP 403** with *"This feature is not enabled for your plan. To access it, please upgrade your plan."* and lists the eligible plans. For the other types the counter is a usage figure ("used / limit"); the modern Discounts create form does not itself block on it — the [[json-api-v2]] create path is where those per-type quotas are enforced server-side. See [[discounts-known-issues]] for the older "HTTP 402" correction.

> **⚙️ Backend — CloudCart staff only (internal; not a merchant-facing answer).**
> **Why the admin create gate only fires for Code PRO — a latent key-mismatch bug.** The platform code store-middleware builds the gate key as `sprintf('discount-%s', type)` (hyphen) and calls the platform code. But the `plan_features.mapping` catalogue is **underscore**-keyed (`discount_global`, `discount_coupon`, `discount_fixed`, `discount_quantity`, `discount_multi_coupon`, `discount_banner`, `discount_labels`, …) — the only dash-keyed mappings are `discount-code-pro` and `discount-code-pro-generator`. So the platform code resolves to **null**, and the platform code returns `true` on null → the 403 never fires for those types. Only `discount-code-pro` matches a real mapping, so only it is genuinely gated. The underscore mappings are usage counters consumed via the platform code / the `PlanUsage` trait (the "used / limit" surface), and the JSON-API v2 path gates through the platform code with the underscore keys (so the API enforces them even though the admin create endpoint doesn't). If the hyphen/underscore mismatch is ever fixed, the admin create gate would start firing for all types — re-verify before relying on the current pass-through behaviour.

## Programmatic access

Discount creation, code generation, and product / category linkage can be driven via [[json-api-v2]] — see [[api-discounts]], [[api-discount-codes]], [[api-discount-codes-pro]], [[api-product-to-discount]]. Same webhook events + plan-feature gating apply. API allowlist is **5 types** (`percent`, `flat`, `fixed`, `shipping`, `code-pro`); Quantity and Countdown must be configured in the admin panel. See [[discounts-known-issues]].

## Related

- [[marketing]] — parent hub.
- [[discount-stacking]] — how multiple discounts / codes / cart-rules combine (the cross-cutting model behind this screen).
- [[order-totals-pipeline]] — where discounts land in the order total (stage 2: before shipping + VAT).
- [[apps-cart-rules]] — composable multi-condition rules engine (runs AFTER Discounts at checkout).
- [[apps-cart-rules-rules]] — Cart Rules sub-page.
- [[marketing-cross-sell]] — conditional product recommendations (different system).
- [[products-banners-labels]] — visual-only Label / Banner type.
- [[products-smart-collections]] — auto-curated lists; referenced by `selection`-target discounts.
- [[customers-custom-groups]] — `customer_groups[]` restriction.
- [[geo-zone]] — `geo_zone_id` restriction.
- [[settings-hooks]] — discount webhooks.
- [[settings-statuses]] — `discounts_used_statuses` setting.
- [[analytics-top-order-discounts]] / [[analytics-top-order-product-discounts]] — analytics dashboards.
- [[marketing-segments]] — segment conditions reference discount usage.
- [[marketing-campaigns]] — campaigns can include dynamic-code replacements via PRO codes.
- [[apps-up-cross-sell]] — Cross-sell app references discounts in its conditional offers.
- [[discount]] / [[discount-code]] — entity pages.
- [[products-products]] / [[products-categories]] / [[products-vendors]] — discount targets reference these.

## Open questions

None — all previously-flagged items resolved or distributed to sub-pages.
