---
type: feature
nav_path: "Orders → + Add order"
route_name: admin.orders.add
route_path: /admin/orders/add
aliases: ["Add order", "Manual order", "New order", "Phone order", "Manual order creation", "Добави поръчка", "Ръчно създаване на поръчка"]
tags: [orders, manual, smarty, draft]
plan_gates: []
created: 2026-05-21
updated: 2026-08-06
source_count: 10
---

# Add order (manual order creation)

## Purpose

The **manual order creation flow** — used by staff to create orders on behalf of customers (phone orders, in-person sales recorded retroactively, B2B negotiated orders, support-assisted carts). Opens as a slide-in side panel from [[orders]] header's **+ Add order** button.

The flow is a **two-step wizard**:

1. **Step 1 — Add order panel.** Merchant picks the customer, picks the delivery method (address / office / locker / marketplace), picks or creates the address (or office / locker / store), fills in name + phone when delivery is non-address. **No products are added here.** Clicking **Save** / **Next** creates an order with `is_draft = 1`.
2. **Step 2 — Order details in draft mode.** The merchant is redirected to [[orders-details]] with `?preview=true`. They add products, configure payment, configure shipping, review totals, then click **Create order** (or **Create order and send to client** for online payments). For an **offline** payment provider that clears the draft flag and fires the post-create pipeline; for an **online** provider the order stays a draft and the customer is emailed a checkout link instead — see [[orders-add-wizard]].

The created order then becomes a regular order in [[orders]] and the merchant continues editing it on [[orders-details]].

## Where to find it

From [[orders]] → header **+ Add order** button. The panel slides in from the right edge of the screen (not a full-page navigation).

Route: `/admin/orders/add` (GET to load the form, POST to `/admin/orders/add/save` to save).

## What the merchant can do here

This page is the **hub** for the manual-order flow. The flow has been split into the following aspect pages — each one covers exactly one slice. Drill into the aspect that matches the question, not every page.

### Sub-pages (in this cluster)

- [[orders-add-wizard]] — the two-step wizard structure; panel layout regions; step-1-to-step-2 transition; after-save redirect into `?preview=true` mode.
- [[orders-add-customer]] — customer autocomplete; inline **+ Add customer**; mandatory-customer rule (no guest manual orders); customer-name fallback chain.
- [[orders-add-delivery-methods]] — the four delivery-method radios (`address` / `office` / `locker` / `marketplace`); when each appears; sub-block JavaScript swapping; Stores app multi-store attribution.
- [[orders-add-address-handling]] — saved-address dropdown; **+ Add new address** slide-out-over-panel; address auto-creation as a side-effect on the customer's saved-addresses list; address cloning for `address` delivery.
- [[orders-add-validation-save]] — required fields per delivery type; locker→office_id pre-validation; office-code parsing; pickup-point validation against the courier API; transaction wrapping.
- [[orders-add-draft-state]] — initial draft order state (`is_draft = 1`, `is_admin = true`, `status = pending`, `notify_customer = 0`); notifications suppressed; stock NOT reserved at draft creation; locale / currency / unit system frozen; admin GeoIP capture; auto-attached shipping provider; tax auto-resolution.
- [[orders-add-no-api]] — why there is **no JSON-API v2 endpoint** for creating orders; the two canonical entry points (storefront checkout + this manual flow); how integrations push orders.

## Settings & fields

The minimal set required at the step-1 save is documented in detail on [[orders-add-validation-save]]. Headline rule: **Customer + Delivery to are always required**; the address / office / locker / store / first-name / last-name / phone become required based on which delivery type is picked.

The remaining product, payment, and shipping configuration happens in step 2 on [[orders-details]] — that page documents the full editable surface of a draft order.

## Business rules

The cross-cutting rules that hold across every aspect of the manual-order flow:

- **Always starts in draft state** — `is_draft = 1`. Invisible to the customer, fires no notifications, decrements no stock. See [[orders-add-draft-state]].
- **Customer is mandatory** — no "guest manual orders". A brand-new customer can be created inline via **+ Add customer**. See [[orders-add-customer]].
- **Address — saved or new.** The address dropdown lists the customer's saved addresses. If they have none, the merchant creates one through a slide-out panel that opens **over** the order panel; the created address is saved to the customer's profile too. See [[orders-add-address-handling]].
- **Transaction wrapping.** The entire save is wrapped in a DB transaction — if any step fails (invalid customer reference, office-code parse error, tax setup error), the whole creation rolls back. See [[orders-add-validation-save]].
- **No JSON-API v2 endpoint.** Orders cannot be created via the API. See [[orders-add-no-api]] for the rationale.
- **Permission.** Standard orders permission scope. To create a customer inline, the merchant also needs the customers create permission.

## Programmatic access

**There is no JSON-API v2 endpoint for creating orders.** See [[orders-add-no-api]] for the full rationale and how integrations push orders into CloudCart via the storefront checkout flow or the checkout-resume mechanism.

## Related

- [[orders]] — parent list (entry point via the + Add order header button).
- [[orders-details]] — where the merchant continues editing the draft order in step 2 to add products, configure payment / shipping, and finally create it.
- [[customers]] — Customer create modal accessible inline via + Add customer.
- [[customers-details-shipping-addresses]] — saved addresses listed in the picker.
- [[settings-cart]] — Google Maps API key powers the sidebar map; `manual_order_payments` setting may restrict which payment providers are offered in the draft.
- [[settings-payment-providers]] — payment providers selectable on the draft.
- [[json-api-v2]] — API overview + rationale on why orders cannot be POSTed.
- [[order]] — entity page.
- [[order-processing-pipeline]] — admin manual order placement variation of the pipeline (Stage 1 entry-point B).
- [[orders-notify-customer]] — notify-customer flag flipped from `0` to `1` only when the merchant commits the draft.
- [[orders-products]] — adding products to the draft order in step 2.
- [[inventory-decrement-timing]] — when products in the draft eventually decrement stock (configured at the store-wide level).

## Open questions

None — all original open questions have been distributed to the aspect pages.
