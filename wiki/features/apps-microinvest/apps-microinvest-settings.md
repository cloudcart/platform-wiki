---
type: feature
nav_path: "Apps → Microinvest → Settings & tabs"
route_name: apps.microinvest.settings
route_path: /admin/apps/microinvest/settings
aliases: ["Microinvest settings", "Microinvest price field", "Microinvest updates", "disable_missings", "Microinvest debug_mode", "Microinvest tabs", "Microinvest units field"]
tags: [apps, erp, microinvest, settings, configuration]
plan_gates: []
created: 2026-06-25
updated: 2026-06-25
source_count: 2
---

> Part of [[apps-microinvest]]. See the hub for the other aspects (sync model, product matching, reset import, sync debug).

# Microinvest — settings & tabs

## Purpose

The Settings-tab configuration fields and the app's tab layout — how the merchant tells the integration which direction to sync, which field to match products by, which price slot and which product fields Microinvest may overwrite, and the defaults for new imports.

## Where to find it

Sidebar → Apps → **Microinvest** → **Settings** tab.

## What the merchant can do here

Configure import / export direction, the product match field, the price slot, the overwrite-allowlist, and new-product defaults — then Save.

## Settings & fields

The Settings tab persists, all under `settings.<key>`:

- **Credentials** — `identifier` (Microinvest license / account ID, required) and `password` (API access password, required). Entered on the Settings tab, not the `credentials.*` wrapper most other ERPs use. There is no separate "Validate & connect" step: the integration is always considered configured, so the merchant just clicks Save. Wrong credentials surface as errors on the next sync attempt.
- **Action** select — `import` (Microinvest → CloudCart, default) or `export` (CloudCart → Microinvest). Drives sync direction — see [[apps-microinvest-sync-model]].
- **Compare by** (`compare_by`) — how to match an existing CloudCart product to a Microinvest record: SKU / EAN / Barcode (or `nothing`). The full matching behaviour is on [[apps-microinvest-product-matching]].
- **Price field** (`price_field`) — which of Microinvest's 10 price slots `PriceOut1`…`PriceOut10` flows to CloudCart (default `PriceOut2`). A merchant can keep retail price in `PriceOut1` and online price in `PriceOut2`; CloudCart only reads the selected slot.
- **Updates** multi-select (`updates`) — the 7 product fields the merchant lets Microinvest overwrite on each sync: `name`, `short_description`, `description`, `category_id`, `track_inventory`, `continue_selling`, `shipping`. Fields left out stay CloudCart-controlled. Useful for hybrid setups ("Microinvest is authoritative for stock + price but I control names / descriptions in CloudCart").
- **Publish as** triplet — `publish_as_active` / `publish_as_featured` / `publish_as_new`, defaults applied to new imports.
- **Require shipping** (`require_shipping`), **Quantity tracking** (`quantity_tracking`), **Continue sell** (`continue_sell`) — boolean defaults for new imports.
- **Disable missings** (`disable_missings`) — when ON, products that disappear from Microinvest's feed are set inactive on CloudCart; when OFF they stay active. Interacts with deletion detection — see [[apps-microinvest-product-matching]].
- **Discount** (`discount_id`) — group all Microinvest-flagged products under a discount.
- **Units** (`units`) — appears ONLY when the **Grocery Store** optional app ([[apps-grocery-store-settings]]) is installed; switching it ON tells the import to skip product grouping, so each Microinvest unit (weight / package size) becomes its own CloudCart product instead of merging into a variant product.
- **Debug mode** (`debug_mode`) — CloudCart-staff-only toggle, hidden for regular merchant sessions; bypasses file-acceptance validation during imports, for diagnosing tricky feeds.

## Business rules

### Tab layout

Visible tabs, in order: **Overview**, **Status**, **Settings**, **Processed products**, **Tasks** (Microinvest-specific), **Import history** (with drilldown). Microinvest does **NOT** have a Categories mapping tab — import keeps the Microinvest category structure verbatim, with no per-category routing.

### Tasks tab

Route `apps.microinvest.tasks/:taskId?` — Microinvest is one of the few ERPs with a dedicated Tasks tab. It lists every async task the integration has run (start_import, sync_orders_usn, finish_import) with status, timestamps, and per-task log drilldown; the optional `:taskId?` opens a task's detail panel (which shows its XML — see [[apps-microinvest-debug]]).

## Related

- [[apps-microinvest]] — hub.
- [[apps-microinvest-product-matching]] — the `compare_by` field's matching behaviour and `disable_missings` deletion detection.
- [[apps-microinvest-sync-model]] — what the `Action` direction does.
- [[apps-microinvest-debug]] — the Tasks tab's underlying debug queries.
- [[apps-grocery-store-settings]] — the Grocery Store app that exposes the `units` field.

## Open questions

(none)
