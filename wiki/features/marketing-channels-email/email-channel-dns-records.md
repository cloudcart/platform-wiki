---
type: feature
nav_path: "Marketing → Channels → Channels setup → Email → DNS records"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Email DNS records", "SPF DKIM Tracking DMARC", "Domain verification", "Tracking CNAME", "Cloudflare auto-CNAME", "Domain.VerifySpf", "Domain.VerifyDkim", "Domain.VerifyDMARC", "Domain.VerifyTracking", "DNS записи за имейл"]
tags: [marketing, channels, email, dns, dkim, spf, dmarc, cloudflare]
plan_gates: ["campaign.channel.email"]
created: 2026-06-10
updated: 2026-06-25
source_count: 4
---

> Part of [[marketing-channels-email]]. See the hub for the other aspects (setup wizard, Elastic Email sub-account, webhook feedback, send pipeline, suspend thresholds, settings pane).

# Email channel — DNS records

## Purpose

Before the Email channel can send any production email, the merchant's chosen sender domain must pass **four DNS checks**: SPF, Tracking CNAME, DKIM, and DMARC. These records prove ownership of the domain, authorise Elastic Email to send mail as that domain, route open / click tracking through the merchant's own hostname, and publish a reporting policy. The Verify step of the setup wizard ([[email-channel-setup-wizard]]) runs all four checks; the channel cannot become `verify = true` until all four pass.

## Where to find it

Setup wizard, **Step 3 — Verify** (`MarketingChannelsEmailConfigurationStep3`). Title: *"Verification for domain '{domain}'"*. Body shows four DNS-record cards; the **Verify** button at the modal footer runs the checks.

The four cards are fetched from `apiMarketingChannels.emailVerification.useQuery` and the Verify action calls `apiMarketingChannels.emailVerifyDomain` (route `GET /email/configuration/verify-domain` on base `/admin/api/core/marketing/campaigns/channels`).

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
| **SPF** | TXT | `@` | `v=spf1 a mx include:_spf.elasticemail.com ~all` | Authorises Elastic Email to send mail as the domain. |
| **Tracking** | CNAME | `tracking` | `api.elasticemail.com` | Routes open / click tracking through the merchant's own domain (looks-like-the-merchant, not a generic redirector). Auto-created on Cloudflare-managed zones. |
| **DKIM** | TXT | `api._domainkey` | `k=rsa;t=s;p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCbmGbQMzYeMvxwtNQoXN0waGYaciuKx8mtMh5czguT4EZlJXuCt6V+l56mmt3t68FEX5JJ0q4ijG71BGoFRkl87uJi7LrQt1ZZmZCvrEII0YO4mp8sDLXC8g1aUAoi8TJgxq2MJqCaMyj5kAm3Fdy2tzftPCV/lbdiJqmBnWKjtwIDAQAB` | Public key receivers use to validate signed headers; prevents spoofing. |
| **DMARC** | TXT | `_dmarc` | `v=DMARC1;p=none;pct=100;rua=mailto:youremailaddress@yourdomain.com;ruf=mailto:youremailaddress@yourdomain.com` | Reporting policy combining SPF + DKIM. |

Each card carries a "Status" badge (inactive until verify-success — Elastic Email re-checks DNS each Verify call).

### Verify-method calls (run sequentially)

| Method | Verifies | Timeout |
|---|---|---|
| `Domain.VerifySpf` | SPF TXT on `@` | 10 s |
| `Domain.VerifyTracking` | CNAME on `tracking` | 10 s |
| `Domain.VerifyDkim` | DKIM TXT on `api._domainkey` | 10 s |
| `Domain.VerifyDMARC` | DMARC TXT on `_dmarc` | 10 s |

## Business rules

### All four must pass — partial verify is not accepted

If ANY of the four `Domain.Verify*` calls returns an error, the platform returns the per-method error message and DOES NOT register the delivery-status webhook. The channel stays at `verify = false`. The merchant fixes the failing record and clicks Verify again.

