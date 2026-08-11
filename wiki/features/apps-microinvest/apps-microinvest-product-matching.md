---
type: feature
nav_path: "Apps → Microinvest → Product matching"
route_name: apps.microinvest.overview
route_path: /admin/apps/microinvest
aliases: ["Microinvest product matching", "compare_by", "Microinvest mapping table", "external_record_key", "sync-ids", "Microinvest sync-ids endpoint", "new Microinvest products not linking", "Microinvest duplicates", "app_import microinvest"]
tags: [apps, erp, microinvest, matching, mapping, import]
plan_gates: []
created: 2026-06-25
updated: 2026-06-25
source_count: 3
---

> Part of [[apps-microinvest]]. See the hub for the other aspects (settings, sync model, reset import, sync debug).

# Microinvest — product matching & the mapping table

## Purpose

How an incoming Microinvest record is matched to an existing CloudCart product (update) versus created as a new one — the two-layer match, how the internal mapping is populated for new products, and how deletions are detected. This is the load-bearing knowledge for "duplicate created / didn't update" tickets.

## Where to find it

The match field (**Compare by**) is on [[apps-microinvest-settings]]; the matching itself runs during import on the **Status** tab. The mapping rows live in the shared [[external-record-mapping]] store.

## What the merchant can do here

Pick the **Compare by** field (Barcode / SKU / EAN) so incoming Microinvest records match the right CloudCart variants. Everything else (the persistent mapping, the id push) is automatic / Microinvest-side.

## Settings & fields

Only `compare_by` (on [[apps-microinvest-settings]]) is merchant-set. The rest is internal: the `ExternalMetaData` mapping (`integration = microinvest`) and the `app_import = 'microinvest-<Code>'` origin tag.

## Business rules

### Two layers decide update vs create

1. **The `compare_by` field** is the identifier used to **first link** a Microinvest record to a CloudCart variant: `barcode` compares Microinvest's **`BarCode1`** against the CloudCart variant's **barcode**; `sku` / `ean` compares Microinvest's **`BarCode2`** against the variant's **SKU**; `nothing` disables field matching. If nothing matches the chosen field, the record is **created as a new product** — so a wrong / blank `compare_by` value is the classic cause of duplicates.
2. **The internal mapping table.** Once linked, the platform stores a **persistent ID↔ID mapping** in the shared external-record store ([[external-record-mapping]], `ExternalMetaData`, scoped `meta_data.integration = microinvest`): `external_record_key = <Microinvest item id>` → the CloudCart **variant** (`record_type = Variant`, `type = variant_import`). On every later sync the variant is found by this stored Microinvest id even if its barcode / SKU later changed. The product also carries the origin tag `app_import = 'microinvest-<Code>'` (the Microinvest product `Code`) — the CloudCart-wide convention (shared with XML / CSV import) for tracking import origin.

### How the mapping is populated for new products — the `sync-ids` endpoint

When **new products are added in Microinvest**, the Microinvest side must push their ids to the storefront endpoint **`POST [store domain]/apps/microinvest/sync-ids`** (route `site.apps.microinvest.sync-ids`) for those ids to land in CloudCart's mapping. It accepts an XML body of `SyncId` pairs — each a **`CloudCartId`** (the CloudCart variant) + its **`MicroinvestId`** — and (re)writes the `ExternalMetaData` rows for them. Until the Microinvest side runs this push, a brand-new Microinvest product has **no mapping row**, so it can only be matched by `compare_by` (barcode / SKU); if that doesn't match either, it imports as a **new** product. So a *"new Microinvest products aren't linking / are duplicating"* ticket usually means the **Microinvest side hasn't called `sync-ids`** to register the new ids.

### Deletion detection

At import the platform compares the incoming Microinvest item ids against the stored `external_record_key`s for `integration = microinvest`; variants whose key is **no longer sent** are treated as removed-from-Microinvest (set inactive when `disable_missings` is ON — see [[apps-microinvest-settings]]). [[apps-microinvest-reset-import|Reset import]] drops exactly these mapping rows, then clears the `app_import` flag.

### Debug check (INTERNAL)

> **INTERNAL.** For a *"duplicate created"* / *"didn't update"* ticket, check **both** layers: (a) does Microinvest's `BarCode1` / `BarCode2` actually equal the CloudCart variant's barcode / SKU for the chosen `compare_by`, and (b) is there an `ExternalMetaData` row linking that Microinvest item id (`external_record_key`) to the variant — or did a prior reset drop it? Mismatch in (a) with no row in (b) is the usual duplicate cause. Read the mapping rows with the `externalMetaData` / `externalMetaIntegrations` queries ([[external-record-mapping]]), and read the exact `BarCode1` / `BarCode2` / `Code` Microinvest sent with the `erpTaskXml` query ([[apps-microinvest-debug]]).

## Related

- [[apps-microinvest]] — hub.
- [[external-record-mapping]] — the shared `ExternalMetaData` table + the read queries.
- [[apps-microinvest-settings]] — the `compare_by` and `disable_missings` settings.
- [[apps-microinvest-reset-import]] — drops the mapping + origin tag.
- [[apps-microinvest-debug]] — the `erpTaskXml` payload to compare against the match fields.

## Open questions

(none)
