---
type: feature
nav_path: "Orders → Details → Addresses"
route_name: admin.orders.details
route_path: /admin/orders/details/:order_id
aliases: ["Order addresses", "Order shipping address", "Order billing address", "Address edit on order", "Office pickup", "Locker pickup", "Choose existing address"]
tags: [orders, order-details, addresses, shipping-address, billing-address, pickup]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 4
---

> Part of [[orders-details]]. See the hub for the other aspects (header, products, payment, shipping, history, actions, known issues).

# Order details — Addresses

## Purpose

The shipping + billing address blocks in the right-hand sidebar of the order details page. The merchant can view both addresses, edit either (with a multi-mode panel that switches between plain address, courier office pickup, and parcel-locker pickup), swap to a different saved address from the customer's profile, or add an address from scratch when the order has none.

This page documents the SIDEBAR SECTION as it appears on order details. The full field-by-field edit flow is on [[orders-address-edit]].

## Where to find it

Sidebar of `/admin/orders/details/<order_id>`, under the **Customer** card. The shipping-address block sits above the billing block; each has its own pencil-icon (edit), **Choose existing address** link (swap), and **Add address** button (when empty).

## What the merchant can do here

### View

Each address block shows the full address as a multi-line snippet: first name + last name + phone + country + city + zip + street + (for couriers that support it) office or locker name.

When the **Customer** card has a Google Maps API key configured (set on [[settings-cart]]), a small Google Maps thumbnail of the shipping address (or billing, for digital-only orders) appears in the customer card.

For an order placed by a **registered customer**, the Customer card also shows that customer's **lifetime stats** — total spend (`orders_total_price`), total order count, completed-order count, and income — plus the customer's [[customers-custom-groups|customer group]]. It's a quick "who is this buyer" summary (returning high-value customer vs first-timer) read from the customer record; guest orders (no `customer_id`) show no stats block.

### Edit (pencil icon)

Opens a slide-in side-panel (medium width) when the address type is still editable (the gates differ for billing vs shipping — see Business rules). Two layouts depending on whether the order's shipping integration exposes office / locker pickup:

**Plain-address mode** (most carriers):

- Full address form (re-uses the customer-address form template): first name, last name, phone (with international phone validation), country, city (with geo-zone autocomplete), zip, street, etc.
- **Update address in customer's profile** checkbox (`update_address_in_profile`) — when ON, the address being saved is ALSO written to the customer's saved-addresses list. Default OFF (order-scope only).

**Office / locker mode** (Econt, Speedy, SameDay, EuShipment, BoxNow, etc.):

- Three radio buttons at the top: **To address** / **To office** / **To locker** — BoxNow shows only **Locker**.
- Switching the radio swaps the form body between three blocks:
  - **Address block** — full address form.
  - **Office block** — office picker (autocomplete from `apps.<integration>.offices`) + first name, last name, phone (all required).
  - **Locker block** — locker picker (autocomplete from `apps.<integration>.lockers`) + first name, last name, phone (all required).
- Switching the radio also dynamically REWRITES the form's POST action URL to point at the integration's `changePickup` endpoint instead of the standard address-change endpoint.

On success: reloads `#order_shipping_address` (or `#order_billing_address`), `#order_summary`, `#order_history`. Full field catalogue: [[orders-address-edit]].

### Choose existing address (swap)

Visible when the customer has ≥1 saved address of that type. Opens a slide-in panel with a single field:

- **Customer address** — select dropdown (`customer_address_id`). Options come from the customer's saved addresses, each formatted as a single-line snippet.

POSTs to `admin.orders.address.{shipping|billing}.change`.

### Add address (when no address yet)

Visible only when the order has no address of that type. Opens a slide-in panel (medium width) with the **same form** as the plain-address edit mode, including the **Update address in profile** checkbox.

## Settings & fields

The address blocks read from the order's shipping- and billing-address snapshots. The form fields are documented in detail on [[orders-address-edit]] and re-use the customer-address form (see [[customers-details]] for the parent customer profile).

