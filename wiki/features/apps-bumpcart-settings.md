---
type: feature
nav_path: "Apps → Bump Cart → Settings"
route_name: apps.bumper_offer.settings
route_path: /admin/apps/bumpcart/settings
aliases: ["Bump Cart Settings", "Bumper Offer Settings", "Bumpcart config"]
tags: [apps, marketing, bumpcart, settings, conversion]
plan_gates: []
created: 2026-05-21
updated: 2026-05-28
source_count: 2
---
# Bump Cart → Settings

## Purpose

The **Settings** tab is where the merchant configures the **goal type + target + bumper products** for the Bump Cart module. See [[apps-bumpcart]] for the full feature set.

## Where to find it

Sidebar → Apps → Bump Cart → **Settings tab**. Route: `/admin/apps/bumpcart/settings`.

## What the merchant can do here

### Goal selector + target fields (per `settings-keys`)

Per [[apps-bumpcart]] settings keys: `['goal', 'total_cart_amount', 'shipping_discount_id', 'discount_id', 'title']`.

The merchant picks ONE goal type:

| Goal (`goal` value) | Required fields |
|---|---|
| **amount_cart** | `options_addon.checkout_min_price` — cart-min threshold. |
| **total_cart** | `total_cart_amount` — target value to motivate cart total toward. |
| **free_shipping** | `shipping_discount_id` — references a free-shipping discount in [[marketing-discounts]]. |
| **discount** | `discount_id` — references a target discount. |

### Title + message

| Field | Notes |
|---|---|
| **Title** (`title`) | Module headline ("Spend X more for Y"). |
| **Bumper products** | Products auto-suggested / auto-added when goal is close. |

### Preview

The Settings page has a `preview_settings` slot showing what the customer will see at cart — goal label, current value vs target, etc.

### What the merchant CANNOT do here
- Run multiple bumpers simultaneously (single module per store).
- Use a goal type not in the predefined list.

## Settings & fields

Per [[apps-bumpcart]] saved configuration:
- `goal` — goal-type enum.
- `total_cart_amount` — for total_cart goal.
- `shipping_discount_id` — for free_shipping goal.
- `discount_id` — for discount goal.
- `title` — customer-facing headline.
- `options_addon.checkout_min_price` — for amount_cart goal.

## Business rules

### Goal-dependent field visibility

Fields show / hide based on the selected goal. Only the relevant field for the chosen goal is editable.

### References to discounts

For free_shipping + discount goals, the merchant must have a corresponding discount in [[marketing-discounts]] first. The referenced discount becomes the goal target.

### Permission
Standard apps permission scope.

## Related

- [[apps-bumpcart]] — hub with full feature set + business rules.
- [[marketing-discounts]] — discounts referenced by goals.
- [[products-products]] — bumper products picked from catalog.

## How it works (verified against backend)

### Bumper products are SUGGESTED, not auto-added

The bumper module always SHOWS suggested products with their own Add-to-cart affordance — there is no auto-add to the customer's cart. The merchant configures WHICH products are suggested via the `filter_group` setting (per [[apps-bumpcart]]). See [[apps-bumpcart]] § "Bumper products are SUGGESTED, not auto-added".

### Single goal per app instance — no multi-goal chaining

Only one goal can be active at a time. The merchant cannot configure goal A → goal B chaining (e.g., reach 50 BGN unlocks free shipping → then reach 100 BGN unlocks 10% off). To approximate this, the merchant should use [[apps-cart-rules]] which supports multiple rows with chained motivational messages.

### Settings keys saved by this page

Per Vue settings keys: `['goal', 'total_cart_amount', 'shipping_discount_id', 'discount_id', 'title']` plus per-goal extras (`filter_group`, `filter_group_value`, `sort_by`, `percent`, `showed`, optional `button_status` / `button_title` / `button_url`).

### Free-shipping / discount goal — requires existing discount

For `free_shipping` and `discount` goals, the picker only shows discounts that match the goal type:
- **Free shipping**: only discounts where `type = 'shipping'`. The merchant sees a warning *"You have not created discounts for free shipping."* when the list is empty.
- **Discount**: only discounts where `type` is `percent` or `flat`. Same warning pattern.

If the merchant hasn't created the corresponding discount in [[marketing-discounts]] first, the page shows the warning and the goal cannot be saved.

### Minimum cart amount warning

For `amount_cart` goal: if the storewide `options_addon.checkout_min_price` is 0, the page shows a warning *"You didn't set a Minimum amount for an order."* — the goal won't fire because there's no threshold to motivate toward. The merchant must set the minimum cart amount in [[settings-cart]] first.

### Three settings boxes, three edit-styles

The Settings page is laid out as **three independent box rows** with different open/close styles:

| Box | Title | Edit method | Keys saved by this row |
|---|---|---|---|
| **Target** | "Target" | `slide` (slide-down inline) | `goal`, `total_cart_amount`, `shipping_discount_id`, `discount_id`, `title` |
| **Action** | "Action" | `panel` (full-width drawer) | `filter_group`, `filter_group_value`, `show_products`, `sort_by`, `percent`, `showed` |
| **Show button** | "Show button" | `inline` (inline edit, no panel) | `button_status`, `button_title`, `button_url` |

Each box has its own Edit / Save controls and its own preview-summary section that shows the chosen values without opening the editor. The page emits a `disableSave` event up to its parent app-settings wrapper when any of the inline editors is open — preventing the top-level Save from firing while one row is still being edited.

### Action box — bumper product picker

The Action box exposes a dependent picker for **filter_group**:
- `category` → `filter_group_value` becomes a tags-mode select wired to `/admin/api/core/product-categories/search`.
- `vendor` → tags-mode select wired to `/admin/api/core/vendors/search`.
- `product` → tags-mode select wired to `/admin/api/core/products/search`.
- `related` → no `filter_group_value` shown (uses the related-products module settings).

Alongside `filter_group_value`, the merchant configures:
- **Filter by** (`show_products`) — tags-mode multi-select of `all` / `new` / `featured` / `sale` (OR-logic).
- **Sort by** (`sort_by`) — single-select: `price-high` (default) / `price-low` / `date` / `rating` / `comments` / `orders`.
- **Amount to reach goal + X in %** (`percent`) — integer with `%` suffix and tooltip explaining the uplift math (10 BGN gap × 50% = show products up to 15 BGN).
- **Show maximum products** (`showed`) — integer 0–100.

### Show button box — fallback CTA

When the chosen `filter_group` yields zero products, the storefront still shows a fallback button if `button_status = 1`:

| Field | Type | Notes |
|---|---|---|
| `button_status` | switch (0/1) | Shows the fallback button when no products match. |
| `button_title` | string | Button text (visible when `button_status = 1`). |
| `button_url` | url | Where the button leads (visible when `button_status = 1`). |

Both `button_title` and `button_url` are only rendered when the switch is ON.

### Storefront variable tokens in the Title

The Title field supports two placeholders that the storefront substitutes at render time:
- `{$remaining}` — amount left until the goal is reached.
- `{$target}` — the goal text (the chosen Minimum amount / % discount / Free shipping label).

The placeholder for new titles defaults to "You have {$remaining} left until the {$target} discount."

### "Related products not activated" warning

If the merchant picks `filter_group = related` but Related Products is OFF in the storefront's module settings, the page shows a link-warning: *"Related products not activated. You can activate it from [here]"* pointing at `/admin/storefront/widgets#tab-store`. Without the module active, the bumper picker has no related-products dataset to pull from.

## Open questions

(none — feature behaviour is fully characterised in [[apps-bumpcart]]'s "How it works" section.)
