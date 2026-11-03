---
type: feature
nav_path: "Apps → Gensoft → Reset import"
route_name: apps.gensoft.status
route_path: /admin/apps/gensoft
aliases: ["Gensoft reset import", "Gensoft last import date", "Gensoft re-sync", "Gensoft full re-import", "reset last_import"]
tags: [apps, erp, gensoft, reset, incremental]
plan_gates: []
created: 2026-06-25
updated: 2026-06-25
source_count: 2
---

> Part of [[apps-gensoft]]. See the hub for the other aspects (settings, sync model, product matching, diagnostics).

# Gensoft — reset import (re-sync from scratch)

## Purpose

What Gensoft's **Reset import** does, when to use it, and what to do after. **Important:** Gensoft's reset is **not** the same as Microinvest's — it forces a full re-fetch, it does **not** unlink products.

## Where to find it

The **Status tab** → **Reset import** card (it previews the dates it will clear — *Last sync* / *Last fast sync*).

## What the merchant can do here

Press **Reset import** to make the next import re-fetch the **entire** Gensoft catalogue from the beginning instead of only the recent delta.

## Settings & fields

No fields — a single action on the Status tab.

## Business rules

### What it does — clears the incremental watermark only

Reset import **deletes the two incremental watermarks**: `last_import` and `last_import_fast` (the dates the [[apps-gensoft-sync-model|incremental import]] uses to ask Gensoft for "articles changed since…"). That is **all** it does.

It does **NOT** drop the product mapping ([[apps-gensoft-product-matching]] `ExternalMetaData` rows / `app_import` tags), and it does **NOT** delete or deactivate any products. Existing products stay fully linked to their Gensoft articles.

> **Contrast with Microinvest.** [[apps-microinvest-reset-import|Microinvest's Reset import]] *unlinks* — it drops the mapping + origin tag. Gensoft's Reset import *re-syncs* — it only clears the date watermark so the next run pulls everything again, with the links intact. Same button name, opposite effect.

### When to use it (the benefit)

- **Backfilled / corrected data in Gensoft** that was changed without bumping its modified-date, so the incremental import wouldn't pick it up — a reset re-pulls the whole catalogue and applies it.
- A run was **partially missed** and the merchant wants a clean full re-sync rather than waiting for the next delta.
- After **changing the catalogue / "Works with" settings**, to re-pull everything under the new configuration.

### What to do after pressing it

- Nothing is lost and nothing is unlinked — products keep their Gensoft mapping.
- The **next import** (the 4-hour sweep, or a manual Start) re-fetches the full catalogue from the beginning and re-applies prices / stock / the chosen `Updates` fields; matching uses the existing mapping + `compare_by`, so it updates existing products rather than duplicating them.
- The watermark is then re-established at the new run's time, and subsequent runs go back to incremental.

## Related

- [[apps-gensoft]] — hub.
- [[apps-gensoft-sync-model]] — the `last_import` watermark this clears.
- [[apps-gensoft-product-matching]] — the mapping that reset leaves intact.
- [[apps-microinvest-reset-import]] — the contrasting "unlink" reset on Microinvest.

## Open questions

(none)
