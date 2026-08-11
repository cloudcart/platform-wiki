---
type: feature
nav_path: "Marketing → Discounts → Flat → Form & entry surfaces"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/global
aliases: ["Flat discount form", "Create flat discount", "Flat discount type-picker", "Discount with code card", "Flat discount sub-flows", "Flat discount code generator", "Flat discount label color"]
tags: [marketing, discounts, flat, form, entry-surface]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-discounts-flat]]. See the hub for the other aspects (targeting, value mechanics, eligibility, stacking, programmatic access).

# Flat discount — form & entry surfaces

## Purpose

This page documents **how the merchant reaches the Flat discount form and what blocks the form contains** — the two type-picker entry cards (Discount vs Discount with code), the layout of the create / edit page, the sliding sub-forms that show / hide based on selections, the Generate-code helper, and the row-level activate / delete actions.

Tickets that land here: *"where do I create a flat-amount discount?"*, *"how do I generate a random code?"*, *"why does the customer-groups picker not appear?"*, *"how do I change the label color on storefront?"*.

## Where to find it

From the [[marketing-discounts]] list, click **+ Add discount**. The type-picker modal shows ten cards.

- For a **no-code, cart-wide Flat discount**: click the **Discount** card → `discounts-create` with `type=global` → `/admin/marketing-new/discounts/create/global`. Set *Discount type* to **Fixed amount**.
- For a **code-driven Flat discount**: click the **Discount with code** card → `discounts-create` with `type=code` → `/admin/marketing-new/discounts/create/code`. The form gains the **Generate a discount code** and **Region** blocks.

Both create the same `flat` discount — the only difference is whether `code` is set. The list-view label summarises the target (e.g., "10 EUR off orders over 50 EUR").

## What the merchant can do here

- Pick between **Discount** (no-code) and **Discount with code** entry cards.
- Set the **General settings** block: name, status, discount type, value.
- Choose a **Discount target** and configure the matching sub-form.
- Set **Discount limits** (when applicable).
- Restrict to **Customer groups** or all groups.
- Restrict to **Registered users** (when applicable).
- Configure **Color settings** for the storefront label.
- Choose how the discount's amount is displayed in the storefront label.
- Set a **Date range** (with or without expiration).
- For code variants: run the **Generate-code helper** and pick a **Region**.
- Toggle **Active / Inactive** on the list row (10-min cooldown — see [[flat-discount-eligibility]]).
- Delete a Flat discount via the row trash icon.

## Settings & fields

### Form blocks (Flat layout)

The "Discount" card uses the layout below; the "Discount with code" card adds the code-generator and region blocks:

1. **General settings** — name, status (active/inactive), discount type (Fixed amount / Percentage / Free shipping), discount value (the amount).
2. **Discount target** — pick where the discount applies (cart-wide, orders-over, specific products, category, vendor, smart collection, or category+vendor) — see [[flat-discount-targeting]].
3. **Discount limits** — total uses and per-customer uses (only shown for `all` and `order_over` targets) — see [[flat-discount-eligibility]].
4. **Customer groups** — restrict to specific groups or "All groups" — see [[flat-discount-eligibility]].
5. **Registered users only** — restrict to logged-in customers (only shown for `order_over` target) — see [[flat-discount-eligibility]].
6. **Color settings** — background and text color for the discount label on storefront.
7. **Discount's amount in label** — what to display on the product label: "As percent", "As fixed amount", or "Don't change". For Flat, defaults to "As fixed amount".
8. **Date range** — start / end dates, or "No expiration" — see [[flat-discount-eligibility]].

For **code-based** variants, the form additionally shows:

- **Generate a discount code** — the code string, barcode mode (EAN-13 / EAN-8), `code_apply`, `apply_regular_price`. See [[flat-discount-stacking]].
- **Region (Geo zone)** — restrict to a specific shipping region or "Make it Global". See [[flat-discount-eligibility]].

### Color & label appearance

