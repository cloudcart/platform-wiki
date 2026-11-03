---
type: feature
nav_path: "Payment Providers → Klear"
route_name: apps.klear.overview
route_path: /admin/payment-providers/klear
aliases: ["Klear", "Klear Lending", "Klear installment", "Klear BNPL", "Klear Pay", "Клиър", "Клиар"]
tags: [paymentproviders, payment-providers, klear, bnpl, installments, bulgaria]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 1
---
# Klear

## Purpose

**Klear** (Klear Lending) is a Bulgarian online consumer-loan provider with a checkout-redirect installment-loan product. The merchant signs up with Klear, gets a **public** and **private** API key pair per environment (test + live), enters them in CloudCart's Klear settings, and customers can pay over 3-N months with Klear's loan. The merchant can ALSO restrict Klear to a specific **financing program** — a special TBI / Klear partnership program (e.g., 0% interest on certain product categories) — by entering a financing-program ID and setting a checkout rule for how it applies.

This integration is **a single-tab settings model** with no schemes or promotions tab — all configuration is in one place. Klear's pricing schemes are fetched live from their API at checkout time and rendered in the customer's installment picker. A "promo button" can be enabled to show a Klear branded button on the product page.

The minimum order amount supported by Klear is **75 BGN**. Below that, Klear is hidden on the storefront regardless of merchant settings.

## Where to find it

Sidebar → **Payment Providers** → click **Klear**.

The route is `/admin/payment-providers/klear`. The hub page renders the standard payment-provider overview, with two tabs at the top: **Overview** and **Settings**.

## What the merchant can do here

- **Read the overview card** — logo, description, and the standard install / activate / deactivate buttons.
- **Install / Uninstall the payment method** through the overview's standard buttons.
- **Activate the payment method** once the API keys are saved.
- **Switch to the Settings tab** ([[payment-providers-klear-settings]]) to manage:
  - Test vs live mode toggle.
  - Public + Private API keys per environment.
  - Manual capture switch.
  - Financing-program ID and a `checkout_rule` (inclusive / exclusive).
  - Product filter for the financing program.
  - Promo-button switch + visual style.

## Settings & fields

This is a hub page — the actual fields live on the Settings sub-tab. The overview itself only exposes the standard payment-provider controls:

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Install** button | Creates the provider configuration for `klear`. | Not installed | One-click. |
| **Active** switch (header) | Turns Klear ON / OFF for storefront checkout. | OFF | Standard activation. |
| **Test mode switch** | Switches between test (`_test`) and live credentials. | test | Both sets saved at once. |
| **Min / Max amount** | Order-total range. **The minimum cannot be set below 75 BGN**. | None | Required. The minimum order amount must be 75 BGN or more (server error: `"Amount from must be greater than 75"`). |
| **Logo / Title / Description** | Customer-facing label on checkout. | Provider defaults | Standard. |
| **Discount** | Optional discount when customer picks Klear. | None | Standard. |

## Business rules

### How Klear works for the merchant

1. **Storefront pricing module** — CloudCart calls Klear's pricing API (HTTP GET to `/v1/pricing/{apiKey}?amount={price}` or `/v1/pricing/{apiKey}/{financing_program}?amount={price}`). Klear returns an `offers` array with: months (duration), monthly installment, interest rate, APR, total amount repaid.
2. **Free-leasing split** — variants with `interestRate > 0` are sorted into the regular scheme's variants; variants with `interestRate == 0` are sorted into a separate `free_leasing` group shown under a separate header.
3. **Customer picks a plan** — selects months in the storefront module.
4. **Redirect to Klear** — CloudCart calls Klear's checkout API with the merchant API key, customer details, billing/shipping addresses, cart items, the customer's selected loan duration, and gets back a `checkout_id` plus a redirect URL.
5. **Customer completes Klear's flow** — identity verification, employment data, etc., on Klear's hosted page.
6. **Klear pushes status callbacks** — Klear sends webhooks to `payments.webhook` to update the order status.

### Minimum order amount = 75 BGN, system-wide

Klear's minimum loan amount is **75 BGN**. The merchant cannot set `amount_from` below this — the validator refuses with `"Amount from must be greater than 75"`. The default value of `amount_from` on a fresh install is `7500` (75 BGN × 100, integer cents).

### Financing program — TBI / Klear special partnership

Klear runs special partnership financing programs (typically 0% interest for specific product categories). The merchant can:

1. Enter the **financing_program ID** issued by Klear for the merchant's contract.
2. Pick a **checkout_rule** ("inclusive" / "exclusive") — this controls how the merchant's product filter is enforced (see [[#checkout-rules-explained]] below).
3. Configure a product filter (e.g., "category = X") via the Helpers component on Settings.

When the storefront pricing module runs, the platform checks each product in the cart against the financing program rules:

- **Inclusive rule**: if ANY cart product matches the filter, the financing program applies — Klear's API is called with `financing_program=<id>` instead of the default catalog.
- **Exclusive rule**: if ANY cart product does NOT match the filter, the financing program is SKIPPED — fall back to default catalog.

### Checkout rules explained

- **Exclusive (default)** — strict: every product in the cart MUST match the filter for the financing program to apply. As soon as one product doesn't, the program is disabled. Useful when the program is, e.g., "only on TVs" — the merchant doesn't want a mixed cart to qualify.
- **Inclusive** — loose: as long as at least one product matches the filter, the financing program kicks in for the WHOLE basket. Useful for, e.g., "anchor offer" promotions where adding one promo item upgrades the whole cart.

### Manual capture

When `manual_capture = 1` (Settings), Klear orders that come back as "authorised" are NOT auto-completed — the merchant must manually confirm the payment from the order's admin view. When OFF, payments auto-complete on the customer's Klear approval. The default is OFF.

### Refund flow

Klear refunds are handled via email — CloudCart sends refund requests to a fixed inbox (`the provider's support address`). There is no API refund call from the CloudCart side; the merchant kicks off a refund and Klear processes it manually.

### Promo button on product page

When the **promo button** is enabled (Settings), CloudCart renders a Klear-branded "pay with Klear" button on each product page, with a preview helper that lets the merchant pick the button style. The merchant doesn't write any HTML themselves.

### Plan-gating

Not plan-gated by CloudCart subscription tier.

### Country + currency

BGN only, Bulgaria only. The Klear API endpoints `www.klearlending.com` (live) and `klear-pre.azurewebsites.net` (test) are both Bulgaria-specific.

## Related

- [[payment-providers]] — parent hub.
- [[payment-providers-klear-settings]] — full settings surface.
- [[payment-providers-iute]] — another EU consumer-loan provider with a similar architecture.
- [[payment-providers-fusion-pay]] — TBI Bank installment loan; partly overlaps with Klear via the Klear-TBI partnership financing programs.

## Open questions

(none)

## Verified — filter scope + callback authentication

- **Financing-program filter scope**: the merchant can target any of `product`, `vendor`, `tag`, `selection` (smart collection), or `category` — not only categories. See [[payment-providers-klear-settings#open-questions|Settings → filter DSL]] for the full list.
- **Callback authentication**: Klear's return URL carries a short-lived `checkout_token`. CloudCart does not verify any signature locally — instead, on receiving the callback it re-queries Klear's `transactions` endpoint with the token + the internal payment ID. The authoritative status comes from that re-query, not from the callback payload, so a forged callback URL cannot mark an unpaid order as completed (the token would not resolve to a successful transaction on Klear's side).
