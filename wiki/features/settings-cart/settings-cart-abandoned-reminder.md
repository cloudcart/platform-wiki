---
type: feature
nav_path: "Settings → Cart and checkout → Abandoned cart reminder"
route_name: cart.settings
route_path: /admin/settings/cart
aliases: ["Abandoned cart reminder", "Abandoned cart email", "Abandoned reminder interval", "abandoned_remainder", "abandoned_remainder_interval", "abandoned_remainder_type", "Abandoned cart pipeline"]
tags: [settings, cart, checkout, abandoned-cart, email, background-jobs]
plan_gates: ["abandoned_orders"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-cart]]. See the hub for the other aspects (accounts, payment/shipping defaults, limits, checkout fields, UI behavior, Google Maps, marketing consent).

# Cart and checkout — Abandoned cart reminder

## Purpose

The box on the Cart and checkout page that controls the **abandoned-cart email pipeline** — a background job that emails customers who left items in their cart without completing the order. The merchant chooses whether the pipeline runs at all, the channel (currently only `email`), and the delay between cart-abandonment and the first reminder email (30, 45, 60, 90, or 180 minutes). The pipeline is gated by the `abandoned_orders` plan feature; without it, the job exits early and sends nothing regardless of the toggle.

## Where to find it

Sidebar → Settings → **Cart and checkout** → box **Abandoned cart reminder** (`abandoned_cart`). Header label on this box reads *"Processing orders"*.

## What the merchant can do here

- Turn the entire abandoned-cart reminder pipeline ON or OFF.
- Pick the delivery channel (currently only **Email** is selectable; Messenger options are present in the Vue source but commented out — see Business rules).
- Pick the delay before the first reminder fires: **30 / 45 / 60 / 90 / 180 minutes**. CloudCart's recommendation is **60**.

## Settings & fields

### Box: Abandoned cart reminder (`abandoned_cart`)

> Help text: *"All customers that haven't finished their orders, will be notified by an email about their abandoned orders. Choose a communication channel where we will send abandoned cart notifications. We strongly recommend to choose only one channel. Otherwise you are at risk to frustrate your potential customers. Here you can specify minutes when CloudCart will send the first abandoned message to the customer. We recommend to set it to 60 minutes after the user abandoned his cart."*

| Field / Control | What it does | Notes |
|-----------------|--------------|-------|
| **Abandoned cart reminder** (`abandoned_remainder`) | Master switch for the entire reminder pipeline. When OFF, no reminders go out regardless of the channel/interval. | Plan-gated: requires the `abandoned_orders` feature on the merchant's plan. Without it, the background job exits early and sends nothing. |
| **Send abandoned cart reminders via** (`abandoned_remainder_type`) | Currently only `email`. (Messenger options are present in code but commented out.) | Visible only when the master switch is ON (dependField rule). |
| **Send abandoned reminder in (minutes)** (`abandoned_remainder_interval`) | 30 / 45 / 60 / 90 / 180. Time after the customer becomes "abandoned" before the first reminder fires. | Visible only when the master switch is ON. CloudCart's recommendation is 60. |

## Business rules

### The reminder pipeline is queued, plan-gated, and runs on a fixed sweep cadence

When the merchant enables the reminder, the merchant-visible effect is delayed delivery, not immediate. The pipeline:

1. The storefront marks a cart as "abandoned" after the customer leaves it for the configured interval (30 / 45 / 60 / 90 / 180 minutes).
2. A platform-wide scheduled sweep iterates every site and dispatches one per-site reminder job. The sweep runs every **3 minutes** (180 seconds), single-instance (no two runs overlap), on the system queue — see [[background-queue-inventory]].
3. Each per-site job:
   - **Skips** if the site is plan-expired, in maintenance mode, on the wrong platform, or doesn't have the `abandoned_orders` plan feature.
   - **Skips** if `abandoned_remainder=no`.
   - Loads all abandoned-cart rows that haven't been emailed yet (`date_sent IS NULL`).
   - For each cart, generates a restore-code and increments a per-site send counter (with up to 3 retries on counter-increment failure).
   - Logs delivery success/failure into the platform's exceptions log.

So merchants should expect a reminder email to be sent within their configured interval **plus up to 3 minutes** of sweep-delay. A 60-minute setting delivers between ~60 and ~63 minutes after the cart was last modified.

### "Abandoned" definition

A cart qualifies for the abandoned-cart reminder when **all three** conditions hold:

1. The cart has items.
2. Its last-modified timestamp is older than the merchant's configured interval (30 / 45 / 60 / 90 / 180 minutes).
3. The customer is **identifiable** — either a logged-in account OR a newsletter subscriber on the email channel (verified email, when the platform requires confirmed subscribers).

Anonymous, never-identified visitors are NOT eligible — the platform has no way to email them.

### Plan-tier double-check

Even with abandoned-cart reminders enabled, an additional plan check gates whether the email is actually sent. If the merchant exhausts the plan's monthly abandoned-notification quota, sending fails silently and the cart stays unemailed. The merchant won't see an error in the admin — only the absence of expected delivery.

### Only the Email channel is active

The **Send abandoned cart reminders via** dropdown renders with only **Email** visible. The Vue source has commented-out options for **Email + Messenger combined** and **Messenger only** — likely temporarily disabled while the Messenger integration is paused. A merchant trying to send via Messenger today cannot; only email is possible.

### Once-per-cart, opt-out via reactivation

The pipeline sends **one** reminder per abandoned cart (driven by the `date_sent IS NULL` filter). If the customer reactivates the cart (adds/removes items, resetting `last_modified`) without completing the order, a new abandoned-cart row is eligible on the next sweep — so the cycle restarts but the platform doesn't send back-to-back reminders to the same customer for the same untouched cart.

### Cron sweep coordination

The sweep job is dispatched onto the `system` queue and is the same scheduler that handles other every-N-minute / hourly housekeeping. The hourly **cart-cleanup** (ages out stale carts entirely) runs on a separate schedule and is documented in [[background-queue-inventory]]. The two interact: a cart that ages out before being marked abandoned (e.g., interval = 180 min but cart-cleanup is 1 hr) will never trigger a reminder — but the abandoned-cart cleanup uses a much longer horizon than the reminder interval so this is rare in practice.

## Related

- [[settings-cart]] — hub.
- [[plan-gates]] — `abandoned_orders` plan feature gates this pipeline.
- [[background-queue-inventory]] — the every-3-minute sweep job; the hourly cart-cleanup that ages out stale carts.
- [[notification-delivery]] — the email-delivery layer this pipeline uses.
- [[cart-vs-order-lifecycle]] — concept page on cart-stage vs order-stage semantics, including the "abandoned" state.
- [[cart]] — Cart entity that the pipeline reads.
- [[customer]] — the identifiable-customer requirement for eligibility.
- [[settings-admin-notifications]] — administrator-side notification gating (can suppress notifications indirectly).

## Open questions

_None._
