---
type: feature
nav_path: "Orders → Order details → Shipping → Waybill → Print PDF"
route_name: admin.internal.print_waybill
route_path: /admin/orders/action/shipping/:order_id/print_waybill
aliases: ["Print waybill PDF", "Print shipping label", "Packing slip", "Dispatch summary", "Print PDF", "Принтиране на товарителница"]
tags: [orders, shipping, waybill, pdf, print, label]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[orders-shipping-waybill]]. See the hub for other aspects (generate flow, courier specifics, payer side, remove/void, generic modal, API path).

# Waybill — print PDF

## Purpose

The flow for **rendering a printable PDF** of an active waybill. Two distinct PDFs exist depending on which button the merchant clicks — and only ONE of them is the actual courier-formatted barcode label.

## Where to find it

Two entry points:

| Button | Route | Output |
|--------|-------|--------|
| **Print PDF** (in the order's shipping action row on [[orders-details]]) | `admin.internal.print_waybill` | Generic platform PDF template (the platform code) — a packing slip / dispatch summary listing the order's products. |
| **Print waybill** (inside the courier-specific app — e.g., [[apps-econt]] → order action) | per-courier `apps.<courier>.print_waybill` | Courier-formatted thermal label (100×150mm) with the courier's barcodes, addresses, COD info, and tracking glyphs. |

## What the merchant can do here

- Click Print PDF → opens the generic platform PDF in a new tab (`target="_blank"`).
- Click Print waybill (from the courier's app) → downloads the actual courier label suitable for thermal label printers.

## Settings & fields

The generic PDF has no configurable fields — it renders whatever the order currently has. The courier-formatted label inherits whatever was sent at Generate time (see [[waybill-generate-flow]]) — to change the label, the merchant must Remove (see [[waybill-remove-void]]) and re-Generate.

## Business rules

### Platform-side print PDF is GENERIC, not courier-formatted

The platform's `admin.internal.print_waybill` route renders a generic PDF template with the order's products listed — it's NOT the courier-formatted label with barcodes and tracking info. The actual courier label (with thermal-printer barcode) is downloaded SEPARATELY from each courier's app — e.g., Econt's "Print waybill" action gets the courier's PDF.

The platform-side print-PDF is more like a packing-slip / dispatch summary than a courier label. A merchant clicking the generic "Print PDF" from the waybill area on the order details should NOT expect a thermal-label-formatted output.

### Thermal-label print is per-courier

For real shipping-label print (barcodes + tracking number + courier's brand markings sized for 100×150mm thermal label printers), the merchant uses each courier's own integration:

- [[apps-econt]] → Print waybill (Econt's PDF endpoint).
- [[apps-boxnow]] → Print locker label.
- Speedy → Print label (Speedy's PDF endpoint).
- Other couriers: each app exposes its own print action through their own PDF endpoint.

### PDF includes only non-digital products

When opening the print form, the platform pre-fetches only products with `digital = no`. Digital products are EXCLUDED entirely. So a mixed-cart order (physical book + ebook) shows only the physical book on the printout.

### Print after Remove → no PDF

Once the waybill is removed via [[waybill-remove-void]], the print button disappears from the action row. There is no historical record of the original label PDF — the merchant must download it BEFORE voiding if they want a paper copy.

### Multi-package orders

The platform PDF lists ALL non-digital products on the order in one document — there is no per-package or per-box split. For multi-box shipments, the courier-formatted label (from the courier's app) is what handles the box numbering; the platform's summary PDF is one document for the whole order.

### No bulk print

There is no bulk-print action on the [[orders]] list page. Each waybill's PDF is downloaded per-order. For high-volume merchants, the courier's own dashboard typically provides a batch-print queue.

## Related

- [[orders-shipping-waybill]] — hub.
- [[waybill-generate-flow]] — the label content is fixed at Generate time.
- [[waybill-remove-void]] — Remove discards the PDF surface.
- [[apps-econt]] — Econt's per-app Print waybill action (courier-formatted).
- [[apps-boxnow]] — BoxNow locker-label print.
- [[orders-details]] — parent screen with the Print PDF button.
- [[orders]] — list page (no bulk print).

## Open questions

- Does the generic PDF render for orders without a generated waybill yet? (verify)
