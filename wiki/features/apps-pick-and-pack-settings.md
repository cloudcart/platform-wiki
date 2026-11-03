---
type: feature
nav_path: "Apps → Pick and Pack → Settings"
route_name: apps.pick_and_pack.settings
route_path: /admin/apps/pick_and_pack/settings
aliases: ["Pick and Pack Settings", "PickAndPack config", "Warehouse terminal config"]
tags: [apps, administration, pick-and-pack, warehouse, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-05-26
source_count: 1
---
# Pick and Pack → Settings

## Purpose

The **Settings** tab is where the merchant configures **warehouse terminal access**, dispatch / packing rules, and barcode-scanning preferences for the in-house warehouse Pick and Pack flow. See [[apps-pick-and-pack]] for the full feature set.

## Where to find it

Sidebar → Apps → Pick and Pack → **Settings tab**. Route: `/admin/apps/pick_and_pack/settings`.

## What the merchant can do here

### Terminal access

| Field | Notes |
|---|---|
| **Terminal credentials** | Username + password for warehouse staff to access the terminal UI (via `AccessToTerminal` middleware per [[apps-pick-and-pack]]). |
| **Allowed IP whitelist** | Restrict terminal access to specific IPs (warehouse network only). |
| **Per-terminal device ID** | Map each tablet / scanner to a unique terminal ID (stored as `terminal_id` per [[apps-pick-and-pack]]). |

### Dispatch / packing rules

| Setting | Notes |
|---|---|
| **Auto-transition on Pack** | When packed, auto-update order status to "Packed" / "Ready to ship". |
| **Auto-generate waybill on Pack** | Trigger [[orders-shipping-waybill]] when an order is packed. |
| **Per-staff metrics** | Track per-staff pick / pack performance. |
| **Missing-product alerts** | Where to send `terminal_missing` flags (email / Slack / etc.). |

### Barcode / scanning

| Setting | Notes |
|---|---|
| **Accepted barcode formats** | EAN / Code 128 / QR / etc. |
| **Camera vs handheld scanner** | Default input mode for the terminal. |
| **Scan failure threshold** | Alert when scans repeatedly fail (e.g., damaged barcode label). |

### What the merchant CANNOT do here
- Use without configured terminal devices.
- Override the per-order meta keys set by terminal actions.

## Settings & fields

Per [[apps-pick-and-pack]] Manager: 9 order-meta constants drive the workflow (`terminal_count_package`, `terminal_is_packed`, `terminal_is_unpacked`, `terminal_id`, `terminal_dispatch_time`, `terminal_confirmation_time`, `terminal_for_pack`, `terminal_missing`, `terminal_product_confirmation`).

## Business rules

### Terminal UI is separate

The terminal interface lives at a separate route (verify) with its own access middleware. Staff log in there to do actual picking/packing — not through the regular admin UI.

### Per-warehouse settings

When the merchant has multiple warehouses (via [[apps-store-locations]]), each may have its own Pick and Pack settings — verify.

### Permission
Standard apps permission scope. Terminal access has its own dedicated middleware `AccessToTerminal`.

## Related

- [[fulfillment-and-warehouse]] — fulfillment & warehouse hub.
- [[apps-pick-and-pack]] — hub.
- [[apps-store-locations]] — multi-warehouse setup.
- [[orders-shipping-waybill]] — waybill generation triggered by Pack confirmation.

## How it works (verified against backend)

### One terminal per configuration row

Settings are not "global app settings" — each terminal the merchant creates is its own row in `@apps_order_terminal` with its own configuration. The Settings tab is really a list of terminals plus a "Create new terminal" CTA. To override settings for a different warehouse, the merchant creates another terminal with that geo zone / store binding. There is no "default settings" applied across terminals.

### Form fields per terminal (full list)

- **Terminal name** — required (error: *"You have not entered a name for the terminal"*).
- **Allowed users** — required (error: *"You have not selected users who have access to the terminal"*); multi-select of [[settings-staff]] admin accounts.
- **Active / inactive** — checkbox.
- **Locations** — optional; comma-separated list (stored as the `locations` column on the terminal).
- **Order statuses** — required, multi-select. Includes the synthetic `pending` and `paid` plus any of the merchant's custom order statuses. Error: *"You have not selected statuses for the order which will be visualised in the terminal"*.
- **Type** — required, one of `products` / `pick_pack` / `pack`. Error: *"You have not selected a type for the terminal"*.
- **Filter by** — `geo_zones` or `stores`. Only one applies at a time.
- **Zones** — multi-select of [[settings-geo-zones]] when filter-by = geo_zones.
- **Shops** — multi-select of [[apps-stores]] store locations when filter-by = stores (only shown when the Stores app is installed).
- **Order time (days)** — show only orders from the last N days; empty = no time window.
- **Sort by** — `id` (creation date) or `shipping_from` (estimated shipping date).
- **Sort type** — ascending / descending.
- **Constant sound on new order** + the "I understand" button toggle.

### Pick & Pack sub-settings (when type = pick_pack)

When the merchant picks the **pick_pack** type, a `pick_pack.show_pick` block appears:

- **Allow packing** (boolean) — enables the pack-related fields below.
- **Allow entering package count** — exposes the `terminal_count_package` action.
- **Allow sending the order** — exposes the send-to-courier flow.
- **Status for packed order** — the order status that gets applied when the picker marks the order packed (error: *"Select a status which will be set for the order after it has been packed"*).
- **Status for packing with missing products** — the order status when the order is packed but one or more items are missing.
- **Status for unpacking** — the order status when the picker unpacks an already-packed order.

### Pack-only sub-settings (when type = pack)

A `pack` block appears:

- **Send-minute intervals** — a list of "minutes after a click" buttons the packer can use to schedule sending the order to the courier (error: *"You have not entered minutes for sending an order"* when the type is pack but no intervals are set). The values are de-duplicated server-side.

### No multi-warehouse "override" — clone the terminal

There is no "default + warehouse override" model. The merchant creates one terminal per warehouse, picks that warehouse's geo zones or store locations on each, and copies the rules manually if they want them identical.

### No barcode-format / camera-vs-handheld settings

Neither the create-form nor the model has fields for barcode format or scanner mode. The terminal accepts whatever keystrokes the connected USB / Bluetooth scanner emits. Camera scanning is not a documented option in the shipped settings.

### No per-staff metrics dashboard, no offline-mode toggle, no pick-by-light / voice-pick

These options do not exist on the settings form. They are not switchable in this app; the merchant who needs them must use external warehouse-management tooling on top of the terminal.

## Open questions

