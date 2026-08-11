---
type: feature
nav_path: "Orders → Abandoned → Detail view"
route_name: admin.abandoned.details
route_path: /admin/abandoned/details/{abandoned_id}
aliases: ["Abandoned cart detail", "Abandoned cart details", "Abandoned cart inspection", "Преглед на изоставена количка"]
tags: [orders, abandoned, detail-view, cart-recovery, smarty]
plan_gates: ["abandoned_orders", "abandoned_notification", "test_mail"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-abandoned]]. See the hub for the other aspects (list view, eligibility, restore link, auto-recovery, plan gates, cart lifecycle).

# Abandoned carts — Detail view

## Purpose

The per-cart inspection page at `/admin/abandoned/details/{abandoned_id}` — the merchant clicks any row from [[orders-abandoned-list-view]] to land here. Shows the cart's line items, totals, owner (customer or subscriber), and shipping address, plus the per-cart **Send restore link** action.

The page is **read-only** — the merchant cannot edit cart contents, quantities, or addresses from here. To act on the cart, the merchant either Sends the restore link (waits for the customer to return) or creates a manual order via [[orders-add]] referencing the cart.

## Where to find it

Reached by clicking any row in the abandoned list. No direct sidebar entry — every entry point flows through [[orders-abandoned-list-view]] first.

## What the merchant can do here

### Main content (left column)

1. **Products table** — items currently in the cart (lazy-loaded via the same data-box-ajax pattern as [[orders-details]] product table). Renders the empty-products warning if the cart has no items (`order.order_has_no_products`).
2. **Totals box** (right-aligned, bottom of products table) — simple totals breakdown for the cart (no taxes / no discounts editor — read-only summary).
3. **Action footer** — the Send restore link button (when eligible) + the *"Restore link last sent: <date>"* timestamp when a previous send exists.

### Sidebar — customer card OR subscriber card (mutually exclusive)

The detail page's right sidebar contains EXACTLY ONE of these two cards, chosen by the cart's owner:

**Customer card** — when the cart has a `customer_id`:

- Customer group name badge (or *"N/A"* if the customer is an OAuth guest user).
- Google Maps thumbnail of the shipping address (lazy-loaded when [[settings-general]] has a Google Maps key configured).
- Customer avatar.
- Settings cog dropdown: **View customer profile** opens [[customers-details]] in a new tab.
- Full name (linked to [[customers-details]]).
- Email (mailto link).
- Income tile: total income from this customer + completed orders count.
- Order-stats tile: total orders price + total orders count.

**Subscriber card** — when the cart has no customer but has a subscriber:

- Subscriber type badge (*"Subscriber"*).
- Settings cog dropdown: **View subscriber profile** opens a side-panel via `data-ajax-panel` for [[subscriber]] / [[marketing-subscribers]].
- Full name (linked to subscriber details panel).
- Email (mailto link).

### Address box

Below the customer/subscriber card, the sidebar renders an **Address** box with the shipping address (or *"N/A"* if none captured yet). Fields shown: company name + VAT (if business), full name, country, state, city, office (if courier-office address) OR street + number + address line, phone (international format).

### Per-cart Send action

The Send button:

- Calls the per-cart Send endpoint at `/admin/abandoned/send/{abandoned_id}`.
- Returns a payload including the localised string *"Restore link last sent: <datetime>"* (`order.info.abandoned_restore_last_sent_date`) — the page's JavaScript inserts this into the `#js-sent-date` element, so the merchant sees the updated timestamp without reloading.
- Success message: *"Email sent to client"* (`order.succ.abandoned_email_sent_to_client`).
- 404 (cart deleted in the meantime): *"Order no longer exists"* (`order.err.order_no_longer_exists`).
- Plan limit hit: a plan-warning message naming the `abandoned_notification` feature with current usage count + a link to the plan-features upsell. See [[orders-abandoned-plan-gates]].

Unlike the bulk Send from the list, the per-cart Send **does NOT skip a cart that already has a `date_sent`** — the `date_sent` check is disabled in code on this endpoint. The timestamp is overwritten on every successful per-cart send. See [[orders-abandoned-restore-link]] for the bulk-vs-per-cart contrast.

### Send button — adapts to customer vs subscriber

The button's label changes by owner:

- Cart linked to a registered customer → *"Send restore link"* (`order.action.abandoned_send_restore_link`).
- Cart linked to an email subscriber → *"Send restore link to subscriber"* (`order.action.abandoned_send_restore_link_subscriber`) — the merchant sees this is a marketing-list nudge, not a known-customer send.

### What the merchant CANNOT do here

- Edit any cart content (line items, quantities, addresses) — all read-only.
- Apply a discount to the cart — the recovery discount code is attached via the restore-link URL only; see [[orders-abandoned-restore-link]].
- Mark the cart as converted manually — conversion happens automatically when an order is placed against the cart.

## Settings & fields

The detail view itself has no configurable fields — it reflects the cart as captured. Behaviour is shaped by:

- The cart's owner (customer / subscriber) — drives sidebar card selection.
- The `test_mail` plan feature — controls whether the Send button is active or disabled-with-tooltip. See [[orders-abandoned-plan-gates]].
- The `abandoned_notification` plan cap — blocks the Send when exhausted.

## Business rules

- **Read-only by design** — cart state is the customer's session, not editable by the admin. To convert, use [[orders-add]] or wait for the restore-link click.
- **Per-cart Send is the one place a merchant can re-send to the same cart** — the bulk Send from the list silently skips already-sent carts; this endpoint does not. See [[orders-abandoned-restore-link]].
- **Eligibility still applies** — clicking Send on a cart that fails the 7-rule check silently deletes it from the list. See [[orders-abandoned-eligibility]].

## Plan gates

- `abandoned_orders` — access gate; the detail page is only reachable when the cluster is accessible.
- `abandoned_notification` — numeric cap; blocks the Send action when exhausted.
- `test_mail` — when OFF, the Send button is REPLACED with a disabled button styled in purple with a tooltip explaining the plan limit and listing the eligible plans (`order.send_abonded_order_error` + the platform code). The `test_mail` feature also acts as a global mail-suppression gate at the email-send layer. See [[orders-abandoned-plan-gates]] for the full picture.

## Related

- [[orders-abandoned]] — hub.
- [[orders-abandoned-list-view]] — the entry point that opens this page.
- [[orders-abandoned-eligibility]] — what blocks the per-cart Send.
- [[orders-abandoned-restore-link]] — what the Send action emits.
- [[orders-abandoned-plan-gates]] — plan gating of the Send button.
- [[orders-details]] — the analogous detail page for placed orders.
- [[orders-add]] — manual order creation.
- [[customers-details]] — opens from the customer card.
- [[subscriber]] / [[marketing-subscribers]] — opens from the subscriber card.
- [[settings-general]] — Google Maps API key for the address thumbnail.

## Open questions

None.
