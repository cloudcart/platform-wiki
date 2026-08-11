---
type: feature
nav_path: "Sidebar → Services"
route_name: admin.services.list
route_path: /admin/services
aliases: ["Services", "CloudCart services", "Additional services", "Expert services", "Услуги", "Допълнителни услуги", "Експертни услуги"]
tags: [services, billing, catalog, expert-services, paid-services]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 4
---

# Services

## Purpose

This page is the **hub** for the **Services** surface — the catalog of additional **paid services** the merchant can order from CloudCart and its partner network. Services here are distinct from **store plans** (the SaaS subscription tiers, see [[plans]]) and **paid apps** (functional add-ons billed through [[apps]]). Typical catalog content: Design, Migration, Hosting, Platform → System services, and other expert / agency-style add-ons sold by CloudCart's commercial team.

Each service is presented as a checkbox + price line; the merchant ticks one or more services, sees a running total, clicks **Order**, and goes through CloudCart's purchase flow (invoice generation, card-on-file charge via Stripe or Braintree). Some services are one-time payments (`once`); others recur monthly / yearly / 2-yearly and are added as a new row in [[subscriptions]].

The Services surface has been split into 5 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

## Where to find it

- Sidebar → **Services** entry (visible to store owners; staff / moderator roles do not see this menu link).
- URL pattern: `/admin/services` (catalog list). The sub-paths `/admin/services/order/{id}`, `/admin/services/purchase`, `/admin/services/buy` belong to two distinct purchase flows — see [[services-routes]].
- Some in-app flows redirect here to upsell paid services. The most common example is the **Mail boxes** screen: clicking *"Buy more mail boxes"* parks a `service_order` blob in the session and bounces to `/admin/services/purchase` — see [[services-purchase-flow]].

## Sub-pages (in this cluster)

- [[services-catalog]] — the `/admin/services` list view: row UI (checkbox + name + price + period), group categories (Design, Migration, Hosting, Platform → System), running total, footer Order button.
- [[services-purchase-flow]] — the `/admin/services/purchase` confirmation step + `POST /admin/services/buy` Pay Now handler: three preconditions, `service_order` session blob, atomic invoice + charge + activation.
- [[services-routes]] — the `/admin/services/*` route map and the two distinct checkouts: **admin-promo** (`session('promo')`, used by the catalog Order button + single-service link) vs **services-purchase** (`session('service_order')`, used only by upstream in-app flows).
- [[services-billing-cycles]] — `billing_cycle` mapping (`null`/`1`/`12`/`24` → `once`/`month`/`year`/`2years`), source-currency vs displayed currency, VAT computation at invoice time per the merchant's billing country.
- [[services-catalog-controls]] — per-row `cc_gate.services` fields: `public`, `archived`, `sort_order`, `group_id`, `ecosystem`, `tag`; how visibility is gated; why country-limitation records exist but are not enforced.
- [[services-known-gaps]] — catalog country filter not applied, silent FX margin, post-payment activation can fail silently, no self-service refund, no in-app one-off cancel.

## What the merchant can do here

- Browse the catalog (categories curated by CloudCart's commercial team).
- Tick one or many services and see the running total — see [[services-catalog]].
- Click **Order** to start the purchase flow. The next screen shows invoice details + card on file + service summary + Pay Now — see [[services-purchase-flow]].
- Confirm purchase → CloudCart generates an invoice, charges the card on file, emails the invoice PDF, and (for services with an activate callback) switches on the relevant feature.

What the merchant **cannot** do (all detailed on the aspect pages):

- Add their own services to the catalog (curated by CloudCart) — see [[services-catalog-controls]].
- Pay without invoice details on file ([[billing-invoicing]]) or without a card on file ([[billing-cards]]) — see [[services-purchase-flow]].
- Pay with a one-off bank transfer / external method — card-on-file only.
- Refund a purchase self-service, or cancel a one-off after Pay Now — see [[services-known-gaps]].

## Settings & fields

This hub has no merchant-editable settings — it is a catalog browser. The aspect pages own the field-level detail:

- Row UI fields → [[services-catalog]].
- Purchase confirmation fields (invoice block + card block + Pay Now) → [[services-purchase-flow]].
- Per-row data-model fields (`public`, `archived`, `sort_order`, `group_id`, `ecosystem`, `tag`) → [[services-catalog-controls]].
- Billing-cycle labels → [[services-billing-cycles]].

## Business rules — high-level

### Three buckets — services vs apps vs plan-features

These are separate billing surfaces that look similar but are bought on different pages:

- **Store plan** — the SaaS tier. Bought on [[plans]]. One per merchant. Drives most quotas.
- **Plan features / feature packs** — extra-products-pack, extra-storage-pack, extra-admins-pack, etc. Bought on plan-related upsell flows. Stack on top of the plan to raise specific limits.
- **Apps** — functional add-ons. Bought on the [[apps]] surface; each app has its own settings page.
- **Services (this hub)** — paid services like design, migration, hosting, expert hours. Bought here.

All four end up as `SiteSubscription` rows (for recurring ones) and as invoiced charges against the card on file via [[billing-cards]].

### Two parallel checkouts under `/admin/services/*`

The single most-load-bearing rule: there are **two distinct checkouts**, driven by **two distinct session keys**. The catalog's Order button goes through `admin.promo.purchase`; upstream flows go through `/admin/services/purchase`. Full matrix on [[services-routes]].

### Recurring vs one-off — same Pay Now button, different post-purchase

Recurring services (`billing_cycle = 1`/`12`/`24`) join [[subscriptions]] and can be cancelled there. One-offs (`billing_cycle = null`) do NOT — they have no in-app cancel UI. Full mapping on [[services-billing-cycles]]; gap details on [[services-known-gaps]].

### Country filter NOT applied on the catalog

Catalog query fetches all `public = 1, archived = 0` services and does NOT call `filterByInvoicingCountry`. The apps catalog does. See [[services-known-gaps]].

## Related

- [[services-catalog]] — list view aspect.
- [[services-purchase-flow]] — purchase confirmation + Pay Now aspect.
- [[services-routes]] — route map + the two parallel checkouts.
- [[services-billing-cycles]] — `once` / `month` / `year` / `2years` + VAT + currency.
- [[services-catalog-controls]] — per-row catalog fields.
- [[services-known-gaps]] — gaps and support-only paths.
- [[plans]] — separate billing surface for the SaaS tier.
- [[apps]] — separate billing surface for functional add-ons; closest neighbour.
- [[subscriptions]] — where recurring services appear after purchase.
- [[billing-invoicing]] — required precondition for Pay Now.
- [[billing-cards]] — required precondition for Pay Now.
- [[expired-subscription]] — what happens to a recurring service when the card later fails.
- [[orders-invoices]] — storefront-side invoicing (distinct from CloudCart billing invoices).

## Open questions

None — distributed to aspect pages.
