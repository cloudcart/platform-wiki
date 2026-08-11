---
type: feature
nav_path: "Marketing → Segments → Condition vocabulary"
route_name: segments.core_new.list
route_path: /admin/marketing-new/segments
aliases: ["Segment conditions", "Segmentation conditions", "Condition vocabulary", "AND composition", "Allowed combinations"]
tags: [marketing, segments, conditions, rules]
plan_gates: ["subscribers-rfm"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-segments]]. See the hub for related aspects (editor, inactive errors, rebuild mechanics).

# Segments — condition vocabulary

## Purpose

This aspect catalogues the **60+ condition managers** the merchant can pick from in the segmentation rule builder — grouped by mental model — and documents the AND-only composition rule, the allowed-combination restrictions (notably for `subscriber.missing_product`), the channel-aware filters, and the verified-email gate. The visual builder itself lives on [[marketing-segments-editor]].

## Where to find it

Inside [[marketing-segments-editor]] → **Segmentation conditions** section. The condition picker is a typeahead/tree that exposes the groups below.

## What the merchant can do here

- Add up to 4 conditions (tooltip hint: *"You can add up to 4 conditions"*; actual hard cap may differ — (verify)).
- Pick an operator per condition (`any`, `=`, `<>`, `<`, `>`, `<=`, `>=`, plus type-specific ones like `begin with`, `contains`, `end with` for channel identifiers).
- Combine multi-value pickers (categories, products) with "any of" / "none of".
- Exclude "ghost" subscribers (no configured channel) via the `no_channels` filter labelled *"No channels (ghost)"*.
- Filter by which channel(s) the subscriber accepts marketing on via `subscribed_for` / `subscribed_only_for`.

## Settings & fields

### Condition vocabulary (grouped)

The full list (from the conditions catalogue):

| Group | Condition keys (examples) | What it tests |
|-------|---------------------------|---------------|
| **Subscriber** | `subscriber.channel`, `subscriber.channel.verified`, `subscriber.channel.contains`, `subscriber.type`, `subscriber.from`, `subscriber.from_form`, `subscriber.click_rate`, `subscriber.open_rate`, `subscriber.last_active`, `subscriber.browser`, `subscriber.os`, `subscriber.device_type`, `subscriber.rfm`, `subscriber.custom_field`, `subscriber.missing_product` | Channel (Email / SMS / Phone / WebPush / Messenger), email-verified state, channel-identifier substring match, subscriber-vs-customer type, source ("Subscribed by" — login, form, import, system, …), engagement (open/click rates), last-active recency, device/browser, RFM bucket, custom fields, stock-notification subscription. |
| **Customer** | `customer`, `customer.custom_field`, `customer_group`, `customers_customer` | Specific customer/customer-group membership, customer custom-field values. |
| **Country / Region** | `country`, `country.region` | Subscriber's country and city. |
| **Date** | `date`, `date_interval` | Subscribed-on date or relative interval ("in last 30 days", "before more than 6 months", "never", "sometime", "in next N days"). |
| **Order** | `order`, `order.last`, `order.status`, `order.status_fulfillment`, `without_order` | Has placed an order with specific product/category/vendor/discount/utm/status; is the order their LAST order; has NOT placed an order (with criteria); fulfillment state. |
| **Order amount/price** | `amount`, `price`, `average` | Order total turnover, single-order total, average-order-value. |
| **Cart / Abandoned cart** | `cart`, `cart.abandoned`, `begin_order` | Has active cart matching criteria; cart was abandoned; initiated checkout but didn't finish. |
| **Product / Category / Vendor** | `product`, `product.newest`, `product.sale`, `category`, `vendor` | Specific products / new-flagged / sale-flagged / category / vendor in the order / cart / view / wishlist. |
| **View / Pageview** | `view`, `page` | Viewed product / category / vendor / specific landing page (event-based tracking). |
| **Wishlist** | `wish_list` | Added a product to wishlist (with category/vendor/date filters). |
| **Quantity / Times** | `quantity`, `times` | Product count thresholds and repetition counts ("ordered ≥ 3 times", "viewed ≥ 5 times"). |
| **UTM** | `utm_source`, `utm_medium`, `utm_campaign` | Order arrived via specific marketing-attribution source. |
| **Shipping / Payment** | `shipping`, `payment` | Order used specific shipping provider / payment method. |
| **Discount** | `discount` | Order applied a specific discount. |
| **Tag** | `tag` | Subscriber has a specific tag. |
| **Others — Names** | `others.first_name`, `others.last_name` | Substring match on first / last name. |
| **Subscribed-for missing product** | `subscriber.missing_product` (special) | Subscribed to a stock-availability notification for a product that is now back in stock — combinable only with a small whitelist of conditions (see Business rules). |
| **App-provided** | `apps.others.product_review.subscriber_segments.*` (10+ conditions), `apps.administration.membership.subscriber_segments.*` (membership state) | Conditions contributed by installed apps; only available when the corresponding app is installed and active (see [[apps-product-review]], membership app). |

