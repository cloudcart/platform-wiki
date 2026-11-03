---
type: feature
nav_path: "Settings → Shipping → List & Add modal"
route_name: admin.shippingProviders
route_path: /admin/shipping
aliases: ["Shipping methods list", "Add shipping method", "Browse shipping integrations", "Create new shipping method"]
tags: [settings, shipping, providers, integrations, modal]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-shipping]]. See the hub for the other aspects (Custom rates, edit panel, rate matching, lifecycle, API & permissions).

# Shipping — list & Add modal

## Purpose

The Shipping settings page is structured as a **single table of configured methods** plus a header **+ Add shipping method** action that opens a slide-in *"Create new shipping method"* panel. This aspect documents the table columns, the table-level actions (per-row toggle, delete, **+ View more Shipping methods** link), and the Add panel's two sections (Browse shipping integrations / Custom).

## Where to find it

Sidebar → Settings → **Shipping**. Page title: "Shipping methods". Header description:

> *"Manage domestic shipping couriers, access international providers, or set up custom shipping rates by price, weight, or both"*.

## What the merchant can do here

### List columns

| Column | What it shows |
|--------|---------------|
| **Name** | Logo + name. A **Recommended** badge appears for country-default carriers (set per-app via the manifest's `other.recommend = true`, not toggleable from the UI). Below the name, a parameters line describes the pricing model — e.g., *"Price based"*, *"Weight based"*, *"Price based to address"*, *"Weight based to office"*, *"Calculator based + handling fee to address"*, *"Local Pickup"*, *"Fixed shipping rate calculated by the price and weight of the products"*. |
| **Delivery time** | Appears only when the [[apps-shipping-hours-settings|Shipping Hours]] app is installed. Shows the courier's promised delivery window. |
| **Deliver to** | *"Global"* / *"Regions are determined by the provider"* (integrations) / a specific [[settings-geo-zones]] name (Custom methods). When the zone has multiple conditions, the cell shows `<first condition> and {N} other conditions`. Clicking opens a side modal listing every condition. |
| **Show in store** | Per-row active toggle. ON = appears at checkout for matching orders; OFF = hidden. Persists immediately (no save button). |
| **Remove** | Trash-can icon. Confirmation: *"Are you sure you want to delete that shipping method?"*. See [[settings-shipping-lifecycle]] for delete protection + cascade. |

### View more link

Below the table, a **+ View more Shipping methods** link navigates to the [[apps]] catalog filtered to the Shipping category (`apps.all?category=4`). The merchant installs any additional integration from there.

### Add shipping method modal — overall layout

Opened from the **+ Add shipping method** button in the header. Loads as a **slide-in side panel** (not a centered modal) titled *"Create new shipping method"* with the explainer *"Choose the shipping method type. You cannot change this after a type has been chosen."* The panel stacks two sections inside one screen.

| Section | Behaviour |
|---------|-----------|
| **Browse shipping integrations** | List of installable shipping apps for the store's operation country (DHL, Speedy, Econt, GLS, DPD, Fan Courier, Cargus, etc.). Each card: logo, name, **Recommended** / **Featured** badges, and the app's settings description. Clicking a card navigates the merchant **directly out of this panel** to the integration's settings page (`apps.<provider>.settings`) — no "next" step inside the modal. |
| **Custom** | Four cards: Based on price, Based on weight, Based on price and weight, Local Pickup. Clicking a card **opens the per-type rate-config side panel** as a new wide slide-in (see [[settings-shipping-edit-panel]]). |

The integrations section is filtered server-side by the country defined in [[settings-general]] (the `country` field). A Bulgarian store sees Econt / Speedy / Bulgarian Posts; a Romanian store sees Fan Courier / Cargus / DPD Romania; etc.

### All-installed empty state

When every installable integration is already installed, the integrations section collapses to an illustration and the message *"You have installed all available shipping methods"*. The Custom section remains visible regardless.

### Local Pickup visibility

The **Local Pickup** card in the Custom section is hidden when the [[apps-stores]] (Stores) app is NOT installed; when the app IS installed but a marketplace shipping provider already exists, the card is hidden too (so the merchant cannot create two marketplace methods). See [[settings-shipping-custom-rates]] for the `marketplace` type semantics.

## Settings & fields

The list-level fields are the five columns above. The Add modal exposes only **type cards** — the actual rate-config fields live on the per-type edit panel — see [[settings-shipping-edit-panel]].

## Business rules

- **Type is chosen at creation; permanent thereafter.** The explainer *"You cannot change this after a type has been chosen"* is the merchant-facing warning. See [[settings-shipping-custom-rates]] for the type catalogue.
- **Integration card clicks navigate away from the modal** — there is no nested install flow. The merchant returns to the Shipping list by completing (or cancelling) the app's settings page.
- **Country filter cannot be overridden from this UI** — to access integrations for other countries, the merchant must change the operation country in [[settings-general]] (which has cascade effects — see that page's language/currency rebuild rules).
- **`Show in store` toggle is per-row and saves immediately** — no platform cache invalidation delay (see [[settings-shipping-lifecycle]]).

## Related

- [[settings-shipping]] — hub.
- [[settings-shipping-edit-panel]] — what opens when the merchant clicks a Custom type card or a Custom method's row name.
- [[settings-shipping-custom-rates]] — the four Custom type cards and their `type` keys.
- [[settings-shipping-lifecycle]] — `active=yes/no` toggle, delete protection, hash deep-link `#add-shipping`.
- [[apps]] — `apps.all?category=4` (the **View more Shipping methods** link target).
- [[apps-shipping-hours-settings]] — adds the **Delivery time** column.
- [[apps-stores]] — required for the **Local Pickup** card.
- [[settings-general]] — operation country drives the integrations filter.
- [[settings-geo-zones]] — populates the **Deliver to** column for Custom methods.

## Open questions

_None._
