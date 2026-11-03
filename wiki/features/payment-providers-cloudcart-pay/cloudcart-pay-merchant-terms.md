---
type: feature
nav_path: "Payment Providers → Cloudcart Pay → Agreement and terms"
route_name: apps.cloudcart_pay.onboarding
route_path: /admin/payment-providers/cloudcart_pay/onboarding
aliases: ["CloudCart Pay agreement", "CloudCart Pay contract", "CloudCart Pay terms", "Tri-Party Merchant Agreement", "CloudCart Pay chargebacks", "CloudCart Pay prohibited products", "Договор CloudCart Pay", "Условия CloudCart Pay", "Споразумение CloudCart Pay", "Оспорени плащания CloudCart Pay"]
tags: [paymentproviders, payment-providers, cloudcart-pay, agreement, chargebacks, compliance]
plan_gates: []
created: 2026-10-06
updated: 2026-10-06
source_count: 2
---

> Part of [[payment-providers-cloudcart-pay]]. See the hub for the other aspects.

# CloudCart Pay — the agreement and its terms

## Purpose

What the merchant agrees to when they start using CloudCart Pay, and the terms a merchant is most likely to ask about: what the agreement covers, chargebacks, prohibited products, changes and termination.

There is no separate negotiation with a bank: the agreement is accepted with ticks in step 5 of the onboarding. It covers:

- **Accepting card payments** through CloudCart Pay, and **paying the money out** to the merchant's bank account.
- **The onboarding checks** — the business and identity information and documents, and keeping them up to date.
- **The fees** for the service ([[cloudcart-pay-pricing]]).
- **Chargebacks and disputes** — who bears them and how they are handled.
- **What may not be sold** with CloudCart Pay.
- **Card data and security**, and the handling of personal data.
- **Support** for onboarding, technical, payout and chargeback questions.
- **Suspension, changes and termination.**

## Where to find it

Payment Providers → CloudCart Pay → **Onboarding** → step 5, **Споразумения и верификация на самоличността** (Agreements and identity verification). Each document opens from its link and must be ticked:

| Document | What it is |
|---|---|
| **Tri-Party Merchant Agreement** | The main agreement for the service. |
| **Tri-Party Merchant DPA** | The terms for processing personal data. |
| **Payment Instruction** | Required; its text opens from the link. |
| **Fee Schedule to the Tri-Party Merchant Agreement** | The prices — see [[cloudcart-pay-pricing]]. |
| **Nominee Agreement** | Required; its text opens from the link. |
| **Paynetics Privacy Policy** | The privacy policy that applies to the payment data. |

All six are required. The button is **Приемане и изпращане** (Accept and submit). See [[ccpay-onboarding-verification-attestation]] for the rest of the step.

## What the merchant can do here

- Read and accept the six documents during onboarding.
- End the agreement at any time with written notice. Either side may do so.

## Settings & fields

None. The documents are accepted once, in the onboarding.

## Business rules

**Accurate information, kept current.** The merchant must keep their details accurate and report changes: ownership or control, legal form, products or services sold, main activity and merchant category (MCC), sales channels, trading names, country, approved web addresses and payout account. Some changes need a new review.

**Prohibited activities.** CloudCart Pay may not be used for:
- illegal, deceptive or harmful activity;
- selling without the intent or ability to deliver;
- taking payments on behalf of third parties;
- goods that infringe intellectual property;
- activity breaching sanctions;
- anything banned by the card schemes or the payment institution.

Gambling, virtual currencies, adult content and weapons are allowed only when specifically approved. The list can be updated at any time.

**Chargebacks.**
- The merchant is fully liable for chargebacks and any related card-scheme or payment-institution fees.
- Evidence must be provided by the deadline given. Not responding can lose the dispute automatically.
- Chargeback costs, fees and penalties can be deducted from the money being paid out or from a reserve.
- The store's refund and delivery policies must be clear and easy to find.

**Amounts that cannot be deducted** are invoiced and payable within **10 business days**. Unpaid amounts can lead to suspension or be set off against future payouts.

**Card data.** The card fields at checkout are provided in a PCI-compliant form. The merchant must never store card data themselves and must keep their own systems secure.

**Suspension.** Access can be suspended or limited for:
- a serious breach of the agreement;
- fraud or suspected fraud;
- too many chargebacks or disputes;
- security concerns;
- missing documents or information;
- serious customer complaints;
- an instruction from the payment institution, the card schemes or an authority.

Access is restored once the issue is resolved.

**Changes to the terms and prices** take effect **30 days** after notice, unless a shorter period is required by law or by the card schemes. Notices arrive by e-mail or in the dashboard. Continued use means acceptance.

**Ending the agreement.** Either side may end it at any time with written notice. Fees, chargebacks, refunds and penalties still owed then become due at once.

**Law and language.** Bulgarian law applies and Bulgarian courts decide disputes. The English text prevails over any translation.

## Related

- [[payment-providers-cloudcart-pay]] — hub.
- [[cloudcart-pay-pricing]] — the Fee Schedule and the 0% promotion.
- [[ccpay-onboarding-verification-attestation]] — step 5, where the documents are accepted.
- [[payment-providers-cloudcart-pay-onboarding]] — the whole onboarding.
- [[payment-providers-cloudcart-pay-payouts]] — the payouts from which deductions are made.

## Open questions

- The full published list of prohibited and restricted business categories, beyond the examples in the terms.
