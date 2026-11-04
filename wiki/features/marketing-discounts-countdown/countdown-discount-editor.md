---
type: feature
nav_path: "Marketing → Discounts → Countdown → Editor"
route_name: discounts-create
route_path: /admin/marketing/discounts/create/countdown
aliases: ["Countdown discount editor", "Countdown form", "Countdown create form"]
tags: [marketing, discounts, countdown, editor]
plan_gates: ["discount-countdown", "discount_global"]
created: 2026-06-10
updated: 2026-11-04
source_count: 2
---

> Part of [[marketing-discounts-countdown]]. See the hub for the other aspects (storefront popup + timer, eligibility, a second Countdown, cart totals + stacking, programmatic access).

# Countdown discount — editor (form + fields)

## Purpose

The Countdown editor is the admin form where the merchant configures a Countdown discount: the inner discount value (flat or percent), the target (**For every product in the cart** or **Orders over**), the per-customer-session timer length, the popup description HTML, and the celebration animation that plays once when the popup first fires at checkout.

## Where to find it

From [[marketing-discounts]], click **+ Add discount** → **Countdown discount** in the type-picker modal. The form opens at `/admin/marketing/discounts/create/countdown` (or `/admin/marketing/discounts/edit/{id}` when editing). Breadcrumb: **Marketing → Discounts → Create discount**. A second Countdown can be saved, but checkout uses only the first active one found — see [[countdown-discount-single-instance]].

## What the merchant can do here

- Pick **Fixed amount** (`flat`) or **Percentage** (`percent`) as the inner value type — Free shipping (`shipping`) is NOT offered as the inner type for Countdown.
- Enter the **discount value** (amount in store currency for flat, up to 100 in this form; 0-100 for percent).
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
- Set the **Discount name** (`name`) — internal label + customer-facing totals row label.
- Toggle the **Active** flag (`active`) — Active = the timer can fire; Inactive = configured but skipped.

### What the editor does NOT expose

- No Region / Geo zone block — Countdown applies regardless of shipping region.
- No Color settings, no "Discount amount in label" radio.
- No `code` field — Countdown is auto-applied.
- No **Save the discount on your order** switch.
- No `timer_in_listing` / `timer_in_details` switches — the countdown renders via the dedicated checkout popup, not the listing-timer overlay.

## Settings & fields

### General settings

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Discount status** | `active` | Active = timer eligible at checkout. Inactive = configured but skipped. | `yes` / `no`. |
| **Discount name** | `name` | Internal label + the totals row label customers see at checkout. | Required, max 191 chars. |
| **Discount type** | `type` | **Fixed amount** (`flat`) or **Percentage** (`percent`). The Countdown is stored as that type with timer settings. | One of `flat`, `percent`. |
| **Discount value** | `type_value` | The amount or percent the Countdown waives from the qualifying cart. | Required, numeric. Percent is limited to 100. The fixed-amount field stops at 100 in this form. |

### Discount target

| Value | Means | Required companion |
|-------|-------|--------------------|
| `all` ("For every product in the cart") | Any cart that passes other restrictions. Percent comes off once on the subtotal. A fixed amount is amount × total quantity when VAT applies to the cart, once otherwise. | — |
| `order_over` ("Orders over") | Products subtotal at or above `order_over`. One amount off. | `order_over` (amount in store currency). |

See [[discount-stacking-amount-by-target]] for the other discount types.

The Discount-target dropdown filters product / category / vendor / `category_vendor` / `selection` out for Countdown.

### Discount conditions (timer + popup)

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Display effect** | `countdown_popup_effect` | Animation that fires once on first popup view. | One of `confetti`, `fireworks`, `school_pride` (Parade), or null. |
| **Validity time** | `countdown_minutes` | Minutes the per-session timer runs from the first popup view. | Required integer. 0 saves, and the discount then does not behave as a Countdown. Stored as a discount `meta_data` entry. |
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
| **Discount available only to registered users** | `only_customer` | When ON, guests get no discount row. The popup still shows to them and their timer starts. |

Like Flat / Percent, the **"Registered users only"** block is shown only when the target is **"Orders over"** (`order_over`) — for "For every product in the cart" it is hidden. It defaults to **OFF** (`0`), so a Countdown on that target saves with guests included and the merchant never sees the toggle. (The save validator marks `only_customer` required, but the default `0` satisfies it.)

### Customer groups

| Field | Backend key | What it does |
|-------|-------------|--------------|
| **All groups** | `customer_groups_target` | `yes` = visible to all groups. `no` = restrict via `customer_groups[]`. |
| **Customer groups** | `customer_groups[]` | Array of [[customers-custom-groups]] ids. |

### Date range (no-timer variant)

| Field | Backend key | What it does |
|-------|-------------|--------------|
| **Start date** | `date_start` | When the Countdown becomes eligible. Required. |
| **End date** | `date_end` | When the Countdown stops being eligible. Nullable; cannot be before the start. Today and past dates save. |
| **No expiration** | `no_expire` | Clears `date_end`. |

### Saved payload shape

The save payload includes: `is_countdown: 1`, `countdown_discount: 1`, `type` (`flat` or `percent`), `type_value`, `settings` (`all` / `order_over`), `order_over` (when applicable), `countdown_minutes`, `countdown_description`, `countdown_popup_effect`, plus standard fields (`max_uses`, `maxused_user`, `customer_groups[]`, `customer_groups_target`, `only_customer`, `date_start`, `date_end`, `name`, `active`). The save creates the discount, then stores the three timer fields as `meta_data` entries.

## Business rules

- Saving a second Countdown is allowed — see [[countdown-discount-single-instance]].
- On create the form checks whether this kind of discount is enabled on the plan (`discount-countdown`). If not: HTTP 403 *"This feature is not enabled for your plan. To access it, please upgrade your plan."* The Countdown type-picker card is not greyed out (only the **Discount code** (PRO) card is plan-gated). See [[marketing-discounts]] → Plan gates.

## Related

- [[marketing-discounts-countdown]] — hub.
- [[marketing-discounts]] — parent feature.
- [[customers-custom-groups]] — customer-group picker contents.
- [[settings-statuses]] — `discounts_used_statuses` controls the counted statuses for uses.
- [[discount-stacking-amount-by-target]] — what each target's amount comes off.

## Open questions

None.
