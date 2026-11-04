---
type: feature
nav_path: "Marketing → Discounts → Lifecycle"
route_name: ""
route_path: ""
aliases: ["Discount lifecycle", "Discount scheduling", "Discount start date", "Discount end date", "No expiration", "Auto-disable expired discounts", "Discount status toggle", "Жизнен цикъл на отстъпки", "Активиране на отстъпка", "Изтичане на отстъпка"]
tags: [marketing, discounts, promotions, lifecycle, scheduling]
plan_gates: []
created: 2026-06-10
updated: 2026-11-04
source_count: 3
---

# Discount lifecycle, scheduling & activation

> Part of [[marketing-discounts]]. See the hub for the other cross-cutting aspects (eligibility, tax/VAT, storefront display, audit trail, known issues) plus per-type details.

## Purpose

This aspect covers **when** a discount can fire: its `active` flag, its `date_start` / `date_end` window, the **"No expiration"** toggle, and the **hourly background sweep** that auto-disables expired discounts. The date window and the hourly auto-disable sweep apply to **every** discount type.

## Where to find it

**Sidebar → Marketing → Discounts → row toggle / Edit form → Date range block.** The activation switch is the per-row toggle on the list (`/admin/marketing/discounts`). The date window is configured in the **Date range** block of the create/edit form for every type.

## What the merchant can do here

- Schedule a discount to start on a future date — it stays `active = yes` but is **skipped at checkout** until `date_start` arrives.
- Schedule a discount to end automatically — set a `date_end` and the hourly sweep auto-deactivates it once the cutoff passes.
- Run an open-ended discount — toggle **"No expiration"** to clear `date_end`.
- Toggle a discount on/off mid-window via the row switch; it takes effect immediately.
- Bulk activate / deactivate multiple discounts via the table action bar.
- Render a countdown timer on storefront listings + product detail pages (per-type — see [[marketing-discounts-countdown]] and the per-Date-range timer switches on [[marketing-discounts-flat]] / [[marketing-discounts-percent]] / [[marketing-discounts-shipping]]).

## Settings & fields

| Field / Control | Backend key | What it does | Validation |
|-----------------|-------------|--------------|------------|
| **Discount status** | `active` | `yes` = fires when in window. `no` = skipped even if in window. | `yes` / `no`. |
| **Start date** | `date_start` | When the discount begins applying. | Required. |
| **End date** | `date_end` | When the discount stops applying. Nullable. | Cannot be before `date_start`. Asked for unless **No expiration** is on. Past dates and today save. |
| **No expiration** | (toggle) | Wipes `date_end` and clears any date-end errors. | — |
| **Show timer in product listing** | `timer_list` | Renders countdown badge on category pages. | 1 / 0. Auto-disables when `date_end` is empty. |
| **Show timer in product details page** | `timer_details` | Renders countdown badge on product detail page. | 1 / 0. Disabled until an end date is set. |

## Business rules

### "Active for evaluation" — four-part gate

A discount is considered active at checkout when **ALL** of these hold:

- `active = 'yes'`.
- `date_start <= today` (in store timezone).
- `date_end IS NULL OR date_end >= today` (in store timezone).
- `max_uses IS NULL OR max_uses > uses` — strictly greater. A discount with `max_uses = 100` is still active at `uses = 99` and flips inactive when `uses = 100`. See [[discounts-eligibility]] for the per-customer cap counterpart.

Failing any one of these makes the discount invisible to the checkout lookup. The same active-scope is the single source of truth used by both the discount-lookup engine and the per-product attachment regeneration jobs (see [[discounts-storefront-display]]).

### Auto-disable on expiry — hourly background sweep

A platform-wide job runs **every 3 600 seconds (60 minutes)** and **toggles `active = no`** on an expired discount at the first run after 00:00 UTC on the day after its `date_end`. This retires expired holiday sales without manual intervention. Skipped for plan-expired stores.

### Status switch — immediate

The switch in the Discounts list, the bulk action, the edit form and GraphQL take effect immediately, any number of times, on every discount type. At checkout the new status applies at once. The list switch and the bulk action send no webhook and start no background rebuild; see [[discounts-audit-trail]].


### After a save

Saving a discount writes its per-variant rows during the save. The listing engine and smart collections are refreshed afterwards, so listings can take a moment to catch up. See [[discounts-storefront-display]]. A discount that holds a stored rebuild time shows *"Latest update: {time}"* as a tooltip on its name in the list; a save does not set that time.

### Scheduling vs activation — independent switches

The `active` flag and the date window are independent:

- `active = yes` + `date_start` in the future → checkout skips until the date arrives. No timer fires at midnight; the discount just starts being eligible.
- `active = no` + dates valid → configured but never fires (useful to "stage" a discount).
- `active = yes` + `date_end` in the past → skipped at checkout immediately; next hourly sweep flips `active = no`.

For Black-Friday-midnight starts, pre-create with `active = yes` + `date_start = target date`. There is no "activate at X o'clock" cron beyond the date window.

### Counted statuses — when `uses` ticks

The `uses` counter only counts orders in one of the **counted statuses**, configured store-wide via `discounts_used_statuses`. Defaults: **`paid`, `completed`, `fulfilled`**. A `pending` order does not consume a `max_uses` slot until it reaches `paid` (or the configured status), or until it is marked fulfilled under the defaults. A merchant can add Cancelled or Refunded to the set, and those orders then count. The merchant changes the set via the **Statuses** modal on the list page; see [[settings-statuses]]. The set is intersected with the live status dropdown so **renamed** statuses still work via their CODE (not their label).

### Bulk operations + delete

Bulk status change applies to every selected row immediately. A discount used in a smart collection or an XML import / sync task cannot be deleted: *"This discount cannot be deleted because it is still used in: ..."*. Otherwise bulk-delete removes the discount; its targets, customer_groups, customers, per-variant fixed rows and Code PRO codes go with it (verify). Historical order-discount rows survive for analytics — [[analytics-top-order-discounts]] / [[analytics-top-order-product-discounts]]. A list delete sends no `discount.deleted` webhook; see [[discounts-audit-trail]].

## Related

- [[marketing-discounts]] — hub.
- [[discounts-eligibility]] — the other half of the "is this discount eligible?" check (customer, region, stacking).
- [[discounts-storefront-display]] — what fires when a discount is saved (per-variant rows, cache invalidation).
- [[discounts-audit-trail]] — webhook events on create / update / delete.
- [[discounts-known-issues]] — the strict-greater-than `max_uses` check.
- [[settings-statuses]] — `discounts_used_statuses` setting + the order-statuses-map modal.
- [[order-processing-pipeline]] — status transitions that drive the `uses` counter.

## Open questions

None.
