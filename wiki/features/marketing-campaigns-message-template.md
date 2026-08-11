---
type: feature
nav_path: "Marketing → Campaigns → Edit → Set message"
route_name: admin.api.campaigns.message-template.create
route_path: /admin/api/core/marketing/campaigns/message/create/{campaign_id}/{action_order}/{type}/{predefined?}
aliases: ["Message editor", "Campaign message editor", "Set message", "Edit campaign message", "Email designer (campaign)", "SMS editor (campaign)", "Viber editor (campaign)", "Web Push editor (campaign)", "Редактор на съобщение", "Шаблон на съобщение"]
tags: [marketing, campaigns, message, template, editor]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-05-23
updated: 2026-06-10
source_count: 2
---

# Campaign message editor

## Purpose

The **campaign message editor** is where the merchant writes / designs the actual content that a campaign step will send to subscribers. It's not a separate page — it's a side-panel that opens when the merchant clicks **Set message** on any delivery step inside [[marketing-campaigns-edit|the campaign editor]]. The editor's shape depends on the step's action type: Email uses the **Unlayer drag-and-drop designer** + an HTML preview iframe; SMS / Viber / Web Push are text-based editors with character counters and per-channel field requirements; transactional helpers (Set tags, Set customer group) don't use this editor — they're configured inline on the step.

The editor lets the merchant compose the message body, choose / save reusable layouts (Email only), insert dynamic variables (customer name, dynamic discount code, store name, etc.), and send a **demo** message to themselves before saving. The merchant can also save the current design as a reusable template (Email only) and pull from saved templates on the next campaign.

This page is the **hub** — it carries the overview + the routing table. Drill into the aspect pages below for the channel-specific UI, the variables catalogue, the per-channel validation rules, and the save / delete persistence.

## Sub-pages (in this cluster)

The editor is split into 7 aspect pages, each one well-scoped. The Assistant should drill into the aspect that matches the question, not read every page.

- [[message-template-email-designer]] — Unlayer drag-and-drop designer flow; the two stacked panels (template picker + scratch designer); custom **Product** block; lazy-loaded Unlayer script.
- [[message-template-channel-variants]] — SMS / Viber / Web Push editor (the channel settings panel wrapping the system-message configuration form); per-channel field shapes; mobile-phone preview; **Write with AI** helper; character-count caps.
- [[message-template-merge-tags]] — variables catalogue (`{$shop.name}`, `{$customer.first_name}`, `{$dynamic_discount_code}`, `{$generate_discount_code:N%}`, `{$triggered_products:N}`, `{$unsubscribe_url}`); the Variables legend pane; click-to-copy.
- [[message-template-saved-and-predefined]] — Email-only library; saved-template payload + link propagation; predefined-template catalog; saved-template edits ripple to linked campaigns.
- [[message-template-demo-send]] — **Send example email** / **Send demo message**; synthetic subscriber substitution; transactional-mail rails; bypasses plan caps + the campaign delivery log; UTM stamping still applies.
- [[message-template-validation]] — two-pass validation (field-level + per-variable); per-channel max-length caps (Email 191/191, Viber 1000/30, Web Push 63/128); required-with trio for Viber; base64 local-image rejection for Email.
- [[message-template-save-flow]] — POST `/admin/api/core/marketing/campaigns/message/create/...`; one saved message per (campaign, step) slot; predefined-campaign JSON path vs the merchant's per-step saved-message path; inline HTML response; hard-delete endpoint.

## Where to find it

Sidebar → **Marketing** → **Campaigns** → open a campaign → in Step 3 (Campaign actions) of [[marketing-campaigns-edit|the editor]], click **Set message** on any delivery step. The side-panel opens with the editor for that step's action type.

The modern Vue admin uses the JSON API (note: `message` is **singular** in these paths):

| Endpoint | Method | Route path | Purpose |
|----------|--------|------------|---------|
| load existing | GET | `/admin/api/core/marketing/campaigns/messages/{campaign_id}/{action_order}/{type}` | Load any previously-saved message for the step (plural `messages` here). |
| save message | POST | `/admin/api/core/marketing/campaigns/message/create/{campaign_id}/{action_order}/{type}/{predefined?}` | Save the message template for the step. |
| demo email | POST | `/admin/api/core/marketing/campaigns/message/demo/email` | Send an example email to the merchant. |
| delete template | POST | `/admin/api/core/marketing/campaigns/message/delete/{id}` | Remove a saved message template from a step. |

