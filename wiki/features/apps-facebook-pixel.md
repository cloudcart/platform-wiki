---
type: feature
nav_path: "Apps → XML Feed → Facebook"
route_name: apps.facebook.overview
route_path: /admin/apps/xml_feed/facebook
aliases: ["Facebook Pixel", "Meta Pixel", "Facebook Conversions API", "Facebook CAPI", "Meta CAPI", "Facebook tracking pixel"]
tags: [apps, facebook, meta, pixel, capi, conversions-api, tracking, analytics]
plan_gates: ["facebook.capi"]
created: 2026-06-08
updated: 2026-08-08
source_count: 3
---
# Facebook Pixel + Conversions API (CAPI)

## Purpose

**Facebook Pixel + Conversions API (CAPI)** integration — fires Meta's standard ecommerce events (`PageView`, `ViewContent`, `AddToCart`, `Search`, `AddToWishlist`, `InitiateCheckout`, `Purchase`) on the storefront to **Meta Ads** for:

- Conversion attribution (which Facebook / Instagram ad drove the sale).
- Custom audiences (re-target visitors of specific product pages).
- Lookalike audiences (prospecting based on past buyers).
- Conversion-optimised campaign bidding.

Two transport paths fire in parallel for each event:

1. **Browser Pixel** — `fbq('track', ...)` JS call from the storefront → Meta's edge.
2. **Conversions API (CAPI)** — server-side POST to `https://graph.facebook.com/v<X>/<pixel_id>/events` from CloudCart → Meta's API.

Both legs share an `event_id` so Meta can dedupe — the browser event and the server event represent the same conversion. See [[apps-facebook-pixel-events]] for the event vocabulary + dedup mechanics, and [[apps-facebook-pixel-capi]] for the server-side gating, PII matching, and error handling.

The Facebook sub-feed (product catalog XML) is documented in [[apps-xml-feed]]; this cluster covers the **Pixel + CAPI tracking** half of the same integration. They share an app key (`app.xml_feed.facebook`) and one settings page.

## Sub-pages (in this cluster)

