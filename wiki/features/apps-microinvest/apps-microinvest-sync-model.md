---
type: feature
nav_path: "Apps → Microinvest → Sync model"
route_name: apps.microinvest.overview
route_path: /admin/apps/microinvest
aliases: ["Microinvest sync direction", "Microinvest conflict resolution", "Microinvest on-demand sync", "Microinvest multi-store", "Microinvest local deployment", "Microinvest not invoicing"]
tags: [apps, erp, microinvest, sync, inventory]
plan_gates: []
created: 2026-06-25
updated: 2026-06-25
source_count: 2
---

> Part of [[apps-microinvest]]. See the hub for the other aspects (settings, product matching, reset import, sync debug).

# Microinvest — sync model

## Purpose

How the integration actually syncs: which side is authoritative for what, when a sync runs, and the boundaries (one feed per store, product/stock only — not invoicing).

## Where to find it

There is no dedicated screen — this is the behaviour behind the **Status** tab's sync actions. The direction is set by the **Action** field on [[apps-microinvest-settings]].

## What the merchant can do here

Choose the sync direction (Action = `import` / `export`) and which fields Microinvest may overwrite (Updates), then trigger syncs from the Status tab.

## Settings & fields

No fields of its own — the levers are `Action`, `Updates`, and `disable_missings` on [[apps-microinvest-settings]].

## Business rules

### Direction of sync and conflict resolution

Common pattern: Microinvest is master for stock + invoicing; CloudCart is master for orders + customers. For products imported through Microinvest (flagged `app_import = 'microinvest-<id>'`, see [[apps-microinvest-product-matching]]), direction is set by **Action**: `import` overwrites CloudCart on each sync (the fields chosen in **Updates**, plus price and stock), `export` pushes CloudCart data to Microinvest with no overwrite back. When `action = import`, Microinvest wins for the chosen fields only.

### Sync is on-demand, not polled

The integration does NOT poll Microinvest on a fixed cadence. Syncs are event-driven — triggered by the merchant clicking Sync, by order status changes / stock updates, or by Microinvest pushing data when changes occur. This differs from the cron-driven distributor ERPs ([[apps-polycomp]] / Also / IT4Profit). Microinvest also opts out of the working-lock pattern other ERPs use to block concurrent runs, assuming the merchant manages scheduling on the Microinvest side.

### Multi-store source-of-stock

Microinvest can host multiple warehouses / objects, but the CloudCart integration uses ONE credential set per store. A merchant running multiple physical stores chooses which Microinvest object feeds CloudCart's stock inside the Microinvest-side configuration; CloudCart consumes whatever the feed returns.

### Local Microinvest deployment

Microinvest is typically installed on the merchant's own server / network. The integration may require the merchant's IT to expose Microinvest's API over the internet — an important security consideration.

### Microinvest is NOT an invoicing provider

The integration is **product / stock sync only** — it does NOT register as an invoicing provider on the store. The merchant can run Microinvest alongside [[apps-fgo]] (for invoicing) without conflict: Microinvest handles inventory + product data, FGO handles tax-compliant invoice issuance.

## Related

- [[apps-microinvest]] — hub.
- [[apps-microinvest-settings]] — the `Action` / `Updates` / `disable_missings` levers.
- [[apps-microinvest-product-matching]] — how synced products are matched / dedup'd.
- [[apps-fgo]] — pair for tax-compliant invoicing (Microinvest does not invoice).
- [[apps-polycomp]] — contrast: a cron-polled distributor ERP.

## Open questions

(none)
