---
type: feature
nav_path: "Marketing → Campaigns → Edit → Set message → Saved + predefined"
route_name: admin.api.campaigns.email-templates.saved
route_path: /admin/api/core/marketing/campaigns/email-templates/saved
aliases: ["Saved email templates", "Predefined templates", "Template library", "Saved layouts", "Запазени шаблони", "Готови шаблони"]
tags: [marketing, campaigns, message, template, library, predefined]
plan_gates: ["campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-message-template]]. See the hub for the other aspects (Email designer, channel variants, merge tags, demo send, validation, save flow).

# Campaign message editor — Saved & predefined templates (Email)

## Purpose

The saved-and-predefined template flow is **Email only** — SMS / Viber / Web Push have no library / catalogue equivalent. This aspect documents two distinct things that share UI in the picker modal:

- **Saved templates** — merchant-authored reusable layouts. The merchant saves a design from the scratch modal, then picks it on later campaigns.
- **Predefined templates** — CloudCart-curated layouts (just designs, not whole campaigns). The merchant picks one and customises it.

Both surface in the same picker modal — see [[message-template-email-designer]] for the picker UI. This page focuses on persistence, saved-template link propagation, and the merchant-facing implications.

## Where to find it

Sidebar → **Marketing** → **Campaigns** → open a campaign → Step 3 → click **Set message** on an Email step → the **Email template** picker opens with two tabs: **Select template** (predefined) and **Saved templates** (merchant's library).

The Saved Email templates are also browsable as a sidebar item under [[marketing-campaigns]] → Saved templates (the same library as the picker's Saved tab).

## What the merchant can do here

### Save a design as a saved template (from the design modal)

In the Email design modal, clicking **Save template** captures the current design plus a screenshot of the rendered HTML to use as a thumbnail, then stores it in the merchant's library. On success the merchant sees *"Template saved successfully."* and the modal closes. If the merchant opened the design from an existing saved template, **Save template** updates that template rather than creating a new one, and the Saved-templates list refreshes.

### Pick a saved template

In the picker's **Saved templates** tab, a table (no filters, no pagination) lists the merchant's templates with columns **Name** / **Subject** / **Action**. Each row has a **Select template** button — click opens the design modal in edit mode, loading that template's design, subject, and name; **Save template** then becomes an update of that saved template.

### Pick a predefined template

In the picker's **Select template** tab, predefined templates are grouped by category (left sidebar) and rendered as 3-column thumbnail grids. A synthetic **Start from scratch** entry sits under *"Others"* at the top. Click any predefined to open the design modal loaded with that layout for customisation.

Predefined templates are **just layouts** — different from predefined campaigns (whole campaign blueprints including actions and segments). Picking a predefined layout replaces the current design; the merchant then customises.

### Saved-template tab on the campaigns hub

Outside the picker, the merchant can manage their saved templates from [[marketing-campaigns]] → Saved templates (sidebar). Edit / rename / delete a saved template propagates to every campaign-action-template row that links to it — see Business rules below.

## Settings & fields

### Saved-template fields

| Field | Notes |
|-------|-------|
| **Name** | Required, max 191 characters. The merchant-facing label in the library. |
| **Subject** | Required, max 191 characters. The Email subject used for sends that load this layout. |
| Design | The full layout, captured from the design modal. |
| Thumbnail | An auto-generated screenshot of the rendered Email, shown in the library. |

### Saved-template link (when a step loads from a saved template)

When a campaign step is built from a saved template, the campaign save (see [[message-template-save-flow]]) records a reference to that saved template so later edits can propagate. The reference is verified at save time — if the referenced template can no longer be loaded, the step is saved without the link (see Business rules).

## Business rules

### Saved-template edits propagate to existing campaigns

When a step is loaded from a saved Email template, the link to that template is preserved. Later edits to the saved template from the Saved templates page update **both** the saved template and any campaign step that still references it, so future sends use the new design.

A merchant who wants a frozen snapshot should detach the link by editing and re-saving the step locally — that creates a template body decoupled from the saved one.

### A broken link is dropped silently

If a step references a saved template that can no longer be loaded (e.g., CloudCart retired that template type), the save skips the link without erroring — the step is saved without a saved-template reference. This protects against orphaned links.

### Predefined template vs predefined campaign — two different things

Two confusable concepts share the word "predefined":

- **Predefined template** — a CloudCart-curated Email layout in the picker's Select template tab. The merchant picks one and customises. Documented here.
- **Predefined campaign** — a whole campaign blueprint (actions + segment + templates) curated by CloudCart staff. This is the CloudCart-staff curation path; merchant campaign saves never use it. See [[message-template-save-flow]].

### Library is Email-only

Only Email has a saved + predefined template library. SMS / Viber / Web Push have no reusable-layout intermediary; their **Set message** modal saves directly against the campaign step.

### Deleting a saved template

Deleting a saved template from the Saved templates page removes it permanently. Campaigns whose steps were built from it keep their own copy of the design, so existing campaigns continue to send the old layout — but reopening that step in the editor shows the design as if authored locally, because the link is gone. (verify)

### Campaign must be saved first

If the campaign hasn't been saved yet, the picker body is replaced with *"Save the campaign first to set the email template."* plus a **Close** button. The merchant can't browse the library against an unsaved campaign — see [[message-template-email-designer]] for the disabled-state UI.

## Related

- [[marketing-campaigns-message-template]] — hub.
- [[marketing-campaigns]] — campaigns hub; Saved templates sub-page links to the same library managed here.
- [[message-template-email-designer]] — the picker + scratch modal UI.
- [[message-template-save-flow]] — campaign-action-template persistence + the link-verification path.
- [[email-template]] — EmailTemplate entity (saved layouts).
- [[marketing-channels-email]] — Email channel internals.

## Open questions

- After a successful **Save template**, does the modal close, or switch to show the just-saved template in the list? Modern admin behaviour unconfirmed.
- Confirm permanent-delete semantics for saved templates and exactly what happens to the linked campaign steps.
