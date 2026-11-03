---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Onboarding → Profile & Business"
route_name: apps.cloudcart_pay.onboarding
route_path: /admin/payment-providers/cloudcart_pay/onboarding
aliases: ["CloudCart Pay KYB fields", "Account step", "Profile step", "Business step", "Legal entity fields", "Business information CloudCart Pay", "Настройка на акаунт", "Бизнес информация", "ЕИК CloudCart Pay", "Код на категорията на търговеца"]
tags: [paymentproviders, payment-providers, cloudcart-pay, onboarding, kyb]
plan_gates: []
created: 2026-06-10
updated: 2026-10-06
source_count: 2
---

> Part of [[payment-providers-cloudcart-pay-onboarding]]. See the hub for the other aspects (wizard flow, people, documents, verification, bank, status, review and alerts, connect/disconnect).

# Onboarding — Profile & Business fields

## Purpose

Every field of the first two onboarding steps: **Profile** (screen **Account Setup**, which creates the connected account) and **Business** (screen **Business Information**: the public profile, customer support contacts, the legal entity and its registered address). Labels, required flags and help texts follow the operator's field list; the code agrees with it on every field here. The people are covered in [[ccpay-onboarding-people-roles]].

## Where to find it

Settings → Payment methods → CloudCart Pay → **Onboarding** tab → steps 1 and 2.

## What the merchant can do here

- **Create the account**: country, business type, email — **Create Account** (Създаване на акаунт).
- **Change the account email later** with **Update** (Актуализация).
- **Fill in the business**, then **Save & Continue** (Запазване и продължаване).

## Settings & fields

### Step 1 — Account Setup (Настройка на акаунт)

| Field | Required | Notes / help text |
|---|---|---|
| **Connected Account ID** (ID на свързания акаунт) | — | Read-only, once the account exists, with **Copy** and **Disconnect**. *"Account created on CloudCart. Country and business type are locked after creation. Disconnect only clears the local link — the account still exists on CloudCart."* |
| **Country** (Държава) | Yes | *"Country where the business is registered. Determines available currencies and compliance rules."* Searchable list of 30 European countries (EU members, Norway, Switzerland, United Kingdom). Pre-filled with the store's country. **Locked once the account exists.** |
| **Business Type** (Тип бизнес) | Yes | **Company** or **Non-Profit** (Нестопанска организация). *"Legal form of the entity. This cannot be changed after the account is created."* **Locked once the account exists.** |
| **Email** (Имейл) | Yes | *"Primary contact email for the connected account. Used for onboarding notifications."* Pre-filled with the store's email. |

The button stays disabled until **Country** and **Email** are filled. A new account asks for both card payments and payouts.

### Step 2 — Business Information (Бизнес информация)

**Public business profile** (Публичен бизнес профил)

| Field | Required | Notes / help text |
|---|---|---|
| **Business Name (Trading Name)** (Търговско име) | Yes | *"Public name shown to your customers on invoices, receipts, and statement descriptors."* Up to 255 characters. |
| **Website** (Уебсайт) | Yes | *"Public website where your products or services are offered."* A valid web address, up to 255 characters. |
| **Merchant Category Code (MCC)** (Код на категорията на търговеца (MCC)) | Yes | Searchable list grouped into 26 industries, each entry a four-digit code with a name, e.g. "5691 — Men's & Women's Clothing". *"Pick the category that best describes your primary business activity. Required for some capabilities and risk checks."* |
| **Estimated Employees** (Приблизителен брой служители) | No | A whole number, 0 or more. |
| **Product Description** (Описание на продукта) | Yes | *"Short description of the products or services the business sells."* Up to 500 characters. |

**Customer support** (Обслужване на клиенти) — all optional: **Support Email** (Имейл за поддръжка), **Support Phone** (Телефон за поддръжка, up to 40 characters), **Support URL** (URL за поддръжка).

**Legal entity (KYB)** (Юридическо лице (KYB))

| Field | Required | Notes / help text |
|---|---|---|
| **Legal Company Name** (Юридическо име на фирмата) | Yes | *"Official registered name as it appears on the certificate of incorporation or commercial register."* |
| **Tax ID** (ЕИК) | Yes, unless on file | *"National tax identifier (EIN, UIC, VAT, etc.) matching the legal entity."* Up to 64 characters. |
| **Company Phone** (Телефон на фирмата) | Yes | *"Official business phone used for verification and compliance contact."* |
| **Company Structure** (Структура на фирмата) | No | Sole Proprietorship (ЕТ), Single-Member LLC (ЕООД), Multi-Member LLC (ООД), Private Corporation (непублично АД), Public Corporation (публично АД), Private Partnership (СД), Public Partnership (КД), Unincorporated Association, Incorporated Non-Profit, Unincorporated Non-Profit. |

**Registered company address** (Регистриран адрес на фирмата): **Address Line 1** (required), **Address Line 2**, **City** (required), **State / Region**, **Postal Code** (required), **Country** (required).

## Business rules

### Country and business type are fixed after creation

Both lists are disabled as soon as the account exists. To register under another country or business type, the merchant disconnects and onboards a new account — see [[ccpay-onboarding-connect-disconnect]].

### Save & Continue needs every required field

The button stays disabled until all required fields of step 2 are filled. A missing field is marked *"This field is required."* with *"Please fill in all required fields before continuing."* (Моля, попълнете всички задължителни полета, преди да продължите.). Errors returned for a field appear under that field in plain words, for example *"Website must be a valid URL."*

### Tax ID can stay on file

When the account already holds a tax ID, the field shows *"On file — leave blank to keep current"* (Налично — оставете празно, за да запазите текущото) and *"Tax ID is on file"* (Данъчният номер е наличен). Leaving it blank keeps the stored one; typing a new one replaces it.

### When step 2 counts as done

When the account holds both the legal company name and the trading name. A store that links an existing account with these details sees steps 1 and 2 already done.

### Details live on the account

Everything entered here is saved to the connected account and read back live each time the tab opens; the store keeps no copy. Missing or rejected details are listed on the **Status** step with a **Resolve** button that opens step 2.

## Related

- [[payment-providers-cloudcart-pay-onboarding]] — hub.
- [[ccpay-onboarding-wizard-flow]] — moving between steps.
- [[ccpay-onboarding-people-roles]] — step 3, the people.
- [[ccpay-onboarding-connect-disconnect]] — the country and business-type lock.
- [[ccpay-onboarding-status-capabilities]] — where missing or rejected details are listed.

## Open questions

- Bulgarian label of the **Company** business type and holder type (only **Non-Profit** — Нестопанска организация — is in the translation files read).
