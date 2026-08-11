---
type: concept
nav_path: "Concept → Invoicing & accounting"
route_name: (none)
route_path: (none)
aliases: ["Invoicing", "Accounting", "Invoices and credit notes", "E-invoicing", "Фактуриране", "Счетоводство", "Фактури и кредитни известия", "Издаване на фактури", "Accounting integration", "Issue invoice"]
tags: [invoicing, accounting, finance, fiscal, e-invoicing, concepts, hub]
plan_gates: []
created: 2026-06-11
updated: 2026-06-11
source_count: 1
---
# Invoicing & accounting

## Definition

**Invoicing & accounting** covers every way the store produces the financial documents for a sale and keeps its books — the **invoices and credit notes CloudCart issues natively**, the **Bulgarian fiscal-compliance** obligations around them, and the **external accounting / e-invoicing integrations** for merchants whose market or back-office needs a legal e-invoice or a synced ledger. This page is the map; each piece is documented on its own page.

> **Don't confuse this with [[billing-invoicing]]** — that is the invoice **CloudCart issues to the merchant** for the platform subscription. This concept is about invoices the **merchant issues to their own customers**.

## Scope

**1. Native invoicing (built in)**

- [[settings-invoicing]] — the 3-tab config: layout, numbering, what prints, credit-note refund rules, raw PDF templates.
- [[orders-invoice]] — issue a single invoice from an order (eligibility, numbering, rendering, customer email).
- [[orders-credit]] — credit notes (eligibility, document, numbering).
- [[orders-invoices]] — the cross-order invoice list (table, filters, bulk), with [[orders-invoices-download]] (bulk PDF) and [[orders-invoices-export]] (accounting export).

**2. Fiscal compliance (Bulgaria / Наредба Н-18)**

- [[tax-computation]] — the VAT lines on every invoice.
- [[apps-n18-audit]] — the Наредба Н-18 audit-file register.
- [[online-sales-without-cash-register]] — when the courier issues the fiscal receipt for COD (no merchant cash register).
- [[apps-profisc]] — fiscal-device integration.

**3. External accounting / e-invoicing apps**

- One **active invoicing provider** can take over issuance per market: [[apps-fgo]] (Bulgaria), [[apps-szamlazz]] (Hungary — with its own invoice / credit-note / receipt flows), [[apps-smart-bill]] (Romania).
- [[apps-flix-facts]] — accounting connector that syncs on order status change.
- Back-office ledger sync via [[erp-integrations]] (Microinvest, Gensoft, Barsy, …).

## Contrasts

- **Native PDF invoice vs external e-invoice.** CloudCart's native invoice is a PDF for general use; in markets that mandate legal e-invoicing an app ([[apps-smart-bill]] / [[apps-szamlazz]] / [[apps-fgo]]) becomes the **active invoicing provider** and issues the compliant document instead.
- **Invoice vs fiscal receipt (касов бон).** An invoice is an accounting document; the fiscal receipt is a separate legal document produced by a fiscal device or — for COD — by the courier (see [[online-sales-without-cash-register]]).
- **Customer invoices vs your subscription invoices.** Everything here is merchant → customer; [[billing-invoicing]] is CloudCart → merchant.

## Where it applies

- Invoices are issued against a placed order; tax + totals are snapshotted at placement — see [[order-processing-pipeline]] and [[tax-computation]].
- B2B fields (company, VAT ID) on the billing address feed the invoice — see [[api-order-billing-address]] and [[settings-invoicing]].

## Related

- [[settings-invoicing]] — the central configuration screen.
- [[tax-computation]] — VAT on invoices.
- [[erp-integrations]] — back-office accounting sync.
- [[online-sales-without-cash-register]] — the COD fiscal-receipt regime.
- [[billing-invoicing]] — (contrast) the merchant's own platform-subscription invoices.

## Open Questions

- Precedence when both native invoicing **and** an external active provider are enabled (verify which issues the customer-facing document).
- Whether credit-note export covers all external providers uniformly (verify).
