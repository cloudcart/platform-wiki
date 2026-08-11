---
type: feature
nav_path: "Marketing → Seo → 301 Redirects"
route_name: seo-301-redirects
route_path: /admin/marketing-new/seo/301-redirects
aliases: ["301 Redirects", "URL redirects", "Per-URL redirects", "SEO redirects", "301 пренасочвания", "Пренасочвания", "URL пренасочвания"]
tags: [marketing, seo, redirects, migration, url-management]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 10
---

# 301 Redirects (per-URL redirects manager)

## Purpose

This screen is where the merchant creates and manages **permanent (HTTP 301) redirects from old URLs to new URLs**. Each row tells the storefront: "if a customer or search engine hits this old URL, send them to this new destination with a 301 response." Common uses:

1. **Migration** — moving to CloudCart from another platform and preserving SEO from old URLs (`/old-shop/product-123` → the matching CloudCart product).
2. **Restructuring** — a renamed category or product (slug changed) keeps its old URL working.
3. **Removed pages** — a deleted product redirects to a related category or replacement instead of returning a 404 to Google.

This is **per-URL**, not domain-wide. To redirect an entire OLD DOMAIN to the current store (e.g., `oldbrand.com` → `newbrand.com`) use the separate [[apps-domain-redirect]] app — that operates at the host layer, this operates at the URL/path layer.

The platform also auto-creates 301 redirects in some cases (renaming a product slug, importing from CSV) — those rows appear here automatically alongside merchant-created ones. See [[seo-301-redirects-auto-tracking]].

## Where to find it

Sidebar → Marketing → SEO → **301 redirects**. Route name `seo-301-redirects`, path `/admin/marketing-new/seo/301-redirects`. Page title "301 Redirects", breadcrumb "Marketing → 301 Redirects".

## What the merchant can do here

- See a paginated table of all configured 301 redirects, sorted newest first (`id desc`).
- Filter by **Type** (Manual / External / Product / Category / Vendor / Blog / Article / Page / Section) — see [[seo-301-redirects-types]] for the type enum.
- Search across **Old URL**, **New URL**, and the **name / URL handle of the linked entity**.
- Click **Add redirect** to prepend a blank inline row, fill in old URL + type + destination, click Create.
- Edit any existing row inline — the "New URL" field changes shape based on the selected type.
- Cancel an in-progress edit (reverts the row) or delete a saved row.
- **Bulk delete** selected rows.
- **Import redirects from CSV** via a three-step wizard — see [[seo-301-redirects-csv-import]].

### What the merchant CANNOT do here

- Use 302 (temporary) redirects — every redirect is always 301.
- Use regex; only literal `*` is supported as a wildcard. See [[seo-301-redirects-wildcards]].
- Redirect from an external domain (use [[apps-domain-redirect]]).
- Sort the table by any column other than the default `id desc`.
- Edit the URL of the linked entity from this screen — the merchant changes URL slugs on the entity's own page; the redirect follows automatically (it references the entity, not a frozen URL).
- Redirect physical files (`.pdf`, `.jpg`) — they bypass the redirect layer entirely. See [[seo-301-redirects-middleware]].

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[seo-301-redirects-types]] — the 9 redirect types (`manual`, `external`, `section`, `product`, `category`, `vendor`, `blog`, `article`, `page`); per-type "New URL" field shape; entity-typed rules follow the entity's current URL.
- [[seo-301-redirects-validation]] — Create/Update validation rules, error messages and precedence, same-URL silent skip.
- [[seo-301-redirects-csv-import]] — the 3-step CSV-import wizard (upload → map columns → submit); auto-typing as `external` / `manual`; idempotent re-import.
- [[seo-301-redirects-middleware]] — how the storefront applies redirects; the 4 skip conditions; `has_301_redirects` short-circuit; 24-hour per-URL cache and its invalidation.
- [[seo-301-redirects-wildcards]] — literal `*` wildcard matching; the 7 named prefixes (`product`, `category`, `vendor`, `blog`, `article`, `page`, `selection`); URL parsing (fragment stripped, query kept); trailing-slash variant.
- [[seo-301-redirects-marketing-passthrough]] — the 10 tracking params preserved on redirect (`fbclid`, `gclid`, `gclsrc`, `msclkid`, `utm`, `utm_source`, `utm_medium`, `utm_campaign`, `dclid`, `zanpid`); `utm_term` and `utm_content` NOT preserved.
- [[seo-301-redirects-auto-tracking]] — 30-day auto-redirect on rename; entity-delete cascade (deleting a product/category/vendor/page/blog/article clears its rules); manual / external / section rules never auto-deleted.

