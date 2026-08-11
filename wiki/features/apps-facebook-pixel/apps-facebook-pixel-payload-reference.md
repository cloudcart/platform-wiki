---
type: feature
nav_path: "Apps → XML Feed → Facebook → Event payload reference"
route_name: apps.facebook.overview
route_path: /admin/apps/xml_feed/facebook
aliases: ["Facebook event payload", "Facebook event attributes", "Facebook event fingerprint", "Is this a CloudCart Facebook event", "distinguish CloudCart Facebook events", "second Facebook pixel GTM custom js", "Facebook event contents fields", "Facebook eventID external_id", "foreign Facebook pixel"]
tags: [apps, facebook, meta, pixel, capi, events, payload, debugging]
plan_gates: []
created: 2026-06-19
updated: 2026-06-19
source_count: 1
---

> Part of [[apps-facebook-pixel]]. See the hub for the other aspects (events & dedup, CAPI, event_source_url bug) and the settings tab.

# Facebook Pixel — event payload reference & fingerprint

## Purpose

The exact attributes CloudCart puts in **each** Facebook (Meta) Pixel event, and — the support-critical part — **how to tell a CloudCart event apart from a foreign one** firing on the same storefront. Merchants frequently add a *second* Meta Pixel themselves (via [[apps-google-tags|Google Tag Manager]] or Custom CSS/JS — see [[design-custom-assets]]), and those events do **not** carry the attributes CloudCart sends. So when a merchant reports *"your events are wrong / missing fields"*, the first thing to establish is whether the event in Meta Events Manager is actually CloudCart's or their own extra pixel's. This page is the reference for that distinction.

The event **vocabulary** + dedup mechanics are on [[apps-facebook-pixel-events]]; the server-side `user_data` PII chain is on [[apps-facebook-pixel-capi]].

## Where to find it

Events fire from the storefront — there is no admin screen. Inspect them in **Meta Events Manager** (Test Events / Overview) or the browser network tab (the `fbq` call + CloudCart's `/facebook/pixel/<event>` relay to the server CAPI leg).

## What the merchant can do here

Nothing is configured here — this is a reference for inspecting the events CloudCart already fires. In practice the merchant (or a support agent) uses it to:

- Read a storefront event's attributes in **Meta Events Manager** / the browser network tab.
- Confirm an event is CloudCart's (via the fingerprint below) rather than a second pixel the merchant added via [[apps-google-tags|GTM]] / Custom JS.

### What the merchant CANNOT do here

- Change which attributes are sent — the payload shape is fixed (see [[apps-facebook-pixel-events]] for why the event vocabulary isn't editable).

## Settings & fields

This page has no settings of its own — the payload is assembled at fire time from the storefront action. Pixel ID / Access Token / CAPI toggle are on [[apps-facebook-pixel-settings]].

## The common envelope (every CloudCart event)

Every event CloudCart fires carries:

| Attribute | What it is | Foreign-pixel signature |
|---|---|---|
| **`eventID`** | CloudCart-generated dedup id, sent on **both** the browser `fbq(..., {eventID})` and the CAPI server event so Meta dedupes the two legs. | A GTM / custom pixel fires without a matched `eventID` (or Meta's PCM plugin overrides it to `pcm_plugin-set_<hash>`). |
| **`external_id`** | CloudCart's subscriber / customer identifier (inside `user_data`). **Required** — CloudCart drops the CAPI relay entirely if it's missing. | Foreign events have no `external_id`. |
| **`event_source_url`**, **`action_source = website`**, **`event_time`** | Standard CAPI envelope. | — |
| **`user_data`** | `fbp` + `fbc` cookies, client IP, user-agent, and the hashed PII chain (email / phone / name / address) — full chain on [[apps-facebook-pixel-capi]]. | Foreign events usually send only `fbp`, no hashed PII. |
| **`value`** + **`currency`** | Money for the event (cart value / order total / line price); `currency` defaults to the site currency ([[multi-currency]]). | — |

## Per-event `custom_data`

| Event | `content_type` | Carries | `eventID` derivation |
|---|---|---|---|
| `PageView` | — | `url` only (no `contents`) | client-side hash |
| `ViewContent` (product) | `product` | `contents[]`, `content_ids[]`, `content_name`, `value`, `currency` | client-side hash |
| `ViewContent` (category) | `product_group` | same, for the category's products | client-side hash |
| `Search` | — | `search_string`, `contents[]`, `content_ids[]` | client-side hash |
| `AddToCart` / `AddToWishlist` | `product` | `contents[]`, `content_ids[]`, `value`, `currency` | client-side hash |
| `InitiateCheckout` / `InitiateFastCheckout` | `product` | `contents[]`, `content_ids[]`, `num_items`, `value`, `currency` | deterministic `md5(cart_id + ':' + product_ids)` |
| `Purchase` / `FastPurchase` | `product` | `contents[]`, `content_ids[]`, `num_items`, `value`, `currency` | deterministic `md5(cart_id + ':' + product_ids)` |

### The `contents[]` element shape — CloudCart's signature

Each item in `contents[]` is an object with CloudCart's specific keys:

`{ id, quantity, item_price, title, brand, category }`

(the CAPI leg additionally adds `product_id` = the stringified `id`). A foreign pixel typically sends a bare `content_ids[]` with **no** `contents[]`, or `contents` objects without `item_price` / `title` / `brand` / `category`. **The presence of these per-item fields is the clearest single sign that the event is CloudCart's.**

## Business rules — how to tell a CloudCart event from a foreign one

In Meta Events Manager (or the browser), a genuine CloudCart event shows **all** of:

1. A matched **`eventID`** across the **browser + server** legs — Events Manager labels it "Browser and Server" and deduplicated.
2. An **`external_id`** in `user_data`.
3. **`contents[]`** with the `item_price / title / brand / category` keys above (plus `content_type` = `product` / `product_group`).
4. For `Purchase` / `InitiateCheckout`, an `event_id` in the `md5(cart_id: product_ids)` shape.
5. A **CAPI server counterpart** — CloudCart sends both legs.

An event **missing** these — e.g. a browser-only `ViewContent` with no `contents[]`, no `external_id`, and no matching server event — was **not** fired by CloudCart. It is almost always a **second Meta Pixel the merchant installed themselves** via [[apps-google-tags|GTM]] or Custom CSS/JS ([[design-custom-assets]]). That second pixel is outside CloudCart's control and will not carry the attributes above — which is the usual root cause behind *"CloudCart's events are wrong"* tickets that turn out to be the merchant's own duplicate pixel.

> Reminder: CloudCart events don't fire at all while the browser is logged into the store admin panel (a safeguard — see [[apps-facebook-pixel-events]]), so always test from a logged-out / incognito session.

## Related

- [[apps-facebook-pixel]] — hub.
- [[apps-facebook-pixel-events]] — event vocabulary + dedup + the admin-session testing caveat.
- [[apps-facebook-pixel-capi]] — the `user_data` PII chain + server CAPI leg.
- [[apps-google-tags]] — GTM, a common source of a second (foreign) pixel.
- [[design-custom-assets]] — Custom CSS/JS, another common source of a second pixel.
- [[multi-currency]] — the `currency` default.

## Open questions

- None.
