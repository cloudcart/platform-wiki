---
type: feature
nav_path: "Apps → FGO → Settings"
route_name: apps.fgo.settings
route_path: /admin/apps/fgo/settings
aliases: ["FGO Settings", "FGO credentials", "FGO config"]
tags: [apps, administration, fgo, invoicing, settings, bulgaria]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 2
---
# FGO → Settings

## Purpose

The **Settings** tab is where the merchant connects CloudCart to their **FGO** (Bulgarian online invoicing) account — enters API credentials, sets up document numbering series, configures defaults. See [[apps-fgo]] for the full feature set.

## Where to find it

Sidebar → Apps → FGO → **Settings tab**. Route: `/admin/apps/fgo/settings`.

## What the merchant can do here

### Credentials

| Field | Notes |
|---|---|
| **FGO API credentials** | Username + password OR API key from the merchant's FGO portal. |

When the merchant saves credentials, CloudCart connects to FGO with the supplied values and verifies they are valid before storing them (per [[apps-fgo]]).

### Document numbering

| Field | Notes |
|---|---|
| **Series** | FGO uses series + number identification (e.g., series "A" + number 12345). The merchant can configure: |
| - **Invoice series** | Series for normal invoices. |
| - **Credit note series** | Separate series for credit notes (per Bulgarian accounting practice). |
| **Starting number** | Where the sequence begins. |

### Default behaviour

| Setting | Notes |
|---|---|
| **Auto-generate on Paid** | Issue invoice automatically when order hits Paid status. |
| **Auto-send email** | Email the customer the invoice PDF. |
| **Language for invoices** | EN / BG. |

### Activate as invoicing provider

Once credentials are valid, the merchant activates FGO → becomes the store's `invoicing_provider` (per [[apps-fgo]]).

### What the merchant CANNOT do here
- Use FGO without an FGO subscription.
- Activate FGO alongside another invoicing provider (single-provider model).
- Edit historical FGO-issued documents — Bulgarian tax law forbids.

## Settings & fields

The FGO integration (per [[apps-fgo]]) supports:
- App Store metadata for the listing.
- A credential validity check on save.
- Geographic lookups (country / state / city codes) used when building documents.
- Issuing an invoice for an order.
- Cancelling a document by its number + series.

## Business rules

### Number + Series identification

FGO documents are identified by series (prefix) + number (sequential within series). This is legacy Bulgarian accounting practice — different from Szamlazz's single-number model.

### NAP compliance

Per [[apps-fgo]]: FGO handles Bulgarian National Revenue Agency (NAP) reporting requirements. Without FGO active, the merchant must handle this manually.

### Permission
Standard apps permission scope.

## Related

- [[apps-fgo]] — hub.
- [[apps-szamlazz]] / [[apps-smart-bill]] / [[apps-flix-facts]] — alternative invoicing apps.
- [[apps-n18-audit]] — Bulgarian fiscal-audit compliance (sister concern).

## How it works (verified against backend)

### Required save fields

The settings form mandates ALL of the following:
- `password` — FGO API password.
- `merchant_name` — merchant identifier on FGO.
- `unique_code` — FGO unique code (CodUnic).
- `platform_url` — FGO platform URL.
- `environment` — `production` or `test` (validated `in:production,test`).
- `invoice_type` — one document type from the 13 allowed values (see [[apps-fgo]] table).
- `seria` — ONE document series prefix.

If the merchant tries to activate FGO with any field missing, save is blocked with a validation message.

### Test mode IS supported

Per the `environment` field validator (`in:production,test`), FGO has a separate test environment. The merchant flips this field to `test` for sandbox testing without affecting production-numbered invoices. Switching back to `production` resumes live numbering. Useful for the merchant to verify the integration before going live.

### Credential validation hits FGO API live

When the merchant saves credentials, the platform constructs an FGO API client with the supplied values and tries listing articles. If FGO accepts, credentials are saved; if not, the merchant sees "Invalid credentials".

### Single document type and series per merchant

The settings model holds ONE `invoice_type` and ONE `seria` field globally — not per order, not per document type. To issue different document types (e.g., proforma vs invoice) the merchant must change the global setting, issue the document, then change back. There's no per-order document-type override in the UI.

For credit notes / cancellations, FGO uses the SAME series — cancelling deletes the document (which removes it at FGO and clears the stored reference in CloudCart). There's no separate credit-note series concept in this integration.

### No bulk re-issuance

The FGO integration only exposes per-order actions (generate document, cancel document). There's no bulk re-issuance for historical orders. To backfill, the merchant must trigger generation per order one at a time.

### Multi-series configuration

The merchant configures ONE `seria` per store at any given time. To use multiple series within a calendar year (e.g., switch series after a numbering reset), the merchant changes the `seria` setting in the Settings tab — future documents use the new series. CloudCart doesn't track series transitions; the merchant's FGO portal does.

### `is_billing_address` skip condition

When `is_billing_address = 1` AND the order has NO billing address, auto-generation is **skipped silently** (no error, no history entry). The merchant won't see the order pass through FGO — they must add a billing address (or disable this gate) for the document to issue. Useful to prevent generating B2C invoices without proper buyer data.

### Two extra body-text fields

The Settings form persists `text` and `additional_text` — merchant-defined snippets that FGO embeds into the invoice body. The Settings UI exposes them as free-text inputs.

### Settings form structure (2-box accordion)

The merchant sees **TWO sequential boxes**:

#### Box 1 — "Fgo connect" (credentials)

Renders inline (no slide modal) until credentials are first validated; afterwards switches to slide-modal mode. Fields:

| Field | Type | Label | Notes |
|---|---|---|---|
| `connect.password` | string | "API Password" | required |
| `connect.unique_code` | string | "Company unique code" | required; help: "Your company's unique identification code" |
| `connect.merchant_name` | string | "Merchant name" | required |
| `connect.platform_url` | string | "URL address" | required |
| `connect.environment` | select | "Mode" | required; 2 options: **Sandbox** (`test`) / **Production** (`production`) |
| Validate-and-save action | embedded button | — | "Validate credentials and save" button; visible while credentials are being changed |

The form has a `live-watch` on the 5 connect-fields — changing any one re-locks the second box (forces re-validation).

#### Box 2 — "Fgo settings" (document config)

Hidden until credentials are validated. Slide-modal edit. Fields:

| Field | Type | Label | Conditional visibility |
|---|---|---|---|
| `invoice_type` | select (loaded live from `/admin/api/fgo/invoice-types`) | "Document type" | always; resolveOnLoad |
| `seria` | string | "Series" | always |
| `text` | string | "Text" | always |
| `additional_text` | string | "Additional information" | always |
| `automate_generate` | switch (1/0) | "Automatic document creation" | always |
| `is_billing_address` | switch (1/0) | "Generate invoice only if billing address is provided" | only when `automate_generate = 1` |
| `order_status` | select | "Create document in FGO when order status is" | only when `automate_generate = 1`; 4 options: New order / Paid / Completed / Fulfilled |

### Box-lock behaviour

When credentials change (live-watch fires), Box 2 ("Fgo settings") becomes locked + hidden until the merchant clicks "Validate credentials and save" in Box 1. This prevents the merchant from editing document-template settings against unvalidated credentials.

## Open questions

(none — questions about merchant-facing behaviour have been resolved against backend)
