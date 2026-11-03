---
type: feature
nav_path: "Settings → Queue → Running detection"
route_name: queue.settings
route_path: /admin/settings/queue-view
aliases: ["is_running computed", "Stuck job detection", "kill_long_process watchdog", "Retry window"]
tags: [settings, queue, diagnostics, running, watchdog]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-queue-view]]. See the hub for the other aspects (page UI, actions, visibility, recurring jobs, queue families, event subscribers).

# Queue — how `is_running` is detected and how stuck rows are freed

## Purpose

Explain how the binary **Running / Pending** badge on the Queue page is computed (it's NOT a literal "currently processing" boolean), what the 10-minute reservation retry window means, and how the platform's 2-minute watchdog `kill_long_process` reclaims rows that a crashed worker left stuck in *Running*.

This is the aspect support needs when a merchant asks: *"why has my import shown 'Running' for the last 8 minutes?"*

## Where to find it

Sidebar → Settings → **Queue**. Route `/admin/settings/queue-view`. The "Is running" column shows the derived state.

## What the merchant can do here

Nothing — the merchant observes the state and waits for the watchdog cycle. There is no manual "kill" button (see [[settings-queue-view-actions]]).

## Settings & fields

### `is_running` is computed, not stored

`is_running` is **not** a literal "this is processing right now" boolean on the row. It is derived from two columns plus a config value (verify):

```
is_running ≈ reserved_at + retry_after_seconds ≥ now AND !available
```

In words: the row was reserved for a worker within the last `retry_after_seconds` and has not yet been released back to the pool.

### The queue `retry_after` value — ~10 minutes

The queue connection's `retry_after` is configured at **610–630 seconds** on the platform (roughly 10 minutes) (verify). A job that was reserved within the last ~10 minutes and isn't yet released is considered "running".

### The stuck-row pattern

A worker that crashes silently (process killed by OOM, segfault, hard reboot of the queue host, etc.) can leave its row stuck in the *Running* state for the full retry window before it becomes available again. **This is the most common cause of the "stuck job" pattern** the merchant sees on the Queue page.

Once `reserved_at + retry_after_seconds` falls behind `now`, the row becomes available again to the next worker — at which point another worker picks it up and the badge flips from *Running* back to *Pending* (or the job retries and the cycle continues).

## Business rules

### Watchdog: `kill_long_process` every 2 minutes

A platform-wide watchdog job sweeps the queue every 2 minutes looking for worker processes that have exceeded their max execution budget and terminates them:

- **Mapping**: `kill_long_process`
- **Interval**: 120 s
- **Queue**: `cc-system7`
- **Visibility**: hidden (`is_visible = false`) — see [[settings-queue-view-visibility-rules]]
- **Single-flighted**: yes (one execution platform-wide)

### Practical reclaim window — 2 to 12 minutes

A job that crashed silently or hung indefinitely will be reclaimed within roughly **2–12 minutes**:

- ~0–2 min for the next `kill_long_process` tick.
- Up to ~10 min for the queue `retry_after` window to elapse.

The merchant sees the badge eventually flip from *Running* back to *Pending* (or the job retries). No merchant or support intervention is required for the badge to update — the platform self-heals on the watchdog cycle.

### When to flag support

Repeated stuck patterns on the **same mapping** are worth flagging to CloudCart support — the underlying cause (poison message, malformed payload, bad data, recurrent OOM in a specific code path) will not fix itself. The 2-12 min self-heal reclaims the row but doesn't prevent the next attempt from failing the same way.

Single-occurrence stuck jobs that resolve within the watchdog window are normal — see [[settings-queue-view-actions]] for the per-job-type recommended action.

### Why the badge doesn't show "Queued / waiting"

Because `is_running` is derived from the reservation state (reserved-and-not-released), the platform has no separate "queued / waiting to be picked up" state to surface. A row in that intermediate state will show as **Pending** with a `next_execution_at` in the past or near-now. The merchant infers "this should have run already" from the `Last run` and `Next run` timestamps. See [[settings-queue-view-page]] for the binary badge mechanics.

### Distinguishing the three actual states from the binary badge

| What the badge shows | What's really happening |
|---|---|
| **Running** + recent `Last run` empty | Worker is currently processing (normal). |
| **Running** + `reserved_at` more than ~10 min old | Worker crashed; row will be reclaimed by the next `kill_long_process` tick. |
| **Pending** + `Next run` in the future | Scheduled — will run at that time. |
| **Pending** + `Next run` empty + `Last run` populated | One-shot job already completed. |
| **Pending** + `Next run` in the past or null + no `Last run` | Should have run already — may be queued, may need support attention. |

The merchant infers which case applies by reading the timestamps next to the badge.

## Related

- [[settings-queue-view]] — hub.
- [[settings-queue-view-page]] — the binary badge UI itself.
- [[settings-queue-view-actions]] — what the merchant should do when a job stays Running too long.
- [[settings-queue-view-recurring-jobs]] — `kill_long_process` interval and queue.
- [[settings-queue-view-queue-families]] — the worker groups that process these jobs.

## Open questions

None.
