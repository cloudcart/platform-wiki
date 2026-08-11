---
type: feature
nav_path: "Apps → FGO"
route_name: apps.fgo.overview
route_path: /admin/apps/fgo
aliases: ["FGO", "FGO invoicing", "FGO accounting", "Българско счетоводство FGO", "enable disable button", "app active toggle"]
tags: [apps, erp, invoicing, bulgaria, accounting]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 2
---
# FGO (Bulgarian invoicing)

## Purpose

**FGO** integration — Bulgarian online invoicing platform. When activated, FGO becomes the platform's active invoicing provider for Bulgarian merchants (alongside [[apps-szamlazz]] for Hungary, [[apps-smart-bill]] for Romania, and [[apps-flix-facts]] for other markets).

Handles invoice generation, cancellation with audit trail, PDF retrieval, and tax-compliant numbering per Bulgarian tax law.

> **Has an on/off control.** The app screen carries an **Enable / Disable** button, so the merchant can switch it off without uninstalling it. A disabled app stops working while keeping its settings — so *"the app is disabled"* IS a valid explanation to check here.

## Where to find it

Sidebar → Apps → install → **FGO**.

## What the merchant can do here

- See app status + configuration health.
- Configure FGO API credentials in Settings ([[apps-fgo-settings]]).
- Activate to make FGO the active invoicing provider.
- Generate documents per order through orders-details / orders-invoice flow.

### What the merchant CANNOT do here
- Use FGO without a paid FGO subscription.
- Run FGO alongside another active invoicing provider (one at a time).

## Settings & fields

The Manager exposes:
- `appInfo` — Returns metadata about the FGO integration.
- the configured check — Checks whether FGO credentials are valid + ready to use.
- `getClient($credentials)` — Returns FGO API client for direct API calls.
- `generateDocument(Order $order)` — Issues an invoice for the given order.
- `cancelDocument(Order $order, $number, $seria)` — Cancels a previously-issued document by FGO number + series identifier.
- Geographic lookups: `getCountryByCode(iso2)`, `getStateByCode(iso2)`, `getCityCode`.

FGO uses a **number + series** identification model (legacy Bulgarian accounting practice), unlike Szamlazz's single-number approach.

## Business rules

### Bulgarian tax compliance

FGO handles requirements of Bulgarian National Revenue Agency (NAP) — sequential numbering per series, document retention, cancellation audit.

### Series structure

The Bulgarian invoice has both a `series` (prefix identifier, e.g., "A") and a `number` (sequential within the series). The merchant typically uses one series for normal invoices and another for credit notes.

### the configured check gate

Before issuing documents, the platform calls the configured check to verify credentials. If not, document generation is blocked.

### Side effects

Activation sets `invoicing_provider = fgo`. Document generation stores metadata on order meta.

### Permission

Standard apps permission scope.

## Related

- [[apps]] — App Store.
- [[apps-fgo-settings]] — settings sub-page.
- [[apps-szamlazz]] — Hungarian counterpart.
- [[apps-smart-bill]] — Romanian counterpart.
- [[apps-flix-facts]] — additional markets.
- [[settings-invoicing]] — invoicing provider configuration.
- [[orders-invoice]] — invoice flow.
- [[orders-credit]] — credit note flow.

## How it works (verified against backend)

### Required settings (5 fields)

ALL five must be non-empty for the integration to fire:
- `password` — FGO API password.
- `merchant_name` — merchant identifier on FGO.
- `unique_code` — FGO unique code.
- `platform_url` — FGO platform URL (e.g., specific FGO instance).
- `environment` — likely production / staging toggle.

Missing any blocks document issuance.

### Document creation flow

When generating a document for an order:
1. The platform converts the order to FGO's expected payload.
2. Calls FGO's invoice-create endpoint.
3. FGO returns a response containing `Factura.Numar` (number), `Factura.Serie` (series), `Factura.Link` (PDF URL).
4. Stores on `order.meta`:
   - `fgo_document_number` — invoice number.
   - `fgo_document_seria` — series prefix.
   - `fgo_document_link` — URL to download the PDF from FGO.
   - `fgo_document_type` — from `invoice_type` setting (likely invoice / receipt / credit-note).
5. **On failure**: writes a `send_erp_error` action to the order's history with the FGO error details.

So **failures appear in [[orders-history]]** as ERP errors — same pattern as other ERP integrations.

### Cancellation flow

