---
type: feature
nav_path: "Marketing → Discounts → Quantity → Plan gating"
route_name: discounts-create
route_path: /admin/marketing/discounts/create/quantity
aliases: ["Quantity discount plan limit", "discount_quantity gate", "Quantity discount API access", "Quantity discount un-validated fields"]
tags: [marketing, discounts, quantity, plan-gates, json-api-v2, graphql]
plan_gates: ["discount_quantity", "total_discounts"]
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[marketing-discounts-quantity]]. See the hub for the other aspects (form, tier evaluation, stacking, uniqueness constraint, storefront display).

# Quantity discount — plan gating, API access, un-validated fields

## Purpose

This aspect documents:

1. The **plan checks** on creating a Quantity discount.
2. The **programmatic-access surface** — Quantity discounts are excluded from JSON-API v2 writes; the only programmatic path is GraphQL.
3. The set of fields that are **submitted-but-NOT-validated** for the Quantity type (`max_uses`, `maxused_user`, `force_save`, region, code).
4. The auto-disable sweep that runs hourly in UTC.

## Where to find it

The `discount_quantity` plan limit is a **usage counter** (the "used / limit" figure), **not** a hard create-time block in the modern panel:

- **Discount-type picker** (when creating a new discount from [[marketing-discounts]]) — the **Quantity discount** card is **not** greyed out by the `discount_quantity` quota; it stays selectable. (Only the Discount code (PRO) card is plan-gated at create time — see [[marketing-discounts]] → Plan gates.)
- **Create endpoint** — the admin form checks on create only whether the kind is enabled on the plan (`discount-quantity`). If not: HTTP 403 with *"This feature is not enabled for your plan. To access it, please upgrade your plan."* No numeric limit applies here.
- **JSON-API v2** — POST / PATCH against `/api/v2/discounts` with `discount_type=quantity` IS rejected at the resource validator — but as a **type restriction** (Quantity is excluded from the v2 writable allowlist), not a plan gate.
- **Admin GraphQL API** ([[settings-pat-tokens]]) — `createDiscount` with type `quantity` IS refused once the store has as many Quantity discounts as `discount_quantity` allows (or the plan does not include it); `updateDiscount` is not plan-checked.

## What the merchant can do here

The merchant cannot raise the quota from this screen — the controls are at the plan / feature-pack level (see [[plan-vs-feature-pack]]). To raise the `discount_quantity` usage quota:

- **Upgrade to a plan that includes `discount_quantity`** (or a higher numeric cap).
- **Buy a feature pack** that extends `discount_quantity` (numeric gates extend via packs).
- **Delete unused Quantity discounts** (deactivation alone keeps the slot held — see [[quantity-discount-uniqueness-constraint]]).
- **For programmatic access**, use the Admin GraphQL API's `createDiscount` / `updateDiscount` with a personal access token the store owner creates at [[settings-pat-tokens]], instead of JSON-API v2 with an API key (Quantity is excluded from the JSON-API v2 writable allowlist).

## Settings & fields

The plan-gating aspect has no merchant-tunable fields on the Quantity form. The fields below are submitted in the API request body but **NOT validated or enforced** for Quantity-type discounts (the type-specific validator path only validates `name`, `active`, `product_id`, `conditions[]`):

| Field | Backend key | Status for Quantity type |
|-------|-------------|--------------------------|
| Total uses cap | `max_uses` | NOT shown on form; NOT validated; NOT enforced at cart-time. |
| Per-customer uses cap | `maxused_user` | NOT shown; NOT validated; NOT enforced. |
| Force save bypass | `force_save` | NOT shown; NOT validated. |
| Region / geo-zone restriction | region keys | NOT shown; NOT validated. |
| Discount code | `code` | NOT shown; NOT validated (Quantity is always-automatic). |
| Code-apply stacking flag | `code_apply` | NOT shown; on for a discount saved from the admin form, and the cart reads it. See [[quantity-discount-stacking]]. |
| Apply on regular price | `apply_regular_price` | NOT shown; NOT validated. |

For the validated fields, see [[quantity-discount-form]].

## Plan gates

