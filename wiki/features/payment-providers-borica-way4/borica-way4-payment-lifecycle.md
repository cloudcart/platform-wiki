---
type: feature
nav_path: "Payment Providers → Borica Way4 → Payment lifecycle & 3DS"
route_name: apps.borica_way4.overview
route_path: /admin/payment-providers/borica_way4
aliases: ["Borica 3DS", "Borica MPI_OW_APGW", "Borica IPN", "Borica return URL", "Borica P_SIGN", "Borica status codes", "Borica RC", "Borica NONCE", "Borica purchase flow"]
tags: [paymentproviders, payment-providers, borica-way4, lifecycle, 3ds, ipn, status-codes]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-borica-way4]]. See the hub for related aspects (setup/CSR, settings, authorize/capture, save card, refund/sync).

# Borica Way4 — Payment lifecycle & 3DS

## Purpose

This aspect documents what happens on the wire from "customer clicks Pay" to "order shows Completed in the admin". The flow is: purchase request → redirect to Borica's hosted Way4 page → mandatory 3-D Secure → return POST + IPN to CloudCart → signature verification → status mapping. The mapping table from Borica's response code (`RC`) to CloudCart's `payment-status` lives here.

## Where to find it

This aspect is invisible to the merchant — it's the runtime behaviour behind every order paid through Borica Way4. The merchant sees the result on the order in [[orders-details]] and on the [[orders-payment-refund]] / [[orders-payment-capture]] actions.

## What the merchant can do here

- **Inspect a payment's lifecycle** on the order details page — the Borica response (`RC`, `STATUSMSG`, `RRN`, `INT_REF`) is stored on the payment row.
- **Manually re-sync a pending payment** from the order details — see [[borica-way4-refund-sync]] for the sync mechanism.
- **Read the verbatim webhook URL** to give Borica — see [[borica-way4-settings-fields]] for the `EGW_MERCH_BACKREF` field.

## Settings & fields

This aspect does not expose its own fields — the lifecycle is the runtime behaviour determined by the settings on [[borica-way4-settings-fields]] (Mode, MID, EGW_SECURITY, Currency, EGW_MERCH_BACKREF). Authorization-mode interactions are documented on [[borica-way4-authorize-capture]].

## Business rules

### 3-D Secure is mandatory

Every Borica Way4 purchase is routed through the **MPI_OW_APGW** (Merchant Plug-In Online Worldwide — Acquirer Payment Gateway) 3-D Secure flow. The merchant cannot disable 3DS — it's enforced by the bank-level gateway certificate (`MPI_OW_APGW_D_2026.cer` for test, `MPI_OW_APGW_P_2026.cer` for live, both bundled in CloudCart and rotated by year).

The platform sends `M_INFO` (cardholder name + billing address + shipping address, **ASCII-only, 45-char-max each**) in every purchase request to support frictionless 3DS challenges where the issuer chooses.

### Order ID format

Borica's hosted page requires a numeric reference up to 6 digits. The platform sends:

- **`order`** field — the **last 6 digits of the internal payment ID**.
- **`orderId`** field — additional identifier of the form `<MMDD>|<order_id>` (e.g., `0522|12345`) for internal tracking.
- **`DESC`** field — the customer-visible description, reads `Order #<order_number>` using the merchant's chosen Order ID display setting (sequential ID or `increment_hash`).

### Currency handling on the wire

Amounts are sent in **stotinki / cents** (minor units — multiplied by 100). If the storefront order is in a currency different from the terminal's provisioned currency (BGN or EUR), the platform converts the amount on the fly using the store's currency rates before sending — see [[borica-way4-settings-fields]] for the currency rule.

### Webhook URL the merchant gives to Borica

The single URL used for both customer-return and IPN webhook:

```
<cc_payments_domain>/return/provider/borica_way4
```

The merchant copy-pastes this into Borica's terminal configuration form as the `EGW_MERCH_BACKREF` value when their bank registers the terminal — see [[borica-way4-settings-fields]].

### Signature verification

