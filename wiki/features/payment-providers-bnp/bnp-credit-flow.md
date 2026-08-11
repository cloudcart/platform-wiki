---
type: feature
nav_path: "Payment Providers → BNP Paribas Personal Finance → Credit flow"
route_name: apps.bnp.settings
route_path: /admin/payment-providers/bnp
aliases: ["BNP credit flow", "BNP credit application", "BNP email request flow", "BNP eCom API flow", "BNP underwriting flow", "BNP request email", "BNP certificate handling"]
tags: [paymentproviders, payment-providers, bnp, bulgaria, credit, leasing, ecom, postbank]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[payment-providers-bnp]]. See the hub for the other aspects (settings & fields, eligibility & promotions, market positioning).

# BNP — credit application flow

## Purpose

This page documents **what actually happens when a customer picks BNP at checkout** — the two parallel underwriting flows (legacy email-request and the newer eCom API), what CloudCart records at order placement, how the eCom flow fails loudly rather than silently, the certificate handling for the eCom mutual-TLS connection, and the terms-acceptance links the storefront shows in email mode. It is the page to read for "what happens after my customer chooses BNP?" and "why did the BNP checkout error out?".

## Where to find it

The flow runs on the storefront checkout once BNP is installed and active (Sidebar → **Payment Providers** → **BNP Paribas Personal Finance**). The flow that runs is determined by the `ecom_enabled` setting documented on [[bnp-settings-fields]].

## What the merchant can do here

- **Choose which flow runs** by toggling `ecom_enabled` — email-request (default) or eCom API.
- **Keep an email record-copy** even in eCom mode by turning on `send_email_after_checkout`.
- **See BNP underwriting errors surfaced at checkout** rather than silently degraded (eCom mode).

## Settings & fields

The flow is selected by two settings (full field details on [[bnp-settings-fields]]):

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **eCom enabled** (`configuration.ecom_enabled`) | When ON, use the online API + portal redirect instead of email-only. | OFF | Requires eCom client ID / secret / certificate. |
| **Send request email after checkout** (`configuration.send_email_after_checkout`) | Even with eCom on, also send the legacy email for record-keeping. | OFF | The "send both" mode. |

## Business rules

### Two parallel flows

1. **Email-request flow** (legacy / default) — at checkout, CloudCart sends an email to BNP at `the provider's support address` with the order details, customer data, and chosen financing scheme. BNP staff process the application manually.
2. **eCom API flow** (newer, enabled with `ecom_enabled=true`) — at checkout, CloudCart calls BNP's eCom API directly and redirects the customer to BNP's online underwriting portal. The customer completes underwriting online, and BNP posts back to CloudCart with the outcome.

### Customer flow — credit application, not a charge

BNP is fundamentally a credit-application flow, not a payment:

1. **At checkout** — the customer enters their EGN (Bulgarian personal ID), full name, phone, email, delivery address. They pick a financing scheme (months / down payment / installment amount) from the promo-scheme dropdown (schemes are managed on [[bnp-eligibility-promotions]]).
2. **At order placement** — CloudCart creates a **Payment row** with `provider=bnp` in a pending-credit state.
   - **Email mode:** a request email is sent to `the provider's support address` with the order details rendered via the `mail.creditor.request_bnp` view. The subject line is `<merchant_code>, онлайн заявка по поръчка <order_id>` (in Bulgarian). Postbank staff process the application offline; the merchant phones BNP / waits for an email back to learn the outcome.
   - **eCom mode:** CloudCart calls BNP's eCom API with the order goods, customer data, address, and financial parameters (installment count, amount, scheme, total, credit amount, down payment). BNP returns a redirect URL; the customer is bounced to BNP's online underwriting portal.
3. **After approval / rejection** — BNP either calls back via eCom or the merchant manually marks the payment as Completed / Failed.

The integration does NOT use the standard CloudCart card-payment status flow — BNP payments stay in pre-completion states until BNP confirms underwriting.

### eCom mode short-circuit (verified against backend)

When `ecom_enabled` is ON but the eCom API call fails (e.g., expired token, certificate trouble, network), the integration captures the exception, JSON-decodes the error into `provider_data.ecom_error`, flips the payment to **Failed**, and re-throws as a CloudCart Error. The merchant sees the underlying BNP error message in the checkout response — this is intentional so credit-application errors get attention immediately rather than degrading silently to email mode.

The legacy email path is only used when `ecom_enabled=false` OR when `ecom_enabled=true` AND `send_email_after_checkout=true` (the "send both" mode for record-keeping).

### Certificate handling

For the eCom flow, the merchant uploads a PFX/PEM certificate + password. The integration converts the upload to PEM and writes it to a per-site temp file (`<site_id>-bnp.pem` in the system temp directory). The temp file is reused across requests for the same site.

### Storefront terms — only shown in email mode

When the integration is in email mode (`ecom_client_id` empty), the storefront renders three terms-acceptance links the customer must agree to:

- Application conditions (link to `postbank.bg/common-conditions-PFBG`)
- Personal data protection (link to `postbank.bg/Personal-Data-PFBG-retailers`)
- Product information (link to `postbank.bg/product-information-PBPG-retailers`)

The first two require checkbox acceptance; the third is informational. In eCom mode the customer agrees to terms on BNP's hosted portal instead.

## Related

- [[payment-providers-bnp]] — hub.
- [[bnp-settings-fields]] — the `ecom_enabled` / `send_email_after_checkout` switches and eCom credentials this flow consumes.
- [[bnp-eligibility-promotions]] — the financing schemes the customer picks at checkout.
- [[payment-status]] — credit-flow status mapping (pending-credit → Completed / Failed).
- [[checkout-flow]] — storefront checkout where BNP surfaces.
- [[payment-provider]] — entity definition.

## Open questions

- ⏸️ Exact enum of `Status` values BNP returns in the eCom protocol — passed through to `payment.status` unmodified. The authoritative list lives in BNP / Postbank's own eCom protocol docs, not in CloudCart.
