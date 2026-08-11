---
type: feature
nav_path: "Apps → Szamlazz → Settings"
route_name: apps.szamlazz.settings
route_path: /admin/apps/szamlazz/settings
aliases: ["Szamlazz Settings", "Szamlazz credentials", "Szamlazz config", "Számlázz settings"]
tags: [apps, administration, szamlazz, invoicing, settings, hungary]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 2
---
# Szamlazz → Settings

## Purpose

The **Settings** tab is where the merchant connects CloudCart to their Számlázz.hu account by entering their **API key** (`apiKey`), validates it against Szamlazz, and configures the per-document-type defaults. Saving valid credentials makes Szamlazz the active store-wide **invoicing provider** (`invoicing_provider = szamlazz`) and unlocks the per-order tabs ([[apps-szamlazz-orders-invoice]] / [[apps-szamlazz-orders-credit-note]] / [[apps-szamlazz-orders-receipt]]).

This page documents the Settings **screen itself** — the connect-and-validate flow and the box layout. The meaning of the document-config fields is owned by the cluster aspects: [[apps-szamlazz-automation]] for `generate` / `generate_status`, [[apps-szamlazz-localization]] for language / template / currency, [[apps-szamlazz-operations]] for `credit_note.active`. For the whole feature, see the hub [[apps-szamlazz]].

## Where to find it

Sidebar → Apps → Szamlazz → **Settings tab**. Route: `/admin/apps/szamlazz/settings`.

API routes: `GET /api/szamlazz/settings` (load), `POST /api/szamlazz/settings` (save), `GET/POST /api/szamlazz/validate` (validate the API key against Szamlazz).

## What the merchant can do here

- Enter the **API key** (`apiKey`) and validate-then-save it.
- Once validated, configure each document type — enable it (`active`), set manual vs auto issuance and the trigger statuses (see [[apps-szamlazz-automation]]), set prefix / comment, and pick invoice language and PDF template (see [[apps-szamlazz-localization]]).
- Toggle `credit_note.active` to control what cancelling an invoice does (see [[apps-szamlazz-operations]]).

### What the merchant CANNOT do here
- Use Szamlazz without a paid Számlázz.hu subscription + API access enabled.
- Activate Szamlazz alongside another invoicing provider — only ONE invoicing provider can be active at a time per store.
- Bypass validation — an invalid API key blocks save, and the document-config boxes stay locked until the key validates.

## Settings & fields

### The four boxes (sequential, lock until the key validates)

The page renders four boxes in order. Boxes 2–4 are **locked and hidden** until the API key validates (see the box-lock rule below).

| Box | Fields | Aspect that owns the field meaning |
|---|---|---|
| **1 — Szamlazz connect** | `apiKey` + the embedded ValidateAndSave button | this page |
| **2 — Receipt settings** | `receipt.active`, `receipt.prefix`, `receipt.comment`, `receipt.generate` (Manual / Auto), `receipt.generate_status` | [[apps-szamlazz-automation]] |
| **3 — Invoice settings** | `invoice.active`, `invoice.language`, `invoice.prefix`, `invoice.comment`, `invoice.template`, `invoice.generate`, `invoice.generate_status`, `invoice.extra_logo` | language / template → [[apps-szamlazz-localization]]; generate → [[apps-szamlazz-automation]] |
| **4 — Credit note settings** | `credit_note.active` | [[apps-szamlazz-operations]] |

`prefix` / `comment` are an optional document-number prefix and free-text comment per document type. The conditional-visibility chain (the secondary fields appear only when the box's `active` switch is `1`, and `generate_status` only when `generate = auto`) and the auto-reset of `generate` / `generate_status` when a box is switched off are detailed in [[apps-szamlazz-automation]]. The 8 invoice languages, 5 PDF templates, `extra_logo`, and order-derived currency are detailed in [[apps-szamlazz-localization]].

### ValidateAndSave button + live-watch

The connect box embeds a **ValidateAndSave** button that validates the key, then (if valid) saves. The button is hidden only when the app is already configured AND the credentials are unchanged AND currently valid; any change re-shows it. A live-watch on `connect.apiKey` re-validates in the background as the merchant edits the key, so "Valid" / "Invalid" feedback appears before they click Save.

### API key validation flow

Validation calls the Szamlazz tax-payer lookup with a fixed test tax number (`13421739-2-13`). If that call succeeds the key is accepted and saved; if it fails the merchant sees an unprocessable-entity error surfaced on the `apiKey` field. The same check is exposed as a GET (against the currently-saved key) — that is what the live-watch fires.

### What happens on save

The platform clears the existing settings, re-saves the submitted values, and (if a logo was uploaded) base64-encodes it with a `data:image/<type>;base64,...` mime prefix into `invoice.extra_logo`, then returns the new settings to the UI. The API key is persisted encrypted.

## Business rules

### Box-lock dependency chain

The merchant must complete Box 1 (validate the API key) before any document-config box becomes editable. Whenever the credentials are changed or not yet valid, Boxes 2/3/4 stay locked and hidden; they unlock only on a valid, unchanged key.

### Activation sets `invoicing_provider`

Flipping a document type's `active` to `1` activates the app and sets the store-wide `invoicing_provider` to `szamlazz`, routing all order-side invoice generation through Szamlazz; deactivating reverts to the previous provider (built-in `platform` invoicing). See [[apps-szamlazz]] and [[settings-invoicing]].

### Activation blocks concurrent invoicing providers

Activation is allowed only when the current `invoicing_provider` is already `szamlazz`, or when no invoicing app is active and the store is on built-in invoicing. Otherwise it is BLOCKED with "Invoicing is not available for the selected provider." A merchant on another invoicing app (e.g. [[apps-fgo]], [[apps-smart-bill]], [[apps-flix-facts]]) must deactivate that app FIRST.

### Migration from another invoicing provider

After switching to Szamlazz, documents already issued by the previous provider stay attached to their historic orders (their old-prefix meta remains); only new orders use Szamlazz. Past invoices cannot be re-issued under Szamlazz numbering — they keep their original provider numbering for tax-audit purposes.

### Permission
Standard apps permission scope.

## Related

- [[apps-szamlazz]] — Szamlazz hub.
- [[apps-szamlazz-automation]] — `generate` / `generate_status`, manual vs auto, auto pay/cancel.
- [[apps-szamlazz-localization]] — invoice language, PDF template, currency, taxpayer classification.
- [[apps-szamlazz-operations]] — document mechanics, `credit_note.active` cancellation branching, PDF storage.
- [[apps-szamlazz-orders-invoice]] — per-order invoice flow.
- [[apps-szamlazz-orders-credit-note]] — per-order credit note flow.
- [[apps-szamlazz-orders-receipt]] — per-order receipt flow.
- [[settings-invoicing]] — invoicing provider store-wide config.
- [[apps-fgo]] / [[apps-smart-bill]] / [[apps-flix-facts]] — alternative invoicing apps.

## Open questions

(none — questions about merchant-facing behaviour have been resolved against backend)