When cancelling a document:
1. The platform calls FGO's invoice-delete endpoint with the number, series, and platform URL.
2. **On success**: REMOVES the 4 meta keys (`fgo_document_number`, `_seria`, `_type`, `_link`) — the order looks like it never had an FGO document.
3. **On failure**: throws exception.

**Important distinction from Szamlazz**: FGO cancellation REMOVES the document metadata entirely (no credit-note counter-document). This is different from Szamlazz's `credit_note.active` behaviour. Verify whether FGO's API requires the merchant to issue a credit-note separately for legal compliance OR whether the delete IS the legally-valid cancellation in Romanian/Bulgarian context.

(Note: FGO's response keys are in Romanian/Bulgarian — `Factura` = invoice, `Numar` = number, `Serie` = series, `PlatformaURL` = platform URL. This confirms FGO is a Romanian-language API, even though used by Bulgarian merchants.)

### PDF stored as link, not base64

Unlike Szamlazz (which caches PDF base64 on `order.meta`), FGO stores only the LINK to the PDF on the FGO platform. The merchant clicks → opens FGO-hosted PDF. Pros: smaller order.meta footprint. Cons: PDF accessibility depends on FGO platform availability.

### Production vs test environments

FGO supports a `test` environment via the `environment` setting (allowed values: `production` / `test`). The same merchant credentials may behave differently in test vs production; the merchant can switch via the Settings page without re-installing.

### Document type is set globally per merchant (not per order)

The merchant picks ONE document type at the global level from FGO's taxonomy list. That type applies to ALL documents the integration creates for this merchant. The standard FGO types are:

| Code | Label |
|------|-------|
| `f` | Invoice (factura) |
| `t` | Reverse charge (taxare inversa) |
| `p` | Proforma invoice |
| `a` | Notice (aviz) |
| `s` | Exempt with deduction |
| `com` | Order |
| `u` | Services according to Art. 311 |
| `h` | Sales according to Art. 312 |
| `n` | Non-taxable operations |
| `x` | Special regime according to Art. 314–315 |
| `d` | Estimate |
| `c` | Receipt with tax code |
| `b` | Receipt |

(These labels are Romanian-tax-code-aware — FGO is a Romanian platform serving the cross-border Bulgarian/Romanian market.)

### Auto-trigger conditions (4 cases)

FGO auto-fires when ALL of these are true:
- `automate_generate = 1` (the merchant enabled auto mode).
- The order's status matches one of these patterns:
  - On order create with status `new_order`.
  - On order status change to `completed` AND `order_status` setting = `completed`.
  - On order status change to `paid` AND `order_status` setting = `paid`.
  - On fulfillment add with order status `fulfilled`.
- If `is_billing_address = 1` AND the order has NO billing address → SKIP. Otherwise → fire document generation.

The merchant can disable auto-generation entirely (`automate_generate = 0`) and trigger document creation manually from the order page.

### Cancellation is permanent removal from CloudCart's side

When cancellation succeeds, the platform DELETES the 4 FGO meta records (`fgo_document_number`, `_seria`, `_type`, `_link`) entirely. From CloudCart's perspective, the order looks as if FGO was never invoked. FGO's own portal retains the audit trail per Bulgarian/Romanian tax law — but the merchant must visit FGO directly to see cancelled documents.

### Settings persisted (per `the platform code::$only`)

Exactly these 11 keys are accepted on save:
- Connection: `password`, `unique_code`, `merchant_name`, `platform_url`, `environment`.
- Document: `invoice_type` (one of the 13 types), `seria` (single series prefix), `text` (text appended to invoice body), `additional_text` (extra body text).
- Automation: `automate_generate` (0/1), `order_status` (which CloudCart status triggers), `is_billing_address` (when 1, skip orders without billing address).

Any other field POSTed is silently dropped.

### Throws after writing `send_erp_error`

When `generateDocument` catches a failure, it both writes a `send_erp_error` history entry AND re-throws the exception. So upstream callers (the platform code for auto-generation, or the manual route from the order page) see the exception bubble up — useful for the merchant-facing error toast on manual click, and for retry logic in queued contexts.

### No scheduled jobs

FGO has no recurring queue mapping — it's purely event-driven. Document creation fires only on the platform code triggers (`OrderCreated` with `new_order` status, `OrderStatusChange` to `completed`/`paid`, `FulfillmentAdd`) or on manual click. There is no cron-based "issue all unbilled orders" sweep.

## Open questions

(none — questions about merchant-facing behaviour have been resolved against backend)
