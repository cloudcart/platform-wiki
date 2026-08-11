---
type: feature
nav_path: "Orders → Abandoned"
route_name: admin.abandoned.list
route_path: /admin/abandoned
aliases: ["Abandoned carts", "Abandoned orders", "Cart recovery", "Abandoned cart list", "Изоставени поръчки", "Изоставени колички"]
tags: [orders, abandoned, cart-recovery, smarty]
plan_gates: ["abandoned_orders", "abandoned_orders_info", "abandoned_notification"]
created: 2026-05-23
updated: 2026-06-10
source_count: 9
---

# Abandoned carts

## Purpose

The **abandoned-cart list** — shows shopping carts where a customer (or identified email subscriber) added products, stayed inactive past the recovery threshold, but did NOT place an order. The merchant uses this page to manually send the customer a **restore link** encouraging them to return and complete checkout.

This page complements the automated abandoned-cart recovery email flow — the merchant can send the recovery link on demand (for VIP customers, or as a manual nudge) instead of relying solely on the scheduled email that runs every 3 minutes. See [[orders-abandoned-auto-recovery]] for the scheduled flow.

When the store has zero abandoned carts, the page shows a dedicated empty-state screen — see [[orders-abandoned-list-view]].

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages. Each aspect stands alone; the Assistant should drill into the page that matches the question, not read every one.

- [[orders-abandoned-list-view]] — list grid (4 columns, 4 filters, 2 bulk actions), sort behaviour, empty-state screen, what the merchant CANNOT do.
- [[orders-abandoned-detail-view]] — per-cart detail page, customer-vs-subscriber sidebar, products / totals / address boxes, button-label adaptation.
- [[orders-abandoned-eligibility]] — the 7-rule eligibility check, subscriber email-channel resolution at update time, silent cart deletion on invalid eligibility.
- [[orders-abandoned-restore-link]] — restore URL format `/restore-abandoned/{code}/{source}/{discount_code?}`, unique-code generation, UTM stamping, recovery-source vocabulary (`email` + `messenger`), order attribution.
- [[orders-abandoned-auto-recovery]] — the every-3-minutes scheduled job, `abandoned_remainder` master switch, `date_sent` skipping in bulk + auto contexts, queued dispatch with 10-second delay.
- [[orders-abandoned-plan-gates]] — the three plan features (`abandoned_orders` access gate, `abandoned_orders_info` dashboard tile, `abandoned_notification` numeric cap), `test_mail` per-cart Send gating, plan-disabled landing page, counter persistence across plan resets.
- [[orders-abandoned-cart-lifecycle]] — `abandoned_remainder_interval` 60-minute default and 30-minute clamp floor, the hourly cart cleanup at 7 days inactivity, why sent carts persist indefinitely.

## Where to find it

Sidebar → **Orders** → **Abandoned**.

The page is part of the Orders module. Listed under [[orders]] in the sidebar navigation.

## What the merchant can do here

At a glance:

- Browse abandoned carts (4-column grid + 4 filters). See [[orders-abandoned-list-view]].
- Open any cart for read-only inspection (line items, totals, customer/subscriber info, address). See [[orders-abandoned-detail-view]].
- Send a restore-link email — single cart from the detail view, or bulk-selected from the list. See [[orders-abandoned-restore-link]] for the URL contract and [[orders-abandoned-eligibility]] for what blocks a send.
- Delete abandoned carts in bulk.

The cart contents are NOT editable from these pages — the merchant must use [[orders-add]] to convert a cart to a manual order, or wait for the customer to return through the restore link.

## Settings & fields

The cluster involves three store-level settings (all on [[settings-cart]] / store settings — verbatim keys):

- `abandoned_remainder` (yes / no) — master switch for the automated 3-minute recovery job. When OFF, only manual sends from this page fire. See [[orders-abandoned-auto-recovery]].
- `abandoned_remainder_interval` (minutes, default `60`, effective floor `30`) — inactivity threshold before a cart appears in the list. See [[orders-abandoned-cart-lifecycle]].
- `cart.lifetime` (days, default `7`) — global cart-record lifetime; sent + unsent carts age out via the hourly `clear_all_old_carts` cleanup.

Plus three plan-feature keys: `abandoned_orders`, `abandoned_orders_info`, `abandoned_notification`. See [[orders-abandoned-plan-gates]].

