---
type: feature
nav_path: "Apps → Mailchimp → Sync engine"
route_name: apps.mailchimp.overview
route_path: /admin/apps/mailchimp
aliases: ["Mailchimp sync engine", "Mailchimp sync cadence", "Mailchimp incremental sync", "Mailchimp queue mappings", "Mailchimp batch info", "Mailchimp customer field mapping", "Mailchimp sync retry", "last_mailchimp_synchronization"]
tags: [apps, marketing, mailchimp, sync, queue, background]
plan_gates: ["mailchimp"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[apps-mailchimp]]. See the hub for the other aspects (two-list model, Commerce, limits & consent).

# Mailchimp — the sync engine

## Purpose

The Mailchimp integration syncs in the **background, hourly, and incrementally** — not in real time. This page documents the two queue mappings and their cadence, how the integration tracks "what changed since last time", the retry/backoff behaviour when Mailchimp is slow or unreachable, the per-contact field payload, and the `batch_info` status card the merchant sees on the disconnect screen.

## Where to find it

There is no dedicated merchant UI for the sync engine — it runs in CloudCart's background-job system (see [[settings-queue-view]]). Its visible surfaces are the **batch_info card** on the Mailchimp disconnect screen (see [[apps-mailchimp-settings]]) and the eventual appearance of contacts/orders in the merchant's Mailchimp account.

## What the merchant can do here

- Read the **batch_info card** on the disconnect screen to see the last sync's outcome (operations queued / finished / errored, submission + completion time).
- Trigger an initial full sync by clicking **Connect** (which enqueues the sync jobs — see [[apps-mailchimp-settings]]).

### What the merchant CANNOT do here

- Set the sync interval — it is fixed at hourly for both queues.
- Force an immediate (real-time) push — changes appear in Mailchimp on the next hourly run.
- Configure retry/backoff thresholds — they are platform-fixed (see below).

## Settings & fields

| Setting | Meaning |
|---|---|
| `last_mailchimp_synchronization` | Timestamp of the last full sync — drives incremental scoping. |
| `mailchimp_last_batch_id.id` | The Mailchimp batch ID of the last run — read back to populate the `batch_info` card. |
| `api_connect_sync` | Failure counter for the 3-strike API-connection backoff. |

### Per-contact field payload (Customer)

The data pushed to Mailchimp's ecommerce store for each customer:

- `id` — CloudCart customer ID.
- `email_address` — customer's email.
- `opt_in_status` — always `true` (see [[apps-mailchimp-limits-consent]]).
- `first_name` / `last_name`.
- `orders_count` — the customer's `completed_orders` count.
- `total_spent` — the customer's `income` (money-formatted).
- `address` block — `address1`, `street`, `street_number`, `city`, `postal_code`, `country`, `country_code`, `phone`, `province`, `longitude`, `latitude`. For a company customer, also `company_name` + `company_vat`.

The address is taken from the customer's `shipping_address`; if missing, it falls back to `billing_address`. Separately, a PATCH to `lists/{list_id}/members/{hash}` sets the audience member's `language` — see the language note below.

## Business rules

### Two queue mappings, both hourly

| Queue mapping | What it does | Interval |
|---|---|---|
| `mailchimp_sync` | Full ecommerce sync (customers, products, order-products, orders), enqueued as a Mailchimp Batch operation. | 3600 s (1 hour) |
| `mailchimp_newsletter` | Newsletter-specific sync (subscribers from [[marketing-subscribers]]). | 3600 s (1 hour) |

Both run on the `export` queue. So even at peak, expect roughly a **1-hour lag** between a new subscriber/customer in CloudCart and them appearing in Mailchimp. Clicking Connect dispatches the initial run; thereafter the queues fire hourly.

### Incremental sync via `last_mailchimp_synchronization`

After each full sync, the integration stores the run timestamp in `last_mailchimp_synchronization`. Subsequent syncs scope to changed records only — a customer is included when `updated_at >= last_mailchimp_synchronization` OR `date_added >= last_mailchimp_synchronization` OR the customer has a related order with `updated_at >= last_mailchimp_synchronization`. So ongoing sync is **incremental by record-change-time**, not real-time event-driven. The merchant should expect a sync lag between a change in CloudCart and its appearance in Mailchimp; the lag depends on when the hourly job next runs.

### Batch state tracking — the `batch_info` card

The integration stores Mailchimp's batch ID in `mailchimp_last_batch_id.id` after each run. The settings endpoint reads it back and queries Mailchimp's `/batches/{id}` for live status — this powers the **batch_info card** on the disconnect screen. The card shows whatever the batch-status endpoint returns:

| Key | Meaning |
|---|---|
| `id` | Mailchimp batch ID. |
| `status` | `pending`, `preprocessing`, `started`, `finalizing`, `finished`. |
| `total_operations` | Operations queued in the batch. |
| `finished_operations` | Operations completed. |
| `errored_operations` | Operations that returned errors. |
| `submitted_at` | When the batch was submitted (datetime). |
| `completed_at` | When Mailchimp finished it (datetime; null until done). |

If Mailchimp returns an error envelope instead, the card shows its `title` + `detail` keys. Each key renders as a label-value row.

### Retry on a still-running batch — 2-minute backoff

If a previous Mailchimp batch is still running when the sync job fires, the job exits with a 120-second retry delay — preventing concurrent batches from clobbering each other.

### API-connection failure — 3-strike retry then disable

If the Mailchimp API is unreachable, the job increments the `api_connect_sync` counter. After **3 failures** the counter resets and the job returns successfully (skipping that sync). Below 3 failures, the job retries every 6 minutes. This is the platform's defensive backoff against a stuck Mailchimp account.

### Site locale → Mailchimp member language

For every customer sync, the integration PATCHes `lists/{list_id}/members/{hash}` with `{language: <site current locale>}` — pushing the **site's active locale**, NOT the customer's individual locale preference. So a multi-language store syncing in one locale tags ALL customers with that one language in Mailchimp. To tag a different language, the merchant must run sync after switching the site's active locale.

### Permission

Standard apps permission scope.

## Related

- [[apps-mailchimp]] — hub.
- [[apps-mailchimp-two-list-model]] — the two audiences the two queues feed.
- [[apps-mailchimp-commerce]] — the ecommerce push the `mailchimp_sync` queue performs.
- [[apps-mailchimp-settings]] — where the batch_info card renders.
- [[apps-mailchimp-limits-consent]] — why `opt_in_status` in the payload is always true.
- [[settings-queue-view]] — the background-job system that runs both queues.
- [[customers]] — source of the per-contact payload.
- [[marketing-subscribers]] — source for the newsletter queue.

## Open questions

_None._
