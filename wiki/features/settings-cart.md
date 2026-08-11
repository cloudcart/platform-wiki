---
type: feature
nav_path: "Settings → Cart and checkout"
route_name: cart.settings
route_path: /admin/settings/cart
aliases: ["Cart and checkout", "Checkout settings", "Cart settings", "Кошница", "Чекаут", "Поръчка"]
tags: [settings, cart, checkout, orders]
plan_gates: ["abandoned_orders", "checkout"]
created: 2026-05-21
updated: 2026-06-10
source_count: 7
---

# Cart and checkout

## Purpose

The single admin screen where the merchant configures everything that happens between "customer hits Add to cart" and "order is placed". It is the **hub** for: account requirements, the abandoned-cart reminder pipeline, default payment/shipping at checkout, hard caps on cart contents, the stock-decrement timing rule, the order-number format, per-field visibility of every standard checkout field (incl. company/VAT), cart-UI behaviour on the storefront, Google Maps integration for address/office/locker maps, the payment-method list available when the merchant creates an order manually from admin, and (when CloudCart's GDPR app is OFF) the marketing-consent checkbox + Terms of Service page link.

## Where to find it

Sidebar → Settings → **Cart and checkout**. Route: `/admin/settings/cart`. Breadcrumb: "Settings → Cart and checkout".

The page is a single scrollable surface of **ten inline-editable boxes** (eleven when the GDPR app is not installed — the "Marketing and Terms of service" box appears only in that case). One global **Save** button in the page header POSTs the entire payload across every box in one request. There is no per-box partial save. Each box has an info-help panel on the right side with explanatory text.

## Sub-pages (in this cluster)

This feature is split into 9 aspect pages, each scoped to one box (or one set of related boxes). The Assistant should drill into the aspect that matches the merchant's question.

- [[settings-cart-accounts-registration]] — Customer accounts verification, registered/guest mix, guest-to-member auto-conversion, registration-time address requirements, hide-prices-for-anonymous toggle.
- [[settings-cart-abandoned-reminder]] — Abandoned-cart email pipeline; master switch, channel (only `email` active), 30/45/60/90/180-minute interval, the 3-minute sweep cadence, plan-gate skip rules.
- [[settings-cart-payment-shipping-defaults]] — Default payment provider, default shipping type/provider, single-option auto-select, payment-method description toggle, the **separate** `manual_order_payments` list for admin-created orders.
- [[settings-cart-limits-and-decrement]] — `checkout_min_price`, `checkout_max_price`, `cart_max_products`, `cart_max_quantity`, `product_threshold`, `order_status_for_quantity_decrease`, `order_id_display`, `order_complete`.
- [[settings-cart-checkout-fields]] — Per-field visibility (first name, last name, phone, state, street, apartment, postal code), `checkout_hide_billing_address` + invoicing-address rule, EU VIES VAT validation, company name / VAT / BULSTAT / MOL fields.
- [[settings-cart-ui-behavior]] — Cart icon, bubble counter (variants vs total qty), in-cart sort order, button animations, Buy-now action options, side-panel cart, merge-on-login.
- [[settings-cart-google-maps]] — Google Maps API key + live validation, the three map switches (addresses / office / locker), the legacy-version warning module.
- [[settings-cart-google-maps-troubleshooting]] — the **legacy Places API** breakage (autocomplete stops working at checkout → *"Въведете улица и град…"* required-region error), the fix (enable **Places API New** + re-validate), and the `googleMapKeyStatus` live diagnostic.
- [[settings-cart-marketing-consent]] — (GDPR app OFF only) "I accept marketing" checkbox, Terms of Service page picker, additional consent pages module.

## What the merchant can do here

Every capability on this page is covered by a dedicated aspect page (see the Sub-pages list above). Briefly: configure accounts, the abandoned-cart reminder, payment/shipping defaults, cart caps and stock-decrement, checkout-field visibility, cart UI behaviour, Google Maps, and marketing consent.

## Settings & fields

See each aspect page. The full inventory of setting keys is grouped by box:

| Box (code identifier) | Aspect page |
|-----------------------|-------------|
| `account_and_profile`, `reg_and_req` | [[settings-cart-accounts-registration]] |
| `abandoned_cart` | [[settings-cart-abandoned-reminder]] |
| `payment_and_shipping`, `payment_methods` | [[settings-cart-payment-shipping-defaults]] |
| `order_quantity` | [[settings-cart-limits-and-decrement]] |
| `process_orders`, `company_info` | [[settings-cart-checkout-fields]] |
| `miscellaneous` | [[settings-cart-ui-behavior]] |
| `google_api_key` | [[settings-cart-google-maps]] |
| `marketing` (GDPR off only) | [[settings-cart-marketing-consent]] |

## Business rules (cross-cutting only)

These rules apply across boxes; rules specific to one box live in that box's aspect page.

### Settings cache is cleared on save

Saving the page flushes the platform settings cache. The next read everywhere in the system (admin and storefront) sees the new values immediately.

### Cart settings save uses an attribute-by-attribute setter pattern

When the page POSTs the settings payload, the backend iterates each `<key, value>` pair and calls a corresponding `set<Key>` method on a settings formatter. Any key the merchant or client sends that doesn't have a matching setter is **silently dropped** — no validation error, no save. Typos in setting keys are swallowed.

### Backend validation is permissive

The backend the platform code only validates four fields:

- `product_threshold` (nullable, integer ≥ 0)
- `checkout_customer_access` (required, one of `both`, `member`, `guest`)
- `unconfirmed_accounts_restrict` (required, one of `none`, `checkout`)
- `google_map_api_key` (nullable, max 50 chars; live-validated against Google's endpoint when non-empty)

**Every other field on this page passes without server-side validation rules.** Min / max prices, cart quantities, etc., are not validated for type or range at save-time. The frontend converts empty values to `0`, but bad clients could send any string.

### Numeric defaults on save

The save handler explicitly defaults the following numeric fields to `0` if empty on submit: `checkout_min_price`, `checkout_max_price`, `cart_max_products`, `cart_max_quantity`, `product_threshold`. So clearing a field is equivalent to setting it to 0 (i.e., "no limit" for the first four; "no low-stock email" for the threshold). The `checkout_other_pages` array is dropped from the payload entirely if empty (rather than sent as `[]`).

### "Hide" switches sometimes invert semantics

Several switches use inverted semantics for code reasons — the UI label is positive (*"Show…"* / *"Require…"*) but storage is the opposite. See each aspect page for which switches behave this way. Complete cross-cutting list:

| UI label | Setting key | UI ON stores | Aspect |
|----------|-------------|--------------|--------|
| Require postal/zip code at checkout | `post_code_not_required` | `false` (required) | [[settings-cart-checkout-fields]] |
| Show Google map in addresses | `checkout_hide_address_map` | `false` (show) | [[settings-cart-google-maps]] |
| Show Google map in Office Delivery | `checkout_hide_office_map` | `false` (show) | [[settings-cart-google-maps]] |
| Show Google Map in Locker Delivery | `checkout_hide_locker_map` | `false` (show) | [[settings-cart-google-maps]] |
| Show "I accept marketing" checkbox | `hide_marketing` | `false` (show) | [[settings-cart-marketing-consent]] |

A support agent looking at a raw API dump should mentally invert these five keys before reasoning about merchant intent.

### Conditional field visibility — `dependField` map

The Cart page has these UI-level `dependField` rules controlling sub-field visibility (the parent must hold the listed value). They are **purely cosmetic** — the backend doesn't enforce them.

| Sub-field | Parent field | Parent value | Aspect |
|-----------|--------------|--------------|--------|
| `guest_to_customer` | `checkout_customer_access` | `both` | [[settings-cart-accounts-registration]] |
| `abandoned_remainder_type` | `abandoned_remainder` | `true` | [[settings-cart-abandoned-reminder]] |
| `abandoned_remainder_interval` | `abandoned_remainder` | `true` | [[settings-cart-abandoned-reminder]] |
| `checkout_require_billing_address` | `checkout_hide_billing_address` | `false` or `0` | [[settings-cart-checkout-fields]] |

## Related

- [[settings]] — parent hub.
- [[settings-general]] — `site_email` (where admin notifications including low-stock alerts go) and the currency setting that affects min/max amount fields.
- [[settings-admin-notifications]] — gates the `product_quantity_low` alert + the abandoned-cart pipeline indirectly (notification suppression).
- [[settings-payment-providers]] — storefront payment options the merchant configures separately; this page selects DEFAULT and MANUAL-ORDER payment options.
- [[shipping]] — storefront shipping options; this page selects defaults.
- [[settings-invoicing]] — `invoicing_address` (BillingAddress vs ShippingAddress) decision also affects how invoices compute totals.
- [[settings-statuses]] — `order_status_for_quantity_decrease` references the order/payment statuses defined there.
- [[checkout-flow]] — the cross-feature concept page on the end-to-end checkout sequence.
- [[cart]] — the merchant-visible cart entity.
- [[order]] — the order entity created from a successful checkout.
- [[discount-stacking]] — discount application logic that interacts with cart total caps.
- [[plan-gates]] — `abandoned_orders` and `checkout` are gated plan features.
- [[notification-delivery]] — concept page on email/SMS/webhook delivery used by the abandoned-cart pipeline.
- [[background-queue-inventory]] — catalogue of all background processes; covers the every-3-minute abandoned-cart sweep and the hourly cart-cleanup that ages out stale carts.
- [[order-processing-pipeline]] — the guest-to-customer conversion side-effect at order placement (Stage 1 step 1).
- [[inventory-tracking]] — uses `order_status_for_quantity_decrease` + `product_threshold` from this page.
- [[inventory-decrement-timing]] — the canonical reference for the `paid` vs `pending` decrement rule.

## Open questions

_None._
