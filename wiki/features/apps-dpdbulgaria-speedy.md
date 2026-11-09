---
type: feature
nav_path: "Apps → DPD Bulgaria (Speedy)"
route_name: apps.dpdbulgaria.overview
route_path: /admin/shipping/dpdbulgaria, /admin/shipping/dpdbulgaria/settings, /admin/shipping/dpdbulgaria/payments, /admin/shipping/dpdbulgaria/shipments, /admin/shipping/dpdbulgaria/shipments-return, /admin/shipping/speedy, /admin/shipping/speedy/settings, /admin/shipping/speedy/payments, /admin/shipping/speedy/shipments, /admin/shipping/speedy/shipments-return
aliases: ["DPD Bulgaria", "DPD BG", "DPD Bulgaria courier", "Speedy", "Спиди", "Speedy v2", "Спиди v2", "Speedy AD", "Speedy shipping", "Speedy APT", "Speedy office"]
tags: [apps, shipping, courier, bulgaria, omniship]
plan_gates: []
created: 2026-05-22
updated: 2026-11-09
source_count: 7
---
# DPD Bulgaria (Speedy)

## Purpose

**DPD Bulgaria** integration, DPD's Bulgarian company (Geopost group): BG delivery and shipments abroad, an alternative to [[apps-econt]]. Standard OmniShip pattern: real-time quotes → bill-of-lading → tracking (see [[orders-shipping-waybill]]).

> **This is "Speedy v2".** The platform's own notice calls this app **Speedy v2**, with the same login as the old Speedy app. The old **Speedy** app (v1) is discontinued: at checkout it shows nothing, switches itself off and raises an alert to migrate here. Details: [[apps-dpdbulgaria-speedy-credentials]].

## Where to find it

Sidebar → Apps → install → **DPD Bulgaria**, or the direct routes. Standard OmniShip sub-pages: Overview, Settings, Payments, Shipments, Shipments return. Requires an active DPD contract; without one the courier cannot be used.

## What the merchant can do here

Three delivery channels are supported: `address`, `office`, `locker` (door / DPD office / APS locker) — the most flexible of the BG couriers, matching Econt. Each channel has its own enable toggle; the storefront only offers channels the merchant has enabled.

There is no fixed country list: a destination is offered when DPD returns a price for one of the selected **Services**, within the **Ships to** zone. Address matching abroad: [[apps-dpdbulgaria-speedy-parcels]].

DPD Bulgaria also supports per-order pickup-point changes after placement — the merchant or customer can update which DPD office the package departs from.

### What the merchant CANNOT do here
- Get waybills quoted in BGN — DPD always quotes in EUR (see Business rules).

## Settings & fields

Credentials: **Username** + **Password** (a `client_id` is also stored internally). A **Renew client information** button re-reads DPD's contract, sender addresses and services. Connecting, rejected logins and changing accounts: [[apps-dpdbulgaria-speedy-credentials]].

> **These are NOT the merchant's DPD website login.** The Username + Password entered here are dedicated **API / integration credentials** issued by DPD Bulgaria for connecting external platforms — they are different from the login the merchant uses for DPD's own website / client portal. Entering the website login here will not connect. A merchant who doesn't have the integration credentials should **call DPD Bulgaria and request the API credentials** for the CloudCart integration. (verify — a DPD rule, not the platform's.)

### Sender data
Pickup radio (required): **Client's address**, **Office**, or **Automat (APS locker)**. When pickup = APS, a yellow warning appears: *"Sending from a DPD Bulgaria locker (APS) requires prior authorization with DPD Bulgaria. Without valid identification, the service will not be available, regardless of the module settings."* Keys: `client_name`, `address_id`, `office_id`, `client_phone`. The **DPD location** select shows only when pickup = office (`office_id`, required); the **Automat** select (`apt_id`) shows only when pickup = apt.

### Services & per-channel rate cards

**Services** is a multi-tag select against DPD's services list. Each of the **three delivery channels — to **address**, to **office**, to **locker (Automat / APS)** — is a separate rate card with a status badge and its own enable toggle (`to_address` / `to_office` / `to_locker`).

**Per channel, the merchant picks a "Delivery price calculation" type — the same six on every channel:**

| Option | Label | What it does |
|---|---|---|
| `calculator` | **DPD calculator** | Real-time DPD-quoted price (automatic calculation of the delivery price). |
| `calculator_fixed` | **DPD calculator + processing fee** | The DPD-quoted price plus a fixed fee entered in the **Parcel processing Fee** field (`fixed_price_<channel>`). |
| `free` | **DPD calculator + free shipping** | The DPD price, but **free when the cart total before shipping is at or above** the **Minimum Order Value for Free Delivery** (empty = always free). |
| `fixed_price` | **Fixed value at price without DPD calculator** | A merchant-defined rate table keyed by **cart subtotal** tiers — DPD's quote is ignored. |
| `fixed_weight` | **Fixed weight value without DPD calculator** | A merchant-defined rate table keyed by **weight** tiers. |
| `price_and_weight` | **Fixed value for price and weight without DPD calculator** | A merchant-defined rate combining **both** subtotal and weight. |

