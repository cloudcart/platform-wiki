---
type: feature
nav_path: "Marketing → Campaigns → Edit"
route_name: campaigns-edit
route_path: /admin/marketing-new/campaigns/edit/:type(regular|automated)/:id
aliases: ["Edit campaign", "Campaign editor", "Setup campaign", "Configure campaign", "Редакция на кампания", "Настройка на кампания"]
tags: [marketing, campaigns, edit]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-05-23
updated: 2026-06-10
source_count: 2
---

# Edit campaign

## Purpose

The **Edit campaign** screen is where the merchant builds (or re-builds) a campaign — title, trigger segment, action steps, message templates, exit tag, and exit goal. It's the same screen for both **Regular** and **Automated** campaigns (with slightly different fields visible per shape) and for both fresh-from-scratch drafts and clones from predefined templates. Every campaign passes through here at least once on its way from Draft to Active.

The page is a **5-step vertical form** with a numbered step badge on each box. The merchant works top-to-bottom: name + schedule → segment → action steps + messages → exit tag → exit purpose. The top-right action area carries **Save draft** and **Start campaign** buttons. Started campaigns become read-only on the same URL — the merchant can still open the editor to inspect the configuration, but the boxes are visually disabled.

Because the editor is large and covers several independent concerns, it is split into aspect pages. Drill into the aspect that matches the question rather than reading every page.

## Where to find it

Sidebar → **Marketing** → **Campaigns** → click any campaign row on any tab → opens the editor.

The route is type-aware: `regular` and `automated` campaigns each use a distinct URL path. The trailing `{campaign_id}` is the campaign's numeric ID.

| Route name | Route path |
|------------|------------|
| `campaigns-edit` (Vue page) | `/admin/marketing-new/campaigns/edit/:type(regular\|automated)/:id` |
| `apiMarketingCampaigns.update` (PUT save target) | `/admin/api/core/marketing/campaigns/{id}` |
| `apiMarketingCampaigns.status` (activation target) | `/admin/api/core/marketing/campaigns/status/{id}/{status}` |

Type values: `regular` or `automated`. A campaign cannot be re-typed — opening a regular campaign at the automated URL (or vice versa) loads the campaign but the form's UI affordances are wrong. Saving goes through the JSON API (`PUT /campaigns/{id}`), not a form POST to the page route.

## What the merchant can do here

The page is structured as a 5-step vertical form. Each step is a box with a numbered badge on its left, and each step has its own aspect page below.

- **Step 1 — Campaign info**: title, start delay (Regular), repeat + use-existing-subscribers switches (Automated). See [[campaigns-edit-step-1-info]].
- **Step 2 — Trigger / segment**: trigger condition (Automated), segment autocomplete + live subscribers count chip, inline "Create segment" side-panel. See [[campaigns-edit-step-2-trigger]].
- **Step 3 — Campaign actions**: the funnel builder. Pick action type per step (Email / SMS / Viber / Web Push), set execute delay, attach message template; for Automated only, chain steps and add conditional branches. See [[campaigns-edit-step-3-actions]] for action steps and [[campaigns-edit-step-3-conditions]] for IF/ELSE condition blocks.
- **Step 4 — Tag customers + Step 5 — Campaign exit**: the exit tag (autocomplete with **+ Add new**) and the exit condition (`makes_an_order`). See [[campaigns-edit-exit-and-tagging]].
- **Per-channel message editor sub-modals** (Viber / SMS / Web Push / Email): fields, character limits, variables legend, mobile-phone preview, save behaviour. See [[campaigns-edit-message-modals]].
- **Save draft + Review-and-launch + draft guard + activation cascade**: what happens when the merchant clicks **Save draft** or **Start campaign**, including the modal, the chained jobs, and the `beforeunload` guard. See [[campaigns-edit-launch-flow]].
- **Business rules** (edit-only-in-Draft, pre-flight checks, save transaction, plan-tier quota, max-steps cap, `?edit=1` legacy fallback): see [[campaigns-edit-validation-rules]].

## Sub-pages (in this cluster)

