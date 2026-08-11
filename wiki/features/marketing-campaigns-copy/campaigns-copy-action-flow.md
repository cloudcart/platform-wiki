---
type: feature
nav_path: "Marketing → Campaigns → Copy → Action flow"
route_name: admin.api.campaigns.copy
route_path: /admin/api/core/marketing/campaigns/copy/{id}
aliases: ["Copy campaign action", "Copy campaign mechanics", "Duplicate campaign flow", "Copy button behaviour"]
tags: [marketing, campaigns, copy, duplicate]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Copy campaign — action flow

> Part of [[marketing-campaigns-copy]]. See the hub for the other aspects (what transfers, state & quota).

## Purpose

This aspect documents the **mechanics** of the Copy action — what happens between the merchant clicking the Copy icon and landing on the editor for the new Draft. It covers the endpoint call, the click / loading sequence, the absence of any confirmation modal or "copy options" picker, and the `?edit=1` query trick that unlocks the editor.

The Copy action is **non-destructive on the source** and resolves into a single navigation to [[marketing-campaigns-edit]] for the freshly-cloned Draft.

## Where to find it

Sidebar → **Marketing** → **Campaigns** → any non-archived tab (Active / Inactive / Draft) → the **Copy** icon (a stack-of-papers `fa-light fa-copy` in a small round button with a *"Copy campaign"* tooltip) in each row's [[campaigns-list-row-actions|Actions column]].

The action is wired to the `apiMarketingCampaigns.copy` mutation:

```
GET /admin/api/core/marketing/campaigns/copy/{id} → {id: newId} → router.push(campaigns-edit/{type}/{newId}?edit=1)
```

The endpoint clones the campaign in a DB transaction and returns the new campaign's `id`; the front-end then navigates to the editor for the new copy.

## What the merchant can do here

Clicking the Copy icon on a row:

1. Activates the Copy button's loading state — `opacity-60 pointer-events-none` is applied to all action icons on that row to prevent double-firing.
2. Calls `GET /admin/api/core/marketing/campaigns/copy/{id}` with the source campaign ID.
3. **On success:** toasts *"Campaign copied successfully."*, the current tab refetches (so the new row appears on the Draft tab), then opens [[marketing-campaigns-edit]] for the new copy with `?edit=1`.
4. **On failure:** the row's loading state clears and an error toast surfaces (`error.message` if present, otherwise *"Error copying campaign."*).

Once on the editor the merchant can rename the copy, pick a different trigger segment, adjust step delays, edit message templates, set a new start delay, and click **Start campaign**.

## Settings & fields

The action exposes no input fields of its own — it consumes only the source `id`. The relevant behaviours are interaction states, not settings:

| Element | Behaviour |
|---------|-----------|
| Copy icon | `fa-light fa-copy` in a round button; `CcTooltip` shows *"Copy campaign"* on hover. |
| Loading state | `opacity-60 pointer-events-none` on all row action icons while the mutation is in flight (prevents double-firing). |
| Success toast | *"Campaign copied successfully."* |
| Error toast | `error.message`, falling back to *"Error copying campaign."* |
| Editor entry | `router.push({name: 'campaigns-edit', params: {type, id: String(result.id)}, query: {edit: '1'}})`. |

### Editor entry: the `?edit=1` query trick

When Copy redirects to the editor it explicitly passes `query: {edit: '1'}`. This is what unlocks the editor for an editable Draft — the editor's `isReadOnly` computed checks `route.query.edit === '1'` first; without that flag, even a Draft would render read-only. This mirrors how the campaigns list's row-click also passes `?edit=1` for Draft rows. The query flag is the editor's "force editable" override.

## Business rules

### No confirmation modal

There is **no** "Are you sure?" prompt — Copy is a one-click action. This is intentional: Copy is non-destructive on the source (no risk of data loss), and the merchant lands on the editor immediately and can discard / delete the copy if they didn't mean to.

### No "Copy options" picker

Unlike some other admin tools, there is no modal asking the merchant to choose what to copy ("Copy actions only? Copy segment? Rename?"). The action is **all or nothing** — the entire campaign config is replicated (see [[campaigns-copy-what-transfers]] for the exact field set). To customise the copy, the merchant uses the editor after landing on it.

### The clone is one all-or-nothing transaction

The clone runs inside a single DB transaction: saves are atomic. If anything fails inside the transaction, nothing is saved and the merchant gets the error message back. The high-level sequence is:

1. Load the source with only the cloneable fields, eager-loading its actions and action templates.
2. Make an in-memory copy without `archived_at` or `progress`.
3. Replicate each action and template **without** their parent campaign ID.
4. Set `active=2` (Draft) and the *"{title} - Copy"* title.
5. Save inside one transaction — the cascading save covers the campaign + its action relations.
6. After save, walk the new actions and re-link their templates by `(campaign_id, action_order)` to the new action IDs.
7. Redirect to the editor for the new copy.

### Why templates are re-linked after save

The clone replicates each template **without** an action ID (because the new actions don't exist yet at replication time), then links them after creation. The new campaign is saved first (which cascades to the action relation), then each new action's template gets its `action_id` set to the new action's ID. This two-step pattern is required by the create-then-link ordering.

### Failure mode

If the clone fails (rare — usually a DB constraint), the endpoint redirects the merchant back to the campaigns list with a flash error. The merchant sees the error toast and the **source campaign is untouched**.

## Related

- [[marketing-campaigns-copy]] — hub.
- [[campaigns-list-row-actions]] — the row action column where the Copy icon lives.
- [[marketing-campaigns-edit]] — destination editor; opened with `?edit=1` for the new Draft.
- [[marketing-campaigns-draft]] — Draft tab where the new copy appears.
- [[campaign]] — Campaign entity (carries the actions / steps that get cloned).

## Open questions

No outstanding questions.
