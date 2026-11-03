---
type: feature
nav_path: "Apps → Google Search Console → Settings"
route_name: apps.google_search_console.settings
route_path: /admin/apps/google_search_console/settings
aliases: ["Google Search Console Settings", "GSC settings", "GSC verification"]
tags: [apps, google, search-console, seo, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-05-28
source_count: 4
---
# Google Search Console → Settings

## Purpose

The **Settings** tab is where the merchant enters the **GSC verification code** (or completes another verification method) for site verification. See [[apps-google-search-console]] for the full feature set.

## Where to find it

Sidebar → Apps → Google Search Console → **Settings tab**. Route: `/admin/apps/google_search_console/settings`.

## What the merchant can do here

### Verification code field

| Field | Notes |
|---|---|
| **Verification code** | The content of the meta tag Google provides in the verification flow. Validated against `ValidHtml` rule (per [[apps-google-search-console]]). |

The Manager's `getMeta` returns the formatted meta tag string for injection: `<meta name="google-site-verification" content="..." />`.

### Verification methods (alternative)

While the meta-tag method is the default supported here, GSC also supports:
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

`ValidHtml` rule (per [[apps-google-search-console]] Request) ensures the verification code is valid HTML. Pasting plain text instead of the full meta tag may surface validation errors.

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

The Vue settings page renders a single text field with placeholder `<meta name='google-site-verification' content='XXXX_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'>`. The merchant is expected to paste the COMPLETE meta tag string (not just the content token). The ValidHtml rule will accept either, but Google's verifier needs the full tag — pasting only the token value passes save but fails verification.

### "Meta tag is required" trigger

When the app is active, leaving the field empty produces *"Meta tag is required"*. Pasting non-HTML text (e.g., random letters) produces *"Code must be a valid HTML"* via the ValidHtml rule. Whitespace alone passes the HTML check but fails the required check.

### Single box, inline edit (no slide-over)

The Vue page renders ONE settings box (`box-key: google_search_console`) with `editMethod: 'inline'` — clicking Edit reveals the textarea in place. There is no slide-over panel, no modal dialog, no separate Connect/Disconnect button (no OAuth in this app). The single field has no label text; the placeholder is the meta tag example. Save is via the standard top-right save action.

## Open questions

(None currently outstanding for this page.)
