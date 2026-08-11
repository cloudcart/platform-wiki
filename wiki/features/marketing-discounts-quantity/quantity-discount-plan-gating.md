---
type: feature
nav_path: "Marketing → Discounts → Quantity → Plan gating"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/quantity
aliases: ["Quantity discount plan limit", "discount_quantity gate", "Quantity discount API access", "Quantity discount not supported by plan", "Quantity discount un-validated fields"]
tags: [marketing, discounts, quantity, plan-gates, json-api-v2, graphql]
plan_gates: ["discount_quantity", "total_discounts"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-discounts-quantity]]. See the hub for the other aspects (form, tier evaluation, stacking, uniqueness constraint, storefront display).

# Quantity discount — plan gating, API access, un-validated fields

## Purpose

This aspect documents:

1. The **plan-feature gates** that cap how many Quantity discounts a merchant can create.
2. The **programmatic-access surface** — Quantity discounts are excluded from JSON-API v2 writes; the only programmatic path is GraphQL.
3. The set of fields that are **submitted-but-NOT-validated** for the Quantity type (`max_uses`, `maxused_user`, `force_save`, region, code, `code_apply`).
4. The auto-disable sweep that runs daily in UTC.

## Where to find it

The `discount_quantity` plan limit is a **usage counter** (the "used / limit" figure), **not** a hard create-time block in the modern panel:

- **Discount-type picker** (when creating a new discount from [[marketing-discounts]]) — the **Quantity discount** card is **not** greyed out by the `discount_quantity` quota; it stays selectable. (Only the Discount code (PRO) card is plan-gated at create time — see [[marketing-discounts]] → Plan gates.)
- **Create endpoint** — creating a `quantity` discount in the modern panel is **not** rejected by the plan gate: the create-time gate keys on `discount-quantity` (hyphen), which does not resolve against the underscore-keyed `discount_quantity` quota, so the gate passes through.
- **JSON-API v2** — POST / PATCH against `/api/v2/discounts` with `type=quantity` IS rejected at the resource validator — but as a **type restriction** (Quantity is excluded from the v2 writable allowlist), not a plan gate.

## What the merchant can do here

The merchant cannot raise the quota from this screen — the controls are at the plan / feature-pack level (see [[plan-vs-feature-pack]]). To raise the `discount_quantity` usage quota:

- **Upgrade to a plan that includes `discount_quantity`** (or a higher numeric cap).
- **Buy a feature pack** that extends `discount_quantity` (numeric gates extend via packs).
- **Delete unused Quantity discounts** (deactivation alone keeps the slot held — see [[quantity-discount-uniqueness-constraint]]).
- **For programmatic access**, use GraphQL `createDiscount` / `updateDiscount` with **admin-session auth** instead of JSON-API v2 with API token (Quantity is excluded from the JSON-API v2 writable allowlist).

## Settings & fields

The plan-gating aspect has no merchant-tunable fields on the Quantity form. The fields below are submitted in the API request body but **NOT validated or enforced** for Quantity-type discounts (the type-specific validator path only validates `name`, `active`, `product_id`, `conditions[]`):

| Field | Backend key | Status for Quantity type |
|-------|-------------|--------------------------|
| Total uses cap | `max_uses` | NOT shown on form; NOT validated; NOT enforced at cart-time. |
| Per-customer uses cap | `maxused_user` | NOT shown; NOT validated; NOT enforced. |
| Force save bypass | `force_save` | NOT shown; NOT validated. |
| Region / geo-zone restriction | region keys | NOT shown; NOT validated. |
| Discount code | `code` | NOT shown; NOT validated (Quantity is always-automatic). |
| Code-apply stacking flag | `code_apply` | NOT shown; defaults to `0`. See [[quantity-discount-stacking]]. |
| Apply on regular price | `apply_regular_price` | NOT shown; NOT validated. |

For the validated fields, see [[quantity-discount-form]].

## Plan gates

This feature is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `discount_quantity` | Numeric + Access | Per-plan cap for Quantity (volume / BOGO) discounts. Lower plans cannot pick the Quantity discount type from the type-picker — the card shows *"Not supported by plan"* and is disabled. Access route: `discounts/add/quantity`. Each Quantity discount can have up to 12 tiers (cap is UI-side, not plan-driven — see [[quantity-discount-tier-evaluation]]). Extendable via feature pack. |
| `total_discounts` | Numeric (aggregate) | Aggregate cap across all discount types — Quantity discounts also count toward this global ceiling. |