- [[campaigns-edit-step-1-info]] — Step 1 "Main settings": title, `start_at` + `start_at_enabled`, `repeat`, `use_exists_subscribers`.
- [[campaigns-edit-step-2-trigger]] — Step 2 "Trigger": `trigger_condition` dropdown, segment autocomplete, live subscribers-count chip, inline segment-create side-panel.
- [[campaigns-edit-step-3-actions]] — Step 3 action steps: action-type dropdown (configured channels only), execute-after delay, per-channel state preservation, credit / channel-limit banners.
- [[campaigns-edit-step-3-conditions]] — Step 3 condition blocks (Automated only): IF / ELSE branches, deadline interval, condition-type options, overdue actions.
- [[campaigns-edit-exit-and-tagging]] — Steps 4 + 5: exit-tag autocomplete + `customers_tags` and the `purpose` exit-condition dropdown.
- [[campaigns-edit-message-modals]] — per-channel message editor sub-modals: Viber / SMS / Web Push field shapes, character limits, AI writer, variables legend, mobile preview, save endpoint.
- [[campaigns-edit-launch-flow]] — Save draft + Review-and-launch modal + draft guard + activation cascade (`SetSubscribersToSingleSegment` → `ExecuteCampaign`).
- [[campaigns-edit-validation-rules]] — business rules: edit-only-in-Draft, pre-flight checks on Start, save-cascade transaction, plan-tier quota, max-steps cap, `?edit=1` legacy fallback, title uniqueness.

## Settings & fields

The top-level form payload (`PUT /admin/api/core/marketing/campaigns/{id}`) is composed of fields from all five steps. The exhaustive field-by-field tables live on each step's aspect page. The save endpoint validators that gate the whole payload live on [[campaigns-edit-validation-rules]].

The top-right action area carries:

| Button | Visible when | Action |
|--------|--------------|--------|
| **Save draft** | Not read-only (create page OR draft being edited) | Persists current form state with `draft=true` payload; navigates to `campaigns-draft` on success and toasts *"Draft saved successfully."* See [[campaigns-edit-launch-flow]]. |
| **Start campaign** | Same condition AND campaign already has an ID | Opens the **Review and launch** modal. See [[campaigns-edit-launch-flow]]. |

For already-started campaigns (`active=1`), both buttons are hidden — the boxes display the configuration but inputs are disabled (see [[campaigns-edit-validation-rules]]).

## Business rules

The full catalogue lives on [[campaigns-edit-validation-rules]]. The most-impactful rules at a glance:

- **Edit is only fully open in Draft state** (`active=2`). Active (`active=1`) and Inactive (`active=0`) are view-only; Archived is permanently locked.
- **Title uniqueness per store** — duplicate save returns *"Campaign with this title already exists"*.
- **Pre-flight checks on Start campaign** — all steps saved, all messages set, channels configured + active + sufficient credits, segment finished filtering.
- **Max action steps per campaign** — Regular: **1**; Automated: **5**.
- **Save-as-draft skips pre-flight checks** — only title uniqueness is checked.
- **Channel credit pre-check is on Start, not on Save draft**.
- **`?edit=1` URL query is a usability layer only** — the API still rejects edits to non-Draft campaigns.

## Related

- [[marketing-campaigns]] — parent hub; the campaigns list links to this editor on every row.
- [[marketing-campaigns-create]] — the picker that creates the Draft this editor opens.
- [[marketing-campaigns-from-predefined]] — pre-built templates that also land here on clone.
- [[marketing-campaigns-message-template]] — message editor that opens for each step (the Unlayer designer for Email).
- [[marketing-campaigns-banned-info]] — banned-reason explainer when a campaign is broken.
- [[marketing-campaigns-statistics]] — analytics for a started campaign.
- [[marketing-campaigns-subscribers]] — recipient list for an active campaign.
- [[marketing-segments]] — segments are the audience picker in Step 2.
- [[marketing-channels]] — channels referenced by the action steps.
- [[marketing-subscribers]] — the customers / subscribers being enrolled.
- [[campaign]] — Campaign entity.
- [[customer-group]] — referenced by the `set_customer_group` action.

## Open questions

No outstanding questions.
