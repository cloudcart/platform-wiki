---
type: feature
nav_path: "Customers → Customer details → Ban flow"
route_name: customers-details.new
route_path: /admin/customers-new/details/:id
aliases: ["Customer ban flow", "Customer ban modal", "Remove ban", "Ban reason card"]
tags: [customers, profile, detail, ban, moderation]
plan_gates: ["customers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[customers-details]]. See the hub for the other aspects (identity card, tab strip, email verification, default address, delete).

# Customer details — Ban / Unban flow

## Purpose

The **Ban customer / Remove ban** flow and the **Ban reason card**. Banning is the merchant's blunt instrument for blocking a customer from checking out — they may still browse and log in, but storefront checkout is rejected. The flow is gated by a required free-text reason; unbanning is a one-click action with no confirmation.

This aspect covers three surfaces:

1. The **Ban customer** modal (triggered from the page header).
2. The **Remove ban** button (also in the page header, with no modal).
3. The **Ban reason card** on the right column, visible only when banned.

## Where to find it

[[customers]] → click any row → opens `/admin/customers-new/details/:id`. All three surfaces live on this page:

- **Ban customer** button — in the page header (top-right area of the Customers wrapper), visible when the customer is **NOT** currently banned.
- **Remove ban** button — same location, visible when the customer **IS** currently banned. Accompanied by a *"Banned"* status chip next to the customer's name in the header.
- **Ban reason card** — right column of the two-column detail layout, between the (empty) top of the right column and the [[customer-details-default-address|default address card]]. Visible only when banned.

## What the merchant can do here

### Ban customer modal

Triggered by the **Ban customer** button in the page header. The modal is a `CcConfirmModal` with the destructive variant (red Confirm button).

| Element | Notes |
|---------|-------|
| **Title** | *"Ban customer"* |
| Explanation text | *"Short explanation what banning a customer means. Provide info about how the ban can be removed."* |
| **Ban reason** textarea (`v-model="banReason"`) | Placeholder: *"Please describe the reason for banning this customer. Keep in mind that the reason will be set to your customer via email"*. Required — the Confirm button is disabled while empty (`:disabled-confirm="!banReason"`). Inline error renders under the textarea on validation fail. |
| Cancel button | Closes the modal **AND clears** the typed reason. |
| Confirm button | Calls the ban mutation with `{ids: [customer_id], reason: banReason.trim}`. On success: customer's local `banned` set to `yes`, `banned_reason` set to the typed string, toast *"Customer banned successfully"*. Failure: per-field errors populated, or toast *"Error while banning customer"*. |

The modal is opened via a handler that **RESETS** the reason and clears prior errors before showing. Closing via the X / Cancel runs the same reset.

### Remove-ban button (no modal, immediate)

Clicking **Remove ban** in the header runs **WITHOUT** confirmation — it directly calls the unban mutation with `{ids: [customer_id]}`. The button shows a spinner during the request.

- **Success**: local `banned = no`, `banned_reason = null`, toast *"Ban removed successfully"*.
- **Failure**: toast *"Error while removing ban"*.

So unbanning is a **one-click action** — there's no "are you sure" gate. The merchant should be careful clicking the green check-mark icon.

### Ban reason card (right column, conditional)

Visible only when the customer is banned. Shows:

- Red prohibition icon.
- Label: *"Ban reason"*.
- The text the merchant typed at ban time.

This card is the merchant's quick reference for **WHY** a customer was banned (e.g., when a banned customer calls and asks why they can't check out). The card disappears as soon as Remove ban is pressed.

## Settings & fields

| Field | Edited from | Type | Notes |
|-------|-------------|------|-------|
| `banned` | Ban / Remove ban buttons | enum `yes` / `no` | Drives the *"Banned"* chip and the ban-reason card visibility. |
| `banned_reason` | Ban modal (set on ban) | string | Free-text reason from the modal textarea. Cleared to `null` on unban. |

There are no other configurable settings — the ban flow itself has no per-merchant configuration (e.g., no template for the ban-notification email).

## Business rules

### Ban reason is required (server- and client-enforced)

The Confirm button is disabled while the textarea is empty, AND the server-side validation rejects an empty reason. The reason is trimmed before submit (`banReason.trim`).

### Ban reason is admin-only on the detail page

The ban reason is visible to admins on the right-column card but is never shown to the customer directly on the storefront. The placeholder text on the ban modal says the reason *"will be set to your customer via email"* — verify whether the customer-notification email is actually sent `(verify)`.

### Cancelling the ban modal clears the typed reason

Closing the ban modal via Cancel or X runs the same reset as opening — the typed reason is discarded. The merchant cannot accidentally submit yesterday's draft reason.

### Unban is one-click — no confirmation

The unban action does NOT use a confirmation modal. A single click on the green check-mark **Remove ban** button immediately calls the API and clears both `banned` and `banned_reason`. Merchants who want to keep the historical reason should screenshot the card before unbanning — there's no audit trail of past bans on this page `(verify)`.

### Ban-state lookup on the detail page

The *"Banned"* chip and the Ban / Remove-ban buttons are driven by `customer.banned == 'yes'`. The Ban reason card on the right column renders only when `banned == 'yes'` AND the customer record has a non-empty `banned_reason`. Unban clears both fields (`banned = 'no'` AND `banned_reason = null`).

### Storefront behaviour after ban

A banned customer can still log in and browse the storefront, but checkout is rejected. The platform does not delete their cart or addresses — the ban is reversible at any time. The customer's order history (past orders + lifetime KPIs) is preserved.

## Programmatic access

The ban / unban endpoints are exposed under the admin REST customer namespace (the same paths the modal uses). They are **NOT** part of [[json-api-v2]] — merchants needing programmatic ban must call the admin REST routes directly.

Setting `customer.banned = 'yes'` via JSON-API v2 PATCH is **not** equivalent to the dropdown flow `(verify)` — the merchant should use the dedicated admin endpoints to guarantee the same side-effect chain.

## Related

- [[customers-details]] — hub.
- [[customers]] — list page; the *"Banned"* chip also appears in the list view.
- [[customer]] — entity page; carries `banned` and `banned_reason`.
- [[customer-details-identity-card]] — identity card on the left column (where the *"Banned"* chip echoes next to the customer's name).
- [[settings-staff]] — moderator permissions; not every staff role can ban.

## Open questions

- Verify whether the customer-notification email referenced in the ban modal placeholder text (*"will be set to your customer via email"*) is actually sent.
- Verify whether there is any audit-log entry created for past bans, or whether unbanning fully erases the historical reason.
- Verify whether JSON-API v2 PATCH to `customer.banned` triggers the same side-effects as the admin REST endpoint.
