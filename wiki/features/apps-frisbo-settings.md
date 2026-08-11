---
type: feature
nav_path: "Apps → Frisbo → Settings"
route_name: apps.frisbo.settings
route_path: /admin/apps/frisbo/settings
aliases: ["Frisbo Settings", "Frisbo credentials", "Frisbo config"]
tags: [apps, administration, frisbo, fulfillment, 3pl, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-06-11
source_count: 2
---
# Frisbo → Settings

## Purpose

The **Settings** tab is where the merchant connects CloudCart to their **Frisbo** 3PL fulfillment account — enters credentials, picks which Frisbo organization, warehouse and channel to use, and configures whether orders auto-send to Frisbo for picking, packing and shipping. Without valid Settings the integration can't send orders to Frisbo.

For the full Frisbo feature set, see [[apps-frisbo]].

## Where to find it

Sidebar → Apps → Frisbo → **Settings tab**. Route: `/admin/apps/frisbo/settings`.

## What the merchant can do here

The page shows three stacked cards. Cards 2 and 3 stay hidden until credentials are saved and valid, and re-lock whenever the merchant edits the email or password again — so credentials are always validated before organization settings can be touched.

- **Card 1 — Connect (credentials).** Enter the Frisbo **email** and **password**, then click **Validate credentials & save**. The platform calls Frisbo's API to verify them; on success the credentials are stored and the integration becomes active, on failure it surfaces the Frisbo API error.
- **Card 2 — Organization scope.** Pick the Frisbo **organization**, **warehouse** and **channel** (lists are fetched live from Frisbo).
- **Card 3 — Order automation.** Turn on **Automatic order dispatch** and choose which order status auto-sends to Frisbo.

### What the merchant CANNOT do here
- Use Frisbo without an active Frisbo merchant contract + Frisbo-allocated warehouse.
- Connect more than one Frisbo organization at a time — single org per CloudCart store. Switching org/warehouse/channel is done by re-editing these same selectors and saving; there is no separate "switch org" wizard.

## Settings & fields

| Field | Key | Notes |
|---|---|---|
| **Email address** | `email` | Frisbo login email. Routed through the validate-and-save flow, not the normal settings save. |
| **Password** | `password` | Frisbo login password. Routed through validate-and-save (not the normal settings save). |
| **Organization** | `organization_id` | Searchable list fetched from Frisbo. Selecting a new org **clears the saved warehouse and channel**. |
| **Warehouse** | `warehouse_id` | Source warehouse holding the merchant's inventory. Disabled until an organization is chosen. |
| **Channel** | `channel_id` | Sales channel inside Frisbo. Disabled until an organization is chosen. |
| **Automatic order dispatch** | `automate_send` | Switch (`1` / `0`). When on, paid/new orders auto-send to Frisbo. |
| **Sending an order with status** | `order_status` | Visible only when `automate_send = 1`. Options: `new_order` ("New order") / `paid` ("Paid"). |

A **Create a product in Frisbo** option (`create_products` — "If the product does not exist in Frisbo, create it") exists in the code but is not currently shown to merchants.

## Business rules

### Authentication is email + password (not OAuth)

Frisbo uses email + password, not OAuth keys or an API key. The platform logs in with the stored credentials and keeps a short-lived token behind the scenes, re-authenticating automatically when it expires. A long quiet period followed by a single order send triggers a transparent re-login the merchant never sees.

### Wrong credentials fail per-order, not on the Settings page

If the Frisbo password is later rotated or wrong, the silent re-login simply fails and the next order send fails at Frisbo's API. The error appears on the affected order (in its Frisbo response detail), **not** as a "credentials invalid" banner in Settings. Practical impact: after a Frisbo password change the merchant sees individual orders failing rather than a clear Settings warning — re-enter and re-validate the credentials here to fix it.

### Editing credentials re-locks the rest of the page

Changing the email or password re-hides the Organization and Order-automation cards and re-shows the **Validate credentials & save** button. This guarantees the merchant re-validates before editing organization-level settings, which depend on a working token.

### Inventory lives in Frisbo, and does not pull back

When Frisbo is active the merchant's physical stock lives in Frisbo's warehouses. CloudCart does **not** automatically pull Frisbo's stock counts into its own product quantities — product stock remains merchant-managed in CloudCart and is not auto-synced from Frisbo.

### Auto-send-on-status

When **Automatic order dispatch** is on, orders auto-send to Frisbo the moment they reach the chosen status (`new_order` or `paid`); Frisbo then picks, packs and ships. With it off, the merchant sends each order manually from the order screen.

### Side effects on Connect
- Credentials are stored and the integration becomes active.
- The organization list is fetched from Frisbo.
- The other Frisbo tabs unlock.

### Disconnecting via Uninstall

Uninstalling the app removes the credentials from CloudCart and stops it pushing new orders or polling Frisbo. Orders already shipped to Frisbo continue their lifecycle on Frisbo's side (tracking lives in Frisbo's portal); CloudCart performs no cleanup of in-flight Frisbo orders — those resolve through Frisbo's own systems.

### Permission
Standard apps permission scope.

## Related

- [[fulfillment-and-warehouse]] — fulfillment & warehouse hub.
- [[apps-frisbo]] — Frisbo hub.
- [[apps-frisbo-orders]] — orders sent to Frisbo.
- [[orders-details]] — per-order send-to-Frisbo action.
- [[orders-shipping-waybill]] — Frisbo replaces normal waybill generation.

## Open questions
