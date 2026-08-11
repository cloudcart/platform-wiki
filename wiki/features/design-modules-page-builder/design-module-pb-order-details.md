---
type: feature
nav_path: "Marketing → Dynamic Pages → Page-builder modules → Order details"
route_name: admin.pages.builder
route_path: /admin/marketing/pages/builder/{page_id?}
aliases: ["Order details module", "Thank-you page receipt", "Receipt block", "Модул детайли поръчка"]
tags: [design, modules, page-builder, order, thank-you, marketing]
plan_gates: [storefront_builder]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Order details block (`order-details`)

> Part of [[design-modules-page-builder]]. See the category page for the other page-builder modules.

## Purpose

The **Order details** block renders the customer's order summary on a Dynamic page — primarily the **Thank-you page** the customer lands on after placing an order. It surfaces the order's line items, totals, shipping address, payment method, and (if available) a tracking link. The merchant uses it on the Thank-you / receipt page to give the customer a confirmation view they can save or print.

## Where to find it

Open a Dynamic page in [[marketing-landing-pages]] → click **+ Add block** → pick **Order details** from the block picker.

The block is only meaningful when the page is assigned to the `thank_you` system slot (see [[marketing-landing-pages]]) — on any other page the customer context doesn't have an order to render, and the block returns empty.

## What the merchant can do here

- Toggle the master enable switch.

(The block has no merchant-facing fields beyond the enabled toggle — what it renders is fully driven by the current customer's order context.)

## What the merchant cannot do here

- The merchant cannot customise which order fields are surfaced — the block renders the full receipt as defined by the platform.
- The merchant cannot bind it to a specific historical order — the block always uses the current checkout-success context.
- The merchant cannot use it on a non-thank-you page meaningfully — outside the post-checkout context it returns empty.

## Settings & fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `enabled` | toggle | `true` | Master on/off. |

(No additional fields — the block self-configures from the current order context.)

### Save / Reset / Cancel

Page-builder side panel — see [[marketing-landing-pages]].

## Business rules

### Renders the current checkout success order

The block pulls the order from the platform's checkout context. If the customer is currently on the Thank-you page after placing an order, the order details render. If the order context is missing or the URL segment matches `cancel`, the block returns empty.

### Thank-you slot is the intended surface

The block is designed for pages assigned to the `thank_you` system slot in [[marketing-landing-pages]]. On any other Dynamic page, the block renders empty because the platform's `checkout.order_payment` registry entry isn't populated outside the post-checkout flow.

### Customer + order are passed to the receipt partial

The block renders the order via the platform code view, passing `customer`, `order`, and the `TRACK17` shipping provider constant (so tracking links resolve correctly). The view itself is the same one used for the order-confirmation email and the order-details email link — keeping the on-page receipt visually consistent with the email receipt.

### Tracking-link integration

When the order has shipping tracking data and the carrier supports it, the receipt embeds a tracking link via Track17 (or the carrier's own URL). The block doesn't expose merchant controls for this — it's automatic per order.

### No merchant overrides

The merchant has no way to hide specific lines, tweak the totals layout, or rebrand the receipt. The block is a thin per-page surface for the platform-managed receipt template. For per-store branding, the merchant configures the theme (see [[design-themes]]) or uses [[design-custom-assets]] for CSS overrides.

## Related

- [[design-modules-page-builder]] — hub.
- [[marketing-landing-pages]] — Dynamic pages (the `thank_you` system slot is the intended surface).
- [[orders-details]] — admin-side order detail view (the receipt source).
- [[cart-vs-order-lifecycle]] — checkout flow that populates the order context.
- **Settings → Tracking** — shipping tracking configuration (drives the on-receipt tracking link).

## Open questions

- 📡 **Behaviour on cancelled order.** The block returns false when `segment(3) == 'cancel'`. Confirm exact URL patterns for cancel flows. (verify)
- 📡 **Per-payment-method receipt variants.** Some payment methods (e.g., bank transfer) include extra IBAN / reference info — confirm whether those surface here or in a sibling block. (verify)
