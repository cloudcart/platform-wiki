---
type: feature
nav_path: "Apps → OLX → Advert format"
route_name: apps.olx.products
route_path: /admin/apps/olx/products
aliases: ["OLX advert format", "OLX description", "OLX title trim", "OLX image cap", "OLX logo attach", "OLX activate deactivate", "OLX reason code"]
tags: [apps, olx, marketplace, adverts, formatting]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# OLX — advert format & lifecycle commands

> Part of [[apps-olx]]. See the hub for the other aspects (connection, sync, publishing).

## Purpose

How CloudCart assembles each advert before sending it to OLX, and how it toggles an advert on/off afterwards. Covers the auto-built description, the title length cap, the per-category image limit, the logo attach, and the activate/deactivate command model. This is the aspect to read for "where does the OLX description come from?", "why is my title cut off?", "why are emojis / Romanian characters missing?", and "why didn't my logo show up?".

## Where to find it

Adverts are assembled when the merchant publishes from the **Products tab** ([[apps-olx-products]]) and managed from the **Adverts tab** ([[apps-olx-adverts]]). The formatting described here is automatic — there is no separate "OLX description" editor.

## What the merchant can do here

- Publish a product, letting CloudCart auto-build the advert title, description, images, and logo.
- Activate / deactivate an existing advert without re-publishing.

The merchant does **not** write a separate OLX-specific description — it is generated (see below).

## Settings & fields

| Field | Behaviour |
|---|---|
| Title | Auto-trimmed to **70 characters** (the `label.trim.title` / `help.trim.title` setting controls whether the merchant is warned). OLX rejects longer titles. |
| Description | Auto-built — see Business rules. |
| Images | Capped at the **per-OLX-category picture limit** — see Business rules. |
| Logo | Auto-attached from the merchant's main logo if it meets the size minimum — see Business rules. |

## Business rules

### Description auto-built from variants + properties + vendor + product description

The advert description is assembled by concatenating, in order: (1) a "For more information" link to the product URL, (2) the variant parameters (e.g. "Size: S, M, L"), (3) a "Vendor: {name}" line, (4) all category properties as a key: values list, and (5) the product's HTML-stripped description. So the OLX description is **auto-generated** — the merchant does not write a separate one.

### Description regex strips emojis and non-Latin / non-Cyrillic characters

The product description is filtered through a regex that allows only **Cyrillic, Latin, digits, spaces, and a fixed set of punctuation**. **Emojis, Greek, and Romanian-specific diacritics (ă, â, î, ș, ț) get stripped.** This can mangle non-Bulgarian descriptions even for OLX Romania merchants — the merchant should expect lossy text when publishing.

### Title auto-trimmed to 70 characters

Every advert title is truncated to 70 characters before sending, because OLX rejects longer titles. A merchant with long product names will see them cut off on OLX.

### Images auto-capped at the category's picture limit

The formatter iterates the product images but stops at the OLX **category's picture limit** (fetched from OLX). A category that allows 8 photos receives 8; one that allows 4 stops at 4. Extra product images beyond the cap are simply not uploaded.

### Logo auto-attach requires a 300×300 minimum

When publishing, CloudCart fetches the merchant's main logo and attempts to attach it to the new advert (`POST partner/adverts/{id}/logos`; `LOGO_MIN_SIZE = '300'`). The logo must be at least **300 pixels** on its longest side or the attach is **skipped silently** — no warning; the advert just publishes without a logo. (Note: the integration actually comments out the logo upload in the sync flow, so logo attach may not run on every path — verify against current behaviour.)

### Activate / deactivate via a single command endpoint

Enabling or disabling an advert uses `POST partner/adverts/{id}/commands` with `command: 'activate'` or `command: 'deactivate'`. A deactivation includes `is_success: true`, signalling that the deactivation was intentional (not because the item sold). The merchant can toggle an advert on OLX without re-publishing it.

### "Other" deactivation reason is hardcoded to 7

When CloudCart deactivates an advert without specifying a reason, OLX receives reason code 7 ("other") — `REASON_OTHER_ID = 7`. The merchant does not pick from a reason dropdown; every CloudCart-initiated deactivation reads as "other" on OLX's side.

## Related

- [[apps-olx]] — hub.
- [[apps-olx-products]] — where products are selected + published.
- [[apps-olx-adverts]] — the adverts list where activate/deactivate happens.
- [[apps-olx-parameters]] — category properties that feed the description.
- [[products-property]] — product properties surfaced in the description.

## Open questions

- Whether logo auto-attach runs on the publish path given it is commented out in the sync flow (verify).
