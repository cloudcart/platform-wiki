---
type: feature
nav_path: "Settings → Webhooks → Activity log & troubleshooting"
route_name: hooks.settings
route_path: /admin/settings/hooks
aliases: ["Webhook activity log", "Webhook log", "Webhook troubleshooting", "last_used_at", "Last used count", "allowed_logging", "Webhook diagnostics"]
tags: [settings, webhooks, logging, troubleshooting, integrations]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-hooks]]. See the hub for the other aspects (events, delivery, retry, auto-disable, modal, auth & headers).

# Webhooks — activity log & troubleshooting

## Purpose

Every delivery attempt (success and failure) IS recorded on the backend with timestamp, request payload, response code, and error message. **However, the activity log is OFF by default for production stores** — it's an internal diagnostic surface that CloudCart support enables per-store on request. This page documents the gap, the last-used counter behaviour (which IS merchant-visible), and the practical troubleshooting workflow.

## Where to find it

- **Last-used count column** in the webhooks table on Sidebar → Settings → **Webhooks** — the only merchant-visible delivery indicator.
- **No in-product activity-log viewer.** The deep-dive log of past attempts lives only in an internal backend store, gated by an internal allowlist (see below) — not exposed to merchants in any UI.

## What the merchant can do here

- Read the **Last-used count** column in the table to confirm a webhook is firing at all (any non-zero count = the platform has tried delivery; see counter semantics below).
- For deeper diagnostics, the practical options are:
  - **Contact CloudCart support** and ask them to enable the activity log for the store. Support adds the store's Site ID to the allowlist and reads the log back to the merchant.
  - **Add detailed logging on the merchant's own receiver side** (recommended — most reliable, no support roundtrip).
- Watch [[settings-queue-view]] for retry rows (visible) — see [[settings-hooks-retry]] for what is and isn't visible there.
- Watch [[settings-admin-notifications]] for auto-disable and final give-up alerts — see [[settings-hooks-auto-disable]].

## Settings & fields

### Last-used count — increments on EVERY attempt, NOT just success

This corrects an older wiki claim. The hook-usage counter is incremented every time a delivery is logged — which happens **BOTH on success AND on failure** (after the error is caught, before a retry is scheduled). So:

- A webhook that's failing repeatedly will show an **inflated counter** — each retry adds to the count.
- The "Last used count" is more accurately a **"delivery attempt count"**, not a successful-delivery count.
- The webhook's last-used timestamp tracks the most recent attempt (success or fail).

**Practical implication for merchants debugging:** a high counter on a webhook whose receiver claims no successful requests is consistent — those are failed attempts, not successes. To find out which, the merchant needs the activity log (see below).

### Backend activity log (gated)

The platform records every webhook delivery attempt with:

- Timestamp.
- Outgoing request payload (full body).
- Response HTTP status code.
- Response body (or error message for failed attempts / exceptions).

This log lives in an internal backend store that is **NOT merchant-visible**. The merchant has no UI to query it.

### Why the log is OFF by default — the internal allowlist

Logging is gated by an internal allowlist that defaults to **a single internal CloudCart test store** (used for QA). A second store is present in the list but disabled. The merchant **cannot flip this from the admin panel** — there is no UI surface for enabling activity logging on their own store.

Enabling it for a production merchant currently requires:

1. CloudCart support / an engineer adds the merchant's store to the allowlist.
2. The change is deployed.
3. After the next failure, the engineer reads back the recorded log.
4. After troubleshooting, the engineer may remove the store from the allowlist again (or leave it for ongoing diagnosis).

Development environments bypass the allowlist entirely (they log everything) — but that's only for CloudCart engineers, not merchants.

### Practical troubleshooting workflow for a merchant today

1. **Check the Last-used count column.** Non-zero = the platform attempted delivery. Zero = the platform never tried (event didn't fire, or the webhook is inactive, or the event-fanout dispatcher is broken).
2. **Check the webhook's Active flag.** If OFF, the platform skipped delivery entirely — see [[settings-hooks-auto-disable]] for the auto-disable triggers.
3. **Check [[settings-queue-view]]** for any pending retry rows on the webhook-events queue — see [[settings-hooks-delivery]] for what's visible there.
4. **Check [[settings-admin-notifications]]** for an auto-disable or final give-up alert (it will name the URL and the disable reason).
5. **Check the merchant's own receiver logs.** If the receiver has any logging at all, this is the fastest source of truth — what was received, what was returned, when.
6. **Contact CloudCart support** if the above don't isolate the issue — only support can enable the backend activity log.

### Why this is the biggest webhook UX gap

There is no self-service way for a merchant to see *"what was sent, what did my receiver return, when did each attempt happen"*. The gap blocks production merchants from debugging webhook issues independently and forces a support roundtrip for every diagnostic. The merchant's only proactive defence is **adding logging on the receiver side BEFORE issues arise**.

## Business rules

- **The counter never resets on auto-disable.** A webhook auto-disabled at counter=347 stays at 347 visible in the table even after the merchant manually re-enables it. Future successful attempts increment from that base.
- **No counter reset on edit.** Editing the URL, event, or headers does NOT reset the counter — the row is the same logical subscription.
- **Counter is per-webhook, not per-event-instance.** Two webhooks subscribed to `order.created` each maintain their own counters independent of each other.
- **The development-environment bypass is irrelevant to production debugging.** Even though non-production environments enable logging globally, merchants never see those logs — they live in non-production environments.

## Related

- [[settings-hooks]] — hub.
- [[settings-hooks-delivery]] — what triggers the counter increment (every attempt).
- [[settings-hooks-retry]] — retry attempts that inflate the counter.
- [[settings-hooks-auto-disable]] — what stops the counter from incrementing further (the row goes inactive).
- [[settings-queue-view]] — partially-visible diagnostic surface for queued retries.
- [[settings-admin-notifications]] — the alert surface for auto-disable + final give-up.

## Open questions

- Will a self-service activity-log viewer ever ship? This has been the biggest webhook UX gap for years. (verify)
- Confirm whether the counter is reset by the "duplicate then delete" workaround merchants sometimes use to reset their integration metrics. (verify)
