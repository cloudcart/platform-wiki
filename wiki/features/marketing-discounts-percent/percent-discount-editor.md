---
type: feature
nav_path: "Marketing → Discounts → Percent → Editor"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/global
aliases: ["Percent discount editor", "Percent discount form", "Discount with promo code form"]
tags: [marketing, discounts, percent, editor]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-discounts-percent]]. See the hub for the other aspects (fields, targeting, stacking, validity, plan gates, programmatic access).

# Percent discount — editor (form, sections, sub-flows)

## Purpose

The Percent editor is the admin form where the merchant configures a no-code or code-based Percent discount. It is the same `MarketingDiscountsCreateEditPage` used by Flat and Shipping discounts; what changes is which **entry-surface** card the merchant picked in the type-picker modal and whether the inner type dropdown is set to **Percentage**.

## Where to find it

From [[marketing-discounts]], click **+ Add discount** to open the type-picker modal. Two cards open the Percent editor:

- **Global discount** card → route `/admin/marketing-new/discounts/create/global` (route name `discounts-create`, query `type=global`). For a cart-wide no-code Percent.
- **Discount with promo code** card → route `/admin/marketing-new/discounts/create/code` (route name `discounts-create`, query `type=code`). For a promo-code-driven Percent. Adds the **Generate a discount code** + **Region** blocks.

Once on the form, the merchant sets **Discount type → Percentage** in the General settings block.

## What the merchant can do here

### Form sections (top-to-bottom)

The Percent form is composed of these sections (the "Global discount" type-picker card uses the layout below; the "Discount with promo code" card adds the code-generator and region blocks):

1. **General settings** — name, status (active/inactive), discount type (Fixed amount / Percentage / Free shipping), discount value (for Percentage, the percent as a whole number 0-100 — e.g. `15` for 15%, not `0.15`).
2. **Discount target** — pick where the discount applies (cart-wide, orders-over, specific products, category, vendor, smart collection, or category+vendor). See [[percent-discount-targeting]].
3. **Discount limits** — total uses and per-customer uses (only shown for `all` and `order_over` targets).
4. **Customer groups** — restrict to specific groups or "All groups".
5. **Registered users only** — restrict to logged-in customers (only shown for `order_over` target).
6. **Color settings** — background and text color for the discount label on storefront.
7. **Discount's amount in label** — a radio with **two** choices for what to display on the product label: "As percent" or "As fixed amount". For Percent, defaults to "As percent". (The backend also accepts `dont_change`, but it is not offered in this radio.)
8. **Date range** — start / end dates, or "No expiration".

For code-based variants, the form additionally shows:

- **Generate a discount code** — the code string, barcode mode (EAN-13 / EAN-8), `code_apply` ("Apply discount even if the cart contains products with a discount"), `apply_regular_price` ("Apply to the regular price of products, if this discount is greater").
- **Region (Geo zone)** — restrict to a specific shipping region or "Make it Global".

### Form sub-flows triggered by field choices

| Trigger | Sub-flow / visible block |
|---------|--------------------------|
| Picking **Discount target → Orders over** | Slides open: `order_over` currency input + *"Save the discount on your order"* switch (help: *"If the option is enabled and when editing an order that includes this discount and the conditions are not met, the discount will not be removed."*). |
| Picking **Discount target → Specific products** | Slides open: multi-pick product search (api `/admin/api/core/products`). |
| Picking **Discount target → Product category/categories** | Slides open: warning info-box (*"The discount will only be applied to the main product category"*) + multi-pick category search. |
| Picking **Discount target → Product vendor/s** | Slides open: multi-pick vendor search. |
| Picking **Discount target → Smart collection/s** | Slides open: multi-pick smart collection search. |
| Picking **Discount target → Category + vendor** | Slides open: same warning box + category multi-pick + vendor multi-pick. |
| Picking **Discount target ∈ {all, order_over}** | The **Discount limits** block becomes visible. Otherwise hidden. |
| Picking **Discount target = order_over** | The **Registered users only** block becomes visible. Otherwise hidden. |
| Toggling **Customer groups → All groups OFF** | Slides open: multi-pick customer-groups search (api `/admin/api/core/customers/groups`). |
| Toggling **Region → Make it Global OFF** (code variant only) | Slides open: single-pick geo-zone search (api `/admin/api/core/settings/geo-zones/search`). |
| Toggling **No expiration ON** | Wipes `date_end` and clears any date-end errors. |
| Toggling **Code format → Barcode EAN13** or **EAN8** | The free-text "Generate" button hides; the **"Use as barcode prefix"** switch appears below. |
| Toggling **code_apply ON** (in code variant) | The *"Apply to the regular price of products, if this discount is greater"* switch appears — see [[percent-discount-stacking]]. |

### Generate-code helper

Inside the code-variant form, the **Generate a discount code** field-block has the code-generator helper: a code-format dropdown + literal-code text input + a *Generate* button (visible only when format = "Code"). Clicking *Generate* writes a random 10-character uppercase alphanumeric string (from `ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`) into the code input.

### Activate / deactivate toggle

From the Discounts list, the merchant uses the row's **Active** switch to flip the discount on/off. For no-code Percent, the 10-minute cooldown per discount applies — switching too quickly returns a rate-limit error and reverts the toggle. See [[percent-discount-validity]] for the exact message + scope.

### Delete confirmation

The row's trash icon triggers the generic delete-confirmation dialog (*"Are you sure?"*), then the discount is removed. Cascading deletes wipe the discount's customer-groups, targets, and customers join rows.

## Settings & fields

The full field catalogue (every backend key, default, validation string) lives on [[percent-discount-fields]]. This page focuses on the section layout + sub-flow triggers.

## Business rules

- The **Discount type** dropdown's "Percentage" option creates a `type = percent` row regardless of which entry card was used (global or code). The only structural difference between the two surfaces is whether `code` is set on the row.
- The "Save the discount in the order" (`force_save`) switch is offered only for the `order_over` target — see [[percent-discount-targeting]].
- The 10-minute activation cooldown applies to **no-code** Percent only; code-based Percent has no cooldown. See [[percent-discount-validity]].

## Related

- [[marketing-discounts-percent]] — hub.
- [[marketing-discounts]] — parent feature; the type-picker modal lives there.
- [[percent-discount-fields]] — every field + validation rule.
- [[percent-discount-targeting]] — what each `settings` target does.
- [[percent-discount-stacking]] — `code_apply` + `apply_regular_price` semantics.
- [[percent-discount-validity]] — active-toggle cooldown + date rules.
- [[customers-custom-groups]] — customer-group picker contents.
- [[geo-zone]] — geo-zone picker contents (code variant).

## Open questions

None.
