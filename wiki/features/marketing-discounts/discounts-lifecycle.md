---
type: feature
nav_path: "Marketing → Discounts → Lifecycle"
route_name: ""
route_path: ""
aliases: ["Discount lifecycle", "Discount scheduling", "Discount start date", "Discount end date", "No expiration", "Auto-disable expired discounts", "Discount activation cooldown", "Discount status toggle", "Жизнен цикъл на отстъпки", "Активиране на отстъпка", "Изтичане на отстъпка"]
tags: [marketing, discounts, promotions, lifecycle, scheduling]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Discount lifecycle, scheduling & activation

> Part of [[marketing-discounts]]. See the hub for the other cross-cutting aspects (eligibility, tax/VAT, storefront display, audit trail, known issues) plus per-type details.

## Purpose

This aspect covers **when** a discount can fire: its `active` flag, its `date_start` / `date_end` window, the **"No expiration"** toggle, the **hourly background sweep** that auto-disables expired discounts, the **10-minute activation cooldown** that throttles toggle thrashing, and the **"Latest update" badge** that surfaces background-regeneration delay. The date window and the hourly auto-disable sweep apply to **every** discount type; the **10-minute activation cooldown** applies **only to no-code Flat / Percent / Shipping / Fixed** discounts (see that section below).

## Where to find it

**Sidebar → Marketing → Discounts → row toggle / Edit form → Date range block.** The activation switch is the per-row toggle on the list (`/admin/marketing-new/discounts`). The date window is configured in the **Date range** block of the create/edit form for every type.

## What the merchant can do here

- Schedule a discount to start on a future date — it stays `active = yes` but is **skipped at checkout** until `date_start` arrives.
- Schedule a discount to end automatically — set a `date_end` and the hourly sweep auto-deactivates it once the cutoff passes.
- Run an open-ended discount — toggle **"No expiration"** to clear `date_end`.
- Toggle a discount on/off mid-window via the row switch (rate-limited).
- Bulk activate / deactivate multiple discounts via the table action bar.
- Render a countdown timer on storefront listings + product detail pages (per-type — see [[marketing-discounts-countdown]] and the per-Date-range timer switches on [[marketing-discounts-flat]] / [[marketing-discounts-percent]] / [[marketing-discounts-shipping]]).

## Settings & fields

| Field / Control | Backend key | What it does | Validation |
|-----------------|-------------|--------------|------------|
| **Discount status** | `active` | `yes` = fires when in window. `no` = skipped even if in window. | `yes` / `no`. |
| **Start date** | `date_start` | When the discount begins applying. | Required. |
| **End date** | `date_end` | When the discount stops applying. Nullable. | Cannot be before `date_start`; cannot be today or earlier on save. |
| **No expiration** | (toggle) | Wipes `date_end` and clears any date-end errors. | — |
| **Show timer in product listing** | `timer_list` | Renders countdown badge on category pages. | 1 / 0. Auto-disables when `date_end` is empty. |
| **Show timer in product details page** | `timer_details` | Renders countdown badge on product detail page. | 1 / 0. Disabled until an end date is set. |
| **Latest update** | (derived) | Shown as a badge on the freshly-saved row while async regeneration jobs run. | — |

## Business rules

### "Active for evaluation" — four-part gate

A discount is considered active at checkout when **ALL** of these hold:

- `active = 'yes'`.
- `date_start <= today` (in store timezone).
- `date_end IS NULL OR date_end >= today` (in store timezone).
- `max_uses IS NULL OR max_uses > uses` — strictly greater. A discount with `max_uses = 100` is still active at `uses = 99` and flips inactive when `uses = 100`. See [[discounts-eligibility]] for the per-customer cap counterpart.

Failing any one of these makes the discount invisible to the checkout lookup. The same active-scope is the single source of truth used by both the discount-lookup engine and the per-product attachment regeneration jobs (see [[discounts-storefront-display]]).

### Auto-disable on expiry — hourly background sweep

