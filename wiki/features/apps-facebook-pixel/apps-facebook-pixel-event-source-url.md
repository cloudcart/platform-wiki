---
type: feature
nav_path: "Apps → XML Feed → Facebook → event_source_url bug"
route_name: apps.facebook.overview
route_path: /admin/apps/xml_feed/facebook
aliases: ["Facebook event_source_url", "Meta event_source_url warning", "Facebook CAPI events blocked", "Facebook event_source_url bug"]
tags: [apps, facebook, meta, capi, bug, known-issue, tracking]
plan_gates: ["facebook.capi"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[apps-facebook-pixel]]. See the hub for the other aspects (event vocabulary, CAPI gating) and the settings tab.

# Facebook Pixel — `event_source_url` known bug

## Purpose

This aspect documents a **CRITICAL known bug** (BUG, 2026-06-08): CloudCart's storefront does not supply a valid `event_source_url` for several CAPI events, and Meta has warned merchants that events without it will be **blocked**. This is the page support agents should land on when a merchant reports a Meta `event_source_url` warning or a sudden drop in CAPI events.

## Where to find it

There is no admin screen for this — the bug is in CloudCart's storefront JS + CAPI controller, not in any merchant-editable setting. The merchant first sees it as a warning email from Meta (text below) or as missing events in Meta Events Manager.

## What the merchant can do here

- Recognise the symptom (Meta `event_source_url` warning email; events dropping in Events Manager).
- Confirm with support that this is the known platform bug, not a settings error.

### What the merchant CANNOT do here

- **There is no merchant-side workaround.** The Pixel ID, Access Token, and CAPI toggle on [[apps-facebook-pixel-settings]] are all working — the missing URL is produced by CloudCart's storefront, not by the merchant's settings. The fix must ship in CloudCart's storefront JS + CAPI controller.

## Settings & fields

None — this aspect is a known-issue record, not a configurable surface. The affected settings page is [[apps-facebook-pixel-settings]].

## Business rules

### Meta warning received by merchant on 2026-06-08

> "You or your developer should add the `event_source_url` parameter to events sent through Conversions API before the events are blocked. It usually takes about three days for us to receive updated information."

### What's happening

The CAPI controller DOES set `event_source_url` when the storefront JS sends a `url` field in the AJAX request body. However, the storefront JS only supplies `url` for SOME event types:

| Event | `url` sent to CAPI? | Value sent | Result |
|---|---|---|---|
| `PageView` | YES | `document.location.href` (full absolute URL) | OK |
| `ViewContent` (product) | YES | `data.url` (full product URL) | OK |
| `ViewContent` (product_group / category) | YES | `data.url` (full category URL) | OK |
| `InitiateCheckout` / `InitiateFastCheckout` | YES, but WRONG | `window.ccRoutes.checkout` — a **relative path** like `/checkout`, NOT a full URL with `https://shop.example.com/` | Meta likely rejects (verify) |
| `Purchase` / `FastPurchase` | YES, but WRONG | `window.ccRoutes.checkout` — same relative path | Meta likely rejects (verify) |
| `AddToCart` | **NO** — field omitted | (none — `event_source_url` is `null`) | Meta WILL BLOCK |
| `AddToWishlist` | **NO** — field omitted | (none) | Meta WILL BLOCK |
| `Search` | **NO** — field omitted | (none) | Meta WILL BLOCK |

This is a BUG — not by-design. Meta's CAPI documentation has `event_source_url` as required for the `website` action source, and Meta has begun warning merchants that events without it will be dropped in ~3 days from the warning's date.

### Support-agent guidance

If a merchant reports:

- A Meta warning email about `event_source_url`,
- Or their FB CAPI events suddenly stopped being received in Meta Events Manager,
- Or Meta Events Manager shows "low event match quality" or "events being dropped"

→ Escalate to **engineering** with reference to this wiki page. The fix is backend + storefront JS:

1. **Storefront JS** — every event builder must include the current page URL (`window.location.href`) in the formatted payload before sending. Currently missing in the `AddToCart`, `AddToWishlist`, and storefront-search builders.
2. **Storefront JS** — `InitiateCheckout` and `Purchase` currently send only the relative `/checkout` path. They should send the full absolute URL (the actual checkout-page URL the customer is on).
3. **Backend safety net** — in the CAPI controller's event-fire path, if the supplied `url` is empty OR is not a fully-qualified URL, fall back to the request's `referer` header (which the browser sends automatically and is always the page the AJAX was triggered from). That gives every event a sensible `event_source_url` without depending on the storefront JS being updated first.

### Workaround for affected merchants (none — must wait for fix)

There is **no merchant-side workaround**. The Pixel ID, Access Token, and CAPI toggle are all working — the missing URL is being produced by CloudCart's storefront, not by the merchant's settings. Merchants cannot fix this from Apps → XML Feed → Facebook settings. The fix must ship in CloudCart's storefront JS + CAPI controller.

### Impact if not fixed

Per Meta's 2026-06 warning text — ~3 days from the warning date, events without `event_source_url` get **blocked** (not just dropped from match quality scoring). For affected merchants this means:

- `AddToCart` / `AddToWishlist` / `Search` conversion events stop reaching Meta entirely → ad audiences (cart-abandon retargeting) lose data.
- `InitiateCheckout` / `Purchase` may or may not be blocked depending on whether Meta treats the relative `/checkout` path as a valid URL (verify).
- Browser pixel (`fbq`) leg is unaffected — only the CAPI leg ([[apps-facebook-pixel-capi]]) is at risk. But Meta's iOS-14+ attribution loss means the browser pixel alone is significantly less accurate.

### Permission

Standard apps permission scope. CAPI access requires plan feature `facebook.capi`.

## Related

- [[apps-facebook-pixel]] — hub.
- [[apps-facebook-pixel-capi]] — the server-side leg where `event_source_url` is set on the payload.
- [[apps-facebook-pixel-events]] — the event vocabulary; `AddToCart` / `AddToWishlist` / `Search` are the affected events.
- [[apps-facebook-pixel-settings]] — the settings page merchants wrongly suspect (not the cause).
- [[plan-features]] — `facebook.capi` plan feature gate.

## Open questions

- **`event_source_url` engineering fix ETA** (CRITICAL, 2026-06-08) — when will the storefront JS + backend safety-net land? Track engineering ticket.
- **(verify)** Does Meta reject the relative-path `/checkout` value for `InitiateCheckout` and `Purchase`, or does it accept it and silently degrade match quality? The Meta warning text mentions blocking but doesn't enumerate which event types are at risk.
