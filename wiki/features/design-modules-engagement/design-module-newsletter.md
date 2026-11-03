---
type: feature
nav_path: "Design → Modules → Engagement → Newsletter (MailChimp)"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets/newsletter
aliases: ["Newsletter module", "MailChimp newsletter module", "Newsletter popup module", "Mailchimp signup popup", "Newsletter form module", "Модул бюлетин", "Mailchimp бюлетин"]
tags: [design, modules, engagement, newsletter, mailchimp]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Engagement module — newsletter (MailChimp pop-up)

> Part of [[design-modules-engagement]]. See the category page for the other engagement modules.

## Purpose

`newsletter` is the **Mailchimp-backed email-capture surface** on the storefront. The merchant configures a pop-up (and on most themes also an inline footer form using the same instance) that collects a shopper's email and pushes it to the Mailchimp list configured in [[apps-mailchimp]]. The module controls the pop-up's headline, body copy, automatic-open delay, and the initial subscriber status sent to Mailchimp (pending = double opt-in, subscribed = single opt-in).

The module is **gated by the Mailchimp app** — until the merchant has installed [[apps-mailchimp]] AND set a list ID, the panel shows *"Configure app first"* and the storefront pop-up is hidden.

## Where to find it

Sidebar → **Design** → **Modules** → **User** tab → card labelled *"Newsletter (MailChimp)"*.

Clicking the card opens the side panel with the six settings below. When Mailchimp is not installed, the panel renders an empty state with a link to the Mailchimp app installer ([[apps-mailchimp]]).

## What the merchant can do here

- Toggle whether the pop-up renders (`form` — labelled *"Show form"*).
- Decide whether the pop-up opens automatically (`automatic`) — alternative is manual trigger.
- Set the auto-open **delay** in seconds.
- Choose the initial subscriber **status** to send to Mailchimp — pending (double opt-in) or subscribed (single opt-in).
- Edit the pop-up **title** and **description** (TinyMCE rich text).
- Save / Reset / Cancel — standard module controls.

## Settings & fields

| Field | Type | Validation | Default | What it controls |
|-------|------|------------|---------|------------------|
| `enabled` | toggle | `bool` | `true` | Master on/off — when `false`, the module hides the pop-up AND the inline footer form entirely |
| `form` | toggle | `bool` | `false` | Whether the pop-up render at all (label: *"Show form"*); also controls whether themes show the inline footer form |
| `title` | text | `char:0,50` | empty | Pop-up headline (and inline form title) |
| `description` | TinyMCE rich text | `char:0,4096` | empty | Pop-up body copy — e.g., *"Subscribe to get 10% off your first order"* |
| `automatic` | toggle | `bool` | `false` | When ON, the pop-up opens automatically after the delay; when OFF, it requires a manual trigger (theme button) |
| `delay` | number (seconds) | `int:0,300` | `0` | Delay before the pop-up opens (only when `automatic = true`) — max 5 minutes |
| `status` | select | `in:pending,subscribed` | `pending` | Initial subscriber status sent to Mailchimp: **pending** (double opt-in confirmation email) / **subscribed** (single opt-in — added immediately) |

When Mailchimp is **not configured** (the app is disabled OR no list ID is set), the storefront hides the entire pop-up and footer-form markup from the page.

This is a universal module type: every theme that supports newsletter capture ships a `newsletter` instance. Most themes use the SAME settings to drive BOTH a centred modal pop-up AND an inline footer subscribe form. The visual style of the pop-up (centred modal, slide-in, footer banner) is theme-controlled — this module configures content + timing, not visual position.

## Business rules

### Mailchimp app must be configured first

The module is operational only when BOTH of these are true:

1. The Mailchimp app is installed and not disabled, AND
2. A Mailchimp list ID is set (stored under `posts.mailchimp_newsletter_list`).

Without both, the panel shows *"Configure app first"* and the storefront does not render the pop-up. The merchant fixes this in [[apps-mailchimp]].

### `pending` vs `subscribed` status

