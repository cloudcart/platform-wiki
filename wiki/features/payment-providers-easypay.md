---
type: feature
nav_path: "Payment Providers → EasyPay"
route_name: apps.epay.settings
route_path: /admin/payment-providers/epay
aliases: ["EasyPay", "Easypay", "Easy Pay", "EasyPay cash payment", "EasyPay vouchers", "Плати с EasyPay", "EasyPay каса", "Изипей"]
tags: [paymentproviders, payment-providers, easypay, epay, voucher, cash, bulgaria]
plan_gates: []
created: 2026-05-22
updated: 2026-05-22
source_count: 0
---
# EasyPay

## Purpose

EasyPay is the **physical cash-payment chain** operated by ePay.bg in Bulgaria — customers walk into any EasyPay office or partner location (post offices, kiosks, supermarket cash desks) and pay for an online order in cash by referencing a payment code. It is closely related to but separate from the [[payment-providers-epay]] e-wallet gateway.

**In the current CloudCart platform, EasyPay does NOT exist as a standalone, separately-configurable payment provider.** There is no EasyPay integration module and no `easypay` entry in the providers list. The underlying ePay protocol library ships an EasyPay request class, but it is not wired into a CloudCart service or registered in the admin router's providers list.

This means a Bulgarian merchant who wants to offer EasyPay cash payment to their customers today cannot do so via a dedicated provider in CloudCart. The closest options are:

1. **Configure base [[payment-providers-epay]]** — depending on the merchant's ePay account settings, ePay's hosted payment page may itself offer the customer a "Pay via EasyPay cash" option as one of the payment methods on the ePay-hosted screen.
2. **Use [[payment-providers-cod]]** (Cash on delivery) for the cash-payment-at-delivery flow — fundamentally different model (cash to courier, not cash at EasyPay office) but the closest "pay in cash" alternative inside CloudCart.

## Where to find it

The merchant cannot navigate to `apps.easypay.settings` — that route does not exist in the admin router.

To configure ePay (which may surface EasyPay as a payment option on the ePay-hosted page): Payment Providers → ePay.

## What the merchant can do here

(There is no EasyPay-specific configuration screen.) See [[payment-providers-epay]] for ePay configuration, which is the gateway that owns the merchant's ePay account — and that ePay account is what would also let the merchant offer EasyPay cash payment on ePay's side.

## Settings & fields

Not applicable — no EasyPay provider row exists in CloudCart's registered providers list.

## Business rules

### Currently no separate EasyPay registration

The admin router's registered providers list does not include `easypay` / `easy_pay`. There is no EasyPay integration in CloudCart's payment integrations.

### The Omnipay ePay library's EasyPay gateway exists but is dormant

The Omnipay-Epay library ships an EasyPay gateway with request / response classes that target:

- Live: `https://www.epay.bg/ezp/reg_bill.cgi`
- Test: `https://demo.epay.bg/ezp/reg_bill.cgi`

These are NOT instantiated by any CloudCart code today. They appear to be a legacy hook that was either deprecated, never finished, or kept available for future re-integration. No service class, no validator, no Vue settings panel references this gateway.

### Customer-side EasyPay availability via ePay

When a customer chooses [[payment-providers-epay]] at checkout and is redirected to ePay.bg's hosted payment page, ePay itself can present the customer with multiple payment methods including EasyPay cash payment (depending on the merchant's ePay account configuration). In that case:

- The customer picks EasyPay on the ePay side.
- ePay generates a payment code for the customer.
- Customer walks into an EasyPay office and pays cash there.
- ePay confirms the payment via the IPN webhook to CloudCart, marking the order `paid`.

From CloudCart's perspective the payment is still on the `epay` provider (not `easypay`) — the EasyPay routing happens entirely on ePay's hosted page.

### Permission

Same as base ePay configuration — requires `store.payment_providers`.

### Cache + side effects

Not applicable.

## Related

- [[payment-providers-epay]] — the parent ePay gateway through which EasyPay cash payment is offered today (on the ePay-hosted page).
- [[payment-providers-cod]] — the closest alternative cash-payment flow inside CloudCart (cash-on-delivery via courier).
- [[payment-providers]] — parent hub.
- [[settings-payment-providers]] — installed-providers list.

## How it works (verified against backend)

### No EasyPay provider in code

A search across the CloudCart payment integrations for `easypay` / `easy_pay` returns no matches — there is no EasyPay integration module.

### No `easypay` entry in the admin router's providers list

The admin router does not include `easypay` in its registered providers — so even an attempted navigation to `/admin/payment-providers/easypay/settings` would fall through to the platform's no-route fallback.

### What exists at the library level

The vendored Omnipay ePay library ships an EasyPay gateway class — dormant; not used by any CloudCart code.

## Open questions

(none)

## Verified — historical questions

- **Roadmap to enable EasyPay as a first-class provider**: not in the current platform. The dormant Omnipay class is leftover from a previous start-then-stop attempt; whether work resumes is a product decision not visible in the codebase.
- **How a merchant offering EasyPay cash payment today should set up their store**: configure [[payment-providers-epay]] and ask ePay support to enable EasyPay as one of the payment methods on the ePay-hosted page. CloudCart doesn't need to know — the routing to EasyPay happens on ePay's side.
