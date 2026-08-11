---
type: feature
nav_path: "Customers → Bulk actions"
route_name: customers-list.new
route_path: /admin/customers-new
aliases: ["Customers bulk actions", "Bulk ban customers", "Bulk delete customers", "Bulk change customer group", "Bulk change password customers"]
tags: [customers, list, bulk-actions]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[customers]]. See the hub for the other aspects (list view, filters, create modal, ban flow, flags, lifetime KPIs).

# Customers — Bulk actions

## Purpose

The merchant multi-selects rows in the list and applies one action to all of them — bulk ban, bulk unban, bulk group reassign, bulk password reset, bulk delete. This aspect documents each action, the modal it opens, the endpoint it hits, AND the status of the modern Vue handler (several are stubs in the current build; the working flow lives in the legacy index).

## Where to find it

Sidebar → **Customers** → multi-select checkbox column → bulk-action dropdown appears. Route: `/admin/customers-new`.

## What the merchant can do here

### Bulk-action menu

| Action | What it does |
|--------|--------------|
| **Ban customer/s** | Opens a ban modal (the merchant enters a **required ban reason** before confirmation). Banned customers cannot log in or place orders. (Modern Vue handler is a stub — see Business rules below.) See [[customers-ban]] for the modal. |
| **Remove ban** | Clears the banned flag and the stored ban reason for all selected customers. Toast: *"Unbanned successfully"*. |
| **Change customer's group** | Opens a modal to reassign all selected to a different customer group (loyalty tier). (Modern Vue handler is a stub — see Business rules below.) |
| **Change password** | INTENDED: triggers password-reset emails for the selected customers (link to set a new password). **In the modern build this handler is an unimplemented stub — clicking it does nothing.** |
| **Delete** | Permanent. Confirmation: *"Are you are sure you want to delete? Caution: This action cannot be undone."* |

### Bulk delete confirm modal

Triggered by the bulk **Delete** action.

- Centered confirmation modal (CcConfirmModal).
- Title: *"Delete customer"*.
- Message: *"Are you are sure you want to delete? Caution: This action cannot be undone."*
- Confirm button rendered in red (`confirm-button-variant="danger"`).
- Spinner during request; OK only fires when not loading.
- Failure: toast *"Error while deleting customer"*. Success: toast *"Deleted successfully"*.

### Bulk change-customer-group modal

The modal opens via the bulk **Change customer's group** action. In the current modern Vue build the handler is a stub (`console.log('Open change group modal')` placeholder — the working flow lives in the legacy index). Expected behaviour from the legacy build:

- Single dropdown for the target group, populated from `GET /admin/api/core/customers/groups`.
- Confirm → all selected customer IDs move to the picked group; each customer triggers a `customer.updated` webhook; no email to the customer.

### Bulk ban modal — required reason

The bulk **Ban customer/s** action's modern handler in the new Vue listing is also a stub (`console.log('Open ban modal')`). The single-customer ban from the detail page IS implemented in the modern UI and matches the modal documented in [[customers-ban]]. The legacy bulk-ban runs through the same `ConfirmModal` with the textarea (legacy `CustomersIndex` — `confirmPopupKey = 'ban'` opens the same modal with the textarea + danger button).

### Bulk password-reset (NOT wired in the modern build)

In the modern Vue listing the bulk **Change password** action's handler is an empty stub (a `// TODO: Implement change password bulk` placeholder — it does NOT send any request yet). So clicking it in the modern list does nothing. The success-toast string *"A link to reset your password has been sent to your email address"* is pre-wired on the action but never fires because no request is made.

The INTENDED behaviour (verified in the legacy list / backend) is:

- No confirmation modal.
- A POST to `/admin/api/core/customers/change-password-bulk` for each selected customer.
- Silent skip on guest + banned customers (server-side — see Business rules below).
- Until the modern handler ships, true bulk password-reset must be done from the legacy `/admin/old-customers` list.

## Settings & fields

The bulk actions reuse modals documented on sibling aspects:

- Ban modal field set → [[customers-ban]].
- Delete confirmation copy → above.
- Change-group dropdown → populated from `GET /admin/api/core/customers/groups` ([[customers-custom-groups]]).

## Business rules

### Modern Vue build — handler status (current as of this revision)

| Action | Modern Vue handler status | Working path |
|---|---|---|
| Bulk Ban | Stub (`console.log('Open ban modal')`) | Legacy `/admin/old-customers` |
| Bulk Remove ban | Wired | Modern list |
| Bulk Change customer's group | Stub (`console.log('Open change group modal')`) | Legacy `/admin/old-customers` |
| Bulk Change password | Stub (`// TODO: Implement change password bulk`) | Legacy `/admin/old-customers` |
| Bulk Delete | Wired | Modern list |
| Per-customer Ban (detail page) | Wired | Modern detail page — see [[customers-ban]] |
| Per-customer Delete (detail page) | Wired | Modern detail page |

### Bulk actions support both single and array IDs — verified

The internal `changeBanned` / `changeGroup` methods accept a single customer ID OR an array — bulk operations reuse the same backend path as the per-customer action.

### Bulk password reset skips banned and guest customers — verified

The bulk "Change password" action iterates the selected customers and ONLY sends the reset link to customers who are NOT banned AND NOT in the Guest group. Banned customers or guest accounts in the selection are silently skipped (the action returns success without sending them anything). The toast message reports the validity period of the LAST reset code created — not a count of customers actually notified. See [[customers-lifetime-kpis]] for the 1-hour link validity.

### Bulk delete is permanent + `isEmpty` protection — verified

The confirmation message is explicit: *"This action cannot be undone."* Deleted customers cannot be recovered from this UI. The customer model has an `isEmpty` check (true when the customer has NO shipping addresses, NO billing addresses, AND NO orders) that the delete flow uses to refuse deletion of customers with order history — see [[customers-lifetime-kpis]] for the full deletion cascade and the `isEmpty` protection.

### Webhook fan-out on bulk actions

Each customer touched by a bulk action fires its own `customer.updated` (or `customer.deleted`) webhook — receivers should be idempotent and prepared for bursts. See [[settings-hooks]].

### Permission

All bulk endpoints under `/admin/api/core/customers` are protected by `hasApiPermission:customers`. Moderators without the grant get 403.

## Related

- [[customers]] — hub.
- [[customers-ban]] — the ban modal reused by bulk-ban.
- [[customers-flags]] — the flags the bulk actions flip.
- [[customers-lifetime-kpis]] — deletion cascade + 1-hour reset-link validity.
- [[customers-custom-groups]] — group picker source.
- [[customers-list-view]] — selection happens on the table.
- [[settings-hooks]] — webhook fan-out.

## Open questions

- Modern Vue bulk Ban / Change-group / Change-password handlers: ship date? (verify)
- Bulk-delete behaviour against non-empty customers via the modern UI: blocked with an error, or silently skipped? (verify the merchant-UX message)
