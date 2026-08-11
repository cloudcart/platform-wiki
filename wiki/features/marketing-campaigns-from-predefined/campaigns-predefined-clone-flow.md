---
type: feature
nav_path: "Marketing → Campaigns → Create campaign → From template → Clone flow"
route_name: admin.api.campaigns.create
route_path: /admin/api/core/marketing/campaigns/create/automated/{id}
aliases: ["Clone predefined campaign", "Create campaign from template", "Predefined clone transaction", "Стартирай от шаблон — клониране"]
tags: [marketing, campaigns, predefined, templates, clone]
plan_gates: ["campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
> Part of [[marketing-campaigns-from-predefined]]. See the hub for the other aspects (catalog UI, channel gate, segment & tags, curation).

# Predefined campaigns — the clone flow

## Purpose

This page documents what happens when the merchant clicks **Create campaign** on a predefined card: the click handler, the rows the clone materialises in the store's database, the single all-or-nothing transaction, the always-Draft result, and the plan-tier slot the clone consumes. The browse UI that surfaces the cards is on [[campaigns-predefined-catalog-ui]].

## Where to find it

Triggered from any predefined card's purple **Create campaign** link in the **Automated** tab of the Create-campaign modal (Marketing → Campaigns → **+ Create campaign** → **Automated**). The link calls the clone endpoint:

| Endpoint | Method | Route path |
|----------|--------|------------|
| `admin.api.campaigns.create` (`createFromPredefined` mutation) | GET | `/admin/api/core/marketing/campaigns/create/automated/{id}` |

## What the merchant can do here

- **Clone a template into a real Draft campaign** with a single click — every step and message text is copied in.
- **Land in the editor** ([[marketing-campaigns-edit]]) with everything pre-filled, ready to review and adjust.
- **Retry safely** if the clone fails — nothing partial is saved (see Business rules).

## Settings & fields

### Click flow — `handleCreateFromPredefined(id)`

1. Sets the local `creatingPredefinedId.value = id` so only THIS card shows the per-card loading state.
2. Calls `GET /admin/api/core/marketing/campaigns/create/automated/{id}` via the `createFromPredefined` mutation with `suppressGlobalErrorHandling: true` (errors handled inline).
3. **On success:** `router.push({name: 'campaigns-edit', params: {type: 'automated', id: String(result.id)}})` — the new Draft opens in the editor.
4. **On error (missing-channel):** the API returns `{ message: "This campaign required the following channel: {channels}", props: { channels: "Email, Viber" } }`. The front-end replaces `{channels}` with the props value and surfaces the resolved string as a toast; the card returns to idle and no campaign is created. Full mechanics in [[campaigns-predefined-channel-gate]].
5. **On other errors:** generic toast *"Error creating campaign from template"*.

### What the clone materialises

When the clone succeeds, these rows are written into the store's database:

- A new row in `campaigns` with `type=automated`, `active=2` (Draft), `title` and other settings copied from `predefined.data.campaign`, and `trigger_segment` resolved (see [[campaigns-predefined-segment-tags]]).
- New rows in `campaign_actions` for every step in the template, in their original order.
- New rows in `campaign_action_templates` for every step's message template — for Email the full Unlayer HTML JSON, for SMS / Viber the message body text, for Web Push the title + body.
- Any tags referenced by the template are auto-added to the store's tag library — see [[campaigns-predefined-segment-tags]].

On success the merchant gets `status = success`, the toast *"Campaign created successfully"*, and a redirect to the editor with everything pre-filled.

## Business rules

### Cloning is transactional — all or nothing

The entire clone (campaign row + actions + action templates + segment auto-create + tag auto-add) runs inside one DB transaction. If anything throws — malformed template payload, segment creation failure, etc. — the whole transaction rolls back: no campaign row, no segment, no tags. The merchant sees the error and the campaigns list stays clean. Retry is safe.

### The cloned campaign is always a Draft

Even though the template ships with all its steps + messages, the clone starts as `active=2` (Draft). The merchant MUST click **Start campaign** in the editor to launch it. This gives a final review window to adjust title, segment, discount codes, exit tag, etc.

### Clone consumes a plan-tier campaign slot

The clone runs through the standard campaign-creation pipeline and is subject to the plan-tier quota. If the merchant has hit their plan ceiling, the clone fails with a 402 Payment Required (modern Vue API namespace) or a redirect to the plan upgrade page (legacy sitecp). The merchant must free a slot by permanently deleting an Archived campaign first.

### 404 guards before the transaction

Before opening the transaction the endpoint loads the template by ID (404 if missing) and verifies the `data.campaign` key is present (404 if absent — see [[campaigns-predefined-catalog-ui]]). Only then does it build the in-memory campaign and run the channel pre-check ([[campaigns-predefined-channel-gate]]).

## Related

- [[marketing-campaigns-from-predefined]] — hub.
- [[campaigns-predefined-catalog-ui]] — the card grid whose **Create campaign** link triggers this flow.
- [[campaigns-predefined-channel-gate]] — the channel pre-check that can abort the clone before any rows are written.
- [[campaigns-predefined-segment-tags]] — segment resolution + tag auto-add inside the clone transaction.
- [[marketing-campaigns-edit]] — the editor the merchant lands in after a successful clone.
- [[campaign]] — Campaign entity the clone materialises.

## Open questions

None.
