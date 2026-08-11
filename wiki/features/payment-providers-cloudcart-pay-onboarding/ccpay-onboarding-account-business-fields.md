---
type: feature
nav_path: "Payment Providers → Cloudcart Pay → Onboarding → Account / Business / Representative fields"
route_name: apps.cloudcart_pay.onboarding
route_path: /admin/payment-providers/cloudcart_pay/onboarding
aliases: ["CloudCart Pay KYB fields", "Account step", "Business step", "Representative step", "Legal entity fields", "KYB business profile"]
tags: [paymentproviders, payment-providers, cloudcart-pay, onboarding, kyb]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-cloudcart-pay-onboarding]]. See the hub for the other aspects (wizard flow, documents, verification, bank, status, connect/disconnect).

# Onboarding — Account / Business / Representative fields

## Purpose

This aspect catalogues every field collected by the first three wizard steps — **Account** (step 1), **Business** (step 2), **Representative** (step 3) — the core KYB data the platform sends to Paypercut to identify the legal entity, its public profile, and the natural person who controls it.

## Where to find it

Payment Providers → CloudCart Pay → **Onboarding** tab → steps 1, 2, 3 in the stepper.

## What the merchant can do here

- Enter the country, business type and primary email that create the connected account.
- Fill in the public business profile, legal entity, registered address and customer-support contacts.
- Identify the representative person (a real human who controls the entity) — identity, contact, home address.
- Edit previously-entered data by clicking the completed step in the stepper. Country and business type are locked after creation — see [[ccpay-onboarding-connect-disconnect]].

## Settings & fields

### Step 1 — Account

Backend: `POST /admin/cloudcart-pay/account` → Paypercut `POST /v1/accounts`.

| Field | Required? | What it does | Notes |
|-------|-----------|--------------|-------|
| **Country** | Yes | Two-letter ISO country code where the business is registered. Determines available currencies and compliance rules. | Picked from a 30-country EEA+CH+GB+US-style list. **Locked after the account is created.** Pre-filled from the store's `setting('country')` for new accounts. |
| **Business Type** | Yes | `company` or `non_profit`. | **Locked after the account is created.** |
| **Email** | Yes | Primary contact email for the connected account; receives onboarding notifications. | Pre-filled from `setting('site_email')` for new accounts. RFC-validated. |

New accounts request both capabilities by default: `card_payments.requested=true` and `payouts.requested=true`. Paypercut activates each independently after KYB review (see [[ccpay-onboarding-status-capabilities]]).

### Step 2 — Business

Backend: `PUT /admin/cloudcart-pay/account` → Paypercut `POST /v1/accounts/{id}` updating `business_profile.*` and `company.*`.

Four sub-sections: **Public business profile**, **Customer support**, **Legal entity (KYB)**, **Registered company address**.

| Field | Required? | What it does | Notes |
|-------|-----------|--------------|-------|
| Business Name (Trading Name) | Yes | Public name shown to customers on invoices, receipts, statement descriptors. | Max 255 chars. |
| Website | No | Public website where the products / services are offered. | URL-validated, max 255. |
| Merchant Category Code (MCC) | No | Industry-grouped ISO 18245 MCC. The wizard renders a `<optgroup>` selector with 28 industry groups (Apparel, Automotive, Books/Media, Construction, Digital Goods, Education, …) and the underlying 4-digit code as the value. | Required for some capabilities and risk checks. Max 4 chars. |
| Product Description | No | Short description of products / services sold. | Max 500 chars. |
| Support Email | No | Customer-support email. | RFC-validated. |
| Support Phone | No | Customer-support phone. | Max 40 chars. |
| Support URL | No | Public support / contact page URL. | URL-validated, max 255. |
| Estimated Employees | No | Approximate worker count (integer ≥ 0). | |
| Support Address (line 1, line 2, city, state, postal code, country) | No | Customer-facing support address (separate from the legal-entity address). | Country is a 2-letter ISO code. |
| Legal Company Name | Yes | Official registered name as on the certificate of incorporation / commercial register. | Max 255. |
| Tax ID | Yes (unless on file) | National tax identifier (EIN, UIC, VAT, etc.). | Max 64. If the API reports `tax_id_provided` the field shows "On file — leave blank to keep current" and may be skipped. |
| Company Phone | No | Official business phone, used for verification contact. | Max 40. |
| Company Structure | No | Legal structure of the entity. | One of: `sole_proprietorship`, `single_member_llc`, `multi_member_llc`, `private_corporation`, `public_corporation`, `private_partnership`, `public_partnership`, `unincorporated_association`, `incorporated_non_profit`, `unincorporated_non_profit`. |
| Company Address (line 1, line 2, city, state, postal code, country) | No | Registered company address (separate from support address). | |

