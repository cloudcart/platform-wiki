---
type: feature
nav_path: "Orders → Order details → Invoice"
route_name: admin.orders.invoice
route_path: /admin/orders/invoice/:order_id
aliases: ["Invoice", "View invoice", "Generate invoice", "Order invoice", "Фактура", "Издаване на фактура"]
tags: [orders, invoice, pdf, invoicing, smarty]
plan_gates: ["invoices"]
created: 2026-05-21
updated: 2026-06-10
source_count: 7
---
# Invoice (per order)

## Purpose

The **invoice generation and download flow** for a single order. When the merchant clicks **View invoice** on the [[orders-details]] page (or hits the route directly), the platform routes the request to the active **Invoicing provider** (configured via [[settings-invoicing]] / the installed invoicing app), which returns the rendered PDF. The merchant downloads it inline or opens it in a new tab.

The merchant also has access to a **Manual invoice number** dialog (when the platform's `invoice_number_type` is set to manual mode) — used when the merchant needs to assign a specific invoice number rather than the next auto-generated one.

This page is the **hub** for the per-order invoice cluster. The detailed mechanics live in the five aspect pages below — drill into the one that matches the question rather than reading all of them.

## Sub-pages (in this cluster)

This feature is split into 5 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question.

- [[orders-invoice-single-surfaces]] — the four distinct UI surfaces wired into [[orders-details]] (Create-invoice button, manual-number modal, View-invoice PDF link, external-app rows) and which one shows when.
- [[orders-invoice-single-numbering]] — the `invoice_generate` vs `invoice_number_type` distinction; the three numbering modes; sequential `max + 1` generation; manual-number validation; rendered prefix/suffix/token format.
- [[orders-invoice-single-eligibility]] — the gates that decide when an invoice can be issued: `invoices` plan feature, active provider, order-status eligibility, billing-address requirement, number permanence.
- [[orders-invoice-single-rendering]] — server-side PDF rendering (mPDF), template customisation via `invoice_body`, render language, voided/cancelled watermark, PDF protection flags, the no-op `output` parameter.
- [[orders-invoice-single-customer-email]] — the `sendInvoice` email that fires on manual generation, its global-only gating, external-mode failure handling, and why re-issuing is not supported.

## Where to find it

From [[orders-details]] → **View invoice** action in the header toolbar.

The action is visible only when an Invoicing provider is active AND a raw invoice number already exists on the order. The full set of visibility conditions and the four entry-point surfaces are documented on [[orders-invoice-single-surfaces]]; the gating logic is on [[orders-invoice-single-eligibility]].

Route: `/admin/orders/invoice/{order_id}/{output?}` where `output` is `I` (inline) or `D` (download). Defaults to `I`. The `output` parameter is effectively a no-op — see [[orders-invoice-single-rendering]].

Sibling route for manual invoice number assignment: `/admin/orders/generate-invoice/{order_id}` (GET to open dialog, POST to save).

## What the merchant can do here

- **View / download** the invoice PDF — opens in a new tab (inline output `I`); use the browser print / save dialog to keep a local copy.
- **Assign a manual invoice number** when `invoice_number_type = 2` — via the small modal documented on [[orders-invoice-single-surfaces]].

### What the merchant CANNOT do here

- Edit the invoice's content (line items, prices, dates) directly — those come from the order itself. To change what's on the invoice, the merchant edits the order on [[orders-details]] before generating.
- Re-render with a different template — the template is determined by the active Invoicing provider in [[settings-invoicing]].
- Delete or re-issue an issued invoice — once a number is consumed it's part of the audit trail. See [[orders-invoice-single-eligibility]] for permanence and [[orders-invoice-single-customer-email]] for why re-issue is unsupported.

## Settings & fields

The invoice's appearance (logo, layout, line items, totals, footer, VAT-exemption text) is rendered as a Smarty PDF fed by the Invoicing layer and customised on [[settings-invoicing]]. The two commonly-confused controls — `invoice_generate` (WHEN the number is assigned) and `invoice_number_type` (WHAT source provides it) — are documented in full on [[orders-invoice-single-numbering]].

Sub-template includes: manual-number dialog, payment-lines section, line-items section, expected-delivery-date section, totals block (subtotal / discount / tax / total), and VAT-exemption reason text for B2B / EU reverse-charge invoices.

## Business rules

- **Invoice generation is gated by an active Invoicing provider** — without one, the **View invoice** button doesn't render and the route returns 404. See [[orders-invoice-single-eligibility]].
- **Invoice numbers are per-order and permanent** — once generated, the number stays attached even if the order is voided / cancelled / refunded, and is never reused. See [[orders-invoice-single-eligibility]].
- **Receipt vs invoice are different documents** — the platform also exposes a **receipt** route at `/admin/orders/receipt/{order_id}`, a simpler proof-of-payment document; an invoice is a full tax document. Both render through the Invoicing facade with different templates.
- **The customer is emailed the PDF on manual generation** — gated by the store-wide `customer_email_notifications` setting only, NOT the per-order `notify_customer` flag. See [[orders-invoice-single-customer-email]].

## Plan gates

This feature is gated by the following plan-features (see [[plan-gates]] / [[plan-vs-feature-pack]] / [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `invoices` | Access gate (URL family `invoices`) | The merchant-facing invoicing surface ([[orders-invoices]] cross-order list AND the per-order **View invoice** / **Generate invoice** actions surfaced from [[orders-details]]) is gated on the `invoices` plan feature. When the merchant's plan lacks the feature, the plan middleware blocks access — the cross-order list page redirects to [[plan-features]], and the per-order **View invoice** action button is hidden on the order detail page even when an invoice number exists. |

When the gate is hit, the merchant is redirected to [[plan-features]] for the per-feature upsell. `invoices` is a boolean access gate — it requires a plan that includes the feature; it does NOT extend via feature packs ([[plan-vs-feature-pack]]). NOTE: this is DISTINCT from the store-wide `invoicing` setting in [[settings-invoicing]] AND from the per-order `invoice_number` field. The plan-feature gate sits above both. See [[orders-invoice-single-eligibility]] for how the gate interacts with the other eligibility conditions.

## Related

- [[invoicing-and-accounting]] — invoicing & accounting concept hub.
- [[orders-details]] — parent page (View invoice button lives here).
- [[orders-credit]] — credit-note flow (sister document for refunds).
- [[settings-invoicing]] — invoice template + numbering configuration.
- [[apps]] — external invoicing apps (Szamlazz, FGO, SmartBill, FlixFacts, etc.) implementing the invoice interface.
- [[apps-szamlazz-orders-invoice]] — the Szamlazz external-invoicing per-app surface.
- [[orders-invoices]] — cross-order invoice list.
- [[orders]] — parent list.
- [[order]] — entity page.

## Open questions

None.