This feature is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `discount_quantity` | Numeric | Usage quota for Quantity discounts, compared only by the Admin GraphQL API's `createDiscount`. Usage counts discounts whether active or not; only deleting lowers it. The 12-tier cap for a one-variant product is UI-side, not plan-driven ([[quantity-discount-tier-evaluation]]). Extendable via feature pack. |
| `total_discounts` | Displayed figure | A count across all discount types; not enforced. |
| `discount_bogo`, `discount_volume` | Displayed only | No discount type behind them (**Buy X get Y** was removed on 2026-03-05); nothing checks them. |

Only creating is checked, on any path.

Numeric gates extend via packs ([[plan-vs-feature-pack]]); boolean / access gates require a plan upgrade.

## Business rules

### Counted statuses, `max_uses`, per-customer cap — NOT enforced

Unlike code-based discounts (Promo / Container / Code PRO), the Quantity-discount type does NOT count uses against `max_uses` or `maxused_user`. The form doesn't even show those fields (see [[quantity-discount-form]] for the omitted-fields catalogue). A Quantity tier applies on **every** qualifying cart-line, every time, until the discount is deactivated, expires, or its product is removed.

### Fields submitted but NOT validated

The quantity-specific validation path only validates `name`, `active`, `product_id`, and `conditions[]`. Every other field (see the Settings & fields table above) is skipped: not shown on the form, and if submitted via direct API call it is **stored** but **never enforced** at cart-time. The exception is `code_apply`, which the cart does read: see [[quantity-discount-stacking]].

### Programmatic access — NOT writable via JSON-API v2

Quantity discounts are **excluded from JSON-API v2 writes**. The validator allowlist on the `discounts` resource excludes Quantity. Attempted POST / PATCH against `/api/v2/discounts` with `type=quantity` is rejected.

Programmatic create / update / delete is possible **only** via:

1. **The Admin GraphQL API** ([[settings-pat-tokens]]) — `createDiscount` / `updateDiscount` / `discountsBulkDelete`, with a personal access token the store owner creates; per-variant tier prices included.
2. The admin panel.
3. A CloudCart staff member creating them on behalf of the merchant.

For integrators building bulk-tier-management tools, the Admin GraphQL API is the only programmatic option; it works with a personal access token, so it can be wired to a headless integration.

### Auto-disable on expiry — runs in UTC, not store timezone

An hourly background process switches a discount (Quantity included) off at the first run after 00:00 UTC on the day after its end date.

The timezone is **UTC**, NOT the store's timezone. For a Europe/Sofia store, a Quantity discount with `date_end = 2026-06-15` stays switched on for a few hours after the merchant's local end-of-day, until the first run after 00:00 UTC on 2026-06-16.

The cart-engine cart-time checks DO use store timezone at evaluation time, so the customer's cart stops applying the tier ladder at the expected local time — but the merchant's listing still shows the Quantity row as Active until the next UTC sweep runs.

This recurring process is part of [[background-queue-inventory]].

### Active switch

The Active switch takes effect immediately, any number of times. See [[quantity-discount-form]] for the activate / deactivate toggle behaviour.

### Webhooks

`discount.created` / `discount.updated` fire when the discount record is saved through the form. The Active switch, bulk status and list delete send none. See [[settings-hooks]] for the webhook subscriber configuration. Webhook receivers must be idempotent.

## Related

- [[marketing-discounts-quantity]] — hub.
- [[quantity-discount-form]] — confirms the un-validated fields are not rendered on the form.
- [[quantity-discount-stacking]] — what `code_apply` does to the tier price.
- [[quantity-discount-tier-evaluation]] — the 12-tier UI cap (not plan-driven).
- [[plan-gates]] — the cross-cutting plan-feature mechanism.
- [[plan-vs-feature-pack]] — how numeric gates extend via packs.
- [[plan-features]] — full inventory of plan-feature keys.
- [[json-api-v2]] — the API surface this discount type is excluded from.
- [[settings-hooks]] — webhook subscriber surface.
- [[background-queue-inventory]] — hourly auto-disable sweep.

## Open questions

None.
