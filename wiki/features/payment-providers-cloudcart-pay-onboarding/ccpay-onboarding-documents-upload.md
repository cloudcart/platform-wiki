---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Onboarding → Documents"
route_name: apps.cloudcart_pay.onboarding
route_path: /admin/payment-providers/cloudcart_pay/onboarding
aliases: ["CloudCart Pay documents upload", "KYC documents CloudCart Pay", "Which documents CloudCart Pay", "Bank statement CloudCart Pay", "Proof of residence", "Submit account for review", "Документи CloudCart Pay", "Банково извлечение на Юридическото лице", "Документ за местоживеене", "Изпращане на акаунта за преглед"]
tags: [paymentproviders, payment-providers, cloudcart-pay, onboarding, documents, uploads]
plan_gates: []
created: 2026-06-10
updated: 2026-10-06
source_count: 3
---

> Part of [[payment-providers-cloudcart-pay-onboarding]]. See the hub for the other aspects (wizard flow, fields, people, verification, bank, status, review and alerts, connect/disconnect).

# Onboarding — Documents (step 4)

## Purpose

Step 4 collects the documents the review needs — one set for the company and one set **for every person** added in step 3 — plus anything extra the compliance team asks for. It is also where the merchant **submits the account for review**. This is the page for "which documents do I need?" and "I uploaded it, why does it still ask?".

## Where to find it

Settings → Payment methods → CloudCart Pay → **Onboarding** tab → step 4, **Documents** (Документи). Intro: *"Upload identity and business verification documents as required."*

## What the merchant can do here

- **See the documents already on file** and open each one.
- **Upload the company's documents** and **each person's documents**.
- **Answer extra document requests** from the compliance team.
- **Replace** a document that is already waiting for review, after a confirmation.
- **Submit the account for review** (Изпращане на акаунта за преглед).

## Settings & fields

### Documents on file (Налични документи)

Each uploaded file with its upload date, name (opens in a new tab), type (**Identity document**, **Business document** or **Additional verification**) and size. The newest three are shown; **Show all** / **Show less** toggles the rest. Note: *"Upload a new file below and click Continue to add/replace."*

### Company documents (Документи на дружеството)

| Document | Required | Description on screen |
|---|---|---|
| **Legal entity bank statement** (Банково извлечение на Юридическото лице) | Yes | *"Банково извлечение - не по-старо от 3 месеца, с ясно видим титуляр и IBAN - необходимо за изплащане на сумите"* (no older than 3 months, account holder and IBAN clearly visible). |

Extra company documents by country:

| Country | Extra documents |
|---|---|
| Bulgaria | none |
| Romania | **Certificat constatator** — *"Company registration certificate issued by the Trade Register."* |
| Greece | **Company extract** (official registration extract), **Memorandum of association**, **UBO document** (identifies the ultimate beneficial owners). |

### One card per person

Above the cards: *"Please attach the required documents for each ultimate beneficial owner (UBO) holding more than 25% ownership of the company, and for every manager added in the Representative step."* Each card shows the person's name and roles and a counter such as "1 / 2".

| Document | Required | Description on screen |
|---|---|---|
| **Identity document** (Документ за самоличност) | Yes | *"Копие на валиден документ за самоличност - лична карта (предна и задна страна) или паспорт"* (ID card front and back, or passport). |
| **Proof of residence** (Документ за местоживеене) | Yes | *"Сметка за комунални услуги, банково извлечение или друг официален документ, показващ адреса на местоживеене на лицето, не по-стар от 3 месеца"* (no older than 3 months). |

Below: *"Missing someone? Beneficial owners and managers are added in the Representative step."* with **Add or edit people** (Добавяне или редактиране на лица).

### Additional documents requested by our compliance team

(Допълнителни документи, изискани от нашия екип за съответствие.) One upload slot for each document the reviewer asked for that the checklist does not already cover — for example **Proof of current address**, **Company licence** or **Proof of company registration** (Удостоверение за актуално състояние). The reviewer's own explanation, which names the person a document is about, is shown above the slot.

### Files

PDF, PNG, JPG or JPEG, up to **10 MB**. A picked file shows **Ready to upload**; after upload, **Uploaded**.

## Business rules

### Submitting the account

The footer button reads **Submit account for review** until the account has been submitted, then **Continue**. Clicking it uploads the files picked this time, attaches each one to the company or to its person, and — if not done yet — submits the account for review. The acceptance is recorded with the date, the IP address and the browser on CloudCart's side. Then the wizard moves to step 5, where the agreements appear.

If information is still missing: *"The account still has missing required information. Review the highlighted requirements and complete the previous steps, then submit again."* Clicking without picking new files uploads nothing again.

Note on the screen before submission: *"When your documents are ready, submit the account for review. Once review starts, you will accept the agreements and verify the representative's identity in the next step."*

### Submitted — waiting for review

Once a document answers something the review asked for, its slot shows **Submitted — waiting for review** (*"Submitted on <date> · <file>"*) instead of an upload box. The review is done by a person; uploading the same document again does not speed it up. See [[ccpay-onboarding-review-alerts]].

### Replace document

**Replace document** first asks: *"This document is already with our compliance team. Upload a new one only if it is a different document, for example when the one you sent was wrong or unreadable. Sending the same document again does not speed up the review."* — buttons **Upload a different document** and **Cancel**.

### Each upload reaches the review team

Every upload notifies CloudCart's compliance team at once; an upload left unreviewed is chased automatically — see [[ccpay-onboarding-review-alerts]].

### Opening a document

File names open the document inside the admin panel; the file is never handed out through a public link.

### When step 4 counts as done

When at least one document has been uploaded.

## Related

- [[payment-providers-cloudcart-pay-onboarding]] — hub.
- [[ccpay-onboarding-people-roles]] — the people whose documents are asked for.
- [[ccpay-onboarding-verification-attestation]] — step 5, after submission.
- [[ccpay-onboarding-status-capabilities]] — rejected documents and pending requirements.
- [[ccpay-onboarding-review-alerts]] — waiting for review and approval time.
- [[ccpay-onboarding-wizard-flow]] — when steps count as done.

## Open questions

- The operator's field list shows the step 4 buttons as **Добавяне или редактиране на лица**, **Назад** and **Продължете**; on screen the main button reads **Submit account for review** (Изпращане на акаунта за преглед) until the account is submitted.
- The merchant help article still names a "business registration document" for every merchant; the screen asks Bulgarian companies only for the bank statement plus each person's ID and proof of residence.