Each calculator-based card also shows a **fallback price** sub-switch, but DPD Bulgaria never applies it: with no DPD price the channel is not offered ([[shipping-calc-rate-card-fields]]). Every card adds a **category-condition** sub-switch (different rates for products in chosen categories). The **office** and **locker** channels add a **country** multi-tag (`{channel}_countries`) controlling which countries' offices / lockers are shown. When the type is **`free`**, City / Intercity / International **free-delivery service** selects appear (International is multi-tag) so the merchant designates which DPD service fulfils the free legs. The shared field-by-type reference is on [[shipping-calc-rate-card-fields]].

### Additional settings
Parcel & waybill box (rendered first): **Who pay the shipping cost** (`side`); **Payer** (`payer_id`, only when `side = other`); **Enable cash on delivery** (`cd`); **Show cash on delivery in the ref2 field** (`cod_ref2`, needs `cd = 1`); **Add a Fiscal Receipt** (`fiscal_receipt`, needs `cd = 1`, only when contract `codFiscalReceiptAllowed = true` AND store VAT is configured); **Do not allow card payment when COD shipment** (`pos_enabled`); **Money transfer** (`money_transfer`, only when contract `moneyTransferAllowed = true`); **Declared value** (`declared_value`); **The package contains fragile** (`fragile`, needs `declared_value = 1`); **Back documents request** (`back_documents`); **Back receipt request** (`back_receipt`); **Document shipment** (`documents`); **Automatically set order status to paid** (`sync_payments`) — **paid plan-feature gated**.

General box: **Default weight for one item** (`default_weight`, required; 0.1 kg default when products lack a weight); default width / depth / height (mm); **Package type by default** (`packing`, required); **Choose a content description** (`order_content` — a dropdown of **Product name / Product SKU / Product barcode** that sets the **product-description note (заб.)** on the waybill, **not** the main **content (съдържание)** field — that shows the **order number** (`Поръчка: <order number>` → "ПОРЪЧКА # …" on the label). Shared OmniShip rule incl. the name-fallback when a product has no SKU / barcode — see [[shipping-provider-mech-waybill]]); **Submit product sizes** (`item_sizes`); **Delivery boxes** (`boxes`); **Print paper size** (`speedy_print_size`) — All / A4 / A6, drives the bulk-print flow. Parcels and boxes: [[apps-dpdbulgaria-speedy-parcels]]. A third box, last-mile settings: **Options before payment** (No options / Test before payment / Open before payment), **If the order is canceled the returning cost is paid by the merchant**, **Select return service**, **Return voucher** with its service, payer and validity, and **Tracking shipment** (In your store / On courier site).

Also standard: Name & logo, Geo zones, Payment providers, and a submit-changes sticky footer.

## Business rules

### EUR base currency
DPD quotes in **EUR**, unusual among BG couriers (Econt quotes in BGN). The platform converts the order's BGN amounts to EUR on **each** API call — at quote time and at waybill creation — so no rate is locked at order placement. The conversion currency follows the recipient country: EUR for BG, RON for RO. Because BGN is pegged to EUR, any rounding difference between displayed price and courier invoice is effectively zero for BG. The declared (insurance) amount is likewise converted to the destination currency before being sent.

### COD support
Default is receiver-pays (customer pays courier, like Cargus), door delivery on, real-time calculator pricing. COD applies when the merchant's `cd` toggle is on AND the order is within the COD cap (10000 BGN for BGN stores, or a lower custom cap); above the cap the COD option is hidden and payment must be online. When a customer changes payment method on an existing order, shipping cost recalculates — DPD's COD fee comes off when payment moves online.

### Waybill price and COD
Syncing the order to the courier's price, the history entry, the cash-on-delivery and fiscal-receipt options and the delivery options of the waybill form: [[apps-dpdbulgaria-speedy-waybill-price]].

### Other behaviours
There is no test or DEBUG mode: every waybill is a real shipment. The waybill PDF comes directly from DPD's API, fetched when the merchant prints. Bulk-print on the Shipments tab honours `speedy_print_size`; when set to All, a Print Format Select modal (A4 / A6) opens.

## Related

- [[shipping-calc-rate-models]] — rate-table semantics: when a method uses a from/to rate table (по тегло / по цена), an **empty upper bound (`до` / `to`) means no upper limit — the bracket runs to infinity** (both bounds inclusive). A blank top row is intended, not invalid, and never hides the method at checkout.
- [[apps-dpdbulgaria-speedy-waybill-price]] — waybill price, COD and waybill options.
- [[apps-dpdbulgaria-speedy-credentials]] — Speedy v1 / v2, credentials, account changes.
- [[apps-dpdbulgaria-speedy-parcels]] — parcels, boxes and foreign addresses.
- [[apps]] — App Store.
- [[apps-dpdromania]] — sister DPD operating company in Romania (different code base, different credentials).
- [[apps-gls]] — pan-European alternative.
- [[apps-econt]] — Bulgarian alternative courier.
- [[shipping]] — shipping landing.
- [[orders-shipping-waybill]] — waybill flow.
- [[orders-sync-cod]] — COD sync.

## Open questions
