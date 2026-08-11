---
type: feature
nav_path: "Orders → Details → Right-rail actions"
route_name: admin.orders.details
route_path: /admin/orders/details/:order_id
aliases: ["Order sidebar", "Customer card", "Notify customer toggle", "Admin note", "Recalculate lock", "Convert to EUR", "Banned IP add", "ERP rows", "Fiscal printer rows", "SmartBill", "FGO", "Profisc"]
tags: [orders, order-details, sidebar, notify-customer, admin-note, recalculate-lock, eur-conversion, erp]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 4
---

> Part of [[orders-details]]. See the hub for the other aspects.

# Order details — Right-rail actions + convenience surfaces

## Purpose

The right-hand sidebar of the order details page groups the convenience actions: the **Customer card** (Notify-customer switch + Edit customer info / View customer profile), info cards (**Order source**, IP info, cart time life), the **Convert to EUR** button, and the **Banned IP add** action. Below the products table sit the **admin Note** textarea and the **Recalculate lock** toggle. Conditional ERP / fiscal-printer rows (SmartBill, FGO, Profisc) appear when those apps are installed. **Customer address** cards are covered in [[orders-details-addresses]]; detail pages for each major action are linked inline.

## Where to find it

Sidebar: right column of `/admin/orders/details/<order_id>`. Cards stack vertically: **Customer**, **Customer address** (see [[orders-details-addresses]]), **Order source**, **Customer IP info**, **Other info**, **Cart time life**, then **Convert prices to EUR** when applicable. Below the products table: the **Comments** textarea (admin note) and the **Totals** box with the **Recalculate lock** icon next to the shipping subtotal.

## What the merchant can do here

### Customer card

| Element | When visible | What it does |
|---|---|---|
| Customer name + group badge | Always | Display name + customer-group badge. |
| Google Maps thumbnail | Only when Google Maps API key is set on [[settings-cart]] | Static map of the shipping address (billing for digital-only orders). |
| Settings cog → **Edit customer info on this order** | Only on a **registered-customer** order whose status is `pending`, `paid`, or `disputed` | Opens a slide-in side-panel — see fields below. |
| Settings cog → **View customer profile** | Only on a registered-customer order | Opens [[customers-details]]. |
| **Notify customer** switch | Only on a registered-customer order (and DISABLED for drafts) | Gates ALL future automated emails for this order. See [[orders-notify-customer]]. |

### Guest orders show a reduced Customer card

When the order was placed **without a registered customer account** (a guest checkout), the Customer card falls back to a plain name + email block. It has **no settings cog** — so no **Edit customer info on this order**, no **View customer profile** — **no Notify-customer switch**, and none of the lifetime-spend tiles. There is nothing to configure: with no customer record behind the order there is nothing to edit or link to. To get those controls the merchant has to create a customer and place the order against it.

**Customer-edit panel** (POST to `admin.orders.customer.edit`). Fields prefilled:

| Field | Name | Notes |
|---|---|---|
| **First name** | `customer_first_name` | — |
| **Last name** | `customer_last_name` | — |
| **Email** | `customer_email` | — |
| **Update customer profile too?** | `update_info` | Yes/No switch, default OFF. ON updates the customer's master record; OFF keeps it order-scoped. |

### Notify-customer switch

The **Notify customer** switch toggles `admin.orders.notify-customer` and **gates ALL future automated customer emails** for this order. Default OFF for manual orders, ON for storefront orders. See Business rules below and [[orders-notify-customer]].

### Admin-note textarea (in the totals area)

Free-form textarea at the bottom-left of the order summary, saved via `admin.orders.edit-note` (**Save** link to its right). **Visible to admin staff only** — NOT shown to the customer. Distinct from `note_customer`, the customer's checkout note shown above it in a yellow bubble.

### Recalculate-lock toggle (totals → shipping row)

A small lock icon next to the shipping subtotal, toggled via `admin.orders.recalculatele.lock` (`value=0` / `value=1`). When LOCKED (red filled lock) the platform's auto-recalculation of order totals is suppressed on save — used after a manual price adjustment to stop it reverting. Default is locked (=1) when the order's payment is `completed`, unlocked otherwise. Toggling writes a history entry: `order_lock` (action code 54) or `order_unlock` (action code 55) — see [[orders-details-history]].

### Convert-to-EUR button (Bulgarian transition)

Visible only when the site currency is `EUR` but the order's currency is `BGN`. It is **not** a display toggle: on confirm, the order's stored amounts — products, subtotals, discounts, option prices, totals, taxes, shipping and payments — are all divided by the fixed rate and written back, and the order's currency becomes `EUR`. The summary reloads and the button disappears. **The action cannot be undone from the admin.**

The confirmation dialog says exactly that ("This action cannot be undone"), and names the invoice number when the order has one — but naming it is not permission: **an order that already has an invoice number is rejected outright** with *"Cannot convert order with existing invoice number"*, and nothing is changed. So the conversion must happen **before** the invoice is issued; an invoiced BGN order stays in BGN permanently. An order whose currency is not BGN is likewise rejected.

The same conversion is needed before generating a waybill for a BGN order after 2026-01-01 — see [[orders-details-shipping]]. Every converted value is recorded in the order's history ([[orders-details-history]]).

### Banned-IP add (sidebar — IP info card)

Visible only when the order has a `customer_ip`. Each IP-info row has a **Banned IP add** button that opens the banned-IP form panel (see [[settings-banned-ip]]) prefilled with the order's IP — a fast path for blocking fraudulent buyers.

