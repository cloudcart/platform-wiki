---
type: entity
aliases: ["Campaign email template", "Saved template", "Email design", "Email layout", "Unlayer editor", "Predefined template", "Шаблон за кампания"]
tags: [marketing, email, templates, campaigns, unlayer, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[email-template]]. See the hub for the other aspects (transactional family, merge variables, channel delivery).

# Email Template — campaign authoring

## Identity

A **campaign Email Template** is a merchant-authored email design used as the message body of one step of a [[campaign|Campaign]]. Unlike the [[email-template-transactional|transactional family]] (where labels are fixed in code), campaign templates are free-form: the merchant designs the artwork in the **Unlayer** drag-and-drop visual editor (`CampaignEmailTemplateScratchModal`) on [[marketing-campaigns-message-template]] — the **Set message** side-panel inside the campaign editor.

Two reuse mechanisms layer on top:

- **Saved templates** — when the merchant clicks **Save template** in the campaign editor, the layout is filed into a reusable **Saved templates** library so it can be re-applied across campaigns. A `html2canvas` screenshot of the rendered HTML is auto-generated as the picker thumbnail.
- **Predefined templates** — CloudCart ships a curated catalog of starter layouts (separate from predefined campaigns). The merchant can clone one as a starting point. The authoring side of the catalog is an internal CloudCart-staff flow (see Key Attributes) — merchants only consume it.

A campaign template is distinct from a CloudCart **predefined Campaign** ([[marketing-campaigns-from-predefined]]), which clones an entire pre-wired automation (segment + steps + templates) — not just a layout.

## Aliases

- **Campaign email template** — the canonical term for the merchant-authored family.
- **Saved template** — specifically a template the merchant has filed into the reusable library.
- **Email design** / **Email layout** — informal phrasing in the campaigns editor referring to the Unlayer artwork.
- **Шаблон за кампания** — Bulgarian phrasing.

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Name** (`name`) | Free-text | The internal label (e.g., *"Black Friday teaser v2"*). Enforced at `required\|max:191`. |
| **Subject** (`subject`) | Free-text | The email subject line; may reference merge variables — see [[email-template-variables]]. Enforced at `required\|max:191`. |
| **HTML body** (`message_html`) | Edited in the Unlayer visual editor | The rendered HTML the recipient receives. Stored alongside `template_json`. |
| **Design payload** (`template_json`) | Edited in the Unlayer visual editor | The Unlayer JSON design — opaque to the merchant, used by the editor to round-trip the design for further edits. |
| **Saved-template ID** | Set on **Save template** | Links the campaign step's template back to the merchant's saved-templates library so future opens load the saved layout. |
| **Thumbnail** | Auto-generated on save | A `html2canvas` screenshot of the rendered HTML, used as the preview thumbnail in the saved-templates picker. |
| **Predefined-template flag** | Set internally when CloudCart staff curate the catalog | When edited via the `{predefined}` URL param, the template saves to `predefined.data.templates` instead of the merchant's `campaign_action_templates` table. Merchants never see this flow — it's an internal authoring path for the curated catalog. |

Campaign templates are stored in `campaign_action_templates` (or, for saved layouts, in the merchant's saved-templates table). Predefined templates ship as seeded data inside `predefined` rows.

### Validation enforced on save

| Rule | What happens |
|------|--------------|
| **Local image paste rejected** | The campaign template validator rejects any `data:image/{type};base64` substring with the message *"Local image paste has been disabled. Local images have been removed from pasted content."* — keeps the email payload small and forces image-gallery uploads. Applies on save, before storage. |
| **`name` and `subject` capped at 191 chars** | Both fields enforced at `required\|max:191`. The merchant sees a validation toast if they exceed the cap. |
| **Triggered-products limit clamped to max 12** | The `{$triggered_products:N}` placeholder accepts N from 1 to 12 — any larger requested count is silently clamped to 12 (`triggerProductsLimit` override). Full variable behaviour on [[email-template-variables]]. |

### Test / Demo send uses a different pipeline

Test/Demo sends from the campaign editor route through the platform's transactional `MailManager` — NOT the merchant's Elastic Email sub-account. So demo sends:

- don't count against the plan-cap,
- don't appear in the channel log,
- use the platform's primary mail sender (not the merchant's verified `send_email`).

This is why a test send can succeed while a real campaign send is blocked by the channel — the two go through different infrastructure. The real-send path and its channel mechanics are documented on [[email-template-delivery]].

## Where it appears

- [[marketing-campaigns-message-template]] — the campaign Email Template editor (the **Set message** side-panel inside the campaign editor).
- [[marketing-campaigns]] — the campaigns hub; the **Saved email templates** sub-page lists the merchant's reusable layouts.
- [[marketing-channels-email]] — the Email channel setup; **Saved templates** is exposed as a sub-route here too.
- [[marketing-campaigns-from-predefined]] — picker for predefined CAMPAIGNS (different concept — clones a whole automation including its templates).

## Related

- [[email-template]] — hub.
- [[campaign]] — campaign templates power the message body of email-channel campaign steps.
- [[segment]] — segment-bound variables (e.g., `{$triggered_products:N}`) resolve against the campaign's segment — see [[email-template-variables]].
- [[discount]] — campaign templates can include dynamic-discount-code variables that reference [[marketing-discounts]] setup.
- [[marketing-discounts]] — discount setup required when a template uses dynamic-discount-code variables.
- [[marketing-campaigns-policy]] — anti-spam policy gate that applies to campaign sends (but NOT to transactional sends).
- [[subscriber]] — the recipient of campaign templates.

## Open Questions

- ⏸️ Whether editing a saved campaign Email Template after a campaign has been started propagates to in-flight sends or only affects future sends (i.e., is each campaign step a snapshot of the template at start, or a live reference?).
