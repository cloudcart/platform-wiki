---
type: storefront-page
nav_path: "Storefront → Checkout → Payment step"
route_name: checkout.payment
route_path: /checkout/payment
themes_using: [all]
aliases: ["Checkout payment step", "Card payment", "Offline payment", "COD", "Bank transfer", "BNPL checkout", "Leasing checkout", "Стъпка плащане", "Карта на изплащане"]
tags: [storefront, checkout, payment, providers, card, offline, bnpl, leasing]
plan_gates: []
created: 2026-06-12
updated: 2026-06-12
source_count: 4
---

> Part of [[checkout]]. Follows [[checkout-step-shipping-method]]; precedes [[checkout-page-submit]]. The full backend filter pipeline that decides which providers reach this step lives in [[settings-payment-providers]] + this page's "How filtering works" section.

# Checkout — Payment step

## Purpose

The customer picks the payment provider for the order. The platform supports **5 broad payment types** under one UI: card gateways, offline methods (COD, bank wire, voucher), buy-now-pay-later (BNPL), leasing/installments, and digital wallets. This page documents how the storefront groups them, what each row carries, what filters decide which providers appear, and the per-provider extras (leasing terms tables, customer-details forms, descriptions).

## URL & route

See `route_name` and `route_path` in frontmatter. This is a sub-section of [[checkout]] — the parent `/checkout` page hosts these step containers; container reload routes are listed under "Where to find it".

## How it loads

Loaded as a sub-region of the `/checkout` page (see [[checkout-page-routing]] for the parent route + middleware stack). On step transitions, the container is GET-reloaded via its `data-ajax-box` URL — see [[checkout-flow-storefront-backend-bridge]] for the full reload-fragment map.

## Where to find it

Below the shipping-method step on `/checkout`. DOM: `<div class="cc-checkout-step js-checkout-payment">`. Container reloads via `data-ajax-box="{route('checkout.payment')}"` whenever upstream state (address, shipping method) changes.

## What the customer sees — two payment groups

The template splits providers into TWO accordion groups based on `$m->payment_provider->group`:

### Group 1 — Regular (`$managers->get('regular')`)

Every non-credit provider — card gateways, COD, bank wire, vouchers, e-wallet integrations, BNPL providers (Mokka / Klear / DSK BNPL / Fibank BNPL). Each gets its own accordion row:

- **Radio button** under `name="checkout[payment][provider]"` value = provider code (e.g. `stripe`, `cod`, `borica_way4`, `dsk_bnpl`).
- **Provider logo** (`$m->getImage('150x150')`).
- **Storefront display name** (`$m->storefront_name`).
- (Optional) **Description body** — when `payment_description` setting is `1` (default) AND the provider has `configuration['payment_description']` set, the merchant's HTML description renders in the row body.
- (Optional) **Customer-details sub-form** — when `$m->supportCustomerDetails = true`, an extra form section appears via `$m->renderCustomerDetails` — e.g. additional identity fields, terms-of-service link.

### Group 2 — Credit (`$managers->get('credit')`)

All consumer-credit / leasing providers (TBI, BNP Paribas, UCF, Smart-UCF, etc.) collapse into ONE parent accordion called **"Buy on credit"** (`sf.leasing.buy.label.submit`). Inside, each provider gets its own nested accordion row with:

- Provider radio (under `name="checkout[payment][provider]"` — same field as Group 1).
- **Customer info sub-form** (`creditor_checkout_form_customer.tpl`) — leasing requires more data (date of birth, monthly income, etc.).
- **Leasing terms table** — the available installment plans for the cart total. Built by the platform code with the current cart products + total + already-picked plan.
- **Conditions block** — provider-specific T&Cs from `$m->html['conditions']`.

## How filtering works — why provider X may not appear

The controller (the platform code line ~1651) runs a multi-stage filter on the platform code. Verified pipeline (2026-06-12):

| Stage | Filter |
|---|---|
| 1 | `min_price` — provider's configured min order amount. Cart `getTotal('input') < min_price` → drop. |
| 2 | `isAllowedByOrderAmount` — per-provider min/max amount allowance (often used by BNPL to cap small orders). Drop if outside. |
| 3 | Hide-billing-address gate — when the cart hides billing, **credit-group providers are dropped** (leasing requires a billing identity). |
| 4 | **Per-category restrictions** — for each cart product, the category's `restrictions` rows of type `payment` allowlist the providers it accepts. The provider must be allowlisted by EVERY cart product's category (AND-intersection). Outside the intersection → drop. |
| 5 | If a shipping manager is picked: `supportsCashOnDelivery` AND quote `allowanceCashOnDelivery` — both true to keep `cod`. Else drop. |
| 6 | Same gate for `pop` (Pay on place) — needs `supportsPayOnPlace` AND quote `allowancePayOnPlace`. |
| 7 | If the shipping provider has a **per-provider payment allowlist** (`provider->payments`), only providers IN the list survive. Used by carrier integrations that restrict which gateways they accept on COD-style orders. |
| 8 | If the cart is **not shippable** (digital-only), `cod` and `pop` are dropped from the list. |

