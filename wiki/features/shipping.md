---
type: feature
nav_path: "Settings → Shipping → Courier integrations (directory)"
route_name: admin.shippingProviders
route_path: /admin/shipping
aliases: ["Shipping", "Couriers", "Courier integrations", "Shipping providers", "Delivery providers", "Куриери", "Доставчици на доставка", "Куриерски интеграции", "Доставка с куриер"]
tags: [shipping, couriers, providers, directory, hub]
plan_gates: []
created: 2026-05-21
updated: 2026-06-11
source_count: 1
---
# Shipping — courier integrations directory

## Purpose

This page is the **directory of every courier integration** CloudCart supports, so the merchant (or the support Assistant) can jump straight to the right courier's app page. The **Shipping screen itself** — where couriers are enabled, priced per channel, and gated by geo zone — is documented at [[settings-shipping]] (the canonical Settings → Shipping screen). Use this page to *find* a courier; use [[settings-shipping]] to *configure* one.

Most couriers run on CloudCart's shared shipping engine (OmniShip): the merchant connects credentials, picks the delivery channels (address / office / locker), chooses a pricing model, and enables cash-on-delivery — see each courier page for its specifics.

## Where to find it

Sidebar → **Settings → Shipping** (`/admin/shipping`). Add a courier from **+ View more Shipping methods** (the App Store, Shipping category) → install → open its settings. Each courier is also listed in the [[apps]] App Store catalog.

## What the merchant can do here

- Browse the supported couriers below and open the one they need.
- Enable / configure a courier on [[settings-shipping]] (credentials, channels, pricing, geo zones, COD).
- See which couriers are deprecated, locker-only, aggregators, or country-specific before choosing.

## Settings & fields

This is a directory — it has no settings of its own. All shipping configuration lives on [[settings-shipping]] and its sub-pages (custom rates, rate matching, edit panel, lifecycle, API & permissions).

### Bulgaria

- [[apps-econt]] — Econt Express; the dominant BG courier (address / office / Econtomat). Richest integration.
- [[apps-dpdbulgaria-speedy]] — DPD Bulgaria (Geopost network).
- [[apps-pigeonexpress]] — Pigeon Express (address / office / locker).
- [[apps-nextlevel]] — Next Level Delivery (address / office / locker, COD + insurance).
- [[apps-dpdbulgaria-speedy|Speedy]] — Speedy — **discontinued by CloudCart support** (existing merchants only; new stores → DPD Bulgaria).
- [[apps-rapido]] — Rapido — **discontinued** (→ DPD Bulgaria).

### Romania

- [[apps-sameday]] — Sameday; Romania's dominant courier (also serves BG).
- [[apps-cargus]] — Urgent Cargus.
- [[apps-dpdromania]] — DPD Romania.
- [[apps-fancourier]] — FanCourier.

### Greece & Cyprus

- [[apps-acscourier]] — ACS Courier; largest private GR courier, strong Cyprus presence.
- [[apps-speedex]] — Speedex (Greek).
- [[apps-ultracep]] — Ultracep (Greek).
- [[apps-tcscourier]] — TCS Courier (Greek).

### Western Balkans & Adriatic

- [[apps-dexpress]] — D-Express (Serbia).
- [[apps-elslogistic]] — ELS Logistic (North Macedonia).
- [[apps-mikmik]] — MikMik (Kosovo / Albania / North Macedonia).
- [[apps-ntclogistics]] — NTC Logistics (Montenegro).
- [[apps-albanian-courier]] — Albanian Courier (Albania).
- [[apps-evropat]] — Evropat.

### International / pan-European

- [[apps-dhl]] — DHL; worldwide parcel network.
- [[apps-dhlexpress]] — DHL Express; premium time-definite international.
- [[apps-gls]] — GLS; pan-European parcel network.

### Locker-only

- [[apps-boxnow]] — BoxNow; locker-only network (BG, RO, GR, CY, HR, …).

### On-demand / hyperlocal

- [[apps-glovo]] — Glovo; last-mile on-demand delivery.

### Aggregators (multiple couriers via one app)

- [[apps-eushipment]] — EuShipment; EU B2B / palletised shipping aggregator (each activated sub-courier becomes its own provider).
- [[apps-sendcloud]] — Sendcloud; European multi-courier aggregator.

### Not in active use

- [[apps-berry]] — Berry — not active on the platform (kept for reference).

## Business rules

- **Shared engine.** Most couriers extend the OmniShip framework, so their Settings layout, the three delivery channels, the five pricing models (`calculator`, `calculator_fixed`, `free`, `fixed_price`, `price_and_weight`), and geo-zone gating are common — only credentials and per-courier service lists differ. [[apps-econt]] is bespoke and the most feature-rich.
- **Deprecations are business-level, not code-level.** Speedy and Rapido still have working code for existing merchants, but new integrations should use [[apps-dpdbulgaria-speedy]].
- **Aggregators expose sub-couriers.** [[apps-eushipment]] and [[apps-sendcloud]] each surface multiple downstream couriers under one app.
- **Configuration is per store** on [[settings-shipping]]; this directory never holds settings.

## Related

- [[shipping-calc-rate-models]] — rate-table semantics: when a method uses a from/to rate table (по тегло / по цена), an **empty upper bound (`до` / `to`) means no upper limit — the bracket runs to infinity** (both bounds inclusive). A blank top row is intended, not invalid, and never hides the method at checkout.
- [[settings-shipping]] — the canonical Shipping screen (enable / price / geo-zone couriers).
- [[apps]] — App Store (the Shipping category lists these couriers).
- [[orders-shipping-waybill]] — generating a courier waybill on an order.
- [[shipping-calculation]] — how delivery prices are computed and quoted.
- [[shipping-provider-mechanism]] — the courier-integration model behind these apps (config, pricing, pickup points, waybill, COD, status tracking).
- [[settings-shipping-rate-matching]] — which rate wins when several match.

## Open questions

_None._
