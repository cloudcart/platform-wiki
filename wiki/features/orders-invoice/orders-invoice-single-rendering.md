---
type: feature
nav_path: "Orders → Order details → Invoice → PDF rendering"
route_name: admin.orders.invoice
route_path: /admin/orders/invoice/:order_id
aliases: ["Invoice PDF rendering", "Invoice template", "invoice_body", "Invoice watermark", "Invoice language", "Рендиране на фактура PDF"]
tags: [orders, invoice, pdf, mpdf, smarty, rendering]
plan_gates: ["invoices"]
created: 2026-06-10
updated: 2026-11-09
source_count: 8
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

The platform uses the **mPDF** PHP library to render invoice PDFs from Smarty-rendered HTML. mPDF supports most modern HTML / inline CSS (no JavaScript). The PDF is A4 portrait, titled *"Invoice <number>"*. The margins in the code are written in a form the current PDF library ignores, so its defaults apply: about 15 mm left and right, 16 mm top and bottom (verify on a printed copy).

### How the standard invoice fills pages

The standard template (empty `invoice_body`) has **no page-break or keep-together rule**. Its blocks run top to bottom and break wherever a page is full:

1. The top block: invoice logo, number, date, order number and its barcode. It prints once, on page 1.
2. The title, then the seller and buyer blocks side by side.
3. One table with the product lines and, under them, the totals. A long table continues on the next page, its heading row repeated (verify).
4. The **Payments** table, when **Display payment details** is on and the order has a payment; then the payment method's description, when that option is on.
5. The no-VAT reasons, when the order has them.
6. On **Bulgarian-language** invoices only: *Съставил: <name>* and *Подпис: шифър <code>*, beside the footer note (or, without one, the sentence that a code may replace a signature). Being last, this is the "signature" that lands alone on page 2 when page 1 is just full. Where the name comes from: [[settings-invoicing-issuer-block]].
7. Blocks that apps add at the end.

A centred *"Page X of Y"* line is the page footer. What pushes the last block over: more product lines, product images or barcodes in the list, the payments table, the payment description, the no-VAT reasons, header rows and a long footer note. Credit notes use the same layout. A custom `invoice_body` follows its own HTML.

The preview on Settings → Invoicing is a drawing of the sections, not the PDF: it has no page boundaries, so it cannot show where a page will break ([[settings-invoicing-template-editor]]).

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
- [[settings-invoicing-issuer-block]] — the *Съставил* name and code.
- [[orders-invoice-single-numbering]] — the rendered (formatted) number that appears on the PDF.
- [[orders-invoice-single-surfaces]] — the View-invoice link that triggers rendering.
- [[order]] — entity carrying the order locale that drives render language.

## Open questions

None.
