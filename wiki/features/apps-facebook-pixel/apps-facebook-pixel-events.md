---
type: feature
nav_path: "Apps → XML Feed → Facebook → Events & dedup"
route_name: apps.facebook.overview
route_path: /admin/apps/xml_feed/facebook
aliases: ["Facebook Pixel events", "Meta standard events", "Facebook event vocabulary", "Facebook event_id dedup", "Facebook custom_data fields", "Facebook Dynamic Ads events", "Facebook events not firing when logged in admin", "test Facebook pixel without admin session", "no Facebook events for admin session", "SubscribedButtonClick", "Meta automatic events", "double AddToCart", "AddToCart fires twice", "duplicate add to cart event", "Meta over-counts AddToCart", "events I did not send"]
tags: [apps, facebook, meta, pixel, capi, events, tracking]
plan_gates: ["facebook.capi"]
created: 2026-06-10
updated: 2026-08-08
source_count: 4
---

> Part of [[apps-facebook-pixel]]. See the hub for the other aspects (CAPI gating, `event_source_url` known bug) and the settings tab.

# Facebook Pixel — events & dedup

## Purpose

This aspect documents **which events fire**, **when**, and **how Meta dedupes the two transport legs**. The integration fires Meta's fixed standard ecommerce event vocabulary at storefront user actions, sending each event on both the browser pixel leg (`fbq`) and the server-side [[apps-facebook-pixel-capi|CAPI]] leg with a shared `event_id`. There is no UI to add, rename, or toggle individual events — the vocabulary is fixed.

## Where to find it

The events fire automatically from the storefront once the Pixel is configured. There is no per-event screen in the admin. Configuration of the Pixel ID / Access Token / CAPI toggle that enables these events lives on [[apps-facebook-pixel-settings]].

## What the merchant can do here

- Verify that events are firing via Meta Events Manager (browser + server) — not inside CloudCart.
- Use a **Test Event Code** ([[apps-facebook-pixel-settings]]) to route events to Meta's Test Events panel for live verification.
- **Test from a browser that is NOT logged into the store's admin panel** — events are suppressed while an admin-panel session is active (see Business rules), so a logged-in admin sees no events even when the Pixel is configured correctly.

### What the merchant CANNOT do here

- Add custom events — only the fixed standard vocabulary below fires. For custom events use [[apps-google-tags]] (GTM).
- Toggle individual events on/off — they fire automatically per the customer's storefront actions.
- Change the `event_id` derivation or the dedup behaviour.

## Settings & fields

No fields of its own — see [[apps-facebook-pixel-settings]] (`pixel`, `token`, `test_event_code`, `capi_status`). The event payload assembles `custom_data` (below) and `user_data` (the PII chain on [[apps-facebook-pixel-capi]]) at fire time.

## Business rules

### Standard event vocabulary

The integration fires Meta's standard ecommerce events at storefront user actions:

| Event | Fires when | Browser pixel | CAPI server-side |
|---|---|---|---|
| `PageView` | Any storefront page view | Yes | Yes (when `data.url` set) |
| `ViewContent` (product) | Product detail page view | Yes | Yes |
| `ViewContent` (product_group) | Category / collection page view | Yes | Yes |
| `Search` | Storefront search results page | Yes | Yes (see [[apps-facebook-pixel-event-source-url]]) |
| `AddToCart` | Customer adds item to cart | Yes | Yes (see [[apps-facebook-pixel-event-source-url]]) |
| `AddToWishlist` | Customer adds item to favourites | Yes | Yes (see [[apps-facebook-pixel-event-source-url]]) |
| `InitiateCheckout` / `InitiateFastCheckout` | Customer enters checkout | Yes | Yes |
| `Purchase` / `FastPurchase` | Order successfully placed | Yes | Yes |

Anything outside this list is silently ignored. There is no UI to add custom events — for that the merchant has to use [[apps-google-tags]] (GTM).

### Dedup via `event_id`

The browser pixel and the server CAPI call both carry the same `event_id`. Meta dedupes when both arrive within ~24h:

- `AddToCart`, `AddToWishlist`, `ViewContent`, `PageView`, `Search` — `event_id` is generated client-side per event (`generateEventId` — hex hash).
- `InitiateCheckout`, `Purchase` (and their `Fast*` variants) — `event_id` is deterministic: `md5(cart_id + ':' + product_ids_joined)`. So if the same Purchase event accidentally fires twice on the same cart, Meta dedupes it because `event_id` is identical.

### Meta Events Manager also shows events CloudCart never sent

