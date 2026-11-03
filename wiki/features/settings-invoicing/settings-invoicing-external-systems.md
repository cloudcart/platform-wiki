---
type: feature
nav_path: "Settings → Invoicing → External accounting systems"
route_name: invoicing.settings
route_path: /admin/settings/invoicing
aliases: ["External accounting integration", "Gensoft", "Szamlazz", "SmartBill", "FlixFacts", "FGO", "ERP integration", "External invoicing", "External system dropdown"]
tags: [settings, invoicing, integrations, external, erp]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[settings-invoicing]]. See the hub for the other aspects (activation modes, numbering, issuer block, template editor, credit note, HTML templates).

# Invoicing — external accounting systems

## Purpose

CloudCart can hand invoice issuance over to an external ERP / accounting system when the merchant has the matching App installed. The Invoicing page surfaces one **External system** dropdown, and it does exactly one job: it names the App that supplies the invoice **number** when the numbering mode is set to *External system*. The only App the dropdown ever offers is **Gensoft**. A second, entirely separate shape exists: **full-replacement providers** (Szamlazz) that flip `invoicing_provider` and own the whole issuance flow without appearing in this dropdown at all.

## Where to find it

Sidebar → Settings → **Invoicing** → Invoice template tab → "General settings" box → **External system** picker. It is the last of the chained selects in that box, so it only appears after **Generate Invoice** = *Manual* AND **Invoice number** = *External system*. In any other numbering mode the picker is not rendered.

## What the merchant can do here

- Pick which installed-and-active App supplies the invoice number while the store is in external numbering mode.
- Revert to platform numbering by changing **Invoice number** back to *Automated by system* or *Manual by admin* (the picker then disappears; deactivating the App also empties the dropdown).

## Settings & fields

| Field | Key | Notes |
|-------|-----|-------|
| External system | `invoice_external_number` | Stores the selected App's identifier. Visible **only** when `invoice_number_type=3`, and required in that mode. The dropdown is built from a fixed single-entry list — **Gensoft** — filtered to Apps that are both **installed** AND **active**, so it is empty (and the save then fails validation) when Gensoft is missing or deactivated. |
| Invoicing provider (hidden, read-only here) | `invoicing_provider` | `platform` (default) or the App slug (e.g., `szamlazz`). Set automatically by full-replacement provider Apps; those Apps do **not** appear in the dropdown above. See [[settings-invoicing-activation-modes]]. |

## Business rules

### The dropdown supplies NUMBERS, it does not push documents

Selecting an App here does not make CloudCart mirror invoices into that App. What it does is far narrower: while the store's numbering mode is *External system*, every time an invoice number is needed the platform asks the selected App for the next one and stamps whatever it returns onto the order. Rendering, storage and the customer email all stay on the platform. If the App returns nothing, no number is assigned and the merchant sees *"No invoice has been created in the selected external system"* — see [[settings-invoicing-activation-modes]].

Merchants who want a copy of every document inside an ERP configure that on the ERP App's own settings page, not here.

### Number-source Apps vs full-replacement providers — two different shapes

Two distinct shapes, often confused:

- **Number-source App** — **Gensoft** is the only App exposed in this dropdown. CloudCart still owns the document (its own PDF, its own email); only the number comes from Gensoft. The App does NOT flip `invoicing_provider`, and the merchant continues to use the platform's invoicing UI.
- **Full-replacement providers** — **Szamlazz** is the documented App that **replaces** platform invoicing entirely. Activating Szamlazz sets `invoicing_provider=szamlazz` and the platform's own `invoicing` toggle is blocked by the mutex (see [[settings-invoicing-activation-modes]]). The App owns numbering, PDF rendering, and customer email delivery. It never appears in the External system dropdown — it takes over through the provider setting instead.

Merchants who install Szamlazz can't accidentally double-issue invoices — the platform-level toggle silently locks out.

Other accounting Apps (**SmartBill**, **FlixFacts**, **FGO**) have their own settings screens and their own sync behaviour — see [[apps-smart-bill]], [[apps-flix-facts]], [[apps-fgo]]. None of them are selectable here.

### NO standardised retry policy on the invoicing layer

There is **NO** unified retry / backoff policy applied by the invoicing layer itself. Each App's integration code decides how to handle a failed call — some apps simply log and continue, others queue their work with their own retry logic, others fail loudly.

The merchant-facing surface for failure is the relevant App's settings page (see [[apps-szamlazz]], [[apps-smart-bill]], etc.) and/or the platform alerts panel when the App's job logs an exception. **There is no "retry from the order detail page" affordance** for the App's own syncing; the merchant can, however, simply click **Generate invoice** again once the App is healthy, since no number was assigned on the failed attempt.

### The dropdown is filtered by install + active state

The External system dropdown lists Gensoft only while it is BOTH installed AND active. If the App is uninstalled or deactivated, the dropdown empties — and since the field is required in external numbering mode, saving the invoicing settings then fails until the merchant switches **Invoice number** back to a platform mode.

### One external number source per store

The setting holds a single value, so the store has exactly one external number source at a time. Selecting one replaces any previous selection.

## Related

- [[settings-invoicing]] — hub.
- [[settings-invoicing-activation-modes]] — the `invoicing_provider` mutex + `invoice_number_type=3` external-app-owned numbering.
- [[apps-gensoft]] — the only App offered in the External system dropdown.
- [[apps-szamlazz]] — full-replacement provider (sets `invoicing_provider=szamlazz`); not in the dropdown.
- [[apps-smart-bill]] — accounting App with its own settings screen; not in the dropdown.
- [[apps-fgo]] — accounting App with its own settings screen; not in the dropdown.
- [[apps-flix-facts]] — accounting App with its own settings screen; not in the dropdown.
- [[invoice]] — entity whose number the external system supplies.
- [[credit-note]] — entity whose number the external system supplies.
- [[order-processing-pipeline]] — when the invoicing provider is invoked during order processing.

## Open questions

- The exact retry / failure surface per accounting App (varies by App; see each App's own page).
