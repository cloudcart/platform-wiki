---
type: feature
nav_path: "Marketing → Campaigns"
route_name: campaigns
route_path: /admin/marketing-new/campaigns
aliases: ["Campaigns", "Email campaigns", "Marketing automation", "Кампании", "Маркетингови кампании", "Имейл кампании"]
tags: [marketing, campaigns, automation, email, sms, viber, web-push]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-05-21
updated: 2026-06-10
source_count: 2
---

# Campaigns

## Purpose

The **Campaigns** screen is the merchant's hub for every outbound marketing message the store sends — newsletters, promotional blasts, automated drip sequences, abandoned-cart-recovery flows, re-engagement, birthday offers, post-purchase upsells. Two shapes are managed here: **Regular** (a one-shot blast to a segment — pick segment, pick channel, write message, send) and **Automated** (a multi-step automation triggered by a customer event, with conditional branches and per-step delays). Both deliver through **Email**, **SMS**, **Viber**, or **Web Push**, with statistics aggregated per channel + per step + per campaign.

The list shows campaigns split across four status tabs (**Active**, **Inactive**, **Archived**, **Draft**) with a cross-tab channel filter row under the table. Clicking a row opens that campaign's editor; the page also exposes an **AI Assistant** drawer with machine-generated campaign suggestions.

## Where to find it

Sidebar → **Marketing** → **Campaigns** (under the Campaigns dropdown).

The base route `/admin/marketing-new/campaigns` redirects to `/admin/marketing-new/campaigns/active`. Each status tab is a distinct route.

## Sub-pages (in this cluster)

Drill into the aspect page that matches the question rather than reading every page.

- [[campaigns-list-tabs-and-filters]] — the four status tabs, the cross-tab channel filter row, the table columns, the status enum, and the progress enum.
- [[campaigns-list-create-modal]] — the **+ Create campaign** modal: Regular vs Automated tabs, the predefined-automation catalogue, and loading / error / close behaviour.
- [[campaigns-list-ai-assistant]] — the **AI Campaign Assistant** drawer that surfaces seasonal, trending, and behaviour-derived suggestions and mints a Draft in one click.
- [[campaigns-list-row-actions]] — the row-actions column (archive / unarchive, copy, delete) plus the bulk-delete bar on the Archived tab; confirm patterns and toast strings.
- [[campaigns-list-types-and-actions]] — the **Regular** vs **Automated** shape decision plus the per-step action-type catalogue (`email`, `sms_*`, `viber_message`, `web_push`, `set_tags`, etc.) and completion conditions.
- [[campaigns-list-rules]] — every invariant that gates create / save / start / attribution: title uniqueness, Draft-only edits, channel guards, last-touch attribution, plan quota, step caps, autosave.
- [[campaigns-list-execution-internals]] — the enrolment + send pipeline once a campaign launches, batch sizes, and the hourly statistics aggregation lag.

### Sub-screens (deep links)

| Label | Route name | Route path |
|-------|------------|------------|
| Campaigns (Active default) | `campaigns` | `/admin/marketing-new/campaigns` |
| Active list | `campaigns-active` | `/admin/marketing-new/campaigns/active` |
| Inactive list | `campaigns-inactive` | `/admin/marketing-new/campaigns/inactive` |
| Archived list | `campaigns-archived` | `/admin/marketing-new/campaigns/archived` |
| Draft list | `campaigns-draft` | `/admin/marketing-new/campaigns/draft` |
| Saved email templates | `campaigns-email-saved-templates` | `/admin/marketing-new/campaigns/configuration/channel/email/saved` |
| Channels | `campaigns-channels` | `/admin/marketing-new/campaigns/channels` |
| Anti-spam policy | `campaigns-policy` | `/admin/marketing-new/campaigns/policy` |
| Create | `campaigns-create` | `/admin/marketing-new/campaigns/create/:type(regular\|automated)` |
| Edit | `campaigns-edit` | `/admin/marketing-new/campaigns/edit/:type(regular\|automated)/:id` |
| Statistics | `campaigns-statistics` | `/admin/marketing-new/campaigns/statistics/:id` |

## What the merchant can do here

- Switch between status tabs (Active / Inactive / Archived / Draft) and filter by channel (All / Email / SMS / Viber / Web push) via the bottom tab row — see [[campaigns-list-tabs-and-filters]].
- Click **+ Create campaign** (Regular vs Automated modal) or **AI Assistant** (suggestion drawer).
- Click a row to open the editor (`campaigns-edit/{type}/{id}`) — see [[marketing-campaigns-edit]].
- Toggle a campaign's Active/Inactive switch inline; archive/unarchive, copy, or delete — see [[campaigns-list-row-actions]].
- Drill into per-campaign **Statistics**, **Subscribers**, and **Logs**.
- Filter by Type / Progress / Has subscribers / Subscribers / Segment; search by title; sort by ID / title / subscribers count.

## Settings & fields

The hub catalogues the list-page surface only; column meanings, modal layout, and the action catalogue live on the sub-pages.

