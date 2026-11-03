---
type: entity
aliases: ["Queue families", "Queue names", "Worker groups", "system queue", "import queue", "order-events queue", "analytics queue", "campaigns queue", "Per-site vs platform-wide"]
tags: [settings, ops, jobs, queue, background, families, workers, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[queue-job]]. See the hub for related aspects (persistent storage, populate-poller, lifecycle, priority tiers, visibility).

# Queue Job — families and worker groups

## Identity

CloudCart organises background jobs into **queue families** — each family is a set of numerically-suffixed queue names (`<name>`, `<name>1`, … `<name>9`, occasionally `<name>10`) processed by one dedicated **worker group**. Splitting jobs across families means a heavy CSV import doesn't block transactional emails, a stuck webhook delivery doesn't block currency-rate refreshes, and the analytics denormalisation pipeline doesn't slow down marketing-campaign sends.

The numeric suffix encodes plan-tier priority (so a merchant on a higher plan lands on `import9` instead of `import2`) — see [[queue-job-priority-tiers]].

Each family also has a per-family **populate-poller** that drives its recurring schedule — see [[queue-job-populate-poller]].

## Aliases

- **Queue families** — generic catalogue term.
- **Worker groups** — the daemon-side label (`worker`, `worker-import`, `worker-system`, etc.).
- **Per-site vs platform-wide jobs** — orthogonal scope dimension applied across families.
- **Family + suffix** — e.g., `system7` means family `system` at priority tier 7.

## Key Attributes

| Attribute | Notes |
|-----------|-------|
| **Family name** | The prefix (e.g., `system`, `import`, `order-events`). Same prefix across all numeric suffixes. |
| **Worker group** | The daemon that listens on the whole family (e.g., `worker-import` listens on `import`, `import2`, …, `import10`). |
| **Suffix range** | Usually `<name>`, `<name>1`, …, `<name>9`. Some go to 10. The base (no suffix) is the lowest-priority tier; `9` (or `10`) is the highest. |
| **Per-site vs platform-wide** | Per-site jobs reference `site_id`; platform-wide single jobs leave it null. |
| **Heartbeat** | Each family has an uptime monitoring heartbeat; if pings stop, on-call engineering is paged — see [[queue-job-visibility-and-errors]]. |

## Where it appears

- [[settings-queue-view]] — each visible job row shows its queue name (e.g., `system7`).
- [[settings-import-history]] — imports run on the `import` family.
- [[settings-hooks]] — webhook deliveries run on the `order-events` family.
- [[apps-csv-import]] / [[apps-xml-feed-generator]] / [[apps-xml-import-settings]] — origin pages whose jobs land on specific families.
- [[customers-export]] / [[orders-export]] — origin pages for `export` family jobs.

## The full family catalogue

Each family covers a coherent category of work and is processed by exactly one worker group:

