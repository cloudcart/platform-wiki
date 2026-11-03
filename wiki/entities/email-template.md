---
type: entity
aliases: ["Email Template", "Mail template", "Email design", "Email layout", "Saved template", "Имейл шаблон", "Шаблон на имейл"]
tags: [marketing, email, templates, entity]
created: 2026-05-21
updated: 2026-06-10
source_count: 5
---
# Email Template

## Identity

An **Email Template** is a reusable email design — a subject line plus an HTML body (typically authored in the **Unlayer** drag-and-drop visual editor, `CampaignEmailTemplateScratchModal`) plus the merge-tag variables it consumes — that the platform sends to customers or subscribers. Each template stores both the editable Unlayer design (`template_json`) and the rendered HTML output (`message_html`); at send time the per-channel send job substitutes the variables against the recipient's data and dispatches via the configured email channel (typically Elastic Email — see [[marketing-channels-email]]).

The merchant works with **two distinct families** of Email Templates, both edited in the same Unlayer editor but managed in different screens:

1. **Transactional templates** — one per platform event (Order confirmation, Order status changed, Abandoned cart restore link, Welcome, Password reset, Invoice attached, etc.). The label set is **fixed in code** — merchants edit wording and layout, not the set of events. Managed on [[marketing-omnichannel-mails-list]]. Full detail on [[email-template-transactional]].
2. **Campaign templates** — merchant-authored designs used as the message body of a [[campaign|Campaign]] step, authored on [[marketing-campaigns-message-template]], with a reusable **Saved templates** library and a CloudCart-curated **Predefined templates** catalog to clone from. Full detail on [[email-template-campaign-authoring]].

An Email Template is distinct from a **Campaign** itself ([[campaign]]): the Campaign defines the audience, schedule, and step sequence; the Email Template is just the rendered content of one step. It is also distinct from a CloudCart **predefined Campaign** ([[marketing-campaigns-from-predefined]]), which clones an entire pre-wired automation (segment + steps + templates) — not just a layout.

## Sub-pages (in this cluster)

This entity is split into 4 aspect pages. Drill into the one that matches the question rather than reading all four.

- [[email-template-transactional]] — the per-event customer-notification family; fixed label set; per-language `MailLanguage` rows; the `active` flag; the master `customer_email_notifications` toggle that silences every customer-facing transactional email.
- [[email-template-campaign-authoring]] — merchant-authored campaign designs in the Unlayer editor; Saved/Predefined template libraries; save-time validation (local-image-paste rejection, 191-char caps, triggered-products clamp); the Test/Demo send path.
- [[email-template-variables]] — `{$...}` merge tags and encrypted magic URLs (`{$cart_url}`, `{$checkout_url}`, `{$unsubscribe_url}`, `{$verify_url}`, `{$discount_code:CODE}`, `{$triggered_products:N}`); per-template allow-lists.
- [[email-template-delivery]] — Elastic Email channel mechanics: auto-provisioned sub-account credentials, webhook install, delivery-feedback cascades (abuse → campaign removal, hard-bounce → suppression, engagement → verified), Cloudflare tracking CNAME.

## Aliases

- **Email Template** — the canonical merchant-facing term for both families.
- **Mail template** — alternative phrasing, especially around the transactional list (the Vue model is literally `Mail` + `MailLanguage`).
- **Email design** / **Email layout** — informal phrasing in the campaigns editor for the Unlayer artwork.
- **Saved template** — specifically a template the merchant has filed into the reusable library from the campaign editor.
- **Имейл шаблон** / **Шаблон на имейл** — Bulgarian terms used across the marketing area.

## Key Attributes

Shared across both families (family-specific attributes are documented on the aspect pages):

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Type** | Implicit by where it's managed | **Transactional** ([[email-template-transactional]]) or **Campaign** ([[email-template-campaign-authoring]]). The same Unlayer editor handles both. |
| **Name** (`name`) | Free-text | The internal label the merchant sees in the list. Capped at `max:191`. |
| **Subject** (`subject`) | Free-text | The email subject line; may reference merge variables — see [[email-template-variables]]. Capped at `max:191`. |
| **HTML body** (`message_html`) | Edited in the Unlayer editor | The rendered HTML the recipient receives. Stored alongside `template_json` for re-editing. |
| **Design payload** (`template_json`) | Edited in the Unlayer editor | The Unlayer JSON design — opaque to the merchant, used to round-trip the design for further edits. |
| **Variables / merge tags** | Inserted via the editor's variable dropdown | Per-template allow-list. Full catalogue on [[email-template-variables]]. |

Storage: transactional templates live in `mails` + `mails_language`; campaign templates in `campaign_action_templates` (or the merchant's saved-templates table); predefined templates ship as seeded `predefined` rows.

## Where it appears

- [[marketing-omnichannel-mails-list]] — master list of transactional templates (Sidebar → Marketing → Channels → Email notifications); includes the global *Send notifications to customers* toggle.
- [[marketing-campaigns-message-template]] — the campaign Email Template editor (Set message side-panel).
- [[marketing-campaigns]] — campaigns hub; the Saved email templates sub-page lists reusable layouts.
- [[marketing-channels-email]] — the Email channel that delivers templates; Saved templates is exposed as a sub-route here too.
- [[marketing-campaigns-from-predefined]] — picker for predefined CAMPAIGNS (different concept).
- [[settings-invoicing]] / [[orders-invoice]] — the `send_invoice` transactional template emailed with the invoice PDF.

## Related

- [[campaign]] — Email Templates power the message body of email-channel campaign steps.
- [[notification-delivery]] — the platform-wide notification pipeline that routes templates through the configured email channel.
- [[marketing-channels-email]] — Elastic Email integration that delivers the rendered template — see [[email-template-delivery]] for the channel mechanics.
- [[order]] — many transactional templates fire on Order events; they reference the order via merge variables.
- [[customer]] — the recipient of most transactional templates.
- [[subscriber]] — the recipient of campaign templates (and of `abandoned_restore_link` when the leaver is a subscriber rather than a registered customer).
- [[cart]] — the source object for the `abandoned_restore_link` template.
- [[discount]] — campaign templates can include dynamic-discount-code variables — see [[email-template-variables]].
- [[segment]] — segment-bound variables resolve against the campaign's segment.
- [[marketing-discounts]] — discount setup required when a template uses dynamic-discount-code variables.
- [[marketing-campaigns-policy]] — anti-spam policy gate that applies to campaign sends (but NOT to transactional sends).
- [[checkout-flow]] — produces the order-related events that fire transactional templates.
- [[abandoned-cart-recovery]] — concept that the `abandoned_restore_link` template powers.

## Open Questions

None at the hub level — see the aspect pages ([[email-template-transactional]], [[email-template-campaign-authoring]], [[email-template-variables]]) for their open items.
