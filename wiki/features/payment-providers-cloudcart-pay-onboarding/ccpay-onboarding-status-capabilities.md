---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Onboarding → Status"
route_name: apps.cloudcart_pay.onboarding
route_path: /admin/payment-providers/cloudcart_pay/onboarding
aliases: ["CloudCart Pay status dashboard", "CloudCart Pay account status", "Action needed items were rejected", "Pending Requirements", "Pending Verification", "Compliance Tasks", "Capability active provider finalizing", "Статус на акаунта", "Необходимо е действие", "Чакащи изисквания", "Задачи за съответствие", "Обнови статуса"]
tags: [paymentproviders, payment-providers, cloudcart-pay, onboarding, status, capabilities, compliance]
plan_gates: []
created: 2026-06-10
updated: 2026-10-06
source_count: 3
---

> Part of [[payment-providers-cloudcart-pay-onboarding]]. See the hub for the other aspects (wizard flow, fields, people, documents, verification, bank, review and alerts, connect/disconnect).

# Onboarding — Status (step 7)

## Purpose

Step 7, **Account Status**, is the account's dashboard. It shows whether **card payments** and **payouts** are active, what the compliance team rejected and why, what has been sent and is waiting for review, what is still missing, and any compliance tasks. It is the page for "is my account approved?", "what is missing?" and "what does this red item mean?".

Approval takes from a few hours to 2 business days after submission, longer for a complicated company structure (operator statement). See [[ccpay-onboarding-review-alerts]].

## Where to find it

Settings → Payment methods → CloudCart Pay → **Onboarding** tab → step 7, **Status** (Статус); screen title **Account Status** (Статус на акаунта). It can be opened at any time from the step indicator.

## What the merchant can do here

- **Read the Payments and Payouts status.**
- **Fix rejected items** with **Resolve** (Коригирай), which opens the right step.
- **See what is waiting for review** and replace a document if it was wrong.
- **Open the step for a missing item** from its link.
- **Refresh Status** (Обнови статуса) without reloading the page.

## Settings & fields

Read-only. The blocks, top to bottom (each appears only when it has content):

| Block | What it shows |
|---|---|
| **Some people are still missing from your account** | The roles the review still expects, e.g. beneficial owners holding 25% or more, with **Add or edit people**. |
| **Action needed — items were rejected during review** | *"Our compliance team could not verify the items below. Please correct them or upload a new document, then submit again."* Each item: whose it is (**Company**, a person's name, or **Required document**), what it is, the reason, and **Resolve**. |
| **Submitted — waiting for review** | Items already answered, each with *"Submitted on <date> · <file>"* and **Replace document**. Text in [[ccpay-onboarding-review-alerts]]. |
| **Payments** / **Payouts** cards | A badge **Active**, **Pending** or **Inactive**, and **Enabled** or **Disabled**. |
| **Pending Requirements** (Чакащи изисквания) | What is still needed, in plain words (e.g. "Business website", "Proof of residence"), each linking to its step; answered ones add "(submitted on <date> — waiting for review)". |
| **Pending Verification** (Чакаща верификация) | What is being checked; nothing to do. |
| **Compliance Tasks** (Задачи за съответствие) | Cards with a title, a **Blocking** (Блокиращо) badge when it blocks the account, a status badge such as **Action Required**, what is needed, "Affects: Card payments, Payouts", and **Resolve**. With none: *"No outstanding compliance tasks."* |

Buttons: **Back** (Назад) and **Refresh Status** (shows **Refreshing…** while it works).

## Business rules

### Payments and Payouts cards

- **Payments** reads **Enabled** when card payments are active on the account. When the card-payment capability is active but final activation is still being completed, it adds *"Capability active — provider finalizing"* (Възможността е активна — доставчикът финализира). Only an enabled **Payments** card lets the method be switched on ([[cloudcart-pay-activation-gate]]).
- **Payouts** reads **Enabled** when payouts are active; *"Payouts capability not requested"* when the account never asked for payouts. The [[payment-providers-cloudcart-pay-payouts|Payouts tab]] uses the same rule, so both always agree.
- Badge: **Active** = in use; **Pending** = under review; **Inactive** = not enabled.

### Rejected items

Each rejection carries the reviewer's reason when one was written; otherwise a standard sentence, for example:

- *"The document is not readable. Please upload a clearer copy."*
- *"The document has expired. Please upload a valid one."*
- *"A photocopy is not accepted. Please upload the original document."*
- *"The back side of the document is missing. Please upload it."*
- *"The name on the document does not match the details provided."*
- *"Additional information was requested by our compliance team."*

**Resolve** opens the step where it is fixed: business details → step 2, people → step 3, documents → step 4, agreements → step 5, bank account → step 6. After an upload the item moves from the red block to **Submitted — waiting for review**.

### Compliance tasks

- A task with agreement documents says *"Agreement documents are reviewed and accepted in the Identity Verification step."*, lists the documents and has **Resolve** to step 5 ([[ccpay-onboarding-verification-attestation]]).
- Other tasks list what they need, with ✓ for what is done.
- Optional tasks (not required yet) are hidden, so an approved account does not show reminders it does not owe.
- Known titles: **Activate card payments** (*"Submit your account details so card payments can be reviewed and activated."*), **Activate payouts**, **Three-party agreement**.

### The step indicator turns red

While anything is outstanding — requirements, items being verified, rejections or a required task — the **Status** step in the indicator is red.

### Refresh

**Refresh Status** reads the account, the review markers and the compliance tasks again. Changes made by the review also arrive as an admin notification and an email ([[ccpay-onboarding-review-alerts]]).

### When step 7 counts as done

When the account is submitted and nothing is outstanding, or when card payments and payouts are both enabled.

## Related

- [[payment-providers-cloudcart-pay-onboarding]] — hub.
- [[ccpay-onboarding-review-alerts]] — approval time, waiting for review, alerts.
- [[ccpay-onboarding-documents-upload]] — uploading and replacing documents.
- [[ccpay-onboarding-people-roles]] — adding missing people.
- [[ccpay-onboarding-verification-attestation]] — agreements.
- [[cloudcart-pay-activation-gate]] — switching the method on.
- [[payment-providers-cloudcart-pay-payouts]] — the Payouts tab.

## Open questions

- Bulgarian wording of the task status badges (e.g. **Action Required**), which the operator's list also shows in English.
