---
type: feature
nav_path: "Orders → + Add order → Validation & save"
route_name: admin.orders.add
route_path: /admin/orders/add
aliases: ["Add order validation", "Manual order save validation", "Add order required fields", "Add order locker office_id merge", "Add order office code parsing", "Manual order transaction wrapping"]
tags: [orders, manual, smarty, draft, validation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-add]]. See the hub for the other aspects (wizard, customer, delivery methods, address handling, draft state, no-API rationale).

# Add order — validation & save

## Purpose

Step 1 of the manual-order wizard ends with the merchant clicking **Save** / **Next**, which posts the form to `/admin/orders/add/save` and either creates a draft order or surfaces validation errors. This page documents the validation rules enforced at step-1 save, the locker→office_id pre-validation merge, office-code parsing against the courier API, and the DB-transaction wrapping that keeps the merchant from ever seeing a half-created order.

## Where to find it

Validation fires on POST to `/admin/orders/add/save` — the endpoint invoked when the merchant clicks **Save** / **Next** on the **+ Add order** side panel (see [[orders-add-wizard]]).

## What the merchant can do here

### Required-fields validation (verified)

The save endpoint enforces the following rules — every OTHER field shown on the panel is **optional** at this step:

| Field | Required when | Error message |
|---|---|---|
| **Customer** | Always | *"Please select a customer"* |
| **Delivery to** | When customer is selected | *"Please pick a delivery type"* |
| **Office / locker ID** | Delivery-to = office or locker | *"Please select an office"* |
| **Address ID** | Delivery-to = address | *"Please select an address"* |
| **Store ID** | Delivery-to = marketplace | *"Please select a store"* |
| **First name / Last name / Phone** | Delivery-to = office, locker or marketplace | Field-level required |

**No other validations fire at this step** — no email format checks, no phone format checks, no minimum/maximum products. The merchant cannot save the draft without a customer + a delivery type, but everything else is loose. Stricter validation runs only when the merchant clicks **Create order** in step 2 (see [[orders-details]]).

### Locker submissions are renamed to office_id pre-validation

In the request's `prepareForValidation`, if the merchant's chosen delivery type is `locker`, the request's `locker_id` value is **silently merged into the `office_id` field**. So the same backend validation rule (`office_id required`) covers both office and locker, and the controller can parse the courier prefix uniformly regardless of which UI input the value came from.

This is why the validation table above lists *"Please select an office"* as the error message even for the locker case — there is only one underlying field at validation time.

### Office vs locker — pickup-point validation against courier API

When delivery-to is `office` or `locker`, the office ID must follow the format `<courier>-<office-code>` (e.g., `econt-1234`). The platform:

1. **Parses the courier prefix** off the ID.
2. **Validates the courier is among the installed pickup-capable shipping integrations.**
3. **Calls the courier's API** to look up the office or locker details (name, address, hours, etc.).
4. If the office code isn't found in the courier's catalog → save fails with *"Office does not exist"* and the entire draft creation is rolled back.

This protects against stale Select2 values (e.g., merchant typed a manual ID, courier removed the office overnight) and against typos.

### Transaction wrapping (verified)

The entire save is wrapped in a DB transaction. If **any** step fails — invalid customer reference, office-code parse error, courier API "office does not exist", tax setup error, address-create error for pickup modes — the **entire creation is rolled back**. The merchant never sees a half-created order.

This applies symmetrically to the side effects: a rolled-back save **does not** leave a stray new saved address on the customer's profile (for pickup modes — see [[orders-add-address-handling]]).

### Save uses `ajaxForm`

The form submits via the platform's `ajaxForm` helper. On success, the platform shows a toast and redirects to the new order's details page with `?preview=true` (step 2 — see [[orders-add-wizard]]).

## Settings & fields

There are no merchant-configurable validation settings — the rules above are hard-coded in the save request validator.

The conditional first/last-name / phone requirements for pickup modes are driven by the chosen delivery-method radio — see [[orders-add-delivery-methods]] for the full sub-block table.

## Business rules

### Step-1 validation is intentionally loose

The merchant can save a draft with just a customer + a delivery target. No products, no payment provider, no shipping provider (for address delivery), no email check. Step-2 validation (on the **Create order** click) is much stricter — but step 1 is designed to let the staff member capture the bare minimum during a phone call without being blocked.

### Step-1 errors return the merchant to the same panel

Validation errors are returned per field in the AJAX response. The slide-in panel stays open, errors highlight the offending field. No state is lost; the merchant fixes the field and clicks Save again.

### Office-code parsing fail is fatal

A successful office-code parse but a failed courier-API lookup (e.g., "office does not exist") rolls back the entire save — the order shell is not created. This is rare in practice because Select2 only offers valid offices, but it can happen when:

- The merchant types a manual ID (Select2 allows free text in some configurations).
- The courier removes the office between the dropdown render and the form submit.
- The courier's API is unreachable at save time (timeout → fail).

When this happens, the merchant sees *"Office does not exist"* on the **Delivery to** sub-block.

### `prepareForValidation` is also where defaults are inferred

Beyond the locker→office_id merge, `prepareForValidation` is where the controller normalises any other minor input shape mismatches before the validator runs. Verified specific to the locker case; broader normalisations not documented (verify).

### Permission

Standard orders permission scope. To create a customer inline as part of the same flow, the merchant also needs the customers create permission — but the validator at this endpoint only checks the orders scope; customer creation is gated separately upstream in the inline-create panel (see [[orders-add-customer]]).

## Related

- [[orders-add]] — hub.
- [[orders-add-wizard]] — the **Save** / **Next** button submits to this endpoint.
- [[orders-add-customer]] — the customer-is-mandatory rule that drives the first validation row.
- [[orders-add-delivery-methods]] — the four radio values and their sub-block required fields.
- [[orders-add-address-handling]] — the saved-address side effect that is rolled back when validation fails.
- [[orders-add-draft-state]] — what the order looks like once a successful save completes.
- [[orders-details]] — where strict step-2 validation runs on **Create order**.

## Open questions

- Whether other normalisations beyond the locker→office_id merge happen in `prepareForValidation` (verify).
