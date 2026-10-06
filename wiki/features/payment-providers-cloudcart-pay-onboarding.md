---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Onboarding"
route_name: apps.cloudcart_pay.onboarding
route_path: /admin/payment-providers/cloudcart_pay/onboarding
aliases: ["CloudCart Pay onboarding", "Connect account", "Connected account", "KYB", "KYC", "CloudCart Connect", "Identity verification", "Регистрация CloudCart Pay", "Онбординг CloudCart Pay", "Свържи акаунт", "Колко време отнема одобрението"]
tags: [paymentproviders, payment-providers, cloudcart-pay, onboarding, kyb]
plan_gates: []
created: 2026-05-21
updated: 2026-10-06
source_count: 3
---

# CloudCart Pay — Onboarding

## Purpose

The **Onboarding** tab (Регистрация / Онбординг) is a **7-step wizard** that registers and verifies the merchant's business so CloudCart Pay can take card payments for it. It creates the merchant's **connected account**, collects the company details, every person who owns or manages the company, their documents, the agreements and the payout bank account, and sends the account for review. Until the account is approved, the CloudCart Pay method cannot be switched on at checkout ([[cloudcart-pay-activation-gate]]).

**How long approval takes.** A new account is approved from a few hours to 2 business days after it is submitted. It can take longer when the company's structure is complicated (operator statement). What the merchant sees while waiting is on [[ccpay-onboarding-review-alerts]].

The wizard reads the account live each time it opens, so a merchant who leaves halfway continues where they stopped. After approval the same tab stays the account's dashboard: status, requests from the compliance team, and **Disconnect**.

## Where to find it

Settings → Payment methods → CloudCart Pay → **Onboarding** tab. Address: `/admin/payment-providers/cloudcart_pay/onboarding`; adding `?step=1` … `?step=7` opens a given step.

The seven steps, with the labels in the step indicator and the screen titles (Bulgarian from the operator's field list):

| # | Step | Screen title | Aspect page |
|---|---|---|---|
| 1 | Profile (Профил) | Account Setup (Настройка на акаунт) | [[ccpay-onboarding-account-business-fields]] |
| 2 | Business (Бизнес) | Business Information (Бизнес информация) | [[ccpay-onboarding-account-business-fields]] |
| 3 | Representative (Представител) | Representative (Представител) | [[ccpay-onboarding-people-roles]] |
| 4 | Documents (Документи) | Documents (Документи) | [[ccpay-onboarding-documents-upload]] |
| 5 | Verification (Верификация) | Agreements & Identity Verification (Споразумения и верификация на самоличността) | [[ccpay-onboarding-verification-attestation]] |
| 6 | Bank (Банка) | Bank Account (Банкова сметка) | [[ccpay-onboarding-bank-account]] |
| 7 | Status (Статус) | Account Status (Статус на акаунта) | [[ccpay-onboarding-status-capabilities]] |

## Sub-pages (in this cluster)

- [[ccpay-onboarding-wizard-flow]] — the step indicator, resuming, opening a step directly, when a step counts as done, staff access.
- [[ccpay-onboarding-account-business-fields]] — steps 1 and 2: country, business type, email; trading name, website, category, legal entity, registered address.
- [[ccpay-onboarding-people-roles]] — step 3: the legal representative, beneficial owners and managers, roles and ownership share.
- [[ccpay-onboarding-documents-upload]] — step 4: the document checklist per country and per person, extra documents requested by compliance, submitting the account for review.
- [[ccpay-onboarding-verification-attestation]] — step 5: the agreements and the representative's identity verification.
- [[ccpay-onboarding-bank-account]] — step 6: the payout IBAN.
- [[ccpay-onboarding-status-capabilities]] — step 7: Payments and Payouts status, rejected items, pending requirements, compliance tasks.
- [[ccpay-onboarding-review-alerts]] — approval time, "waiting for review", reminders to the review team, account alerts by notification and email.
- [[ccpay-onboarding-connect-disconnect]] — Connect Existing Account, Disconnect, an account that cannot be loaded, changing country.

## What the merchant can do here

- **Start onboarding** or **link an existing account** — [[ccpay-onboarding-connect-disconnect]].
- **Fill in the company** — [[ccpay-onboarding-account-business-fields]].
- **Add every person** the review needs — [[ccpay-onboarding-people-roles]].
- **Upload the documents and submit the account for review** — [[ccpay-onboarding-documents-upload]].
- **Accept the agreements and send the identity verification link** — [[ccpay-onboarding-verification-attestation]].
- **Add the payout IBAN** — [[ccpay-onboarding-bank-account]].
- **Follow the account status and answer requests** — [[ccpay-onboarding-status-capabilities]].

## Settings & fields

The hub has no fields of its own; each step's fields are on its aspect page (see the table above).

## Business rules

- **Order of work.** Business details, people and documents come first; the account is submitted for review from the **Documents** step. Only then do the agreements appear in step 5 and identity verification become possible.
- **Approval** takes from a few hours to 2 business days after submission, longer for a complicated company structure (operator statement). Card payments can be switched on only after approval.
- **Documents wait for a human review.** After an upload the item shows **Submitted — waiting for review**; uploading the same document again does not speed it up. See [[ccpay-onboarding-review-alerts]].
- **Alerts.** Changes to the account arrive as admin notifications and as an email to the owner — [[ccpay-onboarding-review-alerts]].
- **Country and business type cannot change** after the account is created — [[ccpay-onboarding-connect-disconnect]].
- **People cannot be removed** in the wizard, only added and edited — [[ccpay-onboarding-people-roles]].
- **Disconnect** keeps the account but switches the payment method off — [[ccpay-onboarding-connect-disconnect]].
- **Staff access** needs the permission for the store's payment methods settings — [[ccpay-onboarding-wizard-flow]].

## Related

- [[payment-providers-cloudcart-pay]] — CloudCart Pay hub.
- [[cloudcart-pay-activation-gate]] — why the method can be switched on only after approval.
- [[cloudcart-pay-merchant-terms]] — the agreement accepted in step 5.
- [[payment-providers-cloudcart-pay-settings]] — the Settings tab, which shows the connected account.
- [[payment-providers-cloudcart-pay-transactions]] — available once the account exists.
- [[payment-providers-cloudcart-pay-payouts]] — payout bank accounts after onboarding.
- [[settings-staff]] — staff permissions.
- [[notifications]] — where account alerts appear.

## Open questions

(none)
