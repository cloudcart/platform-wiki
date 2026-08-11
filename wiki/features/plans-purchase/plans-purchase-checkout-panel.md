---
type: feature
nav_path: "Profile → Choose plan → {Plan} → Purchase → Pay now"
route_name: admin.checkout
route_path: /admin/checkout
aliases: ["Plan checkout panel", "Plan checkout", "Pay now panel", "Checkout side-panel", "Order overview card", "Плащане на плана", "Чекаут панел"]
tags: [plans, purchase, checkout, payment, stripe, braintree, 3ds]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[plans-purchase]]. See the hub for the other aspects (billing cycle, recommended add-ons, plan detail view, business rules, subscription outcomes, discount codes).

# Plans purchase — checkout side-panel

## Purpose

After the merchant has picked a billing cycle and (optionally) ticked add-ons on the PlanPanel, clicking *Proceed to checkout* slides in the **Checkout side-panel** — a stack of cards summarising the cart and gathering the invoice profile + payment method needed to charge. This is the screen where the merchant **actually pays**. The plan-detail subscription is only created on success of this step, not on PlanPanel submission.

## Where to find it

Triggered from `/admin/plan/{mapping}/purchase` by clicking *Proceed to checkout* on the PlanPanel. The panel slides in from the right at size `xll` (one size larger than the PlanPanel beneath it) with `no-close-on-esc` + `no-close-on-backdrop`. The merchant can return to the PlanPanel without losing selection via the **Cancel** / *Back* button in the panel header.

The standard backend route used for the cart redirect is `/admin/checkout`.

## What the merchant can do here

- Review the cart-item lines (plan + add-ons) with original prices and any discount badges.
- Add or edit their invoice details inline (collapsed summary → pencil → form).
- Add or edit their saved payment card inline (Stripe or Braintree gateway).
- Apply a discount / promo code (when the cart allows it).
- See live totals (subtotal, discount, total without VAT, VAT, total to pay).
- Submit the payment via **Pay now** — handles 3DS challenges on Braintree mid-flight.

## Settings & fields

### Card stack (top to bottom)

| Card | What it shows | Where it links |
|------|---------------|----------------|
| **Order overview** (`CartItems`) | Per group (plans / applications / services): item name + billing period, original price right-aligned, optional discount-line badges, `Total:` line with the per-item current-cycle price, and a small *"Price for next billing cycle"* hint when the next-cycle amount differs (e.g. promo first cycle vs. regular renewal). | — |
| **Invoice details** (`InvoiceDetails`) | Collapsed summary view by default (Company name, Company number/VAT, Company ID, Country, Address, Name, Email). Pencil icon → inline edit form (`FormDetails`); *Add invoice details* button when none on file. | [[billing-invoicing]] |
| **Payment method** (`Payments`) | Shows saved card when present (brand uppercased + masked last-4 + expiry *"Exp. MM/YY"*). Pencil icon → inline gateway module (`FormStripe` or `FormPayments`, depending on `siteUser.payment_provider`). | [[billing-cards]] |
| **Discount code** (`Discount`) | Single text input + **Apply** button. Visible only when `cart.id` is set AND `cart.hide_discount` is false. On success, input flips read-only and **Remove** replaces *Apply*. | [[plans-purchase-discount-codes]] |
| **Totals** (`Totals`) | Subtotal (without VAT) / Discount (negative) / Total (without VAT) / VAT / **Payment amount** (with VAT, bold). | — |

### Stripe Setup-Element configuration

When `payment_provider = stripe`, the inline gateway module mounts a `payment` Element into `#dropin-container` with:

- `clientSecret`
- `customerSessionClientSecret`
- `locale` per merchant language
- Custom appearance (primary color `#8d58e0`)

Confirming runs `stripe.confirmSetup({ redirect: 'if_required', payment_method_data: { allow_redisplay: 'always' } })`. See [[billing-cards]] for the full gateway behaviour.

### Currency formatting source

Totals formatting is sourced from `cart.currency`: `sign_left`, `sign_right`, `dec_point`, `thousands_sep`, `coins_pad`. The merchant cannot change these on this screen — they flow from the invoicing-country setup.

### Pay now button states