- `status = pending` — Mailchimp sends a **double opt-in confirmation email**; the subscriber is added only after they click the confirmation link. GDPR-safe default.
- `status = subscribed` — the email is added to the Mailchimp list **immediately**, no confirmation email. Higher capture rate but only legal in jurisdictions that permit single opt-in.

Most merchants should leave this on the default `pending` unless their legal counsel has confirmed single opt-in is permitted in the markets they sell to.

### Single Mailchimp list per store

Every `newsletter` module instance on the merchant's storefront subscribes to the SAME Mailchimp list — the list ID is store-wide, configured once in [[apps-mailchimp]]. There is no per-module list override. Multi-list segmentation requires [[marketing-subscribers-subscribe-forms]] with the [[design-module-cc-form]] embed instead.

### Footer-form rendering

The `form` setting (labelled *"Show form"* in the panel) is a misleading name — it does NOT just control the pop-up; it ALSO governs the inline footer form. When `form = true` AND `enabled = true` AND Mailchimp is configured, themes that render an inline footer subscribe form will show it. When `form = false`, both the pop-up AND the footer form are hidden. Note: the default `form = false` means a fresh install with Mailchimp configured still doesn't show the pop-up until the merchant flips this on.

### Reset wipes everything

Reset restores: `enabled=true`, `form=false`, `title=''`, `description=''`, `automatic=false`, `delay=0`, `status=pending`. The pop-up will not auto-open until the merchant re-configures.

### Submission endpoint

The pop-up form posts to the storefront's `site.newsletter.subscribe` route, which sends the email to Mailchimp in the current locale. Success message: *"You have been successfully subscribed to our newsletter"* (default — translatable per locale). If the email is sent with `status = subscribed`, the confirmation step is skipped.

### Anti-spam

The submit form includes the platform's GDPR consent block (chunked variant in the pop-up, full variant in the inline footer form). reCAPTCHA is NOT applied to this form by default — Mailchimp's own bot detection handles abuse.

### Failed signups show a generic error

When the Mailchimp signup fails, the shopper sees a generic *"Unexpected error"* message in production — the underlying detail (list-mismatch, API-key issue) is not surfaced. A merchant debugging a failed newsletter signup needs developer help to see the real error.

### Uninstalling Mailchimp preserves settings

When the merchant uninstalls the Mailchimp app, the panel re-shows *"Configure app first"* and the pop-up stops rendering, but the saved module settings are preserved — re-installing Mailchimp restores access without re-entering them.

### Rich-text quirk

The pop-up strips line breaks from `description`, so rich-text content with multi-line HTML may render differently in the pop-up vs the inline footer.

## Related

- [[design-modules-engagement]] — hub.
- [[apps-mailchimp]] — install + configure Mailchimp; provides the list ID this module targets.
- [[apps-mailchimp-settings]] — Mailchimp app settings (list ID, API key).
- [[design-module-cc-form]] — sibling; the way to embed a custom multi-page form when this simple pop-up isn't enough.
- [[marketing-subscribers-subscribe-forms]] — alternative subscriber-capture pipeline (multi-list, multi-field, branching).
- [[multi-language]] — per-language `title` / `description` via the `multylang` app.

## Open questions

- 📡 **Mailchimp list ID.** Configured in [[apps-mailchimp]] — stored under `posts.mailchimp_newsletter_list`. GraphQL-resolvable: query the Mailchimp app settings for this merchant's list.
- 📡 **Subscriber status default.** `pending` (double opt-in) is the safer default for GDPR; `subscribed` skips the confirmation email. GraphQL-resolvable: query the module's saved `status` value.
- ⏸️ **reCAPTCHA on newsletter form.** Not applied by default — Mailchimp's bot detection handles abuse. (verify) whether merchants can request reCAPTCHA enablement.
- ⏸️ **Multi-list segmentation.** Not supported by this module — every instance subscribes to the same list. Multi-list flows require [[marketing-subscribers-subscribe-forms]].
