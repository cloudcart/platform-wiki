---
type: feature
nav_path: "Apps → GDPR → Policy → Seeding"
route_name: apps.gdpr.policies
route_path: /admin/apps/gdpr/policy
aliases: ["GDPR seeded policies", "Starter policies", "Default policies", "Policy install", "Policy languages", "Policy placeholders", "Privacy policy template", "Terms template"]
tags: [apps, gdpr, compliance, policy, seeding, multilang]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---
# GDPR — Policy: seeding

> Part of [[apps-gdpr-policy]]. See the hub for the other aspects (editor, form mapping, storefront rendering).

## Purpose

This aspect documents what the platform **creates automatically when the merchant installs the GDPR app** — the 4 starter policy records, the languages their text ships in, the placeholder variables substituted from the store's settings, the English fallback, and the deliberate absence of jurisdiction-specific templates. After install, the merchant manages these records like any other policy via [[apps-gdpr-policy-editor]].

## Where to find it

Seeding happens once, at GDPR app install. The resulting policies appear in the Policy list (`/admin/apps/gdpr/policy`) and, for the ones auto-attached, on the storefront forms — see [[apps-gdpr-policy-forms]].

## What the merchant can do here

- Start with 4 ready-made policies instead of an empty list.
- Edit, rename, deactivate, or delete any seeded policy afterwards (it is a normal policy record).
- Rely on the merchant's store settings being substituted into the seeded text at install.

## Settings & fields

### Install seeds 4 starter policies

When the merchant installs the GDPR app, the platform creates **4 starter policy records** with full text in the store language:

| Policy mapping | Title (EN) | Default attachment |
|---|---|---|
| `privacy-policy` | Privacy policy | Attached as **required** to `register` + `submit_payment`. |
| `marketing-policy` | Declaration of consent to the processing of personal data | Attached as **optional** to `register` + `submit_payment` + `segment_subscription_popup`; designated as THE `marketing_policy` (controls `customer.marketing` — see [[apps-gdpr-policy-forms]]). |
| `terms-policy` | Terms of conditions | Attached as **required** to `register` + `submit_payment`. |
| `cookie-policy` | Cookies Policy | Not auto-attached to forms (informational only — see [[apps-gdpr-policy-storefront]]). |

### Placeholder-variable substitution

The seeded text contains placeholder variables substituted from the merchant's store settings at install time: `{company_name}`, `{store_name}`, `{address}`, `{phone}`, `{email}`, `{mol}`, `{company_eik}`, `{domain}`, `{terms_url}`, `{policy_url}`, `{exersize_your_rights}`. The store address values come from [[apps-gdpr-address]].

## Business rules

### Seeded policies are STORE-LANGUAGE-aware, with English fallback

The seeder reads the store's `site('language')` and picks the corresponding translation. The seeded text is hard-coded to support **English, Bulgarian, Romanian, Greek, Hungarian, and Macedonian** — that's it. If the store's language is not in that set (e.g., Italian, Spanish, German, French, Serbian, Albanian), the seeder **falls back to English**. The text is GDPR-oriented and references EU regulations.

### No jurisdiction-specific presets

The autocomplete dropdown searches only the policies the merchant has CREATED (including the seeded ones — see [[apps-gdpr-policy-editor]]). It does NOT offer additional jurisdiction-specific templates: there is no "CCPA mode" or "UK GDPR" preset. A merchant operating outside the EU must adapt the seeded text manually.

### Seeded policies are ordinary records after install

Once seeded, each starter policy behaves like any merchant-created policy: it can be edited, renamed, deactivated, or hard-deleted (see [[apps-gdpr-policy-editor]]), and its form attachments can be changed (see [[apps-gdpr-policy-forms]]). Re-installing the app does not re-seed over edited records (verify).

## Related

- [[apps-gdpr-policy]] — hub.
- [[apps-gdpr-policy-editor]] — managing seeded policies after install.
- [[apps-gdpr-policy-forms]] — the default required/optional attachments + marketing designation.
- [[apps-gdpr-policy-storefront]] — the seeded Cookie Policy page rendering.
- [[apps-gdpr-address]] — store address values substituted into seeded text.

## Open questions

- Whether re-installing the GDPR app re-seeds over edited policy records or skips existing ones (verify).
