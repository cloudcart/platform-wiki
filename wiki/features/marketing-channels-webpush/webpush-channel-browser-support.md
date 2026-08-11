---
type: feature
nav_path: "Marketing → Channels → Channels setup → Web Push → Browser support"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Web Push browser support", "Web Push Safari", "Web Push iOS", "PWA Web Push", "Web Push compatibility", "In-app browser Web Push", "Уеб пуш съвместимост", "Web push PWA Safari"]
tags: [marketing, channels, web-push, browser-support, pwa, safari, ios, compatibility]
plan_gates: ["campaign.channel.web_push"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[marketing-channels-webpush]]. See the hub for the other aspects (storefront prompt, subscription flow, VAPID config, send pipeline, DLR webhook, system messages).

# Web Push channel — Browser support and PWA requirements

## Purpose

Web Push is a browser-vendor feature, not a CloudCart feature — which means the reachable audience depends on which browser + OS the customer is using. A non-trivial slice of mobile customers (older iOS users, anyone browsing inside an in-app browser like the Instagram or Facebook in-app webview) is simply **unreachable** via Web Push. This page documents the support matrix so the merchant can plan their channel mix (when to fall back to SMS / Viber / Email for unreachable segments).

## Where to find it

There is no admin UI for this — it's a browser / OS capability question. The merchant's awareness of these limits drives:

- Their decision about whether Web Push is worth enabling at all.
- Their **multi-channel strategy** — e.g. send Web Push first, fall back to Email for non-WebPush subscribers.
- Their **PWA enablement** — for Safari coverage, the storefront must be installed as a PWA.

## What the merchant can do here

- Choose whether to enable the channel based on their customer mix.
- Customise the storefront's PWA manifest (icon, name, theme color) via the storefront design system, which improves Safari subscription rates.
- Use [[marketing-campaigns]] step-conditions to fall back to SMS / Viber / Email when a customer doesn't have a Web Push channel row.

## Settings & fields

### Browser-support matrix

| Browser | Support | Notes |
|---|---|---|
| Chrome / Edge / Opera | Full | Via FCM (Google's push service). |
| Firefox | Full | Via Mozilla Autopush. |
| Safari (macOS) | Limited | Web Push for Safari 16.1+ requires the storefront to be installed as a Web App (added to the Dock). Safari does **NOT** support browser-tab push notifications outside of Web Apps. |
| Safari (iOS) | Yes (iOS 16.4+) | The storefront must be added to the Home Screen as a PWA first. Push then works through APNs (Apple Push Notification service). Older iOS versions don't support Web Push at all. |
| In-app browsers (Instagram, Facebook, TikTok webviews) | None | Customers browsing inside these embedded webviews cannot subscribe — the in-app browsers don't expose the Push API. |

### PWA requirements for Safari coverage

For Safari (macOS or iOS) to support Web Push, the storefront must be installed as a PWA. The PWA requirements are:

- A proper `manifest.json`.
- A registered service worker.
- HTTPS (already mandatory on CloudCart storefronts).
- An "Add to Home Screen" / "Add to Dock" UX hint shown to the customer.

CloudCart's storefronts ship with PWA manifests by default. The merchant can customise the manifest icon, name, and theme color through the storefront design system.

## Business rules

### Web Push is not a universal-reach channel

A non-trivial slice of mobile customers is unreachable via Web Push — older iOS, in-app-browser users, customers on browsers without push support, and customers who DENIED the prompt. The merchant must accept Web Push as an **acquisition + retention bonus** on a subset of customers, not as a replacement for SMS / Viber / Email reach.

Realistic opt-in rate: **5-15%** of storefront visitors accept the prompt. The other 85-95% never become WebPush-reachable on that browser, even if they're loyal customers.

### Safari requires the PWA path — and the customer must Add to Home Screen

A customer browsing the storefront in Safari (macOS or iOS) **cannot** subscribe to Web Push from the regular browser-tab view. They must first add the storefront to their Home Screen (iOS) or Dock (macOS Safari 16.1+), then open the storefront as a Web App, then accept the prompt. This is two extra friction steps versus Chrome / Firefox, where the prompt fires on any normal page load.

The implication: Safari-heavy merchant audiences (heavily iOS, e.g. premium / fashion / Bulgaria-affluent demographics) need to actively promote PWA install (custom UX nudge, "Add to Home Screen" banner) — otherwise their WebPush subscriber base will lean heavily Chrome-on-Android.

### In-app browser users never see the prompt

A customer who clicks the merchant's Instagram ad and lands on the storefront inside Instagram's in-app browser **cannot** subscribe to Web Push — the Push API isn't available in that environment. They must open the storefront in their device's normal browser first (which they often won't).

This is a tax on social-media-traffic-heavy merchants: a meaningful share of "first touch" sessions never get the chance to opt in.

### iOS 16.4+ vs older iOS

iOS 16.4 (released March 2023) was the first iOS version to support Web Push at all — and only via the PWA path. Customers on iOS 15 or earlier cannot subscribe at all. As of 2026, this excludes a small but non-zero share of iPhones (older devices that can't update past iOS 15).

### Falling back via campaign step-conditions

For customers without a WebPush channel row, the merchant's campaign should fall back to another channel. Pattern:

1. Step 1: Send Web Push if WebPush channel exists.
2. Step 2: Conditional — if Step 1 was `link_not_clicked` (or if no WebPush channel exists at all), send Email / SMS / Viber.

This requires the merchant to model the campaign with multi-channel awareness — Web Push alone is not enough.

### Native browser prompt is one-shot per user — re-prompt is not possible

Once a customer DENIES the native browser permission prompt, browsers (Chrome, Firefox, Safari) will NOT show it again until the user manually resets the permission in browser settings. This is a hard browser-vendor limit — CloudCart cannot work around it.

The [[webpush-channel-storefront-prompt|two-stage popup design]] exists specifically to preserve the merchant's ability to re-prompt: the CloudCart popup can be dismissed without burning the native prompt, so the merchant gets multiple chances to convert.

## Related

- [[marketing-channels-webpush]] — hub.
- [[webpush-channel-storefront-prompt]] — the popup → native-prompt UX whose conversion is gated by these browser-support constraints.
- [[webpush-channel-subscription-flow]] — what happens when the browser does support push and the customer does accept the prompt.
- [[marketing-campaigns]] — multi-channel campaigns that fall back to SMS / Viber / Email for unreachable customers.
- [[marketing-channels-sms-nth]] — fallback channel for unreachable customers.
- [[marketing-channels-viber]] — fallback channel for Bulgarian-heavy audiences.
- [[marketing-channels-email]] — universal fallback channel.

## Open questions

- ⏸️ Exact share of Bulgarian customers on iOS 16.4+ vs older iOS — would inform whether the PWA-install push is worth the friction for any given merchant.
- ⏸️ Whether the CloudCart storefront's default PWA manifest already triggers the "Add to Home Screen" UX hint on iOS Safari, or whether the merchant must add it via a theme customisation.
