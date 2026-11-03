---
type: feature
nav_path: "Payment Providers → cPay"
route_name: apps.cpay.settings
route_path: /admin/payment-providers/cpay
aliases: ["cPay", "CPay", "CaSys cPay", "CaSys", "плати с cPay", "cPay Macedonia", "cPay Севернa Македония"]
tags: [paymentproviders, payment-providers, cpay, casys, card, macedonia, online]
plan_gates: []
created: 2026-05-22
updated: 2026-05-22
source_count: 0
---
# cPay

## Purpose

A configuration screen for **cPay** — the card-payment gateway operated by CaSys for the North Macedonian market. cPay processes Mastercard, Visa, and domestic card payments denominated in **MKD (Macedonian denar)**. The customer chooses cPay at checkout, is redirected to the cPay-hosted card-entry form, completes the payment, and is returned to the store with a success / failure status.

This provider is intended for stores selling in North Macedonia or accepting MKD payments. Currency conversion to MKD happens automatically inside the integration when the cart is in a different currency.

## Where to find it

Payment Providers → **cPay**. Provider key: `cpay`. Route name `apps.cpay.settings`, path `/admin/payment-providers/cpay/settings`.

## What the merchant can do here

- **Toggle Test / Live mode**.
- **Enter the cPay credentials**: Merchant ID, Merchant Name, Merchant Password.
- **Customer-facing title** override.
- **Logo override**.
- **Per-provider discount / fee** ([[discount]]).
- **From / To availability window**.
- **Active toggle**.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Test mode** switch | Test → cPay sandbox. Live → production. | test after install | Help text: *"Use test mode to test your connection. Live mode is for the actual payment processing. Use live mode when you have verified your credentials."* |
| **Merchant Name** | The merchant's registered name in cPay. Once stored, cannot be changed. | required | Required, alphanumeric only, length 1-200. Help text: *"The name of the merchant in cPay. Once stored can't be changed."* Validation errors: "Please enter merchant name", "Only alphanumeric allowed." |
| **Merchant ID** | The merchant's numeric ID issued by cPay. Once stored, cannot be changed. | required | Required, numeric. Help text: *"Merchant ID given by cPay. Once stored can't be changed."* Validation errors: "POS ID is required", "POS ID should be only digits". |
| **Merchant Password** | Password used to identify with cPay during payment requests. Masked input. | required | Help text: *"Payment password to identify with cPay"*. Validation error: "Please, enter password". |

There is **no separate Test ID / Live ID** — the same Merchant ID, Name, and Password fields are used in both modes; only the endpoint URL changes based on the Mode toggle.

## Business rules

### Currency: MKD (Macedonian denar)

cPay processes in **MKD only**. The currency is fixed inside the integration.

If the cart currency is NOT MKD (BGN, EUR, RON, etc.), the platform auto-converts the amount to MKD at the current FX rate before sending it to cPay. The amount sent must be an integer (no fractional denars), so the converted figure is rounded to a whole denar — e.g. a 99.49 EUR cart becomes a whole-denar MKD amount.

The customer's card is charged in MKD; their bank may show a different amount after currency conversion on their side.

### Checkout flow — HTML form auto-submit

On purchase:

1. Builds two encrypted return URLs — one for success (`s = encrypted STATUS_COMPLETED`), one for failure (`s = encrypted STATUS_FAILED`).
2. Builds the form parameters with all the merchant credentials, the amount in MKD, the cart total reference, and the customer's billing address.
3. Validates the form parameters against cPay's protocol rules (amount integer, currency length 3, merchant name 1-200 alpha-numeric, telephone integer-only, etc.).
4. Returns an HTML form that the storefront auto-submits to cPay.
5. cPay shows its hosted card-entry page.
6. Customer enters card data; cPay processes.
7. cPay redirects back to the appropriate success/fail URL based on the result.

### Encrypted return-URL parameter

The return URL receives a `pid` (payment ID) and an encrypted `s` (status) parameter. The `s` value is an encrypted `STATUS_COMPLETED` / `STATUS_FAILED`. On return, the platform decrypts `s` and validates it is one of those expected statuses — protecting against URL tampering, since only the platform can produce a value that decrypts to a valid status. Anything that doesn't decrypt to a valid status returns a Bad Request error.

### Form parameter validation rules

| Parameter | Rules |
|-----------|-------|
| AmountToPay | required, integer |
| AmountCurrency | required, string, length 3 |
| Details1 | required, string, between:1,32 |
| Details2 | required, string, between:1,10 |
| PayToMerchant | required, integer |
| MerchantName | required, string, between:1,200 |
| PaymentOKURL | required, string, between:1,500 |
| PaymentFailURL | required, string, between:1,500 |
| OriginalAmount | sometimes, integer |
| OriginalCurrency | sometimes, string, length 3 |
| Fee | sometimes, string, between:1,16 |
| CRef | sometimes, string, between:1,50 |
| TransactionType | sometimes, string, between:1,3 |
| Installment | sometimes, digits:2, max:99 |
| RPRef | sometimes, string, between:1,50 |
| FirstName | sometimes, string, between:1,64 |
| LastName | sometimes, string, between:1,64 |
| Address | sometimes, string, between:1,50 |
| City | sometimes, string, between:1,50 |
| Zip | sometimes, integer |
| Country | sometimes, numeric, length 3 |
| Telephone | sometimes, integer |
| Email | sometimes, string, between:1,64 |

These are cPay's own protocol limits — exceed them and cPay will reject the payment request.

### Installments / BNPL

The `Installment` parameter exists in the protocol (digits:2, max:99) but is **not** surfaced in the CloudCart settings UI. Any cPay-side installment program is configured through cPay's own merchant dashboard, not CloudCart.

### Merchant ID + Merchant Name are immutable

The UI help text says: *"Merchant ID given by cPay. Once stored can't be changed."* and *"The name of the merchant in cPay. Once stored can't be changed."*

This reflects cPay's onboarding flow: the credentials are issued once and the merchant is locked to that identity. If the merchant needs to change Merchant ID or Name, they have to coordinate with cPay support and likely re-onboard.

### Test cards

cPay provides standard test card numbers in their sandbox documentation. CloudCart does not embed the test card list — request from cPay support.

### Refund

Refunds are not supported through CloudCart. Refunds must be done via cPay's merchant dashboard, then marked Refunded in CloudCart manually.

### No periodic status sync

Payment status is driven entirely by the return-URL flow; there is no periodic status sync.

### Availability by store country

cPay's primary market is North Macedonia; Bulgarian merchants selling cross-border into MK occasionally enable it. The provider is filtered by the `operation_country` setting in [[settings-general]] — only stores whose operation country covers MK see cPay in the Add-payment-method modal.

### Permission

Requires `store.payment_providers`.

## Related

- [[payment-providers]] — parent hub; the `payments` row gets `provider=cpay`.
- [[settings-payment-providers]] — install/uninstall.
- [[settings-general]] — `operation_country` filter (cPay typically available for MK stores).
- [[discount]] — per-provider fee/discount.
- [[orders-payment-refund]] — Refund flow.

## Open questions

(none)
