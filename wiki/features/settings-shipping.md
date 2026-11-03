---
type: feature
nav_path: "Settings → Shipping"
route_name: admin.shippingProviders
route_path: /admin/shipping
aliases: ["Shipping", "Shipping methods", "Shipping providers", "Shipping settings", "Доставка", "Методи на доставка", "Куриери", "Настройки на доставка"]
tags: [settings, shipping, providers, geo-zones, integrations]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 7
---
# Shipping

## Purpose

The merchant's **shipping methods hub** — a single screen listing every shipping option the store offers at checkout, whether from an integration (DHL, Speedy, Econt, GLS, DPD, Fan Courier, Cargus, etc.) or a **Custom** rate the merchant configured (price-based, weight-based, price-and-weight, or local pickup). Each row shows logo, name, pricing model, geographic regions, an active/inactive toggle, and edit / delete actions.

The header **+ Add shipping method** opens a *"Create new shipping method"* slide-in with two sections: **Browse shipping integrations** (third-party carrier apps filtered by the store's operation country) and **Custom** (Based on price, Based on weight, Based on price and weight, Local Pickup).

This page is the **central setup point** for storefront shipping. Defaults — which method auto-selects at checkout, which appears when only one is available — live on a **separate** page; see [[settings-cart]].

## Where to find it

Sidebar → Settings → **Shipping**.

Breadcrumb reads "Settings → Shipping". Header icon is the shipping truck. Page title is "Shipping methods".

## Sub-pages (in this cluster)

Drill into the aspect that matches the question, not every page.

- [[settings-shipping-list-and-add]] — table columns, the **+ View more Shipping methods** link to `apps.all?category=4`, and the *"Create new shipping method"* slide-in.
- [[settings-shipping-custom-rates]] — the four Custom **type** cards, the type-is-permanent rule, the free-shipping `amount = 0` pattern, the "Different price for categories" split, and the **Recommended** badge logic.
- [[settings-shipping-edit-panel]] — the Custom rate-config slide-in: every field with verbatim setting keys, the rate-bracket auto-fill quirk, and N18 Audit / marketplace conditional sections.
- [[settings-shipping-rate-matching]] — the deterministic rate-matcher, **cheapest matching rate wins on overlap**, and the four-gate storefront-visibility cascade.
- [[settings-shipping-lifecycle]] — activation + delete side-effects: the *"Shipping method is not configured…"* activation guard, delete protection when orders are attached, and the delete cascade.
- [[settings-shipping-api-and-permissions]] — read-only API access via [[api-shipping-providers]], the `settings.shipping` and `store.shipping` permission grants, and the Geo Zone deletion fallback.

## What the merchant can do here

- See every configured shipping method (integration-backed + Custom) in one table.
- Toggle a method's per-row **Show in store** flag — persists immediately, no save button.
- Click **+ Add shipping method** to browse installable integrations (filtered by the operation country in [[settings-general]]) or create a Custom rate.
- Click a row name to edit: integration-backed → opens the integration's app settings page; Custom → opens the rate-config side panel.
- Delete a method via the trash-can icon (blocked if orders are attached).
- Click **+ View more Shipping methods** below the table to jump to the [[apps]] catalog filtered by `apps.all?category=4`.

What the merchant **cannot** do here:

- Set a store-wide free-shipping threshold as a single setting (use an `amount = 0` rate row on a Custom Based-on-price method — see [[settings-shipping-custom-rates]]).
- Pick the **default carrier** (lives on [[settings-cart]]).
- Configure fallback rules between carriers (no fallback UI exists).
- Bulk-import / bulk-export shipping methods, or reorder methods at checkout (order is database insertion order — see [[settings-shipping-rate-matching]]).
- Change a method's **type** after creation (delete + recreate is the workaround).

## Settings & fields

Top-level fields surfaced on this hub. Per-method edit fields with verbatim setting keys live on [[settings-shipping-edit-panel]].

### List columns

| Column | What it shows |
|--------|---------------|
| **Name** | Logo + name. **Recommended** badge if tagged. Parameters line: type + scope (e.g., *"Price based to address"*, *"Weight based to office"*, *"Local Pickup"*). |
| **Delivery time** | Only when the [[apps-shipping-hours-settings|Shipping Hours]] app is installed. |
| **Deliver to** | *"Global"* / *"Regions are determined by the provider"* / a specific [[settings-geo-zones]] name. When the zone has multiple conditions, shows `<first condition> and {N} other conditions`. |
| **Show in store** | Per-row active toggle. Maps to the method's `active` boolean; reflects on the storefront immediately, no cache delay (see [[settings-shipping-lifecycle]]). |
| _(actions)_ | Trash-can icon (delete). |

### Add modal Custom type keys

| Card | `type` key |
|------|-----------|
| Based on price | `price` |
| Based on weight | `weight` |
| Based on price and weight | `price_and_weight` |
| Local Pickup | `marketplace` |

## Business rules

Cluster-wide rules. Aspect-specific rules (rate matching, lifecycle cascades, permission grants) live on their respective sub-pages.

### Each method has one geographic scope

A method has exactly one scope: **The whole world** (`provider[target] = restofworld`) OR **A specific Geo Zone** (`target = regions` with `geo_zone_id` set). For different rates in different regions, create two separate methods — there is no per-zone rate split inside a single method.

### Integrations vs Custom — different config surfaces

- **Integration-backed methods** (Speedy, Econt, DHL, GLS, DPD, Fan Courier, Cargus, etc.): configured through each app's own settings page; rates come from the integration's pricing rules / live API. The merchant cannot edit individual rate rows from this list.
- **Custom methods**: rate rows, zones, and payment allow-lists edited directly through the Custom config panel (see [[settings-shipping-edit-panel]]).

The "Deliver to" column reflects this — integrations show *"Regions are determined by the provider"*; Custom methods show their zone name.

### Country-default recommendations

The platform tags methods as **Recommended** based on the store's operation country in [[settings-general]]. The "Browse shipping integrations" modal also filters its app list by that country (Bulgarian store → Econt / Speedy / Bulgarian Posts; Romanian store → Fan Courier / Cargus / DPD Romania). The merchant cannot override this filter from the list.

### Defaults live in Settings → Cart and checkout

[[settings-cart]] owns the **Default shipping type**, **Default shipping provider**, **Automatically select shipping if only one is available**, and **Ask for shipping address for digital products** toggles. None are configured on this list.

### Cash-on-delivery sync per integration

For integrations that support cash-on-delivery (Econt, Speedy, etc.), the *"Automatically set order status to paid when we get information from shipping provider with Cash on delivery"* toggle lives on each integration's settings page — not on this list.

## Related

- [[checkout-step-shipping]] — storefront-side shipping channel picker (address / office / locker / marketplace).
- [[checkout-step-shipping-method]] — storefront-side method picker (provider × service).

- [[shipping-calc-rate-models]] — rate-table semantics: when a method uses a from/to rate table (по тегло / по цена), an **empty upper bound (`до` / `to`) means no upper limit — the bracket runs to infinity** (both bounds inclusive). A blank top row is intended, not invalid, and never hides the method at checkout.
- [[settings]] — parent hub.
- [[settings-cart]] — DEFAULT shipping type / provider / "auto-select if only one" toggles live here.
- [[settings-geo-zones]] — region definitions used by the **Deliver to** column for Custom methods.
- [[settings-geo-distances]] / [[geo-polygons-settings-main-new]] — advanced geo-zone configs.
- [[settings-payment-providers]] — payment methods paired with each shipping method via the allowed-payments multi-select.
- [[settings-statuses]] — shipping status definitions referenced by integration syncing.
- [[settings-boxes]] — delivery box configurations used by some integrations for cubage calculation.
- [[settings-general]] — operation country that filters the integrations list.
- [[settings-staff]] — moderator permission grants for Shipping.
- [[apps]] — the apps catalog (the **+ View more Shipping methods** link sends the merchant here).
- [[apps-shipping-hours-settings]] — adds the "Delivery time" column to this list.
- [[apps-stores]] — required for the Local Pickup card to appear.
- [[apps-n18-audit]] — adds the postal money order switch to the edit panel.
- [[api-shipping-providers]] — JSON-API v2 read-only endpoint.
- [[json-api-v2]] — auth, rate limit, side-effects principle.
- [[checkout-flow]] — how the shipping config shows up at the customer's checkout step.
- [[shipping-calculation]] — the full shipping-quote computation model (rate matching, cascade, geo-gating, COD surcharge).
- [[shipping-provider-mechanism]] — the courier-integration model behind each method (config, pricing, pickup points, waybill, COD, status tracking).
- [[order]] — orders carry references to the chosen shipping method.

## Open questions

_None._
