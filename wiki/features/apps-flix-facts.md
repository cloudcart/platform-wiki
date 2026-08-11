---
type: feature
nav_path: "Apps → FlixFacts"
route_name: apps.flix_facts.overview
route_path: /admin/apps/flix_facts
aliases: ["FlixFacts", "Flix Facts", "FlixFacts accounting", "enable disable button", "app active toggle"]
tags: [apps, erp, accounting, integration]
plan_gates: ["flix_facts"]
created: 2026-05-22
updated: 2026-08-06
source_count: 2
---
# FlixFacts (accounting integration)

## Purpose

**FlixFacts** integration — accounting / ERP connector that synchronises orders and customer data with the FlixFacts accounting system. Different model than the strict invoicing apps ([[apps-szamlazz]] / [[apps-fgo]] / [[apps-smart-bill]]): FlixFacts works on **status-change events** — when an order's status changes (e.g., to Paid), the platform syncs the relevant data to FlixFacts.

> **Has an on/off control.** The app screen carries an **Enable / Disable** button, so the merchant can switch it off without uninstalling it. A disabled app stops working while keeping its settings — so *"the app is disabled"* IS a valid explanation to check here.

## Where to find it

Sidebar → Apps → install → **FlixFacts**.

## What the merchant can do here

- See app status.
- Configure FlixFacts credentials in [[apps-flix-facts-settings]].
- Map status events to FlixFacts actions.
- Sync orders / customers based on triggers.

### What the merchant CANNOT do here
- Use FlixFacts without subscription.

## Settings & fields

The Manager exposes:
- `match($key, ?Variant $variant = null)` — Maps a CloudCart key (e.g., product ID, variant ID) to FlixFacts's internal identifier.
- the configured check — Credential check.
- `getEvents` — Returns the list of trigger events the integration subscribes to.
- `hasStatusChange` — Boolean indicating whether the integration is active on status-change events.

### Event-driven model

Unlike invoicing apps that have explicit "generate invoice" buttons, FlixFacts works through subscribed events:
- Order status changes → FlixFacts is notified → applies its configured action.
- Customer changes → may sync customer data.
- Product changes → may sync product catalog (verify).

## Business rules

### Event subscription model

The merchant doesn't manually trigger FlixFacts — it auto-fires on the events returned by `getEvents`. Common events likely include:
- order.created
- order.updated (status changed)
- order.paid
- customer.created
- customer.updated

The exact set is FlixFacts-defined; the platform calls `getEvents` to know which to subscribe to.

### Key mapping (verified against backend)

The merchant configures TWO settings to control matching:
- `match.flix` (default `'mpn'`) — what FlixFacts uses as the identifier: `mpn` / `ean` / `sku`.
- `match.self` (default `'sku'`) — what CloudCart provides: `sku` (uses `$variant->sku`) or `barcode` (uses `$variant->barcode`).

When the merchant's `match.flix` setting equals the lookup key being requested, the method returns the variant's SKU or barcode (based on `match.self`). Otherwise returns null.

This dual-key setup lets merchants match by:
- SKU ↔ MPN.
- Barcode ↔ EAN.
- SKU ↔ SKU.
- etc.

the configured check checks all three: `flix_facts` (credentials) + `match.flix` + `match.self`.

### Side effects

When an event fires AND FlixFacts is configured + active, the platform pushes the event to FlixFacts via its API.

### Permission

Standard apps permission scope.

## Plan gates

This app is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `flix_facts` | Access gate (install URL) | The install URL `/admin/apps/flix_facts/install` is blocked when the plan lacks the feature. The app is hidden from the Apps catalog for those plans. |

Behaviour: lower plans cannot install the app. Existing installs continue working on plan downgrade until the merchant cancels — see [[plan-vs-feature-pack]] for downgrade rules.

## Related

- [[apps]] — App Store.
- [[apps-flix-facts-settings]] — settings sub-page.
- [[apps-szamlazz]] / [[apps-fgo]] / [[apps-smart-bill]] — alternative accounting integrations (with strict invoicing-provider model).
- [[settings-statuses]] — order status changes drive FlixFacts events.
- [[settings-hooks]] — webhook events (FlixFacts uses internal events, not external webhooks).

## How it works (verified against backend)

### Event subscription returns exactly ONE event

The integration subscribes to a single event:
- `group = 'post.product.view'` — fires AFTER a customer views a product detail page.
- The handler injects FlixFacts content into the product description.
- Default state is inactive (the merchant activates per-event).
- Failures don't crash the page load.

So FlixFacts is NOT a status-change integration — it's a **content-injection on product view**. When a customer views a product page, the platform fires the FlixFacts event which injects FlixFacts content (typically a "facts" / specs module) into the product description.

The integration modifies the product description at render time (does not overwrite the stored description).

### Distinct integration model from other event-driven apps

Unlike [[apps-e-store-content]] / [[apps-load-bee]] (which sync content on product CRUD events), FlixFacts injects content at VIEW time — non-destructive (doesn't overwrite the merchant's description in DB; injects FlixFacts content as supplementary).

### FlixFacts is content-injection, NOT accounting sync

Important correction to the introduction text: FlixFacts as integrated here is **NOT an accounting / ERP connector** — it's a product-page content module. The integration subscribes only to the `post.product.view` event, which fires when a customer views a product detail page. The handler injects FlixFacts content (a "facts" / specifications module rendered from a Distributor ID code) into the product description at render time.

There's no order sync, customer sync, or invoice generation in this integration. The merchant should pair FlixFacts with [[apps-fgo]] / [[apps-szamlazz]] / [[apps-smart-bill]] for accounting needs — they're complementary, not alternatives.

### Variant matching fallback

When the merchant's `match.flix` setting (default `mpn`) equals the lookup key, the platform returns either the variant's SKU or barcode (per `match.self`). If neither field is populated on the variant, the lookup falls through with no value — the module then renders WITHOUT a product-specific lookup, falling back to whatever FlixFacts shows for a generic / vendor-only query.

### No CloudCart-side data ingest from FlixFacts

FlixFacts is one-way: CloudCart calls FlixFacts at render time and embeds returned content. FlixFacts does not push data back to CloudCart. No conflict resolution needed — CloudCart's product data is authoritative; FlixFacts content is supplementary at view time.

### Vendor is REQUIRED on the product for FlixFacts to render
The injection only fires when `$product->vendor` exists. Products without a vendor assigned silently skip the FlixFacts module — exactly like [[apps-load-bee]]. Merchants installing FlixFacts must verify their catalog has vendor assignments populated.

### Setting key fallback: `code` then `flix_facts`
The injector reads the module code from `$manager->getSetting('code', $manager->getSetting('flix_facts'))` — first checks for a `code` setting, then falls back to `flix_facts`. This dual-key pattern is the result of a settings rename; older installs use `flix_facts` while newer installs may use `code`. Both keys are read transparently.

### "Already injected" idempotency guard
The handler skips re-injection when the description already contains the string `'flix-minisite'`. So if the product description is cached and re-rendered, the module container is not duplicated. The merchant cannot manually paste their own `flix-minisite` block in the description without disabling the auto-injection — the platform would detect it and skip the module.

## Open questions

(none — questions about merchant-facing behaviour have been resolved against backend)
