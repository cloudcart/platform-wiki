---
type: feature
nav_path: "Apps → Szamlazz"
route_name: apps.szamlazz.overview
route_path: /admin/apps/szamlazz
aliases: ["Szamlazz", "Számlázz.hu", "Szamla", "Hungarian invoicing", "Szamlazz accounting", "enable disable button", "app active toggle"]
tags: [apps, erp, invoicing, hungary, accounting]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 2
---
# Szamlazz (Hungarian invoicing & accounting)

## Purpose

**Számlázz.hu** integration — Hungary's leading online invoicing service. When installed and activated, Szamlazz becomes the store's **active invoicing provider** — replacing CloudCart's built-in invoicing. Every order's invoice, credit note, and receipt is then generated through Szamlazz (which is what Hungarian tax law requires for e-commerce). Szamlazz assigns the legally-required, gap-free document number, reports the document to NAV (Hungary's real-time invoice system), and returns a PDF that the merchant can download from CloudCart.

For Hungarian merchants this is a near-mandatory app — without it, the platform's invoicing doesn't meet local tax requirements.

This page is the hub for the Szamlazz cluster. The deep mechanics are split into aspect pages (see **Sub-pages** below); this hub covers what the app is, where to find it, and the store-wide rules.

> **Has an on/off control.** The app screen carries an **Enable / Disable** button, so the merchant can switch it off without uninstalling it — a disabled app stops working while keeping its settings. The button is briefly absent while the screen is still loading its configuration; it appears once the settings arrive.

## Where to find it

Sidebar → **Apps** → install → **Szamlazz**.

The app has an Overview tab (status + quick-link to Settings) plus configuration and per-order tabs documented on the sub-pages.

## What the merchant can do here

- See Szamlazz installation status and whether it is the active invoicing provider.
- Jump to **Settings** to enter API credentials, pick a numbering sequence, choose invoice language / template, and set per-document-type automation — see [[apps-szamlazz-settings]].
- Issue / cancel / mark-paid an **invoice** per order — see [[apps-szamlazz-orders-invoice]].
- Issue a **credit note** (storno) on refund — see [[apps-szamlazz-orders-credit-note]].
- Issue a **receipt** for cash / non-tax-document scenarios — see [[apps-szamlazz-orders-receipt]].
- Let CloudCart drive Szamlazz automatically from order events, or keep each document type in manual mode for human review — see [[apps-szamlazz-automation]].

### What the merchant CANNOT do here

- Use Szamlazz without a Számlázz.hu account + paid subscription (the integration needs the merchant's own credentials).
- Run Szamlazz alongside another active invoicing provider — there is exactly **one** invoicing provider at a time per store.
- Bypass Hungarian numbering rules (Szamlazz enforces them server-side).

## Settings & fields

Credential entry, numbering-sequence selection, default language, PDF template, the per-document-type `active` / `generate` / `generate_status` settings, and the `credit_note.active` toggle all live on the Settings tab — fully documented on [[apps-szamlazz-settings]].

The store-wide field this app controls directly is `invoicing_provider`: activating Szamlazz sets it to `szamlazz`; deactivating / uninstalling reverts it to the previously-active provider (built-in or another invoicing app).

## Business rules

### Becomes THE invoicing provider on activation

Installing + activating Szamlazz immediately sets the store's `invoicing_provider` to `szamlazz` and bypasses the platform's built-in invoicing. Deactivating or uninstalling reverts to the previous provider. There is only ever one active invoicing provider per store. See [[settings-invoicing]].

### Hungarian legal compliance is handled by Szamlazz

Sequential gap-free numbering, real-time NAV reporting (Online Számla), document cancellation with audit trail, and Hungarian VAT rules are all enforced on the Szamlazz side. The merchant doesn't implement any of this.

### No document is ever deleted — only counter-recorded

When an invoice is cancelled, the original stays in Szamlazz's permanent audit and a counter-document (cancellation / credit note) is created alongside it. Whether a formal credit note is produced is controlled by the `credit_note.active` setting — see [[apps-szamlazz-operations]] for the full cancellation logic and the `credit_note.active = 0` "silent removal" branch.

### PDFs are stored on the order, base64-encoded

Issued PDFs are cached on the order record so the merchant can download instantly without a fresh API call. The trade-off is larger order records. See [[apps-szamlazz-operations]].

### All Szamlazz operations are synchronous (except auto-triggered ones)

Manual issue / cancel / pay actions call the Szamlazz API in real time, so a slow connection causes a merchant-side delay. Auto-triggered issuance runs as a background task off the order-events queue — see [[apps-szamlazz-automation]].

### Tax classification happens at invoice creation

For B2B buyers, Szamlazz validates the Hungarian tax number against NAV and the platform classifies the buyer (Hungarian / EU / non-EU), which drives the EU-VAT flag. This is decided at invoice-creation time, not at cart validation — see [[apps-szamlazz-localization]].

### Per-store account

Each store has its own Szamlazz app instance with its own API key (apps are scoped per store). A merchant running multiple stores connects each store separately. See [[apps-szamlazz-localization]].

### Permission

Standard apps permission scope.

## Sub-pages (in this cluster)

- [[apps-szamlazz-settings]] — Settings tab: API credentials, numbering sequence, default language, PDF template, per-document-type automation toggles.
- [[apps-szamlazz-orders-invoice]] — per-order invoice generation, cancel, and pay flow.
- [[apps-szamlazz-orders-credit-note]] — per-order credit-note (storno) flow on refund.
- [[apps-szamlazz-orders-receipt]] — per-order receipt flow (cash / proof of payment).
- [[apps-szamlazz-operations]] — document mechanics: the three document types, per-document order-meta fields, PDF-on-meta storage, cancellation → credit-note logic (`credit_note.active`), pay-invoice flow, error handling.
- [[apps-szamlazz-automation]] — auto-generation from order events; per-document `active` / `generate` / `generate_status`; manual vs auto mode; auto pay / cancel on status change.
- [[apps-szamlazz-localization]] — multi-currency support, the 8 invoice languages, the 5 PDF templates + extra logo, NAV taxpayer-status classification, per-store account model.

## Related

- [[apps]] — App Store.
- [[invoicing-and-accounting]] — the platform-wide invoice / receipt / credit-note + accounting-integration concept this app plugs into.
- [[settings-invoicing]] — invoicing-provider configuration (Szamlazz overrides this).
- [[orders-invoice]] — generic invoice flow that delegates to Szamlazz when active.
- [[orders-credit]] — generic credit-note flow.
- [[orders-receipt]] — generic receipt flow.
- [[apps-fgo]] / [[apps-smart-bill]] / [[apps-flix-facts]] — alternative invoicing apps for non-HU markets.
- [[order]] — entity page.

## Open questions

(none — questions about merchant-facing behaviour have been resolved against backend)
