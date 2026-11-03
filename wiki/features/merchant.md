---
type: feature
nav_path: "Merchant"
route_name: merchant
route_path: /admin/merchant
aliases: ["Merchant profile", "Account holder", "Billing contact"]
tags: [base, merchant, owner-only]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 1
---
# Merchant

## Purpose

The **Merchant** screen shows the personal contact details and invoicing identity of the human person who owns the CloudCart account — first name, last name, email, phone, country, language — alongside the invoicing entity (company name, VAT ID, etc.) and the current default payment method tied to the account for monthly platform billing. It is distinct from [[settings-staff]] (per-store admin users), distinct from [[settings-general]] (store-wide settings), and distinct from [[account]] (the currently-signed-in admin's profile). The Merchant record is the CloudCart-platform-level identity that owns one or more stores.

## Where to find it

Merchant (top-right profile / account area). URL: `/admin/merchant`.

## What the merchant can do here

- Edit the account holder's first name, last name, email, phone, country, and preferred admin-panel language.
- Review the invoicing identity (the legal entity CloudCart bills monthly).
- See the default stored payment method and whether the invoicing record is flagged invalid.

## Settings & fields

| Field | What it does | Notes |
|-------|--------------|-------|
| First name | Account holder's given name. | Plain text. |
| Last name | Account holder's family name. | Plain text. |
| Email | Account holder's primary contact email. | Used for billing receipts and platform notices. |
| Phone | Account holder's contact number. | Plain text. |
| Country | Account holder's country. | ISO country code; affects available payment methods. |
| Language | Preferred admin-panel UI language. | Drop-down of supported locales. |

## Business rules

### Owner-only — moderators have no access

**Only the store owner can view or edit the Merchant record.** Staff/moderators — regardless of their [[settings-staff]] permissions — are blocked (they get a "forbidden" response) and the Merchant entry is hidden from their account area. This gate is binary and **cannot be delegated** through the [[settings-staff]] permission tree (there is no permission row for it): owner vs everyone else.

### The Merchant is the platform-level account, not a store admin

A CloudCart Merchant can own multiple stores. Editing the Merchant updates the account that owns the **current** store, and the change propagates to monthly billing receipts and to platform-level (account) communications. This is distinct from [[settings-staff]] (per-store admin users), [[settings-general]] (store-wide settings), and [[account]] (the signed-in admin's own profile).

## Related

- [[account]] — the signed-in admin's own profile (a moderator's profile is not the account owner).
- [[settings-staff]] — per-store admin users & permissions.
- [[settings-general]] — store-wide settings.
- [[account-plan]] — the subscription plan billed to this merchant account.
- [[details-billing]] — billing transactions for the account.
- [[contracts]] — long-term-agreement surface for accounts on a negotiated contract.

## Open questions

_None._
