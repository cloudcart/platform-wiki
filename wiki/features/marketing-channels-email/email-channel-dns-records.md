---
type: feature
nav_path: "Marketing → Channels → Channels setup → Email → DNS records"
route_name: campaigns-channels
route_path: /admin/marketing/campaigns/channels
aliases: ["Email DNS records", "SPF DKIM Tracking DMARC", "Domain verification", "Tracking CNAME", "Cloudflare auto-CNAME", "Domain.VerifySpf", "Domain.VerifyDkim", "Domain.VerifyDMARC", "Domain.VerifyTracking", "Valid DKIM not found", "No valid tracking domain found", "Proxied tracking CNAME", "DNS записи за имейл", "DKIM запис"]
tags: [marketing, channels, email, dns, dkim, spf, dmarc, cloudflare]
plan_gates: ["campaign.channel.email"]
created: 2026-06-10
updated: 2026-11-09
source_count: 5
---

> Part of [[marketing-channels-email]]. See the hub for the other aspects (setup wizard, Elastic Email sub-account, webhook feedback, send pipeline, suspend thresholds, settings pane).

# Email channel — DNS records

## Purpose

Before the Email channel can send campaigns, the merchant's chosen sender domain must pass **four DNS checks**: SPF, Tracking CNAME, DKIM, and DMARC. These records prove ownership of the domain, authorise Elastic Email to send mail as that domain, route open / click tracking through the merchant's own hostname, and publish a reporting policy. The Verify step of the setup wizard ([[email-channel-setup-wizard]]) runs all four checks; the channel cannot become `verify = true` until all four pass.

## Where to find it

Setup wizard, **Step 3 — Verify** (`MarketingChannelsEmailConfigurationStep3`). Title: *Verification for domain "{domain}"*. Body shows four DNS-record cards (*"SPF Record"*, *"Tracking CNAME"*, *"DKIM Record"*, *"DMARC Record"*); the **Verify** button at the modal footer runs the checks.

The Verify action calls `GET /email/configuration/verify-domain` on base `/admin/api/core/marketing/campaigns/channels`.

## What the merchant can do here

- Read the four required DNS records and their per-record values.
- Copy each record's value to clipboard with one click (toast: *"Copied to clipboard"*).
- Add the four records at their DNS provider (or rely on auto-CNAME for the Tracking record on Cloudflare zones — see below).
- Click **Verify** to re-run all four checks against Elastic Email.
- Click **Change Domain** to return to Step 2 without losing profile data.

## Settings & fields

### Domain DNS records — the four required entries

