---
type: feature
nav_path: "Apps → Google Search Console → Settings"
route_name: apps.google_search_console.settings
route_path: /admin/apps/google_search_console/settings
aliases: ["Google Search Console Settings", "GSC settings", "GSC verification"]
tags: [apps, google, search-console, seo, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-11-09
source_count: 5
---
# Google Search Console → Settings

## Purpose

The **Settings** tab is where the merchant pastes Google's **verification meta tag** for site verification. It offers no other verification method. See [[apps-google-search-console]] for the full feature set.

## Where to find it

Sidebar → Apps → Google Search Console → **Settings tab**. Route: `/admin/apps/google_search_console/settings`.

## What the merchant can do here

### The Meta tag box

| Box / field | Notes |
|---|---|
| Box titled **Meta tag**, one text field with no label of its own | Takes the whole meta tag Google gives in its verification flow, as the placeholder shows. Validated against the `ValidHtml` rule (per [[apps-google-search-console]]). |

The Bulgarian wording of this tab and box comes from the admin's translation table and is not recorded here.

The Manager's `getMeta` returns the formatted meta tag string for injection: `<meta name="google-site-verification" content="..." />`.

### Verification methods (alternative)

The meta tag is the only method this app handles. Google also supports the following, done outside the app (a DNS TXT record goes in **Manage DNS** for a domain on CloudCart's nameservers, [[settings-domains-dns-cloudflare]]):
- HTML file upload.
- DNS TXT record.
- Google Analytics property (when GA is already verified).

The merchant typically uses meta-tag (zero DNS work).

### What the merchant CANNOT do here
- View GSC analytics data (only at search.google.com/search-console).
- Submit sitemaps directly — GSC console only.
- Get search-query reports inside CloudCart.

## Settings & fields

Per [[apps-google-search-console]] Manager:
- `getMeta` — returns the meta tag string for `<head>` injection.
- the configured check — verifies the tag content is set.

### Validation

`ValidHtml` rule (per [[apps-google-search-console]] Request) ensures the pasted text parses as HTML. Pasting only the code instead of the full meta tag is refused with *"Code must be a valid HTML"*.

## Business rules

### Tag injected on all storefront pages

Once configured + active, the platform injects the verification meta tag on every storefront page's `<head>` section. Google's crawler reads it on the next visit + confirms ownership.

### Required for many SEO actions

Without verification, the merchant can't:
- Submit sitemaps for faster indexing.
- See search Performance reports.
- View Coverage / Indexing reports in GSC.

### Permission
Standard apps permission scope.

## Related

- [[apps-google-search-console]] — hub.
- [[apps-google-connect]] — OAuth foundation (verify whether GSC uses OAuth here).
- [[marketing-seo]] — SEO landing.

## How it works (verified against backend)

### Strictly meta-tag — no OAuth in this app

The settings controller saves a single field: `meta_tag`. There is no OAuth flow, no token storage, no GSC API client in the codebase. The merchant pastes the verification meta tag from Google's UI; CloudCart injects it into every storefront page's `<head>`; Google's crawler confirms ownership on its next visit. To use any other GSC feature (sitemap submission, search analytics, coverage reports) the merchant logs into search.google.com directly.

### No auto-submission of sitemaps on catalog changes

The Search Console app does NOT trigger any "resubmit sitemap" event when products / categories change. CloudCart's sitemap is generated on demand by the platform code and reflects the live catalog (with internal caching). Google re-discovers updates via its regular crawl of the sitemap URL, or by the merchant manually re-submitting in GSC.

### GSC data inside CloudCart is not available

There is no current capability to pull queries / impressions / clicks data from GSC into CloudCart reports. The merchant gets that data only by logging into search.google.com — CloudCart's role is exclusively "host the verification tag".

### Vue UI is a single textarea — pasting the full meta tag

The Vue settings page renders a single text field with placeholder `<meta name='google-site-verification' content='XXXX_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'>`. The merchant pastes the COMPLETE meta tag string. Only the content token, on its own, does not save: it fails the HTML check (see Validation).

### "Meta tag is required" trigger

When the app is active, leaving the field empty produces *"Meta tag is required"*. Pasting non-HTML text (e.g., random letters) produces *"Code must be a valid HTML"* via the ValidHtml rule. Whitespace alone passes the HTML check but fails the required check.

### Single box, inline edit (no slide-over)

The Vue page renders ONE settings box (`box-key: google_search_console`) with `editMethod: 'inline'` — clicking Edit reveals the textarea in place. There is no slide-over panel, no modal dialog, no separate Connect/Disconnect button (no OAuth in this app). The box's title is **Meta tag**; the single field inside has no label text, and the placeholder is the meta tag example. Save is via the standard top-right save action.

## Open questions

(None currently outstanding for this page.)
