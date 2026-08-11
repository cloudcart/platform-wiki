---
type: concept
nav_path: "Concept → Background processes"
aliases: ["Background processes", "What runs automatically", "Scheduled jobs", "Async processes", "Queue inventory", "Background queue registry"]
tags: [background, async, troubleshooting, support, concepts]
plan_gates: []
created: 2026-05-28
updated: 2026-06-10
source_count: 4
---

# Background processes (what runs automatically on your site)

## Definition

CloudCart runs a set of **background processes** that work on the merchant's site without the merchant needing to click anything. Some run on a regular schedule (every few minutes, every hour, every day); others run **on-demand** whenever the merchant or a customer triggers a specific action (uploading a CSV, placing an order, fetching a product image). The merchant cannot start or stop these processes manually — they are part of the platform — but they CAN check the progress of the visible ones on [[settings-queue-view]].

This concept is the **inventory of every background process the platform runs**: what each one does in the merchant's terms, how often it runs, whether the merchant can see it on the Queue View screen, and what to do if a process appears stuck. The single most-asked support pattern — *"I updated something and the storefront still shows the old version"* — almost always resolves to **queue lag on `searchable-import4`**, the search index sync queue; see [[background-queue-search-sync]] for the full chain.

## Sub-pages (in this cluster)

This concept is split into 6 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[background-queue-recurring-platform]] — recurring scheduled processes the platform fires on its own (cart cleanup, subscription renewals, SSL renewal, statistics rollups, catalog-badge maintenance, internal housekeeping).
- [[background-queue-imports-exports]] — on-demand merchant-triggered processes: CSV / XML / JSON imports (products, customers, subscribers, blog, redirects, ERP feeds), CSV / XLSX / PDF exports, image fetch from URL, dominant-colour detection, text-overlay placeholders.
- [[background-queue-search-sync]] — the storefront read-side index sync chain (`searchable-import4`, `searchable-import8`, `cc-system7` queues). The "I changed something and the storefront still shows the old version" page.
- [[background-queue-order-side-effects]] — order-driven async fan-out: discount-usage counters, outbound webhook delivery, admin-panel notifications, marketing-campaign segment recalculation, scheduled-campaign send.
- [[background-queue-view-and-stuck]] — what shows up on [[settings-queue-view]], visibility rules per process, the 10 / 30-minute stuck-process diagnosis, automatic watchdog kill-and-retry, plan-tier priority on shared queues.
- [[background-queue-process-catalogue]] — internal-identifier reference table (merchant-facing process name → platform identifier → recurrence → single-platform-wide lock). Internal-use only; the Assistant must never paste identifiers to a merchant.

## Scope

What this concept covers (across the 6 sub-pages):

- Recurring scheduled processes (cleanup, billing, SSL, statistics, catalog badges, housekeeping).
- On-demand processes triggered by the merchant or a customer action (imports, exports, image fetching, order side-effects, campaign delivery).
- Visibility rules — which processes the merchant sees on [[settings-queue-view]] and which run silently.
- Stuck-process troubleshooting — when to worry, when not to.
- The internal-identifier catalogue used to query the platform queue-inspection tool.

Out of scope:

- The lifecycle of an individual queued job (started, running, finished, failed, retry) — see [[queue-job]].
- Synchronous in-request operations (form submission, page render, login). Those finish before the merchant sees the response and are not "background" processes.
- The Cron daemon configuration itself — that is platform-internal infrastructure.

## Contrasts

| | Background process (this concept) | Synchronous in-request operation |
|---|---|---|
| Triggered by | Schedule OR merchant / customer action | Merchant / customer click |
| Visibility | Hidden until done; merchant checks [[settings-queue-view]] for progress | Merchant sees loading spinner until response returns |
| Failure mode | Status: **Failed** in Queue View; retries on next schedule (recurring) OR stays failed (on-demand) | HTTP error response shown immediately |
| Examples | Abandoned-cart emails, daily SSL renewal, CSV import, image fetch from URL | Form submission, page render, login, search query |

A merchant's complaint *"the action didn't work"* hits this concept when the action is async (import, export, image fetch, campaign send, storefront catalogue refresh) — the action probably DID start, the merchant just doesn't see the result yet. For synchronous actions, the merchant would have seen an error response at click time.

**Recurring scheduled vs on-demand.** Recurring processes fire on a fixed cadence (every 3 minutes, every hour, every day) regardless of whether the merchant did anything. On-demand processes only fire when triggered (CSV upload, order placement, campaign send). The merchant can re-trigger an on-demand process by repeating the action; recurring processes have to wait for the next schedule.

**Visible vs hidden.** Visibility is a per-process flag — see the catalogue in [[background-queue-process-catalogue]]. Visible processes appear on [[settings-queue-view]] with title, last-run, next-run, status, and error message. Hidden processes still run; they are just platform-internal housekeeping the merchant has no actionable role in. The Assistant should not invent visibility for a process; consult the catalogue.

## Where it applies

The merchant interacts with background processes on these surfaces:

- [[settings-queue-view]] — read-only diagnostics: which visible processes ran, when they last ran, when they next run, any error message.
- [[settings-import-history]] — drill-down for the specific imports the merchant has triggered (file, mapping, outcome).
- Email and admin-notification arrival — the proof that scheduled processes have run (transactional emails, daily summaries, expiry warnings).
- The storefront itself — when an admin save reflects on the storefront, the search-index sync chain has run; see [[background-queue-search-sync]].

Most stuck-process tickets resolve with [[background-queue-view-and-stuck]] (watchdog mechanics + 10 / 30-minute thresholds) plus the specific aspect for the affected category.

## Related

- [[queue-job]] — the entity describing one queued job's lifecycle.
- [[settings-queue-view]] — the merchant's read-only diagnostics surface.
- [[settings-import-history]] — drill-down per-import row with file, mapping, and outcome.
- [[notification-delivery]] — the Event → Subscriber → Background Process pattern for outbound notifications.
- [[settings-hooks]] — webhook delivery sits on the order-events background queue; see [[background-queue-order-side-effects]].
- [[inventory-tracking]] — every stock save fires an search-index sync (see [[background-queue-search-sync]]) so stock changes appear on the storefront after the queue drains.
- [[storefront-architecture]] — the search index read-side that the sync chain feeds.
- [[order-processing-pipeline]] — order status transitions that trigger [[background-queue-order-side-effects]].

## Open Questions

- Per-process SLA targets — the merchant currently has no published expectation of "this should finish in N minutes". The order in which platform-shared queues are processed is plan-tier-first (see [[background-queue-view-and-stuck]]), but the absolute wait time depends on overall platform load. Worth capturing once a published SLA exists.
