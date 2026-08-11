---
type: feature
nav_path: "Marketing → Discounts → Countdown → Editor"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/countdown
aliases: ["Countdown discount editor", "Countdown form", "Countdown create form"]
tags: [marketing, discounts, countdown, editor]
plan_gates: ["discount_global", "total_discounts"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-discounts-countdown]]. See the hub for the other aspects (storefront popup + timer, eligibility, single-instance rule, cart totals + stacking, programmatic access).

# Countdown discount — editor (form + fields)

## Purpose

The Countdown editor is the admin form where the merchant configures the single Countdown discount per store: the inner discount value (flat or percent), the target (whole cart or `order_over` threshold), the per-customer-session timer length, the popup description HTML, and the celebration animation that plays once when the popup first fires at checkout.

## Where to find it

From [[marketing-discounts]], click **+ Add discount** → **Countdown discount** in the type-picker modal. The form opens at `/admin/marketing-new/discounts/create/countdown` (or `/admin/marketing-new/discounts/edit/{id}` when editing the existing one). Breadcrumb: **Marketing → Discounts → Create discount**. If a Countdown already exists (even inactive), the save fails — see [[countdown-discount-single-instance]].

## What the merchant can do here

- Pick **Fixed amount** (`flat`) or **Percentage** (`percent`) as the inner value type — Free shipping (`shipping`) is NOT offered as the inner type for Countdown.
- Enter the **discount value** (amount in store currency for flat, 0-100 for percent).
- Pick a target: **For every product in the cart** (`all`) or **Orders over** (`order_over`). No products / categories / vendors / smart collections / selections.
- Set **Validity time** in minutes (`countdown_minutes`) — the per-session window the customer has.
- Write the **Description** (`countdown_description`) in a WYSIWYG editor — appears inside the checkout popup.
- Pick a **Display effect** (`countdown_popup_effect`) — `confetti`, `fireworks`, or `school_pride` (Parade); nullable.
- Click **Preview** to play the chosen animation inline in the admin form before saving.
- Set **Maximum total uses** (`max_uses`) and **Maximum uses per customer** (`maxused_user`); unlimited via NULL.
- Restrict to **Registered users only** (`only_customer`) — shown only when target = "Orders over"; defaults to OFF.
- Restrict to selected **Customer groups** (`customer_groups[]`) when `customer_groups_target = no`.
- Set **Start date** / **End date** (`date_start` / `date_end`) — the no-timer date-range block (no time-of-day picker).
- Toggle **No expiration** (`no_expire`) to clear `date_end`.
- Toggle **Save the discount on your order** (`force_save`) when the target is `order_over`.
- Set the **Discount name** (`name`) — internal label + customer-facing totals row label.
- Toggle the **Active** flag (`active`) — Active = the timer can fire; Inactive = configured but skipped.

### What the editor does NOT expose

- No Region / Geo zone block — Countdown applies regardless of shipping region.
- No Color settings, no "Discount amount in label" radio.
- No `code` field — Countdown is auto-applied.
- No `timer_in_listing` / `timer_in_details` switches — the countdown renders via the dedicated checkout popup, not the listing-timer overlay.

## Settings & fields

### General settings

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Discount status** | `active` | Active = timer eligible at checkout. Inactive = configured but skipped. | `yes` / `no`. |
| **Discount name** | `name` | Internal label + the totals row label customers see at checkout. | Required, max 191 chars. |
| **Stored discount type** | `type` | Always stored as `type = 'countdown'`. The flat-vs-percent **inner mode** is NOT carried on the `type` column for Countdown rows. | The Countdown save validator's rules do NOT include a `type` field at all — the row is identified by `countdown_discount = 1` and `type` is set to `'countdown'` server-side. |
| **Discount value** | `type_value` | The amount or percent the Countdown waives from the qualifying cart. | Required, numeric. The standard `type_value` cap-by-inner-type checks (100,000 cents cap for flat, ≤ 100% for percent) do NOT fire for Countdown because the validator branches on `input('type')`, which is `'countdown'` — sanity-check manually `(verify)`. |

### Discount target

| Value | Means | Required companion |
|-------|-------|--------------------|
| `all` | Apply to any cart that passes other restrictions. | — |
| `order_over` | Cart subtotal ≥ `order_over` (the calculation may exclude shipping). | `order_over` (amount in store currency) + `force_save` flag. |