Borica POSTs the response with a `P_SIGN` HMAC over the concatenated response fields. The platform verifies the signature using either `MAC_GENERAL` (SHA-256) or `MAC_ADVANCED` per the `EGW_SECURITY` configuration value. A mismatch marks the payment `Failed`. The platform finds the payment row by `NONCE=<provider_reference_id>` so the IPN can locate the order even if the customer never reaches the return page.

### Status code mapping

The Borica response code (`RC` or `RESPONSE`) plus the `TRTYPE` (transaction type) maps to the platform's [[payment-status]]:

| Borica code | TRTYPE | Mapped status |
|-------------|--------|---------------|
| `00` | `1` (purchase) | `Completed` |
| `00` | `12` (authorize) | `Authorized` (see [[borica-way4-authorize-capture]]) |
| `00` | `22` (cancel) | `Canceled` |
| `00` | `isReversal` flag | `Refunded` (see [[borica-way4-refund-sync]]) |
| `-25` | any | `Canceled` (customer aborted on Borica's page) |
| `-31`, `-33`, `-39`, `-40` | any | `Pending` (3DS waiting, no terminal response yet) |
| Anything else | any | `Failed` |

### Pending → final-state reconciliation

When the customer closes the browser mid-payment and never reaches the return URL, the payment row sits in `Pending` until reconciled. The platform-wide sync job polls Borica every 5 minutes — see [[borica-way4-refund-sync]] for the cadence and the `-24` "transaction not found" auto-cancel rule.

## How it works (verified against backend)

### Purchase initiation

The platform builds the form payload with:

- `TERMINAL` — the merchant's Terminal ID.
- `MERCHANT` — the configured MID (or the platform Site ID as fallback — see [[borica-way4-settings-fields]]).
- `AMOUNT` — in stotinki/cents.
- `CURRENCY` — `BGN` or `EUR` per terminal configuration.
- `ORDER` — last 6 digits of the payment ID.
- `DESC` — `Order #<order_no>`.
- `M_INFO` — customer name + billing + shipping addresses, ASCII-only, 45-char max.
- `EGW_MERCH_BACKREF` — the return URL.
- `NONCE` — the platform's provider-reference ID, used to locate the payment on IPN.
- `P_SIGN` — HMAC signature over the concatenated request fields (algorithm per `EGW_SECURITY`).
- `TRTYPE=1` for auto-capture purchase, `TRTYPE=12` for authorize-only (manual capture mode — see [[borica-way4-authorize-capture]]).

### Redirect

The customer is redirected to Borica's hosted Way4 page via an **auto-submitting form** that POSTs to Borica's MPI_OW_APGW endpoint. They complete 3DS and (if the issuer challenges) authenticate.

### Return

Borica POSTs the customer back to `<cc_payments_domain>/return/provider/borica_way4` with the full response payload:

- `ACTION` — the transaction action code.
- `RC` — the response code (mapped per the table above).
- `STATUSMSG` — human-readable status message.
- `RRN` — Retrieval Reference Number (used for refund).
- `INT_REF` — internal Borica reference (used for refund + sync).
- `P_SIGN` — HMAC signature for verification.

### IPN webhook

Borica **also** POSTs to the same return URL with `NONCE=<provider_reference_id>` so the platform can locate the payment row even if the customer never reaches the return page. The platform verifies `P_SIGN` and updates the payment + order status.

### Result

`RC=00` + the current `TRTYPE` decides the next status. Anything else marks the payment `Failed`. The `RRN` + `INT_REF` are stored on the payment row for later refund / sync — see [[borica-way4-refund-sync]].

## Related

- [[payment-providers-borica-way4]] — hub.
- [[borica-way4-settings-fields]] — where the return URL the merchant gives Borica is displayed.
- [[borica-way4-authorize-capture]] — TRTYPE 12 / 21 / 22 details for the manual-capture path.
- [[borica-way4-save-card-wallets]] — adds `MERCH_TRAN_STATE=S` to the purchase request when Save Customer Card is on.
- [[borica-way4-refund-sync]] — what happens to stranded `Pending` payments + the refund path.
- [[payment-status]] — the merchant-visible Authorized / Completed / Canceled / Refunded / Failed values.
- [[orders-details]] — where the payment lifecycle is surfaced in the admin.
- [[checkout-flow]] — concept page on storefront checkout, where the Borica option triggers this flow.

## Open questions

(none)
