---
type: feature
nav_path: "Settings → Domains → SSL → Auto-renewal"
route_name: domains.settings
route_path: /admin/settings/domains
aliases: ["SSL auto-renewal", "SSL renewal sweep", "ssl:sites", "renew_error", "Let's Encrypt renewal", "25-day renewal window"]
tags: [settings, ssl, certificate, lets-encrypt, renewal, background]
plan_gates: ["ssl_certificate"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[settings-ssl]]. See the hub for the other aspects (automatic install, manual install, expiry fallback, edge propagation, troubleshooting).

# SSL — Auto-renewal mechanics

## Purpose

For **Let's Encrypt** certificates (`free=1`), the platform sweeps daily and renews any cert within the renewal window. The merchant does NOT need to take action — successful renewals are silent. **Manual certificates (`free=0`) do NOT participate** in this sweep; the merchant must renew them manually before expiry (see [[settings-ssl-manual-install]] and [[settings-ssl-expiry-fallback]]).

This page covers the sweep's timing, the renewal window threshold, what blocks renewal, and how renewal errors surface in the SSL modal.

## Where to find it

There is no merchant-visible renewal-configuration screen — the sweep runs automatically. What the merchant CAN see lives inside the Manage-existing-certificate state of the SSL modal (Sidebar → Settings → **Domains** → SSL action on a domain row):

- The **Renewal** badge — *"Automatic"* (green chip) for Let's Encrypt or *"Manual"* (purple chip) for external.
- The **Expiry date** — `DD.MM.YYYY` format, kept current by successful renewals.
- The **SSL ERROR** banner — red panel with the verbatim `renew_error` text when the last sweep failed.

## What the merchant can do here

### See the renewal status

The Manage state of the SSL modal shows the current renewal mode + expiry. For a successfully-renewing Let's Encrypt cert, the expiry date moves forward by ~90 days after each successful renewal; the merchant typically only notices renewal happening at all when checking the date.

### React to a failed renewal

If the daily sweep fails to renew a cert (DNS broken, ACME challenge can't reach the server, app subscription lapsed, etc.), the error is stored on the cert record as `renew_error` (text) and surfaced in the modal as a red **SSL ERROR** banner with the verbatim error message. The merchant must:

1. Read the error in the banner (see [[settings-ssl-troubleshooting]] for the common messages and what they mean).
2. Fix the underlying issue (e.g., correct DNS in [[settings-domains]], re-purchase the [[apps-lets-encrypt]] app).
3. Wait for the next daily sweep to retry (or contact CloudCart support to trigger an immediate retry — `(verify)` whether merchant-side retry button exists).

### Understand why renewal might not happen

The merchant cannot directly disable the renewal sweep, but it WILL skip a Let's Encrypt cert in these cases:

- The cert is `free=0` (manual / external). The sweep targets only `free=1`.
- The cert is not yet within the **25-day** renewal window (see Business rules).
- The store's billing status is `not_paid` (see Business rules).
- The `lets_encrypt` app's subscription has lapsed.

## Settings & fields

### Manage-state fields relevant to renewal

| Field | What it shows |
|-------|---------------|
| **Source row** | Let's Encrypt logo + *"Managed by [Let's Encrypt Manager]"* (when `free=1`) OR external icon + *"Managed by external provider. You should change it manually before the expiration date."* (when `free=0`). |
| **Expiry date** | `DD.MM.YYYY` — read from the cert's `validTo`, updated on successful renewal. |
| **Renewal** badge | *"Automatic"* (green chip — Let's Encrypt) or *"Manual"* (purple chip — external). |
| **SSL ERROR** banner | Red panel with *"SSL ERROR: {error}"* — shown only when `renew_error` is non-null. Cleared automatically on the next successful renewal. |

There are NO renewal-config inputs on this UI — the sweep's behaviour is platform-wide, not per-store.

## Business rules

### Sweep timing — once per day, single-flighted

The platform-wide renewal job (artisan `ssl:sites`) runs **once per day** (interval 86 400 s, single-flighted on the `cc-system8` queue). It sweeps all candidate Let's Encrypt certs in one pass.

### Renewal window — 25 days, NOT 30

Some older internal docs describe a 30-day renewal window. The actual filter is `valid_to < now + 25 days`. Practical impact:

- A freshly-issued Let's Encrypt cert (Let's Encrypt issues 90-day certs) sits idle for **65 days**, then enters the renewal window.
- If the merchant's DNS breaks mid-life, the SSL ERROR banner shows up no earlier than 25 days before expiry — which still gives the merchant 25 days to fix the underlying issue before the cert actually expires and [[settings-ssl-expiry-fallback]] fires.

