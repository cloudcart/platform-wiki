---
type: feature
nav_path: "Sidebar → Services → Routes & entry points"
route_name: admin.services.list
route_path: /admin/services
aliases: ["Services routes", "Services entry points", "admin.services.order", "admin.services.purchase", "admin.services.buy"]
tags: [services, routes, navigation, admin-promo]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[services]]. See the hub for related aspects (catalog, purchase flow, billing cycles, catalog controls, known gaps).

# Services — routes & entry points

## Purpose

This page maps the **three URL pairs** under `/admin/services/*` and the **three distinct entry-point paths** that lead to a service being charged. The single most-misstated rule on this surface is that the catalog's Order button and the `/admin/services/purchase` confirmation step do **NOT** share a session key and do **NOT** share a checkout route — they belong to different flows.

## Where to find it

This is the navigation / routing reference for the screens documented in [[services-catalog]] and [[services-purchase-flow]]. The merchant does not see "Routes" as a menu — this page is the LLM's lookup for "which URL does what".

## What the merchant can do here

Nothing directly — this is the routing reference. The merchant interacts via the screens those routes back. The three entry-point paths are:

1. **Direct browse from the catalog** — sidebar → Services → tick services → Order.
2. **Single-service catalog link** — clicking the inline `Order` link on an individual service row at `/admin/services/order/{id}`.
3. **In-app upstream redirect** — flows like mailbox creation that bypass the catalog entirely.

## Settings & fields

The route map under `/admin/services/*`:

| Route | Method | Route name | What it does |
|-------|--------|------------|--------------|
| `/admin/services` | GET | `admin.services.list` | Renders the catalog list — see [[services-catalog]]. The catalog's Order button POSTs `service[]` to `admin.promo.services`, NOT to a `/admin/services/*` endpoint. |
| `/admin/services/order/{id}` | GET | `admin.services.order` | Single-service catalog link. Seeds `session('promo') = ['service' => [id]]` and a `googleProducts` flash, then redirects to `admin.promo.purchase` (the shared admin-promo checkout). Does NOT set `service_order` and does NOT go to `/admin/services/purchase`. |
| `/admin/services/purchase` | GET | `admin.services.purchase` | Purchase confirmation page. Requires a `service_order` session blob with an `id` set by an upstream flow (NOT by the catalog's `order/{id}` link). Empty blob → redirect back. See [[services-purchase-flow]]. |
| `/admin/services/buy` | POST | `admin.services.buy` | Pay Now POST endpoint. Requires the `service_order` session blob. Issues invoice + charges card + runs activate callback. See [[services-purchase-flow]]. |

## Business rules

### Two parallel checkouts: admin-promo vs services-purchase

The single most-load-bearing rule on this surface: there are **two separate checkouts** under `/admin/services/*`, driven by **two separate session keys**.

| Checkout | Session key | Entry points | Confirmation route | Pay route |
|----------|-------------|--------------|--------------------|-----------|
| **Admin-promo flow** | `session('promo')` | Catalog Order button (multi-service) + single-service catalog link `/admin/services/order/{id}` | `admin.promo.purchase` | `admin.promo.buy` |
| **Services-purchase flow** | `session('service_order')` | Upstream in-app flows (paid mailboxes, etc.) — never the catalog itself | `/admin/services/purchase` | `/admin/services/buy` |

The two flows look similar but they are NOT interchangeable. Clicking Order on the catalog will NEVER hit `/admin/services/purchase` — it goes through `admin.promo.purchase`. Conversely, an upstream flow that parks `service_order` will NEVER hit `admin.promo.purchase` — it goes through `/admin/services/purchase`.

### Catalog Order button POSTs to `admin.promo.services`

The catalog's `<form id="serviceForm">` POSTs ticked `service[]` checkboxes to **`admin.promo.services`** (the shared admin-promo checkout). Multi-service ticks all go through this one POST. The merchant sees the admin-promo confirmation screen, not the services-purchase confirmation screen.

### `/admin/services/order/{id}` is single-service, still admin-promo

The single-service catalog link (the per-row inline `Order` link) handler:

1. Loads the service by ID.
2. Puts `session('promo') = ['service' => [<service_id>]]` and flashes `googleProducts`.
3. Redirects to `admin.promo.purchase`.

So this catalog link routes into the admin-promo flow as well. It does NOT set `service_order` and does NOT go to `/admin/services/purchase`.

### Upstream flows park `service_order` directly

The `service_order`-driven `/admin/services/purchase` + `/admin/services/buy` pair is used only by upstream flows (e.g. paid mailboxes), which:

1. Set `service_order` in the session — service ID + optional `activate` callback + optional `redirect`.
2. Bounce the merchant to `/admin/services/purchase` (skipping the catalog list).
3. After Pay Now succeeds, the post-purchase redirect uses the session's `redirect` URL.

The full mechanics of the `service_order` blob and Pay Now handler are documented on [[services-purchase-flow]].

### Why direct URL hits bounce back

`/admin/services/purchase` and `/admin/services/buy` cannot be opened by typing the URL — the controller's middleware requires `service_order['id']` to be present and redirects back when it is empty. This is intentional: those routes are NOT a public entry point; they are the back-half of an upstream flow.

## How it works (verified against backend)

### Mailbox-purchase example (upstream flow)

The most common example of the upstream path is the **Mail boxes** screen: clicking *"Buy more mail boxes"* on a mailbox add / edit form parks a `service_order` in the session (with the mailbox service ID + an `activate` callback that switches the box on after payment + a `redirect` back to the mailbox list) and bounces the merchant to `/admin/services/purchase`. After Pay Now, the activate callback runs and the merchant is sent back to the mailbox list — see [[services-purchase-flow]] for the full Pay Now mechanics.

## Related

- [[services]] — hub.
- [[services-catalog]] — list view; where the Order button + `order/{id}` single-service link live.
- [[services-purchase-flow]] — the `service_order`-driven confirmation + Pay Now mechanics.
- [[services-billing-cycles]] — what `SiteSubscription` records the Pay routes create.
- [[services-known-gaps]] — gaps in the route-level guard rails.
- [[billing-invoicing]] / [[billing-cards]] — preconditions enforced at the Pay step.

## Open questions

- Confirm the exact serialised shape of `session('promo')` for the admin-promo flow `(verify)`.
