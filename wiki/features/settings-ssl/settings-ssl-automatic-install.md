---
type: feature
nav_path: "Settings → Domains → SSL → Automatic install"
route_name: domains.settings
route_path: /admin/settings/domains
aliases: ["Let's Encrypt install", "SSL automatic install", "Free SSL install", "ACME issuance", "Auto SSL"]
tags: [settings, ssl, certificate, lets-encrypt, acme]
plan_gates: ["ssl_certificate"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[settings-ssl]]. See the hub for the other aspects (manual install, auto-renewal, expiry fallback, edge propagation, troubleshooting).

# SSL — Automatic install (Let's Encrypt)

## Purpose

The **Automatic install** tab of the SSL Modal issues a **free Let's Encrypt** certificate for the selected domain. After install, the certificate is auto-renewed by the platform's daily sweep with no merchant intervention — see [[settings-ssl-auto-renewal]]. This is the recommended path for most merchants.

The flow is one-click from the merchant's side, but requires the **Let's Encrypt Manager** paid app installed first — see [[apps-lets-encrypt]].

## Where to find it

Sidebar → Settings → **Domains** → SSL action on a domain row → **Automatic install** tab.

The tab is only enabled when no certificate is already installed on the domain. If a manual external cert exists, the merchant is told to remove it first.

## What the merchant can do here

### Trigger Let's Encrypt issuance

1. Click the **SSL** action on a domain row in [[settings-domains]].
2. In the modal, ensure the **Automatic install** tab is active (it is the default for empty-cert domains).
3. Confirm the **Common Name (CN)** field shows the correct domain hostname (read-only).
4. Click **Automatic install** (primary button).
5. The platform calls Let's Encrypt's ACME service, generates a CSR, performs HTTP-01 verification, and installs the issued certificate.
6. On success, the modal flips to **Manage existing certificate** state showing the new cert with the green **Automatic** renewal badge.

### Install the Let's Encrypt Manager app first

If the `lets_encrypt` app is not installed and/or not paid, the tab shows a **Required-app card** instead of the install button:

- *"To use this method, please install the following apps:"* + the Let's Encrypt Manager logo + name.
- **Install app** button (when the app is paid but not installed) OR **Buy for {price}** button (when the app needs purchase).
- Clicking **Buy for {price}** sets `checkout = true` on the modal — the modal morphs to size `xll` and embeds the standard app-purchase checkout panel inline. After successful purchase, the modal returns to the Automatic install tab with the **Automatic install** button now enabled.

### Remove an existing manual cert first (if any)

If a manual external cert (`free=0`) is already installed, the Automatic tab shows:

- A warning panel: *"To make automatic install, first you need to remove the certificate from the manual install"*.
- A **Remove** danger button below the warning.

The merchant must click **Remove** (and confirm the *"Are you sure you want to remove it?"* dialog) before the **Automatic install** button activates.

## Settings & fields

| Field | What it does | Source |
|-------|--------------|--------|
| **Common Name (CN)** | Read-only — the domain hostname being issued for. | Domain row |
| **Automatic install** button | Primary button. Triggers Let's Encrypt issuance. | (action) |
| **Required app card** | Shows Let's Encrypt Manager app with **Install app** or **Buy for {price}**. | (`lets_encrypt` app state) |
| **External-cert collision warning** | *"To make automatic install, first you need to remove the certificate from the manual install"* | (shown when `free=0` cert exists) |
| **Remove** button (under the warning) | Danger-styled; clears the existing manual cert. | (action) |

### When the **Automatic install** button is disabled

- The Let's Encrypt Manager app is not installed (`!app.is_installed`).
- The Let's Encrypt Manager app is not paid (`!app.paid`).
- A submit is already in flight (`autoInstallLoader`).
- A `free=0` cert exists and hasn't been removed yet.

## Business rules

### Issuance covers apex AND `www.` together

The issuance helper hits both `<host>` and `www.<host>` and the resulting cert's SAN covers BOTH variants. Merchants who manage their own A / CNAME records should ensure **both** the apex and the `www` form point at CloudCart, otherwise the verification step prunes the unreachable name and the cert is issued only for the reachable one. This rarely matters for storefront serving (the platform's edge routing handles both anyway) but it does matter for SSL coverage on the second name.

### The `lets_encrypt` app gate is re-checked server-side on every install attempt

Beyond the page-level `ssl_certificate` plan gate, the Automatic install endpoint has a `cc_apps_purchase:lets_encrypt` middleware that re-checks the app is purchased + installed at submit time. If the app subscription has lapsed (e.g., the merchant's payment failed for the Let's Encrypt Manager app), the middleware redirects to the apps catalog without issuing the cert — the modal then surfaces the **Install app** panel instead of confirming the cert.

### After install, the cert is marked `free=1`

The Automatic install endpoint sets `free=1` on the cert record — this is the platform's marker that "this cert is managed by Let's Encrypt and should be picked up by the renewal sweep". The Manage-mode view then shows the green **Automatic** renewal badge plus the *"Managed by [Let's Encrypt Manager]"* label linking to [[apps-lets-encrypt]].

### Issuance errors are surfaced as host-field validation errors

On ACME failure (DNS-broken, rate-limit, HTTP-01 timeout, etc.), the exception message is returned to the modal as a validation error against the `host` field. **Specific timeout errors during verification are NOT logged to the platform exception store** (they're common transient failures, suppressed to keep error-noise down). For the merchant-facing error catalogue, see [[settings-ssl-troubleshooting]].

### Free-SSL after-install propagation

After a Let's Encrypt cert is issued, it must propagate to the edge (Cloudflare custom-hostname push, GCloud LB push). The cert record is stored with `pending=1` / `gcloud_pending=1` until the background workers complete the push — see [[settings-ssl-edge-propagation]] for timing and what the merchant sees during propagation.

## Related

- [[settings-ssl]] — hub.
- [[apps-lets-encrypt]] — the paid app that powers this tab.
- [[apps]] — apps catalog for installing the Let's Encrypt Manager app.
- [[settings-domains]] — the parent page where DNS is configured; correct A / CNAME setup is required for ACME HTTP-01 verification to succeed.
- [[plan-features]] — the `ssl_certificate` plan-feature upsell when stores lack the feature.

## Open questions

_None._
