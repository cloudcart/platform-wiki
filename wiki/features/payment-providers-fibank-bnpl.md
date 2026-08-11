---
type: feature
nav_path: "Payment Providers → Fibank BNPL"
route_name: apps.fibank_bnpl.overview
route_path: /admin/payment-providers/fibank_bnpl
aliases: ["Fibank BNPL", "Fibank Buy Now Pay Later", "Fibank E-Credit", "First Investment Bank BNPL", "Fibank installment", "Фибанк БНПЛ", "Фибанк покупка на изплащане"]
tags: [paymentproviders, payment-providers, fibank-bnpl, bnpl, installments, bulgaria]
plan_gates: []
created: 2026-05-21
updated: 2026-05-28
source_count: 1
---
# Fibank BNPL

## Purpose

**Fibank BNPL** ("Buy Now Pay Later") is the installment-loan payment method offered by Fibank (First Investment Bank, Bulgaria). The merchant signs a contract with Fibank for their E-Credit product, receives a **Store Unique ID** from the bank, enters it in this section of the admin panel, and the **Fibank BNPL** payment method becomes selectable on the storefront checkout. The customer picks an installment plan, fills in a credit application redirected from Fibank, and on approval the bank pays the merchant in full while the customer pays the bank back over the agreed number of months.

This provider behaves almost identically to [[payment-providers-dsk-bnpl|DSK BNPL]] — same status sync, same Promotions tab. The one big difference for the merchant: **Fibank's public key is bundled with CloudCart**, so the merchant does NOT upload one — they only need the Store Unique ID. The configuration surface is shorter.

This page is the entry point — from here the merchant lands on three sub-tabs: **Overview** (this page), **Settings** (Store Unique ID + minimum order value), and **Promotions** (per-product promotion overrides). All loan-product configuration, eligibility rules, max loan amount, customer age limits, and which goods are eligible are managed by Fibank on their side — the merchant does NOT configure those in CloudCart.

**Target market: Bulgaria.** All amounts in BGN. The customer flow is conducted in Bulgarian by Fibank. Loan terms (number of installments, monthly payment, NIR, APR, total repayment) are returned by Fibank's pricing in real time per order.

## Where to find it

Sidebar → **Payment Providers** → click **Fibank BNPL**.

The route is `/admin/payment-providers/fibank_bnpl`. The hub page renders the standard payment-provider overview shared with other providers, with three tabs at the top: **Overview**, **Settings**, **Promotions**. Switching tabs is handled by the router; the URL becomes `/admin/payment-providers/fibank_bnpl/<tab>`.

## What the merchant can do here

- **Read the overview card** — logo, description, and the standard install / activate / deactivate buttons that all payment providers share.
- **Install / Uninstall the payment method** through the overview's standard buttons. Installing also provisions the Fibank promotions storage if it doesn't already exist.
- **Activate the payment method** once the Store Unique ID is saved and verified against Fibank.
- **Switch between the three tabs** to manage the lifecycle:
  - [[payment-providers-fibank-bnpl-settings]] — enter the Store Unique ID and set a minimum order value.
  - [[payment-providers-fibank-bnpl-promotions]] — override the calculated installment plans for specific products with a Fibank "promotion ID" assigned by the bank.

## Settings & fields

This is a hub page — the actual fields live on the two sub-tabs. The overview itself only exposes the standard payment-provider controls shared with every other provider:

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Install** button | Installs the provider; also provisions the Fibank promotions storage if missing. | Not installed | One-click action. |
| **Active** switch (header) | Turns the payment method ON / OFF for storefront checkout. | OFF | Activation is refused unless the Store Unique ID is saved AND Fibank's calculation responds successfully. |
| **Logo / Title / Description** | Customer-facing label of the method on checkout. | Provider defaults | Standard payment-provider settings fields. |
| **Min / Max amount** | Order-total range in which Fibank BNPL shows on checkout. | Empty | Independent of the **Minimum order value** field on the Settings tab — both must pass. |
| **Discount** | Optional discount applied when the customer picks this method. | None | Standard. |

