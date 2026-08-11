---
type: feature
nav_path: "Concept → Analytics pipeline → Event processing"
route_name: ""
route_path: ""
aliases: ["Analytics event processing", "Per-order analytics job", "Raw events store", "Fast lane analytics"]
tags: [analytics, pipeline, queue, orders]
plan_gates: []
created: 2026-06-10
updated: 2026-06-11
source_count: 3
---

> Part of [[analytics-pipeline]]. See the hub for the other aspects (event capture, aggregation, dashboard reads, known gaps, backfill commands).

# Analytics — event processing (raw events + per-order fast lane)

## Purpose

This page covers the **storage + fast-lane processing** stages: where the captured browser events land (the raw analytics events store), and the parallel **per-order pipeline** that reacts to order changes and writes per-order analytics records within seconds. This is the **fast lane** — what makes a brand-new order show up in **Total Sales** within ~1–2 minutes, while **Total Visits** still waits up to an hour for [[analytics-aggregation]] to tick.

## Where to find it

Invisible to the merchant — no admin screen. The merchant only sees the downstream effect: order-driven dashboard boxes (Total Sales, Total Orders, Customer Value, Top Products by Sales, Sales by Location, etc.) updating within ~1–2 minutes of an order being placed or edited.

## What the merchant can do here

Nothing directly — this is the data plumbing behind the order-driven dashboard boxes. Merchant-side actions that trigger writes here:

- **Place an order on the storefront** → a per-order analytics task runs after a 60-second delay → the order's analytics records are written.
- **Edit an order's lines, discounts, or shipping** (add / edit / remove a product line, add / remove a line discount, remove a line modification, change shipping) → a per-order task runs after a 5-second delay → the records are re-written.
- **Update an order's payment** (e.g. mark a bank-transfer order paid) → re-write after a 5-second delay.
- **Change an order's status** (e.g. to Paid / Completed / Pending), **add or remove a fulfilment line**, or **run a payment-provider sync** → the per-order task runs **immediately**, with no delay.

## Settings & fields

Not applicable — no merchant-facing controls. Two ops-side kill switches (set in platform config, not in any admin screen) are checked at the very top of every analytics task:

| Setting key | Effect |
|-------------|--------|
| `uuid.enabled` | Platform-wide kill switch — when `false`, ALL analytics writes are suspended. |
| `uuid.disabled_sites` | Per-site opt-out list — any `site_id` listed here is skipped (the task logs a warning and returns). |

## Business rules

- **Raw events store.** The browser `CCE.event(...)` calls (see [[analytics-event-capture]]) post a tiny payload to the ingest service, which stores **one record per event** in the raw analytics events store. Each event record carries: which store it belongs to (`site_id`), the visitor's anonymous identity (`uuid_id`) and `session_id`, the event type (`product`, `category`, `cart`, `initiatedCheckout`, `purchase`, `home`, `page`, etc.), parsed browser info (`device` = desktop / mobile / tablet, plus name and OS), `referrer` (referrer host and UTM source / medium / campaign), a logged-in `customer` snapshot (null for guests), an `order` snapshot for `purchase` events, the per-event-type payload, and the UTC timestamp. Two companion stores hold **visitor identity over time** (one record per anonymous visitor; a marketing-campaign click can bind a visitor to a subscriber id here — see [[analytics-event-capture]]) and **per-session aggregates**. A customer login or logout invalidates the session cache so the customer snapshot is re-attached on the next page view. The raw events store is read by [[analytics-aggregation]] on every hourly tick.

- **Per-order fast lane.** When an order is created or modified, the per-order task reloads the order, re-runs the denormalisation across every analytics surface (full order details, bundles, categories, customer value, discounts, landing pages, locations, product discounts, products, referrers, returning customers, totals, UTM attribution, vendors), and writes the per-order analytics records that the order-driven dashboard boxes read.

- **Why the 60-second delay on a new order.** It is deliberate: the storefront checkout request returns the thank-you page to the customer without waiting for the analytics write. Order edits use a shorter 5-second delay; status, fulfilment, and payment-sync events run immediately because their audit value is real-time.

- **Per-order writes are idempotent.** Each record is keyed per order, so re-running the task overwrites the same record rather than duplicating it.

- **Isolated processing lane.** Per-order processing runs on its own background lane, separate from the hourly aggregation lane. A flood of order edits cannot block the hourly tick, and a slow tick cannot block per-order processing.

- **Kill switches apply here too.** Both `uuid.enabled` and `uuid.disabled_sites` are checked at the top of every per-order task and every hourly-aggregation task. Toggling either one suspends analytics for all stores (or one store) at the next worker run — no partial writes, no half-aggregated rows. See [[analytics-known-gaps]] for the full kill-switch model.

### Effect on the merchant

A brand-new order placed at 14:35 typically shows up in **Total Sales / Total Orders / Customer Value / Top Products by Sales / Sales by Location** within about **1–2 minutes** of placement (the 60-second initial delay, plus queue processing and denormalisation time). If a merchant says *"I placed an order 30 seconds ago and Total Sales still says zero"*, the right answer is: *"wait 1–2 minutes; the per-order task runs with a 60-second delay so the storefront checkout doesn't have to wait for the analytics write."*

## Related

- [[analytics-pipeline]] — hub.
- [[analytics-event-capture]] — where the raw events come from in the first place.
- [[analytics-aggregation]] — the hourly slow-lane that reads the raw events and rolls them up.
- [[analytics-dashboard-reads]] — how the per-order records written here surface on the dashboard boxes.
- [[analytics-known-gaps]] — currency / FX behaviour on the rolled-up `amount` fields.
- [[settings-hooks]] — outbound webhooks fire on the same order-event stream.
- [[notification-delivery]] — admin alerts share the same event stream.
- [[order-status-workflow]] — status transitions drive the per-order task chain.

## Open questions

None.
