---
type: feature
nav_path: "Marketing → Campaigns → Statistics → Log → Status archive"
route_name: admin.api.campaigns.statistics.logs
route_path: /admin/api/core/marketing/campaigns/{campaign}/statistics/{action}/logs
aliases: ["status_archive", "Status transition timeline", "Status history tooltip", "Late-Sent idempotency", "PENDING → SENT → DELIVERED → SEEN → CLICKED"]
tags: [marketing, campaigns, statistics, logs, history]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-statistics-log]]. See the hub for the other aspects (surfaces, status values, filters & table, view-message, side-effects, Email mapping, storage).

# Per-send log — status archive (transition timeline)

## Purpose

Each log row preserves not just its **current** status but the **full transition history** — every state it has been in, when, and what status preceded it. This is the merchant's audit trail for understanding the delivery lifecycle of a single send: was the email opened? When? How long after delivery? Did the recipient click? The history is surfaced as a hover-tooltip on the status pill in the table, so the merchant sees the timeline without leaving the log view. This page documents the archive format, the model hook that maintains it, and the idempotency rule that protects against out-of-order webhooks.

## Where to find it

The archive is surfaced as a **hover-tooltip on the status pill** in the log table. The merchant doesn't navigate to a separate page — they hover any pill in the Status column on the [[campaigns-statistics-log-filters-table|log table]] and the full transition timeline appears as a tooltip.

## What the merchant can do here

- **Hover any row's status pill** to read the full SENT → DELIVERED → SEEN → CLICKED timeline with timestamps.
- **Identify the time gap** between each transition (delivery → open → click) to gauge engagement speed.
- **Spot the absence** of expected transitions (a row stuck at SENT without DELIVERED → the provider hand-off failed silently).
- **Sort the table by `updated_at`** to surface rows with the most-recent archive entries first — useful when investigating a current incident.

## Settings & fields

Each log row keeps a `status_archive` array. Every time the status changes, the platform appends an entry with the new status, the previous status (as `original`), and a UTC timestamp:

```
[
  { status: "SENT", date: "2026-05-20T10:00:00Z", original: null },
  { status: "DELIVERED", date: "2026-05-20T10:00:08Z", original: "SENT" },
  { status: "SEEN", date: "2026-05-20T11:42:30Z", original: "DELIVERED" },
  { status: "CLICKED", date: "2026-05-20T11:43:00Z", original: "SEEN" },
]
```

Each archive entry carries:

- `status` — the NEW status being recorded.
- `original` — the OLD status that was replaced (null on the first entry, since there's no prior status).
- `date` — UTC timestamp of the transition.

The `updated_at` column on the parent row mirrors the timestamp of the **most recent** archive entry — so sorting the log table by `updated_at` desc surfaces rows with recent state changes (newly bounced, newly clicked, etc.).

## Business rules

- **Status archive auto-builds on every status update.** Each time a log row is updated AND `status` changes, the model boot hook captures the OLD status, the NEW status, and a UTCDateTime timestamp, then appends the entry. There's no manual append API — every status change goes through this hook. (verify the hook still fires on bulk updates as well as single updates.)
- **Entries are append-only.** The platform never removes or rewrites archive entries. So a row with 5 status transitions has exactly 5 archive entries, in chronological order. Even if the merchant were to manually re-trigger a delivery confirmation, a new entry is appended — the history isn't rewritten.
- **`original` preserves transition direction.** Because each entry includes the previous status, the merchant can see "PENDING → SENT → DELIVERED → SEEN → CLICKED" as 5 explicit transitions, not just a list of states. This is critical for debugging — a row that went DELIVERED → BOUNCED is a different story from one that went DELIVERED → SEEN → BOUNCED (which would suggest the customer received it, opened it, then their mailbox bounced subsequent mail).
- **Status webhook is idempotent against late Sent confirmations.** If a webhook arrives with `status='Sent'` but the log row is already in `CLICKED` or `SEEN`, the platform **skips the update** — the early-exit short-circuit prevents the row from being downgraded. Provider webhooks can arrive out of order (a "Sent" confirmation can arrive AFTER an "Opened" confirmation due to provider queuing), so without this protection the row could regress from SEEN to SENT and lose the engagement signal.
- **No similar idempotency for OTHER downgrades.** The "skip stale Sent" rule is specifically for the `SENT` provider status. Other downgrades (e.g., a DELIVERED-then-BOUNCED sequence) are recorded normally — they're not stale-webhook artefacts, they're real subsequent state changes.
- **Hover tooltip shows the full timeline.** In the log table, hovering the status pill renders the archive as a vertical timeline: each entry shows the status name + the timestamp + the time delta from the previous entry. The merchant sees at a glance whether the recipient opened the email 10 seconds after delivery (engaged) or 3 days later (passive).
- **PURCHASE is appended after CLICKED.** When a tracked click leads to an order attributed to the campaign, a PURCHASE entry is appended to the archive of the originating log row. So the row's current status becomes PURCHASE while the archive preserves the full SENT → DELIVERED → SEEN → CLICKED → PURCHASE chain. See [[campaigns-statistics-log-status-values]] for the synthetic PURCHASE state.

## How it works

The model has a `saving` (or equivalent boot) hook that runs before every write. The hook checks whether `status` is in the dirty set; if so, it captures `getOriginal('status')` as the OLD value, the new value, and a UTC date, and pushes the entry into `status_archive`. The append happens atomically with the status update — both fields persist in the same write.

Webhooks from Elastic Email (Email), MsgHub / NTH (SMS), Viber, and Web Push providers each call into their channel-specific status-mapping function (see [[campaigns-statistics-log-email-mapping]] for the Email mapping table), which returns one of the canonical platform statuses. The mapping result is then assigned to the log row's `status` — and the boot hook handles the archive append automatically.

The late-Sent idempotency check happens in the webhook handler, BEFORE the status assignment: if the canonical mapped status is `SENT` AND the row's current status is already `CLICKED` / `SEEN` / `PURCHASE` / similar engagement-positive state, the handler returns early (an `EXECUTE_DESTROY` signal in legacy Smarty paths, or an equivalent short-circuit in the modern handler) and no write happens — the row's status and archive are untouched.

## Related

- [[marketing-campaigns-statistics-log]] — hub.
- [[campaigns-statistics-log-status-values]] — the 20 status values that can appear in the archive.
- [[campaigns-statistics-log-email-mapping]] — provider-status → canonical-status mapping that feeds the archive.
- [[campaigns-statistics-log-side-effects]] — what triggers when a NEW archive entry has certain statuses (auto-bounce / auto-verify).
- [[campaigns-statistics-log-filters-table]] — `updated_at` column sorted desc by default; mirrors the latest archive entry.

## Open questions

- Confirm the archive append fires reliably on bulk update paths (not just single-row updates).
- Confirm the late-Sent idempotency covers all "engagement-positive" states (PURCHASE included) or only CLICKED / SEEN.