A platform-wide job runs **every 3 600 seconds (60 minutes)** and **toggles `active = no`** on any discount whose `date_end < (UTC now) - 1 day`. This retires expired holiday sales without manual intervention. A discount whose `date_end` was yesterday at 23:59 UTC gets deactivated at the next hourly tick after the +1 day cutoff — approximately 23:59 UTC the following day plus 0–60 minutes of sweep latency. The 1-day buffer prevents racing the merchant's evening edits. Skipped for plan-expired stores.

### Activation rate-limit — 10 minutes per discount (no-code Flat / Percent / Shipping / Fixed only)

Toggling `active` is **rate-limited to once per 10 minutes** — but **only for no-code Flat, Percent, Shipping and Fixed discounts** (the types that trigger per-product attachment regeneration). Quantity, Countdown, Code (single-code / Container) and Code PRO discounts are **not** throttled. Trying to re-toggle a throttled discount within the window returns one of two messages:

> *"You've already activated this discount. Please wait:minutes minutes in order to be able to deactivate it again."* (when trying to deactivate)
> *"You've already deactivated this discount. Please wait:minutes minutes in order to be able to activate it again."* (when trying to re-activate)

This protects the listing-engine regeneration job that rebuilds `product_to_discount` rows on every status flip — for high-catalog stores (10 000+ products) it can take minutes. See [[discounts-storefront-display]]. Bypassed in dev / CLI. On bulk-activate / bulk-deactivate, in-cooldown rows are **silently skipped**.

### "Latest update" badge

Creating or updating a discount fires several background jobs (per-product attachment recompute, smart-collection refresh, listing-engine patch). Because these run async, the merchant sees a **"Latest update: :date"** label on a freshly-saved discount until the jobs complete. Not an error — just signals "storefront catching up". See [[discounts-storefront-display]].

### Scheduling vs activation — independent switches

The `active` flag and the date window are independent:

- `active = yes` + `date_start` in the future → checkout skips until the date arrives. No timer fires at midnight; the discount just starts being eligible.
- `active = no` + dates valid → configured but never fires (useful to "stage" a discount).
- `active = yes` + `date_end` in the past → skipped at checkout immediately; next hourly sweep flips `active = no`.

For Black-Friday-midnight starts, pre-create with `active = yes` + `date_start = target date`. There is no "activate at X o'clock" cron beyond the date window.

### Counted statuses — when `uses` ticks

The `uses` counter only ticks when an order reaches one of the **counted statuses**, configured store-wide via `discounts_used_statuses`. Defaults: **`paid`, `completed`, `fulfilled`**. Cancelled / refunded orders **never** count. A `pending` order does not yet consume a `max_uses` slot — the slot is reserved when the order reaches `paid` (or the configured status). The merchant changes the set via the **Statuses** modal on the list page; see [[settings-statuses]]. The set is intersected with the live status dropdown so **renamed** statuses still work via their CODE (not their label).

### Bulk operations + soft-delete

Bulk-status-change applies the 10-minute cooldown per row; in-cooldown rows are silently skipped (no per-row error toast). Bulk-delete cascades through targets, customer_groups, customers, per-variant fixed rows, and Code PRO child codes — but does NOT delete historical order-discount rows (those survive for analytics — [[analytics-top-order-discounts]] / [[analytics-top-order-product-discounts]]). See [[discounts-audit-trail]] for the `discount.deleted` webhook.

## Related

- [[marketing-discounts]] — hub.
- [[discounts-eligibility]] — the other half of the "is this discount eligible?" check (customer, region, stacking).
- [[discounts-storefront-display]] — what fires when `active` flips (per-product attachment regen, cache invalidation).
- [[discounts-audit-trail]] — webhook events on create / update (toggle) / delete.
- [[discounts-known-issues]] — the strict-greater-than `max_uses` check + bulk-toggle silent-skip surprises.
- [[settings-statuses]] — `discounts_used_statuses` setting + the order-statuses-map modal.
- [[order-processing-pipeline]] — status transitions that drive the `uses` counter.

## Open questions

None.
