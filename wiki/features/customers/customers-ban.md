---
type: feature
nav_path: "Customers → Ban flow"
route_name: customers-list.new
route_path: /admin/customers-new
aliases: ["Ban customer", "Unban customer", "Customer ban", "Banned customers", "Ban reason", "Remove ban", "banned_reason", "date_banned"]
tags: [customers, ban, moderation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customers]]. See the hub for the other aspects (list view, filters, bulk actions, create modal, flags, lifetime KPIs).

# Customers — Ban flow

## Purpose

The merchant's disciplinary lock on a customer account. Ban prevents login AND order placement. This aspect documents the ban modal (required reason), the per-customer ban from the detail-page header, the `banned` / `date_banned` / `banned_reason` fields, the unban-clears-both rule, and the relationship to the distinct order-IP ban concept.

## Where to find it

- Customer detail page header (`/admin/customers-new/details/:id`) → **Ban customer** action → modal.
- Customer detail page header → **Remove ban** action (visible when banned) → spinner + clear.
- Customer list bulk actions → **Ban customer/s** / **Remove ban** — see [[customers-bulk-actions]] (modern bulk Ban handler is currently a stub).
- Banned status surfaces as a **"Banned"** chip next to the customer name on [[customers-details]].

## What the merchant can do here

### Per-customer ban (detail page)

When viewing `/admin/customers-new/details/:id`, the page header surfaces:

- **Ban customer** — opens the Ban modal with a required textarea (see below).
- **Remove ban** — visible when the customer is banned; clears the ban (with spinner during the call).
- Dropdown menu → **Delete customer** — see [[customers-bulk-actions]] for the delete confirm copy and [[customers-lifetime-kpis]] for the deletion cascade.
- Status badge: **"Banned"** chip is shown next to the customer name when applicable.

### Ban modal — required reason

When the merchant clicks Ban (either bulk or per-customer), a modal opens with:

- Explanation text: *"Short explanation what banning a customer means. Provide info about how the ban can be removed."*
- **Ban reason** textarea — REQUIRED. Placeholder: *"Please describe the reason for banning this customer. Keep in mind that the reason will be set to your customer via email"* (suggesting the reason is communicated to the customer when implemented).
- Confirm button is **disabled until the reason is non-empty**.
- Confirmation styled as a danger action (red).

## Settings & fields

### Customer status fields — verified

The Customer model has these status-related fields:

- `banned` — boolean (stored as `0` / `1`).
- `date_banned` — timestamp when banned.
- `banned_reason` — free-text reason.
- `active` — boolean (separate flag — see [[customers-flags]]). When false, throws `'sf.err.account.inactive'` error on login.

### the platform code — verified

Per the model method (lines 1572-1588):

```
if ($banned):
   set date_banned = now
   set banned_reason = $reason
else:
   set date_banned = null
   set banned_reason = null
set banned = (banned ? 1: 0)
update WHERE id IN (array)$id
```

Key findings:

- Accepts a SINGLE id OR an ARRAY of ids — supports bulk operations from the same method.
- Unbanning clears both `date_banned` AND `banned_reason`.
- Banning preserves the reason for audit purposes.

The docstring claims: *"Function also sends a notification for the banned status to the customer along with the reason"*. But the ban-action body itself does NOT trigger any email — the notification is presumably wired through a model observer / event listener elsewhere. (verify)

## Business rules

### Ban requires a reason

Every ban action (bulk or single) requires a non-empty reason in the modal. The reason is stored on the customer record (`banned_reason`) and shown to admins on the [[customers-details]] page. The placeholder text indicates the reason is also intended to be communicated to the customer (via email — verify whether currently implemented).

### Unban clears both fields

The Remove ban action sets `banned=no` AND clears `banned_reason`. There is no audit history of past bans / unbans visible to the merchant from this page.

### Banned customers cannot log in OR place orders

Banned is the strictest disciplinary state — both storefront login and order placement are blocked. Contrast with `active = false`, which blocks login only and throws `'sf.err.account.inactive'` — see [[customers-flags]] for the cascade rule (banning doesn't auto-deactivate, deactivating doesn't auto-clear marketing consent).

### Distinct from order-IP ban

The `banned` flag locks a customer **account**. To reject orders by source IP regardless of which customer account they come from, the merchant uses [[settings-banned-ip]] — a separate concept on the settings side.

### Banned visibility for restricted moderators

Per [[settings-staff]] restrictions, moderators may see only customers in specific groups. Moderators **without the Banned grant** may still see banned customers in the list but won't have ban/unban buttons. (verify: full grant name + whether banned rows are hidden or just non-actionable)

### Toast copy

- Ban success → (verify) toast string.
- Unban success → *"Unbanned successfully"*.

## Related

- [[customers]] — hub.
- [[customers-details]] — surfaces the **Banned** chip and the ban-reason card.
- [[customers-flags]] — the three independent flags (Active, Banned, Accept marketing) and the no-cascade rule.
- [[customers-bulk-actions]] — bulk Ban / Remove ban (modern bulk Ban handler is a stub).
- [[customers-lifetime-kpis]] — bulk password-reset skips banned customers; deletion cascade.
- [[settings-banned-ip]] — distinct order-IP-level rejection.
- [[settings-staff]] — moderator grants affecting ban visibility.
- [[settings-hooks]] — `customer.updated` webhook fires on ban / unban.

## Open questions

- Does the platform currently send the email-to-customer notification on ban? (placeholder text says so; ban-action body doesn't trigger it — verify the observer / listener)
- Exact toast string on successful ban. (verify)
- Banned visibility for restricted moderators: row hidden vs row non-actionable? (verify)