### `not_paid` billing status blocks renewal

The sweep filters out certificates for sites whose billing status is `not_paid`. So a merchant whose CloudCart subscription has lapsed will NOT have their Let's Encrypt cert auto-renewed — the cert will expire and the platform's [[settings-ssl-expiry-fallback]] will activate. This is **intentional**: don't keep renewing certs for stores that aren't paying.

Practical implication: a merchant who clears a billing issue late may find their custom domain's storefront has fallen back to the CloudCart subdomain. They will need to manually re-issue the cert via [[settings-ssl-automatic-install]].

### `lets_encrypt` app subscription must be active

In addition to the store-level billing status, the `lets_encrypt` paid app has its OWN subscription. If THAT lapses (e.g., the app's auto-renewal payment failed), the renewal sweep records *"Renew error: no active subscription"* against the cert and does not renew. The merchant must re-purchase the app via [[apps-lets-encrypt]] before the next sweep succeeds.

### `renew_error` is cleared on successful renewal

When a renewal succeeds after previously failing, the new ACME-cert workflow clears `renew_error` (sets to null), the SSL ERROR banner disappears, and the merchant doesn't need to take action. This is helpful when fixing DNS or app-subscription issues: the merchant can repair the underlying cause and wait one day for the next sweep to confirm.

### Common `renew_error` messages

The verbatim strings the merchant may see in the SSL ERROR banner are catalogued in [[settings-ssl-troubleshooting]]. The two most common are:

- *"Header x-powered-by not found for domain X"* — pre-renewal HTTP check can't find a CloudCart-identifying header on either the apex or `www.` variant. DNS isn't pointing at CloudCart anymore.
- *"Renew error: no active subscription"* — the Let's Encrypt Manager app's subscription has lapsed.

### Manual certs are explicitly skipped

The Manage view for a `free=0` (manual) cert shows the purple **Manual** badge plus the *"Managed by external provider. You should change it manually before the expiration date."* line. The renewal sweep does not touch these certs at all. If the merchant forgets to replace before expiry, the platform's daily expired-cert sweep activates instead — see [[settings-ssl-expiry-fallback]].

### Plan downgrade doesn't break in-flight renewals

The `ssl_certificate` plan-feature gate blocks NEW install / replace actions, but it does NOT halt the renewal sweep — existing certs continue auto-renewing on plan downgrade for the contract duration. This is documented on [[settings-ssl]]'s plan-gate note.

### Cert chain push is separate from renewal

A successful renewal updates `validTo` and clears `renew_error`, but the new cert may need to be pushed to Cloudflare's edge and GCloud's LB before HTTPS at the edge reflects the renewal. The `pending` / `gcloud_pending` flags handle this — see [[settings-ssl-edge-propagation]].

## Related

- [[settings-ssl]] — hub.
- [[apps-lets-encrypt]] — the paid app subscription that gates the renewal eligibility check.
- [[settings-ssl-expiry-fallback]] — what happens when renewal fails and the cert actually expires.
- [[settings-ssl-troubleshooting]] — full catalogue of `renew_error` strings.
- [[settings-domains]] — DNS configuration; broken DNS is the single most common renewal-failure cause.

## Open questions

- Does the modal expose a "Retry now" button for the merchant to force-trigger a renewal attempt after fixing DNS, or is the next attempt always gated by the next daily sweep? `(verify)`