## Business rules

### AND-only composition

The help text on the create/edit form reads exactly: **"All conditions have a logical 'AND'"**. There is no OR composition at the top level — every condition row must match for the subscriber to qualify. To express OR, the merchant creates separate segments. Internally, a small subset of conditions can express compound logic via `sub_conditions` (e.g. `begin_order` joined with an order branch), but the merchant-visible composition is always AND.

### Allowed-combination restrictions

Some conditions can only be combined with a whitelist of other conditions. For example, `subscriber.missing_product` (subscribed-for-product-availability) can only be combined with a small set, shown as the validation message *"The condition ':condition' can only be combined with the following conditions: ':conditions'"*. This is enforced by the `allowed_combinations_conditions` array on each condition — most conditions are freely combinable; `subscriber.missing_product` and a few apps-provided conditions tighten the set.

The allowed-combinations check ALSO runs at evaluation time, not just save — see [[segments-inactive-errors]].

### Channel-aware filtering

Subscribers without a configured channel (the "ghost" condition) can be excluded explicitly via the `no_channels` filter label *"No channels (ghost)"*. Conversely, conditions like `subscribed_for` and `subscribed_only_for` filter by which channel(s) the subscriber accepts marketing on (Email, SMS, Phone, WebPush, Messenger — see [[marketing-subscribers]] channels).

### Verified-email gate

The `subscribers_channels_verified` filter labelled *"Verified his email"* only returns true for subscribers whose Email channel `verified = 1`. Unverified subscribers don't receive most campaigns by default — the Subscribers detail view warns: *"No message will be sent to this email because it has not been verified."*

### App-provided conditions require their app

`apps.others.product_review.subscriber_segments.*` conditions appear in the picker only when [[apps-product-review]] is installed and active. Same for `apps.administration.membership.subscriber_segments.*`. Uninstalling the app does NOT auto-clean existing segments that reference its conditions — instead the segment self-disables on the next rebuild (see [[segments-inactive-errors]]).

### RFM condition is plan-gated

The `subscriber.rfm` condition (RFM bucket targeting — Recency / Frequency / Monetary) is gated by the boolean plan-feature `subscribers-rfm`. When off, the RFM condition does not appear in the condition picker. See [[segments-api-and-plan-gates]].

## Related

- [[marketing-segments]] — hub.
- [[marketing-segments-editor]] — the visual builder that exposes this vocabulary.
- [[segments-inactive-errors]] — what happens when a referenced condition's dependency disappears.
- [[segments-api-and-plan-gates]] — the `subscribers-rfm` boolean gate that hides the RFM condition.
- [[marketing-subscribers]] — channel definitions (Email / SMS / Phone / WebPush / Messenger).
- [[apps-cart-rules]] — cart-rule conditions and segment conditions share managers.
- [[apps-product-review]] — contributes the `apps.others.product_review.subscriber_segments.*` family.
- [[customer-group]] — `customer_group` condition references this.

## Open questions

- 📡 **Hard cap on conditions per segment.** The tooltip hint says "up to 4 conditions" but the actual enforcement may differ (verify).
