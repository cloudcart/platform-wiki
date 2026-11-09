---
type: concept
nav_path: "Concept → Storefront architecture → Root files, web manifest and service worker"
aliases: ["PWA", "Progressive web app", "Install as app", "Add to Home Screen", "manifest.json", "Web app manifest", "Service worker", "cc-sw.js", "sw.js", "Root files", ".well-known", "assetlinks.json", "apple-app-site-association", "Файл в root директорията", "Инсталиране като приложение"]
tags: [storefront, pwa, manifest, service-worker, root-files, well-known, concepts]
plan_gates: []
created: 2026-11-09
updated: 2026-11-09
source_count: 1
---

> Part of [[storefront-architecture]]. See the hub for related aspects (request lifecycle, JS bundles, CSS assets, caching).

# Storefront — root files, web manifest and service worker

## Definition

A store on a standard theme answers a fixed set of addresses at the root of its domain. The merchant edits two of them as text and cannot upload any other file there. The storefront is not set up as an installable web app (PWA): its pages link no web app manifest, and the platform's only service worker handles Web Push messages.

## Scope

Covered: the root addresses a store answers, the web manifest, the service worker, "install as app", offline use, and the same addresses on a Nitrogen domain.

Not covered: the store's own Mobile app, a separate product outside this page. Safari's rules for Web Push are on [[webpush-channel-browser-support]].

## Contrasts

- **Root file vs uploaded file** — files uploaded to the admin's file storage are served from CloudCart's storage address (`…/<store id>/files/…`), not from the store's domain. They can never stand in for a file a third party expects at `https://<store>/<file>` or under `/.well-known/`.
- **The platform `/manifest.json` vs a web app manifest** — the address answers on every store, but it is one fixed platform file holding only a push sender ID: no name, icons, start address, colours or display mode. No storefront page links to it, and no admin setting changes it.

## Where it applies

### What a store serves at its root

| Address | What it is | Merchant control |
|---|---|---|
| `/robots.txt` | Crawler rules — [[marketing-seo-robots]] | Editable text |
| `/llms.txt` | Summary for AI crawlers — [[marketing-seo-llms]] | Editable text |
| `/favicon.ico` | The store's favicon, else the platform's | The favicon card on [[settings-brand]] |
| `/meta.json` | Store name, domain, language, currency, logo | None |
| `/manifest.json` | Fixed platform file (push sender ID only) | None |
| `/cc-sw.js`, the OneSignal and Firebase worker files | Platform push service workers | None |
| `/.well-known/apple-developer-merchantid-domain-association` | Apple Pay domain file for CloudCart Pay | None |
| `/.well-known/acme-challenge/…` | Certificate checks — [[settings-domains-ssl]] | None |

Any other root path — `/.well-known/assetlinks.json`, `/.well-known/apple-app-site-association`, a merchant's `sw.js` — has no page and ends in the store's 404. A [[marketing-seo-301-redirects|301 rule]] can send a path with no page elsewhere; whether Google's Digital Asset Links check or Apple's app-site-association check accepts a redirect is decided by Google and Apple, not by CloudCart.

### The service worker

The platform registers `/cc-sw.js` only from its Web Push script. That script loads when the Web Push channel is set up ([[marketing-channels-webpush]]) and the visitor is not signed in to the admin, and registers the worker only while the visitor has neither allowed nor blocked notifications nor dismissed the prompt. The worker shows push messages, reports their delivery and clicks, and opens the message's link. It caches no pages, so the storefront has **no offline mode**.

Merchant code cannot add a service worker of its own: a browser accepts a service worker only from the store's own domain, and no merchant file can be placed there.

### Install as app

- The storefront sets no install prompt, "Add to Home Screen" hint, app icon, theme colour or splash screen, and the admin offers no setting for them. Theme pages carry no Apple web-app tags.
- A shopper can still add the store to the Home Screen from the browser's own menu. What the device then shows (icon, title, full screen or not, splash) is the browser maker's behaviour, not a CloudCart setting.

### On a Nitrogen domain

A domain routed to a [[headless-storefront|Nitrogen storefront]] keeps sending `/robots.txt`, `/llms.txt`, `/cc-sw.js`, the OneSignal and Firebase worker files and every `/.well-known/` address to the platform. Other root paths, `/manifest.json` included, go to the Nitrogen app, so a manifest or a service worker there is up to that storefront's own code (verify what the starter ships). A Nitrogen app cannot answer under `/.well-known/` itself.

## Related

- [[storefront-architecture]] — hub.
- [[webpush-channel-browser-support]] — Safari offers Web Push only to a store opened from the Home Screen or Dock.
- [[marketing-channels-webpush]] — the channel whose script registers the service worker.
- [[marketing-seo-robots]] — the editable `/robots.txt`.
- [[marketing-seo-llms]] — the editable `/llms.txt`.
- [[marketing-seo-301-redirects]] — redirect rules for paths without a page.
- [[headless-storefront]] — the Nitrogen storefront.

## Open Questions

- Whether the 301 rule editor accepts a `/.well-known/` path, and whether such a request reaches the store's redirect lookup (verify).
