---
type: feature
nav_path: "Apps → Profics → Settings"
route_name: apps.profics.settings
route_path: /admin/apps/profisc/settings
aliases: ["Profics Settings", "Profisc Settings", "Profics config"]
tags: [apps, administration, profics, pos, settings, bulgaria]
plan_gates: []
created: 2026-05-21
updated: 2026-05-28
source_count: 2
---
# Profics → Settings

## Purpose

The **Settings** tab is where the merchant connects CloudCart to **Profisc** (Albanian fiscal e-invoicing service, `profisc.al`) — enters account credentials, picks the legal entity + branch + cash register, and configures auto-submission on order status. See [[apps-profisc]] for the full feature set.

(Note: The wiki file uses slug `apps-profisc`; the actual app key in code is `profics`.)

## Where to find it

Sidebar → Apps → Profics → **Settings tab**. Route: `/admin/apps/profisc/settings`.

## What the merchant can do here

### Credentials

| Field | Notes |
|---|---|
| **Profics API credentials** | Username + password OR API key (verify auth model). |

The Profics integration (per [[apps-profisc]]):
- Runs a dedicated credential check (separate from the generic configured check).
- Converts a CloudCart order into the Profics format before sending it.

### Sync configuration

| Setting | Notes |
|---|---|
| **Auto-send on Paid** | Trigger order sync when order status hits Paid. |
| **Sync direction** | One-way (CloudCart → Profics) or bi-directional. |
| **Conflict resolution** | When both sides have differing data, who wins. |

### What the merchant CANNOT do here
- Use without an active Profics subscription / license.
- Override the per-order format mapping inline.

## Settings & fields

The Profics integration (per [[apps-profisc]]):
- Runs a credential validity check on save.
- Serialises the order into the Profics format before submitting it.

## Business rules

### Bulgarian POS focus

Profics primarily serves Bulgarian merchants with physical retail + online operations. Similar use case to [[apps-microinvest]] / [[apps-posmaster]].

### Permission
Standard apps permission scope.

## Related

- [[apps-profisc]] — hub (note slug typo: profisc).
- [[apps-microinvest]] / [[apps-posmaster]] / [[apps-selmatic]] — alternative BG ERP/POS apps.
- [[orders]] — orders synced.
- [[orders-history]] — sync events appear here.

## How it works (verified against backend)

### Cloud-hosted REST API (not on-prem)

Profisc is hosted by Profisc itself. Endpoints:
- Sandbox: `https://demoapi.profisc.al/`.
- Production: `https://onlineapi.profisc.al/`.

The merchant flips `test_mode` (1 = sandbox, 0 = live) in the Settings to switch.

### Required settings

Form validation requires: `username`, `password`, `country`, `seller`, `branch`, `tcr`. Additional optional: `op_code`, `send_order`, `test_mode`.

### Credential validation flow

The platform calls `POST public/authenticate` against the configured endpoint (test or live) with username + password + `isAgent: 0`. On success, the response includes a session token (used for subsequent requests). On failure, validation returns `false` and the merchant sees an error.

### NO inventory sync

Profisc is a FISCAL-INVOICING integration only — it submits order data for fiscal stamping. There's no product / stock / customer sync from Profisc to CloudCart. The merchant runs CloudCart's normal product / stock management; Profisc only receives finalized orders.

### Settings UI flow

The merchant configures Profisc in this order (the controller exposes specific endpoints):
1. Enter username + password → `apps.profics.api.validate` POST verifies credentials.
2. Pick country.
3. `apps.profics.api.company` GET returns the list of companies (sellers) the credentials have access to → merchant picks one.
4. `apps.profics.api.branches/{companyId}` returns branches for the selected company → merchant picks one.
5. `apps.profics.api.tcr/{companyId}/{branchId}` returns cash registers for the selected branch → merchant picks one.
6. Configure `send_order` + `test_mode` → save.

This step-by-step API-driven flow lets the merchant select from their actual Profisc account structure rather than typing IDs manually.

### Bulgarian-POS-focus note is incorrect — Profisc is ALBANIAN

The earlier "Bulgarian POS focus" paragraph is wrong: Profisc is the Albanian / SE-European fiscal-invoicing platform (profisc.al). The merchant verticals are Albania, Greece, Macedonia, Kosovo, Montenegro, Italy — NOT Bulgaria. See [[apps-profisc]] for the correct vertical breakdown.

### Per-order send endpoint

A `send-order/{orderId}` route exists (`apps.api.profics.send_order`) — lets the merchant manually trigger a Profisc submission for a specific order from the order page, independent of the auto-send-on-status trigger.

### Settings layout — 2-stage form

The merchant sees a TWO-STAGE form:

#### Stage 1 — Credentials card (always visible)

| Field | Type | Required | Error |
|---|---|---|---|
| **Username** | text | yes | "Invalid credentials" or per-field server error |
| **Password** | password (masked) | yes | "Invalid credentials" or per-field server error |
| **Test mode** | switch | no | toggles sandbox vs production endpoint |

Below the fields: a **Connect** button (with a loading spinner while it works). Hidden once the credentials validate.

#### Stage 2 — Settings row (only visible after credentials validate)

Renders as a preview card with a slide-modal edit. Preview shows Country / Seller / Branch / TCR / Operator code / Send Order status badge.

Edit modal contents — **CASCADING selects** with dependent visibility:

| Field | Type | Conditional visibility | API endpoint |
|---|---|---|---|
| **Country** (`country`) | searchable dropdown | always | options provided inline (6 country codes) |
| **Seller** (`seller`) | searchable dropdown | always (companies for the logged-in account) | `/admin/api/profics/company` |
| **Branch** (`branch`) | searchable dropdown | only when `seller` is set | `/admin/api/profics/branches/{sellerId}` |
| **TCR** (`tcr`) | searchable dropdown | only when `branch` is set | `/admin/api/profics/tcr/{sellerId}/{branchId}` |
| **Operator code** (`op_code`) | text | always | — |
| **Send Order** (`send_order`) | switch | always | — |

Each dropdown's options resolve live from the merchant's actual Profics-side account structure.

## Open questions

(none — questions about merchant-facing behaviour have been resolved against backend)