When over the cap or below the access tier, the create endpoint returns **HTTP 403 Forbidden** with *"Not supported by plan"* and the list of plans that allow additional capacity. The type-picker modal grays out the *Quantity discount* card with the same upgrade prompt.

Numeric gates extend via packs ([[plan-vs-feature-pack]]); boolean / access gates require a plan upgrade.

## Business rules

### Counted statuses, `max_uses`, per-customer cap — NOT enforced

Unlike code-based discounts (Promo / Container / Code PRO), the Quantity-discount type does NOT count uses against `max_uses` or `maxused_user`. The form doesn't even show those fields (see [[quantity-discount-form]] for the omitted-fields catalogue). A Quantity tier applies on **every** qualifying cart-line, every time, until the discount is deactivated, expires, or its product is removed.

### Fields submitted but NOT validated

The quantity-specific validation path only validates `name`, `active`, `product_id`, and `conditions[]`. Every other field (see the Settings & fields table above) is skipped: not shown on the form, and if submitted via direct API call it is **stored** but **never enforced** at cart-time. This is most-noticed for `code_apply`: see [[quantity-discount-stacking]] for the "dormant `code_apply` branch" detail.

### Programmatic access — NOT writable via JSON-API v2

Quantity discounts are **excluded from JSON-API v2 writes**. The validator allowlist on the `discounts` resource excludes Quantity. Attempted POST / PATCH against `/api/v2/discounts` with `type=quantity` is rejected.

Programmatic create / update / delete is possible **only** via:

1. **GraphQL** `createDiscount` / `updateDiscount` mutations with **admin-session authentication** (NOT API-token authentication — the mutations are gated to admin sessions).
2. The admin panel.
3. A CloudCart staff member creating them on behalf of the merchant.

For integrators building bulk-tier-management tools, the GraphQL path is the only programmatic option — and the admin-session requirement means it can't be wired to a typical headless integration that uses API tokens.

### Auto-disable on expiry — runs in UTC, not store timezone

A daily background process toggles `active = no` for any discount (Quantity included) whose `date_end` is at least 1 day in the past in **UTC**.

The timezone is **UTC**, NOT the store's timezone. For a Europe/Sofia store, a Quantity discount with `date_end = 2026-06-15` may remain technically "active" for up to ~27 hours after the merchant's local end-of-day before the UTC sweep flips the flag.

The cart-engine cart-time checks DO use store timezone at evaluation time, so the customer's cart stops applying the tier ladder at the expected local time — but the merchant's listing still shows the Quantity row as Active until the next UTC sweep runs.

This recurring process is part of [[background-queue-inventory]].

### No activation cooldown for Quantity

Unlike no-code Flat / Percent / Shipping / Fixed discounts (which have a 10-minute throttle on the active toggle), Quantity discounts can be toggled instantly as many times as the merchant likes. The cooldown does not apply because Quantity discounts don't trigger the per-product attachment regeneration that the cooldown protects. See [[quantity-discount-form]] for the activate / deactivate toggle behaviour.

### Webhooks fire on save

`discount.created` / `discount.updated` / `discount.deleted` webhooks fire on every successful Quantity-discount save and delete — same as all other discount types. See [[settings-hooks]] for the webhook subscriber configuration. Webhook receivers must be idempotent; they get one event per save, regardless of whether the tier ladder actually changed.

## Related

- [[marketing-discounts-quantity]] — hub.
- [[quantity-discount-form]] — confirms the un-validated fields are not rendered on the form.
- [[quantity-discount-stacking]] — the `code_apply` dormant-branch detail.
- [[quantity-discount-tier-evaluation]] — the 12-tier UI cap (not plan-driven).
- [[plan-gates]] — the cross-cutting plan-feature mechanism.
- [[plan-vs-feature-pack]] — how numeric gates extend via packs.
- [[plan-features]] — full inventory of plan-feature keys.
- [[json-api-v2]] — the API surface this discount type is excluded from.
- [[settings-hooks]] — webhook subscriber surface.
- [[background-queue-inventory]] — daily auto-disable sweep.

## Open questions

None.
