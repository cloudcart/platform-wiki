---
type: feature
nav_path: "Apps → Pick and Pack"
route_name: apps.pick_and_pack.overview
route_path: /admin/apps/pick_and_pack
aliases: ["Pick and Pack", "Pick & Pack", "Warehouse terminal", "Mobile warehouse app", "Складова система", "no enable disable button", "app has no active toggle"]
tags: [apps, administration, fulfillment, warehouse, terminal]
plan_gates: ["pick_and_pack_terminals"]
created: 2026-05-22
updated: 2026-08-06
source_count: 1
---
# Pick and Pack (in-house warehouse terminal)

## Purpose

**Pick and Pack** adds a **tablet/terminal-based warehouse interface** for in-house picking + packing. Warehouse staff use a touchscreen device to scan products, count package contents, confirm pickups for shipping, manage dispatch timing, and flag missing items. Unlike [[apps-frisbo]] (outsourced 3PL), it is for merchants running their **own** warehouses.

Used by merchants with own warehouses + dedicated picking staff, high-volume stores where order-by-order processing is too slow, and merchants wanting barcode scanning.

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.
>
> What *can* be switched off is an individual **terminal** — every terminal configuration has its own Active / inactive toggle.

## Where to find it

Sidebar → Apps → install → **Pick and Pack**. Admin configuration lives in [[apps-pick-and-pack-settings]]; warehouse staff use the dedicated terminal interface (served from a CloudCart URL).

## What the merchant can do here

- Create + configure **terminals** (each terminal is a saved configuration — see Business rules).
- Assign warehouse staff (existing admin accounts) to each terminal.
- Set dispatch / packing rules + status transitions per terminal.
- View terminal activity (the action history records the admin who triggered each action).

### What the merchant CANNOT do here

- Use Pick and Pack without devices for staff (tablets, scanners).
- Process orders without staff trained on the terminal UI.
- Rely on pick-by-light, voice-pick, or offline mode — none are shipped (the terminal is a web app needing a live connection; if wifi drops, staff lose the queue until it returns).
- Configure a barcode format or use camera scanning — the terminal accepts whatever string a connected USB / Bluetooth scanner types into the focused field, so EAN / Code 128 / QR all work identically.
- See a per-staff performance dashboard — the data is in the order-meta history but is not a report.

## Settings & fields

A **terminal** is a saved configuration row (not a physical device). All the merchant's choices collapse into a single JSON `settings` blob, so a config is portable (exportable / copyable between terminals). The simple stored columns are: name, `user_access` (allowed admin IDs), `is_active`, and `slug` (auto-generated URL slug). The public terminal URL (`apps.pick_and_pack.index`) uses the **slug**, not the ID — renaming the terminal re-generates the slug.

Each terminal carries:

- **Name** + auto-generated slug. Staff bookmark the slug-URL; one terminal URL can serve many physical tablets.
- **Type** — one of `products` / `pick_pack` / `pack` (see Business rules), controlling the staff UI.
- **Active / inactive** toggle.
- **Allowed users** — CloudCart admin accounts ([[settings-staff]]) who can log in. There is no separate "terminal staff" role.
- **Filter scope** — `geo_zones` (orders whose shipping address falls inside a linked [[settings-geo-zones]]) **OR** `stores` (orders shipped via Glovo or a store-location whose `service_id` / `marketplace_id` matches, when [[apps-stores]] is installed). Multi-warehouse routing is geo-zone-based by default.
- **Order-statuses filter** + an **order-time window** in days (e.g. last 30 days).
- Per-type rules (for `pick_pack` / `pack`): post-pack status transition, packing-with-missing transition, unpacking transition, send-to-courier rules, dispatch-time intervals.
- UI toggles: constant sound on new order (with per-order mute), show price, show order-cancel button, generate printable form (waybill / picking slip PDF), show pick controls.

The integration tracks pick-and-pack state per order via these order-meta keys (complete list, each set by a matching terminal action key):

