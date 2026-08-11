---
type: feature
nav_path: "Payment Providers → DSK BNPL"
route_name: apps.dsk_bnpl.overview
route_path: /admin/payment-providers/dsk_bnpl
aliases: ["DSK BNPL", "DSK Buy Now Pay Later", "DSK покупка на изплащане", "DSK Pay", "DSK Bank installment", "ДСК БНПЛ", "ДСК покупка на изплащане"]
tags: [paymentproviders, payment-providers, dsk-bnpl, bnpl, installments, bulgaria]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 1
---
# DSK BNPL

## Purpose

**DSK BNPL** ("Buy Now Pay Later") is the installment-loan payment method offered by DSK Bank (Bulgaria's largest retail bank). The merchant signs a DSK Pay contract with the bank, receives a **Store Unique ID** and a **public-key PEM file**, enters those on the Settings tab, and the **DSK BNPL** method becomes selectable on the storefront checkout. The customer picks an installment plan, fills in a credit application on DSK Bank's redirected page, and on approval the bank pays the merchant the full order amount (like a regular card payment) while the customer repays the bank over the agreed number of months.

All loan-product configuration — interest-free schemes, eligibility rules, max loan amount, age limits, which goods qualify — is managed by DSK Bank. The merchant does NOT configure those in CloudCart; CloudCart only asks DSK to calculate plans for the cart and shows the results at checkout.

**Target market: Bulgaria.** All amounts in BGN (currency code `1` in the API). The customer flow runs in Bulgarian on DSK Bank's pages. Loan terms (installments, monthly payment, NIR, APR / GPR, total repayment) are returned by DSK in real time per order — the merchant doesn't pre-define them.

## Where to find it

Sidebar → **Payment Providers** → click **DSK BNPL**.

The route is `/admin/payment-providers/dsk_bnpl`. The hub renders the standard payment-provider overview with three tabs: **Overview**, **Settings**, **Promotions**. Switching tabs makes the URL `/admin/payment-providers/dsk_bnpl/<tab>`.

## What the merchant can do here

- **Read the overview card** — logo, description, and the standard install / activate / deactivate buttons all payment providers share.
- **Install / Uninstall** through the overview's standard buttons. Installing creates the provider configuration for `dsk_bnpl`.
- **Activate** once the Store Unique ID + public key are saved and verified against DSK Bank.
- **Switch between the three tabs** to manage the lifecycle:
  - [[payment-providers-dsk-bnpl-settings]] — enter the Store Unique ID, upload the public-key PEM file, set a minimum order value.
  - [[payment-providers-dsk-bnpl-promotions]] — map specific products to a DSK "promotion ID" assigned by the bank.

## Settings & fields

This is a hub page — the integration fields live on the two sub-tabs. The overview itself exposes only the standard payment-provider controls:

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Install** button | Creates the provider configuration for `dsk_bnpl`. | Not installed | One-click; safe to undo via Uninstall. |
| **Active** switch (header) | Turns the method ON / OFF for checkout. | OFF | Server refuses activation unless Store Unique ID + public key are saved AND DSK's calculation responds. |
| **Logo / Title / Description** | Customer-facing label at checkout. | Provider defaults | Standard. |
| **Min / Max amount** | Order-total range in which DSK BNPL shows. | Empty | Independent of the **Minimum order value** on the Settings tab — both must pass. |
| **Discount** | Optional discount when the customer picks this method. | None | Standard. |

The Store Unique ID, public-key file, and minimum order value live on the [[payment-providers-dsk-bnpl-settings|Settings sub-tab]]; per-product promotion overrides on the [[payment-providers-dsk-bnpl-promotions|Promotions sub-tab]].

## Business rules

### How DSK BNPL works for the merchant

DSK BNPL is **NOT a true split-payment-at-checkout product** — it's a **redirect-to-bank credit application** that ends with DSK Bank paying the merchant the full order amount. For the merchant's cash flow it behaves like any card-payment provider: a single payout after the loan is approved. The customer takes out a 3–60 month consumer loan with DSK Bank for a single basket.

The customer flow:

1. **Checkout** — the customer picks DSK BNPL. CloudCart asks DSK to calculate plans for the cart total and product IDs (or mapped DSK promotion IDs), and shows the returned schemes — each with number of installments (Maturity), monthly payment, down payment, NIR, APR / GPR, and total repayment.
2. **Picks a plan** — scheme + variant + optional down payment.
3. **Redirect to DSK** — the customer is sent to DSK Bank's page with their name / phone / email / address and fills in DSK's credit application. This step is entirely on DSK's side; CloudCart holds the order as PENDING.
4. **DSK approves or rejects** — payment status updates via the [[#status-sync-every-hour|hourly status sync]]: PENDING while DSK reviews, CANCELED if DSK rejects or the customer abandons, COMPLETED once DSK approves and pays; otherwise FAILED.
5. **Merchant gets paid** — on approval the merchant receives the full order amount, less DSK's commission, settled outside CloudCart per the DSK contract.

### Refund handling

Refunds are NOT initiated through CloudCart — there is no refund flow in the DSK BNPL integration. The merchant contacts DSK Bank directly and updates the order status manually.

### Initial payment (down payment)

The customer can specify a down-payment amount at checkout, sent to DSK as `initial_payment`; DSK then returns plans whose monthly installment is calculated on `(price − initial_payment)`. There is no default percentage — it's per-order, customer-chosen.

### Mobile vs desktop redirect

The redirect to DSK includes `type_client`: `1` for mobile/tablet, `0` for desktop, so DSK renders a phone- vs desktop-friendly credit-application page.

### Status sync — every hour

DSK does NOT push status updates back — CloudCart polls. An hourly background job checks DSK for every PENDING DSK BNPL payment and updates it; this is the main way orders move from PENDING to COMPLETED or CANCELED in the admin.

### Promotions — per-product DSK loan-product mapping

DSK Bank can assign specific catalog products a custom "promotion ID" (e.g. "0% interest for 6 months on TV X"). The merchant maps the CloudCart product to that DSK promotion ID on the Promotions tab so pricing uses it instead of the product's CloudCart ID. See [[payment-providers-dsk-bnpl-promotions]].

### Plan-gating

NOT gated by CloudCart plan — every plan can install DSK BNPL. (The merchant needs an active DSK Pay contract, a separate business relationship.)

### Country + currency

Currency is hardcoded to BGN (currency code `1` in the API); customer addresses are expected to be Bulgarian. DSK BNPL is not usable in other countries.

## Related

- [[payment-providers]] — parent hub.
- [[payment-providers-dsk-bnpl-settings]] — Store Unique ID, public key, minimum order value.
- [[payment-providers-dsk-bnpl-promotions]] — per-product DSK loan-product mapping.
- [[payment-providers-dsk-zero]] — DSK Bank's 0% interest installment method (separate provider, see [[#dsk-bnpl-vs-dsk-zero]]).
- [[payment-providers-fibank-bnpl]] — equivalent BNPL product from Fibank; near-identical integration shape (different bank).
- [[payment-providers-fusion-pay]] — TBI Bank installment payment (different bank).

### DSK BNPL vs DSK Zero

CloudCart has TWO separate DSK Bank payment providers, frequently confused:

- **DSK BNPL** (this page) — general installment loan; DSK picks the interest rate per customer, repaid over 3–60 months. Available to ALL stores.
- **DSK Zero** (see [[payment-providers-dsk-zero]]) — 0% interest, no down payment. The merchant pre-defines which products qualify and the maximum number of months. Available only to stores flagged as `zora` (DSK Bank's partner program); hidden for non-zora stores.

Both can be installed in the same store; they have different APIs, settings, and cash-flow models.

## Open questions

- ⏸️ The payout schedule (when DSK transfers funds after approval) depends on the DSK contract, not CloudCart. CloudCart receives no settlement webhook — settlement is reconciled by the merchant in their DSK Bank portal.
