---
type: feature
nav_path: "Customers → Customer details → Delete customer"
route_name: customers-details.new
route_path: /admin/customers-new/details/:id
aliases: ["Delete customer", "Customer delete cascade", "Customer hard delete", "Customer delete redirect"]
tags: [customers, profile, detail, delete, cascade]
plan_gates: ["customers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customers-details]]. See the hub for the other aspects (identity card, tab strip, ban flow, email verification, default address).

# Customer details — Delete customer

## Purpose

The **Delete customer** action — the merchant's terminal command on a customer record. Triggered from the page-header dropdown, gated by a single confirmation modal, then cascade-deletes the customer's active cart and marketing subscriber while preserving past orders as orphaned snapshots. Hard-delete only — no soft delete, no undo from the UI.

This action is one of the few destructive operations on a customer that cannot be reversed inside CloudCart. Restoring a deleted customer requires re-creating them (and losing the link from past orders to the recreated record, which keeps the original snapshot).

## Where to find it

[[customers]] → click any row → opens `/admin/customers-new/details/:id`. The action lives in the page-header dropdown (the dropdown next to the **Ban customer** / **Remove ban** button in the Customers wrapper). The dropdown option is labelled **Delete customer** with a red trash icon.

The same delete behaviour is also reachable from [[customers]] via bulk actions on the list — see that page for the bulk delete flow.

## What the merchant can do here

### Delete customer modal

Triggered by the **Delete customer** option in the page-header dropdown. Opens a `CcConfirmModal` with the destructive variant (red Confirm button).

| Element | Notes |
|---------|-------|
| **Title** | *"Delete customer"* |
| **Message** | *"Are you are sure you want to delete? Caution: This action cannot be undone."* |
| Confirm button | Red (`confirm-button-variant="danger"`). Calls the bulk-delete mutation with `{ids: [customer_id]}`. On success: toast *"Customer removed successfully"*, modal closes, then a **1-second delay** before the merchant is auto-redirected to `/admin/customers-new`. |
| Cancel button | Closes the modal without action. |

The 1-second delay before redirect lets the toast finish its fade-in animation before the page swap — the merchant sees confirmation that the delete succeeded.

### Effects on related records (cascade)

The Delete customer action fires the following cascade — the merchant sees only the success toast, but the platform performs all of these in the background:

| Record type | Effect |
|-------------|--------|
| Active **Cart** | Cascade-deleted along with the customer. |
| **Subscriber** record | Removed via an async job — drops them from segments, newsletter lists, abandoned-cart sequences, and every targeting flow keyed on `customer_id`. |
| Past **Orders** | NOT deleted. Past orders remain orphaned with the snapshot customer data they carried at order-creation time (name, email, addresses, etc., copied onto the order line). The order detail page still shows the customer name from the snapshot, but the *"view customer"* link returns a *"Customer not found"* message. |
| **Customer record** | Hard delete — row removed from the customers table. No soft-delete column, no UI to undelete. |
| **`customer.deleted` webhook** | Fires. Subscribers see the customer's pre-delete payload as the event body. |

## Settings & fields

The delete flow has no editable settings — the action is binary (confirm or cancel) and the cascade is fixed by the platform. The only configurable surface is the merchant's response to the `customer.deleted` webhook (e.g., a CRM sync that removes the matching contact); see [[settings-hooks]].

## Business rules

### Past orders are preserved as orphans

When a customer is deleted, their past orders are **NOT** removed — they remain in the orders table with the snapshot customer data (name, email, billing/shipping addresses) frozen at the time each order was created. This preserves the merchant's order history and financial records, which is required for tax filing and dispute handling.

Consequence: clicking the *"view customer"* link from an orphaned order yields a *"Customer not found"* message (since the URL points to a deleted customer ID). The order detail itself still renders fine — it just no longer links back to a live customer profile.

### Hard delete only — no soft delete from the UI

There is **no soft-delete / undelete** path from the admin UI. Once confirmed, the customer record is gone. If the merchant deleted the wrong customer, the only recovery is to:

1. Re-create the customer manually with the same email.
2. Re-link past orders by hand (not supported via UI — the orphaned orders stay orphaned).

Merchants who suspect they may need to undo a deletion should **ban** the customer instead — see [[customer-details-ban-flow]] — which is fully reversible.

### Subscriber removal is async

The Subscriber record is removed via a queued job, not synchronously with the customer delete. So immediately after the delete, the marketing segments and newsletter lists may still show the customer for a few seconds until the job runs. This is the typical eventual-consistency window.

### Webhook fires AFTER the cascade

The `customer.deleted` webhook fires after the cascade has completed (cart and subscriber removed). Receivers see a payload representing the pre-delete state of the customer. The webhook is the merchant's hook for syncing the deletion to external systems (CRM, ERP, marketing tool).

Subscribers must be **idempotent** — webhook redelivery is possible. See [[settings-hooks]].

### Delete is NOT bulk-able from this page

The detail page's Delete action targets exactly one customer (the one currently open). To delete multiple customers at once, the merchant uses the bulk action on [[customers]] — same cascade, but invoked over a list of IDs.

### Plan-gate notes

Deleting a customer **frees** one slot under the numeric `customers` plan gate. So a merchant at their plan's customer cap can delete an old, inactive customer to make room for a new registration. (Restoring the deleted customer is not possible, so this is a one-way capacity recovery.)

## Programmatic access

The bulk-delete endpoint is exposed under the admin REST customer namespace. The same cascade applies when invoked via [[json-api-v2]] DELETE — cart cascade-deleted, Subscriber removed, `customer.deleted` webhook fires, past orders preserved as orphans. See [[api-customers]] for the JSON-API v2 endpoint and [[json-api-v2]] for authentication / rate-limit / side-effects principles.

## Related

- [[customers-details]] — hub.
- [[customers]] — list page; bulk delete uses the same cascade.
- [[customer]] — entity page; the row this action removes.
- [[customer-details-ban-flow]] — the reversible alternative to delete.
- [[settings-hooks]] — `customer.deleted` webhook lifecycle.
- [[plan-gates]] — numeric `customers` cap; delete frees a slot.
- [[api-customers]] — JSON-API v2 DELETE endpoint with the same cascade.

## Open questions

- Verify whether the 1-second redirect delay is configurable, or whether it is hard-coded in the modern UI.
- Verify whether the cart-cascade also removes any cart-attached coupons / discount events from analytics.