This feature is split into 4 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[apps-facebook-pixel-events]] — the standard event vocabulary (`PageView`, `ViewContent`, `AddToCart`, `Search`, `AddToWishlist`, `InitiateCheckout`, `Purchase`); dedup via `event_id`; the `custom_data` payload fields per event; the admin-session testing caveat; and **why Events Manager shows events CloudCart never sent** (Meta's own automatic tracking, e.g. `SubscribedButtonClick` on the Buy button).
- [[apps-facebook-pixel-payload-reference]] — the exact attributes in each event + the **fingerprint** that distinguishes a CloudCart event from a foreign one (a second pixel the merchant added via GTM / Custom JS). The page to reach for *"your events are wrong / missing fields"* tickets.
- [[apps-facebook-pixel-capi]] — the server-side Conversions API leg: the three gating conditions, Targeting-cookie consent, the PII `user_data` fallback chain, single-pixel-per-store, storefront-only firing, CSRF requirement, silent error logging.
- [[apps-facebook-pixel-event-source-url]] — the CRITICAL `event_source_url` known bug (Meta warned 2026-06-08 that events without it get blocked); which events are affected; support-agent escalation guidance; merchant impact.

The settings tab (Pixel ID, Access Token, Test Event Code, Enable CAPI) lives on [[apps-facebook-pixel-settings]].

## Where to find it

Sidebar → Apps → install → **XML Feed** → **Facebook** sub-feed. See [[apps-facebook-pixel-settings]] for the configuration fields (Pixel ID, Access Token, Test Event Code, Enable CAPI).

## What the merchant can do here

- Configure **Facebook Pixel ID** (numeric, from Meta Events Manager).
- Configure **Access Token** for the Conversions API.
- Optionally set a **Test Event Code** to route events to Meta's Test Events panel.
- Toggle **Enable CAPI** (server-side events).
- The product catalog feed URL (XML) — paste into Meta Commerce Manager.

### What the merchant CANNOT do here

- View Pixel analytics inside CloudCart — those live in Meta Events Manager.
- Configure per-event toggles (events fire automatically per the storefront's user actions — see [[apps-facebook-pixel-events]]).
- Use without a Meta Business account + Pixel created in Events Manager.
- Send custom events (only the fixed standard event vocabulary fires).
- Override the deduplication / hashing logic.

## Settings & fields

See [[apps-facebook-pixel-settings]] for the saved fields (`pixel`, `token`, `test_event_code`, `capi_status`).

## Business rules

- **Two transport legs, one `event_id`.** Browser pixel + server CAPI both carry the same `event_id` so Meta dedupes the duplicate conversion. Full vocabulary + dedup rules: [[apps-facebook-pixel-events]].
- **CAPI is triple-gated.** Plan feature `facebook.capi` + Access Token filled + Enable CAPI on + visitor accepted the Targeting cookie group. If any gate fails only the browser pixel fires. Full mechanics: [[apps-facebook-pixel-capi]].
- **Targeting cookie group gates BOTH legs.** Reject Targeting consent in the GDPR banner → neither browser pixel nor CAPI sends data to Meta. See [[apps-gdpr-cookies]].
- **One Pixel ID per store install.** Multi-pixel routing requires [[apps-google-tags]] (GTM) with CAPI disabled here.
- **Storefront-only.** The pixel + CAPI relay runs only from the storefront; the admin panel is excluded so admin previews never fire conversion events.
- **`event_source_url` CRITICAL BUG.** Meta warned (2026-06-08) that CAPI events without `event_source_url` will be blocked. `AddToCart`, `AddToWishlist`, `Search` send no URL; `InitiateCheckout` / `Purchase` send a relative path. See [[apps-facebook-pixel-event-source-url]].
- **Permission.** Standard apps permission scope (any admin with Apps access can edit). CAPI access requires plan feature `facebook.capi`.

## Related

- [[apps]] — App Store.
- [[apps-facebook-pixel-events]] — event vocabulary + dedup (aspect).
- [[apps-facebook-pixel-payload-reference]] — per-event attribute reference + how to tell CloudCart events apart from a foreign pixel (aspect).
- [[apps-facebook-pixel-capi]] — server-side CAPI gating + PII matching (aspect).
- [[apps-facebook-pixel-event-source-url]] — the `event_source_url` known bug (aspect).
- [[apps-facebook-pixel-settings]] — settings sub-page (Pixel ID, Access Token, Test Event Code, CAPI toggle).
- [[apps-xml-feed]] — the Facebook product catalog feed (sister half of this integration; same app key `app.xml_feed.facebook`).
- [[apps-facebook-comments]] — Facebook Comments module (different integration, just shares the brand).
- [[apps-tiktok-pixel]] — sister tracking integration with the same browser+CAPI architecture.
- [[apps-google-analytics]] — alternative analytics pixel.
- [[apps-google-tags]] — GTM-based alternative if the merchant needs multi-pixel routing or custom events.
- [[apps-gdpr-cookies]] / [[apps-gdpr-overview]] — Targeting cookie consent gating.
- [[plan-features]] — `facebook.capi` plan feature gate.
- [[checkout-flow]] — where `InitiateCheckout` + `Purchase` events originate.
- [[order-processing-pipeline]] — `Purchase` fires from the storefront after the order is placed.
- [[multi-currency]] — `currency` field defaults to site currency.
- [[marketing-subscribers]] — subscriber PII fallback chain (channel-verified email/phone).
- [[platform-rate-limits]] — GeoIP fallback for `countryCode` in CAPI payload (MaxMind).

## Open questions

- **`event_source_url` engineering fix ETA** (CRITICAL, 2026-06-08) — tracked in [[apps-facebook-pixel-event-source-url]].
- **(verify)** The Meta Graph API version used by the bundled FB SDK — older SDK versions hit deprecated `v<X>` endpoints. Confirm which version is in the active composer-locked `facebook/php-business-sdk`.
- **Events in Meta Events Manager that CloudCart did not send.** Meta's pixel auto-tracks on its own — most visibly `SubscribedButtonClick` on the Buy button, which looks like a duplicate `AddToCart`. The platform sends exactly one `AddToCart` per add. Turned off in Meta Events Manager, not in CloudCart — see [[apps-facebook-pixel-events]].
- **PCM plugin event_id mismatch** — when Meta's PCM (Privacy-enhanced Conversions Measurement) plugin is active, the browser-side `event_id` gets overridden to `pcm_plugin-set_<hash>` format, which never matches CloudCart's hex `event_id` sent server-side → Meta cannot dedupe → events double-count. Distinct from the `event_source_url` bug; tracked in [[apps-facebook-pixel-events]].
