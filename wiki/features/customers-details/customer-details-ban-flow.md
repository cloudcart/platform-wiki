---
type: feature
nav_path: "Customers → Customer details → Ban flow"
route_name: customers-details
route_path: /admin/customers/details/:id
aliases: ["Customer ban flow", "Customer ban modal", "Remove ban", "Ban reason card"]
tags: [customers, profile, detail, ban, moderation]
plan_gates: ["customers"]
created: 2026-06-10
updated: 2026-11-03
source_count: 4
---

> Part of [[customers-details]]. See the hub for the other aspects (identity card, tab strip, email verification, default address, delete).

# Customer details — Ban / Unban flow

## Purpose

The **Ban customer / Remove ban** flow and the **Ban reason card**. Banning is the merchant's blunt instrument for blocking a customer: storefront login and checkout are both rejected. The flow is gated by a required free-text reason; unbanning is a one-click action with no confirmation.

This aspect covers three surfaces:

1. The **Ban customer** modal (triggered from the page header).
2. The **Remove ban** button (also in the page header, with no modal).
3. The **Ban reason card** on the right column, visible only when banned.

## Where to find it

[[customers]] → click any row → opens `/admin/customers/details/:id`. All three surfaces live on this page:

- **Ban customer** button — in the page header (top-right area), visible when the customer is **NOT** currently banned.
- **Remove ban** button — same location, visible when the customer **IS** currently banned. Accompanied by a *"Banned"* status chip in the header.
- **Ban reason card** — top of the right column, above the [[customer-details-default-address|default address card]]. Visible only when banned.

## What the merchant can do here

### Ban customer modal

Triggered by the **Ban customer** button in the page header.

| Element | Notes |
|---------|-------|
| **Title** | *"Ban customer"* |
| Explanation text | *"Short explanation what banning a customer means. Provide info about how the ban can be removed."* |
| **Ban reason** textarea | Placeholder: *"Please describe the reason for banning this customer. Keep in mind that the reason will be set to your customer via email"*. Required — **Yes** is disabled while empty. Inline error renders under the textarea on validation fail, e.g. *"Reason is required"*. |
| **No** button | Closes the window and clears the typed reason. |
| **Yes** button | Bans the customer. On success: the **Banned** chip and the reason card appear, toast *"Customer banned successfully"*. |

### Remove-ban button (no modal, immediate)

Clicking **Remove ban** in the header runs **WITHOUT** confirmation. The button shows a spinner during the request.

- **Success**: the chip and the reason card disappear, toast *"Ban removed successfully"*.

So unbanning is a **one-click action** — there's no "are you sure" gate. The merchant should be careful clicking the green check-mark icon.

### Ban reason card (right column, conditional)

Visible only when the customer is banned. Shows:

- Red prohibition icon.
- Label: *"Ban reason"*.
- The text the merchant typed at ban time.

This card is the merchant's quick reference for **WHY** a customer was banned (e.g., when a banned customer calls and asks why they can't log in or check out). The card disappears as soon as Remove ban is pressed.

## Settings & fields

| Field | Edited from | Type | Notes |
|-------|-------------|------|-------|
| `banned` | Ban / Remove ban buttons | enum `yes` / `no` | Drives the *"Banned"* chip and the ban-reason card visibility. |
| `banned_reason` | Ban modal (set on ban) | string | Free-text reason from the modal textarea. Cleared to `null` on unban. |

There are no other configurable settings — the ban flow itself has no per-merchant configuration (e.g., no template for the ban-notification email).

## Business rules

### Ban reason is required (server- and client-enforced)

**Yes** is disabled while the textarea is empty, AND the server-side validation rejects an empty reason.

### Who sees the ban reason

The ban reason is visible to admins on the right-column card. The customer sees it in the storefront message when they try to log in or check out: *"Account has been suspended due to {reason} on {date}"*. The ban itself sends no email.

### Closing the ban window clears the typed reason

Closing the window with **No** discards the typed reason. The merchant cannot accidentally submit yesterday's draft reason.

### Unban is one-click — no confirmation

The unban action does NOT use a confirmation window. A single click on the green check-mark **Remove ban** button immediately clears both `banned` and `banned_reason`. The reason shown on the card goes with it.

### Ban-state lookup on the detail page

The *"Banned"* chip and the Ban / Remove-ban buttons follow the customer's `banned` value. The Ban reason card on the right column renders when the customer record has a `banned_reason`. Unban clears both fields (`banned = 'no'` AND `banned_reason = null`).

### Storefront behaviour after ban

A banned customer cannot log in on the storefront, and checkout is rejected. The platform does not delete their cart or addresses — the ban is reversible at any time. The customer's order history (past orders + lifetime KPIs) is preserved.

## Programmatic access

The ban / unban endpoints are exposed under the admin REST customer namespace (the same paths the window uses). They are **NOT** part of [[json-api-v2]] — merchants needing programmatic ban must call the admin REST routes directly.

Setting `customer.banned = 'yes'` via JSON-API v2 PATCH is **not** equivalent to this flow `(verify)` — the merchant should use the dedicated admin endpoints to guarantee the same side-effect chain.

## Related

- [[customers-details]] — hub.
- [[customers-ban]] — the ban on the list, including the bulk window and the reason popup.
- [[customer]] — entity page; carries `banned` and `banned_reason`.
- [[customer-details-identity-card]] — identity card on the left column.
- [[settings-staff]] — moderator permissions; not every staff role can ban.

## Open questions

- Verify whether JSON-API v2 PATCH to `customer.banned` triggers the same side-effects as the admin REST endpoint.