The Google Maps thumbnail is gated on a Google Maps API key set in [[settings-cart]] — without it, the thumbnail is hidden but the addresses themselves still display normally.

## Business rules

### Address-edit form — radio-driven URL switching

When the shipping integration exposes office / locker pickup, switching the radio at the top of the edit panel REWRITES the form's POST action URL on the fly:

- **To address** → `admin.orders.address.shipping.edit` (standard endpoint).
- **To office** → `apps.<integration>.changePickup?type=office`.
- **To locker** → `apps.<integration>.changePickup?type=locker`.

So the SAME form submits to different backend endpoints depending on the radio choice. Office / locker submissions also expose **required** first-name / last-name / phone fields that aren't required when editing a plain address.

### Address change does NOT propagate by default

Saving a new address from the edit panel updates ONLY the order snapshot — not the customer's saved-address list. To also update the customer's master record, the merchant must tick **Update address in customer's profile** (`update_address_in_profile`) before saving. Default OFF.

This is the same toggle exposed on Add-address. The merchant should expect that, by default, addresses on the order DRIFT from the customer's profile after an edit. See [[orders-details-known-issues]].

### Billing and shipping are gated DIFFERENTLY — an invoice blocks only billing

This is the single most misread rule on the page. The pencil / **Choose existing address** / **Add address** controls are hidden per address type, and the two types do **not** use the same condition:

| Address | Editing is blocked when |
|---|---|
| **Billing** | an **invoice number** exists on the order, **OR** the order status is `completed`, **OR** the order is fulfilled. |
| **Shipping** | the order status is `completed`, **OR** the order is fulfilled. **An invoice number does NOT block it.** |

So on a `paid`, invoiced, not-yet-fulfilled order the merchant **can still fix the shipping address** (a wrong street, a wrong courier office) but **cannot** touch the billing address — the billing address is what the issued invoice was made out to, so it is frozen with it. That asymmetry is deliberate, not a bug.

Being `paid` on its own no longer freezes the billing address — only the invoice, `completed`, or fulfilment does. And note that with default invoicing settings the invoice number is issued automatically as soon as the order becomes `paid` / `completed` / fulfilled, so in practice most paid orders have a locked billing address anyway (see [[orders-details]]).

The **line-item** editing gate and the **customer-info** gate are different again — see [[orders-details-products]] and [[orders-details-actions]].

### Office / locker fields are required when in pickup mode

Switching the radio to **Office** or **Locker** turns first-name, last-name, and phone into REQUIRED fields. The plain-address mode allows partial entries; office / locker mode does not.

### Fully-digital orders may show no shipping address

When **every** line on the order is digital AND the store's `checkout_digital_shipping` setting is off, the order has no shipping address block — there is nothing to ship, so the platform drops the shipping-address relation and the customer card falls back to the **billing** address (and its map thumbnail). A mixed order (at least one physical line) keeps the shipping address.

## Related

- [[orders-details]] — hub (side-by-side comparison of the three edit gates).
- [[orders-address-edit]] — canonical address-edit detail page.
- [[orders-details-products]] — the line-item edit gate (invoice-first).
- [[orders-details-actions]] — the customer-info edit gate (`pending` / `paid` / `disputed`).
- [[customers-details]] — parent customer profile (`update_address_in_profile` writes here).
- [[customers-details-shipping-addresses]] / [[customers-details-billing-addresses]] — the customer's saved-address lists surfaced by **Choose existing address**.
- [[settings-cart]] — Google Maps API key for the sidebar address thumbnail.
- [[shipping]] — shipping integrations + the office / locker autocomplete endpoints.
- [[apps-econt]] / [[apps-dpdbulgaria-speedy|Speedy]] / [[apps-eushipment]] / [[apps-boxnow]] / [[apps-sameday]] — couriers with office / locker pickup modes.

## Open questions

None.