The **Save & Continue** button is disabled until Business Name, Legal Company Name, and Tax ID (or "on file") are present.

### Step 3 — Representative

Backend: `POST /admin/cloudcart-pay/persons` (create) or `POST /admin/cloudcart-pay/persons/{id}` (update) → Paypercut `POST /v1/accounts/{id}/persons` (create) OR `POST /v1/accounts/{id}/persons/{personId}` (update).

Three sub-sections: **Identity**, **Contact**, **Home address**.

| Field | Required? | What it does | Notes |
|-------|-----------|--------------|-------|
| First Name | Yes | Given name as on the rep's government-issued ID. | Max 100. |
| Last Name | Yes | Family name as on the rep's government-issued ID. | Max 100. |
| Date of Birth (day / month / year) | No | Day 1–31, month 1–12, year 1900–2010. | Sent as three integers (`dob.day`, `dob.month`, `dob.year`), not a date string. |
| Nationality | No | Country of citizenship (2-letter ISO). | |
| Title / Position | No | Job title (e.g., Director, CEO, Owner). | Max 100. Stored as `relationship.title`. |
| Email | No | Personal email for verification notifications. | RFC-validated. |
| Phone | No | Personal phone for verification contact. | Max 40. |
| Home Address (line 1, line 2, city, state, postal code, country) | No | Country is 2-letter ISO. | |

The representative is auto-flagged `relationship.representative=true`. Once verification is complete, some fields may become locked by CloudCart.

## Business rules

### Step 1 fields locked after account creation

Country and business type become disabled the moment an account exists. The Paypercut platform does not let either change after creation. To "change country" the merchant must disconnect, create a new account, and re-onboard — see [[ccpay-onboarding-connect-disconnect]].

### Step 2 completion is API-derived

The stepper marks step 2 complete only when `company.name` AND `business_profile.name` are set on the live account — not when the merchant clicks Save. The step does not flip to "complete" until both core names exist.

### Tax ID may be "on file"

If the platform reports `tax_id_provided=true`, the Tax ID input shows "On file — leave blank to keep current" and the merchant can submit step 2 without re-entering it. Entering a new value overwrites the stored one.

### Step 3 — representative replacement is edit-in-place

The wizard does NOT expose a "delete person" or "swap representative" action. There is only an **edit-in-place** flow: when a representative already exists, step 3 loads their fields and saves changes back to the same person record. A merchant whose representative needs to be replaced (original rep left the company, or failed identity verification) edits the existing person's fields through this same step rather than creating a second person. To attach a new identity document, the merchant re-uploads in step 4 — see [[ccpay-onboarding-documents-upload]].

### Step completion derived live, not stored

Each step's "complete" state is recomputed from the live Paypercut account on every load — see the rules under [[ccpay-onboarding-wizard-flow]]. A merchant who linked an existing account via *Connect Existing Account* sees steps 1, 2, 3 already marked complete if the underlying account already has the data.

## Related

- [[payment-providers-cloudcart-pay-onboarding]] — hub.
- [[ccpay-onboarding-wizard-flow]] — step indicator + resume behaviour.
- [[ccpay-onboarding-documents-upload]] — step 4, where the representative's ID document is uploaded.
- [[ccpay-onboarding-verification-attestation]] — step 5, identity verification of the representative.
- [[ccpay-onboarding-connect-disconnect]] — country / business-type lock rationale + disconnect-to-reset.

## Open questions

(none)
