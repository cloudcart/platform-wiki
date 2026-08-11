---
type: concept
nav_path: "Concept → Background processes → Internal-identifier catalogue"
aliases: ["Background process catalogue", "Process identifiers", "Queue identifiers", "Internal queue reference", "Platform process names", "AI Agent process catalogue"]
tags: [background, async, internal-reference, ai-agent, support, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[background-queue-inventory]]. See the hub for related aspects (recurring platform jobs, imports/exports, the search index sync, order side-effects, Queue View).

# Background processes — internal-identifier catalogue (AI Agent reference)

## Definition

This aspect maps every merchant-facing background process to the platform's **internal process identifier** (the string used in the queue-inspection tooling), so the Assistant can identify the right process when querying that tool. It is never shown to the merchant.

**Critical rule: do not paste these identifiers to the merchant.** They are dev-internal strings (e.g., `abandoned_all_cart_email`, `ssl_sites`). The merchant sees the human-readable name on [[settings-queue-view]] ("Abandoned cart recovery emails", "SSL renewal — merchant sites"). Always answer with the human name from the left column.

## Scope

Covered:

- One-to-one mapping: merchant-facing process name → internal identifier.
- Per-process recurrence cadence (3 min, hourly, every 4 / 6 / 12 h, daily, on-demand).
- The single-platform-wide-lock flag — whether the process holds a global lock (one at a time) or runs concurrently across sites.

Not covered:

- The merchant-facing behaviour of each process — see the corresponding aspect ([[background-queue-recurring-platform]], [[background-queue-imports-exports]], [[background-queue-order-side-effects]]).
- Per-process Queue View visibility — see the visibility column in each aspect's table.
- The underlying scheduler / Cron configuration — platform-internal.

## Contrasts

- **Internal identifier vs merchant-facing name.** The identifier is a stable string used in queue tooling; the name is human-readable and may be translated. Assistant uses the identifier internally, the name externally.
- **Single-platform-wide lock vs concurrent.** Locked processes (subscription renewals, settlement batches, SSL renewal) run one at a time across the entire platform — only one execution exists globally. Concurrent processes (CSV imports, image fetches, webhook delivery) run in parallel per site / per merchant.
- **Recurring cadence vs on-demand.** Recurring processes have a fixed cadence; on-demand processes fire only when triggered. A few are both (e.g., `marketing_dashboard` recurs every 6 h, but a separate execute branch is on-demand).

## Where it applies

### Catalogue table

Look up the internal identifier before querying the queue-inspection tool. Identifiers are verbatim platform data, not code references.

