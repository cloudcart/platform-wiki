---
type: feature
nav_path: "Marketing → Campaigns → Create campaign → Draft & gating rules"
route_name: campaigns-create
route_path: /admin/marketing-new/campaigns/create/:type(regular|automated)
aliases: ["Create campaign draft rules", "Campaign created as draft", "Campaign quota check", "Campaign plan gating", "Campaign create permission", "Anti-spam policy gate", "Кампания създадена като чернова"]
tags: [marketing, campaigns, create]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Create campaign — draft & gating rules

> Part of [[marketing-campaigns-create]]. See the hub for related aspects (Regular vs Automated, modal anatomy, predefined clone).

## Purpose

This aspect documents what happens **when the merchant clicks Create campaign** — the database write, the Draft state every new campaign is born into — plus the gates that surround the picker: the anti-spam policy gate, the staff permission gate, the plan-feature gate, and the plan-quota check. It answers "where did my new campaign go?" and "why can't I create one?".

## Where to find it

Sidebar → **Marketing** → **Campaigns** → **+ Create campaign**. The gates described here run around this entry point; the resulting Draft lands on the [[marketing-campaigns-draft|Draft]] tab.

## What the merchant can do here

- Create an empty Draft (Regular or Custom Automation) or a pre-filled Draft (predefined clone) — see [[campaigns-create-modal-anatomy]].
- Find the new Draft immediately on the **Draft** tab, labelled "(No title)" until edited and saved.

## Settings & fields

### What the Create button writes

| Path | API call | Row written |
|------|----------|-------------|
| Regular | `POST /admin/api/core/marketing/campaigns` `{type: regular, title: null, active: 2}` | Draft Regular campaign; `trigger_condition=gets_in_segment` auto-set server-side. |
| Custom Automation | `POST /admin/api/core/marketing/campaigns` `{type: automated, title: null, active: 2}` | Empty Draft Automated campaign. |
| Predefined card | `GET /admin/api/core/marketing/campaigns/create/automated/{id}` | Cloned Draft Automated campaign + actions + templates (see [[campaigns-create-predefined-clone]]). |

On success every path navigates the merchant to [[marketing-campaigns-edit|the editor]].

## Business rules

### Nothing is saved until a Create button is clicked

Picking a tab is a UI-only action — switching between Regular and Automated does NOT create any database rows. The merchant can open the panel, browse the catalog, close it, and there's zero residue in the campaigns list.

### Draft created with no title

When the merchant clicks **Create campaign** (for any shape), the platform inserts a row with `title=null` and `active=2`. The campaign is **immediately** visible on the Draft tab of the campaign list (see [[marketing-campaigns-draft]]) — labelled "(No title)" until the merchant edits and saves it from the editor.

### Anti-spam policy gate

Like every campaign controller, the create flow runs through the campaign anti-spam policy gate. A merchant who hasn't accepted the policy is redirected to [[marketing-campaigns-policy]] before reaching this picker. The merchant accepts the policy once per store — afterwards this picker is reachable freely.

### Permission

Like every campaign endpoint, this picker is gated behind the campaign permissions — a staff member's role must include the campaign-edit permission to see the **+ Create campaign** button and use this panel.

### Plan-gating affects what shows up

The plan-gate `abandoned_orders` toggles the entire campaigns feature on or off — on plans without it, the merchant cannot reach this picker at all (the sidebar item is hidden). The per-channel plan-gates (`campaign.channel.email`, `campaign.channel.sms_*`, `viber_messages`, `campaign.channel.web_push`) affect which channels can later be used inside the editor — they don't block this picker but they do constrain which predefined templates the merchant can actually launch (a template using a channel the merchant doesn't have access to will fail the channel-required check at clone time — see [[campaigns-create-predefined-clone]]).

### Plan-limit check fires on the Create button, not on the picker open

The plan-tier campaign quota is checked at row-insert time, not when the merchant opens the create panel. So the merchant can browse the catalog freely; the 402 / SiteCp redirect only fires after they click **Create campaign**. If the merchant is at quota, the failure appears as a SweetAlert error or a redirect to the plan-upgrade page. The plan check applies even to predefined-template cloning — clicking **Create campaign** on a curated template still costs one campaign slot.

## Related

- [[marketing-campaigns-create]] — hub.
- [[marketing-campaigns-draft]] — where the new Draft lands (`active=2`, "(No title)").
- [[marketing-campaigns-policy]] — anti-spam policy gate the create flow passes through.
- [[marketing-campaigns-edit]] — the editor the create navigates to.
- [[campaign]] — Campaign entity written on Create.

## Open questions

None.
