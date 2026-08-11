---
type: feature
nav_path: "Apps → Barsy"
route_name: apps.barsy.overview
route_path: /admin/apps/barsy
aliases: ["Barsy", "Barsy ERP", "Barsy retail", "enable disable button", "app active toggle", "missing enable button"]
tags: [apps, erp, retail]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 3
---
# Barsy (retail ERP)

## Purpose

**Barsy** (barsys.eu) is a Bulgarian retail and restaurant/hospitality management system (POS + ERP). The integration syncs products, inventory, prices, customers, and orders between CloudCart and Barsy, so a merchant running physical stores or restaurants can share the POS catalogue with their CloudCart storefront and push storefront orders back to Barsy.

> **On/off control appears only when the integration is configured.** Every ERP that uses this shared screen supports being switched on and off, but the **Enable / Disable** button (and the enabled / disabled indicator next to the app name) stays hidden until the connection credentials are filled in and saved — so a missing button on a fresh install is not a fault. Fill in the credentials on the **Settings** tab, save, and the button appears.

## Where to find it

Sidebar → **Apps** → install → **Barsy** (`/admin/apps/barsy`).

## What the merchant can do here

The app opens with a tab bar:

- **Overview** — intro card explaining the integration.
- **Status** — start/stop the sync, watch import-limit progress bars ("Your product import limit is N products. Currently imported: X"), see Last update / Next update / Pending execution per sync task, and use **Reset import** to start over. Visible only once the app is configured.
- **Settings** — credentials + all behaviour configuration (see below).
- **Processed products** — paginated list of products that came in via Barsy; each row shows the Barsy ID, a link to the CloudCart product, a status badge, and a **View change log** action.
- **Orders** — a Barsy-specific orders tab (unique to Barsy among the ERP apps).
- **Link modificators** — only shown when the **Product Options** app is installed and active; maps Barsy modifier groups/values (extras, add-ons) to CloudCart product-option groups/values.
- **Import history** — list of import runs with timestamps + change counts; drill into a run for field-by-field change rows.

### What the merchant CANNOT do here

- Use without a Barsy subscription/account.
- Reach Status / Processed products until credentials validate and the initial metadata fetch finishes.
- Use the integration without the **Store Locations** app installed first.

## Settings & fields

### Credentials (required, validated before saving)

- **Server URL** (`basic_url`) — the Barsy server endpoint.
- **Username**.
- **Password** (masked input).

Bad credentials show *"Invalid Barsy login details."* / *"Invalid credentials."* Changing credentials locks the save button until the merchant clicks **Validate credentials and connect** — credentials are verified before they are stored. On first connect, the platform pulls metadata from Barsy and shows live progress (*Init queue for fetch data from Barsy → Begin fetch data → Fetching queue is completed*); on failure a **Start queue process again** button retries without re-entering credentials.

### Prerequisite & location mode

- Requires the **Store Locations** app — each Barsy location links to a CloudCart store location. Missing it shows *"You need to have the app installed Store Locations so you can use the Barsy app."*
- **Single location** — one Barsy object connected to one CloudCart store location.
- **Multi-location** — multiple Barsy objects, each linked to a store location. *"You have no locations added in Barsy"* shows when Barsy exposes no objects.

### Sync behaviour

- **Action mode** — **Import and Sync** (pull the catalogue and keep it in sync) or **Sync only** (keep the existing CloudCart catalogue, refresh stock + prices only).
- **Product matching** — pick a CloudCart identifier (`compare_by`: **ID**, **SKU**, or **Barcode**) and the matching Barsy identifier (`compare_barsy`, default `article_id`). On import the link is stored in the shared [[external-record-mapping]] store — an `ExternalMetaData` row with `integration = barsy`, `external_record_key = <Barsy article_id>` → the CloudCart variant — plus the `app_import = 'barsy-<article_id>'` origin tag. On later syncs the variant is found by this stored id; a **BackfillMeta** maintenance job repopulates the mapping for any variants missing it.
- **Default category** (`default_category`) — the fallback CloudCart category for imported products that don't resolve one from Barsy.
- **Payment / shipping mapping** (`payments` / `shippings`) — map Barsy payment and shipping methods to CloudCart ones so pushed orders carry the right method.
- **Create stores** — turn each Barsy location into a CloudCart Store.
- **Only update** — when ON, only existing products are updated; new Barsy products are skipped.
- **Clear quantities** — wipe stock before re-syncing.
- **Quantity tracking** — apply a **default quantity** (`qty_default`) to imported products that have no specific stock from Barsy.

### Pricing

- **Main price** (default `actual_price`) and **Promo price** (default `none`) — chosen from Barsy price fields.
- A CloudCart **discount** can be selected to group all Barsy-discounted products.