The Store Unique ID and minimum order value live on the [[payment-providers-fibank-bnpl-settings|Settings sub-tab]]. Per-product promotion overrides live on the [[payment-providers-fibank-bnpl-promotions|Promotions sub-tab]].

## Business rules

### How Fibank BNPL works for the merchant

Fibank BNPL is a **redirect-to-bank credit application** that ends with Fibank paying the merchant the full order amount. From the merchant's cash-flow perspective it behaves like any card-payment provider: a single payout from Fibank after the customer's loan is approved (minus Fibank's commission, settled outside CloudCart per the merchant's contract). From the customer's perspective they sign up for a consumer loan to buy a single basket.

The customer flow is:

1. Customer adds products to cart and picks Fibank BNPL at checkout.
2. Fibank returns pricing schemes for the cart, each with: number of installments (Maturity), monthly payment, initial / down payment, NIR (yearly interest rate), APR (annual cost of credit), and total repayment.
3. Customer picks a scheme + variant + optional initial payment.
4. The customer is redirected to Fibank's E-Credit page (name / phone / email / address / postal code / cart items are sent along) to fill in the credit application — identity verification, employment income, etc. The order stays pending while this happens on Fibank's side.
5. Fibank approves or rejects. Once approved, the merchant receives the full order amount.

### Status mapping

Fibank's status codes map: **0-4 = PENDING; 5 = CANCELED; 6 = COMPLETED; 7 (and anything else) = FAILED.** (This differs from DSK BNPL's mapping.)

### Eligibility is category-level

Fibank's pricing accepts `product_category_ids`, and CloudCart sends the FIRST product/category ID. Fibank's loan-eligibility check is therefore **category-level** on their side: the bank assigns interest rates per merchant-uploaded product category, not per individual product. The [[payment-providers-fibank-bnpl-promotions|Promotions tab]] is what the merchant uses to override this with a Fibank-issued promotion ID for a specific product.

### Status sync

A scheduled task runs hourly and polls Fibank for every pending Fibank BNPL payment, updating the order's payment status. Fibank does not push status updates back to CloudCart; CloudCart polls.

### Refund handling

Refunds for Fibank BNPL orders are NOT initiated through CloudCart's admin panel — the merchant contacts Fibank directly. There is no refund flow that goes through the Fibank BNPL API from the CloudCart side.

### Mobile vs desktop

`type_client` is sent: `1` for mobile/tablet, `0` for desktop — Fibank uses this to render a phone-friendly vs desktop credit-application page.

### Plan-gating

This provider is NOT gated by CloudCart plan — every plan can install Fibank BNPL. (The merchant needs an active E-Credit contract with Fibank.)

### Country + currency

BGN only, Bulgaria only. Customer addresses are expected to be Bulgarian. Fibank BNPL is not usable in other countries.

### Public key shipping

Unlike DSK BNPL where the merchant uploads the public key themselves, **Fibank's public key is bundled with CloudCart**. The merchant cannot upload their own — there's no key-rotation UI. If Fibank rotates the key, CloudCart ships an update with the new key.

## Related

- [[payment-providers]] — parent hub.
- [[payment-providers-fibank-bnpl-settings]] — Store Unique ID + minimum order value.
- [[payment-providers-fibank-bnpl-promotions]] — per-product Fibank promotion-ID mapping.
- [[payment-providers-dsk-bnpl]] — DSK Bank's equivalent BNPL — same shape, but the merchant uploads their own public key.
- [[payment-providers-fusion-pay]] — TBI Bank installment payment (different bank, different API).

## Open questions

- ⏸️ Whether Fibank nets commission out of each settlement or invoices it separately — a Fibank E-Credit contract detail, not encoded in CloudCart. Merchants read this from their Fibank E-Credit agreement.
