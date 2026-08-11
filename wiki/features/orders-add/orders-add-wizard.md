---
type: feature
nav_path: "Orders → + Add order → Wizard structure"
route_name: admin.orders.add
route_path: /admin/orders/add
aliases: ["Add order wizard", "Manual order wizard", "Add order panel layout", "Add order step 1 vs step 2", "Add order side panel structure"]
tags: [orders, manual, smarty, draft, wizard]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 4
---

> Part of [[orders-add]]. See the hub for the other aspects (customer, delivery methods, address handling, validation, draft state, no-API rationale).

# Add order — wizard structure

## Purpose

The manual-order flow is a **two-step wizard** with a deliberate split: step 1 is a slide-in side panel that captures only the **who** and the **where** (customer + delivery target); step 2 is the full order-details page in draft mode, which captures the **what** (products) and the **how-to-pay** (payment + shipping). This page documents the wizard structure itself — the layout regions, the step transition, and the after-save redirect.

## Where to find it

The wizard opens from [[orders]] → header **+ Add order** button. The panel slides in from the right edge of the screen (not a full-page navigation). Route: `/admin/orders/add` (GET to load the form, POST to `/admin/orders/add/save` for step 1).

## What the merchant can do here

### Two-step wizard layout (verified)

| Step # | Step label | What the merchant does here | Save / Next action |
|---|---|---|---|
| 1 | **Add order** (header reads *"Add order"* / *"Добави поръчка"*) | Picks the customer, picks the delivery method, picks/creates the address (or office / locker / store), fills in name + phone when delivery is non-address. NO products are added here. | Clicks **Save** / **Next** (button label comes from `order.new.order.step2`). Backend creates the order with `is_draft = 1` and redirects to step 2. |
| 2 | **Order details — draft mode** | Opens [[orders-details]] with `?preview=true`. Merchant adds products, configures payment, configures shipping (if not auto-attached), reviews totals. | Clicks **Create order** (or **Create order and send to client** for online payments). What happens next **depends on the payment provider** — see below. |

The "step 2" label hint comes from the translation key `order.new.order.step2` ("Next" / "Step 2") — meaning step 1 is acknowledged as preparatory and the real order-building happens in [[orders-details]].

### "Create order" behaves differently for offline vs online payment

The draft flag is **not** cleared for every manual order. Clicking **Create order** marks the order as confirmed in both cases, but only one branch actually promotes it out of draft:

| Payment provider on the order | What clicking **Create order** does |
|---|---|
| **Offline** (cash on delivery, bank transfer, cash on pickup…) | The **draft flag is cleared** — the order becomes a real order. Customer notifications are switched on, the new-order confirmation email is sent, and the full order-created pipeline fires (stock, webhooks, apps). |
| **Online** (card gateway, BNPL, wallet…) | The order **stays a draft**. No order-created pipeline, no confirmation email. If the merchant ticked *notify customer*, the platform emails the customer a **checkout link** so they can pay; the order leaves draft only once that payment (or a later status change) lands. |

This is the mechanism behind the frequent *"I created the order but it's still showing as a draft"* report: the order is waiting on the customer's online payment. To force it, the merchant can pay it manually — **Mark as paid** on the Payment row ([[orders-payment-mark-paid]]) — or change its status, which also clears the draft flag (see [[orders-details-known-issues]]).

### Side-panel structure (verified — sections)

The panel is built from a single form (`#ManualOrder`) with these layout regions:

| Region | Contents |
|---|---|
| **Fixed top bar** | Title + Cancel button + Save/Next button. |
| **Main column — products block** | Empty-state with *"Add products to this order…"* alert + centred **+ Add product** button. Wrapped in the same `order-table` markup as [[orders-details]] but with zero data. Subtotal + Total show `0.00`. |
| **Main column — note** | Disabled `note_administrator` textarea (placeholder *"Type here…"*) — only enabled once products exist (after step 2 lands on details). |
| **Sidebar — Customer card** | Google Maps thumbnail (default centred on Europe lat/lng) + **Customer** autocomplete + **+ Add customer** link that opens the customer-create panel from [[customers]]. See [[orders-add-customer]]. |
| **Sidebar — Delivery method radio block** | One radio per supported type. See [[orders-add-delivery-methods]]. |
| **Sidebar — Shipping method block** (hidden until delivery method picked) | Conditional sub-panel that swaps based on the radio selection. |
| **Sidebar — Address-create slot** (hidden until delivery method = address) | Renders a *"Add new address"* link once customer is selected; the link opens the customer-address create panel inline. See [[orders-add-address-handling]]. |

### Side-panel mechanics

The panel slides in from the right edge (the platform's standard side-panel UX). The merchant can:

- Click outside / Escape / the X icon to close (no save).
- Click Cancel to close.
- Click Save / Next to commit step 1.

Save uses `ajaxForm` — submits via AJAX, shows toast on success, navigates to the new order's details page in preview mode.

### After save the merchant is redirected into preview mode (verified)

On successful step-1 save, the merchant is redirected to `/admin/orders/details/<id>?preview=true`. The `preview=true` flag opens the order-details page in a special read-mostly mode where the merchant continues editing the draft — that is step 2. The flag survives until the merchant clicks **Create order** on [[orders-details]] — which clears the draft flag only on the offline-payment branch (see above).

### Legacy vs modern entry points

The platform has two related entry-point templates:

- **`add.tpl`** (the legacy first-step shortcut) — minimal form with **Customer picker** + **Shipping address picker**. After selecting a customer, the city / shipping address list auto-populates from the customer's saved addresses ([[customers-details-shipping-addresses]]).
- **`add_new.tpl`** (the modern unified panel) — full order summary template scaffolded with empty data. The merchant adds products, configures customer + addresses, picks payment + shipping. POSTs to step 1's save endpoint which creates the order in DRAFT state.

The modern panel is essentially a blank version of the order details page in draft mode — same layout, same sections, but starting from zero.

### Smarty / jQuery / Select2 stack

- Customer + address pickers use Select2 with AJAX URLs.
- Form submission uses platform's `ajaxForm` helper.
- The panel itself uses the platform's side-panel framework (`data-dismiss="panel"`).
- No Vue components are involved on this flow.

## Settings & fields

The wizard itself has no settings. Step-1 required fields are documented on [[orders-add-validation-save]]. Step-2 fields are documented on [[orders-details]].

## Business rules

- **The merchant cannot skip step 1.** Products, payment, and shipping cannot be configured on the slide-in panel — they always go through step 2 on [[orders-details]].
- **The draft is created at the end of step 1, not at the end of step 2.** The draft flag is set on the step-1 save; **Create order** in step 2 removes it **only for offline payment providers**. So a half-finished manual order in step 2 is already a draft visible in [[orders]] (filtered by "Created by admin") — and an online-payment order stays a draft even after **Create order**. See [[orders-add-draft-state]].
- **`preview=true` is not a separate route** — it's a query-string flag on [[orders-details]] that flips the page into draft-edit mode.

## Related

- [[orders-add]] — hub.
- [[orders]] — parent list with the + Add order entry button.
- [[orders-details]] — step 2 lands here in `?preview=true` mode.
- [[orders-add-draft-state]] — initial draft state set on step-1 save.
- [[orders-add-validation-save]] — required fields at step-1 save.
- [[orders-payment-mark-paid]] — the manual way to commit an online-payment draft.
- [[orders-details-known-issues]] — any status change also clears the draft flag.
- [[customers-details-shipping-addresses]] — saved-addresses list referenced by the picker.

## Open questions

None.
