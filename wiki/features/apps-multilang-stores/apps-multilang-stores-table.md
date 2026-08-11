---
type: feature
nav_path: "Apps → Multilang → Stores → Sister-sites table"
route_name: apps.multilang.stores
route_path: /admin/apps/multilang/stores
aliases: ["Multilang sister-sites table", "Multilang stores list", "Sister sites list", "Language sites table", "Show language versions toggle"]
tags: [apps, administration, multilang, stores, sister-sites]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[apps-multilang-stores]]. See the hub for the other aspects (per-sister Configuration modal, network mechanics).

# Multilang → Stores — sister-sites table

## Purpose

This is the **list view** of the Stores tab — the table that shows every sister site in the merchant's Multilang network, plus the row-level actions (Edit / Pause / Delete / View) and the footer toggle that controls whether the storefront shows a language switcher to customers. Per [[apps-multilang]] the model is **one master site + N sister sites** (one per language). This page documents what the merchant reads off the table and the per-row controls; the per-sister translation settings live in the [[apps-multilang-stores-config-modal|Configuration modal]] and the underlying network rules in [[apps-multilang-stores-network]].

## Where to find it

Sidebar → Apps → Multilang → **Stores tab**. Route: `/admin/apps/multilang/stores`.

## What the merchant can do here

- Read each sister site's name, language, creation date, status, and sync state.
- Add a new sister site — the empty state and the add CTA both launch the [[apps-multilang-create-step]] wizard.
- Open a sister site's per-row **Configuration** action — see [[apps-multilang-stores-config-modal]].
- Pause / resume a sister site (Pause stops new translations firing).
- Delete a sister site (hard delete — see [[apps-multilang-stores-network]]).
- View / switch to a sister site's own admin via cross-site login (see [[apps-multilang-stores-network]]).
- Toggle the footer setting **"Show language versions on the site"** to show or hide the storefront language switcher.

## Settings & fields

### Sister-sites data table

Standard table with per-row data (per `IndexHelpers/` components):

| Column | Source |
|---|---|
| **Site name** (`SiteName`) | Friendly name + domain. |
| **Language** (`TableLanguage`) | Language code + flag. |
| **Date created** (`DateCreated`) | When the sister site was created. |
| **Status** (`SiteStatus`) | Active / Inactive / Pending / Failed badge. |
| **Actions** (`SiteActions`) | Edit, Pause, Delete, View. |

### Per-site data fields

| Field | Notes |
|---|---|
| **id** | Site ID. |
| **name** | Friendly name. |
| **domain** | The sister site's domain or subdomain (e.g., `en.merchant.com`, `merchant.ro`). |
| **language** | ISO language code (en / bg / ro / etc.). |
| **status** | Active / Inactive / Pending / Failed. |
| **created_at** | Creation timestamp. |
| **last_sync** | When the last translation sync completed. |
| **settings_override** | Per-site overrides (currency, theme, etc.). |

### Empty state

When no sister sites exist yet, the empty state shows the `CreateSite.vue` helper — a CTA to start the [[apps-multilang-create-step]] wizard.

### Footer toggle: "Show language versions on the site"

Per the Vue component `ActiveSwitch`:

- **Label**: *"Show language versions on the site"*.
- **Field**: `settings.show_language` (true_value="yes", false_value="no").
- **Reverse layout** (toggle position right of label).

When ON, the storefront shows a language switcher to customers (typically in the header) — they can switch between the master site and sister sites mid-browsing. When OFF, each sister site is a standalone storefront the customer reaches via its own domain only.

## Business rules

### Status / progress-state badge semantics

The Sites table tracks `progress_status` with 5 numeric values, mapped on the master:

- `0` = completed (legacy)
- `1` = pending (just created, install not yet finished)
- `2` = in_progress (sync running)
- `3` = configuration (sister installed, awaiting initial config copy)
- `4` = completed / active (live with translations)

The badge the merchant sees corresponds to these progress states. After the new wizard finishes and the sister site is fully provisioned, the master flips its row to `progress_status = 4`. In merchant terms:

- **Active**: site is live + receiving translations.
- **Inactive**: site is paused; no new translations fire.
- **Pending**: site is being created (initial setup in progress).
- **Failed**: setup or sync error; merchant must investigate.

### Show-language switcher visibility is per-sister

The `show_language` flag controls whether the language-switcher module appears on a sister site's storefront — but it's stored on the **sister's** own settings (not on the master's settings JSON). The footer toggle on this page sends a request to update it. With multiple sister sites, the merchant can enable the switcher on the Bulgarian-sister but disable it on the German-sister independently. (The per-sister `settings.show_version` field in the [[apps-multilang-stores-config-modal|Configuration modal]] is the same flag, settable per site from the modal.)

### Per-site iconography: `en` flag = US, `el` = GR, `sr` = RS

The platform maps a handful of language codes to non-matching flag images:

- `en` → `us.png` (US flag, not UK)
- `el` → `gr.png` (Greece for Greek)
- `sr` → `rs.png` (Serbia for Serbian)

Everything else uses `<lang>.png`. Affects only the visual icon on the language switcher and admin dropdowns.

### What the merchant CANNOT do here

- Add more sister sites than the plan allows (verify plan-gating).
- Change a sister site's language code AFTER creation (would orphan translations — verify).
- Delete the master site (only sister sites are listed here; master is implicit).

### Permission

Standard apps permission scope.

## Related

- [[apps-multilang-stores]] — hub.
- [[apps-multilang]] — Multilang feature hub.
- [[apps-multilang-create-step]] — sister-site creation wizard (launched from the add CTA / empty state).
- [[apps-multilang-products]] — per-product translation across sites.
- [[apps-multilang-progress]] — sync progress.
- [[apps-multilang-settings]] — master-level feature toggles.

## Open questions

- Confirm plan-gating cap on the number of sister sites.
- Confirm whether the language code is truly immutable after creation.