- **Status tabs + channel filter row + table columns** — full catalogue on [[campaigns-list-tabs-and-filters]]. Status enum: `0 = Inactive`, `1 = Active`, `2 = Draft`. Progress enum: `waiting`, `waiting_delayed`, `delayed`, `executing`, `completed`. Channel filter keys: `all`, `email`, `sms`, `viber`, `web_push` (`sms` matches both `sms_nth_message` and `sms_msghub_message`).
- **Create modal** — layout, predefined-catalog grid, required-channel gate on [[campaigns-list-create-modal]].
- **AI Assistant drawer** — three suggestion tabs (`events`, `trending`, `behavior`), plan-feature modal on [[campaigns-list-ai-assistant]].
- **Row actions and bulk delete** — confirm patterns, toast strings, Archived-only bulk on [[campaigns-list-row-actions]].
- **Action-type catalogue and step shape** — every `action_type` key, completion-condition and trigger-condition options on [[campaigns-list-types-and-actions]].
- **Plan-feature keys**: `abandoned_orders`, `campaigns` (quota counts every non-deleted campaign — Draft, Inactive, and Archived all count, so freeing a slot requires a permanent delete from the Archived tab — see [[campaigns-list-rules]]).

## Business rules

The full catalogue is on [[campaigns-list-rules]]. Highlights that apply cluster-wide:

- **Anti-spam policy gate.** Every campaign endpoint and the `campaigns-channels` / `campaigns-email-saved-templates` routes require `campaigns.anti_spam_policy_accepted = true`. Until accepted, the merchant is bounced to [[marketing-campaigns-policy]].
- **Draft-only edits.** Saving a non-Draft campaign is rejected with *"Campaign has status {status}! You can only edit draft campaigns!"*. To change a running campaign's trigger segment or steps, the merchant copies it (a new Draft) and launches the copy.
- **Title uniqueness across all non-deleted rows.** Archived and Inactive campaigns still hold their title; only deleted titles are reusable.
- **Plan quota fires on every create path.** Manual create, predefined clone, row copy, and AI-from-suggestion all hit the plan limit; over-quota triggers a 402 / upgrade redirect after the click (no preflight grey-out).
- **Channel guards.** Sending checks `channel.installed`, `status`, and (for credit channels) `plan_remaining` vs the segment's deliverable count. Suspended channels block the campaign with one of `suspended_by.spam` / `suspended_by.bounced` / `suspended_by.open` / `suspended_by.cc_denied` and the merchant fixes the channel first.
- **Step caps.** Regular campaigns max **1** action step; Automated campaigns max **5**.
- **Statistics aggregation lag.** The `reached` / `orders` / `turnover` columns reflect the hourly statistics aggregation, not live state (tooltip: *"Statistical information is updated every hour."*). See [[campaigns-list-execution-internals]].
- **Last-touch attribution.** The `?cc_campaign=...` link parameter is held for the session; later campaign clicks overwrite it, so the order is stamped with the most-recently-clicked campaign. No first-touch / multi-touch model. See [[marketing-campaigns-statistics-full]].
- **Soft-delete with cascade.** Delete is soft; permanent purge cascades to actions, templates, logs, and detaches all subscribers. Bulk-delete on Archived is soft.

## Related

- [[marketing]] — parent hub.
- [[marketing-dashboard]] — Marketing Suite — shows the Top / Recent campaigns table that links here.
- [[marketing-campaigns-policy]] — anti-spam policy gate that must be accepted first.
- [[marketing-campaigns-edit]] — the per-campaign editor opened from any list row.
- [[marketing-campaigns-statistics]] — per-campaign delivery / open / click / order / revenue dashboard.
- [[marketing-campaigns-statistics-full]] — full attribution mechanic and last-touch model.
- [[marketing-campaigns-statistics-log]] — per-message delivery log.
- [[marketing-campaigns-subscribers]] — per-campaign subscriber list (in-funnel, completed, removed).
- [[marketing-campaigns-archive]] — archive / unarchive endpoint behaviour.
- [[marketing-campaigns-copy]] — what the Copy action does and doesn't preserve.
- [[marketing-channels]] — channel configuration prerequisite for the predefined catalogue and credit channels.
- [[marketing-segments]] — segments — every campaign needs a segment as audience.
- [[marketing-subscribers]] — subscriber CRM — the campaigns target subscribers.
- [[marketing-omnichannel-mails-list]] — transactional emails (separate from these promotional campaigns).
- [[marketing-discounts]] — discounts — campaigns can include dynamically-generated discount codes via the `{$dynamic_discount_code}` and `{$generate_discount_code:10%}` placeholders.
- [[campaign]] — Campaign entity.
- [[channel]] — Channel entity (the delivery medium).
- [[segment]] — Segment entity.
- [[subscriber]] — Subscriber entity.
- [[email-template]] — Email template entity.
- [[notification-delivery]] — outbound delivery internals.
- [[plan-gates]] — `campaigns.*` plan limits, channel-credit limits.
- [[background-queue-inventory]] — catalogue of all background processes; covers campaign-send fan-out timing and how to track in-flight sends on Queue View.
- [[marketing-campaigns-select]] — the Regular-vs-Automated type picker shown when creating a campaign.

## Open questions

(All previously listed questions have been resolved — see [[campaigns-list-rules]].)
