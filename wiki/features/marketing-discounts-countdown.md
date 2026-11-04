---
type: feature
nav_path: "Marketing → Discounts → Countdown"
route_name: discounts-create
route_path: /admin/marketing/discounts/create/countdown
aliases: ["Countdown discount", "Flash sale discount", "Timed discount", "Urgency timer", "Countdown timer", "Отстъпка с обратно броене", "Таймер за отстъпка", "Флаш разпродажба"]
tags: [marketing, discounts, countdown, flash-sale, urgency-timer]
plan_gates: ["discount-countdown", "discount_global"]
created: 2026-05-23
updated: 2026-11-04
source_count: 4
---

# Countdown discount (Timer-driven flash sale)

## Purpose

The **Countdown discount** is the discount **type** that pairs a discount in the checkout totals (flat or percent) with a **visible countdown timer** that ticks down from a fixed number of minutes the merchant sets. The intent is urgency-driven conversion: the customer arrives at checkout, sees a pop-up modal ("Only 60 minutes left to save 20%!"), a celebration animation fires once (confetti / fireworks / parade), and a checkout-totals row with a live ticking timer shows them how much time remains.

**The timer is checkout-only.** The Countdown timer is rendered ONLY in the checkout summary's totals area `(verify)`; category and product-detail pages do NOT show the countdown timer for this discount type. See [[countdown-discount-storefront-popup]].

Merchants reach for this type to answer: *"How do I run a 60-minute flash sale that pops a confetti modal at checkout?"* The merchant's mental model is: **one Countdown at a time, per-customer-session timer, no per-product price changes** — the discount is a row in the checkout totals.

A Countdown is stored as a `flat` or `percent` discount with timer settings (`countdown_minutes`, `countdown_description`, `countdown_popup_effect`) — see [[countdown-discount-editor]]. Unlike ordinary `flat` / `percent` [[marketing-discounts]], it **applies per-customer-session**: the timer starts when each customer first sees the popup, not on a global clock, so two customers landing in checkout 30 minutes apart each get the full `countdown_minutes` window. Unlike a hard `date_end` expiry, `countdown_minutes` is a **soft per-session window** independent of the calendar date.

## Where to find it

From the [[marketing-discounts]] list, click **+ Add discount** and pick the **Countdown discount** type card from the type-picker modal. The form opens at `/admin/marketing/discounts/create/countdown`. The breadcrumb reads **Marketing → Discounts → Create discount**.

The type-picker card description reads: *"With this discount you will be able to lower the price of the entire order for a certain amount of time."*

A second Countdown can be saved, but checkout uses only the first active one found — see [[countdown-discount-single-instance]].

## Sub-pages (in this cluster)

This feature is split into 6 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[countdown-discount-editor]] — admin form fields (target, value, timer, description, animation effect, customer-group filter, dates) + the saved payload shape.
- [[countdown-discount-storefront-popup]] — the checkout-only popup endpoint, the per-cart timer meta (`countdown_popup_first_showing`, `countdown_discount_popup_was_shown`), and the three vue-rewards animations.
- [[countdown-discount-eligibility]] — the per-cart validity check chain (target, customer-group, `only_customer`, date range, per-session timer, a fixed amount larger than the subtotal).
- [[countdown-discount-single-instance]] — what happens with a second Countdown, the UTC auto-disable sweep, the `active` switch, the plan check.
- [[countdown-discount-cart-totals]] — totals math, the `countdown` discount group, why per-product attachment is skipped, stacking with code / order-over discounts, FastOrder bypass.
- [[countdown-discount-programmatic-access]] — JSON-API v2 cannot create one, GraphQL mutations, `discount.*` webhooks, no audit-log row.

## What the merchant can do here

- Configure a Countdown discount, with a per-session timer length and animation effect (confetti / fireworks / parade) — see [[countdown-discount-editor]] and [[countdown-discount-storefront-popup]].
- Restrict to **registered users only** (shown only when target = "Orders over"; defaults OFF), customer groups, and a calendar date range — see [[countdown-discount-eligibility]].
- Toggle `active` instantly — see [[countdown-discount-single-instance]].
- Watch the discount apply at checkout as a separate `countdown` discount-group line that stacks with order-over and code discounts — see [[countdown-discount-cart-totals]].
- Mirror Countdown saves via `discount.*` webhooks — see [[countdown-discount-programmatic-access]].

### What the merchant CANNOT do here