The Meta pixel does **its own automatic tracking** on top of whatever the store sends. Once the pixel script is on the page, Meta can record interactions by itself — most visibly **`SubscribedButtonClick`**, which fires when a visitor clicks a button, including the **Buy / Add to cart** button.

So an event appearing in Events Manager is **not** proof that CloudCart sent it. The store's own vocabulary is the fixed list above; anything outside it (`SubscribedButtonClick`, `Microdata`, other auto-collected signals) originates in Meta's pixel, not in the platform.

**Merchant-visible consequence:** a click on *Buy* can show **two entries** around the same moment — CloudCart's `AddToCart` and Meta's automatic `SubscribedButtonClick`. That reads like the store fired twice, and is a recurring report from merchants and their ad agencies. It is not double-sending: they are two different events, one of which the platform did not send.

**Where it is controlled:** these automatic events are switched on and off in **Meta Events Manager** (the pixel's automatic / auto-collected event settings), by whoever administers the Meta Business account. There is no CloudCart setting for them — the merchant or their agency turns them off on Meta's side.

### One add to cart = one `AddToCart` from the platform

The storefront fires a **single** `AddToCart` per add. (An earlier defect in which two listeners — the product-added and the product-updated hooks — each fired one has been fixed; the deployed listener is single and idempotent.)

When judging a suspected duplicate, note that `AddToCart` carries a **per-event generated** `event_id`, not a deterministic one like `Purchase` (see *Dedup via `event_id`* above). Two `AddToCart` calls therefore carry two different ids, and Meta cannot dedupe them — so a real double-fire would genuinely double-count, while Meta's own automatic events are simply a different event type and never dedupe against `AddToCart` at all.

### Event payload `custom_data` fields

For each event the `custom_data` object includes:

- `currency` (defaults to site currency).
- `value` (numeric — cart value / order total / line item price).
- `contents[]` (array of `{ id, quantity, item_price, title, brand, category }`).
- `content_ids[]` (string IDs).
- `content_name` (joined product titles for multi-item events).
- `content_type` (`product` or `product_group`).
- `search_string` (Search event only).
- `num_items` (InitiateCheckout / Purchase only).

Currency defaults to the site's primary currency ([[multi-currency]]) when the browser doesn't supply one.

### `Purchase` fires from the storefront, not the order pipeline

`Purchase` / `FastPurchase` fire from the storefront thank-you page after the order is successfully placed — it is a storefront client action, not a server-side hook off the [[order-processing-pipeline]]. This is why an order created via admin or API does not fire a `Purchase` event.

### Events are suppressed while an admin-panel session is active (a safeguard)

Storefront events are **not sent to Meta** when the same browser also has an **active admin-panel (sitecp) session** for the store. This is a deliberate safeguard so the merchant's / staff's own storefront browsing doesn't pollute the Pixel + Dynamic Ads data with internal traffic.

**Implication for testing:** to confirm events actually reach Meta (Events Manager / Test Events), open the storefront in a browser — or a private / incognito window — that is **not signed into the store's admin panel**. While logged into the admin, no events fire, so the setup looks broken even when the Pixel is correct. The same caveat applies to the [[apps-facebook-pixel-capi|CAPI]] server leg.

### Permission

Standard apps permission scope (any admin with Apps access can edit the Pixel config). CAPI access requires plan feature `facebook.capi`.

## Related

- [[apps-facebook-pixel]] — hub.
- [[apps-facebook-pixel-capi]] — the server-side leg that sends these events (gating + PII).
- [[apps-facebook-pixel-event-source-url]] — the bug affecting `AddToCart` / `AddToWishlist` / `Search` server events.
- [[apps-facebook-pixel-settings]] — Test Event Code + Pixel ID.
- [[apps-google-tags]] — GTM alternative for custom events.
- [[checkout-flow]] — where `InitiateCheckout` + `Purchase` originate.
- [[order-processing-pipeline]] — `Purchase` fires from the storefront after the order is placed (not from the pipeline).
- [[multi-currency]] — `currency` default.

## Open questions

- **PCM plugin event_id mismatch** — when Meta's PCM (Privacy-enhanced Conversions Measurement) plugin is active in the merchant's Meta config, the browser-side `event_id` gets overridden to `pcm_plugin-set_<hash>` format, which never matches CloudCart's hex `event_id` sent server-side → Meta cannot dedupe → events double-count. Distinct issue from the `event_source_url` bug ([[apps-facebook-pixel-event-source-url]]); track separately.
- **(verify)** Whether the deterministic `md5(cart_id + ':' + product_ids_joined)` `event_id` for `Purchase` survives a cart edit between `InitiateCheckout` and order placement (changed product IDs → different `event_id` → no dedup across the two events, which is expected since they are different event types).
