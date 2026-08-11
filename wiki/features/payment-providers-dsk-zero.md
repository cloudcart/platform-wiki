---
type: feature
nav_path: "Payment Providers → DSK Zero"
route_name: apps.dsk_zero.overview
route_path: /admin/payment-providers/dsk_zero
aliases: ["DSK Zero", "DSK 0%", "DSK Bank 0%", "DSK Bank Zero", "DSK 0 percent", "DSK zero interest", "ДСК 0%", "ДСК Зеро", "ДСК лизинг 0%"]
tags: [paymentproviders, payment-providers, dsk-zero, bnpl, installments, zero-interest, bulgaria]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 1
---
# DSK Zero

## Purpose

**DSK Zero** is DSK Bank's 0%-interest installment-loan payment method — a separate product from the general [[payment-providers-dsk-bnpl|DSK BNPL]] integration. The customer picks a number of months from a merchant-curated list and repays the bank at **0% interest** — no monthly interest, no APR markup. The total the customer repays equals the order total, split evenly across the agreed months. The merchant absorbs the cost of the interest-free credit (DSK charges the merchant a commission on the loan).

Unlike DSK BNPL, where DSK's API decides everything, with DSK Zero **the merchant pre-configures the eligible loan schemes themselves** — one or more **Schemes**, each a (months, products) pair saying "these specific products can be bought over this number of months at 0%." At checkout the storefront reads these schemes locally (no call to DSK at calculation time), filters them by the cart contents, and shows the resulting plans. The customer applies for the loan with DSK Bank after picking a scheme.

The provider is gated to stores enrolled in DSK Bank's `zora` partner program — non-zora stores never see it (see Business rules → Zora-only gating). **Target market: Bulgaria; all amounts in BGN.**

## Where to find it

Sidebar → **Payment Providers** → click **DSK Zero**.

The route is `/admin/payment-providers/dsk_zero`. The hub page renders the standard payment-provider overview shared with other providers, with three tabs at the top: **Overview**, **Settings**, **Schemes**. Switching tabs is handled by the router; the URL becomes `/admin/payment-providers/dsk_zero/<tab>`.

## What the merchant can do here

- **Read the overview card** — logo, description, and the standard install / activate / deactivate buttons that all payment providers share.
- **Install / Uninstall the payment method** through the overview's standard buttons. Installing creates a provider configuration row for `dsk_zero`.
- **Activate the payment method** once the email + agreement/merchant ID + at least one scheme are saved.
- **Switch between the three tabs** to manage the lifecycle:
  - [[payment-providers-dsk-zero-settings]] — agreement/merchant ID, contact email, and a toggle to email DSK after every order.
  - [[payment-providers-dsk-zero-schemes]] — manage the list of (months, products) installment schemes the customer can pick from.

## Settings & fields

This is a hub page — the actual fields live on the two sub-tabs. The overview itself only exposes the standard payment-provider controls shared with every other provider:

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Install** button | Creates the provider configuration for `dsk_zero` so the provider exists in the store. | Not installed | Only appears on stores flagged as `zora`. |
| **Active** switch (header) | Turns DSK Zero ON / OFF for storefront checkout. | OFF | Standard payment-provider activation. |
| **Logo / Title / Description** | Customer-facing label of the method on checkout. | Provider defaults | Standard payment-provider fields. |
| **Min / Max amount** | Order-total range in which DSK Zero shows on checkout. | Empty | Standard payment-provider amount-range controls. |
| **Discount** | Optional discount applied when the customer picks this method. | None | Standard. |

## Business rules

### How DSK Zero works for the merchant

DSK Zero is a curated, interest-free installment loan:

1. **Merchant pre-configures schemes** — on the [[payment-providers-dsk-zero-schemes|Schemes tab]] the merchant creates one or more schemes. Each scheme is `(months, products[])` — e.g., "6 months / [SKU-101, SKU-102]" + "12 months / [SKU-101, SKU-103]". A product can appear in multiple schemes.
2. **Storefront cart filtering** — when the customer checks out, the platform filters the merchant's schemes to ones where EVERY product in the cart is in the scheme's `products` array. If even one product in the cart is not in the scheme, that scheme is hidden.
3. **Customer sees 0% plans** — for each surviving scheme the storefront shows: "X months × {orderTotal / X} BGN/month, 0% NIR, 0% APR".
4. **Customer applies for the loan** — DSK Zero does not currently redirect through an API integration to DSK Bank. **The merchant fulfills the order through DSK's offline / portal flow.** Status sync is manual.
5. **Cross-scheme cart rejection** — if the customer somehow gets products from DIFFERENT schemes in the cart, an error message is shown: "Има продукти от различни лизингови схеми. Моля, направете отделни поръчки" ("There are products from different leasing schemes. Please make separate orders."). The merchant doesn't need to configure this.

### Pricing calculation — flat 0%

The platform's installment calculator runs with a 0% monthly rate. For an order of price P over N months the customer sees:

- Monthly installment: `P / N`
- NIR (yearly interest rate): 0%
- APR (annual cost of credit): 0%
- Total repayment: P (no markup)
- Down payment: 0

This is hard-coded to 0% per month; the merchant doesn't pick a rate.

### Zora-only gating

The provider is **invisible to stores not in the `zora` program**. CloudCart checks whether the store is enrolled in DSK Bank's "Zora" partner program (by store ID, against a list maintained by the CloudCart platform team in coordination with DSK Bank) and silently removes DSK Zero before rendering for non-enrolled stores. For non-zora stores the provider never appears in the Payment Providers list, the storefront cannot select it, and there is **no UI message** explaining why — it simply doesn't show up. The merchant cannot self-enrol; enrolment is added or removed on DSK's side.

This is the primary "plan gate" for DSK Zero. It is NOT a CloudCart plan gate (Pro/Business/Enterprise) — it's a per-store enrollment flag.

### Order notification email + manual loan round-trip

The loan-approval round-trip with DSK Bank is entirely manual / email-based — there is **no programmatic status callback** from DSK Zero. When **Send an email after completing an order** is enabled (Settings tab), CloudCart sends an email after every DSK Zero order completion to the configured `email` address (default `the provider's support address`, optionally overridden by the merchant). This is the operational glue between CloudCart's order flow and DSK's offline approval workflow: it flags the order to DSK staff, the merchant logs into DSK Bank's own portal to process the customer's loan application, then **updates the order status in CloudCart manually** after coordinating with the bank.

### Refund handling

DSK Zero refunds are NOT automated. The merchant coordinates with DSK Bank directly via the operational email channel.

### Currency + country

BGN only, Bulgaria only. No API endpoints are called at calculation time — the integration is entirely local; only the post-order email notifies DSK.

## Related

- [[payment-providers]] — parent hub.
- [[payment-providers-dsk-zero-settings]] — agreement / merchant ID + email contact.
- [[payment-providers-dsk-zero-schemes]] — the (months, products) installment-scheme list.
- [[payment-providers-dsk-bnpl]] — DSK Bank's general (non-0%) BNPL — separate integration, no `zora` gating, real-time API to DSK. See [[payment-providers-dsk-bnpl#dsk-bnpl-vs-dsk-zero|DSK BNPL vs DSK Zero]] for the difference.
- [[payment-providers-fibank-bnpl]] — Fibank's BNPL with interest (different bank).

## Open questions

(none)
