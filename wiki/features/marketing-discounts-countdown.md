---
type: feature
nav_path: "Marketing → Discounts → Countdown"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/countdown
aliases: ["Countdown discount", "Flash sale discount", "Timed discount", "Urgency timer", "Countdown timer", "Отстъпка с обратно броене", "Таймер за отстъпка", "Флаш разпродажба"]
tags: [marketing, discounts, countdown, flash-sale, urgency-timer]
plan_gates: ["total_discounts"]
created: 2026-05-23
updated: 2026-06-10
source_count: 4
---

# Countdown discount (Timer-driven flash sale)

## Purpose

The **Countdown discount** is the discount **type** that pairs a whole-order discount (flat or percent) with a **visible countdown timer** that ticks down from a fixed number of minutes the merchant sets. The intent is urgency-driven conversion: the customer arrives at checkout, sees a pop-up modal ("Only 60 minutes left to save 20%!"), a celebration animation fires once (confetti / fireworks / parade), and a checkout-totals row with a live ticking timer shows them how much time remains.

**The timer is checkout-only.** Older wiki phrasing claimed the same timer is rendered on category pages and product-detail pages — that was incorrect. The Countdown timer is rendered ONLY in the checkout summary's totals area; category and product-detail pages do NOT show the countdown timer for this discount type. See [[countdown-discount-storefront-popup]].

Merchants reach for this type to answer: *"How do I run a 60-minute flash sale that pops a confetti modal at checkout?"* The merchant's mental model is: **one Countdown per store, per-customer-session timer, no per-product price changes** — the discount is a single whole-order subtraction at totals time.

A Countdown is a `flat`-or-`percent` whole-order discount stored as `type = 'countdown'` with timer metadata (`countdown_minutes`, `countdown_description`, `countdown_popup_effect`) — see [[countdown-discount-editor]]. Unlike ordinary `flat` / `percent` [[marketing-discounts]], it **applies per-customer-session**: the timer starts when each customer first sees the popup, not on a global clock, so two customers landing in checkout 30 minutes apart each get the full `countdown_minutes` window. Unlike a hard `date_end` expiry, `countdown_minutes` is a **soft per-session window** independent of the calendar date.

## Where to find it

From the [[marketing-discounts]] list, click **+ Add discount** and pick the **Countdown discount** type card from the type-picker modal. The form opens at `/admin/marketing-new/discounts/create/countdown`. The breadcrumb reads **Marketing → Discounts → Create discount**.

The type-picker card description reads: *"With this discount you will be able to lower the price of the entire order for a certain amount of time."*

There can be **only one** active Countdown discount per store at a time — see [[countdown-discount-single-instance]].

## Sub-pages (in this cluster)

This feature is split into 6 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[countdown-discount-editor]] — admin form fields (target, value, timer, description, animation effect, customer-group filter, dates) + the saved payload shape.
- [[countdown-discount-storefront-popup]] — the checkout-only popup endpoint, the per-cart timer meta (`countdown_popup_first_showing`, `countdown_discount_popup_was_shown`), and the three vue-rewards animations.
- [[countdown-discount-eligibility]] — the per-cart validity check chain (target, customer-group, `only_customer`, date range, per-session timer, flat-subtotal cap).
- [[countdown-discount-single-instance]] — the one-Countdown-per-store uniqueness rule, the UTC auto-disable sweep, the cooldown-free `active` toggle, plan gating.
- [[countdown-discount-cart-totals]] — totals math, the `countdown` discount group, why per-product attachment is skipped, stacking with code / order-over discounts, FastOrder bypass.
- [[countdown-discount-programmatic-access]] — JSON-API v2 NOT writable, GraphQL admin-session mutations, `discount.*` webhooks, no audit-log row.

## What the merchant can do here

- Configure the **single** Countdown discount for the store, with a per-session timer length and animation effect (confetti / fireworks / parade) — see [[countdown-discount-editor]] and [[countdown-discount-storefront-popup]].
- Restrict to **registered users only** (shown only when target = "Orders over"; defaults OFF), customer groups, and a calendar date range — see [[countdown-discount-eligibility]].
- Toggle `active` instantly (no 10-minute cooldown for Countdown) — see [[countdown-discount-single-instance]].
- Watch the discount apply at checkout as a separate `countdown` discount-group line that stacks with order-over and code discounts — see [[countdown-discount-cart-totals]].
- Mirror Countdown CRUD via `discount.*` webhooks — see [[countdown-discount-programmatic-access]].

### What the merchant CANNOT do here

