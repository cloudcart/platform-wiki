---
type: concept
nav_path: "Concept → Metafields and metaobjects → Use cases → Banners, announcements and scheduled campaigns"
aliases: ["Banner metaobject", "Announcement bar", "Promo bar", "Scheduled banner", "Campaign banner", "Countdown banner", "Store settings metaobject", "Банер", "Лента с обява", "Промо лента", "Планиран банер", "Кампания"]
tags: [metafields, metaobjects, use-case, marketing, banners, nitrogen]
plan_gates: []
created: 2026-10-20
updated: 2026-10-20
source_count: 4
---

# Use case: banners, announcements and scheduled campaigns

> Part of [[metafields-use-cases]] in [[metafields-metaobjects]].

## Definition

Marketing changes the storefront every week: a free-delivery bar, a Black Friday hero, a countdown to the end of a sale, a notice about holiday delivery times. On a Nitrogen storefront these should not need a deploy. A **`banner` metaobject** holds each message with its placement and time window. Its active/draft status gives the merchant a switch. The storefront shows what is active and inside its window.

## Scope

### The data model

**Metaobject definition `banner`**, active/draft status **on**:

| Field | Type | Notes |
|---|---|---|
| `name` | single-line text, required | Display name, for staff: *BF 2026 — hero*. |
| `placement` | single-line text, `choices`: *announcement_bar, home_hero, category_top, cart, checkout_note* | **Admin filter** on. |
| `message` | single-line text, `max` 120 | |
| `image` | file (Image) | For hero placements. |
| `cta` | `link` | Button text and target. |
| `background`, `text_color` | `color` | |
| `starts_at`, `ends_at` | `date_time` | **Admin filter** on, for the time window. |
| `countdown` | `boolean` | Show a countdown to `ends_at`. |
| `priority` | `number_integer` | When several match, the highest wins. |

### On the Nitrogen storefront

- The layout asks once per page view, or caches briefly: `metaobjects(type: "banner", query: "fields.placement:announcement_bar fields.starts_at:<=2026-11-27T10:00:00Z fields.ends_at:>=2026-11-27T10:00:00Z")`, with the current time in the query.
- Drafts never come back. Only **active** entries of a `PUBLIC_READ` definition are returned.
- Several matches are ordered by `priority` on the storefront, as the API sorts entries only by id or last update.
- A category can point to its own campaign block through a category metafield, `custom.promo` → `banner` ([[metafields-use-case-category-content]]).

### Store-wide settings for the storefront

Store-wide values for the storefront live in a **singleton metaobject**: a `storefront_settings` definition with **one** entry, handle `main`. Its fields might be:

- `free_shipping_note` (single-line text);
- `support_phone` (single-line text);
- `social_links` (`list.link`);
- `footer_text` (rich text);
- `maintenance_message` (multi-line text).

The storefront reads `metaobject(handle: {type: "storefront_settings", handle: "main"})` once. Staff with the Metaobjects permission change these without a deploy.

## Contrasts

- **Banner entries vs native discounts and countdowns**: a discount's own data (end time, countdown on listings) is on the Storefront API with the product (`Product.discount`). A banner only *announces* a campaign and changes no price. The discount itself is set in Marketing.
- **Banner entries vs page sections** ([[metafields-use-case-page-sections]]): sections compose a page and stay until changed. Banners are short-lived messages selected by placement and time.
- **Singleton settings vs environment variables** ([[headless-environment-variables]]): environment variables are configuration for developers and need a redeploy. A settings entry is content staff can edit live.
- **Classic themes** do not read these entries. They are for Nitrogen ([[metafields-nitrogen]]).

## Where it applies

- Every Nitrogen storefront running campaigns: seasonal sales, delivery notices, free-shipping thresholds, store-wide announcements.
- The active/draft switch takes effect on the next read, with no storefront release.

## Related

- [[metafields-use-cases]]: all use cases.
- [[metaobjects-definitions]]: active/draft status.
- [[metafields-capabilities]]: date filters on entry fields.
- [[metafields-use-case-page-sections]]: composing whole pages.

## Open Questions

- None known.