The `{type}` segment is the channel action type (`email`, `sms_nth_message`, `sms_msghub_message`, `viber_message`, `web_push`). The `{action_order}` is the step's 0-based order within the campaign. The optional `{predefined}` flag is the predefined campaign ID for CloudCart-staff curating the template catalog; for merchant saves it's `0`. (The legacy sitecp routes live under `/admin/campaigns/message/...`.) Full save / delete mechanics on [[message-template-save-flow]].

## What the merchant can do here

Top-bar actions common across channels: **Cancel**, **Save** (persists against the step), **Send example email** / **Send demo message** (see [[message-template-demo-send]]). Email adds **Save template as default** (library save — see [[message-template-saved-and-predefined]]).

The editor body varies by channel — Email gets the Unlayer designer (see [[message-template-email-designer]]); SMS / Viber / Web Push get the text-first form (see [[message-template-channel-variants]]). Set tags / Set customer group steps don't use the editor at all — they're configured inline on the step in [[marketing-campaigns-edit]].

## Settings & fields

### Required input per channel (summary)

| Channel | Required fields |
|---------|-----------------|
| Email | Subject line, design (Unlayer JSON + HTML output), Send-to (for demo) |
| SMS (NTH) | Message body (counted in 153-char segments, max 6 = 918 chars in the editor; longer = multi-segment SMS), Send-to (for demo) |
| SMS (MsgHub) | Message body, sender ID (channel-level), Send-to (for demo) |
| Viber | Message body (≤ 1000 chars), optional image URL, optional button title + URL (required-with trio), Send-to (for demo) |
| Web Push | Title (≤ 63 chars), Body (≤ 128 chars), optional image URL, optional click URL, Send-to (for demo — test push endpoint) |

Full per-channel rules — including error strings — on [[message-template-validation]]. Per-channel UI on [[message-template-channel-variants]] (text) / [[message-template-email-designer]] (Email).

## Business rules

### Channels with no editor are stepped inline

`set_tags`, `remove_from_campaign`, `remove_from_campaign_and_set_tags`, `set_customer_group` don't use the editor — they're configured inline on the campaign step. The **Set message** button isn't shown for these.

### Channel must be registered

The route 404s if the requested channel type isn't registered, protecting against orphaned action types.

### Variables resolve at SEND time

Variables are stored verbatim — substitution happens inside the per-channel send job. The editor shows `{$variable_name}` as literal strings. Some variables (like `{$dynamic_discount_code}`) require campaign-level setup — see [[message-template-merge-tags]].

### Demos bypass scheduling AND plan caps

Demo endpoint runs synchronously; channel usage counters do NOT increment against the merchant's plan-cap. Full behaviour on [[message-template-demo-send]].

### Predefined-campaign editing path is CloudCart-staff only

When the URL carries `{predefined}`, the editor saves into the predefined campaign's stored template definition instead of the merchant's per-step saved message. Merchants never see this path. See [[message-template-save-flow]].

### Anti-spam policy gate

Merchants without policy acceptance are bounced before the editor opens.

### Saved-template edits propagate to linked campaigns

Linked Email steps see saved-template edits at the next send. Detach by editing + re-saving locally. See [[message-template-saved-and-predefined]].

## Related

- [[marketing-campaigns-edit]] — parent campaign editor; the **Set message** button on each step opens this editor.
- [[marketing-campaigns]] — campaigns hub; Saved Email templates sub-page links to the same library managed here.
- [[marketing-channels-email]] — Email channel internals (Unlayer + Elastic Email).
- [[marketing-channels-sms-msghub]] — SMS MsgHub channel internals.
- [[marketing-channels-sms-nth]] — SMS NTH channel internals.
- [[marketing-channels-viber]] — Viber channel internals.
- [[marketing-channels-webpush]] — Web Push channel internals.
- [[marketing-discounts]] — discounts; the `{$dynamic_discount_code}` and `{$generate_discount_code:N%}` variables require discount configuration.
- [[marketing-segments]] — segments; `{$triggered_products:N}` resolves against segment-matched products.
- [[email-template]] — EmailTemplate entity (saved layouts).
- [[marketing-omnichannel-mails-list]] — customer-mail flow that reuses the Email scratch modal.

## Open questions

None at the hub level — each aspect page tracks its own. See the open-questions sections on [[message-template-saved-and-predefined]], [[message-template-validation]], and [[message-template-save-flow]].