| State | Cause |
|-------|-------|
| Enabled | Both `invoicing` and `paymentMethod` are non-null AND `submitLoader` is false. |
| Disabled — `invoicing` null | No invoice profile on file. |
| Disabled — `paymentMethod` null | No saved card on file. |
| Disabled — `submitLoader` true | Submission in flight. |
| Spinning | Submission in flight (renders `<b-spinner small>`). |

Button styling: `btn-black wide`.

## Business rules

### Order overview reads from `cart.original_total_without_vat / discount_total_without_vat / total_without_vat / total_vat / total`

The Totals card values come directly from the cart's computed totals — the merchant cannot edit them. Discount lines render only when the cart has applied a discount.

### Cancel button does not lose selection

The **Cancel** / *Back* button in the panel header collapses the checkout panel and returns the merchant to the PlanPanel beneath. The plan + add-on selection is preserved on the PlanPanel — the merchant can adjust and re-open Checkout without re-picking. The Proceed-to-Checkout button on the PlanPanel is `:disabled="buyPanel"` while the checkout panel is open, so the merchant can't double-trigger.

### 3D Secure mid-flight challenge (Braintree)

If *Pay now* returns a `clientToken` (instead of a success/error), the panel knows Braintree needs a 3DS challenge for the renewal charge. It then:

1. Loads `braintree-web/client.min.js` and `braintree-web/three-d-secure.min.js` (v3.94.0) from `js.braintreegateway.com` if not already on the page.
2. Creates a Braintree client + threeDSecure instance with `authorization: clientToken`.
3. Calls `threeDSecure.verifyCard({ amount, nonce, bin, challengeRequested: true })`. The merchant sees the bank's 3DS challenge in a modal (issuer-controlled UI).
4. On success, if `liabilityShifted === true`, re-submits the cart via `submit(response.nonce)`. On `liabilityShifted === false`, surfaces *"3DS response: liabilityShifted = false"* as a toast and the charge is not retried.

The Stripe path does **NOT** use this flow — Stripe's 3DS is embedded into the SetupIntent during card registration on [[billing-cards]]; for the *Pay now* step itself the saved payment-method is charged off-session.

### Per-item success / partial-success view

When *Pay now* succeeds the panel body swaps to a confirmation card:

- Green check icon + *"Thank you for your payment"* + *"Your order was completed successfully."* heading.
- *"We have sent detailed information about the order details to `<email>`"* — uses the cart's user email.
- For plan purchases (`record.type === 'plan_details'`), a per-item status list is rendered: each cart line shows the item name + a *Successful* / *Not successful* badge based on `status[].success`. See [[plans-purchase-subscription-outcomes]] for how partial success is computed server-side.
- The Cancel button in the header swaps to **Close**.

When the panel is closed after success, the parent screen reloads (`window.location.reload` after a 2.5-second delay) so the new plan / app / service / pack appears in the merchant's environment immediately.

### Cart-shape building (recap)

The records passed into this panel come from the PlanPanel's `buy` state, filtered to non-null entries:

- `buy.plan = { type: 'plan_details', mapping: <plan_details_id> }` — always present.
- `buy['service-<id>'] = { type: 'cloudcart_service', mapping: <service_id> }` — per ticked service.
- `buy['app-<key>'] = { type: 'cloudcart_app', mapping: <app_key> }` — per ticked app.

These are passed as `:records="buyFiltered"`. See [[plans-purchase-recommended-addons]] for how the keyed map is built.

## Related

- [[plans-purchase]] — hub.
- [[plans-purchase-billing-cycle]] — the variant picker that seeds the plan line.
- [[plans-purchase-recommended-addons]] — the optional services/apps lines.
- [[plans-purchase-discount-codes]] — Discount card behaviour + promo-code session seeding.
- [[plans-purchase-subscription-outcomes]] — invoice / payment validation, `MODE_UPDATE` reuse, LTA contract path, per-item failure surfacing.
- [[billing-invoicing]] — InvoiceDetails inline form behaviour.
- [[billing-cards]] — saved-card management + Stripe / Braintree gateway modules.
- [[subscriptions]] — where created subscriptions appear after a successful charge.

## Open questions

None.
