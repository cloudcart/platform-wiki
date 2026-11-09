---
type: feature
nav_path: "Orders → Order details → Shipping → Waybill → Print PDF"
route_name: admin.internal.print_waybill
route_path: /admin/orders/action/shipping/:order_id/print_waybill
aliases: ["Print waybill PDF", "Print shipping label", "Packing slip", "Dispatch summary", "Print PDF", "Принтиране на товарителница", "Печат", "Print labels"]
tags: [orders, shipping, waybill, pdf, print, label]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 3
---

> Part of [[orders-shipping-waybill]]. See the hub for other aspects (generate flow, courier specifics, payer side, remove/void, generic modal, API path).

# Waybill — print PDF

## Purpose

The flow for **rendering a printable PDF** of an active waybill. Which PDF the order page's **Print** gives depends on how the order is shipped: a courier's own label, or a generic platform PDF for the store's own (non-courier) methods.

## Where to find it

Two entry points:

| Button | Route | Output |
|--------|-------|--------|
| **Print** / *"Печат"* on [[orders-details]], order shipped by a **courier** (shown once the waybill exists) | the courier app's print route | The courier's own label PDF. Some couriers first ask for the format: DPD Bulgaria opens a small print-format window, then fetches the PDF from DPD. |
| **Print** / *"Печат"* on [[orders-details]], order shipped by the store's **own method** | `admin.internal.print_waybill` | Generic platform PDF (the platform code) — a packing slip / dispatch summary listing the order's products. |
| The courier app's **Shipments** tab (DPD Bulgaria, BoxNow, Econt) | per-courier | A print icon on each row (one label) and **Print labels** on the toolbar (several). A format window opens, except on DPD when its **Print paper size** is A4 or A6. |
| Admin GraphQL `getShippingWaybillPdf` | — | The same courier label, for scripts ([[waybill-api-fulfillment]]). |

## What the merchant can do here

- Click **Print** on the order → the courier's label, or the generic PDF for an own method, in a new tab.
- Print one or several labels from the courier app's **Shipments** tab.

## Settings & fields

The generic PDF has no configurable fields — it renders whatever the order currently has. The courier-formatted label inherits whatever was sent at Generate time (see [[waybill-generate-flow]]) — to change the label, the merchant must Remove (see [[waybill-remove-void]]) and re-Generate.

## Business rules

### The generic PDF is only for the store's own methods

The platform's `admin.internal.print_waybill` route renders a generic PDF with the order's products listed, not a courier label with barcodes. It is what **Print** opens for an order shipped with the store's own (non-courier) method; a courier order's **Print** opens the courier's label.

### Thermal-label print is per-courier

For real shipping-label print (barcodes + tracking number + courier's brand markings sized for 100×150mm thermal label printers), the merchant uses each courier's own integration:

- [[apps-econt]] → Print waybill (Econt's PDF endpoint).
- [[apps-boxnow]] → Print locker label.
- [[apps-dpdbulgaria-speedy|DPD Bulgaria (Speedy)]] → print-format window, then DPD's PDF.
- Other couriers: each app exposes its own print action through their own PDF endpoint.

### PDF includes only non-digital products

When opening the print form, the platform pre-fetches only products with `digital = no`. Digital products are EXCLUDED entirely. So a mixed-cart order (physical book + ebook) shows only the physical book on the printout.

### Print after Remove → no PDF

Once the waybill is removed via [[waybill-remove-void]], the print button disappears from the action row. There is no historical record of the original label PDF — the merchant must download it BEFORE voiding if they want a paper copy.

### Multi-package orders

The platform PDF lists ALL non-digital products on the order in one document — there is no per-package or per-box split. For multi-box shipments, the courier-formatted label (from the courier's app) is what handles the box numbering; the platform's summary PDF is one document for the whole order.

### Bulk printing needs the Bulk print app

Without an app, each waybill's PDF is printed per order from the order page. With the **Bulk print** app installed, **Orders → Enable Bulk print → Waybills print** issues waybills and prints the labels of many orders at once, across couriers, in **A6 thermo** or **A4** ([[apps-bulk-print-labels]]). A courier app's own **Shipments** tab can also print several labels of that one courier together ([[econt-shipments]]).

## Related

- [[orders-shipping-waybill]] — hub.
- [[waybill-generate-flow]] — the label content is fixed at Generate time.
- [[waybill-remove-void]] — Remove discards the PDF surface.
- [[apps-econt]] — Econt's per-app Print waybill action (courier-formatted).
- [[apps-boxnow]] — BoxNow locker-label print.
- [[orders-details]] — parent screen with the Print PDF button.
- [[orders]] — list page.
- [[apps-bulk-print]] — the Bulk print app: waybills and labels for many orders at once.

## Open questions

- Does the generic PDF render for orders without a generated waybill yet? (verify)
