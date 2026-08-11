---
type: feature
nav_path: "Orders → Order details → Customer → Edit → Validation"
route_name: admin.orders.customer.edit
route_path: /admin/orders/action/customer/:order_id/edit
aliases: ["Customer edit validation", "Customer email required", "Archived order block", "Customer edit history diff", "Required fields customer edit"]
tags: [orders, customer, edit, validation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---

> Part of [[orders-customer-change]]. See the hub for the other aspects (panel UI, snapshot model, propagation).

# Customer edit — validation, archived block & history

## Purpose

The **save-time rules**: which fields are required and their length limits, the exact error messages, how the archived-order block layers against field validation, what the order-history diff records, and why there is no email-uniqueness check. This is the page to consult when a customer-edit save is rejected or when a support ticket asks "what exactly changed and when".

## Where to find it

These rules fire on **Save** in the customer-edit side panel ([[orders-customer-change-panel]]), reached via [[orders-details]] → Customer sidebar card → cog → **Edit customer info on this order** (POST to `admin.orders.customer.edit`).

## What the merchant can do here

On Save, the platform:

1. Fills the order's three customer fields (first name / last name / email).
2. Checks if any field actually changed (drives propagation — see [[orders-customer-change-propagation]]).
3. Validates the fields (see below).
4. Saves the order (and conditionally the customer record).

If validation fails, errors render inline next to the failing field via the `ajaxForm` framework's field-error rendering — no toast, no modal. The success path shows *"Customer info edited successfully"* (`order.succ.customer_edit_success`).

## Settings & fields

The validator enforces, on all three snapshot fields:

| Field | Rules |
|-------|-------|
| `customer_first_name` | required, max 191 chars |
| `customer_last_name` | required, max 191 chars |
| `customer_email` | required, must be valid email format, max 191 chars |

Localised error messages returned as 422:

- `customer_first_name.required` → *"First name is required"* (`order.err.customer_first_name_empty`).
- `customer_first_name.max` → *"First name cannot be more than 191 characters"* (`order.err.customer_first_name_cannot_be_more_than_%1$s_characters`).
- Same pattern for last name.
- `customer_email.required` → *"Customer email is required"* (`order.err.customer_email_requred`).
- `customer_email.email` → *"Invalid email format"* (`core.validate.err.email_invalid_format`).
- `customer_email.max` → *"Email max 191 characters"* (`core.validate.err.email_max_chars_%1$s`).

## Business rules

### Email is REQUIRED — despite looking optional

Contrary to the form's appearance (the label looks optional), the backend ENFORCES email as required. If the merchant clears the email field intending to remove it from the order, the save fails with *"Customer email is required"* — there is **no way to remove the email entirely** via this form. To work around (e.g., for a guest checkout where the email was wrong and needs removing), the merchant uses [[customers-details]] or the API.

### Archived orders rejected with a specific error

When the order is archived (`date_archived` is set), the save throws *"Cannot perform this operation on archived order"*. The merchant must unarchive via [[orders-archive]] first — there is no override.

### Archived-order block fires AFTER validation but BEFORE save

The archived check runs INSIDE the save transaction, AFTER the request-validator rules pass. So a merchant submitting blank fields on an archived order sees the **field-validation errors first**; only after fixing those will they hit the archived-order error. Counter-intuitive in practice, but it follows from the validator → business-rule layering.

### History captures full before/after diff

The history entry (`order_customer_edit`, surfaced in [[orders-history]]) stores the order's COMPLETE state before AND after the edit. Despite the visible scope being three fields, the merchant can drill into the entry to see the order's full state at the moment of the edit; only the three mutable fields actually differ. The displayed message focuses on the three fields, with per-field old / new values.

### No email-conflict check

The save accepts any valid email format without checking for collision against other customers. If two distinct customers share an email after the edit, the platform tolerates it — there is no uniqueness enforcement on the order's `customer_email` field nor on the propagated customer record's email. (The customer-facing consequence of this is covered on [[orders-customer-change-snapshot-model]].)

## Related

- [[orders-customer-change]] — hub.
- [[orders-details]] — parent page.
- [[orders-history]] — `order_customer_edit` entry storing the before/after diff.
- [[orders-archive]] — unarchive an order before it can be edited.
- [[customers-details]] — the workaround surface for removing an email entirely.

## Open questions

None.