| Meta key | Action key | What it tracks |
|----------|-----------|----------------|
| `terminal_count_package` | COUNT_PACKAGE | Number of packages for the order. |
| `terminal_is_packed` | PACKED | Order is packed. |
| `terminal_is_unpacked` | UNPACKED | Order was unpacked (e.g. wrong items). |
| `terminal_id` | ID | Which terminal handled the order. |
| `terminal_dispatch_time` | ADD_MINUTE | When the order is dispatched. |
| `terminal_confirmation_time` | SEND_TO | When the dispatch is confirmed. |
| `terminal_for_pack` | COLLECTED | Order is in collection state. |
| `terminal_missing` | MISSING | Some products are missing. |
| `terminal_product_confirmation` | PRODUCT_CONFIRMATION | Per-product confirmation flag. |
| `terminal_shipping_job` | SHIPPING_JOB | Links the order to its shipping job in [[orders-shipping-waybill]]. |
| `terminal_mute_sound` | MUTE_SOUND | Per-terminal / per-order audio mute. |

## Business rules

### Terminal types

Three distinct modes answer the multi-terminal question — a warehouse can run separate Pick and Pack stations or a combined one, all without any per-warehouse install:

- `products` — product-oriented layout listing products (not orders); used for cycle counts + stock receiving.
- `pick_pack` — combined pick + pack in one workflow.
- `pack` — pack-only (assumes another terminal already picked).

A store can run as many terminals as it needs (each on its own slug-URL), assigning different staff + geo zones to each, capped by the `pick_and_pack_terminals` plan-feature.

### Terminal-driven workflow

Warehouse staff log into the terminal interface (typically on a tablet), which is optimised for touch + barcode scanners:

1. Scan an order barcode OR pick from a list.
2. Walk to product locations + scan each product.
3. Confirm count per item.
4. Mark order **Packed** → triggers [[orders-shipping-waybill]] generation via the configured courier (through the `terminal_shipping_job` linkage).
5. Mark **Dispatched** → triggers shipment notification.

### Missing-product handling

When staff find a product missing (out of stock not reflected in the system), they flag it via `terminal_missing`. The order's fulfillment workflow then routes to handling (refund line, substitute, etc.).

### Order-status scope

The terminal config picker adds two **synthetic statuses** to the standard list: `pending` and `paid`. They mean "the order's `paid` / `pending` parameter is met regardless of which custom status it sits in". Real merchant-defined statuses (anything starting `order-...`) also appear, so any status can be included or excluded. Typically merchants pick only paid orders.

### Access control + permissions

A separate access middleware checks the logged-in admin is in the terminal's `user_access` list (set on terminal create / update). App install follows the standard app-subscription flow; the terminal interface uses its own dedicated access path, independent of admin panel permissions.

### Supplier restock interaction

Restocking via [[apps-suppliers]] updates the product's stock; the terminal reads current stock from the same table and sees the new quantity on its next refresh. There is no special handshake between the two apps.

## Plan gates

Gated by the `pick_and_pack_terminals` plan-feature (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `pick_and_pack_terminals` | Numeric quota | How many terminal configurations the merchant can create. Usage is counted **dynamically** from the actual database rows — so deleting a terminal lowers usage immediately for the upgrade-CTA math. Adding a terminal past the cap surfaces the HTTP 402 paywall modal with an *"Upgrade your quota from here"* link to the [[plan-features]] upsell. |

Behaviour: lower plans get redirected to the per-feature upsell at [[plan-features]] or a plan-upgrade panel. The quota is numeric — it extends via packs ([[plan-vs-feature-pack]]); a pack survives plan changes and stacks with the new plan's base value. App install itself follows the standard app-subscription flow, independently of the plan-feature.

## Related

- [[fulfillment-and-warehouse]] — fulfillment & warehouse hub.
- [[apps]] — App Store.
- [[apps-pick-and-pack-settings]] — admin settings.
- [[apps-frisbo]] — alternative outsourced 3PL fulfillment.
- [[apps-suppliers]] — restocking that the terminal reads back.
- [[apps-stores]] — store-locations binding for the `stores` filter scope.
- [[settings-geo-zones]] — geo-zone filter scope for terminals.
- [[settings-staff]] — admin accounts that double as terminal logins.
- [[orders]] — order source.
- [[orders-shipping-waybill]] — waybill auto-triggered on Pack confirm.

## Open questions

