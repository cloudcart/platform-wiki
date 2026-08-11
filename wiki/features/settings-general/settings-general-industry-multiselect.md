---
type: feature
nav_path: "Settings → Store settings → Industry"
route_name: general.settings
route_path: /admin/settings/general
aliases: ["Site industry", "Niches", "Industry multi-select", "Store niche", "Бранш", "Категория на магазина"]
tags: [settings, general, industry, google-shopping, segmentation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-general]]. See the hub for related aspects (store details, locale, language, maintenance, security key, product badges, operational toggles).

# Store settings — Industry box (multi-select)

## Purpose

The Industry box exposes a single multi-select field — *"What niche is your online store?"* — that writes to `site_industry`. It stores the merchant's choice as a **JSON array of Google Product Category IDs** and feeds downstream systems that need to know what the store sells (Google Shopping integration, internal site segmentation, onboarding completion).

This is **separate** from the singular `main_industry` set by the dedicated modal documented at [[settings-general-industry]]. The two fields serve different consumers — see the contrast below.

> The right-side info panel reads: *"Choose one or more industries for your business — Select the industries that best represent your business to help categorize your store."*

## Where to find it

Sidebar → Settings → **Store settings** → Industry box.

## What the merchant can do here

- Pick one or more industries that describe the store from the dropdown of Google Product Category options.
- See currently-selected industries as removable chips.
- Add or remove industries at any time — the value updates on the next save.

## Settings & fields

| Field / Control | What it does | Notes |
|-----------------|--------------|-------|
| **What niche is your online store?** (`site_industry`) | Multi-select of industry categories. | Required — at least one industry must be selected. Options come from the backend (`meta.industries`). Multiple selections allowed. |

## Business rules

### `site_industry` vs `main_industry` — two distinct fields

The screen exposes ONLY the multi-select called "What niche is your online store?" which writes to:

- `setting('site_industry')` — array of Google Product Category IDs, validated as required.
- `site.industry` — same array, also persisted on the Site record column.

This is **separate** from another field called `site.main_industry` (singular integer FK to Google Product Category), which is set via a different onboarding-style modal — see [[settings-general-industry]]. The multi-select on this page does NOT update `main_industry`; it only updates `site_industry` / `site.industry`. The two fields serve different downstream systems:

- **`site_industry` (this multi-select)** → Google Shopping integration's product-category alignment, internal site-segmentation jobs that group merchants for cross-merchant analytics and targeted communications, and the onboarding flow's "industry answered" flag.
- **`main_industry` ([[settings-general-industry]])** → CloudCart Analytics primary categorization for the store's sales analytics and benchmark reports.

A merchant who updates one does NOT automatically update the other. If a merchant changes their store's positioning, both should be updated independently.

### `site_industry` does NOT affect the storefront

Industry is stored as a JSON array of Google Product Category IDs. Consumers:

- CloudCart's internal site-statistics jobs (sites per industry, revenue by industry) — analytics done by the CloudCart team, not visible to the merchant.
- Site segmentation used by CloudCart to target communications to groups of merchants (e.g., "all fashion stores").
- The Google Shopping integration (if installed) — uses the industry mapping to align with Google's product taxonomy.
- The CloudCart onboarding flow — tracked as an answered question.

It does **not** affect the storefront design, product attributes, page templates, or admin UI. A merchant changing industry will not see anything change in their store.

### Required, but invalid IDs are silently filtered

The modern endpoint validates that `site_industry` is `required` but does NOT enforce that each item exists in the Google Product Category table — invalid IDs are silently filtered out on save. The legacy validator was stricter (each entry must be an array). Practical effect: malformed values from API automation get dropped without an explicit error.

### Allowed-industries list comes from a shared source

The dropdown options match the `meta.industries` collection — the same flat list of Google Product Category base options used by the singular [[settings-general-industry]] modal and by Google Shopping integrations. So a category that exists here also exists there.

### Save persists to two locations

The value is written both to the main settings store (`setting('site_industry')`) and to the Site record's `industry` JSON column in the same transaction. Both copies stay in sync.

## Related

- [[settings-general]] — hub.
- [[settings-general-industry]] — the **singular** `main_industry` modal at `/admin/settings/general/industry` (distinct from this multi-select).
- [[apps-google-shopping]] — primary consumer of `site_industry` (product-category alignment).
- [[analytics]] — consumer of `main_industry`, NOT `site_industry`.

## Open questions

None.