So a single missing provider can be traced to any of these 8 stages. Common support diagnostics:

- *"Stripe is missing but I configured it"* → check shipping manager's `provider->payments` allowlist (stage 7) and category restrictions (stage 4).
- *"COD missing for digital goods"* → stage 8.
- *"BNPL missing on small orders"* → stage 2 (`isAllowedByOrderAmount`).
- *"Leasing missing when 'Use different billing' is off"* → stage 3.

## Per-provider extras

### Provider description (`payment_description` setting)

When `payment_description` setting on the store is `1` (default) and the provider has its own `configuration['payment_description']`, the merchant's HTML description renders inside the provider's expanded accordion body. Turning the setting OFF hides ALL provider descriptions store-wide.

### Customer-details extra form

Providers that return `supportCustomerDetails = true` inject extra fields in the row body via `renderCustomerDetails`. Used by:

- **Borica installments** — number-of-installments selector.
- **Some BNPL providers** — additional identification fields.

The form is part of the same `checkout[payment][...]` submission tree.

### Leasing terms table (credit group only)

The leasing terms widget (`widgets/payment/creditor_checkout_form_terms.tpl` or `creditor_checkout_form_terms_multy.tpl` when multi-term) shows the customer the available installment plans for THIS cart total. Each plan is a row with monthly payment, number of installments, total cost. The customer picks one before placing the order.

### Recalculate shipping on payment change

Some providers (typically COD-style ones that add a courier fee) flag `support_recalculate_shipping = true`. The payment radio then carries `data-shipping-recalculate="{route('checkout.shipping.recalculate')}"`. Selecting the radio re-fires the shipping pipeline so totals stay accurate.

## Settings & fields

| Setting | Where | Effect |
|---|---|---|
| `payment_description` | [[settings-cart]] | Toggle provider-description body. |
| `default_payment_provider` | [[settings-cart]] | Pre-selected provider on first render. |
| `min_price`, `min_amount`, `max_amount` | per-provider config — [[settings-payment-providers]] | Drop filter stages 1–2. |
| Category `payment` restrictions | [[products-categories-cart-restrictions]] | Per-category allowlist (stage 4). |
| Shipping provider's `payments` allowlist | [[settings-shipping]] | Stage 7 — couriers restricting payment combos. |

## Business rules

- **`checkout[payment][provider]` is one field across both groups.** The credit group's parent radio is a UI device — the actual submitted value is the inner provider's code.
- **Place order is gated by an explicit pick.** When no provider is active and no default, the next-step CTA stays disabled.
- **Per-provider gateway behaviour at Place Order** — see [[checkout-page-submit]] for redirect / popup / inline-tokenise variants.
- **All providers write to the same `Payment` entity at order creation** — see [[payment-provider-mechanism]] for the 5-stage provider lifecycle.

## Storefront behaviour

See [[checkout-flow-storefront-backend-bridge]] for the DOM → endpoint → cart-attribute → reload-fragment full map. This section's specific form/click handlers + reload arrays are documented inline in the sections above.

## JavaScript behaviour

The container uses the universal checkout JS hooks — `.js-form-submit-ajax-new` (intercepts form submit, processes JSON response), `.js-checkout-hash-reload` (URL hash → auto-reload on page entry), `cc.checkout.step` event. Full catalogue: [[checkout-page-javascript]].

## Customisations available to the merchant

Merchant-controlled settings affecting this section are listed under "Settings & fields" above. Full theme-wide customisation catalogue: [[checkout-page-customisation]].

## Theme variations

The template is shared from the theme templates — every theme inherits the same DOM. Themes can override individual sub-templates for per-theme tweaks, but the structure documented here applies to the default `flair` theme and every variant unless explicitly overridden.

## Known issues / by-design vs bug

None recorded for this section. Any merchant-facing surprises specific to this step are noted inline in the sections above (Business rules / Open questions).

## Related

- [[checkout]] — hub.
- [[checkout-step-shipping-method]] — previous step (flag flow into payment filtering).
- [[checkout-page-submit]] — Place Order CTA + per-provider redirect behaviour.
- [[settings-payment-providers]] — provider catalogue + admin config.
- [[settings-cart]] — `payment_description`, `default_payment_provider`.
- [[products-categories-cart-restrictions]] — per-category restriction model.
- [[settings-shipping]] — shipping-provider's payment allowlist (stage 7).
- [[payment-provider-mechanism]] — 5-stage provider lifecycle.
- [[payment-providers-tbi]] / [[payment-providers-bnp]] / [[payment-providers-dsk-bnpl]] / [[payment-providers-fibank-bnpl]] — leasing/BNPL integrations.
- [[settings-payment-providers]] / per-provider pages — e.g. [[payment-providers-stripe]], [[payment-providers-cloudcart-pay]], [[payment-providers-borica-way4]].

## Open questions

None — 8-stage filter pipeline verified against the platform code line 1651–1750 on 2026-06-12.
