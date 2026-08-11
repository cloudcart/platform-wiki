---
type: feature
nav_path: "Marketing → Discounts → Quantity → Form"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/quantity
aliases: ["Quantity discount form", "Volume discount form", "Quantity discount fields", "Quantity discount editor"]
tags: [marketing, discounts, quantity, form, validation]
plan_gates: ["discount_quantity"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-discounts-quantity]]. See the hub for the other aspects (tier evaluation, stacking, uniqueness constraint, plan gating, storefront display).

# Quantity discount — form layout, fields, validation

## Purpose

This aspect documents the **create / edit form** for a Quantity discount — which blocks render, every visible field with its backend key + validation, the activate-toggle behaviour, the delete-confirmation flow, and the deliberately-narrow set of fields the Quantity type **omits** versus the other discount types.

## Where to find it

Path:

- From [[marketing-discounts]] → **+ Add discount** → pick the **Quantity discount** card.
- The card routes to `discounts-create` with the URL `/admin/marketing-new/discounts/create/quantity` (`type` URL param `quantity` drives the layout).
- After save, the merchant lands on `/admin/marketing-new/discounts/edit/{id}` (same component, route-name `discounts-edit`).

The card's blurb on the type-picker modal reads:

> *"With this discount you can decrease a product's price based on the quantity added to the cart."*

## What the merchant can do here

The Quantity form is the narrowest of the discount types. Only four blocks render.

1. **General settings** — `active` switch + `name` input. No discount-type picker; type is implicit. No `type_value`.
2. **Discount conditions** — the quantity-configuration module:
   - **Customer buys** — single-product searchable picker (API: `/admin/api/core/products/search`).
   - **Tier rows** — Quantity input (unit "pcs.", min 0) + Unit price (currency, min 0) + remove-row X.
   - **+ Add new condition** — appears only when tier-list length `< 12`. Removing the last tier auto-inserts an empty replacement.
3. **Customer groups** — shared block (`All groups` switch + multi-pick on OFF).
4. **Date range** without timer fields — `date_start` + `date_end` + **No expiration** switch.

**Activate / deactivate row toggle** — inline list-row switch. The **10-minute activation cooldown does NOT apply** to Quantity; merchant can toggle as often as they like. The cooldown protects per-product attachment regeneration on Flat / Percent / Shipping / Fixed types; Quantity doesn't regenerate attachments.

**Delete confirmation** — generic table delete-confirm dialog → cascading delete of tier rows + customer_groups. See [[quantity-discount-uniqueness-constraint]].

## Settings & fields

### Top of form (always present)

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Discount status** | `active` | `yes` = evaluated at checkout, `no` = saved but skipped. | Required. |
| **Discount name** | `name` | Internal label visible in the list and reports. | Required. |

### Discount conditions box

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Customer buys** | `product_id` | The single product the discount targets (searchable picker). | Required; must exist in `products`; must not already be on another Quantity discount — see [[quantity-discount-uniqueness-constraint]]. |
| **Quantity** (per tier) | `conditions[].quantity` | Minimum cart-line quantity to unlock this tier. Integer in pieces. | Required, integer, min 0. **Note**: `0` rejected as empty — see [[quantity-discount-tier-evaluation]]. |
| **Unit price** (per tier) | `conditions[].discount_value` | The per-piece price the customer pays once cart-line quantity reaches this tier. Currency value. Stored as integer minor units (cents) — 10 EUR = 1000. | Required, numeric. `0` rejected as empty. |
| **+ Add new condition** | (UI control) | Appends an empty tier row. Hidden once 12 tiers exist. | — |
| **Remove tier** (trash icon) | (UI control) | Removes the tier. If the list becomes empty, a fresh blank tier is auto-inserted. | — |

### Customer groups

