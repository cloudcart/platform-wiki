---
type: concept
nav_path: "Concept → Shipping provider mechanism → Waybill generation"
aliases: ["Waybill generation", "Bill of Lading", "AWB", "Shipping label", "Tracking number", "Issue waybill", "Етикет", "Товарителница", "Бил оф лейдинг", "Издаване на товарителница"]
tags: [shipping, couriers, providers, waybill, fulfillment, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[shipping-provider-mechanism]]. See the hub for the other aspects (configuration, pricing models, pickup points, COD, geo routing, status tracking).

# Shipping provider mechanism — Waybill generation

## Definition

**Waybill generation** is the per-order merchant action that issues a tracking label via the carrier's API once the order is ready to ship. Across carriers the document goes by different names — *Bill of Lading* (Econt), *AWB* (international), *shipping label*, *товарителница* — but the lifecycle is identical: the merchant clicks the waybill action on the order, the platform packages the order data into a carrier-specific API request, the carrier returns a tracking number + a printable label, and the platform records both on the order and surfaces them to the customer.

This is the moment the order transitions from "I owe a package" to "the carrier has it" — the [[shipping-status]] enum flips to `dispatched` (or the carrier's equivalent), and from this point on the carrier's webhooks ([[shipping-provider-mech-status-tracking]]) drive further status updates.

## Scope

Covered:

- The 5-step waybill flow.
- What data is sent in the API request.
- What's returned and how it surfaces.
- Return waybills for customer-initiated returns.
- Label print formats (PDF / ZPL).

Not covered:

- The pickup point passed in the request — see [[shipping-provider-mech-pickup-points]].
- COD amount + COD-paid sync — see [[shipping-provider-mech-cod]].
- Currency conversions on the COD amount at API-call time — see [[shipping-provider-mech-geo-routing]].
- Post-dispatch status updates — see [[shipping-provider-mech-status-tracking]].
- Per-carrier waybill API specifics — see each carrier's app page.
- The UI of the per-order waybill action — see [[orders-shipping-waybill]].

## Contrasts

- **Waybill vs. tracking number**: the waybill is the *printable label* attached to the parcel (PDF / ZPL file the merchant prints). The tracking number is the *identifier* the carrier issues so the customer can check delivery progress on the carrier's tracking page. Both are returned in the same API response.
- **Outgoing waybill vs. return waybill**: a normal waybill ships the package from the merchant *to* the customer. A return waybill ships it back *from* the customer *to* the merchant — used for customer-initiated returns. The sender / receiver fields are swapped, and the COD flag is usually off on returns. Configured per-carrier (e.g., Econt's Shipments Return tab).
- **Pre-payment waybill vs. post-payment waybill**: most merchants wait until the order is paid before issuing the waybill, so a failed payment doesn't ship goods. The platform doesn't block issuing a waybill on an unpaid order — that's the merchant's discipline. (verify — whether any plan-gate or per-carrier toggle enforces "must be paid" before waybill.)

## Where it applies

### The 5-step waybill flow

After the order is paid, the merchant generates a waybill via [[orders-shipping-waybill]] to dispatch the package. The flow:

1. **Merchant opens the order** in [[orders-details]] and clicks the waybill action.
2. **The platform calls the carrier's `createBillOfLading` / `createAWB` / equivalent API** with the order data — see "What data is sent" below.
3. **The carrier returns a tracking number** + a printable label, which the platform stores on the order and surfaces in the order details + the customer's order-confirmation page.
4. **The order's [[shipping-status]] flips to `dispatched`** (or the carrier's equivalent enum value).
5. **The merchant prints the label** (returned as a PDF / ZPL file by some carriers) and attaches it to the package; the carrier picks up the package per the configured pickup schedule.

### What data is sent in the API request

The merchant's saved configuration ([[shipping-provider-mech-configuration]]) plus the order-specific data ride along in the request:

- **Sender address** — from the merchant's sender address book; for multi-warehouse setups, the warehouse picked on this order.
- **Recipient address** — the customer's delivery address (for "to address" channel) OR the pickup-point identifier (for "to office" / "to locker" channels, per [[shipping-provider-mech-pickup-points]]).
- **Package dimensions + weight** — from [[settings-boxes]] and the line items' physical weights. Carriers use this for tariff calculation and locker-size validation.
- **Delivery channel** — to address / to office / to locker.
- **COD amount + currency** — when the order is COD ([[shipping-provider-mech-cod]]).
- **Insurance amount** — when the merchant flagged the package for insurance.
- **Additional services** — fragile, signature required, hazardous goods, etc.

**These values are editable in the waybill form at generation.** The merchant can adjust the COD amount, insurance amount, weight, contents, package type and payer side before issuing the label — the values entered there are what gets transmitted to the carrier, not necessarily the order's stored figures. The **COD amount** entered is stored back on the order as `cod_manual` and re-used on later waybills (so it can diverge from the live order total — see [[shipping-provider-mech-cod]] → *How the collected COD amount is determined*). The **insurance amount** defaults to the order total excluding shipping.

For multi-currency stores, the COD / insurance / subtotal amounts may be converted to the carrier's billing currency at API-call time — see [[shipping-provider-mech-geo-routing]].

### Parcel contents & content description (`order_content`)

The waybill carries two editable text fields, and it is easy to confuse them:

- **Contents (съдържание)** — defaults to the **order number**: `Поръчка: <order number>`. On the printed label this is what prints as **съдържание** (e.g. "ПОРЪЧКА # 178476").
- **Content description / note (заб.)** — the **product-level** description. Its text is chosen by the courier's **"Choose a content description"** setting (`order_content`), a dropdown of **Product name / Product SKU / Product barcode**. This lands in the note (**заб.**) field, **separate** from the order-number contents field — so `order_content` does **not** change the "съдържание"; it changes the product note.

**Per-product fallback:** when `order_content` is set to **SKU** or **barcode** but a given product has none, that product's **name** is used for that line instead; identical descriptions are de-duplicated and comma-joined. So a product missing its SKU / barcode still shows a readable name.

This is **shared behaviour across every OmniShip courier that issues waybills and exposes `order_content`** — [[apps-econt|Econt]], [[apps-dpdbulgaria-speedy|DPD Bulgaria / Speedy]], [[apps-sameday|Sameday]], [[apps-cargus|Cargus]], and others (each courier page just notes the setting and links here). One nuance: some couriers' waybill forms merge the two into a single prefilled `Поръчка: <order number>, <product description>` textarea, but the printed label still separates order-number-as-съдържание from product-description-as-note.

### What's returned + how it surfaces

The carrier responds with:

- **Tracking number** — stored on the order; rendered as a clickable link in the order admin and the customer's order page (link goes to the carrier's tracking site).
- **Label file** — PDF (most carriers) or ZPL (label-printer format used by some carriers). The merchant downloads / prints the file and attaches it to the parcel.
- **Status update** — the carrier acknowledges the waybill was created; CloudCart flips [[shipping-status]] to `dispatched`.