| Record | Type | Host | Value (illustrative) | What it does |
|--------|------|------|----------------------|---------------|
| **SPF** | TXT | `@` | `v=spf1 a mx include:_spf.elasticemail.com ~all` | Authorises Elastic Email to send mail as the domain. Only one SPF record may exist, so merge the include into an existing SPF. |
| **Tracking** | CNAME | `tracking` | `api.elasticemail.com` | Routes open / click tracking through the merchant's own domain (looks-like-the-merchant, not a generic redirector). Auto-created on Cloudflare-managed zones. |
| **DKIM** | TXT | `api._domainkey` | The value shown on the **DKIM Record** card, unique to the domain | Public key receivers use to validate signed headers; prevents spoofing. |
| **DMARC** | TXT | `_dmarc` | `v=DMARC1;p=none;pct=100;rua=mailto:<store email>;ruf=mailto:<store email>` (pre-filled with the store's email) | Reporting policy combining SPF + DKIM. |

Each card carries a "Status" badge. After **Verify**, a failed card shows *"Not verified"* and a *"Verification status"* row with Elastic Email's own wording; a passing one shows *"Verified successfully"*.

### Verify-method calls (run sequentially)

| Method | Verifies | Timeout |
|---|---|---|
| `Domain.VerifySpf` | SPF TXT on `@` | 10 s |
| `Domain.VerifyTracking` | CNAME on `tracking` | 10 s |
| `Domain.VerifyDkim` | DKIM TXT on `api._domainkey` | 10 s |
| `Domain.VerifyDMARC` | DMARC TXT on `_dmarc` | 10 s |

## Business rules

### All four must pass — partial verify is not accepted

If ANY of the four `Domain.Verify*` calls returns an error, the platform returns the per-method error message and DOES NOT register the delivery-status webhook. None is warn-only. The channel stays at `verify = false`. The merchant fixes the failing record and clicks Verify again.

Only the overall `verify` flag is stored, never each check's result, and the checks are never re-run after verification passes, so DNS that breaks later is not noticed by the platform. Existing SPF or DMARC records on the domain, how soon **Verify** sees a new record, and what removing the records or moving the DNS does are on [[email-channel-dns-changes]].

### The DKIM value is the domain's own

Elastic Email issues a separate 2048-bit key when a domain is added to the store's sub-account and accepts only that key, so copy the value from the **DKIM Record** card. A record with another value fails with *"Valid DKIM not found"*. For a domain with no key from Elastic Email (older domains, a service error), or a store with no sub-account yet, the card shows an older shared value.

Since early October 2026, a domain that has its own key rejects the old shared value with *"Valid DKIM not found"*. A store stuck there must **replace** the TXT at `api._domainkey` with the value on the **DKIM Record** card. A store that verified earlier with the old value keeps its verified state.

### Tracking CNAME is auto-created on Cloudflare-managed zones

When the merchant picks a domain whose host row is linked to a Cloudflare-managed zone (`host.cloudflare_zone_id` is set and the zone is active), CloudCart auto-creates the `tracking.{domain}` → `api.elasticemail.com` CNAME via the Cloudflare API. It creates **only** this record: SPF, DKIM and DMARC are not created for the channel, so the merchant adds them (and, for self-managed DNS, the CNAME too).

Tracking links then use `https://tracking.example.com/...` instead of generic Elastic Email URLs.

### The Tracking CNAME must not be proxied

The `tracking.{domain}` CNAME must stay **DNS-only** (grey cloud). With Cloudflare's proxy (orange cloud) on, Cloudflare answers DNS for `tracking.{domain}` with its own edge IPs and hides the CNAME, so the tracking check fails (*"No valid tracking domain found"*) and verification is blocked.

- Since late August 2026 the platform creates the record **unproxied**.
- An existing proxied record is reset to unproxied only when the domain is saved in Step 2 (re-saving the same domain via **Change Domain** counts), or when DNS is changed under Settings → Domains for an already-configured channel. Clicking **Verify** alone does not fix it.
- A CNAME the merchant adds by hand in the store's DNS management defaults to **proxied**, so the proxy must be switched off on it.

### Domain registration is idempotent

Saving Step 2 skips registering a domain that is already on the sub-account, so re-editing the domain creates no duplicates.

### Only after full pass: webhook registration

When all four `Domain.Verify*` calls succeed, the platform then:

1. Sets `verify = true` in settings.
2. Loads existing webhooks via `Account.LoadWebhook` and skips if a webhook with the same URL is already present.
3. Otherwise calls `Account.AddWebhook(url, name="Hook", notify=false, sent=true, opened=true, clicked=true, unsubscribed=true, complaint=true, bounced=true)` — all eight event categories enabled, signed-up notifications disabled.

The webhook URL is `https://{site}/messages/elastic-email-campaign/{site_id}` (HTTPS-only). See [[email-channel-webhook-feedback]] for what arrives at that URL.

### The store's `*.cloudcart.net` address can't be verified

The Step 2 list holds every domain of the store in [[settings-domains]], including its `*.cloudcart.net` address. CloudCart runs no check of its own on the choice: Elastic Email accepts or rejects the domain, and its message shows under the **Domain** field. The `*.cloudcart.net` address has no DNS zone the store can edit, so its records can't be added and Verify can't pass. The sender domain is in practice one the merchant owns.

### Changing the domain after verification

In the current admin, re-saving or changing the domain via **Edit Domain** only overwrites the domain: verification is **not** re-run and the sender address is **not** changed. (An older admin screen wiped the verify, email, sender and configured settings.) The old domain stays registered on the Elastic Email sub-account (see [[email-channel-elastic-email-account]]).

## Related

- [[marketing-channels-email]] — hub.
- [[email-channel-setup-wizard]] — Step 3 hosts these cards; Step 2 picks the domain.
- [[email-channel-webhook-feedback]] — the webhook that's registered after full pass.
- [[email-channel-elastic-email-account]] — domain lives under the per-store sub-account.
- [[settings-domains]] — where merchant adds the domain to the store first.
- [[settings-domains-dns-cloudflare]] — Cloudflare-managed zones that enable auto-CNAME for the Tracking record.
- [[email-channel-dns-changes]] — existing SPF / DMARC records, Verify timing, records removed or DNS moved.

## Open questions

None.
