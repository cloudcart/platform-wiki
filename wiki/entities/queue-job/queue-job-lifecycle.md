---
type: entity
aliases: ["Queue job lifecycle", "Job phases", "Enqueued reserved running completed failed stuck", "Job state machine", "Job phase transitions"]
tags: [settings, ops, jobs, queue, background, lifecycle, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[queue-job]]. See the hub for related aspects (persistent storage, populate-poller, families, priority tiers, visibility).

# Queue Job — lifecycle (7 phases)

## Identity

A Queue Job moves through up to **7 phases** between the moment its mapping is registered and the moment its row leaves the background-job store (or settles into a stable recurring rhythm). The phases are: **Mapped → Enqueued → Reserved → Running → Completed**, with **Failed** and **Stuck** as off-the-happy-path branches. This page documents what each phase means, which columns on the row change, and how the merchant sees the state on [[settings-queue-view]].

The lifecycle is the same for both **recurring** jobs (driven by the populate-poller — see [[queue-job-populate-poller]]) and **one-shot** jobs (dispatched directly by a domain-event subscriber or an admin action). The only difference is the path out of Completed: recurring jobs cycle back to Enqueued at the next poll; one-shot rows are deleted.

## Aliases

- **Job phases** / **Phase transitions** — generic terms.
- **Enqueued / Reserved / Running / Completed / Failed / Stuck** — the canonical phase names.
- **Job state machine** — engineering shorthand.

## Key Attributes

The columns on a background-job row that move between phases (see [[queue-job-storage]] for the row layout):

| Column | Mapped | Enqueued | Reserved | Running | Completed | Failed | Stuck |
|--------|--------|----------|----------|---------|-----------|--------|-------|
| `available` | n/a | true | false | false | true (or row deleted) | true | false |
| `reserved_at` | — | null | set | set | null | null | set, expired |
| `attempts` | — | 0 | +1 | +1 | unchanged | +1 | +1 |
| `completed_at` | — | null | null | null | set | unchanged | unchanged |
| `error` | — | null | null | null | cleared | set | unchanged |
| `is_running` (derived) | — | false | true | true | false | false | true (until window expires) |

## Where it appears

- [[settings-queue-view]] — surface where each row's phase is visible (via *Is running*, *Last run*, *Next run*, and the error tooltip).
- [[settings-import-history]] — phase rendered as a status badge per import.
- [[settings-hooks]] — webhook-delivery rows go through the same lifecycle.

## The 7 phases in detail

**1. Mapped.** At deploy time, the recurring job is registered in the mapping registry with its job type, queue family, interval, `single` / `visible` flags. No background-job row exists yet. This phase is purely a platform-level configuration; merchants cannot add mappings.

**2. Enqueued.** At runtime, either (a) the populate-poller (recurring) or (b) a domain Event subscriber (event-driven) or (c) a manual admin action (one-shot) creates a background-job row with `available = true`, `reserved_at = null`, `next_execution_at` set. The merchant sees the row appear on [[settings-queue-view]] with *Is running = no* and a *Next run* timestamp.

**3. Reserved.** A worker on the matching queue family picks the row off the queue, sets `reserved_at`, increments `attempts`, and marks `available = false`. The row now appears as *Is running = yes* to the Queue View (derived from the reservation window — see [[queue-job-storage]]).

**4. Running.** The job executes the work. For periodic jobs this might take milliseconds; for heavy jobs (XML feed regeneration, CSV import of 50 000 products, marketing-dashboard collector chain) it can take minutes. The row stays Reserved on the row-level columns during this whole phase.

**5. Completed.** On success, the `completed_at` timestamp is written, `is_running` is derived as `false`, the error column is cleared, and (for recurring jobs) the *Next run* timestamp is set to the completion time plus the interval — the row is ready for the next populate-poller cycle. For **one-shot** jobs, the row is removed entirely from the background-job store.

**6. Failed.** On exception, the error column is populated with the failure details, the attempts counter is incremented, `is_running` flips to false. For recurring jobs, the next populate-poll cycle re-enqueues the row after `interval` elapses. For one-shot jobs, the row stays in Failed indefinitely — the merchant can retry from the originating screen, but the failed row remains until support cleans it up. See [[queue-job-visibility-and-errors]] for the error-preservation rules.

**7. Stuck.** If a worker crashes silently mid-execution, the row stays in the Reserved phase forever — `reserved_at` is set, but no `completed_at` will arrive. After the queue's `retry_after` window (~10 minutes — see [[queue-job-storage]]), the row becomes available again, and the next polling worker picks it up. Until then, [[settings-queue-view]] shows it as *Is running = yes*. Support intervention can manually mark it failed.

## Recurring vs one-shot job paths

| Aspect | Recurring | One-shot |
|--------|-----------|----------|
| **Enqueued by** | populate-poller cycle (see [[queue-job-populate-poller]]) | Domain-event subscriber or manual admin action |
| **Has `interval`** | Yes (seconds) | No (`null`) |
| **After Completed** | Row stays, `next_execution_at` is set to the completion time plus the interval for the next cycle. | Row is deleted. |
| **After Failed** | Row stays with error column populated; re-enqueued on the next cycle. | Row stays with error; never auto-retried (merchant must re-trigger from the originating screen). |
| **Visible on Queue View** | Yes (if `visible = true`) | Usually yes during running; some hidden by `visible = false`. |

## Phase-to-merchant-visible-state cheat sheet

| Phase | Queue View — *Is running* | Queue View — *Last run* | Queue View — *Next run* | Error tooltip |
|-------|--------------------------|-------------------------|-------------------------|---------------|
| Enqueued | no | last `completed_at` (or empty) | upcoming timestamp | — |
| Reserved / Running | yes | last `completed_at` (or empty) | upcoming timestamp | — |
| Completed (recurring) | no | just now | completion time + interval | — |
| Failed | no | last successful `completed_at` (NOT this attempt) | upcoming timestamp | yes |
| Stuck | yes (until `retry_after` expires) | last `completed_at` | unchanged | maybe (if previous attempt failed) |

A merchant asking *"why does Queue View show this job running for an hour?"* is almost always seeing a Stuck row — the answer is to wait for the `retry_after` window or ask support to release the lock. See [[queue-job-storage]] for the window mechanics.

## Related

- [[queue-job]] — hub.
- [[queue-job-storage]] — the row columns that change per phase + `retry_after` window.
- [[queue-job-populate-poller]] — Enqueued phase for recurring jobs.
- [[queue-job-visibility-and-errors]] — `visible` flag (whether phase is shown) + error preservation.
- [[settings-queue-view]] — the surface that visualises the phase.
- [[settings-import-history]] — per-import phase rendering.

## Open Questions

None.
