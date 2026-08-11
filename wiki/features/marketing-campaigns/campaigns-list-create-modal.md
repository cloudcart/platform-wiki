---
type: feature
nav_path: "Marketing → Campaigns → Create modal"
route_name: campaigns-create
route_path: /admin/marketing-new/campaigns/create/:type(regular|automated)
aliases: ["Create campaign modal", "Regular vs Automated tab", "Predefined automated catalog", "+ Create campaign button"]
tags: [marketing, campaigns, create, modal, predefined]
plan_gates: ["campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[marketing-campaigns]]. See the hub for the other aspects (tabs & filters, AI assistant, row actions, types & actions, rules, execution internals).

# Campaigns — Create campaign modal

## Purpose

The **+ Create campaign** modal is the entry point for every new campaign. It exposes the two campaign shapes (Regular vs Automated) as a two-tab segmented control and — on the Automated tab — a 3-column catalogue of predefined best-practice templates the merchant can clone in one click.

## Where to find it

The modal opens from the **+ Create campaign** button in the top-right action area of the [[marketing-campaigns]] list (size `lg`). It is also bound to the `campaigns-create` route — navigating to `/admin/marketing-new/campaigns/create/:type` opens the same modal pre-set to the URL `type`. The modal is wired to a shared composable `useCampaigns` so it can also open from sibling routes (e.g., the AI Assistant header button can open it pre-set to `automated`).

## What the merchant can do here

- Pick Regular or Automated.
- For Regular: click **Create campaign** to mint a new Draft and jump straight to the editor.
- For Automated: either click **Create campaign** under the **Custom Automation** card (blank-slate) OR pick a card from the predefined catalogue (pre-populated template).
- Close the modal via backdrop click / Escape (both enabled).

## Settings & fields

### Modal structure

`MarketingCampaignsCreateModal.vue` — a `CcPopup` titled *"Create new campaign"* with a loader spinner while the create-meta query (`GET /admin/api/core/marketing/campaigns/create`) is in flight. The body is `MarketingCampaignsModalTabs.vue` — a two-tab segmented control:

| Tab | Has predefined catalog? |
|-----|--------------------------|
| **Regular** | No |
| **Automated** | Yes — 3-column grid below the "Custom Automation" card |

Default-active tab depends on entry path: the **+ Create campaign** button explicitly sets `activeModalTab = 'regular'`; the AI Assistant button can open it pre-set to `automated`.

### Regular tab body

A single centered call-to-action with a calendar icon:

- **Heading:** *"Create regular campaign"*
- **Description:** *"Keep your subscribers engaged by sharing your latest news, promoting a line of products or announcing an event"*
- **Primary button:** *"Create campaign"* — calls `POST /admin/api/core/marketing/campaigns` with `{type: 'regular', title: null, active: 2}`, then navigates to `campaigns-edit/regular/{id}`.
- **Loading state:** the button shows a spinner while the request is in flight; on error a toast *"Error creating campaign"* fires and the modal stays open.

### Automated tab body

Two sections:

1. **Custom Automation card** (top, full-width)
   - Bolt icon + heading *"Custom Automation"*
   - Subtitle *"Create your own automation. You can start from scratch defining your own ideas"*
   - Primary button *"Create campaign"* — same POST as Regular but with `{type: 'automated', ...}`. Navigates to `campaigns-edit/automated/{id}`.

2. **Predefined catalog** (below — only rendered if `predefinedCampaigns.length > 0`)
   - Divider label *"Or choose one of our predefined best practices"*
   - Cards in a 3-column responsive grid (`grid-cols-1 md:grid-cols-2 lg:grid-cols-3`), one card per active predefined campaign returned by the create-meta endpoint.
   - Each card shows: title (predefined campaign title), description, and a *"Create campaign"* link in purple.
   - Clicking the link calls `GET /admin/api/core/marketing/campaigns/create/automated/{predefined_id}` (`createFromPredefined.useMutation` keyed by ID).
   - **Per-card loading state:** clicking *"Create campaign"* on a card adds `opacity-60` + `pointer-events-none` to that card only; the rest of the catalog stays clickable until the mutation resolves.
   - **Loader skeleton** shows while the create-meta query is loading.

See [[marketing-campaigns-from-predefined]] for the full clone-flow internals (what fields the clone copies vs leaves blank).

## Business rules

### Required-channel gate on predefined clone

If a predefined automated template requires a channel that's missing on the store (e.g., a Viber template on a store that hasn't connected Viber), the API returns an error whose message uses the placeholder `{channels}`. The front-end interpolates the channel list from `error.response.data.props.channels` and surfaces it as a toast. The clone does **NOT** happen — the merchant must configure the missing channels first (see [[marketing-channels]]).

### A new campaign starts as Draft

`POST /admin/api/core/marketing/campaigns` creates with `type` from URL (`regular|automated`), `title = null`, `active = 2` (Draft). The merchant is immediately routed to the edit page to fill it in. See [[campaigns-list-rules]] for the full quota / title-uniqueness check that runs on this POST.

### Modal close behaviour

- Closes on backdrop click and Escape key (`no-close-on-backdrop: false`, `no-close-on-escape: false`).
- Closes automatically when the route changes to `campaigns-create` or `campaigns-edit` (the watcher in `useCampaigns` clears `createModal.value`).

### Plan-quota error fires AFTER the click

When the merchant has reached the plan's campaign quota, the **+ Create campaign** button itself fires the error after click — there is no preflight grey-out. See [[campaigns-list-rules]] for quota details.

## Related

- [[marketing-campaigns]] — hub.
- [[marketing-campaigns-create]] — campaign-create endpoint variants in detail.
- [[marketing-campaigns-from-predefined]] — predefined-clone flow internals.
- [[campaigns-list-types-and-actions]] — Regular-vs-Automated shape comparison + action-type catalogue.
- [[campaigns-list-ai-assistant]] — sibling drawer that also creates campaigns (from AI suggestions).
- [[campaigns-list-rules]] — quota + title-uniqueness rules that gate the create POST.
- [[marketing-channels]] — channels that must be configured before a predefined clone works.

## Open questions

None.
