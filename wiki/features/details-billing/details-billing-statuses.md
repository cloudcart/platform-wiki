---
type: feature
nav_path: "Details → Billing → Statuses"
route_name: billing-list
route_path: /admin/details/billing
aliases: ["Billing transaction statuses", "Approved code mapping", "Failed vs Voided vs Refunded", "Transaction status badge", "Статус на транзакция"]
tags: [accountdetails, details, billing, transactions, status]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---
# Billing — transaction statuses

> Part of [[details-billing]]. See the hub for related aspects (transaction list, invoice download, retry schedule).

## Purpose

This aspect documents what each transaction **status** means on the *Details → Billing* tab: the four-state `approved` code, the coloured badge each maps to, the semantic difference between *Failed*, *Voided*, and *Refunded*, and the fact that voids / refunds only ever appear here when CloudCart support runs them. Knowing these states answers the common merchant question *"what does this red / blue badge on my charge mean?"*.

## Where to find it

- **Details (sidebar) → Billing** tab — the Status column on each row, and the **Status** filter dropdown above the table.
- URL pattern: `/admin/details/billing`.

## What the merchant can do here

- **Read the status badge** on each transaction row.
- **Filter by status** — the dropdown filter values map directly to the `approved` codes (`0` / `1` / `2` / `3`) and are passed straight to the backend as `filters[approved]=N`. Applying the filter re-fetches from page 1.

## What the merchant cannot do here

- **Change a transaction's status** — the merchant cannot mark a charge as voided / refunded / paid. Status transitions are driven by the gateway (at charge time) or by CloudCart support (for after-the-fact voids / refunds).

## Settings & fields

### Approved code mapping

| Code | Status | Badge colour | Badge class |
|------|--------|--------------|-------------|
| 0 | Failed / Unpaid | red | `cc-tag-status--required` |
| 1 | Success / Paid | green | `cc-tag-status--enabled` |
| 2 | Voided | red | `cc-tag-status--required` |
| 3 | Refunded | blue | `cc-tag-status--update` |

### Status filter

The dropdown exposes the same four values, labelled *Unpaid* (`0`), *Paid* (`1`), *Voided* (`2`), *Refunded* (`3`). The option values are stringified codes passed verbatim to the backend.

### Localised status label

The visible label (`status_name`) is produced server-side from the `approved` code and localised to the merchant's admin-panel language — e.g. *Успех* (BG) vs *Success* (EN).

## Business rules

### `Voided` vs `Failed` vs `Refunded`

- **Failed** — an unsuccessful charge attempt (declined by the gateway). No money moved.
- **Voided** — a previously-successful charge that was reversed by CloudCart **before settlement** (typically a same-day correction).
- **Refunded** — a **settled** charge that was refunded **after** settlement.

### Refunds / voids only surface when CloudCart support runs them

Refund and void operations are performed by support agents through internal gateway tools. Once executed, the original transaction's `approved` flips to `3` (Refunded) or `2` (Voided), and a related entry may also be created. The merchant sees the status change appear on the row without taking any action — there is no self-serve void / refund in the admin UI.

### Status reflects the moment of the attempt

A row's status is the outcome of that specific attempt. A failed renewal followed by a successful retry produces two separate rows — one *Failed*, one *Success* — not a single row that flips. See [[details-billing-retry-schedule]] for how the retry sequence generates these rows.

## Related

- [[details-billing]] — hub.
- [[details-billing-transaction-list]] — the table where the Status column + filter render.
- [[details-billing-invoice-download]] — only *Paid* (`approved == 1`) rows expose a Download link.
- [[details-billing-retry-schedule]] — how a sequence of *Failed* rows then a *Success* row is generated.
- [[expired-subscription]] — what repeated *Failed* statuses eventually trigger.

## Open questions

(All resolved.)