### Delivery method

- **All suppliers without Glovo** — non-Glovo delivery options.
- **Delivery with Glovo** — orders are forwarded to Glovo for last-mile delivery. Requires the **Glovo** app with locations configured; otherwise *"You have no locations added in the Glovo app"* shows.

### Order export

- **Order export trigger** — when CloudCart pushes an order to Barsy: **New Order** (on creation), **Order complete** (at "Complete" status), or **Paid or Sent** (when paid or marked as sent).
- **Allow send order** — toggle to pause all order pushes without uninstalling.
- **Cancel reason** — pre-pick a reason sent to Barsy when an order is cancelled.
- **Close order** — when enabled, a paid/completed order with a Barsy order ID is finalised on Barsy's side with payment details (only paid orders with payment details are closed).

## Behaviour modes

Barsy's settings are not a single switch — they form **independent axes** (inbound catalogue/stock/price via **Action mode**, outbound order export via the **Order export trigger**, plus location and delivery), and a store's behaviour is the *combination* of those choices. Inbound (**Import and Sync** vs **Sync only**) and outbound (when orders push) are set, and behave, independently. The full behavioural model — each axis, its modifiers, and worked combinations — is on [[barsy-sync-modes]].

## Business rules

- **Catalogue / stock pull runs every 8 hours.** Order pushes are not scheduled — they fire on the order event (creation, payment, fulfilment, cancellation) with a short delay of a few seconds.
- **Order export timing follows the chosen trigger:** New Order fires on order creation; Paid fires when payment is reported as `completed`; Sent fires when a fulfilment is added.
- **No duplicate pushes.** Once an order has been sent to Barsy (or a push is already in flight), clicking Send again or repeated status changes will not create a second Barsy order.
- **Cancellation** — when a CloudCart order that was already sent to Barsy becomes `cancelled`, the cancellation (with the chosen cancel reason) is pushed to Barsy automatically.
- **Sync results in order history** — successful syncs log `send_erp_success`; failures log `send_erp_error` with the upstream error message, visible in [[orders-history]].
- **Import limit** — a plan-based product import cap applies; the Status tab shows current usage against the limit.
- **Reset import — re-sync, not unlink.** The Status tab's **Reset import** clears Barsy's **`last_sync` watermark** only (`removeSettings(['last_sync'])`). The next catalogue pull then re-fetches **everything** from the beginning instead of only the recent delta. It does **NOT** drop the product mapping (the `ExternalMetaData` rows / `app_import` tags) and does **NOT** delete products — so this is a full re-sync with the links intact (like [[apps-gensoft-reset-import|Gensoft]], the opposite of [[apps-microinvest-reset-import|Microinvest]]'s unlink-style reset).

## Modificators (restaurant modifier mapping)

Barsy is a POS / restaurant system, so its products carry **modificators** — modifier groups (e.g. *"Size"*, *"Extras"*, *"Sauce"*) attached to an item. Gensoft-style catalogue fields aren't enough for this, so Barsy has a dedicated **Modificators** area:

- A **Get modificators** sweep pulls Barsy's modifier groups into a local table (`modificator_id` keyed), kept fresh by a **Sync** action.
- The merchant then **links** each Barsy modificator to a CloudCart **product option** (the *Link modificators* tab) — mapping Barsy modifier groups → CloudCart option values. This tab is gated by the **Product Options** app ([[products-options-overview]]); without it the linking UI isn't available.
- Linked modificators let an order placed on the storefront (with its chosen options) translate into the right Barsy modifier selections when the order is pushed.

## Related

- [[barsy-sync-modes]] — how the settings combine into independent inbound (Import and Sync / Sync only) and outbound (order-export trigger) behaviour modes.
- [[erp-integrations]] — ERP & accounting integrations hub.
- [[external-record-mapping]] — the shared `ExternalMetaData` mapping (`integration = barsy`) the matches write to + the internal read queries.
- [[apps]] — App Store.
- [[apps-store-locations]] — **hard prerequisite**: each Barsy object links to a CloudCart store location; Barsy refuses to configure without it.
- [[apps-glovo]] — required when "Delivery with Glovo" is chosen (orders forwarded to Glovo for last-mile).
- [[products-options-overview]] — the Product Options app; gates the "Link modificators" tab (mapping Barsy modifier groups → CloudCart options).
- [[orders-history]] — Barsy sync `send_erp_success` / `send_erp_error` events appear here.
- [[order-processing-pipeline]] — the order events (create / paid / fulfilled / cancelled) that trigger the order push to Barsy.

## Open questions

_None — all questions answered above._