| Field | Backend key | What it does |
|-------|-------------|--------------|
| **Customer groups** | `customer_groups[]` | Allow-list of [[customers-custom-groups]]. Empty = "All groups" (guests get it via the store's default guest group). |

### Date range

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Date start** | `date_start` | First day the discount applies. | Required. |
| **Date end** | `date_end` | Last day the discount applies. | Required unless **No expiration** is on; must be after `date_start`. |
| **No expiration** | `no_expire` | Sets `date_end` to null — discount runs indefinitely. | Boolean. |

### Endpoints

| Action | Method | URL pattern |
|--------|--------|-------------|
| Load form (edit mode) | GET | `/admin/api/core/discounts/{id}` |
| Create | POST | `/admin/api/core/discounts/quantity` |
| Edit (update) | PATCH | `/admin/api/core/discounts/{id}/quantity` |
| Toggle status (list-level) | POST | shared `change-statuses` endpoint (see [[marketing-discounts]]) |
| Delete | DELETE | shared discounts destroy endpoint (see [[marketing-discounts]]) |

## Business rules

### Save flow

On submit, the discount is saved with `type = quantity`. The standard target-attachment step is skipped (no category/brand/collection targets). Every save fully replaces the tier list: prior tiers are cleared and one row is written per submitted tier. A `discount.created` / `discount.updated` event then fires (refreshes listings and smart collections, notifies webhooks — see [[settings-hooks]]).

### Per-row validator strings (verbatim)

- *"All conditions must be fulfilled"* — emitted when any tier has either `quantity` OR `discount_value` empty. BG: *"Всички условия трябва да се попълнят"*.
- *"Quantity is required"* — per-row error on `conditions[].quantity`.
- *"Discount value is required"* — per-row error on `conditions[].discount_value`.
- *"Product is already in use"* — form-validator on the `product_id` field when another Quantity discount targets the same product. See [[quantity-discount-uniqueness-constraint]].
- *"A volume discount with this product already exists"* — server-side error on save. BG: *"Вече съществува количествена отсъпка с този продукт"*.

### Fields the Quantity form does NOT render

Compared to other discount types, Quantity intentionally omits:

- **Discount target block** — no "Apply to category / brand / smart collection". Strictly one product per discount.
- **Regions / geo-zone block** — no audience filter beyond customer groups.
- **Discount limits block** — `max_uses` / `maxused_user` not shown; not validated. See [[quantity-discount-plan-gating]].
- **Color settings / banner / label color / "Discount amount in label" radio** — storefront renders the tier list itself.
- **Registered-users-only block**.
- **Code-generator helper / code field** — Quantity discounts are always automatic.
- **Timer-in-listing / timer-in-details switches** — no storefront countdown.
- **`force_save`** flag.
- **`code_apply`** checkbox — defaults to `0`; not merchant-tunable. See [[quantity-discount-stacking]].
- **`apply_regular_price`** flag.
- **Per-variant tier override** — tier price applies to every variant of the chosen product equally (compare [[marketing-discounts-fixed]]).
- **Per-tier customer-group** — the allow-list is on the parent Discount; all tiers share it.

### Tier price does not auto-adjust on catalog price changes

Unlike Fixed-discount per-variant rows (which auto-deactivate when catalog price drops at or below the fixed price), Quantity tier values are **independent** of catalog price. A "buy 5, pay 8 EUR" tier stays at 8 EUR even if the catalog price drops to 7 EUR — the tier would now be MORE expensive than catalog. The merchant must manually adjust tiers when changing catalog prices.

### `discount_value` is the replacement unit price, not an amount off

`discount_value` is **NOT** an amount off and **NOT** a percent off. The Quantity type is internally `fixed`: the platform replaces the cart-line price with this exact number per piece. Savings versus catalog are computed at cart-time. See [[quantity-discount-tier-evaluation]].

## Related

- [[marketing-discounts-quantity]] — hub.
- [[marketing-discounts]] — parent feature; shared list / change-statuses / delete endpoints.
- [[customers-custom-groups]] — `customer_groups[]` allow-list source.
- [[settings-hooks]] — `discount.created` / `discount.updated` / `discount.deleted` webhooks fire on save.

## Open questions

None.
