---
type: feature
nav_path: "Orders → Order details → Discount → Add → Form"
route_name: admin.orders.discount.add
route_path: /admin/orders/action/discount/:order_id/add
aliases: ["Add discount modal", "Add discount form", "Order discount form fields", "Choose discount dropdown", "discount_variant field"]
tags: [orders, discount, smarty, form]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[orders-discount-add]]. See the hub for the other aspects (existing-discount eligibility, manual discounts, delete, recalculation, API).

# Order-level discount — the Add Discount form

## Purpose

The **field-level inventory of the Add Discount modal** — the single-form, progressive-reveal UI the merchant uses to attach an order-level discount. One primary dropdown chooses between an existing campaign and a one-off manual discount; the matching sub-form appears below.

## Where to find it

[[orders-details]] → **Discount action row** → **Add Discount** button (shown only when no order-level discount is applied). Opens a side-panel modal (`data-ajax-panel`). The whole modal is one `ajaxForm` posting to `admin.orders.discount.add`.

## What the merchant can do here

- Pick **Existing discount** or **Manual discount** from the primary dropdown.
- Fill the revealed sub-form (a discount target for existing; a type + amount for manual).
- Save → the form posts and the order summary, preview, and history panels reload.

## Settings & fields

### Primary choose-variant dropdown (always visible)

| Field | Element | Default | Options |
|-------|---------|---------|---------|
| **Choose discount** | Select2 dropdown (name `discount_variant`) | empty | `existing` ("Existing discount"), `manual` ("Manual discount"). |

Picking an option reveals the matching sub-form below; picking nothing hides everything and disables all sub-form selects. The dropdown is `data-no-input="true"` (typeahead disabled).

### "Existing discount" sub-form (revealed when `discount_variant = existing`)

| Field | Element | Default | Notes |
|-------|---------|---------|-------|
| **Choose target** | Select2 dropdown (name `discount_target_id`) | empty | Options come from the backend-pre-filtered `$discounts_targets` map keyed by `DiscountToTarget` id. Label format: discount name (+ code / barcode-prefix in parens when the discount has a code). |

If there are NO eligible existing discounts, an inline `alert-danger` shows instead of the dropdown: *"No discounts available"* (`order.err.no_discounts`). The eligibility filter that builds this list is documented on [[orders-discount-add-existing-eligibility]].

### "Manual discount" sub-form (revealed when `discount_variant = manual`)

| Field | Element | Default | Notes |
|-------|---------|---------|-------|
| **Discount type** | Select2 dropdown (name `type`, id `order_discount_type`) | **Percent** (selected) | Two options: `flat` ("Flat") OR `percent` ("Percent"). |
| **Discount amount** | Text input (name `type_value`) | empty | Dynamic mask: when type = Percent, percent-mask + `%` affix on the right. When type = Flat, currency-mask + currency symbol (position before / after per the site's `currency.position` setting). Switches live via jQuery `switchClass` + `App.initAjaxInputMasks` on type change. |

The default type is **Percent**, not Flat — the merchant must explicitly switch to Flat for currency-amount discounts. The detailed manual-discount validation (flat-less-than-subtotal, percent clamping) is on [[orders-discount-add-manual]].

### Submission validation (the request validator)

- `discount_variant` required, one of `existing` / `manual`.
- `discount_target_id` required when `variant = existing`.
- `type` required when `variant = manual`, one of `flat` / `percent`.
- Custom `type_value` validator: flat requires `value < order.price_subtotal` (error *"Flat discount must be less than order subtotal"*); percent requires a non-empty value. Either type rejects empty value with a type-specific message.

On success, the form fires `cc.ajax.reload` on `#order_preview`, `#order_summary`, and `#order_history`.

## Business rules

- **Progressive reveal** — sub-form selects stay disabled until the primary dropdown selects their variant, so the merchant cannot submit a half-filled form for the wrong path.
- **Dynamic mask on type change** — the amount input's mask (currency ↔ percent) and affix switch live via jQuery as the merchant flips the type dropdown; no page reload.
- **One form, one POST** — both paths post to the same `admin.orders.discount.add` route; the backend branches on `discount_variant`.
- **Add button visibility** — the button only renders when no order-level discount is currently applied; otherwise the row shows Remove instead (see [[orders-discount-add-delete]]).

## Related

- [[orders-discount-add]] — hub.
- [[orders-details]] — parent page (Discount action row).
- [[marketing-discounts]] — source of existing discounts shown in the picker.
- [[settings-general]] — `currency.position` drives the flat-amount mask affix side.
- [[order]] — entity page.

## Open questions

None.
