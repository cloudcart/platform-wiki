---
type: entity
aliases: ["Domain SSL", "SSL certificate", "Let's Encrypt", "Manual SSL", "External SSL certificate", "SSL expiry", "SSL fallback", "Punycode certificate", "IDN SSL"]
tags: [settings, apps, domains, ssl, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[domain]]. See the hub for the other aspects (attributes, relationships, lifecycle, DNS / Cloudflare, primary + plan gates).

# Domain — SSL

## Identity

How HTTPS is provisioned, renewed, and recovered for a [[domain|Domain]]. Every custom Domain carries its own SSL certificate (required so the storefront loads over HTTPS without browser warnings — without it modern browsers refuse to load the site or show a red security warning). There are exactly **two modes** — automatic via Let's Encrypt or manual via an externally-obtained certificate — and they are **mutually exclusive per Domain**. A daily platform-wide sweep finds expired certificates and automatically falls back to the always-present `<handle>.cloudcart.net` subdomain so the storefront keeps serving. IDN (internationalised) Domains use the **Punycode form** of the hostname in the underlying certificate — standard ACME behaviour, not a CloudCart choice. This page is the reference the AI Assistant cites when a merchant asks *"How do I install my SSL cert?"*, *"Why did my domain switch back to cloudcart.net?"*, or *"My SSL is about to expire — what now?"*.

## Aliases

- **SSL certificate** — the standard technical term.
- **Let's Encrypt** / **Automatic SSL** — the free, auto-renewed mode driven by the [[apps-lets-encrypt]] app.
- **Manual SSL** / **External SSL** — the merchant-managed mode using a cert from an external CA.
- **SSL fallback** — the automatic switch back to `<handle>.cloudcart.net` when a primary Domain's cert expires.

## Key Attributes

### Automatic OR Manual — mutually exclusive per Domain

A Domain can have either a Let's Encrypt cert OR a manual external cert at any given time. Switching modes requires **Remove + reinstall**:

- **Manual → automatic**: Remove the manual cert, then go to Automatic tab on [[settings-ssl]] and install. The [[apps-lets-encrypt|Let's Encrypt Manager]] app must be installed and paid.
- **Automatic → manual**: Remove the Let's Encrypt cert, then go to Manual tab and start the CSR / install flow.

| Mode | How it's provisioned | Renewal | Failure surface |
|------|----------------------|---------|-----------------|
| **Automatic (Let's Encrypt)** | Installed via [[apps-lets-encrypt]] when the merchant clicks Install on the Automatic tab of [[settings-ssl]]. Provisioning is one-shot via the ACME protocol. | Auto-renewed by a daily platform sweep — renews certs within ~30 days of expiry. | Renewal failure logs an SSL status of `failed` on the row; if not recovered before expiry, the daily expiry sweep fires the fallback rule. |
| **Manual (external CA)** | Merchant obtains a cert from an external CA (Comodo, DigiCert, GoDaddy SSL, etc.) and pastes certificate + chain + private key into the SSL modal on [[settings-ssl]] (Manual tab). | NOT auto-renewed. Merchant must track expiry and replace the cert before the date in the SSL modal. | Same fallback rule as Let's Encrypt — when the merchant misses the deadline, the daily sweep deactivates the Domain and falls back the primary. |

### SSL expiry triggers admin alert + automatic fallback

A platform-wide daily sweep finds expired certs and acts as follows:

- **If the expired Domain is the Site's primary**, the platform switches the primary back to the `<handle>.cloudcart.net` subdomain (which has its own CloudCart-managed wildcard cert) and deactivates the custom Domain. The merchant gets an alert and the storefront keeps serving HTTPS without warnings — the customer just sees the `<handle>.cloudcart.net` URL.
- **If the expired Domain is non-primary**, it is just deactivated. Alert raised.

The alerts surface in the [[admin-notification|admin notification panel]] and are flagged so the merchant also gets an email per [[settings-admin-notifications]] gates. For free Let's Encrypt certs, the fallback should only fire when renewal is **blocked** (DNS broken, domain no longer points at CloudCart, ACME challenge failing). For external manual certs, this is the merchant's primary signal that they forgot to replace an expiring cert.

### IDN SSL certificates use Punycode (third-party behavior, not a CloudCart choice)

When a merchant attaches an IDN (internationalised) domain like `магазин.bg`, the underlying SSL certificate is issued against the **ASCII Punycode form** (`xn--80akijazfba.bg`) — this is the standard Let's Encrypt / ACME behaviour and applies equally to external CAs. Browsers transparently match the Punycode certificate against the Unicode address bar, so customers do not see the Punycode form during normal browsing. Some browser certificate-inspection panels (e.g., the "View certificate" details modal) display the Punycode form, which can confuse merchants opening the cert manually. See [[domain-primary-and-plan-gates]] for the platform-side IDN handling.

### SSL plan gate

The `ssl_certificate` plan-feature controls whether the merchant can install SSL at all on custom Domains — see [[plan-gates]]. Without it, only the wildcard cert on `<handle>.cloudcart.net` is available.

## Where it appears

- [[settings-ssl]] — the per-Domain SSL modal with Automatic / Manual tabs, Install / Manage / Remove / Regenerate CSR actions, and the visible expiry date.
- [[settings-domains]] — surfaces the SSL status chip per row (active / pending / failed / expiring soon).
- [[settings-admin-notifications]] — controls whether SSL-expiry / fallback alerts are emailed.
- [[apps-lets-encrypt]] — the paid app that owns automatic-mode provisioning + renewal.

## Related

- [[domain]] — hub.
- [[apps-lets-encrypt]] — automatic SSL app.
- [[settings-ssl]] — per-Domain SSL management screen.
- [[admin-notification]] — SSL expiry / fallback alerts surface here.
- [[settings-admin-notifications]] — email gating for the alerts.
- [[plan-gates]] — `ssl_certificate` feature gate.
- [[plan]] — plans bundle the SSL feature differently.

## Open Questions

- ⏸️ The exact behaviour when an SSL cert is provisioned but the Domain is then deactivated — does the cert auto-renew on the daily sweep, or skip until the Domain is reactivated? `(verify)`