### Order source / Customer IP info / Other info / Cart time life

Read-only info cards: **Order source** (UTM source / medium / campaign + referer), **Customer IP info** (IP + geo-lookup), **Other info** (miscellaneous fields), and **Cart time life** (how long the session was active before checkout).

### Invoice / Receipt / Credit-note actions (back-references)

From the **header toolbar** (Print order PDF, **Issue return** — see [[orders-details-header]]) and product-table action rows: **Create invoice** ([[orders-invoice]]), **Generate receipt** ([[orders-receipt]]). The credit note is no longer a toolbar action — it is issued from a return in the **Returns & exchanges** box ([[orders-details-returns]] → [[orders-credit]]).

### Manual-invoice-number modal

Triggered by the **Create invoice** action row when the invoicing app uses "manual numbering" (`generate_order_type == 'manual'`). A small modal asks for the **Invoice number** (`invoice_number`, empty by default), then saves via `admin.orders.generate.invoice`. In **auto-numbered** mode no modal opens — the next number is reserved automatically. In **external-API** mode the button saves directly and calls the external service.

### ERP / fiscal-printer per-app rows (conditional)

When these apps are installed and active, extra action rows appear:

| App | Row | Action |
|---|---|---|
| **SmartBill** | "SmartBill <document type>: <number>" | **Create manual document** (no document yet) OR **Cancel document** (one exists). |
| **FGO** | "FGO <document type>: <number>" | **Create manual document** / **Cancel document**. |
| **Profisc** | "Profisc" | **Create manual document**. Only for `completed` / `paid` orders with no existing Profisc invoice ID. |
| **IMOS-3D** | Toolbar — **Download XML** | Only when a product on the order has `imos3d` metadata. |

## Settings & fields

The **Notify customer** switch writes `notify_customer`; the admin **Note** writes the order note; the **Recalculate lock** writes the order meta; **Customer edit** optionally updates the customer's master record (gated by `update_info`).

Settings that affect this surface:

- [[settings-cart]] — Google Maps API key.
- [[settings-general-operational-toggles]] — `lock_orders` + `lock_orders_time`, on **Settings → General** (moderator-lock: [[orders-details-known-issues]]).
- [[settings-invoicing]] — invoice numbering mode (auto / manual / external), driving the manual-number modal.
- [[settings-banned-ip]] — banned-IP form panel for the Banned-IP add button.
- [[settings-statuses]] — the order-status taxonomy. There is no per-status notification toggle; the gates are this order-level Notify-customer flag, the mail template's own Active flag, and the store-wide customer-email setting.
- [[settings-hooks]] — `order.updated` webhook fired by every sidebar action.

## Business rules

### Notify-customer is a flag, not a manual re-send

The switch gates FUTURE automated emails — it does NOT re-send the current status's email. To re-fire a status-change email, re-apply the status via the status pill (see [[orders-details-header]]). The switch is greyed out for drafts (`is_draft = 1`): drafts default to `notify_customer = 0` and can't be flipped ON until committed (see [[orders-add]]).

### Admin note save runs the full pipeline

Every save of the order — even editing just the admin note — runs the full save pipeline. So editing the note on a `paid + fulfilled` order can inadvertently trigger auto-promotion to `completed` and its customer email. See [[orders-details-known-issues]].

### Customer-info edit uses its OWN gate — no invoice check, but archived blocks it

The **Edit customer info on this order** link is gated on the order status being `pending`, `paid` or `disputed`. Two things merchants get wrong about it:

- **`authorized` is NOT on the list.** An order sitting on a card pre-authorisation hold cannot have its customer name / email corrected until it moves to `paid` (or the authorisation is cancelled). This is different from the line-item gate, which *does* allow `authorized`.
- **An invoice number does not block it.** Unlike line items and the billing address, the customer block on the order stays editable after the invoice is issued — the invoice's own recipient details come from the billing address, not from this card.

Saving is separately refused for **archived** orders with *"Cannot perform this operation on archived order"* — unarchive first ([[orders-archive]]). Archived orders reject the **admin note** save for the same reason, even though the textarea and its **Save** link stay on screen.

### Convert-to-EUR is one-way

There is no "Convert back to BGN" path; the conversion cannot be undone.

### `order.updated` webhook fires on every sidebar action

Every sidebar action (Notify-customer toggle, admin-note save, recalculate-lock toggle, customer-edit, address-edit) fires the `order.updated` webhook via [[settings-hooks]]. Receivers must be idempotent.

## Related

- [[orders-details]] — hub.
- [[orders-notify-customer]] — canonical Notify-customer detail page.
- [[orders-invoice]] — invoice creation flow.
- [[orders-credit]] — credit-note flow.
- [[orders-receipt]] — receipt + Print order flow.
- [[orders-user-files]] — per-order file attachments.
- [[customers-details]] — "View customer profile" target.
- [[settings-banned-ip]] — Banned-IP form panel.
- [[settings-cart]] — Google Maps API key.
- [[orders-details-returns]] — the Returns box, which now issues credit notes.
- [[orders-archive]] — archived orders reject the customer-info and admin-note saves.
- [[settings-invoicing]] — invoice numbering mode.
- [[settings-statuses]] — per-status customer-email toggle.
- [[settings-hooks]] — `order.updated` webhook.
- [[orders-add]] — manual-order-add (drafts default to `notify_customer = 0`).

## Open questions

None.
