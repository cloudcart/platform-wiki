---
type: feature
nav_path: "Settings → Queue → Visibility rules"
route_name: queue.settings
route_path: /admin/settings/queue-view
aliases: ["Queue visibility", "is_visible filter", "Queue site scoping", "Queue permission"]
tags: [settings, queue, visibility, permissions]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-queue-view]]. See the hub for the other aspects (page UI, actions, running-detection, recurring jobs, queue families, event subscribers).

# Queue — visibility rules

## Purpose

Document exactly which rows are eligible to appear on the Queue page: the `is_visible` flag (configured per job mapping, code-level, not merchant-toggleable), the per-site `site_id` hard-scoping, the `settings.queue` permission gate, and the catalogue of jobs the platform ships as visible vs hidden.

## Where to find it

Sidebar → Settings → **Queue**. Route `/admin/settings/queue-view`. The rules below decide what the merchant actually sees in the table.

## What the merchant can do here

Nothing configurable — visibility is platform-level and read-only for the merchant. The merchant CAN, however, infer from the visibility catalogue why a given background process never appears on this page.

## Settings & fields

### Three filter layers in series

A queue row only appears on the page if **all three** pass:

1. **Permission gate** (route level) — `hasApiPermission:settings,settings.queue`. Moderator needs either the broad **Settings** permission OR the specific **Queue Jobs** (`settings.queue`) grant from [[settings-staff]]. Owners always pass.
2. **`site_id` filter** — controller hard-codes `site_id = site('site_id')`. Only rows for the current store. Multi-site staff cannot see all sites' queues from one place.
3. **`is_visible = true` filter** — only rows whose mapping is flagged visible in the platform config.

### Mapping-level visibility — config-baked, not merchant-toggleable

The `is_visible` flag for each job type is read from `config('queue.mapping.<name>.visible')` on the platform — a code-level configuration baked into the deploy. The merchant cannot toggle visibility from this page.

### Jobs the platform ships as VISIBLE

| Category | Mappings |
|---|---|
| Imports | `erp_imports`, `erp_imports_execute`, `products_import`, `products_import_csv`, `customers_import_csv`, `customers_import`, `blog_import`, `blog_import_csv`, `redirects_import` |
| Recurring system | `currency_sync` (12 h), `subscription_payments` (24 h), `subscription_payments_notify`, `expire_subscriptions`, `reseller_payouts` (24 h), `settlement_batch` (24 h) |
| Other periodic | XML feed regenerate, the populate-poller mappings (`populate_*_tasks`) |

### Jobs the platform ships as HIDDEN

These run in the background but never surface on this page:

- `disable_all_expired_discounts`, `abandoned_all_cart_email`, `clear_all_old_carts`, `delete_cart_safe`
- `statistic_records`, `marketing_dashboard`, `marketing_dashboard_execute`
- Image-pipeline: `product_variants_images`, `image_from_url`, `text_image_from_url`, `product_image_color`, `product_primary_image_update`
- Housekeeping: `delete_csv_tables`, `delete_temporary_product_full`, `delete_s3_object`, `kill_long_process`, `ping_workers`
- SSL renewal: `ssl_cloudcart`, `ssl_sites`, `ssl_cclink`
- Plan-feature lifecycle: `uninstall_un_paid_apps`, `disable_un_paid_functionality`
- Status sweeps: `product_change_new_status`, `product_change_featured_status`, `expire_offers`, `offer_tasks`, `expire_free_sites_notify`
- Stats rollups: `statistics_orders_fulfillment`, `statistics_orders_payments`
- Misc: `handle_primary_domains`, `handle_site_status_and_db`, `sync_modoboa`, `borica_way4_status`, `remove_global_import_records_failed`, `send_pending_events_for_approval`

For the full interval and queue routing of every mapping see [[settings-queue-view-recurring-jobs]].

## Business rules

### Why webhook deliveries usually do NOT appear

Webhook `HooksSendRaw` deliveries run as the application framework queue jobs on the `order-events8` queue (see [[settings-queue-view-event-subscribers]]) — separately from the per-site `SiteQueue` model that powers this page.

Whether a given webhook delivery shows up on this page depends on whether the platform marks the SiteQueue row as `is_visible=true`. In practice the diagnostic merchant-facing view on this page is more useful for tracking **per-site scheduled jobs** (feed regenerations, imports, abandoned-cart sweeps, etc.); for webhook-specific failures the merchant relies on the webhook auto-disable alert from [[settings-hooks]] and their own receiver-side logging.

### "Single" jobs run platform-wide — may still appear

Some mappings configured as `single => true` (e.g. `currency_sync`, `subscription_payments`, `expire_subscriptions`) run with `site_id = NULL` so a single execution covers the whole platform — they don't fire one-per-store.

These rows can still surface on the merchant's Queue page because the `where('site_id', site_id)` filter is permissive enough to include null on certain views, OR they are wrapped by per-site execute jobs that then create per-site rows. Practical implication: the merchant may see `currency_sync` running once every 12 hours platform-wide, not once per store.

### Permission gate consequence — moderators may see an empty / 403 page

A moderator without the **Settings** or **Queue Jobs** (`settings.queue`) permission grant from [[settings-staff]] cannot reach this route at all (gated by `hasApiPermission`). Owners always pass.

### Visibility cannot be toggled per merchant

There is no merchant-facing screen to flip a job mapping from hidden to visible or vice versa. Changes require a platform-level config update and a deploy.

## Related

- [[settings-queue-view]] — hub.
- [[settings-queue-view-recurring-jobs]] — what each visible / hidden mapping does + interval.
- [[settings-queue-view-event-subscribers]] — why webhook deliveries follow a separate visibility path.
- [[settings-queue-view-page]] — what the merchant sees once all three filter layers pass.
- [[settings-staff]] — `settings.queue` permission grant.
- [[settings-hooks]] — webhook auto-disable alert for webhook-specific diagnostics.

## Open questions

None.
