---
type: concept
nav_path: "Concept → Headless storefronts → Analytics and consent"
aliases: ["Headless analytics", "Server-side tracking Nitrogen", "analyticsEventPublish", "analyticsSettings", "cookieConsent", "reportedInBrowser", "reportsTo", "consentedGroups", "refusedGroups", "Conversions API headless", "Measurement Protocol", "Проследяване Nitrogen", "Съгласие за бисквитки Nitrogen", "Пиксели витрина"]
tags: [nitrogen, headless, storefront-api, analytics, pixels, gdpr, consent, concepts]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 4
---

> Part of [[headless-storefront]].

# Headless — analytics, ad vendors and consent

## Definition

A Nitrogen storefront loads the merchant's pixels itself and also reports events to the platform with `analyticsEventPublish`. The platform then sends them server-side to Meta, TikTok, Google Analytics 4 and CloudCart Analytics, under the buyer's consent. `analyticsSettings` says which pixels the merchant runs. `cookieConsent` gives the banner.

## Scope

Covered:

- The events, and what each reaches.
- Event ids, and counting a conversion once.
- Consent: the groups, and what a refusal stops.
- The `cookieConsent` banner.

Not covered:

- Setting up the pixels in the admin — see [[apps-facebook-pixel-settings]], [[apps-tiktok-pixel-settings]] and [[apps-google-analytics-settings]].
- The merchant's cookie groups — see [[apps-gdpr-cookies-groups]].

## Contrasts

- **Browser pixel vs server-side report** — a storefront with pixels sends both where `AnalyticsPixel.serverSide` is true, since a browser pixel can be blocked. Meta and TikTok count the two once when they share an id. Google Analytics adds them up.
- **`analyticsSettings.consentGroups` vs `cookieConsent.groups`** — the first lists every group a pixel can follow, switched-off groups included. Build a banner from the second, which lists only what the store offers.

## Where it applies

### Events

`analyticsEventPublish(event, input)`. Report each page once: a product page with `VIEW_CONTENT`, a search results page with `SEARCH`, every other page with `PAGE_VIEW` and its `pageType`.

| Event | What it reaches |
|---|---|
| `PAGE_VIEW`, `VIEW_CONTENT`, `SEARCH`, `ADD_TO_CART`, `REMOVE_FROM_CART`, `ADD_TO_WISHLIST`, `REMOVE_FROM_WISHLIST` | The vendors and CloudCart Analytics. A cart change reaches vendors as its line, in the quantity changed, not the whole cart. |
| `IDENTIFY_CUSTOMER` | CloudCart Analytics only. The customer is the buyer in `@inContext(buyer:)`, never an id from the input; without one nothing is sent. |
| `BEGIN_FAST_ORDER` | The start of the fast order form. Meta and TikTok get it under the merchant's name for this step (`fastOrderSettings.trackingEvents.checkout`). `fastOrderSubmit` then reports the purchase and links it for the same visitor. |
| `VIEW_CART` | A cart shown without a page of its own, such as a drawer. CloudCart Analytics records a cart view; ad vendors are not sent it. The cart page is a `PAGE_VIEW` with `pageType: CART`. |
| `BEGIN_CHECKOUT`, `PURCHASE` | Ad vendors only: the checkout itself reports them to CloudCart Analytics. |

**Without `input.visitorId` nothing is sent server-side.** It comes from `visitorSessionCreate`, or from CloudCart Analytics' own `init` in the browser.

Vendors are sent the event right after the response. `reportsTo` lists them. Empty is not a failure: the merchant has no server-side reporting, or the buyer gave no consent. A vendor's later rejection is not reflected there. `dispatched` is deprecated.

### Event ids

- `input.eventId` is 32 hexadecimal characters. Anything else is ignored, and one is made and returned.
- `BEGIN_CHECKOUT` with `cartId` and `PURCHASE` with `orderId` always take the id derived from the cart or the order, so a reloaded page or a retry reports the same conversion. Fire the browser's event with the returned `eventId`.
- Meta and TikTok count once when the browser and the server share the id. Google Analytics does not: list it in `reportedInBrowser` when the browser's gtag already sent the event, and the server does not send it.
- `CLOUDCART_ANALYTICS` in `reportedInBrowser` sends nothing from the server. The request comes back in `cloudCartAnalytics`, for the browser to POST its `body` as JSON to `https://cca.cloudcart.com/{site id}/{name}`.
- `FastOrderPayload.analyticsEventId` is the id for a fast order's purchase; a retry gets the same.

### Order and customer data

- `orderId` is read only when the operation runs for that order's own signed-in customer (`@inContext(buyer)`). Anyone else's, a guest's included, is ignored, and the event goes without order data.
- `customerEmailHash` is the e-mail trimmed, lower-cased and SHA-256 hashed, never the e-mail itself. An order's own e-mail takes precedence.

### Consent

`consentedGroups` and `refusedGroups` state the buyer's choice for this event.

- A refusal wins, and stops Meta, TikTok and Google Analytics for that event.
- A group in neither list counts as its default (`acceptedByDefault`).
- `AnalyticsPixel.consentGroup` says which group each pixel waits for. A browser client must not fire a pixel until its group is accepted.

| Vendor | Group |
|---|---|
| Meta, TikTok | `targeting` |
| Google Analytics | `performance` |
| Google Ads | `targeting` |
| Google Analytics and Ads while the GDPR app's Google Consent Mode group runs | `consent_mode_for_traffic`, default no |

Without the GDPR app, `consentGroups` is empty and nothing gates the pixels.

### The banner

`cookieConsent.active` false means no GDPR app and no banner. Otherwise:

- Build the banner from `cookieConsent.groups`, in that order.
- `cookieConsent.mode` is `BAR` or `WALL`, or null when the merchant shows neither.
- The choice is stored in `cookieName` as `key:yes` or `key:no`, joined with `+`, on path `/`, for 365 days. The platform's storefront and checkout read the same cookie.
- A group the merchant switched off is never on a visitor's cookie, so it counts as its default: accepted, but for Consent Mode's group, whose switching off turns Consent Mode off instead. `cookieConsent.inactiveGroups` lists them.

### Requirements per vendor

- **Google Analytics:** the app installed and active, a `G-` id, the **Measurement Protocol API secret** ([[apps-google-analytics-settings]]), a visitor id, and consent.
- **TikTok:** the pixel, **Enable Events API** with a token, a visitor id, and consent to `targeting`.
- **Meta:** the Conversions API set up in [[apps-facebook-pixel-settings]], a visitor id, and consent.

### Staff visits

The API has no admin session and cannot tell whose browser is asking. Suppressing tracking for staff is the storefront's concern.

## Related

- [[headless-storefront]] — hub.
- [[headless-checkout-submit]] — the fast order's purchase report.
- [[apps-gdpr-cookies-groups]] — the groups.
- [[apps-google-analytics-settings]] — the Measurement Protocol secret.
- [[apps-facebook-pixel-settings]] — Meta.
- [[apps-tiktok-pixel-settings]] — TikTok.
- [[apps-fast-order-tracking]] — the fast order's event names.

## Open Questions

_None._
