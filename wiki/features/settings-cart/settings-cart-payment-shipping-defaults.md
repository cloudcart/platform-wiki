---
type: feature
nav_path: "Settings → Cart and checkout → Payment and shipping defaults"
route_name: cart.settings
route_path: /admin/settings/cart
aliases: ["Default payment provider", "Default shipping type", "Default shipping provider", "Auto-select single shipping", "Payment description on checkout", "Manual order payment methods", "manual_order_payments", "default_payment_provider", "default_shipping_type", "default_shipping_provider"]
tags: [settings, cart, checkout, payments, shipping, manual-orders]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-cart]]. See the hub for the other aspects (accounts, abandoned reminder, limits, checkout fields, UI behavior, Google Maps, marketing consent).

# Cart and checkout — Payment and shipping defaults

## Purpose

Two boxes on the Cart and checkout page that together control **which payment and shipping options the customer (or the merchant) sees pre-selected at checkout**. Specifically: the default payment provider, default shipping type, default shipping provider, a UX optimisation that auto-picks the only available shipping option, whether digital-only orders still go through the shipping-address step, whether to show a description text under each payment method on the storefront, and — in a **separate** box — the subset of payment methods available when the merchant creates an order **manually** from the admin (independent of the storefront).

## Where to find it

Sidebar → Settings → **Cart and checkout** → boxes **Payment and Shipping** (`payment_and_shipping`) and **Payment methods** (`payment_methods`).

The two boxes are visually separate. The first sets storefront defaults; the second restricts admin-side options for the "create new order" flow.

## What the merchant can do here

- Pick a default payment provider that auto-selects on the checkout page.
- Pick a default shipping type and default shipping provider that auto-select.
- Toggle the "auto-pick if there's only one shipping option" UX shortcut.
- Decide whether digital-only orders still require the shipping-address step.
- Show or hide the merchant-configured description text under each payment method on checkout.
- Restrict which payment methods are offered when the merchant creates an order manually from the admin panel (separate from storefront).

## Settings & fields

### Box: Payment and Shipping (`payment_and_shipping`)

> Help text: *"If you select default shipping method and payment and shipping provider, they will be automatically selected in the checkout process. You can choose to automatically select a shipping method, if there is only one available. This will save one click for your customers."*

| Field / Control | What it does | Notes |
|-----------------|--------------|-------|
| **Ask for shipping address for digital products** (`checkout_digital_shipping`) | Whether digital-only orders still go through the shipping-address step. | |
| **Automatically select the shipping option if it is only one** (`checkout_hide_single_shipping`) | UX optimisation — skip the radio button when there's only one shipping method. | |
| **Show a description of payment methods** (`payment_description`) | Under each payment method on checkout, show the merchant-configured description text. | Customer-facing only; admin order-details view shows the description separately regardless. |
| **Choose a default payment provider** (`default_payment_provider`) | Pre-selected payment option at checkout. | Options from `meta.payment_providers`. Clearable. |
| **Choose a default shipping type** (`default_shipping_type`) | Pre-selected shipping type. | Options from `meta.shipping_types`. Clearable. |
| **Choose a default shipping provider** (`default_shipping_provider`) | Pre-selected shipping carrier within the chosen type. | Options from `meta.shipping_providers`. Clearable. |

### Box: Payment methods (manual orders) (`payment_methods`)

| Field / Control | What it does | Notes |
|-----------------|--------------|-------|
| **Payment methods** (`manual_order_payments`) | Multi-select list of payment methods available when the merchant creates an order manually from the admin panel. | Separate from the storefront payment options. Help: *"Available payment methods for orders created through the administrative panel."* |

## Business rules

### Manual-order payment methods are separate from storefront payment methods

`manual_order_payments` affects **only** what payment options the merchant sees when they create an order manually from the admin panel. The customer-facing storefront payment methods are configured in [[settings-payment-providers]]. The two can diverge — e.g., enable "Cash on delivery" only for admin-created orders, but not for the storefront. This is a common pattern when the merchant wants to record offline payments without exposing them publicly.

### `manual_order_payments` is stored as a serialized PHP array

The setting is internally stored as a **PHP-serialized string**, not as JSON. Practical consequences:

- A merchant inspecting the raw settings table (or backup) sees `a:N:{...}` style strings, not `["cod","bank-transfer",...]` arrays.
- A merchant clearing all options (multi-select empty) stores `null` (not `a:0:{}`), which the formatter then returns as an empty array.
- If a merchant has set up `manual_order_payments` and then later removes the underlying payment provider in [[settings-payment-providers]], the removed provider's identifier may remain in the serialized array — defensive but not actively cleaned up. The merchant should re-save this box after removing a provider.

### `payment_description` is a customer-facing detail only

This is the description shown UNDER each payment method on the **checkout page**. It is NOT the description shown to the admin in the order details — that's separate. When OFF, the customer just sees the payment method's name and icon. When ON, the merchant's free-text description appears in small print beneath each option.

### Defaults are pre-selections, not restrictions

Setting `default_payment_provider` does NOT hide the other payment options at checkout — the customer can still change the selection. It is purely a UX pre-fill. To restrict which payment methods appear, the merchant uses the storefront payment options configured in [[settings-payment-providers]] (and for admin-created orders, the `manual_order_payments` multi-select in this same screen).

### Single-shipping auto-pick interacts with shipping rules

`checkout_hide_single_shipping` only triggers when the platform's shipping-rules logic resolves to exactly one shipping option for the current cart (destination + weight + carrier availability). If multiple options resolve, the customer still sees radio buttons. So the merchant cannot use this toggle to force a specific carrier — they configure carrier availability in the [[shipping]] settings; the toggle is a pure UX optimisation.

### Digital-only orders and the shipping address step

`checkout_digital_shipping` controls whether a cart containing ONLY digital products still goes through the shipping-address step. With it OFF, digital-only carts skip the shipping section entirely. Carts mixing physical + digital always show the shipping step regardless.

## Related

- [[settings-cart]] — hub.
- [[settings-payment-providers]] — storefront payment options the merchant configures separately; defaults selected here.
- [[shipping]] — storefront shipping options the merchant configures separately; default type/provider selected here.
- [[orders-add]] — the admin "create new order" flow that uses `manual_order_payments`.
- [[checkout-flow]] — the customer-facing checkout sequence.
- [[settings-cart-checkout-fields]] — sibling aspect; `checkout_digital_shipping` interacts with whether shipping-address fields are visible at all.
- [[product]] — the digital-product flag that drives the `checkout_digital_shipping` rule.

## Open questions

_None._
