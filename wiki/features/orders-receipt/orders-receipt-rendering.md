---
type: feature
nav_path: "Orders → Order details → Receipt → Rendering"
route_name: admin.orders.receipt
route_path: /admin/orders/receipt/:order_id
aliases: ["Receipt rendering", "Receipt PDF format", "Receipt thermal size", "Receipt language", "Receipt currency", "Receipt filename", "Receipt powered by footer", "Receipt template"]
tags: [orders, receipt, pdf, rendering, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---
> Part of [[orders-receipt]]. See the hub for the other aspects (surfaces, eligibility, numbering).

# Receipt — rendering (per order)

## Purpose

Explains **how the receipt PDF is produced and what it looks like**: the small thermal-receipt paper size, print-only protection, the language and currency it renders in, the download filename pattern, the N18-controlled template, and the plan-gated "Powered by" footer. This is the aspect to read for any *"why is the receipt tiny / in the wrong language / not editable / showing the CloudCart footer"* ticket.

## Where to find it

The receipt PDF is opened from the *"Order receipt #&lt;number&gt;"* link in the **Order history** section of [[orders-details]] (see [[orders-receipt-surfaces]]). The route is `/admin/orders/receipt/{order_id}/{output?}` with `output` = `I` (inline, default) or `D` (download).

## What the merchant can do here

- Open the PDF inline (`I`) in a new tab, or download it (`D`).
- Print it from the browser, or save it locally.

The merchant CANNOT change the layout, language, or currency from the admin UI — all are derived automatically (below).

## Settings & fields

The receipt's layout (logo, totals, signature lines, QR code) is rendered by the N18 Audit app's receipt template; the merchant cannot customise it from the admin UI. Logo and store details are pulled from the store settings. The receipt typically does NOT include the customer's full legal company info (that is the invoice's job — see [[orders-invoice]]).

**Three distinct templates, three distinct settings.** The `print_body` setting on [[settings-invoicing]] is for the **Print Order** action (the merchant's quick print from the order header), NOT for receipts or invoices. Receipts use a fixed N18-Audit template; invoices use the `invoice_body` setting if customised.

## Business rules

### PDF format is small thermal-receipt size (`B`), not A4

Unlike the invoice (A4 portrait, 20 mm margins) the receipt PDF uses `format = B` — a smaller paper format closer to thermal-receipt width — with very tight 4 mm margins all around and no header/footer margins. This is intentional: receipts are designed to print on small receipt printers or be glanced at on a phone. Merchants printing receipts on A4 paper will see them centred with significant white space.

### PDF protection — print-only (no modify, no copy)

The receipt PDF carries protection allowing ONLY print. Unlike the invoice (which allows modify and copy), the receipt is locked down — recipients cannot copy text out of it or modify it. This matches the receipt's role as proof-of-payment evidence.

### Render language — the order's locale, not the site default

The receipt PDF wraps its rendering in a language-switching callback that activates the order's stored `locale` (the customer's checkout language). The store's primary language is NOT used unless the order has no locale. This ensures the customer's receipt always renders in the language they used to place the order, even if the merchant later changed the storefront default.

### Currency — the order's stored currency

The receipt renders amounts in the order's stored currency (BGN / EUR / USD / etc. as captured at checkout). The store's default currency is irrelevant for the receipt's display — the customer sees the figures they actually paid in.

### Filename pattern when downloaded

In download mode (`D`) the PDF is named `order_<order_number>_receipt_<YYYY-MM-DD>.pdf`, where the date is the order's `date_added`. The inline route (`I`) returns it as `receipt.pdf`, since the browser handles display.

### Same render stack as the invoice

The receipt is rendered as HTML by the Invoicing provider, then converted to PDF using the platform's PHP PDF library (typically mPDF). Styling uses inline CSS optimised for print. The route returns the PDF binary with `content-type: application/pdf` — no AJAX / no Vue, a direct browser response, typically via an `<a target="_blank">` link.

### "Powered by" footer — only below a plan threshold

Below a configurable plan-level threshold, the receipt PDF gets a small *"Powered by CloudCart"* footer line. On higher-tier plans (the `showPoweredBy` toggle returns false), the footer is omitted. This mirrors the invoice / credit-note behaviour.

## Related

- [[orders-receipt]] — hub.
- [[settings-invoicing]] — the `print_body` / `invoice_body` settings the receipt is deliberately independent of.
- [[apps-n18-audit]] — owns the receipt template layout.
- [[orders-invoice-single-rendering]] — the A4 invoice render this is contrasted against (format, margins, protection).
- [[order]] — entity carrying `locale`, currency, `date_added`, order number.

## Open questions

None.