| Family | Job category | Worker group |
|--------|--------------|--------------|
| `default` | Standard misc per-site jobs (statistics, mailables) | `worker` |
| `email` | Outbound transactional emails | `worker` |
| `system` / `system1` … `system9` | Per-site housekeeping (delete cart safe, statistic, abandoned-cart sweep, admin notify, product change new/featured) | `worker-system` |
| `cc-system` / `cc-system7` / `cc-system8` | Platform-wide single jobs (currency sync, subscription payments, SSL renewal, expire subscriptions, settlement batch, reseller payouts, kill long process, handle primary domains, modoboa sync) | `worker-cc-system` |
| `import` / `import2` … `import10` | Imports (ERP, products CSV, customers CSV, blog CSV, redirects, JSON, supplier) | `worker-import` |
| `order-events` / `order-events6` / `order-events8` / `order-events9` | Order-event side effects (discount-usage sync, webhook deliveries, customer notifications) | `worker-order-events` |
| `analytics` / `analytics2` | Per-order denormalisation + per-day aggregations (sales, sessions, traffic, top products / vendors / categories, conversion rates, abandoned checkouts) | `worker-analytics` |
| `product-images` / `product-images3` / `product-images9` | Image processing (image-from-url download + S3 upload, variant images, primary-image update, image color extraction) | `worker-product-images` |
| `install` | Site provisioning (DB seed, translations install, default templates) | `worker-install` |
| `export` / `export6` / `export9` | Customer / order / product exports + ERP exports | `worker-export` |
| `segments` / `segments9` | RFM + customer-segment aggregation, site-level segments | `worker-segments` |
| `subscribers` / `subscribers9` | Newsletter subscriber import + segment assignment | `worker-subscribers` |
| `campaigns` / `campaigns9` | Marketing campaign workflow (the population poller dispatching per-target jobs) | `worker-campaigns` |
| `campaigns-messages` / `campaigns-messages4` / `campaigns-messages9` | Per-recipient campaign delivery jobs (email / SMS / Viber send) | `worker-campaigns-messages` |
| `campaigns-hooks` | Per-campaign HTML→inline-CSS hook jobs | `worker-campaigns-hooks` |
| `campaigns-process` | Browser-fingerprinting datalayer jobs (one per unique user-agent per week) | `worker-campaigns-process` |
| `translate` | Cloudio multi-language translate jobs (auto-translate of products / categories on language enable) | `worker-translate` |
| `tmp` | Short-lived temporary jobs (file cleanup, S3 migrations of temp data) | `worker-tmp` |
| `cloudio` | Cloudio AI generation (product descriptions / meta / short descriptions, category descriptions, shopperpen analyze) | `worker-cloudio` |
| `the search engine` / `the search engine-import` | the search engine search-index rebuild + bulk import, embedding queue | `worker-the search engine` / `worker-the search engine-import` |

The `___` and bare `worker` group labels are reserved sentinels in the worker config; they are not user-facing queue names. `(verify)` for any newly-added family.

## Per-site vs platform-wide scope

Orthogonal to the family axis, every job has a scope:

- **Per-site** (`site_id` non-null): runs once per store. CSV imports, customer exports, abandoned-cart sweeps, search-index rebuilds, marketing-dashboard collectors, segment aggregations, webhook deliveries, status-change notifications, fulfillment notifications.
- **Platform-wide** (`site_id` null + `single = true`): runs once across the whole platform. Currency rates, subscription billing, SSL renewal, modoboa sync, kill-long-process, populate-pollers themselves. See [[queue-job-visibility-and-errors]] for the single-lock rules.

The Queue page on [[settings-queue-view]] is permissive enough to show platform-wide single jobs too — so the merchant sees `currency_sync` once every 12 h even though it's not specifically running for their store.

## Choosing the right family (engineering rule of thumb)

The placement of a job on a family is a deploy-time decision baked into the mapping registry. The rule of thumb:

- **Transactional + fast** → `default` or `email`.
- **Per-store housekeeping** → `system`.
- **Cross-store / single-lock platform chores** → `cc-system`.
- **Bulk file processing** → `import` or `export`.
- **Order-driven side effects (webhooks, notifications)** → `order-events`.
- **Analytics aggregation** → `analytics`.
- **Marketing-campaign sends** → `campaigns-messages` (per-recipient) preceded by `campaigns` (orchestration).
- **Search indexing** → `the search engine` / `the search engine-import`.
- **AI / Cloudio generation** → `cloudio`.

This is not configurable by the merchant — but support engineers ticketed to investigate a stuck queue will use the family name to scope which worker group to inspect.

## Related

- [[queue-job]] — hub.
- [[queue-job-priority-tiers]] — what the numeric suffix means (plan-tier routing).
- [[queue-job-populate-poller]] — one poller per family.
- [[queue-job-visibility-and-errors]] — uptime monitoring is per family; single-lock applies on `cc-system` family jobs.
- [[queue-job-lifecycle]] — phases run identically across families.
- [[settings-queue-view]] — shows the queue name on every row.
- [[settings-hooks]] — webhook deliveries on `order-events`.
- [[apps-csv-import]] — imports on the `import` family.

## Open Questions

None.
