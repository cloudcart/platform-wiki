---
type: feature
nav_path: "Customers → Bulk actions"
route_name: customers-list
route_path: /admin/customers
aliases: ["Customers bulk actions", "Tools menu customers", "Bulk ban customers", "Bulk tag customers", "Add tags to customers", "Bulk delete customers", "Bulk change customer group", "Bulk change password customers"]
tags: [customers, list, bulk-actions]
plan_gates: []
created: 2026-06-10
updated: 2026-11-03
source_count: 4
---

> Part of [[customers]]. See the hub for the other aspects (list view, filters, create modal, ban flow, flags, lifetime KPIs).

# Customers — Bulk actions

## Purpose

The merchant ticks rows in the list and applies one action to all of them: bulk ban, add tags, remove ban, change group, password reset, delete. This aspect documents each action, the window it opens and the messages it shows.

## Where to find it

Sidebar → **Customers** → tick rows → **Tools** button above the table (disabled until a row is ticked). Route: `/admin/customers`.

## What the merchant can do here

### Tools menu

| Action | What it does |
|--------|--------------|
| **Ban customer/s** | Opens a window that asks for the reason. See [[customers-ban]]. |
| **Tags** | Opens *"Add tags to customer/s"*. |
| **Remove ban** | Runs at once with no window. Clears the banned flag and the stored ban reason for all selected customers. Toast: *"Unbanned successfully"*. |
| **Change customer's group** | Opens a window to move all selected customers to one customer group. |
| **Change password** | Runs at once with no window. Emails a password-reset link to the selected customers. |
| **Delete** | Permanent, after a confirmation. |

### Ban customer/s window

- Title *"Ban customer/s"*, text *"Please enter a reason for banning the selected customer/s."*
- A text area with the placeholder *"Enter the reason for blocking the client. Please note that the customer will see the reason you describe in the automated email they receive."*
- **Cancel** and **Save**. Saving with no reason shows *"Reason is required"*.
- Success toast: *"Banned successfully"*. The rows' **Status** turns to *Banned*.

### Tags window

- Title *"Add tags to customer/s"*, with a tag picker that searches the store's tags. Typing a new name creates it; *"To add new start typing..."* shows when nothing matches.
- **Cancel** and **Save**. Saving adds the tags to every selected customer, on top of the tags they already have.
- Success toast: *"Tags added successfully"*.

### Change customer's group window

- Title *"Change customer's group"*, text *"Here you can specify in which group your customer will be a member"*, and one searchable dropdown of customer groups ([[customers-custom-groups]]).
- **Cancel** and **Save**. Saving with no group shows *"Group id is required"*.
- Success toast: *"Customer's group changed successfully"*. The list reloads when it is filtered by group. No email goes to the customers.

### Delete confirmation

- Title *"Delete"*, message *"Are you are sure you want to delete? Caution: This action cannot be undone."*
- **No** and a red **Yes**.
- Success toast: *"Deleted successfully"*. Failure toast: *"Error while deleting"*.

## Settings & fields

The windows above are the only fields here. The ban reason is explained on [[customers-ban]].

## Business rules

### Bulk password reset skips banned and guest customers

The bulk **Change password** action sends the reset link only to customers who are not banned and not in the Guests group. Others in the selection are skipped. The toast is the same whoever was reached: *"A link to reset your password has been sent to your email address"*. See [[customers-lifetime-kpis]] for the 1-hour link validity.

### Bulk delete is permanent

Deleted customers cannot be recovered from this UI. A customer with orders or addresses can be deleted too; their orders stay. See [[customers-lifetime-kpis]] for the deletion cascade.

### Webhooks

Bulk **Delete** fires one `customer.deleted` webhook per customer, so receivers should be idempotent and prepared for bursts. See [[settings-hooks]]. Bulk ban, remove ban and change group update the records directly, with no `customer.updated` webhook.

### Permission

All bulk endpoints under `/admin/api/core/customers` are protected by `hasApiPermission:customers`. Moderators without the grant get 403.

## Related

- [[customers]] — hub.
- [[customers-ban]] — the ban flow and the reason.
- [[customers-flags]] — the flags the bulk actions flip.
- [[customers-lifetime-kpis]] — deletion cascade + 1-hour reset-link validity.
- [[customers-custom-groups]] — group picker source.
- [[customers-list-view]] — selection happens on the table.
- [[settings-hooks]] — webhook fan-out.

## Open questions

None.