| Merchant-facing process | Internal identifier | Recurrence | Single-platform-wide lock |
|---|---|---|---|
| Abandoned cart recovery emails | `abandoned_all_cart_email` | 3 min | Yes |
| Old cart cleanup | `clear_all_old_carts` | 1 h | Yes |
| Stale safe-delete cart cleanup | `delete_cart_safe` | 1 h | Yes |
| Expired discounts de-activation | `disable_all_expired_discounts` | 1 h | Yes |
| Subscription renewals | `subscription_payments` | 1 d | Yes |
| Subscription renewal notifications | `subscription_payments_notify` | 1 d | Yes |
| Expired subscriptions reconciliation | `expire_subscriptions` | 1 d | Yes |
| Free-site expiry notifications | `expire_free_sites_notify` | 1 d | Yes |
| Site status + DB reconciliation | `handle_site_status_and_db` | 1 d | Yes |
| Reseller payouts | `reseller_payouts` | 1 d | Yes |
| CloudCart Pay settlement batch | `settlement_batch` | 1 d | Yes |
| Offer expiry | `offer_tasks` / `expire_offers` | 1 d | Yes |
| Unpaid-app uninstall | `uninstall_un_paid_apps` | 12 h | Yes |
| Unpaid-functionality disable | `disable_un_paid_functionality` | 12 h | Yes |
| SSL renewal (merchant sites) | `ssl_sites` | 1 d | Yes |
| SSL renewal (CloudCart domain) | `ssl_cloudcart` | 1 d | Yes |
| SSL renewal (CC link) | `ssl_cclink` | 1 d | Yes |
| Order fulfillment statistics | `statistics_orders_fulfillment` | 1 d | Yes |
| Order payment statistics | `statistics_orders_payments` | 1 d | Yes |
| Industry incomes statistics | `sites_incomes_by_payment_type_and_industry_statistic` | on-demand | Yes |
| Industry sites statistics | `sites_per_industries_statistic` | on-demand | Yes |
| Marketing dashboard refresh | `marketing_dashboard` / `marketing_dashboard_execute` | 6 h | Yes / no |
| Currency exchange-rate sync | `currency_sync` | 12 h | Yes |
| Primary domain handling | `handle_primary_domains` | 1 d | Yes |
| Long-process watchdog | `kill_long_process` | 2 min | Yes |
| Modoboa mailbox reconciliation | `sync_modoboa` | 1 d | Yes |
| Worker health probe | `ping_workers` | 2 min | Yes |
| Product "New" badge removal | `product_change_new_Status` | 4 h | No |
| Product "Featured" badge removal | `product_change_featured_Status` | 4 h | No |
| Product primary image update | `product_primary_image_update` | 1 h | Yes |
| Permanent product deletion (full) | `delete_temporary_product_full` | 12 h | Yes |
| Permanent product deletion (per-product) | `delete_temporary_product` / `delete_temporary_product_execute` | on-demand | No |
| Daily CSV staging cleanup | `delete_csv_tables` | 1 d | Yes |
| Failed-import record cleanup | `remove_global_import_records_failed` | 1 d | Yes |
| Pending events approval | `send_pending_events_for_approval` | 1 d | Yes |
| Admin-panel notification | `admin_notify` | on-demand | No |
| CSV product import | `products_import_csv` / `products_import` | on-demand | No |
| CSV customer import | `customers_import_csv` / `customers_import` | on-demand | No |
| CSV blog import | `blog_import_csv` / `blog_import` | on-demand | No |
| CSV URL-redirect import | `redirects_import` | on-demand | No |
| ERP import (XML / JSON) | `erp_imports` / `erp_imports_execute` | on-demand | No |
| Missing-product disable (ERP) | `disable_missing_products` | on-demand | No |
| Product image fetched from remote URL | `image_from_url` | on-demand | No |
| Text-overlay placeholder image | `text_image_from_url` | on-demand | No |
| Auto-generated variant images | `product_variants_images` | on-demand | No |
| Product image colour detection | `product_image_color` | on-demand | No |
| Discount usage sync (per order) | `order_discount_usage_sync` | on-demand | No |
| Outbound webhook delivery (per order) | `order_hooks_send` | on-demand | No |
| Async report export (CSV / XLSX / PDF) | `download_aggregate` / `generate_by_sql` | on-demand | No |
| Generic per-site statistic record | `statistic` | on-demand | No |
| Transactional email send | `email` | on-demand | No |
| Site provisioning | `install_site` | on-demand | Yes |

### the search index sync queue identifiers

The search-index sync chain uses dedicated queue names rather than per-process identifiers — see [[background-queue-search-sync]] for behaviour:

- `searchable-import4` — per-product re-index on writes.
- `searchable-import8` — nightly price re-sync + manual full re-index.
- `cc-system7` — nightly orphan cleanup.

### How the Assistant uses this

For a stuck or failed process: map the human-facing name (left column) → internal identifier (middle column) → query the queue-inspection tool, read the last-run timestamp + status, and reply using **only the human name**. The identifier never appears in the merchant answer.

Example: *"my abandoned cart emails aren't sending"* → "Abandoned cart recovery emails" → `abandoned_all_cart_email` → tool shows last run + status → reply: *"The Abandoned cart recovery emails process last ran at 14:32 and completed successfully. The 3-minute schedule should send your next batch within minutes."*

## Related

- [[background-queue-inventory]] — hub.
- [[settings-queue-view]] — merchant-facing surface that uses human names.
- [[background-queue-recurring-platform]] — recurring jobs grouped by domain.
- [[background-queue-imports-exports]] — on-demand import / export / image processes.
- [[background-queue-order-side-effects]] — order-driven async + campaign delivery.
- [[background-queue-search-sync]] — search-index queue identifiers.
- [[background-queue-view-and-stuck]] — Queue View visibility rules per process.

## Open Questions

- Currency-exchange-rate sync visibility is currently flagged Yes on Queue View despite the 12-hour cadence putting it in the platform-housekeeping group — confirm whether merchant-visible by design or legacy (verify).
- `kill_long_process` per-process budget is not documented in the catalogue — the watchdog clearly has one but the threshold per process is not exposed (verify).
