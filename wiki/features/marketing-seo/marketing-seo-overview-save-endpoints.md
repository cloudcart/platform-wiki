---
type: feature
nav_path: "Marketing → Seo → Save endpoints"
route_name: seo-main
route_path: /admin/marketing-new/seo
aliases: ["SEO save endpoints", "Main SEO API routes", "SEO settings load endpoint", "SEO per-card POST routes", "SEO legacy add-this route", "SEO API крайни точки"]
tags: [marketing, seo, api, routes, integration]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-seo]]. See the hub for the other page-level aspects (layout, card-save model, settings map, trial block) and the seven per-card deep dives.

# Main SEO settings — load & save endpoints

## Purpose

This aspect documents the **request plumbing** behind the Main SEO screen: the single read that loads every card on mount, the dedicated save route each card posts to, and the one card whose save lands on a legacy route instead of the modern API namespace. This is the page-level integration reference — useful for debugging a "this one card won't save" ticket or for anyone reconciling the screen against the API.

## Where to find it

Sidebar → Marketing → **SEO**. Route name `seo-main`, path `/admin/marketing-new/seo`. The endpoints below are called by that screen; the per-card save UX (Save / Revert, confirm modal) is on [[marketing-seo-overview-card-save]].

## What the merchant can do here

Nothing additional — this aspect is reference plumbing. The merchant experiences these endpoints only indirectly, as the network calls fired when they save a card.

## Settings & fields

The screen loads all card values from one read on mount:

- `GET /admin/api/core/seo/settings` returns the consolidated payload for every card:
  ```
  { canonical_is_active, allow_noindex_query_limit, noindex_query_limit,
    meta_page, sitemap, robots: [body, timestamp], og_image_url,
    rss_feed_count, rss_url, module: <social-share module settings> }
  ```

Each card then mutates its own keys and POSTs to its own dedicated endpoint:

| Card | Save endpoint | Body |
|------|---------------|------|
| Canonical | `POST /admin/api/core/seo/settings/canonical-activity/{0\|1}` | none (value is in the URL) |
| Deindex | `POST /admin/api/core/seo/settings/no-index-limit` | `{noindex_query_limit, allow_noindex_query_limit}` |
| Pagination word | `POST /admin/api/core/seo/settings/meta-page-title` | `{meta_page}` |
| Robots.txt | `POST /admin/api/core/seo/settings/robot-txt` | multipart, just the `robots` field |
| Sharing | `POST /admin/marketing/seo/add-this` (legacy route) | Open Graph image + social-share module settings |
| RSS | `POST /admin/api/core/seo/settings/rss-feed` | `{rss_feed_count}` |

The **Sitemap URL** and **RSS feed URL** fields are read-only — there is no save route for them.

## Business rules

### The Sharing card posts to a legacy route

The Sharing card is the **only** card whose POST does NOT live under `/admin/api/core/seo/settings/*`. It hits the legacy route `/admin/marketing/seo/add-this` instead, handled by the legacy settings handler. The screen reuses the same wrapper UX, but the underlying save path differs — relevant when a Sharing save fails while the other cards succeed. See [[marketing-seo-sharing]].

### Canonical save is body-less and URL-constrained

The Canonical POST has **no request body** — the on/off value is embedded in the URL (`canonical-activity/0` or `canonical-activity/1`). The route is regex-constrained to `(0|1)`; any other value returns 404. This is why the card saves instantly on toggle with no Revert (see [[marketing-seo-overview-card-save]]).

### Robots.txt save has no server-side validation

The Robots.txt POST is one of the few save endpoints with **no** server-side validation — anything the merchant submits is accepted and persisted. The "Are you sure?" confirm modal is the only safety net. The save also writes an `update_robots` timestamp so the storefront cache invalidates and crawlers see a fresh `Last-Modified`. See [[marketing-seo-robots]].

### One read, many writes

Because the whole screen hydrates from the single `GET /admin/api/core/seo/settings` read but each card writes through its own route, a stale value in one card after save almost always points at that card's specific endpoint, not the shared read.

## Related

- [[marketing-seo]] — hub.
- [[marketing-seo-overview-card-save]] — the per-card Save / Revert UX these endpoints back.
- [[marketing-seo-canonical]] — body-less canonical-activity route.
- [[marketing-seo-robots]] — unvalidated robot-txt route + `update_robots` timestamp.
- [[marketing-seo-sharing]] — legacy add-this route.
- [[marketing-seo-rss]] — rss-feed route.

## Open questions

None.
