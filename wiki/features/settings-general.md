---
type: feature
nav_path: "Settings → Store settings"
route_name: general.settings
route_path: /admin/settings/general
aliases: ["Store settings", "General settings", "Общи настройки", "Магазин"]
tags: [settings, general, store-details]
plan_gates: ["brand_removal"]
created: 2026-05-21
updated: 2026-06-10
source_count: 12
---
# Store settings

## Purpose

The store's master configuration screen. Holds the **identity** of the store (name, email, copyright, industry, footer branding), **regional defaults** (timezone, currency, language, country, units, date/time formats, customer name display), **storefront-access controls** (maintenance mode + IP whitelist, admin security key), and several **operational toggles** (order locking, automatic "New / Recommended" product badges, product image proportions, admin overlay bar).

It is the entry point most merchants visit on day one and rarely revisit — but several of its fields trigger heavy server-side work on save (storefront language change → translation rebuild + search re-index + JS regenerate; currency change → JS regenerate; admin security key rotation → all admins logged out). Knowing **which** field carries side-effects is the most-asked support topic for this screen.

## Where to find it

Sidebar → Settings → **Store settings**.

(The page's breadcrumb reads "Settings → Store settings". The route is `/admin/settings/general`.)

## What the merchant can do here

- Edit the store's identity — name, primary email (with two-code confirmation flow), footer copyright text, "Powered by CloudCart" footer toggle.
- Pick the store's industry (multi-select of niches for Google Shopping + internal segmentation).
- Set regional defaults — currency, units, language (storefront + admin separately), country of operation, customer-name display order, timezone, date/time formats.
- Put the storefront into maintenance mode and whitelist IPs that can still access it.
- Rotate the admin security key (forces all administrators to log out on next request).
- Toggle order locking so two staff members can't edit the same order at once.
- Toggle automatic "New" / "Recommended" product labels with a configurable expiry.
- Set product image proportions (original or square).
- Toggle the admin overlay bar shown on the storefront when an administrator is logged in.

## Sub-pages (in this cluster)

This feature is split into eight aspect pages, each covering one well-scoped box on the screen. The Assistant should drill into the aspect that matches the question, not read every page.

- [[settings-general-store-details]] — store name, primary email + two-code change flow, footer copyright, plan-gated "Powered by CloudCart" toggle.
- [[settings-general-industry-multiselect]] — `site_industry` JSON array (Google Shopping + internal segmentation); distinct from the singular `main_industry` modal on [[settings-general-industry]].
- [[settings-general-locale]] — date/time formats, timezone (Windows canonicalization), currency (triggers JS regenerate), unit system.
- [[settings-general-language]] — storefront language (heavy translation + search re-index side-effects), admin panel language (applies immediately), customer name display template.
- [[settings-general-maintenance]] — maintenance switch, landing-page picker, IP whitelist; storage-split caveat (lives in a separate Configuration group).
- [[settings-general-security-key]] — `sessionKeyGuard` rotation; invalidates all admin sessions; customer sessions unaffected.
- [[settings-general-product-badges]] — automatic "New" + "Recommended" badge expiry; 4-hour background sweep latency.
- [[settings-general-operational-toggles]] — order locking + lock duration; product image proportions; storefront admin overlay bar.

## Settings & fields

The page is composed of twelve labeled boxes. Each aspect page above documents the fields in one or two related boxes. A quick map:

| Box | Aspect page | Key fields |
|-----|-------------|------------|
| Store Details | [[settings-general-store-details]] | `site_email`, `site_name`, `copyright`, `show_powered_by_info` |
| Industry | [[settings-general-industry-multiselect]] | `site_industry` |
| Date and Time Formats | [[settings-general-locale]] | `date_format`, `time_format`, `timezone` |
| Currency and units | [[settings-general-locale]] | `currency`, `unit_system` |
| Language settings | [[settings-general-language]] | `language`, `language_cp`, `customer_name_display` |
| Country of operations | [[settings-general-locale]] | `operation_country` |
| Maintenance status | [[settings-general-maintenance]] | `maintenance`, `maintenance_page`, `maintenance_ip_list` |
| Security | [[settings-general-security-key]] | `sessionKeyGuard` |
| Product settings | [[settings-general-product-badges]] | `new_products_mark`, `new_products_mark_time`, `remove_feature_products`, `remove_feature_products_time` |
| Locking orders | [[settings-general-operational-toggles]] | `lock_orders`, `lock_orders_time` |
| Additional settings | [[settings-general-operational-toggles]] | `product_image_type` |
| Admin bar | [[settings-general-operational-toggles]] | `admin_bar` |

## Business rules

The screen's cross-cutting save semantics live here; field-specific rules sit on the aspect pages.

### Save splits across multiple stores

The store-settings save is **not a single write** — it fans out into three different storage locations, all wrapped in one database transaction so a failure in any one rolls the others back:

- The bulk of the fields (site name, email, copyright, industry multi-select, footer toggle, security key, product-mark switches, order-lock, admin bar, image proportions, customer name display, date/time formats) live in the **main settings store**.
- A second set lives directly on the **Site record** as columns: `language`, `language_cp`, `timezone`, `currency`, `unit_system`, `operation_country`, `manual_maintenance`, `industry` (also written as a JSON column on Site).
- The third set — maintenance landing page, allowed IPs, maintenance message — lives in a separate **Configuration group** called `maintenance` (see [[settings-general-maintenance]]).

Practical merchant-visible effect: if the merchant reports "I changed setting X but it didn't save," knowing which of the three stores holds the field can speed up support — Site-column fields show up immediately everywhere; settings-store fields wait one cache flush; the `maintenance` Configuration group is independent.

### Settings cache clears immediately on save

Every save flushes the settings cache. Changes take effect on the next read across the platform — there is no delay between saving here and the new value being used everywhere else. **Exception:** anything pre-rendered into JS data files (currency, language) or the search index (language) waits for those rebuilds to finish — see [[settings-general-language]].

### `boarding_settings` flag bumped on every save

Every successful save bumps `setting('boarding_settings')` to `1`. This flag is read by the onboarding wizard to determine whether the merchant has completed the general-settings step. So merchants going through onboarding will see this step marked complete after the first save here, regardless of which field they changed.

### Required fields

The frontend validates these as required before submit: site name, site industry (at least one), timezone, site email, language, language_cp, date format, time format, unit system, currency, operation country, customer name display. Backend re-validates on save and rejects with a per-field error if anything is blank. Field-level validation rules (max length on site name, allowed enum values on date/time format, etc.) are documented on each aspect page.

### Modern endpoint may return settings wrapped or flat

The PUT response (`/admin/api/core/settings/general`) sometimes returns `{ settings: {...} }` and sometimes returns the flat object directly. The Vue page handles both. Merchants who automate against this API (uncommon) should defensively handle both shapes.

### The email-change confirmation is skipped for platform callers

The two-code confirmation applies to the **merchant**. It is skipped — the new address applying immediately, with no codes and no pending placeholder — when the caller is CloudCart staff on a console login **or** CloudCart's own tooling acting with platform authority. So *"this cannot be changed without the codes"* is true of the merchant path only. See [[settings-general-store-details]].

## Related

- [[settings]] — parent hub.
- [[settings-general-industry]] — sibling screen at `/admin/settings/general/industry`; sets the **singular** `main_industry` used by CloudCart Analytics (distinct from the multi-select `site_industry` on this page — see [[settings-general-industry-multiselect]]).
- [[site]] — the Site record holding several of the fan-out fields.
- [[plan]] / [[plan-gates]] — the `brand_removal` feature gate (Powered-by toggle).
- [[multi-language]] / [[multi-currency]] — cross-cutting concepts the language + currency fields seed.
- [[merchant-roles]] / [[settings-staff]] — Administrator vs Moderator (relevant to order locking + security key impact).
- [[settings-translations]] — where translations live after a language change.
- [[settings-cart]] — checkout-side settings; the `order_status_for_quantity_decrease` flag pairs with several store-wide defaults.
- [[settings-admin-notifications]] — uses `site_email` as the recipient address.
- [[settings-emails]] — outgoing mailbox configuration (separate from `site_email` sender).
- [[settings-invoicing]] — uses `site_email`, `site_name`, `copyright` as invoice defaults.
- [[settings-ssl]] — SSL CSR pre-filled from `company_name`, `site_email`, `country`.
- [[settings-shipping]] — filters shipping integrations by `operation_country`.

## Open questions

None.