The Discount-target dropdown filters product / category / vendor / `category_vendor` / `selection` out for Countdown.

### Discount conditions (timer + popup)

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Display effect** | `countdown_popup_effect` | Animation that fires once on first popup view. | One of `confetti`, `fireworks`, `school_pride` (Parade), or null. |
| **Validity time** | `countdown_minutes` | Minutes the per-session timer runs from the first popup view. | Required integer > 0. Stored as a discount `meta_data` entry. |
| **Description** | `countdown_description` | HTML shown inside the popup modal at checkout. | Free string; WYSIWYG; supports basic HTML. Stored as a discount `meta_data` entry. |

The Display effect block includes a **Preview** button — disabled until an effect is picked; clicking replays the chosen vue-rewards animation in-page.

### Discount limits

| Field | Backend key | Validation |
|-------|-------------|------------|
| **Maximum total uses** | `max_uses` | Integer 1-100,000. NULL = unlimited. Counted on orders reaching the configured `discounts_used_statuses` (default: `paid`, `completed`, `fulfilled`) — see [[settings-statuses]]. |
| **Maximum uses per customer** | `maxused_user` | Integer 1-100,000. NULL = unlimited. |

### Registered users only

| Field | Backend key | What it does |
|-------|-------------|--------------|
| **Discount available only to registered users** | `only_customer` | When ON, guests are excluded; the popup will not fire on guest carts. |

Like Flat / Percent, the **"Registered users only"** block is shown only when the target is **"Orders over"** (`order_over`) — for "For every product in the cart" it is hidden. It defaults to **OFF** (`0`), so a whole-cart Countdown saves with guests included and the merchant never sees the toggle. (The save validator marks `only_customer` required, but the default `0` satisfies it.)

### Customer groups

| Field | Backend key | What it does |
|-------|-------------|--------------|
| **All groups** | `customer_groups_target` | `yes` = visible to all groups. `no` = restrict via `customer_groups[]`. |
| **Customer groups** | `customer_groups[]` | Array of [[customers-custom-groups]] ids. |

### Date range (no-timer variant)

| Field | Backend key | What it does |
|-------|-------------|--------------|
| **Start date** | `date_start` | When the Countdown becomes eligible. Required. |
| **End date** | `date_end` | When the Countdown stops being eligible. Nullable; end must be after start. |
| **No expiration** | `no_expire` | Clears `date_end`. |

### Force-save (visible only for `order_over`)

| Field | Backend key | What it does |
|-------|-------------|--------------|
| **Save the discount on your order** | `force_save` | An admin-edited order keeps the Countdown discount even if the edited cart drops below the `order_over` threshold. |

### Saved payload shape

The save payload includes: `is_countdown: 1`, `countdown_discount: 1`, `type`, `type_value`, `settings` (`all` / `order_over`), `order_over` (when applicable), `force_save`, `countdown_minutes`, `countdown_description`, `countdown_popup_effect`, plus standard fields (`max_uses`, `maxused_user`, `customer_groups[]`, `customer_groups_target`, `only_customer`, `date_start`, `date_end`, `name`, `active`). The save creates the Discount row, then stores the three timer fields as `meta_data` entries.

## Business rules

- The form's save validator runs the **uniqueness check** before commit — see [[countdown-discount-single-instance]].
- There is **no** create-time plan gate on Countdown in the modern panel — no `discount_countdown` plan-feature mapping exists, and the Countdown type-picker card is not greyed out (only the **Discount code** (PRO) card is plan-gated). See [[marketing-discounts]] → Plan gates.
- `force_save` is stored even when target = `all`, but is meaningful only for `order_over`.

## Related

- [[marketing-discounts-countdown]] — hub.
- [[marketing-discounts]] — parent feature.
- [[customers-custom-groups]] — customer-group picker contents.
- [[settings-statuses]] — `discounts_used_statuses` controls the counted statuses for uses.

## Open questions

- Confirm whether the `type_value` cap-by-inner-type rules (flat-100,000-cents cap, percent ≤ 100) really skip for Countdown, or whether a separate validator covers them `(verify)`.
