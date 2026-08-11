---
type: feature
nav_path: "Apps → Also"
route_name: apps.also.overview
route_path: /admin/apps/also
aliases: ["Also", "Also ERP", "enable disable button", "app active toggle", "missing enable button"]
tags: [apps, erp]
plan_gates: ["also", "also_total_products"]
created: 2026-05-22
updated: 2026-08-06
source_count: 20 20 12 61 79 80 81 98 101 33 100 204 250 395 398 399 400 333 701(2+1))
---
# Also (ERP)

## Purpose

**Also** integration — ERP / accounting system connector. Syncs orders and customers between CloudCart and Also.

> **On/off control appears only when the integration is configured.** Every ERP that uses this shared screen supports being switched on and off, but the **Enable / Disable** button (and the enabled / disabled indicator next to the app name) stays hidden until the connection credentials are filled in and saved — so a missing button on a fresh install is not a fault. Fill in the credentials on the **Settings** tab, save, and the button appears.

## Where to find it
Sidebar → Apps → install → **Also**.

## What the merchant can do here
- Configure Also credentials.
- Sync orders to Also.

### What the merchant CANNOT do here
- Use without Also subscription.

## Settings & fields
Manager: the backend manager (`APP_KEY = 'also'`).

## Business rules
This is a **distributor catalog integration**, not a generic accounting ERP. Also serves as the supplier — CloudCart imports their catalogue into the merchant's store.

### Permission
Standard apps scope.

## How it works (verified against backend)

### Vertical
**IT / hardware distribution.** Also (also.com) is a global distributor of networking and communications equipment, monitors, multimedia computer systems and components, peripherals, power-protection and physical-protection solutions. The integration is aimed at IT hardware resellers who want to import Also's catalogue into their CloudCart storefront.

### Credentials
The merchant supplies their **Also account username and password**.

### Category mapping
The merchant maps each Also category to a CloudCart category before products are imported. *"Map your categories with Also."*

### Pricing
The merchant chooses which Also price column to use:
- **Dealer price without VAT** (`price`) — wholesale dealer price.
- **Final price including VAT** (`priceEndUser`, default) — recommended retail price.

A **markup percentage** can be applied on top.

### Availability-status quantities
Also returns availability statuses; the merchant assigns a default CloudCart quantity for each:
- **On hand / In stock** (default 5).
- **Minimum** (default 1).
- **On order** (default 0).

### Sync behaviour
- **Update properties** (optional) — what fields are kept in sync on re-import.
- **Delete missing products** (default ON) — when a product disappears from Also's feed, CloudCart removes / disables it.

### Sync events in order history
Successful sync events log `send_erp_success`; failures log `send_erp_error` with the upstream error message.

### Connection failures
If Also's API can't be reached, the integration shows: *"Error in connection with Also. Please try again later."*

### Sync frequency (cron intervals)
The recurring import queue runs on fixed intervals:
- **Catalog parse** (`also_parse`) — every **24 hours** (86400 s). This is the full product re-pull from Also.
- **Categories refresh** (`also_categories`) — every **3 hours** (10800 s) — updates the category tree silently in the background.
- One-off jobs (`also_insert`, `also_delete`, `also_quantity_reset`, `also_categories_fetch`) fire on demand and don't have a recurring schedule.

So the merchant sees the storefront catalogue refresh from Also at most once per day. Changing settings doesn't accelerate the next run — the schedule is fixed.

### Sync direction is PULL ONLY
Also is a **distributor catalogue** integration: products + categories flow Also → CloudCart only. CloudCart does NOT push orders back to Also; the merchant uses Also for catalogue + pricing, then fulfils via their own logistics.

### Settings persisted (per `keySettings`)
The integration persists exactly: `username`, `password`, `price` (price column selector — `priceEndUser` default), `update_properties` (which product fields to keep in sync on re-import), `delete_missing_products` (default ON), `onhand` (default 5), `minimum` (default 1), `onorder` (default 0). Quantities are validated `int|min:0|max:999999`.

## Plan gates

This app is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `also` | Access gate (install URL) | The install URL `/admin/apps/also/install` is blocked when the plan lacks the feature. The app is hidden from the Apps catalog for those plans. |
| `also_total_products` | Numeric (global cap) | App-specific cross-task cap on imported products from the Also distributor catalogue. When the cap is hit, additional products are skipped. |

Behaviour: lower plans cannot install the app. Existing installs continue working on plan downgrade until the merchant cancels — see [[plan-vs-feature-pack]] for downgrade rules.

## UI structure — tabs + sub-flows

The Also admin uses the shared **ErpMain** wrapper. Visible tabs (in order):

1. **Overview** (`apps.also.overview`) — standard ERP intro card.
2. **Status** (`apps.also.status`) — only visible when configured + category mapping done. Renders **TaskStatus**, plan-feature progress bars (the `also_total_products` cap shows here with a "Purchase an additional bundle of products." upgrade link to the plan-feature modal), per-queue **ProgressStatus** modules, and **ResetImport**.
3. **Settings** (`apps.also.settings`) — see *Settings tab layout* below.
4. **Categories mapping** (`apps.also.categoriesMapping`) — **gating tab**: must have at least one mapping before Status / Products tabs unlock. See *Categories mapping modal* below.
5. **Processed products** (`apps.also.products`) — list of products imported via Also.
6. **Import history** (`apps.also.importLog`) → drilldown to `apps.also.importList` (per-run change log).

### Settings tab layout

The credentials block uses Also's `Credentials.vue` with two required fields:
- **Username** (string) — error "Invalid credentials" surfaces on validation failure.
- **Password** (`PasswordInputComponent` — masked).

No URL field — Also's API endpoint is fixed by the integration.

Below credentials sits the fetch-data-queue-progress panel (same standard pattern as Barsy). After validation succeeds, the rest of the Settings tab populates with:
- **Pricing**: which Also price column to use (`price` / `priceEndUser`) + markup percentage.
- **Availability statuses**: numeric defaults for `onhand` (5), `minimum` (1), `onorder` (0) — server-validated `int|min:0|max:999999`.
- **Update properties**: multi-select picker of which product fields to re-sync.
- **Delete missing products** switch.

### Categories mapping modal

The Categories mapping tab is the standard ERP **CategoryMap** table — paginated, filterable by Cloudcart category, with a per-row "Edit" / "Delete" action. Clicking **+ Add new mapping** opens a side-sheet modal (`MappingModal.vue`):

- **Also category** select (searchable, required) — options come from server-loaded `meta.externalCategories`.
- **CloudCart category** select (searchable, required) — options from `meta.internalCategories`.
- **Percent** input (number, unit `%`, step `1`, min `0`, max `500`) — Also-category-level markup that stacks on top of the global markup.

Save / Cancel buttons live in the modal header (not footer). The modal has `:no-close-on-backdrop="true"` and `:no-close-on-esc="true"` — the merchant must explicitly click Cancel to dismiss (prevents accidental loss of partial input). Bulk-delete is available via the table's TableActions component (`delete-url: /admin/api/also/category-map/0`).

Until at least one mapping exists, the Status / Products / Tasks tabs are hidden (the `isAllowStatusTab` computed in `TabsERP.vue` checks `app.required?.categoryMapping` against `app.meta?.hasMappedCategories`).

## Related
- [[erp-integrations]] — ERP & accounting integrations hub.
- [[external-record-mapping]] — the import-origin tagging (app_import = 'also-<id>') the integration uses to track and re-find its imported products + the internal read queries.
- [[apps]] — App Store.
- [[orders-history]] — sync events.

## Open questions

_None — all questions answered above._
