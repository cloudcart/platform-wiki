---
type: feature
nav_path: "Profile → Choose plan → (country / partner filtering)"
route_name: plans
route_path: /admin/plans
aliases: ["Plans country filter", "Plans issuer-company filter", "UniCredit partner catalog", "Partner-network plans", "DE Starter rebrand", "14-Tage-Test Starter", "Тарифи по държава", "UniCredit планове"]
tags: [plans, pricing, country, partner, unicredit, germany]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[plans]]. See the hub for the other aspects (catalog display, LTA override, free-plan expiry, downgrade behavior, plan-feature cache).

# Plans — country / partner filtering

## Purpose

This page documents the rules that decide **which plans show up on the `/admin/plans` catalog** for a given merchant — before any of the visual layout from [[plans-catalog-display]] runs. Filtering combines three signals: the merchant's **invoicing country (issuer company)**, whether they're on a **partner reseller network** (e.g. UniCredit), and a few country-specific catalog overrides (most notably the DE rebrand of the Start Up free plan as *14-Tage-Test (Starter)*).

The merchant doesn't see this filtering directly — they only see the resulting plan list — but it explains why two merchants in different countries see entirely different cards on the same screen.

## Where to find it

Filtering runs server-side when the catalog is loaded at `/admin/plans`. The merchant has no UI control over it; the only way to change the visible catalog is to change the merchant's invoicing entity (handled in [[details-billing]]) or to flag the site as belonging to a partner reseller (handled by CloudCart staff).

## What the merchant can do here

- Nothing directly. The catalog is automatically scoped to their country + reseller. Switching the displayed catalog requires CloudCart-staff action (re-assignment of invoicing entity / reseller flag).
- See partner-only or country-specific plans **if** their site is assigned to that catalog.

## Settings & fields

This is a backend-driven filter — no merchant-editable fields. The signals it reads are:

| Signal | Source | Effect |
|--------|--------|--------|
| **Invoicing country (issuer company)** | Set on the site record by CloudCart staff during onboarding. Configured via [[details-billing]]. | Decides which country-local plans appear in addition to global plans. |
| **Reseller flag** | Set on the site record by CloudCart staff (e.g. `reseller_id = 157` = UniCredit). | When set, replaces the entire catalog with the partner-only catalog. |
| **Country code** | Derived from the issuer company. | Drives country-specific overrides (e.g. DE Starter rebrand). |

## Business rules

### Filter decision tree

When the merchant lands on `/admin/plans`, the platform decides what to show in this order:

1. **Active LTA contract?** → Redirect to the contract's details page. The catalog is not shown. See [[plans-contract-lta-override]].
2. **Partner reseller?** (e.g. UniCredit `reseller_id = 157`) → Show partner-only plans of type `unicredit` exclusively. **Do not** include global or country-local plans of type `default`.
3. **Otherwise** → Show all global plans + plans matching the merchant's issuer-company ID. All plans must be of type `default`.

### Country / issuer-company filtering

Each plan in the catalog is either:

- **Country-specific** — set to a single issuer-company ID (BG, DE, etc.) and visible only to merchants invoiced through that entity, OR
- **Global** — no issuer-company set; visible to all non-partner merchants regardless of country.

A merchant whose store is invoiced by the DE entity sees only DE plans + global plans; a BG merchant sees BG plans + global plans. They cannot see one another's local-only plans.

Issuer-company IDs are stable internal identifiers — BG = **5** internally, DE = **7** internally. The merchant never sees these IDs, but their effect surfaces as the country-specific catalog filtering and the DE-specific free-plan branding below.

### Partner-network catalog (UniCredit and similar)

When the merchant's site is flagged with a partner reseller, the screen shows ONLY plans of type `unicredit` — a separate, partner-network-only catalog with its own pricing and feature limits negotiated through the partner.

Additionally:

- The **Choose plan** link in the profile dropdown is **hidden** for partner-network merchants. Their plan is set by the partner relationship, not picked by the merchant.
- The **Unicorn / Custom** card (Book-a-meeting flow) does still render on the catalog page itself if the merchant reaches it via direct URL.

### DE Starter rebrand — "14-Tage-Test (Starter)"

Germany's invoicing-entity merchants see the **global Start Up free plan re-labelled as *14-Tage-Test (Starter)*** and pointed at the DE Starter plan record. Effect: the free plan becomes a 14-day trial of Starter in Germany. (Other countries continue to use the same global Start Up free plan unchanged.)

This is a per-country branding override — not a separate plan. The DE-Starter expiry threshold (14 days, see [[plans-free-expiry]]) lines up with the rebrand so the trial actually expires at the trial duration.

### Plans-without-details filter happens at the query level

Plans that have **zero priced detail rows** (no monthly / yearly / etc. variant priced) are filtered out at the database query — not in display code. The merchant never sees them. This is how CloudCart soft-disables a plan: removing all price-detail variants makes it invisible end-to-end without deleting the underlying plan record. (verify)

### Currency follows issuer company

Each plan card renders prices in the currency configured for the merchant's invoicing entity. There is no per-merchant currency picker on this screen and no cross-currency comparison view. Merchants who want a different currency must request an invoicing-entity change from CloudCart staff.

## Related

- [[plans]] — hub.
- [[plans-catalog-display]] — visual layout once the filtered plans are returned.
- [[plans-contract-lta-override]] — takes precedence over country / partner filtering.
- [[plans-free-expiry]] — uses the DE vs BG country distinction for expiry thresholds.
- [[details-billing]] — where the merchant's invoicing entity is set up.
- [[expired-subscription]] — DE / BG paths differ here too.

## Open questions

(All resolved.)
