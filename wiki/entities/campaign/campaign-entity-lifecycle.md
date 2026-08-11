---
type: entity
nav_path: "Entity → Marketing Campaign → Lifecycle"
aliases: ["Campaign lifecycle", "Campaign states", "Campaign status flow", "Active campaign edit lock", "Auto-archive on completion", "Campaign archive vs delete", "Campaign copy", "Campaign banned", "Жизнен цикъл на кампания"]
tags: [entity, marketing, campaigns, lifecycle, state-machine]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[campaign]]. See the hub for the other aspects (types, attributes schema, relationships, consent gating, attribution & statistics).

# Campaign — Lifecycle

## Identity

A Campaign moves through a defined sequence of states from creation to retirement. The transitions are gated by merchant action (Save, Activate, Deactivate, Archive), platform action (auto-archive on completion, ban on policy violation), and time (scheduled send arrival, per-step delay expiry). This page documents the state machine, the transition rules, the edit-time locks, and the distinction between Archive and Delete.

## Aliases

- **Status** — the merchant-visible state label (Active / Inactive / Draft / Archived) — backed by `active` integer column + `archived_at` timestamp on the DB row.
- **Activation** = flipping the inline status toggle ON.
- **Deactivation** = flipping it OFF.
- **Archive** = soft-archive — moves off the active list, preserves all data.
- **Delete** = soft-delete (trash icon) — sets `deleted_at`; the bulk-delete action on the Archived tab is the only true delete.
- **Banned** = flagged by anti-spam moderation; cannot send until resolved.
- **Completed** = (Regular only) the one-shot dispatch finished and the platform auto-archived.

## Key Attributes

### The state sequence

| State | Description | Entry condition | Exit options |
|-------|-------------|-----------------|--------------|
| **Draft** | Created but not configured to send yet. Lives in the Draft tab. Can be saved indefinitely without sending. | Created via Create-campaign modal. | Merchant fully configures + activates → Active. |
| **Active (scheduled)** | Fully configured, segment chosen, messages written, status flipped to Active. | Regular: queued for the scheduled send time. Automated: live and listening for the trigger event. | Scheduled time arrives → Active (executing). Merchant deactivates → Inactive. |
| **Active (executing / dispatching)** | The platform is currently sending messages. Per-action counts climb on the Statistics screen. | Scheduled time arrived (Regular) OR trigger fired (Automated). | Regular: full dispatch done → Completed (auto-archives). Automated: stays Active indefinitely. Merchant deactivates → Inactive (pauses). |
| **Inactive (paused)** | The merchant flipped the inline status switch to OFF. | Merchant action. | Merchant flips back to Active → resumes. Pending Automated step-deliveries are paused; existing in-funnel subscribers stay parked. |
| **Completed** | Regular only: the one-shot send is done. Automated campaigns don't strictly "complete" while subscribers continue to enter the trigger. | Hourly aggregation detects `successfully_sent >= subscribers_to_campaign_count > 0`. | Auto-archives to Archived. |
| **Archived** | Soft-archive. Hidden from the active list (filter the Archived tab to see it). Data preserved including all log rows. | Merchant manually archives OR auto-archive on completion. | Bulk-delete from Archived tab → permanent delete. |
| **Banned** | Anti-spam moderation flagged the campaign. `banned_reason` populated. Cannot send. | Channel suspension or platform moderation. | Merchant resolves flagged issue → resume. See [[campaign-entity-consent-gating]]. |

### Edit-time locks

- A campaign cannot be edited while **Active** — the editor is read-only. To edit, the merchant must:
  1. Toggle the status to Inactive (or move to Draft).
  2. Edit the messages / segment / schedule.
  3. Toggle back to Active.
- This prevents accidental mid-flight message changes.
- Copying a campaign duplicates the campaign + all its actions + templates as a new Draft; the copy starts fresh in Draft state.

### Archive ≠ delete

- **Archiving** moves the campaign off the active list but **preserves the entity + all log rows + all statistics**. A historical campaign's per-recipient log can be referenced for years for audit / GDPR-data-export purposes.
- **Bulk-delete on the Archived tab** is the only true delete (the trash icon on individual rows is the archive action, not delete).
- **Archived campaigns do NOT count against the `campaigns` plan-feature cap** (verified) — the count that drives the cap excludes archived campaigns (only those with no archive timestamp count), so archiving frees up cap headroom immediately. To stay under cap, the merchant archives old campaigns instead of deleting them — log rows and statistics are preserved either way.

## Where it appears

- [[marketing-campaigns]] — the master list page where the merchant changes status, archives, copies, deletes.
- [[marketing-campaigns-edit]] — the editor where the lock state is visible (editor read-only while Active).
- [[campaign-entity-attributes-schema]] — for the underlying `status` / `active` / `archived_at` / `progress` columns and the dual-state nuance where a campaign can be both `active = 1` AND `archived_at IS NOT NULL`.
- [[campaign-entity-consent-gating]] — for how the **Banned** state is computed from channel suspension.

### Auto-archive on completion (Regular only — verified against backend)

When the hourly statistics aggregation runs and finds a Regular campaign where `successfully_sent >= subscribers_to_campaign_count > 0`, it marks the campaign completed — setting `progress = 'completed'` AND stamping the archive timestamp. So Regular campaigns silently move themselves to the Archived tab on hourly poll once their full dispatch is acknowledged.

The campaign's `active` column may still read `1` at this moment — so the campaign appears in **both** the Active filter (because `active = 1`) and the Archived filter (because `archived_at IS NOT NULL`). This dual-state is the common cause of "the campaign is gone from my Active tab" support questions.

**Automated campaigns NEVER auto-archive** — by design they're "always-on" listeners. The merchant manually archives when they want the automation to stop.

### Soft-delete cascade (verified against backend)

When a campaign is soft-deleted (`deleted_at` set), the deletion cascades to:

- Action rows (per-channel per-step messages)
- Action template rows
- Action log rows (per-action per-recipient log)
- Subscriber funnel rows (`subscriber_to_campaigns`)

The separately-stored per-channel delivery log rows are **NOT** auto-cleared — they stay for audit purposes, just orphaned from the deleted campaign. See [[campaign-entity-relationships]] for the relations cascaded.

### Banned campaign resolution

When `banned_reason` is populated, the editor surfaces the reason and disables the Activate toggle until the merchant resolves the underlying channel issue (e.g., spam complaint rate dropping back below threshold, sender domain reverification). The reason is computed on-the-fly from the campaign's channels — see [[campaign-entity-consent-gating]] for the full mechanic.

## Related

- [[campaign]] — hub.
- [[campaign-entity-attributes-schema]] — column-level reference for `status` / `active` / `archived_at` / `progress` / `banned_reason`.
- [[campaign-entity-types-regular-automated]] — Regular auto-archive vs Automated "always-on".
- [[campaign-entity-relationships]] — soft-delete cascade scope, `subscriber_to_campaigns` pivot.
- [[campaign-entity-consent-gating]] — how banned state is detected via channel suspension.
- [[marketing-campaigns]] — list page where the merchant operates the lifecycle (Activate / Archive / Copy / Delete buttons).
- [[marketing-campaigns-edit]] — editor where the edit-lock is enforced.
- [[marketing-campaigns-banned-info]] — the channel-level banned-reason source.

## Open Questions

- ⏸️ Whether a banned campaign that the merchant resolves and re-activates resumes from where it stopped or restarts the funnel for in-progress subscribers. `(verify)`
- ⏸️ Whether the merchant can bulk-archive multiple campaigns from the Active tab, or only one at a time. `(verify)`
