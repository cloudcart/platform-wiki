---
type: feature
nav_path: "Apps → Szamlazz → Settings (automation)"
route_name: apps.szamlazz.overview
route_path: /admin/apps/szamlazz
aliases: ["Szamlazz automation", "Szamlazz auto invoice", "Szamlazz auto generate", "Szamlazz manual vs auto", "Szamlazz order events", "Szamlazz generate_status"]
tags: [apps, erp, invoicing, hungary, accounting]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[apps-szamlazz]]. See the hub for the other aspects (settings, per-order invoice / credit-note / receipt flows, document mechanics, localization).

# Szamlazz — automation from order events

## Purpose

This aspect documents how CloudCart can **drive Szamlazz automatically from order events** so the merchant never has to click "Create document" by hand. It covers the per-document-type automation settings, the three order events that can trigger issuance, the conditions that must all be true, and the automatic pay / cancel flows on status change — plus how to switch a document type back to manual review.

## Where to find it

The automation switches live on the Settings tab (Sidebar → **Apps** → **Szamlazz** → Settings — see [[apps-szamlazz-settings]]). Once configured, the behaviour fires from the order side with no further merchant action.

## What the merchant can do here

- Turn auto-generation on or off **per document type** (invoice, receipt).
- Choose, per document type, the exact order statuses at which the document should be generated.
- Keep a document type in **manual** mode so a human reviews each order before issuance.
- Let invoices be marked paid and documents be cancelled automatically as the order moves through `paid` / `completed` / `refunded` / `cancelled`.

## Settings & fields

Automation is configured per document type via three settings (`<type>` is `invoice` or `receipt`):

| Setting | Meaning |
|---|---|
| `<type>.active` | `1` = this document type is enabled at all. |
| `<type>.generate` | `auto` = generate automatically from order events; `manual` = merchant clicks to generate. |
| `<type>.generate_status` | The merchant-configured list of order statuses at which auto-generation should fire. |

These are set on [[apps-szamlazz-settings]].

## Business rules

### Auto-generation triggers (invoice + receipt)

The platform watches three order events: **order created**, **order status change**, and **fulfillment added**. On each event, and for each document type, it auto-generates the document only when **all** of these hold:

- `<type>.active == 1` — the document type is enabled, AND
- `<type>.generate == 'auto'` — auto mode is on, AND
- the order's current status is in `<type>.generate_status`, AND
- no document of that type already exists on the order.

When all are true, the platform queues a background task (on the order-events queue, retried up to 5 times) that issues the invoice or receipt. Because issuance runs as a queued background task rather than inline, a busy queue can introduce a short delay before the document appears on the order; a Szamlazz error is retried automatically up to the attempt limit and otherwise surfaces as `szamlazz_<type>_error` (see [[apps-szamlazz-operations]]).

### Auto pay-invoice on status change

When an order's status becomes `paid` or `completed` and the order already has an invoice that isn't yet marked paid, the platform automatically runs pay-invoice (sets the Szamlazz invoice to PAID). See [[apps-szamlazz-operations]] for the pay-invoice mechanics.

### Auto cancel on status change

When an order's status becomes `refunded` or `cancelled` and the order has an issued document, the platform automatically cancels the invoice / receipt. For invoices, the cancel result follows the `credit_note.active` branching described in [[apps-szamlazz-operations]] — a credit note is created when that setting is `1`.

The net effect: with both document types in `auto` mode and sensible `generate_status` lists, the merchant can let CloudCart fully drive the Szamlazz document lifecycle (issue → pay → cancel/credit-note) end-to-end with no manual action for typical orders.

### Manual mode (per document type)

Setting `<type>.generate = 'manual'` disables all auto-creation for that document type. The merchant then issues the document by hand from [[apps-szamlazz-orders-invoice]] / [[apps-szamlazz-orders-receipt]]. This is the right choice when the merchant wants to review each order (e.g., confirm the buyer's tax number) before a legally-numbered document is committed. The auto pay / cancel behaviours above still depend on a document already existing, so manual issuance + automatic pay/cancel is a valid mix.

## Related

- [[apps-szamlazz]] — hub.
- [[apps-szamlazz-settings]] — where `active` / `generate` / `generate_status` are configured.
- [[apps-szamlazz-operations]] — what issuance / pay / cancel actually record on the order.
- [[apps-szamlazz-orders-invoice]] — manual invoice issuance.
- [[apps-szamlazz-orders-receipt]] — manual receipt issuance.
- [[orders-status-change]] — order status transitions that trigger automation.
- [[order]] — entity page.

## Open questions

(none — resolved against backend)
