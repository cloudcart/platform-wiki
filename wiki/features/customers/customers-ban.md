---
type: feature
nav_path: "Customers → Ban flow"
route_name: customers-list
route_path: /admin/customers
aliases: ["Ban customer", "Unban customer", "Customer ban", "Banned customers", "Ban reason", "Reason for customer ban", "Remove ban", "banned_reason", "date_banned"]
tags: [customers, ban, moderation]
plan_gates: []
created: 2026-06-10
updated: 2026-11-03
source_count: 3
---

> Part of [[customers]]. See the hub for the other aspects (list view, filters, bulk actions, create modal, flags, lifetime KPIs).

# Customers — Ban flow

## Purpose

The merchant's disciplinary lock on a customer account. Ban prevents login AND order placement. This aspect documents the ban modal (required reason), the per-customer ban from the detail-page header, the `banned` / `date_banned` / `banned_reason` fields, the unban-clears-both rule, and the relationship to the distinct order-IP ban concept.

## Where to find it

- Customer detail page header (`/admin/customers/details/:id`) → **Ban customer** action → modal.
- Customer detail page header → **Remove ban** action (visible when banned) → spinner + clear.
- Customer list **Tools** menu → **Ban customer/s** / **Remove ban** — see [[customers-bulk-actions]].
- Banned status surfaces as a **"Banned"** chip in the header of [[customers-details]], and as a **Banned** badge in the list's **Status** column. Clicking that badge opens the popup *"Reason for customer ban"*.

## What the merchant can do here

### Per-customer ban (detail page)

When viewing `/admin/customers/details/:id`, the page header surfaces:

- **Ban customer** — opens the Ban modal with a required textarea (see below).
- **Remove ban** — visible when the customer is banned; clears the ban (with spinner during the call).
- Dropdown menu → **Delete customer** — see [[customers-bulk-actions]] for the delete confirm copy and [[customers-lifetime-kpis]] for the deletion cascade.
- Status badge: **"Banned"** chip in the page header when applicable.

### Ban window on the customer's page

- Title *"Ban customer"*.
- Explanation text: *"Short explanation what banning a customer means. Provide info about how the ban can be removed."*
- **Ban reason** textarea — REQUIRED. Placeholder: *"Please describe the reason for banning this customer. Keep in mind that the reason will be set to your customer via email"*.
- **No** and **Yes**. **Yes** is disabled until the reason is non-empty.

The list's **Ban customer/s** window has its own wording; see [[customers-bulk-actions]].

## Settings & fields

### Customer status fields — verified

The Customer model has these status-related fields:

- `banned` — boolean (stored as `0` / `1`).
- `date_banned` — timestamp when banned.
- `banned_reason` — free-text reason.
- `active` — boolean (separate flag — see [[customers-flags]]). When false, throws `'sf.err.account.inactive'` error on login.

### What banning and removing a ban store

Banning stores the date and the reason. Removing a ban clears both. Both act on one customer or on a whole selection.

## Business rules

### Ban requires a reason

Every ban action (bulk or single) requires a non-empty reason. It is stored on the customer record (`banned_reason`) and shown to admins on the [[customers-details]] page and in the list's popup. The customer sees it in the message shown when they try to log in or check out: *"Account has been suspended due to {reason} on {date}"*. The ban itself sends no email.

### Unban clears both fields

The Remove ban action sets `banned=no` AND clears `banned_reason`.

### Banned customers cannot log in OR place orders

Banned is the strictest disciplinary state — both storefront login and order placement are blocked, with the message above. Contrast with `active = false`, which blocks login only and throws `'sf.err.account.inactive'` — see [[customers-flags]] for the cascade rule (banning doesn't auto-deactivate, deactivating doesn't auto-clear marketing consent).

### Distinct from order-IP ban

The `banned` flag locks a customer **account**. To reject orders by source IP regardless of which customer account they come from, the merchant uses [[settings-banned-ip]] — a separate concept on the settings side.

### Toast copy

- On the customer's page: *"Customer banned successfully"* and *"Ban removed successfully"*.
- On the list: *"Banned successfully"* and *"Unbanned successfully"*.

## Related

- [[customers]] — hub.
- [[customers-details]] — surfaces the **Banned** chip and the ban-reason card.
- [[customers-flags]] — the three independent flags (Active, Banned, Accept marketing) and the no-cascade rule.
- [[customers-bulk-actions]] — bulk Ban / Remove ban.
- [[customers-lifetime-kpis]] — bulk password-reset skips banned customers; deletion cascade.
- [[settings-banned-ip]] — distinct order-IP-level rejection.

## Open questions

None.
