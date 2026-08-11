---
type: feature
nav_path: "Payment Providers → CIB Bank → Payment flow"
route_name: apps.cib_bank.settings
route_path: /admin/payment-providers/cib_bank
aliases: ["CIB Bank payment flow", "CIB redirect", "CIB two-step return", "CIB status mapping", "CIB status sync", "CIB 3DSv2"]
tags: [paymentproviders, payment-providers, cib-bank, hungary, card, redirect, status-sync]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# CIB Bank — payment flow & status

> Part of [[payment-providers-cib-bank]]. See the hub for the other aspects (settings & DES file, save-card & refunds).

## Purpose

This page covers the **runtime payment behaviour** of the [[payment-providers-cib-bank|CIB Bank]] gateway: the hosted-redirect checkout flow, the two-step return (inquiry then complete-purchase), the CIB-response → CloudCart-status mapping, the reconciliation sync flow, the 3DSv2 step-up handling, and the unusual double-query-string return URL. Configuration lives on [[cib-bank-settings]]; save-card and refunds on [[cib-bank-save-card-refunds]].

CIB Bank integrates the bank's "market.saki" ecommerce hosted-payment gateway. The customer is redirected from the storefront checkout to CIB's hosted page (`eki.cib.hu` for live, `ekit.cib.hu` for test), enters card details there, completes 3D Secure if required, and is bounced back to the store after authorisation.

## Where to find it

The flow is invisible in the admin panel — it runs at storefront checkout when a customer picks **CIB Bank** as the payment method. The merchant configures it from Sidebar → **Payment Providers** → **CIB Bank** (`/admin/payment-providers/cib_bank`). Resulting payment status is shown on the order page; see [[orders-details]] and [[payment-status]].

## What the merchant can do here

- Nothing to configure on the flow directly — it is fully automatic once the method is set up on [[cib-bank-settings]].
- Observe the resulting **Completed / Pending / Failed** status on the order.
- Rely on the **scheduled status sync** to resolve Pending payments (e.g. mid-3DS) to a terminal state without manual action.

## Settings & fields

There are no flow-specific settings. The flow reads the per-environment Merchant ID + DES file configured on [[cib-bank-settings]]; the `configuration.mode` value (`test` / `live`) selects the endpoint (`ekit.cib.hu` vs `eki.cib.hu`).

## Business rules

### Customer flow — full redirect

CIB is a **hosted redirect** gateway:

1. The platform builds a CIB purchase request with the customer ID, the **internal Payment ID zero-padded to 16 characters** as the `transactionId`, the amount in HUF minor units, and a return URL.
2. The DES file is parsed at request time into its three components (two keys + initialisation vector — see [[cib-bank-settings]]), and the Omnipay CIB client signs / encrypts the request with those.
3. CIB responds with a redirect URL. The platform returns `action.type=redirect` to the storefront, which navigates the browser to CIB.
4. The customer enters card details on `eki.cib.hu` (live) or `ekit.cib.hu` (test), completes 3D Secure if required.
5. CIB calls back to `/payments.return/cib_bank?ccid=<payment_id>?<query>` — the platform parses the unusual double-query-string format the gateway uses (below) and runs the complete-purchase step.

### Two-step return: inquiry then complete-purchase

CIB's return flow is **two API calls**:

1. **Inquiry** — the platform calls CIB's inquiry endpoint with the return query data to verify the transaction.
2. If inquiry succeeds, the platform calls complete-purchase to finalise the charge.
3. The final status is set from the complete-purchase response — Completed on success, Failed otherwise.
4. If inquiry returns Pending, the payment stays at **Pending** — the platform's status reconciliation will retry later.

### Status mapping

| CIB response sequence | CloudCart status |
|-----------------------|------------------|
| inquiry success → complete-purchase success | **Completed** |
| inquiry success → complete-purchase failed | **Failed** |
| inquiry pending | **Pending** |
| inquiry failed | **Failed** |
| (after refund call returns success — see [[cib-bank-save-card-refunds]]) | **Refunded** |

### 3DSv2 step-up → Pending

A 3DSv2 step-up lands in **Pending** in CloudCart (the inquiry-pending path is the catch-all for in-progress authentications). A pending payment is later resolved to Completed or Failed by the sync flow once CIB returns a terminal state. The customer never sees "Failed" mid-3DS; they see Pending while the challenge runs.

### Status sync (reconciliation)

The sync flow is the reconciliation path used by the scheduled status checker:

1. Calls CIB's transaction-status endpoint.
2. If success → Completed.
3. If pending → calls the inquiry endpoint next; if inquiry succeeds → Completed, pending → Pending, otherwise → Failed.
4. If transaction-status fails outright → Failed.

This dual-call sync exists because CIB's transaction-status and inquiry endpoints report different views of the transaction lifecycle (inquiry is closer to the final settlement state).

### Unusual return URL format

CIB calls back with the payment ID inside a `ccid` parameter that contains a **double query string** (e.g., `ccid=<payment_id>?<additional_query>`). The integration parses this format manually — splits on `?`, extracts the payment ID, parses the inner query string, and rewrites the request's query string to a normalised form. This handles a CIB-specific quirk in their return-URL handling.

## Related

- [[payment-providers-cib-bank]] — hub.
- [[payment-status]] — Completed / Pending / Failed / Refunded mapping.
- [[orders-details]] — where the resulting payment status appears on the order.
- [[checkout-flow]] — concept page on the storefront checkout.
- [[payment-provider-mechanism]] — generic redirect / return / sync mechanism shared across gateways.

## Open questions

(none)
