---
type: feature
nav_path: "Settings → Delivery boxes"
route_name: boxes.settings
route_path: /admin/settings/boxes
aliases: ["Delivery boxes", "Shipping boxes", "Packaging boxes", "Кашони", "Опаковки", "Кутии за доставка"]
tags: [settings, boxes, shipping, packaging]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 5
---
# Delivery boxes

## Purpose

A simple CRUD screen for the packaging boxes the merchant uses to ship orders. Each box has a name plus outer and inner dimensions (length × width × height, in millimetres) and two weights (empty + max content). The platform's shipping-cost calculation layer reads these boxes when computing parcel volumetric weight and matching couriers' tariff bands. Merchants who ship physical products need at least one box defined; digital-only stores can ignore this screen.

This page is the **hub** for the Delivery boxes cluster. It gives the orientation; the detail lives in the sub-pages below.

## Where to find it

Sidebar → Settings → **Delivery boxes**.

The breadcrumb reads "Settings → Delivery boxes". The route is `/admin/settings/boxes`. The header icon is the box-open icon. The list shows all defined boxes (Name, Outer dimensions, Inner dimensions, per-row Edit / Delete), with **+ Add delivery box** opening the create modal.

## What the merchant can do here

- See all defined boxes in a table and sort by name (default sort: id desc — newest first).
- Add a new box, edit an existing box, or delete a box. See [[settings-boxes-fields]] for the full field list and modal layout.
- Define the box catalogue that the shipping-cost calculator packs orders into. See [[settings-boxes-packing]] for how boxes drive courier quotes.
- Retire old box sizes and manage staff access. See [[settings-boxes-lifecycle]] for delete safety + permissions.

## Sub-pages (in this cluster)

- [[settings-boxes-fields]] — the list table + Create / Edit modal: the eight box fields (six dimensions + two weights), validation (inner < outer, empty < max), default pre-fill values, mm-only inputs, and the no-confirmation delete.
- [[settings-boxes-packing]] — why boxes exist: the outer-vs-inner distinction, the 3D bin-packing algorithm that picks which box(es) to use, how boxes feed courier shipping quotes, and what happens with no boxes defined.
- [[settings-boxes-lifecycle]] — delete safety (orders snapshot the chosen box), no bulk-import / CSV, no count cap, the `settings.boxes` moderator permission, and the cache / side-effect profile.

## Settings & fields

Each box carries a **Name** plus eight required numeric values: outer height / width / length, inner height / width / length (all in millimetres), and empty weight / max weight (both in grams). Inner dimensions must be strictly less than their matching outer dimension, and empty weight strictly less than max weight. The full field reference, validation messages, modal layout, and default pre-fill values are on [[settings-boxes-fields]].

## Business rules

- **Inner must be strictly less than outer** (client-side); dimensions are **millimetres only** — no centimetre option. See [[settings-boxes-fields]].
- **Boxes feed the shipping-cost calculator** via a 3D bin-packing algorithm; missing boxes cause inaccurate quotes. See [[settings-boxes-packing]].
- **Deleting a box is safe** — orders snapshot their chosen box, so history is preserved; there is **no bulk-import** path and **no count cap**. See [[settings-boxes-lifecycle]].
- **Access** is gated by the `settings.boxes` permission for moderators (owners always pass). See [[settings-boxes-lifecycle]].
- **No side effects** — box CRUD is a synchronous DB write; no queue, notifications, or webhooks fire.

## Related

- [[settings]] — parent hub.
- [[shipping]] — shipping providers and methods consume defined boxes during cost calculation.
- [[settings-cart]] — default shipping provider/type is configured there; box matching happens during the cart/checkout flow.
- [[shipping-calculation]] — concept page; describes how boxes + product dimensions feed the courier tariff lookup.
- [[settings-geo-zones]] — adjacent geographical configuration also used by shipping cost calculation.
- [[order]] — orders snapshot the chosen box for archival.
- [[product]] — products have their own dimensions; the box-packing algorithm matches them against box inner dimensions.

## Open questions

None — open items are tracked on the relevant sub-page ([[settings-boxes-lifecycle]] carries the delete-during-in-flight-order verification note).
