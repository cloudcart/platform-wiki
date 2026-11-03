---
type: feature
nav_path: "Marketing → Campaigns → Copy → State & quota"
route_name: admin.api.campaigns.copy
route_path: /admin/api/core/marketing/campaigns/copy/{id}
aliases: ["Copy always Draft", "Copy campaign quota", "Copy plan limit", "Copy soft-deleted campaign", "Copy broken campaign", "Copy anti-spam gate"]
tags: [marketing, campaigns, copy, duplicate]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Copy campaign — state & quota

> Part of [[marketing-campaigns-copy]]. See the hub for the other aspects (action flow, what transfers).

## Purpose

This aspect covers the **lifecycle and access** rules around Copy: why every copy lands in Draft no matter the source state, how Copy consumes a slot against the plan-tier campaign quota, how the endpoint treats soft-deleted vs archived sources, the tolerance for broken sources, the permission / anti-spam gate, and the channel + dynamic-tag checks that are deferred to Start / Save rather than enforced at Copy time.

## Where to find it

This is the access / state behaviour of the **Copy** action — Sidebar → **Marketing** → **Campaigns** → any non-archived tab → **Copy** in a row. There is no separate screen; these rules govern whether the Copy succeeds and what state the result is in.

## What the merchant can do here

The merchant can Copy any visible (non-soft-deleted) campaign from any tab. The result is always a Draft they can review before launching. If they're at their plan's campaign quota, they must first free a slot (by permanently deleting an Archived campaign) before Copy will succeed.

## Settings & fields

There are no merchant-set fields for this aspect — the relevant values are the resulting state and the gating conditions:

| Condition | Outcome |
|-----------|---------|
| Source state (any) | Copy → `active=2` (Draft). |
| Plan campaign quota reached | Copy fails: 402 Payment Required (API) / plan-upgrade redirect (legacy sitecp). |
| Source soft-deleted (`deleted_at` set) | Copy → 404; action fails silently (error toast). |
| Source archived (`archived_at` only) | Copyable; result is a fresh Draft with `archived_at` reset to NULL. |
| Source in a broken state | Copy still completes; the merchant fixes issues in the editor. |

## Business rules

### Copy creates a Draft regardless of source state

| Source state | Copy state |
|--------------|------------|
| Active | Draft (`active=2`) |
| Inactive | Draft |
| Archived | Draft |
| Draft | Draft |

This is intentional — the merchant gets to review the clone before launching it, and the copy doesn't auto-enrol anyone. (The reset of `active`, `archived_at`, `progress`, and enrolled subscribers is detailed in [[campaigns-copy-what-transfers]].)

### Copy counts against the plan-tier campaign quota

Like every campaign-creation path, a copy consumes **one** campaign slot from the merchant's plan limit. If the merchant is at quota, the Copy action fails with a 402 Payment Required (API) or a plan-upgrade redirect (legacy sitecp). The merchant must free a slot first by **permanently deleting** an Archived campaign — Inactive / Archived campaigns still count toward the quota.

### Soft-deleted source returns 404; archived source is copyable

The Copy endpoint uses the default query, which **excludes** soft-deleted rows. So a campaign with `deleted_at` set returns 404 on Copy and the action fails silently for the merchant (error toast). **Archived** campaigns (only `archived_at` set, no `deleted_at`) ARE copyable — but the copy itself is a fresh Draft and the source's archive flag is not carried over. A campaign in the Archived tab can therefore be copied; a "deleted" campaign (which the merchant can't see anyway) cannot.

### Copy tolerates a broken source

If the source campaign is in a banned state (channel suspended, segment deleted, etc.), the Copy action still completes — the merchant gets a Draft of the broken campaign and can fix the issues in the editor before starting. **Copy does not validate the source.**

### Channels are validated only on Start, not on Copy

The Copy endpoint does **not** validate that the clone's referenced channels are configured / active. So if the source references Email but the merchant later uninstalls Email, the clone (also a Draft) won't complain until the merchant tries **Start campaign** in the editor — where the pre-flight check fires.

### Dynamic-tag support is re-checked on Save

The copied `dynamic_tags` flag (see [[campaigns-copy-what-transfers]]) is re-validated against the copied trigger segment on the **next Save**: if the segment doesn't support dynamic tags, `dynamic_tags` is force-set to 0. The full validation set is on [[marketing-campaigns-edit]].

### Anti-spam policy gate + permission

This route, like every campaign endpoint, is behind the campaign **anti-spam policy gate**, and standard campaign **permission** applies. A merchant without campaign permission, or a store failing the anti-spam policy, cannot use Copy.

## Related

- [[marketing-campaigns-copy]] — hub.
- [[marketing-campaigns-edit]] — editor where channel + dynamic-tag checks fire on Save / Start.
- [[marketing-campaigns-draft]] — Draft tab where every copy lands.
- [[marketing-campaigns]] — campaigns list / parent hub (quota, archive, delete context).
- [[campaign]] — Campaign entity.

## Open questions

No outstanding questions.
