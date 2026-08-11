---
type: feature
nav_path: "Apps → Microinvest → Reset import"
route_name: apps.microinvest.overview
route_path: /admin/apps/microinvest
aliases: ["Microinvest reset import", "Microinvest unlink", "Microinvest start over", "reset import card", "Microinvest re-link products"]
tags: [apps, erp, microinvest, reset, cleanup]
plan_gates: []
created: 2026-06-25
updated: 2026-06-25
source_count: 2
---

> Part of [[apps-microinvest]]. See the hub for the other aspects (settings, sync model, product matching, sync debug).

# Microinvest — reset import (unlink)

## Purpose

What the **Reset import** button does, when to use it, and what to do after — the integration's "start over" / unlink control.

## Where to find it

The **Status tab** → **Reset import** card (it also previews the state it will clear).

## What the merchant can do here

Press **Reset import** to sever the store's link to Microinvest without losing the catalogue, then re-import to rebuild the links.

## Settings & fields

No fields — it is a single action button on the Status tab.

## Business rules

### What it does

Two passes, both scoped to Microinvest only:

1. **Deletes the whole Microinvest mapping** — every `ExternalMetaData` row for `integration = microinvest` (the Variant ↔ `MicroinvestId` links built by `compare_by` / `sync-ids` — see [[apps-microinvest-product-matching]]).
2. **Clears the origin tag** — sets `app_import = null` on every product tagged `microinvest-%`.

It does **NOT** delete or deactivate products, prices, stock, or any merchant edits — the catalogue stays exactly as it is. It only severs the **link** back to Microinvest, and it touches **only** Microinvest-origin data (products from other integrations or hand-made products are untouched).

### When to use it (the benefit)

- The mapping got **wrong or messy** — duplicates, mis-linked products, or links created under a bad setting.
- The merchant **changed `compare_by`** (e.g. SKU → Barcode): old links were keyed off the previous field; reset + re-import re-links cleanly by the new one.
- **Re-pointing** to a different Microinvest installation / company.
- **Decoupling** before uninstalling, so deletion-detection / *Disable missings* no longer acts on those products.

### What to do after pressing it

- Products remain but are now **unlinked** (no mapping row, no origin tag).
- **Re-import** to rebuild the links: the first pass matches by the `compare_by` field, and the **Microinvest side must re-push ids via `sync-ids`** ([[apps-microinvest-product-matching]]) to repopulate the mapping.
- Until that re-import + `sync-ids` runs: deletion-detection deactivates nothing (no mapping to diff against), and a re-import can **create duplicates** if `compare_by` doesn't match — so confirm `compare_by` points at a field both sides actually share **before** re-importing.
- The unlink is **not** undoable (there is no "restore links" action); the links are rebuilt only by re-importing.

## Related

- [[apps-microinvest]] — hub.
- [[apps-microinvest-product-matching]] — the mapping + `compare_by` + `sync-ids` that reset clears and re-import rebuilds.
- [[apps-microinvest-settings]] — the `compare_by` to confirm before re-importing.
- [[external-record-mapping]] — the `ExternalMetaData` rows that reset deletes.

## Open questions

(none)