| Field | Backend key | What it does |
|-------|-------------|--------------|
| **Background color** | `color` | Hex color for the discount badge / label on storefront. |
| **Text color** | `text_color` | Hex color for the label text. |
| **Show discount amount in label as** | `discount_amount_type_in_label` | `in_percent`, `in_flat`, or `dont_change`. Defaults to `in_flat` for Flat-type discounts. |

### Sliding sub-forms on the Flat edit page

| Trigger | Sliding sub-form / visible block |
|---------|-----------------------------------|
| **Discount target → Orders over** | Currency amount input + *"Save the discount on your order"* switch. |
| **Discount target → Specific products** | Multi-pick product search. |
| **Discount target → Product category/categories** | Warning info-box + multi-pick category search. |
| **Discount target → Product vendor/s** | Multi-pick vendor search. |
| **Discount target → Smart collection/s** | Multi-pick smart collection search. |
| **Discount target → Category + vendor** | Warning box + category + vendor multi-picks. |
| **Discount target ∈ {all, order_over}** | Discount-limits block visible. |
| **Discount target = order_over** | Registered users only block visible. |
| **Customer groups → All groups OFF** | Customer-groups multi-pick visible. |
| **Region → Make it Global OFF** (code variant) | Geo-zone single-pick visible. |
| **No expiration ON** | `date_end` wiped. |
| **Code format → Barcode EAN13/EAN8** | "Use as barcode prefix" switch appears; Generate button hidden. |
| **code_apply ON** (code variant) | `apply_regular_price` switch appears. |

## Business rules

### Two entry surfaces — same `flat` discount

The **Discount** card (`type=global`) has no `code` field and no Region block. The **Discount with code** card (`type=code`) adds the **Generate a discount code** block, the **Region** block (`geo_zone_id` + "Make it Global" toggle), and the `code_apply` + `apply_regular_price` toggles (rules on [[flat-discount-stacking]]). Everything else (target sub-forms, limits, customer groups, dates, color) is identical between the two.

### Generate-code helper

The **Generate a discount code** block has a code-format dropdown (Code / Barcode EAN13 / Barcode EAN8) + code input + *Generate* button (visible only for "Code"). Generate writes a **random 10-char uppercase alphanumeric string** into the code input.

When the format switches to Barcode EAN13 / EAN8, the Generate button hides (codes are scanned, not generated) and a **"Use as barcode prefix"** switch appears — when ON, the scanned value is matched as `code` + scanned-suffix.

### Activate / deactivate row toggle

Inline switch on the list row. The 10-minute cooldown per discount applies (see [[flat-discount-eligibility]]); bad-window toggles return the cooldown error and the switch reverts.

### Delete

Row trash icon triggers a confirm dialog. Deleting also removes the discount's customer-group, target, and customer restrictions.

### General-settings fields

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Discount status** | `active` | Active = fires at checkout. Inactive = configured but skipped. | `yes` / `no`. |
| **Discount name** | `name` | Merchant-facing label. | Required, max 191 chars. *"The discount name must not be more than 191 characters"* / *"The discount name is required"*. |
| **Discount type** | `type` | Set to **Fixed amount** = `flat`. | Required, in `flat,percent,shipping,fixed,quantity,countdown,code-pro`. *"The selected type is invalid"*. |
| **Discount value** | `type_value` | The currency amount subtracted from the cart (or target subtotal). Entered in EUR; stored as cents. | Required when type=flat. *"The field 'amount' can not be empty"*. See [[flat-discount-value-mechanics]] for the amount-cap nuance. |

## Related

- [[marketing-discounts-flat]] — hub.
- [[flat-discount-targeting]] — what each Discount target sub-form does.
- [[flat-discount-value-mechanics]] — `type_value` cents storage + amount validator nuance.
- [[flat-discount-eligibility]] — date range, customer groups, region, limits, activation cooldown.
- [[flat-discount-stacking]] — `code_apply` / `apply_regular_price` rules on the code-variant form.
- [[marketing-discounts]] — Discounts list view.

## Open questions

None.