## Business rules

Cluster-wide rules (each detailed in the aspect pages):

- **Two populations covered** — registered customers (`user_id` link) AND identified email subscribers. Subscribers must be email-verified IF the email channel's `unconfirmed_send` setting is OFF. See [[orders-abandoned-eligibility]].
- **Bulk vs per-cart send differ on the `date_sent` check** — bulk send silently skips already-sent carts; per-cart Send (from the detail view) allows re-send and overwrites the timestamp. See [[orders-abandoned-restore-link]].
- **Invalid carts are silently deleted on Send** — not just blocked. The merchant sees a success toast, the cart vanishes from the list. See [[orders-abandoned-eligibility]].
- **Plan counter `plan.count.email.abandoned_notification` is a permanent setting**, not bound to the plan period — does NOT reset on plan renewal / upgrade. See [[orders-abandoned-plan-gates]].
- **Sent carts persist indefinitely** — there is no scheduled cleanup of sent abandoned carts. They age out only via the 7-day cart cleanup, conversion, or manual delete. See [[orders-abandoned-cart-lifecycle]].

## Plan gates

Three plan-features control this cluster (see [[plan-gates]] / [[plan-vs-feature-pack]] / [[plan-features]]):

| Plan feature | Shape | Effect |
|---|---|---|
| `abandoned_orders` | Access gate | Blocks `/admin/abandoned` route entirely. Sidebar entry hidden. Direct URL → redirected to [[plan-features]] upsell. |
| `abandoned_orders_info` | Boolean (dashboard tile) | Controls the abandoned-orders dashboard tile only — does NOT affect this list. |
| `abandoned_notification` | Numeric cap (sends per period) | Blocks the Send restore link action once the running counter hits the cap. |

Plus the `test_mail` plan feature gates the per-cart Send button on the detail view and acts as a store-wide outbound-email suppression. Full details — including the disabled-state landing template and counter persistence semantics — on [[orders-abandoned-plan-gates]].

## Related

- [[orders]] — parent orders list; recovered orders appear there with the Recovered source filter.
- [[orders-details]] — recovered orders link back to their originating cart.
- [[orders-add]] — manual order creation (the only way to convert a cart to an order without the customer returning).
- [[marketing-discounts]] — recovery discount codes appended to restore-link URLs.
- [[analytics-abandoned-carts]] — analytics view of abandoned-cart trends.
- [[analytics-abandoned-checkout]] — checkout abandonment analytics (one step further down the funnel).
- [[settings-cart]] — `abandoned_remainder`, `abandoned_remainder_interval`, `cart.lifetime`.
- [[settings-admin-notifications]] — adjacent admin-notification configuration.
- [[cart]] — entity page (the abandoned cart is the same underlying cart entity).
- [[customer]] — entity page (cart owner).
- [[subscriber]] / [[marketing-subscribers]] — subscriber side of the population.
- [[marketing-dashboard]] — UTM-tracked attribution surfaces here.
- [[background-queue-inventory]] — catalogue of background jobs; covers the every-3-minute abandoned-cart sweep and the hourly cart cleanup.
- [[plan-gates]] / [[plan-features]] / [[plan-vs-feature-pack]] — plan-gating model.

## How it works (verified against backend)

The detailed verified behaviour lives on the aspect pages — split so each Assistant query can pull the one slice it needs:

- **List rendering, sort, filters, bulk actions, empty state** → [[orders-abandoned-list-view]].
- **Per-cart detail page, sidebar cards, totals, address box** → [[orders-abandoned-detail-view]].
- **Eligibility (the 7-rule gate), subscriber channel resolution, silent deletion** → [[orders-abandoned-eligibility]].
- **Restore-link URL, code generation, UTM, recovery sources, attribution** → [[orders-abandoned-restore-link]].
- **Scheduled 3-minute job, queue dispatch, date_sent semantics** → [[orders-abandoned-auto-recovery]].
- **All four plan keys (`abandoned_orders`, `abandoned_orders_info`, `abandoned_notification`, `test_mail`), counter persistence, disabled landing page** → [[orders-abandoned-plan-gates]].
- **Threshold defaults, 30-minute floor clamp, 7-day cart cleanup, sent-carts-persist rule** → [[orders-abandoned-cart-lifecycle]].

## Open questions

(All resolved — distributed to aspect pages.)
