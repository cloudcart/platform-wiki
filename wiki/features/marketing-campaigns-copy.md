---
type: feature
nav_path: "Marketing → Campaigns → Copy"
route_name: admin.api.campaigns.copy
route_path: /admin/api/core/marketing/campaigns/copy/{id}
aliases: ["Copy campaign", "Duplicate campaign", "Clone campaign", "Replicate campaign", "Дублирай кампания", "Копирай кампания"]
tags: [marketing, campaigns, copy, duplicate]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-05-23
updated: 2026-06-10
source_count: 2
---
# Copy campaign

## Purpose

The **Copy campaign** action is the merchant's fastest way to spin up a new campaign that's "the same as that one, but for a different segment / occasion / month". Clicking Copy on any campaign row clones the campaign's settings, every step, every message template, the exit tag, the exit purpose — everything — into a fresh Draft campaign with a *" - Copy"* suffix on the title. The merchant lands on the editor with everything pre-filled and can tweak whichever fields they want before launching.

This is a **one-click action** — no modal asking for a new title, no per-field "copy / don't copy" picker. It's a full replica that the merchant then customises in the editor. The cloned campaign always starts in **Draft** state regardless of the source's state (Active / Inactive / Archived / Draft), and the source campaign is **never modified** (Copy is non-destructive).

## Where to find it

Sidebar → **Marketing** → **Campaigns** → on any non-archived tab (Active / Inactive / Draft) → click the **Copy** action in any row's action column. The icon is a stack-of-papers in a small round button with a *"Copy campaign"* hover tooltip.

Copy is not a page — it's a one-click row action wired to an API mutation:

| Endpoint | Method | Route path |
|----------|--------|------------|
| `admin.api.campaigns.copy` | GET | `/admin/api/core/marketing/campaigns/copy/{id}` |

(A legacy sitecp route `campaigns.copy` at `/admin/campaigns/copy/{campaign_id}` does a 302 redirect to the legacy editor — but the modern admin uses the API mutation above.)

## What the merchant can do here

Because the whole topic exceeds one concept's worth of detail, it is split into three aspect pages. The Assistant should drill into the aspect that matches the question, not read all three.

At a glance, clicking Copy:

1. Clones the source campaign + all its steps + all its message templates inside a single DB transaction.
2. Toasts *"Campaign copied successfully."* and opens [[marketing-campaigns-edit]] for the new Draft.
3. Leaves the source campaign untouched.

The merchant then renames the copy, optionally swaps the trigger segment, edits step delays / messages, sets a new start time, and clicks **Start campaign**.

## Sub-pages (in this cluster)

- [[campaigns-copy-action-flow]] — the one-click mechanics: the Copy endpoint, the click sequence + loading state, the `?edit=1` editor-unlock trick, why there's no confirmation modal and no "copy options" picker.
- [[campaigns-copy-what-transfers]] — the field-by-field "what gets copied vs what's reset" table; the *" - Copy"* title suffix and its stacking; `start_at` exclusion; message-design snapshots; saved-template linkage; shared tags / segment.
- [[campaigns-copy-state-and-quota]] — the always-Draft result; plan-tier campaign-quota consumption; soft-deleted source 404; broken-source tolerance; anti-spam gate; the silent `dynamic_tags` reset on next save.

## Settings & fields

The Copy action itself exposes **no fields** — it takes only the source campaign's `id` from the row and produces a clone. Every configurable field lives on the destination editor ([[marketing-campaigns-edit]]) that opens after the clone. For the exact list of which fields carry over (`type`, `title`, `description`, `trigger_condition`, `trigger_segment`, `customers_tags`, `purpose`, `repeat`, `use_exists_subscribers`, `dynamic_tags`, all actions, all action templates) and which are reset (`active`, `archived_at`, `progress`, `start_at`, timestamps, `id`, enrolled subscribers, statistics), see [[campaigns-copy-what-transfers]].

## Business rules

The cluster's business rules are documented per aspect:

- Copy always produces a **Draft** regardless of source state; it consumes one campaign slot against the plan quota; soft-deleted sources return 404 — see [[campaigns-copy-state-and-quota]].
- The clone runs as one **all-or-nothing DB transaction**; templates are re-linked to the new actions after save — see [[campaigns-copy-action-flow]].
- Title-collision (*"Campaign with this title already exists"*) is detected only on the next **Save**, not at Copy time; the *" - Copy"* suffix stacks unconditionally — see [[campaigns-copy-what-transfers]].

## Related

- [[marketing-campaigns]] — parent hub; the Copy action sits in every row's action column.
- [[campaigns-list-row-actions]] — the row action column where Copy lives.
- [[marketing-campaigns-edit]] — destination; the editor opens for the new copy.
- [[marketing-campaigns-from-predefined]] — alternative clone path (from a curated template).
- [[marketing-campaigns-draft]] — Draft tab; new copies appear here.
- [[marketing-campaigns-message-template]] — message editor for each cloned step.
- [[marketing-segments]] — the trigger segment is shared between source and copy.
- [[marketing-subscribers]] — tags are shared between source and copy.
- [[campaign]] — Campaign entity (each campaign carries its actions / steps).

## Open questions

No outstanding questions.
