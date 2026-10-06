---
type: feature
nav_path: "Payment Providers → Cloudcart Pay → Pricing"
route_name: apps.cloudcart_pay.overview
route_path: /admin/payment-providers/cloudcart_pay
aliases: ["CloudCart Pay fees", "CloudCart Pay pricing", "CloudCart Pay commission", "CloudCart Pay transaction fee", "0% fee", "Zero commission", "Free until 31.12", "Fee Schedule", "Такси CloudCart Pay", "Комисионна CloudCart Pay", "Цена CloudCart Pay", "0% такса", "Без комисионна до 31.12", "Колко струва CloudCart Pay"]
tags: [paymentproviders, payment-providers, cloudcart-pay, pricing, fees]
plan_gates: []
created: 2026-10-06
updated: 2026-10-06
source_count: 2
---

> Part of [[payment-providers-cloudcart-pay]]. See the hub for the other aspects.

# CloudCart Pay — pricing

## Purpose

What a merchant pays for card payments taken with CloudCart Pay.

> **0% transaction fee until 31 December 2026.** CloudCart Pay went live for all merchants on **6 October 2026**. From then until **31 December 2026** it charges **no fee on transactions**: 0%.

From **1 January 2027** the standard prices apply. They are set out in the **Fee Schedule to the Tri-Party Merchant Agreement**, which the merchant accepts in step 5 of the onboarding ([[cloudcart-pay-merchant-terms]]).

## Where to find it

- The fees are in the **Fee Schedule** linked in step 5 of the onboarding (**Споразумения и верификация на самоличността**) — Payment Providers → CloudCart Pay → **Onboarding**. See [[payment-providers-cloudcart-pay-onboarding]].
- The fee taken on each payment shows in the **Fee** column of the **Transactions** tab ([[payment-providers-cloudcart-pay-transactions]]).

## What the merchant can do here

- Take card payments at 0% transaction fee until 31 December 2026.
- Read the standard prices that apply afterwards, in the Fee Schedule and below.
- See each payment's fee in the Transactions tab.

## Settings & fields

There are no settings for pricing. The standard fee on a transaction is a **percentage of the amount plus a fixed amount**, and depends on three things:

- **the merchant's country** — where the business is registered;
- **the card** — consumer Visa and Mastercard cards issued in the European Economic Area (EEA) are cheaper; "all other cards" covers everything else;
- **the currency** of the payment, which sets the fixed part.

**Standard fees from 1 January 2027**, for a payment in the merchant's own currency:

| Merchant country | EEA consumer Visa / Mastercard | All other cards |
|---|---|---|
| **Bulgaria** | 1.29% + €0.05 | 2.69% + €0.05 |
| **Greece** | 1.29% + €0.10 | 2.69% + €0.10 |
| **Romania** | 0.99% + 0.25 RON | 2.69% + 0.25 RON |
| **Czechia** | 0.99% + 1.25 CZK | 2.69% + 1.25 CZK |
| **Poland** | 1.29% + 0.25 PLN | 2.69% + 0.25 PLN |
| **Hungary** | 1.29% + 25 HUF | 2.69% + 25 HUF |
| **Slovakia, Slovenia, Croatia** | 1.29% + €0.10 | 2.69% + €0.10 |
| **Rest of the EU** | 1.29% + €0.10 | 2.69% + €0.10 |

The percentage stays the same in every currency: 0.99% in Romania and Czechia, 1.29% elsewhere, and 2.69% for all other cards. A payment in another currency carries that currency's fixed part instead:

| Currency | Fixed part |
|---|---|
| EUR | €0.10 (€0.05 for a Bulgarian merchant) |
| USD / GBP / CHF | 0.10 |
| RON | 0.50 (0.25 for a Romanian merchant) |
| PLN | 0.50 (0.25 for a Polish merchant) |
| CZK | 3.00 (1.25 for a Czech merchant) |
| HUF | 50 (25 for a Hungarian merchant) |
| BGN | 0.20 |

All fees are **exclusive of VAT**.

## Business rules

- **The promotion is on transaction fees.** Until 31 December 2026 no transaction fee is charged, whatever the card, currency or country.
- **What is not a transaction fee.** Chargebacks and any penalties a card scheme or the payment institution imposes over a merchant's activity remain the merchant's responsibility. They can be deducted from the money being paid out ([[cloudcart-pay-merchant-terms]]).
- **Fees can change with notice.** The agreement allows the prices to change with at least **30 days' notice**, or less when a change comes from the card schemes or the payment institution. Using the service after the notice period means accepting the new prices.
- **No plan gate.** CloudCart Pay is available on any plan that can install payment methods ([[payment-providers-cloudcart-pay]]).

## Related

- [[payment-providers-cloudcart-pay]] — hub.
- [[cloudcart-pay-merchant-terms]] — the agreement the prices belong to.
- [[payment-providers-cloudcart-pay-onboarding]] — where the Fee Schedule is accepted.
- [[payment-providers-cloudcart-pay-transactions]] — the fee taken on each payment.
- [[payment-providers-cloudcart-pay-payouts]] — the money paid out after fees.

## Open questions

- Whether the Transactions tab shows the fee as 0 during the promotion, or shows no fee line at all.
