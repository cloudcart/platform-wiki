---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Onboarding → Status → NRA declaration information"
route_name: apps.cloudcart_pay.onboarding
route_path: /admin/payment-providers/cloudcart_pay/onboarding
aliases: ["NRA declaration information", "Electronic Store Declaration", "Appendix 33 Ordinance N-18", "Appendix №33", "MID and TID for NRA", "Virtual POS ID", "Декларация за НАП", "Приложение 33 Наредба Н-18", "Декларация за електронен магазин", "Данни за декларацията към НАП", "MID и TID за НАП"]
tags: [paymentproviders, payment-providers, cloudcart-pay, onboarding, n18, nra, compliance, bulgaria]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---

> Part of [[payment-providers-cloudcart-pay-onboarding]]. See the hub for the other aspects (wizard flow, fields, people, documents, verification, bank, status, review and alerts).

# CloudCart Pay — NRA declaration information

## Purpose

A Bulgarian store files an Electronic Store Declaration (Appendix №33 to Ordinance Н-18) with the National Revenue Agency. This card gives the CloudCart Pay payment details that go into it: the payment service provider, the merchant and virtual POS IDs, the settlement type, the receiving bank account and the accepted agreement, with a PDF to download. The card's own intro: *"Payment details for the Electronic Store Declaration (Appendix №33 to Ordinance Н-18) that you file with the National Revenue Agency. CloudCart Pay does not submit the declaration — use this information when you or your accountant complete it."*

## Where to find it

Settings → Payment methods → CloudCart Pay → **Onboarding** tab → step 7, **Status** ([[ccpay-onboarding-status-capabilities]]) → the card **NRA declaration information**. It appears for accounts with country Bulgaria.

## What the merchant can do here

- **Read the payment details** for the declaration.
- **Download PDF**, once the information is ready.
- **Update information**, which prepares a fresh copy, for example after the bank account or the agreement changed.

## Settings & fields

The card has no settings. It shows one block per payment arrangement:

| Label | What it shows |
|---|---|
| **Payment service provider** | Legal name, registration number, country, contact e-mail. |
| **Merchant ID (MID)** | The merchant's ID at the provider. |
| **Virtual POS ID (TID)** | The virtual POS's ID. |
| **Settlement** | *Through the payment service provider*, *Directly to the merchant* or *Not specified*. |
| **Currency and payment methods** | For example the currency and *Card*. |
| **Receiving bank account** | The account numbers, such as IBAN and BIC. |
| **Accepted agreement** | Links to the agreement's documents, with *Accepted on {date}*. |

Below the blocks: *Prepared on {date}*.

| Badge | Meaning |
|---|---|
| **Preparing** | The information is being prepared. |
| **Information complete** | Everything needed is present. |
| **Information incomplete** | See the warning block on the card. |
| **Failed** | The information could not be prepared. |

## Business rules

### When the information is available

Before the account can take payments, the card reads *"The information becomes available once your account can accept payments."* Without data for the account: *"No declaration information is available for your account yet."*

### Preparing a copy

The first visit prepares the first copy on its own. **Update information** prepares a new one. It usually takes about a second, and the page waits up to two minutes (*"Preparing the information…"*). Each copy is fixed at the moment it was prepared, and the card shows the latest. CloudCart stores none of this; the card reads it from CloudCart Pay each time.

### Missing or unverified details

The warning block *"Some information is missing or not yet verified"* lists what is wrong, for example:

- *"The merchant ID (MID) is not available yet."*
- *"The virtual POS ID (TID) is not available yet."*
- *"The accepted agreement could not be found."*
- *"The bank account for payouts could not be found. Check it in the Bank Account step or contact our support team."*

It ends with *"You can still download the document and complete the rest of the declaration yourself."* The bank account is on [[ccpay-onboarding-bank-account]], the agreement on [[ccpay-onboarding-verification-attestation]].

### When preparing fails

*"The information could not be prepared. Update it to try again; if it keeps failing, contact our support team with reference {id}."*

### Who can open it

Staff whose role allows the store's payment methods settings (`settings`, `store.payment_providers`), as for the other CloudCart Pay tabs ([[settings-staff]]).

### The monthly audit file is separate

This card covers the declaration's payment details. The monthly audit file the store submits under the same ordinance comes from another app: [[apps-n18-audit]].

## Related

- [[payment-providers-cloudcart-pay-onboarding]] — hub.
- [[ccpay-onboarding-status-capabilities]] — the Status step holding this card.
- [[ccpay-onboarding-bank-account]] — the receiving bank account.
- [[ccpay-onboarding-verification-attestation]] — the accepted agreement.
- [[apps-n18-audit]] — the monthly audit file.

## Open questions

- Bulgarian labels of the card (production translation table).