## Settings & fields

### Table layout

| Column | What it shows | Editable inline | Notes |
|--------|---------------|-----------------|-------|
| **Old url address** | The path/URL the storefront should match. | Yes (text input). | URL-decoded on save. Wildcards on [[seo-301-redirects-wildcards]]. |
| **Redirect type** | Dropdown — see [[seo-301-redirects-types]]. | Yes (select). | Switching the type changes the "New url address" field. |
| **New url address** | Destination — input or picker depending on Type. | Yes (input / entity picker / section dropdown). | Stored differently per type — see [[seo-301-redirects-types]]. |
| **(Row actions)** | Cancel / Save (or Create) + Delete. | — | Save stays disabled until old or new URL changes from the row's saved value. |

Above the table: a **Type** filter (lists only redirects of that type) and a **Search** box (matches Old URL, New URL, and the name/slug of the linked Product / Category / Vendor / Blog / Article / Page).

The exhaustive per-field validation table lives on [[seo-301-redirects-validation]]. The CSV-import field-mapping wizard lives on [[seo-301-redirects-csv-import]].

## Business rules

The full catalogue lives on the aspect pages. The most-impactful rules at a glance:

- **Every redirect is 301 (permanent)** — no 302 option, by design.
- **Redirects are skipped entirely when the store has none** (`has_301_redirects = false`); results are cached per URL for 24 hours and cleared on any add/edit/delete. A CDN in front of the store may still serve a stale 301 for longer. See [[seo-301-redirects-middleware]].
- **Old URL is unique store-wide** — a duplicate save returns *"Old URL is already exist"*. See [[seo-301-redirects-validation]].
- **Wildcards via literal `*`**; the 7 named prefixes get a fast path. See [[seo-301-redirects-wildcards]].
- **Entity-typed redirects follow the entity's CURRENT URL** — rename adapts automatically. See [[seo-301-redirects-types]].
- **Auto-tracking expires after 30 days; deleting an entity removes its rules**. See [[seo-301-redirects-auto-tracking]].
- **Permission** — requires the `marketing.seo` permission; there is no read-only role. CSV import is separately permissioned and may require 2FA. See [[seo-301-redirects-csv-import]].
- **Plan gates** — none on this screen.

## Related

- [[marketing]] — parent navigation hub.
- [[marketing-seo]] — Main SEO settings (canonical, robots.txt, sitemap, OG image, RSS).
- [[marketing-seo-meta]] — per-section meta titles & descriptions.
- [[apps-domain-redirect]] — whole-domain 301 forwarding (different mechanism: host-layer instead of URL-layer).
- [[apps-domain-redirect-settings]] — Domain Redirect configuration screen.
- [[apps-seo-spinner]] — AI content variation generator for products / categories / meta tags.
- [[seo-redirect]] — the SEO Redirect entity hub (data-model view of these rules).
- [[api-redirects]] — JSON-API v2 endpoint for programmatic management of redirect rules.
- [[product]] — renaming a product slug here auto-tracks the old URL for 30 days (no manual redirect row needed for that window).
- [[category]] — same auto-tracking on rename.
- [[marketing-landing-pages]] — CMS Pages; same auto-tracking on rename.
- [[settings-domains]] — primary domain determines the host used for redirect target Location header.
- [[settings-queue-view]] — the CSV-import background job runs on the `import` queue and is visible there.
- [[background-queue-inventory]] — catalogue of all background processes; covers the async redirects-CSV import job and how to check whether it finished.
- [[json-api-v2]] — authentication, rate limits, side-effects principle that applies to programmatic redirect writes.

## Open questions

- ⏸️ **30-day TTL on URL-handle-history.** Auto-tracked old slugs expire 30 days after the slug change. After the TTL, the redirect stops working unless the merchant has explicitly added a permanent redirect entry on this page. See [[seo-301-redirects-auto-tracking]].
