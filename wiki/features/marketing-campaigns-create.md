---
type: feature
nav_path: "Marketing → Campaigns → Create campaign"
route_name: campaigns-create
route_path: /admin/marketing-new/campaigns/create/:type(regular|automated)
aliases: ["Create campaign", "Start a campaign", "New campaign picker", "Campaign type picker", "Създай кампания", "Нова кампания"]
tags: [marketing, campaigns, create]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-05-23
updated: 2026-06-10
source_count: 2
---
# Create campaign

## Purpose

The **Create campaign** picker is the first screen the merchant sees after clicking **+ Create campaign** in the Campaigns list. It's a **modal** that lets the merchant decide on the campaign's *shape* — **Regular** (a one-shot blast to an existing segment) or **Automated** (a multi-step automation triggered by a customer event) — and, for automated campaigns, the *starting point* — **build from scratch** or **start from one of CloudCart's pre-built best-practice campaigns**.

This is a routing screen — nothing is created in the database until a **Create campaign** button is clicked. The merchant's two choices in this modal decide what happens next:

- **Regular → Create campaign** — creates an empty Regular campaign as Draft, opens [[marketing-campaigns-edit]].
- **Automated → Create your own automation → Create campaign** — creates an empty Automated campaign as Draft, opens [[marketing-campaigns-edit]].
- **Automated → pick a predefined template → Create campaign** — clones a curated template into a new Automated campaign with all its steps and message templates pre-filled, opens [[marketing-campaigns-edit]] for review. See [[campaigns-create-predefined-clone]] for the clone mechanics and [[marketing-campaigns-from-predefined]] for the catalog itself.

## Where to find it

Sidebar → **Marketing** → **Campaigns** → on any tab of the campaign list, click **+ Create campaign** in the top-right.

In the modern admin the picker opens as a **modal** (`MarketingCampaignsCreateModal`, a `CcPopup` titled *"Create new campaign"*), NOT a separate page route. A segmented tab control inside the modal switches between the two campaign shapes (Regular / Automated). Switching the tab is a purely client-side swap of the modal body — no AJAX, no page reload. For the full modal layout, tabs, loader, and per-card states, see [[campaigns-create-modal-anatomy]].

## What the merchant can do here

- **Switch between Regular and Automated** with the two segmented tabs.
- On the **Regular** tab: click **Create campaign** to create an empty Regular Draft and jump to the editor.
- On the **Automated** tab: click **Create campaign** in the *Custom Automation* card to create an empty Automated Draft, OR pick a card from the predefined best-practices catalog to clone a fully pre-filled template.
- **Close** the modal (X / backdrop / Escape) to cancel — no campaign is created.

The mechanics behind each button (loading states, which API call fires, where the merchant lands) are documented in [[campaigns-create-modal-anatomy]]. What the merchant *gets* from each shape is on [[campaigns-create-regular-vs-automated]].

## Settings & fields

The two campaign shapes and the choices the merchant makes in this picker are documented across the cluster:

- **Regular vs Automated** — when to use each, the trigger condition each gets, the editor steps that follow: see [[campaigns-create-regular-vs-automated]].
- **The modal itself** — tabs, the Regular card, the Automated three-area layout, the predefined grid, loader and meta query, per-card loading states: see [[campaigns-create-modal-anatomy]].
- **Predefined catalog** — what's listed, locale + active + configured-channel filtering, the required-channels gate, transactional cloning, auto-segment creation: see [[campaigns-create-predefined-clone]].

## Sub-pages (in this cluster)

This feature is split into 4 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[campaigns-create-regular-vs-automated]] — the two campaign shapes: when to use each, trigger condition (`gets_in_segment` locked for Regular vs merchant-picked for Automated), the 5 editor steps, which trigger options the modern UI actually exposes.
- [[campaigns-create-modal-anatomy]] — the modern Vue picker (`MarketingCampaignsCreateModal`): `CcPopup` shell, two tabs, Regular card, Automated three areas, predefined grid, modal-loader + meta query, per-card loading states, cross-modal disabling.
- [[campaigns-create-predefined-clone]] — the predefined catalog: locale + active + configured-channel filtering, the required-channels gate, transactional clone (campaign + actions + templates + tags), auto-segment creation, central platform-managed `predefined_campaigns` table.
- [[campaigns-create-draft-business-rules]] — what happens on **Create**: nothing saved until the button is clicked, Draft created with `title=null` / `active=2`, trigger auto-lock for Regular, plan-quota check at insert time, anti-spam policy gate, permission gate, plan-gating effects.

## Business rules

The full rule set lives on the aspect pages. The headline rules:

- **Nothing is saved until a Create button is clicked** — picking a tab or browsing the catalog leaves zero residue. See [[campaigns-create-draft-business-rules]].
- **Every new campaign is born as a Draft** with `title=null` and `active=2`, immediately visible on the Draft tab as "(No title)". See [[marketing-campaigns-draft]] + [[campaigns-create-draft-business-rules]].
- **Regular campaigns auto-lock their trigger to `gets_in_segment`** server-side. See [[campaigns-create-regular-vs-automated]].
- **Predefined templates require their channels configured first** — the clone is blocked with a channel-required alert if any channel is missing. See [[campaigns-create-predefined-clone]].
- **The plan-quota check fires on Create, not on picker open** — browse freely; the 402 / upgrade redirect only fires after clicking **Create campaign**. See [[campaigns-create-draft-business-rules]].
- **The anti-spam policy must be accepted once per store** before the picker is reachable. See [[marketing-campaigns-policy]].

## Related

- [[marketing-campaigns]] — parent list page; **+ Create campaign** action on every status tab opens this picker.
- [[marketing-campaigns-edit]] — the editor that opens immediately after a campaign is created here.
- [[marketing-campaigns-from-predefined]] — companion page documenting the predefined campaign CATALOG (what categories exist, how the merchant browses).
- [[marketing-campaigns-draft]] — every new campaign starts on the Draft tab.
- [[marketing-campaigns-policy]] — anti-spam policy gate every campaign action passes through.
- [[marketing-channels]] — channel setup the predefined-campaign flow checks against.
- [[marketing-segments]] — the audience picker the merchant fills in next in the editor.
- [[campaign]] — Campaign entity.

## Open questions

(All previously listed questions have been resolved — see the aspect pages' Business rules.)
