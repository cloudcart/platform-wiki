---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Onboarding → Review, approval time & alerts"
route_name: apps.cloudcart_pay.onboarding
route_path: /admin/payment-providers/cloudcart_pay/onboarding
aliases: ["CloudCart Pay approval time", "How long does CloudCart Pay approval take", "CloudCart Pay review", "Submitted waiting for review", "CloudCart Pay account alerts", "CloudCart Pay capability alert", "Колко време отнема одобрението", "Изпратено — изчаква преглед", "Известия CloudCart Pay акаунт", "Кога ще бъде одобрен акаунтът"]
tags: [paymentproviders, payment-providers, cloudcart-pay, onboarding, review, notifications]
plan_gates: []
created: 2026-10-06
updated: 2026-10-06
source_count: 3
---

> Part of [[payment-providers-cloudcart-pay-onboarding]]. See the hub for the other aspects (wizard flow, fields, people, documents, verification, bank, status, connect/disconnect).

# Onboarding — review, approval time & alerts

## Purpose

What happens after the merchant submits the account and uploads the documents: **how long approval takes**, how the screens acknowledge a document that is waiting for review, how unreviewed documents are chased, and the **alerts** the merchant receives when the account or its card-payment and payout status changes. It is the page for "when will my account be approved?", "I uploaded the document, why does it still ask?" and "what does this CloudCart Pay notification mean?".

## Where to find it

- **Status** step and **Documents** step of the Onboarding tab — Settings → Payment methods → CloudCart Pay → **Onboarding** ([[ccpay-onboarding-status-capabilities]], [[ccpay-onboarding-documents-upload]]).
- Alerts: the admin [[notifications]] and an email to the store owner.

## What the merchant can do here

- **Know how long to wait** for approval.
- **See which uploads are waiting for review** and when they were sent.
- **Replace a document** only when the one sent was wrong or unreadable.
- **Read the account alerts** and open the onboarding when an alert asks for action.

## Settings & fields

There are no settings. The texts the merchant sees:

| Where | Text |
|---|---|
| Status step, blue panel | **Submitted — waiting for review**: *"We received your documents. A compliance specialist checks them by hand, which usually takes a few business days. There is nothing else to do — uploading the same document again will not speed this up. We will email you as soon as the review changes the status of your account."* |
| Documents step, on the slot | **Submitted — waiting for review**, *"Submitted on <date> · <file>"*, **Replace document**. |
| Pending Requirements list | "(submitted on <date> — waiting for review)" next to an answered item. |

## Business rules

### How long approval takes

A new account is approved **from a few hours to 2 business days** after it is submitted. It can take **longer when the company's structure is complicated** (operator statement). Card payments can be switched on only after approval ([[cloudcart-pay-activation-gate]]).

### "Waiting for review" instead of "action needed"

The review is done by hand. Until a reviewer looks at an upload, the account would otherwise still report the item as missing, so CloudCart remembers the upload and shows it as **Submitted — waiting for review** instead of in the red **Action needed** block. Uploading the same file again does not speed anything up; **Replace document** asks for confirmation first.

The acknowledgement ends:

- when the review accepts the item — it disappears;
- when the review rejects it again with a new reason — it returns to **Action needed — items were rejected during review** with that reason;
- after **14 days** without any review result — it shows as needing action again.

### Unreviewed documents are chased

Every upload notifies CloudCart's compliance team at once. If a document answering a request is still unreviewed after **2 business days**, the team is reminded, and again every 2 business days until it is reviewed, answered again or 14 days have passed. The merchant does not need to do anything for this and receives none of these reminders.

### Account alerts

CloudCart receives the account's events (created, updated, a capability requested or changed). Each becomes an **admin notification** and an **email to the store owner**, in the admin panel's language. The message describes the account's state at that moment:

| Event | Message (EN) | Message (BG) |
|---|---|---|
| Account created | Your CloudCart Pay account has been created. Complete the onboarding to start accepting card payments. | Вашият CloudCart Pay акаунт е създаден. Завършете регистрацията, за да започнете да приемате плащания с карти. |
| Account updated | Your CloudCart Pay account was updated. Card payments: <status>. Payouts: <status>. | Вашият CloudCart Pay акаунт е обновен. Плащания с карти: <статус>. Изплащания: <статус>. |
| Something outstanding | Your CloudCart Pay account needs your attention: <n> outstanding requirement(s). Card payments: <status>. Payouts: <status>. Open CloudCart Pay onboarding to see what is missing. | Вашият CloudCart Pay акаунт изисква внимание: неизпълнени изисквания – <n>. … Отворете регистрацията в CloudCart Pay, за да видите какво липсва. |
| Capability requested | CloudCart Pay: <Card payments / Payouts> has been requested and is being reviewed. | CloudCart Pay: заявена е услугата „<…>“ и тя се преглежда. |
| Capability changed | CloudCart Pay: <Card payments / Payouts> is now <status>. | CloudCart Pay: услугата „<…>“ вече е със статус: <статус>. |

Status words: **active**, **inactive**, **pending review**, **disabled**, **rejected**, **not requested** (активна, неактивна, в процес на преглед, деактивирана, отхвърлена, не е заявена). Capability names: **Card payments** (Плащания с карти), **Payouts** (Изплащания).

- The alert is green when card payments and payouts are both active, a warning when something is outstanding or a capability became inactive, disabled or rejected, and informational otherwise.
- There is one alert for the account and one per capability; each is replaced by the newest. A message identical to the one already shown is not sent again, so routine edits during onboarding do not flood the inbox.

Notices about a broken configuration ("CloudCart Pay is deactivated") are separate and appear only in the admin notifications — see [[cloudcart-pay-activation-gate]].

## Related

- [[payment-providers-cloudcart-pay-onboarding]] — hub.
- [[ccpay-onboarding-status-capabilities]] — the Status step.
- [[ccpay-onboarding-documents-upload]] — uploading and replacing documents.
- [[ccpay-onboarding-verification-attestation]] — the last step before approval.
- [[cloudcart-pay-activation-gate]] — switching the method on after approval.
- [[notifications]] — the admin notifications inbox.

## Open questions

- The screen's own text says the manual check "usually takes a few business days", while the operator states a few hours to 2 business days for approval.