If the carrier API rejects the request (invalid pickup point, oversized package, expired credentials, etc.), the platform surfaces the carrier's error inline on the order so the merchant can correct and retry.

### Return waybills

Some carriers also offer **return waybills** for customer-initiated returns — managed under each carrier's app sub-page (e.g., Econt's Shipments Return tab). The flow is analogous but the sender / receiver are swapped: the customer becomes the sender, the merchant the receiver. Often used in conjunction with the order-credit / refund flow ([[orders-credit]]).

## Related

- [[shipping-provider-mechanism]] — hub.
- [[orders-shipping-waybill]] — the per-order action UI.
- [[shipping-status]] — the enum flipped to `dispatched` after a successful waybill.
- [[shipping-provider-delivery-channels-waybill]] — sister entity-side documentation of channels + waybill mapping.
- [[shipping-provider-mech-configuration]] — sender address book + carrier credentials feeding the request.
- [[orders-details]] — per-order edit hub where the action lives.
- [[settings-boxes]] — package dimensions for the request.
- [[shipping-provider-mech-status-tracking]] — what happens after dispatch.
- [[orders-credit]] — refund flow that can pair with a return waybill.
- [[apps-econt]] / [[apps-dpdbulgaria-speedy|Speedy]] / [[apps-boxnow]] / [[apps-cargus]] / [[apps-dhl]] — per-carrier waybill API specifics.

## Open Questions

- ⏸️ Whether the platform enforces "order must be paid" before allowing waybill generation, or whether that's purely merchant discipline. (verify per carrier and per global setting.)
- ⏸️ The exact label format (PDF vs. ZPL vs. PNG vs. ZIP-of-labels) per carrier — needs a per-carrier reference list.