- Run more than one Countdown — see [[countdown-discount-single-instance]].
- Target shipping, products, categories, vendors, smart collections, geo zones, or use a promo code — see [[countdown-discount-editor]].
- Show "was X / now Y" pricing on listings — see [[countdown-discount-cart-totals]].
- Provision via JSON-API v2 (validator allowlist excludes `countdown`) — see [[countdown-discount-programmatic-access]].

## Settings & fields

Per-aspect breakdown:

- General settings (`active`, `name`, `type`, `type_value`), target (`all` / `order_over`), timer + popup fields (`countdown_minutes`, `countdown_description`, `countdown_popup_effect`), limits, `only_customer`, customer groups, date range, `force_save` — see [[countdown-discount-editor]].
- Endpoints: create at `/admin/marketing-new/discounts/create/countdown`, edit at `/admin/marketing-new/discounts/edit/{id}`, save via POST `/admin/api/discounts`, storefront popup at `/checkout/countdown-discount-popup` (route `checkout.countdown_discount_popup`).

## Business rules

Cross-cutting summary; detail lives on the aspect pages:

- **One Countdown per store** — uniqueness ignores `active` state. Delete, don't deactivate, to free the slot. See [[countdown-discount-single-instance]].
- **Popup-driven activation** — the discount becomes active for the customer only after the storefront fires `/checkout/countdown-discount-popup`; each customer then gets their own `countdown_minutes` window from that first view. See [[countdown-discount-storefront-popup]].
- **Whole-order discount only** — Countdown skips per-product attachment, so listings never show "was X / now Y". See [[countdown-discount-cart-totals]].
- **Flat-type silently skips when `type_value > subtotal`** — cart too small, no popup. See [[countdown-discount-eligibility]].
- **No 10-minute `active` cooldown** — Countdown is exempt from the throttle applied to Flat / Percent / Shipping / Fixed. See [[discount-stacking]].
- **Auto-disable sweep runs in UTC**, not store timezone — admin "active" badge may lag by up to ~27 hours for a Europe/Sofia store; customer-visible behaviour stops at the right local time. See [[countdown-discount-single-instance]].
- **FastOrder bypasses Countdown** — [[apps-fast-order]] doesn't fire the popup. See [[countdown-discount-storefront-popup]].
- **No audit-log row** for Countdown CRUD `(verify)`. See [[countdown-discount-programmatic-access]].

## Related

- [[marketing-discounts]] — parent feature; the Countdown discount type lives there alongside flat / percent / shipping / fixed / quantity / code-pro / container.
- [[marketing-discounts-fixed]] — Fixed per-product discount; Countdown is its conceptual opposite (whole-order vs. per-product).
- [[marketing-discounts-shipping]] — Free-shipping discount (sibling type; Countdown cannot have an inner type of `shipping`).
- [[marketing-discounts-codes]] — Container codes (a code-based type; codes can fire alongside Countdown — see [[countdown-discount-cart-totals]]).
- [[marketing-discounts-code-pro]] — Code PRO multi-code campaigns; same stacking story.
- [[marketing-campaigns]] — email / push campaigns for telling customers about a Countdown ("Flash sale starts in 10 minutes!").
- [[customers-custom-groups]] — customer-group entity used by the Countdown eligibility filter.
- [[settings-hooks]] — `discount.created` / `updated` / `deleted` webhooks.
- [[settings-statuses]] — `discounts_used_statuses` setting controls which statuses count toward `max_uses`.
- [[apps-cart-rules]] — alternate engine for time-sensitive promotions (similar effects without the per-customer-session popup).
- [[apps-fast-order]] — bypasses Countdown.
- [[analytics-top-order-discounts]] — analytics dashboard; Countdown redemptions surface via `is_countdown = 1` on the `OrderDiscount` row.
- [[discount]] — entity page for the underlying Discount record.
- [[discount-stacking]] — cross-cutting per-type cooldown table + stacking ladder.
- [[plan-gates]] — `discount_global` + `total_discounts` mechanics.

## Plan gates

This feature is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `total_discounts` | Numeric (aggregate) | Aggregate cap across all discount types. Countdown counts toward this global ceiling. |

There is **no** `discount_countdown` plan-feature mapping and **no create-time plan gate** on Countdown in the modern panel — the Countdown type-picker card is not greyed out by any per-type quota (only the **Discount code** (PRO) card is plan-gated; see [[marketing-discounts]] → Plan gates). The practical limit on Countdown is the **single-instance rule**, not a plan cap: only ONE Countdown discount may exist per store at a time — see [[countdown-discount-single-instance]].

## Open questions

None at the hub level — see each aspect's `## Open questions` for unresolved items.
