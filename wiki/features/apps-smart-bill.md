---
type: feature
nav_path: "Apps → SmartBill"
route_name: apps.smart_bill.overview
route_path: /admin/apps/smart_bill
aliases: ["SmartBill", "Smart Bill", "SmartBill Romania", "Romanian invoicing"]
tags: [apps, erp, invoicing, romania, accounting]
plan_gates: []
created: 2026-05-22
updated: 2026-05-27
source_count: 2
---
# SmartBill (Romanian invoicing)

## Purpose

**SmartBill** integration — Romanian online accounting + invoicing platform. The Romanian counterpart to [[apps-szamlazz]] (Hungary) and [[apps-fgo]] (Bulgaria). When activated, SmartBill becomes the merchant's active invoicing provider — handling invoice generation, payment documents, credit notes, and Romanian tax compliance (e-Factura).

## Where to find it

Sidebar → Apps → install → **SmartBill**.

## What the merchant can do here

- See app status.
- Configure SmartBill API credentials in [[apps-smart-bill-settings]].
- Activate to make SmartBill the active invoicing provider.
- Generate invoices + payment documents per order.

### What the merchant CANNOT do here
- Use SmartBill without a paid SmartBill subscription.
- Run SmartBill alongside another active invoicing provider.

## Settings & fields

The settings form (per `the platform code::$only`) persists exactly these fields:

- `email`, `token`, `cif` — credentials. `cif` is the Romanian VAT identifier (one CIF per store).
- `seria`, `document_type` — series + document type (`invoice` / `proforma`). The Settings UI exposes a single dropdown that combines the two (a "Series A — Invoice" option is stored as `seria*invoice`); the platform splits it back into `seria` + `document_type` on save. So each series-plus-type combination is one entry — a proforma series can't share a number prefix with an invoice series.
- `update_quantity`, `document_language`, `automation_generate`, `only_billing`, `generate_status` — behaviour flags.
- `create_clients`, `create_products`, `warehouse_name` — SmartBill-side data-creation toggles.

`document_language` defaults to `'RO'` (Romanian); switch to EN for international customers.

### update_quantity decrements SmartBill stock

With `update_quantity = 1`, the integration tells SmartBill to decrement its OWN warehouse stock (using `warehouse_name`) for the invoiced products. **This does NOT touch CloudCart's stock** — CloudCart inventory is managed independently (see [[inventory-tracking]]). Enable this ONLY if SmartBill is the authoritative inventory system; otherwise leave it OFF to avoid duplicate stock tracking.

## Business rules

### Invoice vs payment document

SmartBill distinguishes an INVOICE (tax document) from a PAYMENT DOCUMENT (proof a payment was received) — unlike Szamlazz, which uses invoice + credit note + receipt. A payment document is a SECONDARY document referencing an existing invoice by series + number; it confirms payment, it does not replace the invoice. Typical flow: a cash-on-delivery order gets an invoice at packing, then a payment document when the COD cash is collected.

A payment document is only issued when the order ALREADY has a SmartBill invoice and the prior document was an invoice (not a proforma). It is sent as a `'Ordin plata'` (Romanian "payment order"), non-cash, referencing the original invoice.

### Auto-generation triggers

With `automation_generate = 1`, invoice generation is event-driven (no scheduled sweep):

- `OrderCreated` if `generate_status = 'new_order'`.
- `OrderStatusChange` to `completed` if `generate_status = 'completed'`.
- `OrderStatusChange` to `paid` if `generate_status = 'paid'`.
- `FulfillmentAdd` if `generate_status = 'fulfilled'`.

If `only_billing = 1` AND the order has no billing address, generation is SKIPPED.

Separately, on every `OrderStatusChange` to `paid` (regardless of `automation_generate`), a payment document is auto-issued for any order that already has a SmartBill invoice. So a merchant issuing invoices on `paid` sees two API calls at that moment — invoice, then payment document. A proforma order, or one never sent to SmartBill, gets no auto payment document.

Because there is no cron-based sweep for unbilled orders, a missed event (e.g. a failed listener) leaves an order without an invoice — the merchant must then send it manually.

### Currency

CloudCart passes the order's currency to SmartBill as-is and does NOT convert it. SmartBill receives whatever currency the order is in (RON / EUR / USD per the store's currency config) and handles any tax-driven conversion or display on its side. A merchant who needs RON-only domestic invoicing should set the CloudCart store currency to RON.

### Romanian tax compliance (e-Factura)

SmartBill transmits invoices to Romania's tax authority (ANAF) e-Factura system in real time, on the SmartBill side, at the moment of issuance — there is no CloudCart-side reporting schedule. The merchant verifies ANAF delivery in their SmartBill portal.

### Cancellation (CloudCart-side)

The merchant can cancel an issued document directly from the order detail page (route `apps.smart_bill.cancel`). On cancel, CloudCart calls SmartBill's invoice-cancel endpoint, then REMOVES all SmartBill meta from the order (`smart_bill_invoice_number`, `_type`, `_invoice_url`, `_invoice_series`) — so on CloudCart's side the order looks as if it never had a SmartBill document. SmartBill's portal retains the cancellation audit per Romanian tax law.

### Multi-store / multi-CIF

Each CloudCart store has ONE CIF, set via the `cif` setting. A merchant with multiple legal entities across multiple stores must connect each store to the correct CIF. Multiple CIFs within a single store are NOT supported.

### Test environment

There is no built-in sandbox toggle (no `environment` / `test_mode` field). To use SmartBill's test environment, the merchant enters test-account credentials in the settings.

### Side effects & permission

Activation sets `invoicing_provider = smart_bill`; invoice generation stores SmartBill's response on order meta. Standard apps permission scope applies.

## Related

- [[apps]] — App Store.
- [[apps-smart-bill-settings]] — settings sub-page.
- [[apps-szamlazz]] — Hungarian counterpart.
- [[apps-fgo]] — Bulgarian counterpart.
- [[apps-flix-facts]] — additional markets.
- [[settings-invoicing]] — invoicing provider configuration.
- [[orders-invoice]] — invoice flow.
- [[inventory-tracking]] — CloudCart's own stock model (separate from SmartBill stock).

## Open questions

(none — questions about merchant-facing behaviour have been resolved against backend)
