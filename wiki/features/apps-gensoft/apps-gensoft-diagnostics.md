---
type: feature
nav_path: "Apps → Gensoft → Diagnostics"
route_name: apps.gensoft.diagnostics
route_path: /admin/apps/gensoft/diagnostics
aliases: ["Gensoft Diagnostics", "Gensoft Test connection", "Gensoft connection check", "Gensoft no products diagnostic", "Gensoft known products", "erpDiagnostics", "ERP diagnostics"]
tags: [apps, erp, gensoft, diagnostics, debug]
plan_gates: []
created: 2026-06-25
updated: 2026-06-25
source_count: 2
---

> Part of [[apps-gensoft]]. See the hub for the other aspects (settings, sync model, product matching, reset import).

# Gensoft — diagnostics (connection self-check)

## Purpose

The **Diagnostics** tab — a **read-only** check of the live connection to Gensoft and what it currently returns. It is Gensoft's main troubleshooting tool (Gensoft has no per-task XML view; this is the equivalent of "what is Gensoft answering right now?"), and it is currently the **only** ERP app wired to the shared diagnostics framework.

## Where to find it

Sidebar → Apps → **Gensoft** → **Diagnostics** tab (`/admin/apps/gensoft/diagnostics`; backend `GET apps.api.gensoft.diagnostics`). A **Test connection** button re-runs the checks on demand. Intro: *"Run a read-only check of the connection to the ERP and what it currently returns."* Also exposed generically as the `erpDiagnostics(key: "gensoft")` admin query.

## What the merchant can do here

Run the check and read the per-row result. It **changes nothing** — it never imports, writes, or edits settings; it only reports what Gensoft answers.

## Settings & fields

No settings — a button that runs the checks and renders the results.

## Business rules

### States + overall banner

Each check returns `ok`, `warning`, `error`, or `skipped`. The page shows an overall banner from the **worst** status — **"Needs attention."** appears whenever any check is a warning or error. Checks run top-to-bottom and **stop early if Connection fails**.

### The checks

| Check | OK | Warning / Error / Skipped |
|---|---|---|
| **Connection** | *"The GenSoft server is reachable."* | ERROR — server not reachable (stops here; check the URL / that Gensoft is online). |
| **Authentication** | *"Authenticated. GenSoft returned N catalog(s)."* | ERROR — could not authenticate or list catalogs (check the credentials). |
| **Configured catalog** | *"Selected catalog \"X\" exists."* | WARNING — no catalog selected (all catalogs used) · ERROR — the selected catalog no longer exists in Gensoft. |
| **Categories** | *"GenSoft returned N categories."* | (row appears only when the call succeeds). |
| **Products** | *"GenSoft returns N product(s) for the selected catalog."* | WARNING — no products returned (even with no date limit) · ERROR — Gensoft errored requesting products. |
| **Known products** | *"GenSoft returns X of N sampled known products."* | WARNING — none of the sampled previously-imported products are returned anymore · ERROR — Gensoft errored re-checking · SKIPPED — no previously-imported products to re-check. |

### Two checks worth understanding

- **Products** is probed from the very beginning (epoch), so a "no products" warning means Gensoft genuinely returns nothing for that catalogue — not merely nothing recent. Pair this with the catalogue setting on [[apps-gensoft-settings]].
- **Known products** re-samples up to **15** previously-mapped Gensoft article ids (variants already linked via [[apps-gensoft-product-matching]]). A warning here is the classic signal behind products silently disappearing from the store — Gensoft has stopped returning items it previously exported (e.g. unflagged for the online store, or removed from the catalogue).

## Related

- [[apps-gensoft]] — hub.
- [[apps-gensoft-settings]] — the catalogue / credentials these checks validate.
- [[apps-gensoft-product-matching]] — the mapped article ids the Known-products check re-samples.
- [[external-record-mapping]] — read the mappings directly with `externalMetaData` if a deeper look is needed.

## Open questions

(none)
