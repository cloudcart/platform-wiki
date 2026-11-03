---
type: feature
nav_path: "Marketing → Campaigns → Edit → Set message → Email designer"
route_name: admin.api.campaigns.message-template.create
route_path: /admin/api/core/marketing/campaigns/message/create/{campaign_id}/{action_order}/email/{predefined?}
aliases: ["Email designer", "Unlayer designer", "Campaign email designer", "Email template editor", "Дизайнер на имейл", "Редактор на имейл шаблон"]
tags: [marketing, campaigns, message, template, email, unlayer]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-message-template]]. See the hub for the other aspects (channel variants, merge tags, saved + predefined templates, demo send, validation, save flow).

# Campaign message editor — Email designer (Unlayer)

## Purpose

The Email channel of the campaign message editor is the **only** visual designer in the cluster — SMS / Viber / Web Push are text-first editors. This page documents the Email-specific flow: the two stacked windows (a template picker, then the drag-and-drop email designer), the CloudCart **Product** custom block, and how the same designer serves three save paths (library / campaign / customer mail).

## Where to find it

Sidebar → **Marketing** → **Campaigns** → open a campaign → Step 3 (Campaign actions) → click **Set message** on an Email step in [[marketing-campaigns-edit]]. The picker opens; pick a template (or **Start from scratch**) → the email designer opens.

## What the merchant can do here

### Outer window — template picker

A window titled *"Email template"* with two tabs:

| Tab | Body |
|-----|------|
| **Select template** | Predefined-template catalog (left sidebar = category names, right grid = template thumbnails) |
| **Saved templates** | A table of the merchant's previously-saved templates (Name / Subject / Action columns) |

**Predefined tab** — the left sidebar lists category buttons (the first is always *"All"*; categories with no name are bucketed under *"Others"*, pinned to the top). The right pane shows category-grouped sections of thumbnail cards, each with the template's image (or a fallback icon + name + category). Hovering a card shows a button — *"Start from scratch"* on the blank entry, *"Select template"* on all others. Clicking a category in the sidebar scrolls the right pane to it; scrolling the right pane updates which sidebar category is highlighted.

**Click behaviour:**
- Click **Start from scratch** → opens the designer with a blank canvas.
- Click any other template → opens the designer with that template's design loaded for customisation.

**Saved tab** — a table (no filters, no pagination) with Name / Subject / Action columns and a **Select template** button per row. Clicking it opens the designer in edit mode with that saved template's design, subject, and name loaded; the **Save template** button becomes Update.

**Disabled state** — if the campaign hasn't been saved yet, the body is replaced with the text *"Save the campaign first to set the email template."* plus a **Close** button.

### Inner window — Email designer

A window titled *"Email template"* (or *"Edit template"* when editing a saved one). The footer carries up to five buttons depending on context:

| Button | Visible when | Action |
|--------|--------------|--------|
| **Cancel** | Always | Closes the window |
| **Save template** | Library mode, or not editing a predefined template | Persists the design as a reusable saved template (see [[message-template-saved-and-predefined]]) |
| **Save** (customer mail) | Reached from a customer mail | Updates a customer-mail template — see [[marketing-omnichannel-mails-list]] |
| **Save** (campaign) | Reached from a campaign step | Saves the design against the campaign action and closes both windows |
| **Send example email** | Always | One-off test email — see [[message-template-demo-send]] |

**Form fields above the designer:**

| Field | Help text |
|-------|-----------|
| **Send to** | *"Email address to send the test message to"* |
| **Name** | *"This is the name of the notification"* |
| **Subject** | *"This is the subject that the recipient will see"* |

Validation errors for **Name** and **Subject** render inline.

### Designer pane and Product block

The pane hosts a drag-and-drop email designer (the Unlayer editor, lazy-loaded on first open so it does not slow down the campaign editor itself). It is themed with CloudCart styling and adds one custom block on top of Unlayer's defaults.

**Custom Product block** — the merchant can drag a **Product** block into their email. Its editor exposes:

- **Product source:** *"Selected product"* / *"Triggered products"* / *"Best sellers"*
- **Products per row:** 1 / 2 / 3 / 4

While the designer is loading, the pane shows a spinner and all save buttons stay disabled until it is ready.

### Window-open behaviour

When the designer opens it decides what to show: a customer-mail or campaign template loads its existing design; **Start from scratch** always opens a blank canvas even if the campaign step previously had a message saved; a chosen predefined template always wins over any saved design.

## Settings & fields

| Field | Required | Notes |
|-------|----------|-------|
| Subject | Yes | Max 191 chars; validated on save — see [[message-template-validation]]. |
| Template name | Yes for library save | Max 191 chars. |
| Send to | Yes for demo | Defaults to the current admin's email; pre-filled with the store's `site_email`. |
| Email design | Yes | The drag-and-drop layout, stored as-is for re-editing. |
| Rendered email | Yes | The final HTML sent to recipients; rejects locally-pasted (base64) images — see [[message-template-validation]]. |

## Business rules

### Save happens inside the designer, not the picker

The actual save runs from inside the designer window, which closes both windows on success. The outer picker window's Cancel button just closes it — merchants do not save from the picker.

### Local images are rejected

The Email save rejects any image pasted directly into the body (base64-embedded local images). On match: *"Local image paste has been disabled. Local images have been removed from pasted content."* Local images must instead be uploaded to the media library and referenced by URL. Full per-channel rules live on [[message-template-validation]].

### Email-only — Saved templates exist only for Email

The library / saved-template flow is Email-only. SMS / Viber / Web Push have no saved-template equivalent; their **Set message** screen saves directly against the campaign action without a reusable-layout intermediary. See [[message-template-saved-and-predefined]].

## Related

- [[marketing-campaigns-message-template]] — hub.
- [[marketing-campaigns-edit]] — parent campaign editor; **Set message** spawns this modal pair.
- [[marketing-channels-email]] — Email channel internals (Unlayer + Elastic Email).
- [[marketing-omnichannel-mails-list]] — customer-mail flow that reuses the same scratch modal.

## Open questions

None.