### Tracking CNAME is auto-created on Cloudflare-managed zones

When the merchant picks a domain whose host row is linked to a Cloudflare-managed zone (`host.cloudflare_zone_id` is set and the zone is active), CloudCart auto-creates the `tracking.{domain}` → `api.elasticemail.com` CNAME via the Cloudflare API. The merchant doesn't have to add it manually. For self-managed DNS, the merchant adds it themselves.

This makes open / click tracking URLs look like `https://tracking.example.com/...` instead of generic Elastic Email URLs — preserving brand consistency. The auto-create call (`createUpdateRecord`) is idempotent — running it twice does not error.

### Cloudflare proxy on the Tracking subdomain: off to verify, on afterwards

The `tracking.{domain}` CNAME interacts with Cloudflare's **proxy** (the orange-cloud toggle), and the two phases want opposite settings:

- **During verification the proxy must be OFF** (DNS-only / grey cloud). With the proxy on, Cloudflare answers DNS for `tracking.{domain}` with its own edge IPs and hides the underlying CNAME, so `Domain.VerifyTracking` can't see it pointing at `api.elasticemail.com` and the check fails.
- **Once verification has passed, turn the proxy back ON** (orange cloud) — this is the recommended end state. Cloudflare then issues a valid SSL certificate for `tracking.{domain}`. If the proxy is left OFF, the subdomain resolves straight to Elastic Email, whose certificate does **not** cover `tracking.{domain}`; so when a tracking link opens over HTTPS the certificate doesn't match and **some browsers warn that the connection is not secure**.

On Cloudflare-managed zones the auto-created CNAME is set **proxied (orange cloud on) by default** — already the recommended end state — so the proxy typically has to be **switched off only temporarily for the verification step**, then switched back on once the channel is verified.

### Domain registration is idempotent

Behind the scenes, the Step 2 → Step 3 transition runs `Domain.EEList` first and skips `Domain.Add` if the domain (or a prefix match with a space — Elastic Email sometimes appends state markers) is already registered. Re-editing the domain therefore does not create duplicates.

### Only after full pass: webhook registration

When all four `Domain.Verify*` calls succeed, the platform then:

1. Sets `verify = true` in settings.
2. Loads existing webhooks via `Account.LoadWebhook` and skips if a webhook with the same URL is already present.
3. Otherwise calls `Account.AddWebhook(url, name="Hook", notify=false, sent=true, opened=true, clicked=true, unsubscribed=true, complaint=true, bounced=true)` — all eight event categories enabled, signed-up notifications disabled.

The webhook URL is `https://{site}/messages/elastic-email-campaign/{site_id}` (HTTPS-only). See [[email-channel-webhook-feedback]] for what arrives at that URL.

### CloudCart subdomains are not eligible

The sender domain must be a domain the merchant owns and has added to [[settings-domains]]. Sending campaigns from `*.cloudcart.com` is forbidden — that would damage CloudCart's shared reputation. The Verify step ensures the merchant proves ownership before any production send.

### Changing the domain after verification

Re-editing the domain via **Edit Domain** wipes `verify`, `email`, `send_email`, and `configured` settings — the merchant must re-verify the new domain. The old domain stays registered on the Elastic Email sub-account (see [[email-channel-elastic-email-account]]) but is no longer the sender.

## Related

- [[marketing-channels-email]] — hub.
- [[email-channel-setup-wizard]] — Step 3 hosts these cards; Step 2 picks the domain.
- [[email-channel-webhook-feedback]] — the webhook that's registered after full pass.
- [[email-channel-elastic-email-account]] — domain lives under the per-store sub-account.
- [[settings-domains]] — where merchant adds the domain to the store first.
- [[settings-domains-dns-cloudflare]] — Cloudflare-managed zones that enable auto-CNAME for the Tracking record.

## Open questions

None.
