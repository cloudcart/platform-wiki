---
type: feature
nav_path: "Apps → SMTP"
route_name: apps.smtp.overview
route_path: /admin/apps/smtp
aliases: ["SMTP", "Custom SMTP", "Mail server", "Email sending", "enable disable button", "app active toggle"]
tags: [apps, administration, email, infrastructure, deliverability]
plan_gates: ["smtp"]
created: 2026-05-22
updated: 2026-08-06
source_count: 1
---
# SMTP (custom email sending)

## Purpose

**SMTP** integration — routes the store's outbound emails through the merchant's **own SMTP server** (Gmail, SendGrid, Amazon SES, Postmark, Mailgun, custom IMAP host, etc.). Used to:

- Send from the merchant's custom domain email (`info@merchant.com` instead of CloudCart's default).
- Improve deliverability (use a paid sending service with proper SPF/DKIM/DMARC).
- Comply with corporate email policies (route through company server).

Alternative to [[apps-google-workspace]] (Google's SMTP) for merchants on non-Google email infrastructure.

> **Has an on/off control.** The app screen carries an **Enable / Disable** button, so the merchant can switch it off without uninstalling it. A disabled app stops working while keeping its settings — so *"the app is disabled"* IS a valid explanation to check here.

## Where to find it

Sidebar → Apps → install → **SMTP**. See [[apps-smtp-settings]] for configuration.

## What the merchant can do here

- Configure SMTP credentials: host, port, username, password, encryption (TLS / SSL / none).
- Set sender address + display name.
- Test sending (Test Email button typically).

### What the merchant CANNOT do here
- Receive emails (outbound only).
- Use without valid SMTP credentials.

## Settings & fields

Manager exposes:
- the configured check — credential validity check.

Typical SMTP fields:
- **Host** (e.g., smtp.gmail.com, smtp.sendgrid.net).
- **Port** (587 for TLS, 465 for SSL, 25 for unencrypted).
- **Username** + **Password**.
- **Encryption** (TLS / SSL / None).
- **From address** + **From name**.

## Business rules

### Outbound only

The integration handles outbound transactional emails (order confirmations, password resets, etc.). Inbound (customer replies) goes to the merchant's actual mailbox — CloudCart doesn't fetch.

### Per-domain deliverability prerequisites

For best deliverability:
- SPF record at the merchant's domain authorising the SMTP server.
- DKIM signature (from the SMTP provider).
- DMARC policy.

The merchant configures DNS at their domain provider, not in CloudCart. CloudCart just routes through the configured server.

### Permission

Standard apps permission scope.

## Plan gates

This app is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `smtp` | Access gate (install URL) | The install URL `/admin/apps/smtp/install` is blocked when the plan lacks the feature. The app is hidden from the Apps catalog for those plans. |

Behaviour: lower plans cannot install the app. Existing installs continue working on plan downgrade until the merchant cancels — see [[plan-vs-feature-pack]] for downgrade rules.

## Related

- [[apps]] — App Store.
- [[apps-smtp-settings]] — settings sub-page.
- [[apps-google-workspace]] — alternative Google-specific SMTP integration.
- [[settings-domains]] — sender domain DNS configuration.
- [[marketing-campaigns]] — campaign emails (may use SMTP OR external services like Mailgun separately).

## How it works (verified against backend)

### Required settings (5 fields)

The integration requires ALL FIVE settings:
- `host` — SMTP server hostname.
- `port` — typically 587 (TLS) / 465 (SSL).
- `username` — SMTP account username.
- `password` — SMTP password.
- `encryption` — TLS / SSL / null.

All 5 must be non-empty for the integration to be considered configured. Missing any leaves the integration inactive — system falls back to default mail transport.

### Single-server design

The Manager is intentionally MINIMAL — just credentials + isConfigured check. No multi-server fallback, no rate-limit tracking, no test-send method exposed. SMTP integration is purely a transport-replacement: the platform uses this SMTP server INSTEAD of the default mail transport for all outbound emails.

### Live connection test before save

The settings form does **not** rely on the merchant to "test" their SMTP credentials separately. Saving the form runs a live SMTP handshake against the configured host / port / username / password / encryption via the platform code. If the server refuses the connection, the save is rejected with *"Failed to connect to SMTP server."* and no setting is persisted.

So the merchant gets immediate feedback the moment they save — there is no follow-up "Send test email" button needed for credential verification.

### Port and encryption validation

The `port` field is validated as an integer in the range **0–65535** with messages *"Port is required"*, *"Port must be a number"*, *"Port cannot be less than 0"*, *"Port cannot be greater than 65535"*. The encryption setting accepts plain values; the validator treats anything other than `none` as TLS-on. Default port is **25**, default encryption is **none** — the merchant must usually override both (587 + TLS or 465 + SSL) for common providers.

### Single-server only — no fallback, no rate-limit tracking

The Manager stores exactly one set of credentials and one host. The platform does not allow a primary + secondary SMTP server, does not track outgoing email rate limits, and does not throttle sends based on the provider's published per-hour caps. If the merchant's SMTP provider rate-limits, the merchant sees those emails fail at delivery time without an in-app warning.

### Outbound only — no inbound parsing

Customer replies to platform emails land in whatever inbox the merchant's `From` address points to (typically their mail provider's mailbox). CloudCart does not connect IMAP / POP to read replies. Order-related replies are managed in the merchant's own mail client.

### Per-store SMTP

The credentials are stored per CloudCart site (each store's settings are independent). Multi-store merchants configure SMTP separately on each store. There is no shared / inherited SMTP credential across multiple stores.

### Bounce and complaint handling

The app does not implement bounce or complaint feedback loops. If a delivery bounces, the SMTP server returns the bounce to the configured `From` address (the merchant sees it in their mailbox). To track aggregated bounces / spam complaints, the merchant uses their SMTP provider's own dashboard (SendGrid, Postmark, etc.) — the data is not pulled back into CloudCart.

### Send-test destination

Beyond the connection ping on save, the app does not include a "Send a test email to address X" button. To verify end-to-end delivery, the merchant places a real order on the store and confirms the order-confirmation email arrives. This is a known limitation — there is no separate send-test UI.

## Open questions

