---
type: feature
nav_path: "Apps → Profics"
route_name: apps.profics.overview
route_path: /admin/apps/profisc
aliases: ["Profics", "Profisc", "Profics POS", "Profics integration"]
tags: [apps, administration, pos, retail, niche]
plan_gates: []
created: 2026-05-22
updated: 2026-05-28
source_count: 2
---
# Profics (POS / ERP)

## Purpose

**Profics / ProfiscAL** integration — connects CloudCart to **Profisc**, Albania's fiscal-invoicing platform (similar role to [[apps-szamlazz]] in Hungary or [[apps-smart-bill]] in Romania, but for Albania's e-invoicing system). When activated, each completed/paid order is submitted to Profisc for fiscal numbering + compliance reporting.

Supported countries (per the platform code): `ALB` (Albania), `GRC` (Greece), `MKD` (Macedonia), `RKS` (Kosovo), `MNE` (Montenegro), `ITA` (Italy) — covering merchants who sell into Albanian-fiscal jurisdictions.

Invoices are issued in Albanian Lek (`ALL`) — CloudCart auto-converts other currencies using its currency-rate model before sending.

(Note: the wiki slug is `apps-profisc.md`; the actual app key is `profics`. Profisc.al is the company URL.)

## Where to find it

Sidebar → Apps → install → **Profics**. See [[apps-profisc-settings]] for configuration.

## What the merchant can do here

- Configure Profics API credentials.
- Validate credentials (`isValidCredentials`).
- Format orders for Profics export (`formatOrder($orderId)`).
- Sync orders / inventory on configured triggers.

### What the merchant CANNOT do here
- Use without a Profics subscription / license.

## Settings & fields

Manager exposes:
- `appInfo` — App Store metadata.
- `isValidCredentials` — credential validity check (distinct from generic the configured check).
- `formatOrder($orderId)` — converts CloudCart order to Profics's expected format.

## Business rules

### Standard ERP pattern

Same event-driven model as other Administration ERP apps — status changes trigger sync; failures appear in [[orders-history]] as `send_erp_error`.

### Permission

Standard apps permission scope.

## Related

- [[apps]] — App Store.
- [[apps-profisc-settings]] — settings sub-page.
- [[apps-microinvest]] / [[apps-posmaster]] — alternative BG POS / ERP systems.
- [[orders]] — orders synced.
- [[orders-history]] — sync events appear here.

## How it works (verified against backend)

### Cloud-hosted, REST API

Profisc is a CLOUD service. The integration calls `https://onlineapi.profisc.al/` (production) or `https://demoapi.profisc.al/` (test mode). No local server, no FTP — pure HTTPS REST.

### Test mode is built-in

Per the `test_mode` setting: when `test_mode = 1`, all API calls go to `demoapi.profisc.al` (sandbox). When `0`, they go to `onlineapi.profisc.al` (live). The merchant flips this in Settings without re-installing — useful for verifying the setup before going live.

### Auto-submission on order paid / completed

When `send_order = 1` AND the order's status changes to `paid` or `completed`, the platform queues a `profics_send_order` background job — which formats the order and submits it to Profisc.

On success: `profics_invoice_id` is stored on the order's meta, and the order history shows `send_erp_success` with the QR URL from Profisc.

On failure: order history shows `send_erp_error` with Profisc's error message — visible to the merchant in [[orders-history]].

### Required settings (8 fields)

All of these must be populated:
- `username` + `password` — Profisc account credentials.
- `country` — country code (one of: `ALB`, `GRC`, `MKD`, `RKS`, `MNE`, `ITA`).
- `seller` — which legal entity to use (the merchant may have multiple companies on one Profisc account).
- `branch` — which physical branch / object to associate the invoice with.
- `tcr` — Electronic cash register identifier (TCR — Tatim Cash Register, Albanian fiscal-device terminology).
- `send_order` — toggle (1 = auto-submit, 0 = manual).
- `test_mode` — toggle (1 = sandbox, 0 = live).

Additional optional: `op_code` — Operator code (when the merchant uses Profisc's named-operator feature).

Note: the configured-check also validates credentials live — so a misconfigured Profisc account also blocks operations.

### Invoice payload defaults

Default values in the invoice payload:
- `currency = 'ALL'` (Albanian Lek) — non-ALL orders are auto-converted via CloudCart's currency model.
- `taxScheme = 'Normal'`.
- `paymentTerm = 10` days.
- `bankorCash`: when `order.payment.provider == 'cod'` → `'BANKNOTE'` (cash); otherwise → `'CARD'`.
- `invoiceType = 'invoice'`.
- `sendEInv = false` — e-invoice flag explicitly off (basic invoice flow; e-invoice may require separate Profisc-side configuration).

The invoice number sent to Profisc as `invoiceId` is sourced from CloudCart's active invoicing provider (the invoice number or the receipt number, depending on the active invoicing setup). So the merchant typically runs Profisc ALONGSIDE another invoicing app (FGO / SmartBill / built-in) which provides the formal invoice number; Profisc receives the order data + that number for fiscal stamping.

### Multi-company / multi-branch support

The merchant's Profisc account may host multiple `seller` (companies) + `branch` (physical objects) — the API exposes them and the Settings UI picks one per CloudCart store. Multi-store merchants connect each CloudCart store to its corresponding seller+branch on Profisc.

### Slug typo

The wiki file is `apps-profisc.md` (with 'sc') but the actual app key in code is `profics` (with 'cs'). Profisc.al is the platform's domain. Wikilinks use the file-name slug `apps-profisc`.

### Background job: `profics_send_order`

Order submissions go through a single queue mapping (`profics_send_order` on the `order-events2` queue). The job has **no recurring interval** — it fires on demand from the platform code or the merchant clicking Send manually. There is no scheduled retry sweep for failed pushes.

### Event triggers fire only on completed / paid

The platform code listens for `OrderStatusChange` and `PostOrderStatusChange`. When `send_order = 1` AND the order's status becomes either `paid` or `completed`, the job is queued. Other statuses (new order, fulfilled, cancelled) are ignored — so Profisc never sees orders that don't reach a paid/completed state.

### Invoice number falls back through invoicing providers

The platform asks the active invoicing provider for the order's invoice number first; if none exists, it asks for the receipt number. So Profisc receives whichever document number CloudCart's invoicing layer issued (FGO invoice, Szamlazz invoice, built-in receipt, etc.). If no invoicing provider is active, `invoiceId` is empty when sent to Profisc — Profisc's API may reject this.

### Currency conversion via `convertoToAll`

When the order is in a non-ALL currency, the Manager calls `convertoToAll($amount, $orderCurrency)` to convert each monetary value to Albanian Lek using CloudCart's exchange-rate model. This applies to subtotal, neto total, VAT, line items — every numeric field is converted. So the invoice arrives at Profisc in ALL regardless of the merchant's store currency.

### `op_code` is operator identification

When the merchant fills in `op_code`, it's appended as `operatorCode` in the invoice payload — Profisc uses it to identify the cashier / operator on the fiscal device. Leaving empty skips this field. Useful when multiple staff issue invoices under the same merchant account.

## Open questions

(none — questions about merchant-facing behaviour have been resolved against backend)