- Run two Countdowns at checkout at once: only the first active one found is used — see [[countdown-discount-single-instance]].
- Target shipping, products, categories, vendors, smart collections, geo zones, or use a promo code — see [[countdown-discount-editor]].
- Show "was X / now Y" pricing on listings — see [[countdown-discount-cart-totals]].
- Create one through JSON-API v2 — see [[countdown-discount-programmatic-access]].

## Settings & fields

Per-aspect breakdown:

- General settings (`active`, `name`, `type`, `type_value`), target (`all` / `order_over`), timer + popup fields (`countdown_minutes`, `countdown_description`, `countdown_popup_effect`), limits, `only_customer`, customer groups, date range — see [[countdown-discount-editor]].
- Endpoints: create at `/admin/marketing/discounts/create/countdown`, edit at `/admin/marketing/discounts/edit/{id}`, save via POST `/admin/api/core/discounts/countdown`, storefront popup at `/checkout/countdown-discount-popup` (route `checkout.countdown_discount_popup`).

## Business rules

Cross-cutting summary; detail lives on the aspect pages:

- **The first active one is used** — a second Countdown can be saved; checkout uses the first active one found and tries no other. Deactivating the other is enough. See [[countdown-discount-single-instance]].
- **Popup-driven activation** — the discount becomes active for the customer only after the storefront fires `/checkout/countdown-discount-popup`; each customer then gets their own `countdown_minutes` window from that first view. See [[countdown-discount-storefront-popup]].
- **A row in the totals, not a product price** — Countdown skips per-product attachment, so listings never show "was X / now Y". What the amount comes off depends on the type and target; a fixed amount can come off per piece. See [[countdown-discount-cart-totals]] and [[discount-stacking-amount-by-target]].
- **Flat-type silently skips when `type_value > subtotal`** — cart too small, no popup. See [[countdown-discount-eligibility]].
- **Auto-disable sweep runs hourly in UTC**, not store timezone — it switches a discount off at the first run after 00:00 UTC on the day after its end date, about 2 to 4 hours after local midnight for a Europe/Sofia store; checkout stops at local midnight. See [[countdown-discount-single-instance]].
- **FastOrder bypasses Countdown** — [[apps-fast-order]] doesn't fire the popup. See [[countdown-discount-storefront-popup]].
- **No audit-log row** for Countdown CRUD. See [[countdown-discount-programmatic-access]].

## Related

- [[marketing-discounts]] — parent feature; the Countdown discount type lives there alongside flat / percent / shipping / fixed / quantity / code-pro / container.
- [[marketing-discounts-fixed]] — Fixed per-product discount; Countdown is its conceptual opposite (a totals row vs. per-product).
- [[marketing-discounts-shipping]] — Free-shipping discount (sibling type; Countdown cannot have an inner type of `shipping`).
- [[marketing-discounts-codes]] — Container codes (a code-based type; codes can fire alongside Countdown — see [[countdown-discount-cart-totals]]).
- [[marketing-discounts-code-pro]] — Code PRO multi-code campaigns; same stacking story.
- [[marketing-campaigns]] — email / push campaigns for telling customers about a Countdown ("Flash sale starts in 10 minutes!").
- [[customers-custom-groups]] — customer-group entity used by the Countdown eligibility filter.
- [[settings-hooks]] — `discount.created` / `updated` / `deleted` webhooks.
- [[settings-statuses]] — `discounts_used_statuses` setting controls which statuses count toward `max_uses`.
- [[apps-cart-rules]] — alternate engine for time-sensitive promotions (similar effects without the per-customer-session popup).
- [[apps-fast-order]] — bypasses Countdown.
- [[analytics-top-order-discounts]] — analytics dashboard; Countdown redemptions surface via `is_countdown = 1` on the order discount row.
- [[discount]] — entity page for the underlying Discount record.
- [[discount-stacking]] — cross-cutting stacking ladder.
- [[discount-stacking-amount-by-target]] — what each target's amount comes off.
- [[plan-gates]] — plan-gate mechanics.

## Plan gates

This feature is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `discount-countdown` | On / off | The admin form checks it on create. If this kind is not enabled: HTTP 403 *"This feature is not enabled for your plan. To access it, please upgrade your plan."* |
| `discount_global` | Numeric | Usage figure for no-code discounts. A Countdown counts in it, active or not; only deleting lowers it. |

`total_discounts` is a displayed figure, not enforced. The Countdown type-picker card never greys out (only the **Discount code** (PRO) card is plan-gated; see [[marketing-discounts]] → Plan gates).

## Open questions

None at the hub level — see each aspect's `## Open questions` for unresolved items.
