---
type: feature
nav_path: "Marketing → Campaigns → Create campaign → Regular vs Automated"
route_name: campaigns-create
route_path: /admin/marketing-new/campaigns/create/:type(regular|automated)
aliases: ["Regular vs Automated campaign", "Campaign shape", "Regular campaign", "Automated campaign", "Campaign trigger condition", "Регулярна vs автоматизирана кампания"]
tags: [marketing, campaigns, create]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Create campaign — Regular vs Automated

> Part of [[marketing-campaigns-create]]. See the hub for related aspects (modal anatomy, predefined clone, draft business rules).

## Purpose

This aspect explains the **two campaign shapes** the merchant chooses between in the [[marketing-campaigns-create|Create campaign]] picker — **Regular** and **Automated** — what each is for, what trigger condition each gets, and the editor steps that follow. The shape decided here is permanent for the campaign's life: a Regular campaign can never become Automated and vice-versa.

## Where to find it

Sidebar → **Marketing** → **Campaigns** → **+ Create campaign** → the two segmented tabs at the top of the modal (**Regular** / **Automated**). The shape is locked the moment the merchant clicks **Create campaign** on either tab.

## What the merchant can do here

- Choose **Regular** for a one-time blast (newsletter, promotion announcement) to an existing segment.
- Choose **Automated** for an ongoing, event-triggered sequence (welcome series, abandoned-cart recovery, post-purchase upsell, win-back) that keeps enrolling new subscribers as the trigger fires.
- After clicking **Create campaign**, continue into [[marketing-campaigns-edit]], which runs the same 5-step flow for both shapes.

## Settings & fields

### Regular vs Automated — what the merchant gets

| Shape | When to use | Trigger condition | Editor steps |
|-------|-------------|-------------------|--------------|
| **Regular** | One-time promotional blast / newsletter to an existing segment of subscribers. | Always `gets_in_segment` (locked, hidden input) — the campaign launches a single send for everyone in the chosen segment at the chosen time. | 5 steps in the editor: title + start delay, choose segment, choose action(s) + message, exit tag, exit condition. |
| **Automated** | Drip sequences, welcome series, abandoned cart recovery, post-purchase upsell, win-back. Continues running on a schedule, enrolling new subscribers as triggers fire. | Merchant-picked from `gets_in_segment` / `gets_out_of_segment` / `makes_an_order` (and `is_in_segment` for some flows). | Same 5 steps + the ability to chain multiple actions with branching conditions and per-step delays. |

### Trigger options exposed in the modern UI

The modern Vue editor's **Trigger** dropdown for Automated campaigns currently exposes only **Gets in segment** (`gets_in_segment`) and **Gets out of segment** (`gets_out_of_segment`). The platform's underlying campaign model also understands `is_in_segment` and `makes_an_order`, but these are used internally by **predefined templates** (see [[campaigns-create-predefined-clone]]) and are not exposed in the picker / editor for merchant-built automations.

## Business rules

### Trigger condition auto-locks for Regular campaigns

When the merchant creates a Regular campaign, the platform's creation hook auto-sets the trigger condition to `gets_in_segment` regardless of what's submitted — so this is not just a UI restriction but a server-side guarantee. A Regular campaign is **always** a one-shot send to a single segment, and the merchant cannot switch a Regular campaign to a different trigger type after creation.

### Shape is permanent

The Regular/Automated choice is fixed at creation. There is no in-editor switch between shapes — to change a campaign's shape the merchant must create a new campaign of the other shape (optionally via [[marketing-campaigns-copy]] once it exists, but copy preserves the shape too).

### Both shapes start as Draft

Clicking **Create campaign** on either tab inserts a Draft (`active=2`) with no title. See [[campaigns-create-draft-business-rules]] for the full create-time behaviour.

## Related

- [[marketing-campaigns-create]] — hub.
- [[marketing-campaigns-edit]] — the 5-step editor both shapes flow into.
- [[marketing-campaigns-from-predefined]] — predefined Automated templates that use the internal-only triggers.
- [[marketing-segments]] — the audience a Regular campaign blasts and an Automated campaign enrolls from.
- [[campaign]] — Campaign entity carrying `type` and `trigger_condition`.

## Open questions

None.
