---
type: feature
nav_path: "Plan → Services"
route_name: plan-services
route_path: /admin/plan-services
aliases: ["Plan services catalog", "Services card grid", "Browse services", "Recommended services list", "Service cards", "Каталог с услуги", "Преглед на услуги"]
tags: [plans, plan-services, services, catalog]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[plan-services]]. See the hub for the other aspects (checkout, billing lifecycle).

# Plan services — catalogue & browse

## Purpose

This aspect covers the **browse / search surface** of the Plan → Services tab: the card grid of recommended professional services, what each card shows, the search box, and the rules that decide which services appear at all. It is a read-only catalogue — the merchant chooses what to buy here but edits nothing. Buying is covered on [[plan-services-checkout]]; renewal / billing behaviour on [[plan-services-billing-lifecycle]].

## Where to find it

- **Plan → Services** tab in the Plan area's top-level tab bar (owner-only).
- URL pattern: `/admin/plan-services`.

## What the merchant can do here

### Browse recommended services in card form

Each service is rendered as a card showing:
- A user-with-gear icon (services use a uniform icon, not a per-service image).
- A **selection checkbox** (top-right).
- **Service name** (translated to the merchant's language; falls back to the English name).
- **Description** (Markdown-rendered, truncated with *Show more* / *Show less* when it overflows).
- **Pricing** — price (excl. VAT) + the billing period (e.g. *50.00 EUR / month*, *200.00 EUR / onetime*).
- A **Buy service** button — single-service shortcut (the buy flow itself is on [[plan-services-checkout]]).

### Search the catalog

A search box at the top filters cards by name and description, case-insensitive substring across both fields. Filtering is client-side over the already-loaded list (no server round-trip). A **No results** placeholder is shown when search returns nothing (or when the catalog is empty).

## What the merchant cannot do here

- **Edit service pricing or definitions** — the catalog (name, description, price, billing cycle) is managed centrally by CloudCart. The merchant only chooses which to buy.
- **Buy a service marked as not-recommended for them** — the endpoint returns only services with the *recommended* flag set + not archived. If a service exists in the catalog but isn't currently flagged as recommended for the merchant's profile, it doesn't surface here. The merchant must contact CloudCart / their account manager to access non-recommended services.
- **Cancel a service from this screen** — once purchased, services live as subscriptions on [[subscriptions]] and are cancelled from there.
- **Adjust quantity** — each service is a fixed-scope deliverable; the merchant buys one of each at the listed price. To buy "2× the same service" they'd repeat the flow.
- **Use a discount code on this screen** — discounts apply at the standard checkout step (entered there or seeded by a promotional landing URL). This screen has no coupon field.

## Settings & fields

This is a browse / select screen — no editable fields. The merchant sees per card:

| Field shown | What it represents |
|-------------|--------------------|
| **Icon** | Fixed user-with-gear icon (no per-service image) |
| **Selection checkbox** | Per-card toggle — adds the service to the bulk-checkout array |
| **Name** | Localised service name (English fallback) |
| **Description** | Markdown rendered, truncated with *Show more* / *Show less* on overflow |
| **Pricing** | Price (excl. VAT) + billing period (e.g. *50.00 EUR / month*, *200.00 EUR / onetime*, *9.00 EUR / year*) |
| **Buy service** button | Single-service shortcut → opens 1-item checkout (see [[plan-services-checkout]]) |
| **Bulk Buy button** (header) | *Buy selected services ({count})* — disabled when count is 0; opens N-item checkout |

## Business rules

### Recommended + non-archived filter

The list is filtered to services where the *recommended* flag is set (`recommend = 1`) AND `archived = 0`. Archived services are kept in the system for invoicing / reporting purposes but never appear on this screen.

### Sort by sort_order

Services are returned in the order set by CloudCart's `sort_order` field on each record — that's the merchant-visible order. There's no "popular" / "alphabetical" toggle.

### Service descriptions are Markdown

Service descriptions support Markdown formatting (bold, italics, links, lists). The card renders them inline; long descriptions are clipped with a *Show more* link.

### The card grid (ServicesList)

The tab renders a grid of service cards, one per service returned by the catalogue endpoint. The top bar carries the search input and the *Buy selected services ({count})* action button (disabled when nothing is ticked or while loading). A loading skeleton shows while the list loads; an empty-results placeholder shows when the search or catalogue is empty.

### Per-service card detail

Each card row: a generic user-with-gear icon (top-left, all services share it); a selection checkbox (top-right) that adds the service to the bulk array; the translated service name; a Markdown description block that clips by max-height and toggles full text with *Show more* / *Show less*; a **Buy service** button (single-service shortcut); and small pricing text (price + billing-period label — *Monthly* / *Quarterly* / *Semi-annually* / *Annually* / *2 Years* / *One time*).

### Language detection for name + description

Both the service name and description are stored per-language (translatable) and displayed in the current admin-panel language (`language_cp`) with English fallback — each merchant sees the right language without manual switching. Search matching uses both the translated and English text together, so a merchant browsing in Bulgarian still matches a service whose English description contains the searched word (e.g. *design*).

### Catalogue is not plan-gated

The catalogue itself is NOT plan-gated — every merchant sees the same `recommend = 1` + non-archived list regardless of their plan. (A few specific services consume a plan-feature mapping *after* purchase — see [[plan-services-billing-lifecycle]].)

## Related

- [[plan-services]] — hub.
- [[subscriptions]] — where purchased services appear; cancellation happens there.
- [[plans-purchase]] — the per-plan purchase flow that surfaces the same list as a *Recommended services* block.
- [[settings-translations]] — admin-panel language that drives name / description display.

## Open questions

None.
