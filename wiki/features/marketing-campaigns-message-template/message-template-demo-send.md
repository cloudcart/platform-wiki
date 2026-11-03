---
type: feature
nav_path: "Marketing → Campaigns → Edit → Set message → Demo send"
route_name: admin.api.campaigns.message-template.demo
route_path: /admin/api/core/marketing/campaigns/message/demo/{type}
aliases: ["Send demo message", "Send example email", "Test send", "Demo email", "Demo SMS", "Demo Viber", "Demo Web Push", "Изпрати тестово съобщение", "Изпрати примерен имейл"]
tags: [marketing, campaigns, message, template, demo, test-send]
plan_gates: ["campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-message-template]]. See the hub for the other aspects (Email designer, channel variants, merge tags, saved + predefined, validation, save flow).

# Campaign message editor — Demo / test send

## Purpose

Every channel editor exposes a **Send demo** (Email: **Send example email**) button so the merchant can preview the rendered message in their own inbox / phone / browser **before** launching the campaign. This aspect documents how demos differ from real campaign sends: they don't queue, don't consume credits, don't write to the campaign delivery log, and use synthetic subscriber data for variable substitution.

## Where to find it

- **Email** — in the Email scratch designer footer: **Send example email** (secondary button). Available whenever the designer is open.
- **SMS / Viber / Web Push** — in the channel message settings panel: a **Send demo message** action against the **Send to** field (a phone number for SMS / Viber, a test push endpoint for Web Push).

## What the merchant can do here

### Trigger a demo

The merchant fills the **Send to** field (or accepts its default — `siteUser.email` for Email) and clicks the demo button. The platform:

1. Validates the message body + variables (same passes as a real save — see [[message-template-validation]]).
2. Posts the message draft to `POST /admin/api/core/marketing/campaigns/message/demo/{type}` (`{type}` = `email` / `sms_nth_message` / `sms_msghub_message` / `viber_message` / `web_push`).
3. The platform builds a synthetic subscriber + synthetic channel record and dispatches a one-off send through the channel's normal send path with a demo flag.
4. On success: toast *":channel message is successfully send to:to"*.
5. On failure: shows the error from the channel (invalid email, insufficient credits, channel suspended, etc.).

### Email demo — `Send example email`

The Email demo:

- Validates the **Send to** address is non-empty (inline error *"Please enter an email address to send the test message to."*).
- Exports the HTML + design from the Unlayer designer.
- Calls `POST /admin/api/core/marketing/campaigns/message/demo/email`.
- On success: toasts the server message (default *"Example email sent."*).
- On error: toasts *"Error sending example email."* OR the server-supplied error.

### Demo destinations per channel

| Channel | Send-to field accepts |
|---------|----------------------|
| Email | Email address |
| SMS (NTH / MsgHub) | Phone number |
| Viber | Phone number |
| Web Push | Test push endpoint (browser-issued endpoint URL) |

### Variable substitution preview

Variables in the message body resolve to placeholder values during demo sends. Full catalogue on [[message-template-merge-tags]]; the most-used substitutions:

| Variable | Demo value |
|----------|------------|
| `{$customer.first_name}` | `FirstName` |
| `{$customer.last_name}` | `LasName` (typo verified — missing second `T`) |
| `{$shop.name}` | The merchant's actual shop name |
| `{$shop.url}` | The merchant's actual shop URL |

The merchant's real customer data is never touched.

## Settings & fields

### Required fields for a demo

| Channel | Send-to | Body | Notes |
|---------|---------|------|-------|
| Email | Required, valid email | Required | Subject + Name also required (same as save validation) |
| SMS | Required, valid phone | Required | Same as save validation |
| Viber | Required, valid phone | Required | Image / button trio rules same as save |
| Web Push | Required, valid push endpoint | Title + Body required | Same caps as save (63 / 128) |

### Demo response shape

The demo endpoint returns JSON `{status: 'success' | 'error', msg: <translated message>, isDemoMessage: true}`. The `isDemoMessage: true` flag is what the front-end uses to render the demo-specific toast styling. On failure (`status: 'error'`), the response carries the exception message — typically a per-channel validation message (invalid email, insufficient credits, etc.).

## Business rules

### Demos bypass scheduling AND plan caps

The demo endpoint runs synchronously, not queued. It builds an in-memory campaign + action + template + synthetic subscriber and routes through the channel's normal send path with a demo flag, so **channel usage counters do NOT increment against the merchant's plan-cap**. Exceptions are recorded and surfaced as toast.

This means the merchant can demo as often as they like without burning their monthly Email / SMS / Viber / Web Push allowance.

### Demo Email uses transactional rails, not campaign rails

The Email demo doesn't dispatch through the campaign send queue. It sends through the platform's transactional mail path instead, using the store's `site_name` and `site_email` settings as the sender identity. This bypasses:

- The campaign credit counter (no plan-cap consumption).
- The campaign delivery log (no delivery-log entry created for the demo).
- The Elastic Email campaign-channel pipeline.

The demo email uses the merchant's transactional `site_email` sender, **not** their verified marketing-from address. So a deliverability quirk that affects marketing sends (DKIM / SPF mismatches, marketing-from reputation) may not show up in demos — and vice versa.

### Demos use synthetic subscriber data

The demo builds a synthetic subscriber (first name `FirstName`, last name `LasName`, country from the store's `country` setting) plus a synthetic channel record for it. Variables resolve against this synthetic record. The merchant's real subscriber list is never touched.

### Tracking URL shortening + UTM stamping still apply

For Email demos, the body's URLs are rewritten to add tracking + UTM tags (a `cc_campaign` tag, a `cc_subscriber` tag, `utm_source = cloudcart`, `utm_medium` = the channel, `utm_campaign` = the campaign title). So clicking a tracked link in the demo redirects through the platform's tracking infrastructure (`cc_campaign` query param) AND carries Google Analytics UTM parameters identifying CloudCart as the source, the channel as the medium, and the campaign title as the UTM campaign. The merchant gets a realistic-looking tracked URL in the test inbox.

### Anti-spam policy gate

The campaign editor (including demos) runs through the campaign anti-spam policy gate — a merchant without policy acceptance is bounced before opening. See [[marketing-campaigns-edit]].

### A demo failing doesn't block save

A failed demo (insufficient credits, invalid recipient, channel suspended) doesn't prevent the merchant from saving the template against the campaign step. Saving requires the template to pass validation; the demo path is purely a preview tool.

### Per-channel toast distinguishes success vs error

The success toast pattern is *":channel message is successfully send to:to"* (e.g., *"Email message is successfully send to: someone@example.com"* — note the small grammar quirk "is successfully send" is verbatim from the platform string). On error, the channel-specific error message is surfaced verbatim.

## Related

- [[marketing-campaigns-message-template]] — hub.
- [[marketing-campaigns-edit]] — parent campaign editor.
- [[message-template-merge-tags]] — variables that get substituted with synthetic data during demos.
- [[message-template-validation]] — same two-pass validation runs before a demo dispatches.
- [[marketing-channels-email]] — Email channel internals; transactional mail facade used for demos.
- [[marketing-channels-sms-msghub]] / [[marketing-channels-sms-nth]] — SMS demo paths.
- [[marketing-channels-viber]] — Viber demo path.
- [[marketing-channels-webpush]] — Web Push demo path.

## Open questions

None.
