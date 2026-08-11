---
type: feature
nav_path: "Settings → Queue → Queue families & workers"
route_name: queue.settings
route_path: /admin/settings/queue-view
aliases: ["Queue families", "Worker groups", "Numeric suffix routing", "Plan tier priority queue", "Heartbeats"]
tags: [settings, queue, workers, infrastructure, plan-tier]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-queue-view]]. See the hub for the other aspects (page UI, actions, visibility, running-detection, recurring jobs, event subscribers).

# Queue — families, worker groups, and plan-tier routing

## Purpose

Map the platform's queue layer: the 22 worker daemon groups, which queue families each one listens on, the **numeric-suffix routing rule** that makes higher plan tiers process work faster, and the UptimeRobot heartbeat URLs the platform uses to detect a worker family going down.

This is the architectural backdrop for the visible rows on [[settings-queue-view-page]] — the merchant doesn't configure this, but knowing the routing answers *"why did the merchant on Plan X get their import done before the merchant on Plan Y?"*.

## Where to find it

Sidebar → Settings → **Queue**. Route `/admin/settings/queue-view`. The merchant doesn't see worker / family info directly on the page — this aspect documents the layer underneath.

## What the merchant can do here

Nothing — this is infrastructure. The merchant's plan tier (chosen on [[account-plan]]) determines the routing automatically.

## Settings & fields

### Worker daemon groups → queue families

CloudCart's queue layer is processed by 22 worker daemon groups. Each daemon listens on the family of queues matching its name (verify):

| Worker group | Listens on queues | Job category |
|---|---|---|
| `worker` | `default`, `email` | Standard misc jobs + transactional emails |
| `worker-analytics` | `analytics`, `analytics2` | Per-order denormalisation + per-day aggregations |
| `worker-product-images` | `product-images`, `product-images3`, `product-images9` | Image-from-URL download, variant images, primary-image update, image-color extraction |
| `worker-import` | `import`, `import2` … `import10` | CSV / ERP / JSON / supplier / blog / redirects imports |
| `worker-system` | `system`, `system1` … `system9` | Per-site housekeeping (cart cleanup, statistics, admin notify, product-status sweeps) |
| `worker-install` | `install` | Site provisioning (DB seed, translations install, default templates) |
| `worker-cc-system` | `cc-system`, `cc-system7`, `cc-system8` | Platform-wide single jobs (currency sync, subscription billing, SSL renewal, settlement) |
| `worker-order-events` | `order-events`, `order-events6`, `order-events8`, `order-events9` | Order-event side effects (webhook deliveries, discount-usage sync, customer notifications) |
| `worker-export` | `export`, `export6`, `export9` | Customer / order / product exports (`download_aggregate`, `generate_by_sql`, ERP exports) |
| `worker-segments` | `segments`, `segments9` | RFM + customer-segment aggregation jobs |
| `worker-subscribers` | `subscribers`, `subscribers9` | Newsletter subscriber import + segment assignment |
| `worker-campaigns` | `campaigns`, `campaigns9` | Marketing campaign workflow |
| `worker-campaigns-messages` | `campaigns-messages`, `campaigns-messages4`, `campaigns-messages9` | Per-recipient campaign delivery (email / SMS / Viber send) |
| `worker-campaigns-hooks` | `campaigns-hooks` | Per-campaign HTML→inline-CSS hook jobs |
| `worker-campaigns-process` | `campaigns-process` | Browser-fingerprinting datalayer jobs |
| `worker-translate` | `translate` | Cloudio multi-language translate jobs |
| `worker-tmp` | `tmp` | Short-lived temp jobs |
| `worker-cloudio` | `cloudio` | Cloudio AI generation (descriptions, meta, shopperpen) |
| `worker-the search engine` | `the search engine` | the search engine search-index rebuild |
| `worker-the search engine-import` | `the search engine-import` | Bulk the search engine import + embedding queue |

### Numeric-suffix routing → plan tier priority

When a job is dispatched the platform reads a `<feature>-priority` plan-feature value (1-9) and routes onto `<family><suffix>` accordingly. Higher-suffix queues are processed by workers with higher priority.

Examples:

- A merchant on the highest plan tier dispatching a CSV import lands on `import10`; a merchant on a lower tier lands on `import6` or `import2`.
- The same pattern applies to `export6` vs `export9`, `system3` vs `system9`, `campaigns-messages4` vs `campaigns-messages9`, etc.

Practical implication: **merchants on a higher plan tier see their imports / exports / segments / campaigns start running sooner than merchants on a lower tier**, even if both queued at the same moment. This is invisible to the merchant (the Queue page does not show the suffix directly) but it's the architectural reason "priority queue" is a tier feature.

The merchant can infer relative priority from how quickly comparable jobs leave the Running state across stores — but the page itself never labels priority.

### UptimeRobot heartbeats — per family

Each major queue family has a configured UptimeRobot heartbeat URL (verify). The platform pings the URL after every successful job; UptimeRobot raises an alert if no ping arrives within the expected window.

Families with heartbeats:

- `cc-system`
- `install`
- `email`
- `export9`
- `import10`
- `order-events9`
- `product-images9`
- `system9`
- `campaigns9`
- `campaigns-messages9`
- `campaigns-hooks9`
- `campaigns-process9`

Families without heartbeats: `segments9`, `subscribers9`, `translate9`.

This is invisible to the merchant — if `import10` workers go down, an internal CloudCart engineer is paged; the merchant only sees the symptom (import never runs) and would file a support ticket.

## Business rules

### Why a higher tier's job starts sooner

Each worker daemon is configured to prioritise the higher-suffix queues in its family. A worker for the `import` family that polls `import10` before `import6` before `import2` will pick up a higher-tier merchant's job before a lower-tier merchant's even if both arrived at the same moment.

The merchant page on [[settings-queue-view-page]] does not surface this — see also [[settings-queue-view-running-detection]] for what `Running` means.

### Heartbeat alerts are platform-internal — not a merchant signal

If a queue family's heartbeat goes silent, UptimeRobot pages CloudCart engineering. The merchant has no visibility into the heartbeat state; they only experience the symptom (delayed or non-running jobs). Support tickets that match the symptom are the merchant's path.

### The queue backend affects retry behaviour

The `retry_after` setting on the queue connection determines when a reserved-but-unreleased row becomes available again. See [[settings-queue-view-running-detection]] for the ~10-minute window and the `kill_long_process` watchdog interaction.

## Related

- [[settings-queue-view]] — hub.
- [[settings-queue-view-recurring-jobs]] — which mappings route into which family.
- [[settings-queue-view-running-detection]] — `retry_after` + watchdog mechanics on the platform queue.
- [[settings-queue-view-event-subscribers]] — `order-events` family is where webhook deliveries live.
- [[account-plan]] — plan tier that decides the numeric-suffix routing.

## Open questions

None.
