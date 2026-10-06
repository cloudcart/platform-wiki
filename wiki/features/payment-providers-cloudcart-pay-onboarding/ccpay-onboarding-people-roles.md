---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Onboarding → Representative & people"
route_name: apps.cloudcart_pay.onboarding
route_path: /admin/payment-providers/cloudcart_pay/onboarding
aliases: ["CloudCart Pay representative", "Beneficial owners CloudCart Pay", "UBO CloudCart Pay", "Add manager CloudCart Pay", "Ownership share", "Legal representative", "Представител CloudCart Pay", "Действителен собственик", "Лица по акаунта", "Дял на собственост"]
tags: [paymentproviders, payment-providers, cloudcart-pay, onboarding, kyb, ubo]
plan_gates: []
created: 2026-10-06
updated: 2026-10-06
source_count: 2
---

> Part of [[payment-providers-cloudcart-pay-onboarding]]. See the hub for the other aspects (wizard flow, fields, documents, verification, bank, status, review and alerts, connect/disconnect).

# Onboarding — Representative & people (step 3)

## Purpose

Step 3 lists **every person** the review needs: the company's **legal representative**, each **beneficial owner** holding 25% or more, and any additional **manager**. For each person the merchant gives their identity, their roles in the company and their share, contact details and home address. Each person later gets their own document slots in step 4.

## Where to find it

Settings → Payment methods → CloudCart Pay → **Onboarding** tab → step 3, **Representative** (Представител).

Intro on the screen: *"Add the account representative, then add every other beneficial owner holding 25% or more of the company and any additional manager."*

## What the merchant can do here

- **Create the first person** — the form is open until one person exists.
- **Add more people** with **Add beneficial owner or manager** (Добавяне на действителен собственик или управител).
- **Edit** a person (Редактиране) or **Copy** their ID.
- **Continue** (Продължете) to the documents once at least one person exists.

## Settings & fields

**People on the account** (Лица по акаунта): one card per person with name, a **Legal representative** badge, roles and share (e.g. "Beneficial owner · 50% ownership"), ID, **Copy** and **Edit**. Under the list: *"Some fields may be locked by CloudCart once identity verification has completed. A person cannot be removed here - contact support if someone was added by mistake."*

The person form (**New person** / **Edit person**):

| Group | Field | Required | Notes / help text |
|---|---|---|---|
| Identity (Самоличност) | **First Name** (Име) | Yes | As on the person's official ID. |
| | **Last Name** (Фамилия) | Yes | As on the person's official ID. |
| | **Date of birth** (Дата на раждане) | Yes | Typed as DD/MM/YYYY. |
| | **Nationality** (Националност) | Yes | List of 30 countries. |
| | **Title / Position** (Длъжност / позиция) | Yes | Placeholder *"e.g. Manager, Legal Representative"* (напр. управител, законен представител). |
| Relationship to the company (Връзка с компанията) | **Role(s) in the company** (Роля(и) в компанията) | Yes, at least one | Checkboxes: **Legal representative**, **Beneficial owner**, **Director**, **Executive** (Законен представител, Действителен собственик, Директор, Изпълнителен директор). |
| | **Share ownership (%)** (Дял на собственост (%)) | No | 0–100, decimals allowed. |
| Contact (Контакт) | **Email** (Имейл) | Yes | For identity-verification notifications. |
| | **Phone** (Телефон) | Yes | For verification contact. |
| Home address (Домашен адрес) | **Address Line 1**, **City**, **Postal Code**, **Country** | Yes | **Country** = country of residence. |
| | **Address Line 2**, **State / Region** | No | |

Buttons: **Create person** (Създай лице) or **Save person** (Запази лицето), **Cancel** (Отказ), and at the bottom **Back** (Назад) and **Continue** (Продължете).

Role help text: *"Select every role this person holds. Select Beneficial owner for anyone owning 25% or more of the company."*

## Business rules

### One legal representative

Only one person per account can be the **Legal representative**. The first person created is pre-ticked as the representative; once one exists, the box is disabled for everyone else with *"Only one legal representative is allowed per account."* The representative is listed first and is the person who performs identity verification in step 5 ([[ccpay-onboarding-verification-attestation]]).

### Who must be added

- the legal representative;
- every **beneficial owner** owning **25% or more** of the company;
- every additional **manager**.

If the review expects people who are missing, steps 4 and 7 show *"Some people are still missing from your account"* with the roles still expected (for example "beneficial owners holding 25% or more of the company") and **Add or edit people**.

### People can be added and edited, not removed

There is no delete. A person added by mistake has to be removed through CloudCart support (the screen says so). Editing saves over the same person.

### Validation messages

- No role ticked: *"Select at least one role for this person."*
- A missing required field: *"This field is required."* with *"Please fill in all required fields before continuing."*
- Date of birth: *"Enter the date of birth as DD/MM/YYYY, for example 31/12/1985."*, *"This date does not exist. Check the day and month."*, *"The year must be between 1900 and 2010."*
- **Continue** with nobody added: *"Add at least one person before continuing."*; with an unsaved form: *"Save the person you are editing, or cancel the form, before continuing."*

### When step 3 counts as done

As soon as one person is on the account. More people can be added later; each new person gets their own document card in step 4 ([[ccpay-onboarding-documents-upload]]).

### Complex ownership takes longer

A complicated company structure can make the review take longer — see [[ccpay-onboarding-review-alerts]].

## Related

- [[payment-providers-cloudcart-pay-onboarding]] — hub.
- [[ccpay-onboarding-account-business-fields]] — steps 1 and 2.
- [[ccpay-onboarding-documents-upload]] — each person's documents.
- [[ccpay-onboarding-verification-attestation]] — the representative's identity verification.
- [[ccpay-onboarding-status-capabilities]] — rejected person details and missing people.
- [[ccpay-onboarding-review-alerts]] — review time.

## Open questions

- The operator's list marks **Date of birth**, **Nationality**, **Email** and **Phone** as required, as the screen does; the server itself accepts a person without them, so the requirement is enforced by the form only.
