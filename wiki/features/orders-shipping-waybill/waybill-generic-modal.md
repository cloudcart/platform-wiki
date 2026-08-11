---
type: feature
nav_path: "Orders → Order details → Shipping → Waybill → Generic modal"
route_name: admin.internal.waybill
route_path: /admin/orders/action/shipping/:order_id/waybill
aliases: ["Generic waybill modal", "Minimal waybill form", "Fallback waybill", "Tracking number form", "Manual waybill"]
tags: [orders, shipping, waybill, generic, fallback, tracking, manual]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-shipping-waybill]]. See the hub for other aspects (generate flow, courier specifics, payer side, print PDF, remove/void, API path).

# Waybill — generic fallback modal

## Purpose

The platform's **minimal fallback waybill form**, used when the order's shipping provider does NOT register its own waybill route. Allows the merchant to manually enter a tracking number + URL + dates and mark the order fulfilled — without touching a courier's API.

This is the form for "internal / generic shipping" and custom couriers that lack a CloudCart integration. It is also the surface for the EUR-route hard-block (see below).

## Where to find it

[[orders-details]] → Shipping action row → **Generate waybill** button — BUT only when the courier doesn't expose `apps.<courier>.waybill`. The routing rule is documented below.

## What the merchant can do here

- Enter tracking number, tracking URL, expedition date, delivery date by hand.
- Toggle off the customer email notification.
- Submit "Fulfill products" (status_fulfillment → `fulfilled`; status stays as-is).
- Submit "Complete order" (`#fulfillComplete`) — saves waybill AND flips order status to `completed` in one click.

The merchant CANNOT toggle insurance from this form (the insurance block is code-disabled — see below). Insurance changes happen only via courier-specific waybill flows.

## Settings & fields

### TWO distinct waybill entry points — courier-specific vs generic

**This is the single biggest UI nuance.** The Generate waybill button on [[orders-details]] routes to ONE of TWO different forms depending on whether the order's shipping provider exposes its own waybill route:

| Condition | Button opens | Form complexity |
|-----------|--------------|-----------------|
| Provider has `apps.<courier>.waybill` route registered (Econt, Speedy, DPD-BG, BoxNow, Sameday, GLS, etc.) | The COURIER'S own waybill page — see [[waybill-courier-specifics]] | Rich — per-courier fields. |
| Provider has NO `apps.<courier>.waybill` route (internal / generic shipping, custom couriers without their own form) | Generic platform modal `admin.internal.waybill` | Minimal — 4 fields. |
| Order currency = BGN (post-2026-01-01 transition) | `admin.eur.waybill` route is FORCED instead | Hard-throws "Convert order to EUR" error before any form opens. |

So a Bulgarian merchant using Econt for an EUR order opens Econt's rich form; the same merchant on a BGN order gets the EUR-block error; a Romanian merchant on a custom courier gets the minimal generic form.

### Generic waybill modal fields (`product/waybill.tpl`) — verified template

| Field | Element | Default | Notes |
|-------|---------|---------|-------|
| **Shipping expedition date** | Date picker (no minutes) | empty | Format from site's current date format. Stored as `shipping_date_expedition`. |
| **Shipping delivery date** | Date picker (no minutes) | empty | Format from site's current date format. Stored as `shipping_date_delivery`. |
| **Tracking number** | Text input | empty | Free-text. Stored as `shipping_tracking_number`. |
| **Tracking URL** | Text input | empty | Optional. Max 255 chars (silently rejected if longer). Stored as `shipping_tracking_url`. |
| **Email notification** | Hidden input controlled by a switch | `yes` | Modal-switch toggle (on/off labels from data attrs). When OFF, the customer is NOT emailed the fulfillment notification. |
| **Products to ship** | Hidden inputs | (auto) | One hidden `products_ids[]` per non-digital, non-fulfilled product on the order (server-prefilled). Merchant has no checkbox to deselect individual products on this generic form. |
| **Order ID** | Hidden input | (auto) | Stored as `order_id`. |
| **Submit "Fulfill products"** | Submit button | — | Saves waybill (`status_fulfillment` → `fulfilled`; status stays as-is). |
| **Submit "Complete order"** | Submit button (`#fulfillComplete`) | — | Appends `?complete` to the form action — saves waybill AND flips order `status` to `completed` in one click. |

### Empty-products error

When the order has zero shippable products (all digital OR all already fulfilled), the modal shows ONLY this alert with no form: *"No products to fulfill"*.

### Marketplace pickup banner

When `provider->manager->getSupportType` includes `SUPPORT_MARKETPLACE`, an extra Centered button appears ABOVE the form: *"Change marketplace pickup"* — opens `apps.shipping.changePickup` panel in `?type=marketplace` mode. Used by Amazon FBA / Frisbo-style integrations.

### Insurance toggle — currently CODE-DISABLED

The template has a `shipping_provider_insurance` checkbox + `change-shipping-provider-insurance` AJAX call to `admin.internal.insurance`, but the block is wrapped in `{if $provider && $provider->insurance && 1 == 0}` — the `1 == 0` guard makes it ALWAYS hidden. **Insurance changes happen only via the courier-specific waybill flows.** The platform's generic modal cannot toggle insurance.

## Business rules

### EUR-variant waybill — disabled after 2026-01-01

The `admin.eur.waybill` route is hard-coded to throw the Bulgarian-language error message: *"Поръчки в BGN не могат да се изпращат след 01.01.2026. Моля, конвертирайте поръчката в EUR."* (Orders in BGN cannot be shipped after 01.01.2026. Please convert the order to EUR.)

This is part of Bulgaria's BGN→EUR transition. Merchants on BGN orders placed BEFORE 2026-01-01 use the standard waybill route normally; the EUR route was a temporary alias that now surfaces a hard-stop conversion-required error.

The message is HARD-CODED in Bulgarian and is NOT localised. For non-Bulgarian merchants on the platform, this surface should not be hit — but if it is, they get a Bulgarian-only error.

To proceed, the merchant must convert orders to EUR using the [[orders-details]] currency-convert action before dispatch.

### The merchant cannot use this form to talk to a courier

The generic modal does NOT call any courier's API. It only writes the tracking number, dates, URL, and fulfillment status locally. The merchant is responsible for producing the physical label and dispatching the package by other means (the courier's own dashboard, drop-off at an office, etc.).

If the merchant wants programmatic dispatch (courier API call, courier-formatted label PDF), they must use a courier integration that registers `apps.<courier>.waybill` — see [[waybill-courier-specifics]].

### Email notification toggle

The "Email notification" switch on this form maps to the order's `notify_customer` flag for THIS fulfillment event only. When toggled OFF, the customer fulfillment-notification email is NOT sent — but other channels (downstream app webhooks, [[settings-statuses]] notifications) still fire normally. See [[orders-notify-customer]] for the general rule.

### Validation gauntlet still applies

Same validation as the rich form per [[waybill-generate-flow]]: archived-order block, shipping-provider-required, non-digital-products filter, stock-tracking check, already-fulfilled rejection, 255-char URL cap.

## Related

- [[orders-shipping-waybill]] — hub.
- [[waybill-courier-specifics]] — the rich per-courier form (taken when a courier registers its own route).
- [[waybill-generate-flow]] — the validation gauntlet and side effects.
- [[apps-bgn2eur]] / [[apps-bgn2eur-settings]] — BGN→EUR transition app.
- [[orders-details]] — parent screen + currency-convert action.
- [[orders-notify-customer]] — fulfillment-notification email toggle.
- [[shipping]] — provider configuration (whether the provider registers `apps.<courier>.waybill`).

## Open questions

None.
