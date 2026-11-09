---
type: feature
nav_path: "Analytics → Sales by traffic source (referral) → Attribution capture"
route_name: analytics
route_path: /admin/analytics
aliases: ["Sales by traffic source attribution", "Order referer attribution", "How referers are attributed to orders", "referer_key composition", "Ad-click parameter capture", "gad_source mapping"]
tags: [analytics, ccanalytics, orders, traffic, sales-by-traffic-source]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 12
---

> Part of [[analytics-sales-by-traffic-source]]. See the hub for related aspects (UI surfaces, data source + pipeline).

# Sales by traffic source — attribution capture

## Purpose

Explains **where the per-order referer attribution comes from** — i.e., how each order in the "Sales by traffic source (referral)" box gets its `referer_name`, `referer_group`, and `referer_key`. This is the single most surprising rule for merchants: attribution belongs to the **first visit of the session**, not the visit on which checkout completed. The UI that displays these values is in [[analytics-sales-traffic-source-ui]]; how the values are aggregated into the box is in [[analytics-sales-traffic-source-data]].

## Where to find it

There is no merchant UI for attribution capture — it happens silently on the storefront on every visit. The merchant only sees the **result** in the Analytics dashboard box and Details table. This page documents the capture logic so support can explain *why* an order was attributed to a given source.

## What the merchant can do here

- Understand why an order shows as "Direct", "Paid — Meta Ads", "google.com", etc.
- Explain to a merchant why a sale they expected under one channel landed under another (first-touch session attribution).
- Recognise the special `campaign` group (CloudCart's own marketing traffic) that appears in Details with no group label.

## What the merchant sees

The attribution surfaces only as the **referer name + group pill** on each row of the box and Details table (see [[analytics-sales-traffic-source-ui]]). Examples a merchant will encounter:

- `Direct` (no group) — visitor arrived with no referer and no ad-click / UTM params.
- `Google Ads — Display Network` (Paid) — `gad_source=3` was present on the landing URL.
- `Meta Ads` (Paid) — `fbclid` was present.
- `Facebook` (Social) / `google.com` (Search) — classified from the HTTP `Referer` header.

## Settings & fields

There are no merchant-editable settings for attribution. The capture is driven entirely by what the buyer's browser sends on the first visit. The key fields written per order are:

| Field | Meaning |
|-------|---------|
| `referer_name` | Human-readable source label (e.g., `"Google Ads — Display Network"`, `"Facebook"`, `"Direct"`) |
| `referer_group` | One of the 7 UI groups, or the internal `campaign` group, or `unknown` |
| `referer_host` | The parsed host from the HTTP Referer header |
| `referer_key` | The join key — `"{referer_group}-{referer_name}"` |

## Business rules

### Source — the buyer's PHP session, populated by storefront session middleware

The `referer_name`, `referer_group`, `referer_host`, and `referer_key` written per order come from the buyer's **PHP session** (`session('utmData')`), populated by the storefront's `OrderSource` middleware on the **first non-checkout request of the session**. The middleware:

1. Parses the HTTP `Referer` header.
2. Checks for ad-click parameters in the URL (`gclid`, `gad_source`, `gbraid`, `wbraid` → Google Ads; `fbclid` → Meta Ads; `ttclid` → TikTok Ads).
3. Checks for UTM tags (`utm_source`, `utm_medium`, `utm_campaign`).
4. For Google Ads: maps `gad_source` numeric codes (1-6) to network labels — `1=Google Search`, `2=Search Partners`, `3=Display Network`, `4=YouTube Search`, `5=YouTube Videos`, `6=Discover`. The `referer_name` becomes e.g. `"Google Ads — Display Network"`.
5. For Meta Ads: captures `fbclid` into the `_fbc` cookie (90-day, plain, not the application framework-encrypted) so Conversions API events can still include it after the URL parameter is gone.
6. For UTM `source=cloudcart`: assigns `referer_group=campaign` (a special internal group used only for CloudCart's own marketing campaigns; not shown in the standard 7-group dictionary).
7. For everything else: passes the referer URL through [[analytics-sessions-by-traffic-source]]'s `referers.json` classifier.

Falls back to "Direct" / "unknown" when no referer is present and no ad-click parameters / UTMs are detected.

### First-touch session attribution

Once captured, the values persist in the session and are attached to whichever order the buyer eventually places — so **the attribution belongs to the FIRST visit of the session, not the visit on which checkout completed**. A buyer who arrives via a Facebook ad, leaves, and returns later by typing the URL directly is still attributed to Facebook for that session.

### `referer_key` composition

`referer_key = "{referer_group}-{referer_name}"` (same shape as the visits side, but driven by the session middleware's parsing rather than the visitor tracker). Examples: `paid-Google Ads — Display Network`, `paid-Meta Ads`, `social-Facebook`, `unknown-Direct`. This is the join key used by the Details / ViewMore queries documented in [[analytics-sales-traffic-source-data]].

### Window, keys and edge cases

- **Window.** The source is kept in the storefront session until an order is placed (then cleared, so the next order starts afresh) or the session expires after 7 days without a visit. There is no other attribution window.
- **Precedence.** `utm_source=cloudcart` wins over everything (**CloudCart**, `campaign`). Next a Google click ID (`gclid`, `gad_source`, `gbraid` or `wbraid`, with or without UTM tags) gives **Google Ads** or **Google Ads — {network}** (`paid`); when no `utm_campaign` is set, `gad_campaignid` fills it as `gad_{id}`. Then `fbclid` gives **Meta Ads** and `ttclid` **TikTok Ads**. Only then the referring site counts. UTM tags alone do not change the row; they feed [[analytics-orders-by-social-source]].
- **Checkout first.** Checkout pages capture nothing. A session that opens on a checkout page and orders without visiting another page lands in **Direct**, even with a click ID in the address.
- **Join key.** The order copies the session's source and UTM tags and stores the visitor's `uuid` cookie value; no session ID goes on the cart or the order. The landing page ([[analytics-landing-pages-by-sales]]) is found through that `uuid`. Visits meet this box only through the source label; see [[analytics-sales-traffic-source-data]].
- **CloudCart campaigns.** The order also records the last campaign link clicked in the session, which the campaign revenue statistics read. The referral is first-touch per session; the campaign credit is last-click.
- **Fast orders** are created the same way and get the same source, UTM tags, `uuid` and campaign.
- **Cookie consent.** Nothing here waits for the cookie banner: the source lives in the store's own session, and neither the analytics tracker nor its `uuid` cookie checks the visitor's choice.
- **`cca_sid`.** Not a cookie: a random ID the tracker keeps in the browser tab's session storage and sends with its events. Closing the tab drops it.

### The "Direct" bucket

Orders where the visitor arrived with no referer have `referer_name = 'Direct'`. These are kept in the aggregation but the `group` is forced to `null` so the row doesn't show a misleading group chip.

### Eight referer groups can be emitted (`unknown` covers Direct + many uncategorised)

The UI lists seven groups (search / social / email / paid / news / payments / unknown), but the ingest pipeline can also emit `campaign` (CloudCart's own `utm_source=cloudcart` traffic). `campaign` rows appear in the Details list but the UI's group dictionary does not have a translation for it, so they render with no group label.

## Related

- [[analytics-sales-by-traffic-source]] — hub.
- [[analytics-sessions-by-traffic-source]] — Visits side; owns the `referers.json` classifier this page hands off to.
- [[analytics-orders-by-social-source]] — sibling box that ranks by source/medium with utm_campaign drill-down.
- [[apps-google-analytics]] — separate, external analytics integration.
- [[order]] — entity page for orders.

## Open questions

_None._
