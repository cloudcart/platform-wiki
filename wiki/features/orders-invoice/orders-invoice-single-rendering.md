---
type: feature
nav_path: "Orders → Order details → Invoice → PDF rendering"
route_name: admin.orders.invoice
route_path: /admin/orders/invoice/:order_id
aliases: ["Invoice PDF rendering", "Invoice template", "invoice_body", "Invoice watermark", "Invoice language", "Рендиране на фактура PDF"]
tags: [orders, invoice, pdf, mpdf, smarty, rendering]
plan_gates: ["invoices"]
created: 2026-06-10
updated: 2026-06-10
source_count: 7
---
> Part of [[orders-invoice]]. See the hub for the other aspects (action surfaces, numbering, eligibility, customer email).

# Invoice — PDF rendering (per order)

## Purpose

Describes **how the invoice PDF is produced**: the mPDF rendering engine, the standard-vs-custom template switch (`invoice_body`), the render language resolution, the voided/cancelled watermark, the PDF protection flags, and the no-op `output` parameter. This is the aspect to read for "the invoice looks wrong / is in the wrong language / shows a watermark" tickets.

## Where to find it

Rendering happens when the merchant opens `/admin/orders/invoice/{order_id}` (the View-invoice link, Surface C on [[orders-invoice-single-surfaces]]). Template and watermark configuration live on [[settings-invoicing]].

## What the merchant can do here

- Open the rendered PDF inline in a new tab and use the browser print / save dialog.
- Customise the template body and watermark text on [[settings-invoicing]] (HTML knowledge required for a custom body).

## Settings & fields

The renderer reads `invoice_body` (custom template HTML), `invoice_watermark` (watermark string), and the standard layout settings from [[settings-invoicing]]. The order's stored locale drives the render language.

## Business rules

### PDF rendering — mPDF

The platform uses the **mPDF** PHP library to render invoice PDFs from Smarty-rendered HTML. mPDF supports most modern HTML / inline CSS (no JavaScript). The PDF is rendered in A4 portrait with 20 mm margins, with the title set to *"Invoice <number>"*.

### Custom template via `invoice_body`

When `invoice_body` on [[settings-invoicing]] is EMPTY, the platform renders the standard invoice Smarty template. When `invoice_body` has content, the platform renders the merchant's custom HTML template — supporting placeholder substitutions for invoice fields (variables resolved through the platform's order-print helper). So the merchant CAN customise the template via the Invoicing settings page, but with HTML knowledge required.

### Render language — order's locale, then site primary, then admin

The platform sets the rendering locale to the order's stored locale before rendering. So the invoice renders in:

1. The order's stored locale (set at checkout based on the storefront language the customer used).
2. Falling back to the site's primary language (the merchant's storefront default).
3. Falling back to the admin's language.

The invoice is NOT rendered in the merchant-admin's current session language — it follows the customer's order context.

### Voided / cancelled invoices render with a watermark (BG sites)

For Bulgarian-locale invoices, the PDF carries a watermark string. When the order is in a status OTHER than `paid` / `completed` / `pending` AND has no credit note, the watermark uses the configured `invoice_watermark` setting OR falls back to *"Voided"* (`sf.order.status_voided`). For normal active invoices the watermark renders *"Original"* (`order.invoice.type.original`). The watermark is shown at 10 % opacity, drawn in Arial. This applies only when the order's locale is `bg`.

### PDF protection — print / modify / copy granted

The generated invoice PDF carries DRM-style protection flags with the explicit grant list `modify`, `print`, `copy`. Most viewers honour these flags.

### Output `I` vs `D` parameter — unused, always inline

The route accepts an `output` parameter (`I` inline, `D` download), but the platform does not branch on it — the download controller ALWAYS returns the PDF binary as a raw response with `content-type: application/pdf`. Whether it opens inline or downloads is decided by the browser's PDF handler, not the route. The `D` variant is a route-shaped no-op legacy alias.

## Related

- [[orders-invoice]] — hub.
- [[settings-invoicing]] — `invoice_body`, `invoice_watermark`, layout settings.
- [[orders-invoice-single-numbering]] — the rendered (formatted) number that appears on the PDF.
- [[orders-invoice-single-surfaces]] — the View-invoice link that triggers rendering.
- [[order]] — entity carrying the order locale that drives render language.

## Open questions

None.
