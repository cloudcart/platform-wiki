---
type: feature
nav_path: "Apps → Delivery time → List of shipping methods"
route_name: apps.shipping_hours.shipping_list
route_path: /admin/apps/shipping_hours/shipping-list
aliases: ["Shipping Hours Shipping List", "Delivery time shipping methods list", "List of shipping methods"]
tags: [apps, shipping, shipping-hours]
plan_gates: [shipping_hours]
created: 2026-05-21
updated: 2026-05-27
source_count: 3
---
# Delivery time → List of shipping methods

## Purpose

The **List of shipping methods** view shows all shipping methods the merchant has set up + lets them drill into per-method delivery-day schedules. See [[apps-shipping-hours]] for the full feature.

## Where to find it

Sidebar → Apps → Delivery time → **List of shipping methods tab**. Path `/admin/apps/shipping_hours/shipping-list`.

## What the merchant can do here

### Shipping methods table

The table lists shipping methods configured on the store. Per row the merchant can click into a per-method delivery-days editor.

**Important:** Only shipping methods WITHOUT a carrier integration are editable here. Courier-integrated methods (Econt / Speedy / GLS / BoxNow / etc.) supply their own delivery scheduling and either don't appear in this list or appear without an actionable link.

### Per-method drill-down

Clicking a method opens the delivery days editor at `/admin/apps/shipping_hours/delivery_hours/:id`. There the merchant defines:
- A schedule per day of week (Monday–Sunday). One entry per weekday.
- Multiple time slots per day, each with: From, To, Orders limit, Start, Interval.
- Exception dates (calendar days excluded from booking).

See [[apps-shipping-hours]] for the full per-slot field definitions.

### What the merchant CANNOT do here
- Add a NEW shipping method from this page — that's done in [[settings-shipping]].
- Bulk-copy / bulk-enable across methods — each method's schedule is edited individually.
- Configure across methods — each shipping method has its own independent schedule.

## Settings & fields

The table shows the merchant which shipping methods have a delivery-days schedule attached. The per-method editor (one level deeper) holds the actual schedule data.

## Per-method editor — modals & sub-flows (verified against backend)

The per-method editor lives at `/admin/apps/shipping_hours/delivery_hours/:id` and is composed of three surfaces: the **days list** (top-level grid of the configured weekdays), the **New / Edit day** modal (per-weekday slot editor), and the **Exceptions** modal (calendar of excluded dates).

### "New day with hours" modal (Create) — `Helpers/Create.vue`

A right-side slide-in modal (size `xll`, no-footer, custom header). Header title:
- Create mode: **"New day with hours"**.
- Edit mode: the day name itself (Monday / Tuesday / …).

**Header actions**: `Close` (white) and `Save` (primary; shows spinner during submit). The merchant cannot dismiss with Esc — they must use Close.

**Form fields (Create mode only)**:

| Field | Notes |
|-------|-------|
| **Day** (select, `SelectWithAjax`, half-width) | Required. Options: Monday / Tuesday / Wednesday / Thursday / Friday / Saturday / Sunday — minus any days already configured for this method (the parent passes `without` so a merchant can't double-add Monday). Error: *"Day is required"*. Edit mode disables this select. |

**Slots table** (always shown — both Create and Edit). One row per slot, plus a footer **+ Add new row** link. Columns (each is its own helper component):

| Column | Component | Notes |
|--------|-----------|-------|
| **From** | `CreateTableFrom` | Time-picker for the slot's open time. Required (*"From is required"*). |
| **To** | `CreateTableTo` | Time-picker for the slot's close time. Required (*"To is required"*). Must be after the row's **From** (*"To must be after From"*) AND after the previous row's **To** (*"To must be after previous To"*). |
| **Orders limit** | `CreateTableLimit` | Integer cap on orders inside this slot. Required (*"Limit is required"*), must be > 0 (*"Limit must be greater than 0"*). When the cap is reached at checkout, the slot is not offered. |
| **Start** | `CreateTableStart` | Toggle — when ON the lead-time gap (see "Interval" below) is computed from the slot's START time; when OFF it's computed from the slot's END time. Tooltip: *"If you enable this option, the distance that will be taken into account will start from the start time. If it is turned off, the end time will be used."* |
| **Interval** | `CreateTableInterval` | Number-of-hours gap between the order time and the FIRST possible delivery slot for that order. Tooltip: *"Choose a gap of hours between the order and the first possible delivery time."* |
| **Remove** | `CreateTableRemove` | Trash icon — deletes the row in memory (no API call until Save). |

**Change-day confirmation**: editing the **Day** select after rows are filled in opens a sub-modal:
- Title: **"Change the day?"**.
- Body: **"Are you sure you want to change the day, this will reset your current hours settings!"**.
- Buttons: Cancel / OK. Cancel reverts the picker; OK clears all slot rows.

**Save** POSTs to:
- Create: `POST /admin/api/shipping_hours/delivery-time/:methodId/save` (body: `{ day_of_week, hours: [...] }`).
- Edit: `POST /admin/api/shipping_hours/delivery-time/:methodId/save/:dayId` (same body + `id`).

Success toast (Create): *"You have successfully created a new day of the week with time zones"*. Edit: *"You have successfully updated the day of the week"*.

Validation errors render inline per-row + per-field; the modal stays open until all rows pass.

### "Exceptions" modal — `Helpers/Exeptions.vue`

Opened by the **Exceptions** button (white, top toolbar). Right-side modal, size `lg`.

**Header**: title *"Exceptions"*, Close + Save actions.

**Body**:

- Label: **"Add exception days"**.
- A `date-picker` (Persian date picker library, format `DD.MM.YYYY`, language from `serverSettings('language_cp')`).
- A click-to-open container — clicking it opens the date picker overlay. Each picked date becomes a tag (chip) inside the container.
- Per-tag: a small × button removes that date.
- Empty state placeholder text: *"Click to add days"*.
- Inline error text under the picker — used when an invalid date is selected (e.g., past date or duplicate).

The exception list is the union of all days the merchant wants to mark as "no delivery" — public holidays, vacation days, etc. On Save the platform persists the list for this shipping method only (NOT global).

### "Days" table (top level of per-method editor) — `Helpers/TableDays.vue`

The editor's main view is a grid of configured weekdays. Each card shows: day name, the slots inside it (From–To, limit), and action buttons via `TableActions` (Edit, Delete).

**Delete day** triggers an inline confirm before calling `DELETE /admin/api/shipping_hours/delivery-time/:methodId/:dayId`.

### Permission

Standard apps permission scope. The route also requires the `shipping_hours` plan gate to be active.

## Business rules

### Per-method independent schedules
Each non-courier shipping method has its own schedule. The merchant can run completely different rules across methods — e.g., "Personal delivery" 9:00–17:00 Mon–Fri vs "Local pickup" 10:00–22:00 every day.

### Storefront cascade
When a method has a delivery-day schedule configured, the customer sees a slot picker at checkout AFTER selecting that method. The slot picker honours the configured schedule, exceptions, and the global `interval` / `category` settings from [[apps-shipping-hours-settings]].

### No per-warehouse split
Slot capacity is stored per shipping method only. When [[apps-store-locations]] is installed, the slot's `Orders limit` is a single shared cap across all warehouses — there's no per-warehouse capacity. To run per-warehouse caps, the merchant creates separate per-warehouse shipping methods.

### Permission
Standard apps permission scope.

## Related

- [[apps-shipping-hours]] — hub with full slot-field documentation.
- [[apps-shipping-hours-settings]] — global settings.
- [[settings-shipping]] — where the merchant adds shipping methods (sources for this list).

## Open questions

_None._
