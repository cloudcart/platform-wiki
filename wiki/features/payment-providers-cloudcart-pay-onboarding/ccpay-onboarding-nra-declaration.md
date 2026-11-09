---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Onboarding → Status → NRA declaration information"
route_name: apps.cloudcart_pay.onboarding
route_path: /admin/payment-providers/cloudcart_pay/onboarding
aliases: ["NRA declaration information", "Electronic Store Declaration", "Appendix 33 Ordinance N-18", "Appendix №33", "MID and TID for NRA", "Virtual POS ID", "Декларация за НАП", "Приложение 33 Наредба Н-18", "Декларация за електронен магазин", "Данни за декларацията към НАП", "MID и TID за НАП", "Информация за деклариране пред НАП", "Merchant ID за Приложение 33 т. 7.3"]
tags: [paymentproviders, payment-providers, cloudcart-pay, onboarding, n18, nra, compliance, bulgaria]
plan_gates: []
created: 2026-11-03
updated: 2026-11-09
source_count: 2
---

> Part of [[payment-providers-cloudcart-pay-onboarding]]. See the hub for the other aspects (wizard flow, fields, people, documents, verification, bank, status, review and alerts).

# CloudCart Pay — NRA declaration information

## Purpose

A Bulgarian store files an Electronic Store Declaration (Appendix №33 to Ordinance Н-18) with the National Revenue Agency. This card gives the CloudCart Pay payment details for it, with a PDF to download. The card's own intro: *"Payment details for the Electronic Store Declaration (Appendix №33 to Ordinance Н-18) that you file with the National Revenue Agency. CloudCart Pay does not submit the declaration — use this information when you or your accountant complete it."*

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

A row with nothing to show reads "—". With no arrangement at all the card says *"No payment arrangement was found for your account yet."*

### Which point of Appendix №33 each row fills

Point 7 of Appendix №33 (Article 52р of the ordinance):

| Appendix №33 | Card row |
|---|---|
| 7.1 payment methods | **Currency and payment methods** |
| 7.2 payment service providers with a virtual POS contract | **Payment service provider** |
| 7.3 merchant's unique ID at the provider (Merchant ID) | **Merchant ID (MID)** |
| 7.4 accounts that receive the payments | **Receiving bank account** |
| 7.6 or 7.7 virtual POS number | **Virtual POS ID (TID)**: 7.6 when **Settlement** reads *Directly to the merchant*, 7.7 when it reads *Through the payment service provider* (verify) |

The Merchant ID for point 7.3 is the card's **Merchant ID (MID)**, not the connected account's ID (**Connected Account ID** in onboarding step 1, **Connected Account** on the Settings tab). That ID is the CloudCart Pay account's own reference; the MID is the merchant's ID at the payment service provider and can still be missing while the account ID exists. The card gives only the payment part: the rest of the declaration, including point 4 (platform or own e-shop), is completed by the merchant or their accountant.

## Business rules

### When the information is available

Before the account can take payments, the card reads *"The information becomes available once your account can accept payments."* Without data for the account: *"No declaration information is available for your account yet."*

### Preparing a copy

The first visit prepares the first copy on its own. **Update information** prepares a new one. It usually takes about a second, and the page waits up to two minutes (*"Preparing the information…"*). Each copy is fixed at the moment it was prepared, and the card shows the latest. CloudCart stores none of this; the card reads it from CloudCart Pay each time.

### Missing or unverified details

The warning block *"Some information is missing or not yet verified"* lists what is wrong. The full set of messages:

| Message | What it concerns |
|---|---|
| *"The merchant ID (MID) is not available yet."* / *"The virtual POS ID (TID) is not available yet."* | The IDs for points 7.3 and 7.6/7.7. |
| *"The accepted agreement could not be found."* | The agreement ([[ccpay-onboarding-verification-attestation]]). |
| *"The contracted payment service provider could not be determined. Contact our support team."* | Why **Payment service provider** can read "—". |
| *"Some details of the contracting parties are missing. Contact our support team."* | Missing provider details, e.g. the registration number. |
| *"Some details could not be confirmed. Contact our support team."* | Unconfirmed details. |
| *"A reference from the card acquirer is missing. Contact our support team."* | A reference the arrangement needs from the card acquirer. |
| *"One of your payment arrangements is not covered. Request its details from that provider."* | Another provider's arrangement: its details come from that provider. |
| *"Your payout settings could not be confirmed. …"* / *"The bank account for payouts could not be found. …"* / *"… could not be determined. …"* / *"Some bank account details are missing. …"* | The receiving account: check it in the Bank Account step ([[ccpay-onboarding-bank-account]]) or contact support. |
| *"The details of your bank account type cannot be included. Add them to the declaration yourself."* | An account type the card cannot show. |
| *"The currency of your bank account could not be confirmed. Check that it accepts payouts in your store currency."* | The account's currency. |

An unknown problem shows *"Unrecognized issue: {code}"*. The block ends with *"You can still download the document and complete the rest of the declaration yourself."* Several problems need CloudCart's support team, not a setting. Once a detail is corrected, **Update information** prepares a copy with it.

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

- Bulgarian labels of the card and of **Update information** (production translation table).
- The provider's legal name and registration number come from CloudCart Pay per account; no fixed value is held in the code.
- Which option of point 4 of Appendix №33 (online platform or own/rented e-shop) fits a CloudCart store is a legal assessment the card does not make.
