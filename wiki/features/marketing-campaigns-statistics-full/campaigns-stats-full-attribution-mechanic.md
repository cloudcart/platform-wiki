---
type: feature
nav_path: "Marketing → Campaigns → Statistics → Attribution mechanic"
route_name: campaigns.statistics.full
route_path: /admin/campaigns/statistics
aliases: ["Last-touch attribution", "Campaign attribution window", "cc_campaign query param", "Click tracking middleware", "Session attribution", "Атрибуция по последно докосване"]
tags: [marketing, campaigns, attribution, tracking, session]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-05-23
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-statistics-full]]. See the hub for the other aspects (dashboard, revenue panel, attribution metadata, revenue statuses, order processing).

# Attribution mechanic — session-based, last-touch

## Purpose

This page documents **how** an order gets credited to a campaign in the first place: the click-through link, the tracking middleware, the session store, and the last-touch rule. It explains the answers to merchant questions like *"why did only one of the two campaigns I sent get credit for this order?"* and *"why didn't my order get attributed even though the customer clicked my email?"*

## Where to find it

This is a storefront-side mechanic, not an admin screen. Its results surface on [[campaigns-stats-full-dashboard]] and [[campaigns-stats-full-revenue-panel]]. The behaviour is a platform invariant — there is nothing for the merchant to configure.

## What the merchant can do here

Nothing is configurable. Understanding the mechanic lets a merchant interpret why attribution credited (or didn't credit) a given order.

## Settings & fields

There are no settings. The attribution window is governed by the platform's standard session lifetime (see Business rules).

## Business rules

### The click-through link carries a `cc_campaign` query param

A campaign's click-through link carries a `cc_campaign` query parameter encoding the campaign id, action (step) id, channel, subscriber id, etc. (plus `cc_subscriber`). This query string is the only attribution carrier — there is no separate "attribution cookie".

### The tracking middleware reads the param, then stores it server-side

When the customer hits the storefront, the `CampaignTrack` middleware reads the `cc_campaign` query parameter and writes the parsed data into the **PHP session** (`campaignData` and `subscriberData` keys) — server-side, not a client cookie. So the attribution lifetime IS the PHP session lifetime: typically **2 hours of inactivity** (CloudCart's default the application framework session config) or until the customer closes the browser.

### The tracking redirect strips the query params

After parsing `cc_campaign`, the middleware **redirects** to the same URL **without** the `cc_campaign` and `cc_subscriber` params (it rebuilds `fullUrlWithQuery` with those keys nulled and trims a trailing `?`). This is a UX cleanup so the address bar shows the canonical URL without the long tracking blob. Because the session was already populated before the redirect, subsequent in-session orders are still attributed.

### Last-touch wins — re-clicking overwrites the session

When the same customer clicks another campaign's link, the new `cc_campaign` param **overwrites** the previous `campaignData` in the session. **Last-touch wins.** There is no first-touch, multi-touch, or split-credit model:

- Customer receives Campaign A's email, then Campaign B's email, then orders → only **Campaign B** is credited. Campaign A's revenue does not include this order.

### Attribution is per-order, not proportional

The entire order `price_total` is credited to the single last-touch campaign (and to its step). There is no proportional attribution across multiple campaigns a customer may have received.

### Attribution does not persist across sessions

If the customer abandons a session and starts a fresh one, **no campaign attribution applies** to the new session's orders — even if they had recently clicked an email — because the `campaignData` lived only in the prior session.

## Related

- [[marketing-campaigns-statistics-full]] — hub.
- [[campaigns-stats-full-attribution-metadata]] — the meta rows written once an attributed order is placed.
- [[campaigns-stats-full-order-processing]] — the job that consumes the captured session data and stamps the order.
- [[campaigns-stats-full-revenue-panel]] — where attributed orders are listed.
- [[campaign]] — Campaign entity.
- [[marketing-channels]] — channels carried in the `cc_campaign` blob.

## Open questions

No outstanding questions.
