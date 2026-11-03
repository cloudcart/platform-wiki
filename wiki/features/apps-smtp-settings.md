---
type: feature
nav_path: "Apps → SMTP → Settings"
route_name: apps.smtp.settings
route_path: /admin/apps/smtp/settings
aliases: ["SMTP Settings", "Custom mail server config"]
tags: [apps, administration, smtp, email, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 1
---
# SMTP → Settings

## Purpose

The **Settings** tab is where the merchant configures their **custom SMTP server credentials** for outbound transactional emails. See [[apps-smtp]] for the full feature set.

## Where to find it

Sidebar → Apps → SMTP → **Settings tab**. Route: `/admin/apps/smtp/settings`.

## What the merchant can do here

### Server credentials — the only configurable fields

The SMTP app exposes five fields and nothing more:

| Field | Notes |
|---|---|
| **Hostname** (`host`) | SMTP server hostname (e.g., smtp.gmail.com, smtp.sendgrid.net, smtp.mailgun.org). Required when active. |
| **Port** (`port`) | 0–65535. Default `25`. Standard values: 587 (TLS/STARTTLS), 465 (SSL), 25 (unencrypted). Required when active. |
| **Username** (`username`) | Account username (typically the email address). Required when active. |
| **Password** (`password`) | Account password / app-specific password. Required when active. |
| **Encryption** (`encryption`) | Select: `NONE` / `SSL` / `TLS/STARTTLS`. Default `none`. |

There is NO **From address**, **From name**, or **Reply-to** field on this page — the From/Reply-to headers come from the merchant's email-configuration in [[settings-emails]] / per-template settings, not the SMTP credentials.

There is NO **Test email** button — the connection is validated automatically on save by opening a live SMTP session against the server (see Validation below).

### Validation on save — live SMTP handshake

When the merchant clicks Save with `active = 1`, the platform attempts a real connection to the configured server (`host` + `port`, optionally TLS when `encryption ≠ none`) and runs a `NOOP` command. If the handshake fails, the save is rejected with the validation message *"Failed to connect to SMTP server."* on the Hostname field. This effectively replaces a manual test-send button — the merchant cannot save bad credentials.

### What the merchant CANNOT do here
- Receive emails (outbound only — inbound goes to the merchant's actual mailbox).
- Send without valid DNS records (SPF / DKIM / DMARC) at their domain for deliverability.
- Configure multiple SMTP servers / failover — only ONE server can be set at a time.
- Set rate limits or bounce-handling rules — the platform sends one-by-one; deliverability and bounce-handling are entirely up to the configured SMTP provider.
- Override the From / Reply-to / sender name from this page.
- Trigger a manual test email — connection is validated automatically on save.

## Settings & fields

The configured check requires all five fields (`host`, `port`, `username`, `password`, `encryption`) to be set. Validation messages — exact text:

| Trigger | Message |
|---|---|
| Hostname missing while active | *"Hostname is required"* |
| Port missing while active | *"Port is required"* |
| Port not numeric | *"Port must be a number"* |
| Port < 0 | *"Port cannot be less than 0"* |
| Port > 65535 | *"Port cannot be greater than 65535"* |
| Username missing while active | *"Username is required"* |
| Password missing while active | *"Password is required"* |
| Connection handshake fails | *"Failed to connect to SMTP server."* |

## Business rules

### Deliverability requires DNS

For best deliverability, the merchant configures at their domain provider:
- **SPF** record authorising the SMTP server.
- **DKIM** signature from the SMTP provider.
- **DMARC** policy.

CloudCart only routes through the configured server; the DNS work is the merchant's responsibility.

### Encryption recommended

TLS (port 587) is the modern standard. SSL (port 465) is legacy but still supported. None (port 25) is unencrypted and rarely allowed by SMTP providers.

### Single SMTP server — no failover

The app stores ONE set of credentials. If the configured server is unreachable, outbound mails fail individually — there is no built-in failover to a backup server. Merchants who need redundancy should configure their SMTP provider to handle failover on its side.

### Rate-limit handling — none built in

CloudCart sends emails one at a time as triggers fire. If the SMTP provider throttles or rejects the send (e.g., per-hour cap), each affected email logs its provider error message — but there is no automatic retry queue or rate-limit smoothing inside the SMTP app. The merchant should pick a provider whose per-account limits comfortably exceed the store's outbound volume.

### Bounce / complaint handling — entirely provider-side

CloudCart does NOT pull bounce or complaint reports from the SMTP provider. If a recipient marks the merchant's mail as spam or the address bounces, that signal lives only in the SMTP provider's dashboard. The merchant monitors and cleans their audience there.

### Permission
Standard apps permission scope.

## Related

- [[apps-smtp]] — hub.
- [[apps-google-workspace]] — Google-specific outbound email alternative.
- [[settings-domains]] — sender domain DNS configuration.

## Open questions

All previously-flagged questions resolved. See body sections.
