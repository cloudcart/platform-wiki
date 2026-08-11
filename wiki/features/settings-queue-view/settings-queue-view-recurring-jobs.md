---
type: feature
nav_path: "Settings → Queue → Recurring jobs"
route_name: queue.settings
route_path: /admin/settings/queue-view
aliases: ["Recurring jobs", "Populate poller", "Queue intervals", "One-shot jobs", "Job mappings"]
tags: [settings, queue, recurring, scheduler, populate]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[settings-queue-view]]. See the hub for the other aspects (page UI, actions, visibility, running-detection, queue families, event subscribers).

# Queue — recurring jobs + populate-poller engine

## Purpose

Catalogue every recurring job mapping the platform runs — including its interval, queue, and visibility — and explain the **populate-poller** engine that schedules them (CloudCart does NOT use the application framework's Scheduler / crontab for its recurring jobs). Also documents the on-demand one-shot mappings dispatched by app actions.

## Where to find it

Sidebar → Settings → **Queue**. Route `/admin/settings/queue-view`. The visible mappings here are a small subset of the table below — see [[settings-queue-view-visibility-rules]] for which ship visible vs hidden.

## What the merchant can do here

The merchant reads `Next run` on this page to know when a periodic job will fire again. The Next run timestamp is computed by the populate-poller engine described below — NOT by a cron expression.

## Settings & fields

### Populate-poller engine — every 60 seconds

CloudCart does NOT use the application framework's Scheduler / crontab for its recurring jobs (apart from one bootstrap: `queue:init-populate` every 5 minutes, which kicks the populate-pollers if they crashed).

Instead, every **60 seconds** a set of `populate_*_tasks` jobs scan the mapping registry in the platform code and enqueue any mappings whose `last completed_at + interval` has elapsed:

| Populate mapping | Routes to queue |
|---|---|
| `populate_default_tasks` | `email` |
| `populate_system_tasks` / `populate_system_tasks_odd` / `populate_system_tasks_even` | `system9` |
| `populate_import_tasks` / `populate_import_tasks_odd` / `populate_import_tasks_even` | `import10` |
| `populate_product_images_tasks` | `product-images9` |
| `populate_segments_tasks` | `segments9` |
| `populate_subscribers_tasks` | `subscribers9` |
| `populate_campaigns_tasks` | `campaigns-messages9` |
| Plus dedicated populates for | `analytics`, `install`, `export`, `cc-system`, `campaigns-hooks`, `campaigns-process`, `searchable` (the search engine), `searchable-embedding`, `searchable-import`, `cloudio` queues |

The merchant-visible **Next run** timestamp is computed from `last completed_at + interval` — NOT from a cron expression. This means a job whose previous run is delayed will have its `Next run` shift accordingly.

### Full recurring-job table

| Mapping | Interval | Queue | Visible? | What it does |
|---|---|---|---|---|
| `currency_sync` | 12 h | `cc-system7` | yes | Refresh exchange rates platform-wide |
| `subscription_payments` | 24 h | `cc-system8` | yes | Charge due CloudCart plan invoices |
| `subscription_payments_notify` | 24 h | `cc-system8` | yes | Email merchants ahead of upcoming charge |
| `expire_subscriptions` | 24 h | `cc-system8` | yes | Mark expired subscriptions |
| `expire_free_sites_notify` | 24 h | `cc-system8` | no | Email free-tier owners ahead of trial expiry |
| `expire_offers` | 24 h | `cc-system8` | no | Close expired sales offers |
| `offer_tasks` | 24 h | `cc-system8` | no | Offer follow-up notifications |
| `ssl_cloudcart` / `ssl_sites` / `ssl_cclink` | 24 h | `cc-system8` | no | Renew Let's Encrypt certs |
| `handle_primary_domains` | 24 h | `cc-system7` | no | Reconcile primary-domain settings |
| `handle_site_status_and_db` | 24 h | `cc-system8` | no | Garbage-collect sites pending cleanup |
| `sync_modoboa` | 24 h | `cc-system7` | no | Email-hosting mailbox sync |
| `reseller_payouts` | 24 h | `cc-system8` | yes | Process reseller payouts |
| `settlement_batch` | 24 h | `cc-system8` | yes | Daily payment-provider settlement batches |
| `marketing_dashboard` | 6 h | `system7` | no | Schedule marketing-dashboard collector chain per active store |
| `borica_way4_status` | per-plugin | `cc-system8` | no | Poll Borica Way4 for delayed-capture status |
| `disable_all_expired_discounts` | 1 h | `system` | no | Disable discounts past end-date |
| `abandoned_all_cart_email` | 3 min | `system` | no | Sweep + dispatch abandoned-cart reminders |
| `delete_cart_safe` | 1 h | `system3` | no | Remove carts past retention window |
| `kill_long_process` | 2 min | `cc-system7` | no | Kill HTTP / worker processes over CPU budget — see [[settings-queue-view-running-detection]] |
| `ping_workers` | 2 min | (no fixed queue) | no | Worker liveness ping |
| `delete_temporary_product_full` | 12 h | `system` | no | Clean up half-created product records |
| `delete_s3_object` | 2 min | `system` | no | Process deferred S3-deletion queue |
| `delete_csv_tables` | 24 h | `system` | no | Drop per-site CSV staging tables older than 72 h — see [[settings-queue-view-actions]] |
| `product_change_new_status` | 4 h | `system1` | no | Demote products from "New" once auto-expiry passes |
| `product_change_featured_status` | 4 h | `system1` | no | Demote products from "Featured" once auto-expiry passes |
| `populate_*_tasks` | 1 min | varies | yes | The recurring-job poller itself |
| `populate_tasks` (legacy) | 1 min | `system8` | yes | Legacy global populate (deprecated) |
| `uninstall_un_paid_apps` | 12 h | `system7` | no | Disable apps on lapsed accounts |
| `disable_un_paid_functionality` | 12 h | `system7` | no | Disable plan features on lapsed accounts |
| `statistics_orders_fulfillment` | 24 h | `system7` | no | Aggregate order-fulfillment stats |
| `statistics_orders_payments` | 24 h | `system7` | no | Aggregate order-payment stats |
| `remove_global_import_records_failed` | 24 h | `import` | no | Cleanup failed import log records |
| `send_pending_events_for_approval` | 24 h | `cc-system` | no | Send gateway-pending events for approval |

### One-shot job mappings — dispatched on demand (no `interval`)

| Mapping | Queue | Trigger |
|---|---|---|
| `statistic` | `default` | Visit-tracking record write |
| `email` | `email` | Transactional email send |
| `products_import` | `import6` | XML / supplier product import |
| `products_import_csv` | `import6` | CSV product import |
| `customers_import` / `customers_import_csv` | `import6` | Customer import |
| `blog_import` | `import6` | Blog import |
| `blog_import_csv` | `import` | Blog CSV import |
| `redirects_import` | `import6` | Redirects import |
| `erp_imports` / `erp_imports_execute` | `import` | ERP integration import |
| `disable_missing_products` | `import2` | Post-import sweep removing missing products |
| `install_site` | `install` | Provision a new store |
| `image_from_url` | `product-images` | Download image to S3 |
| `text_image_from_url` | `product-images` | Text-image variant |
| `product_variants_images` | `product-images` | Variant-image attachment |
| `product_image_color` | `product-images` | Image dominant-color extraction |
| `product_primary_image_update` | `product-images3` | Re-pick product primary image |
| `download_aggregate` | `export6` | Export CSV / file build |
| `generate_by_sql` | `export6` | Sub-job generation by SQL |
| `delete_temporary_product` / `delete_temporary_product_execute` | `system` | Cascade-clean temp product |
| `admin_notify` | `system7` | Admin notification (bell icon) |
| `marketing_dashboard_execute` | `system7` | Per-store marketing-dashboard collector chain |
| `order_discount_usage_sync` | `order-events6` | Post-order discount usage write |
| `order_hooks_send` | `order-events8` | Webhook delivery attempt (initial multi-webhook + all retries) — see [[settings-queue-view-event-subscribers]] |
| `sites_per_industries_statistic` / `sites_incomes_by_payment_type_and_industry_statistic` | `system` | Platform-wide industry rollups |

## Business rules

### Why `Next run` can drift

Because intervals are computed as `last completed_at + interval` and the populate-poller fires every 60 s, a job whose previous run completed late will have its `Next run` shift by the lag amount. There is no fixed wall-clock schedule like cron — the schedule is relative.

### Hidden vs visible — see the visibility aspect

The "Visible?" column above mirrors `config('queue.mapping.<name>.visible')`. The full visible-vs-hidden catalogue with rationale lives in [[settings-queue-view-visibility-rules]].

### Plan tier affects which numbered sub-queue a job lands on

Many of the mappings above route to a family queue (e.g. `import`, `export`, `system`); the specific numbered sub-queue (`import6` vs `import10`, `system3` vs `system9`) is decided by the merchant's plan tier via the `<feature>-priority` plan-feature value. See [[settings-queue-view-queue-families]] for the routing rules.

## Related

- [[settings-queue-view]] — hub.
- [[settings-queue-view-visibility-rules]] — which mappings are surfaced on the merchant page.
- [[settings-queue-view-queue-families]] — worker groups + numeric-suffix routing by plan tier.
- [[settings-queue-view-running-detection]] — `kill_long_process` watchdog details.
- [[settings-queue-view-actions]] — `delete_csv_tables` 72-hour impact on re-triggering imports.
- [[settings-queue-view-event-subscribers]] — webhook fan-out via `order_hooks_send`.
- [[background-queue-inventory]] — companion catalogue: same jobs, organised by domain area.

## Open questions

None.
