---
type: feature
nav_path: "Settings → Domains → Add domain flow"
route_name: domains.settings
route_path: /admin/settings/domains
aliases: ["Add domain", "Buy a domain", "Add existing domain", "Purchase new domain", "WHOIS contacts", "Domain renewal warning", "IDN domains", "Punycode domain", "No inbound transfer"]
tags: [settings, domains, namecom, whois, idn, registrar]
plan_gates: ["domains", "custom_hostname"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[settings-domains]]. See the hub for related aspects (DNS / Cloudflare, SSL, primary, deletion, plan gates).

# Domains — Add domain flow

## Purpose

The Add New Domain modal lets the merchant attach a new domain to their store in one of two mutually-exclusive ways: **Add existing** (keep the registration at the merchant's original registrar, point nameservers at CloudCart) or **Buy new** (register a fresh domain via CloudCart's Name.com reseller integration). This page covers the modal itself, the WHOIS / ICANN checkout panel, the IDN (internationalised domain name) handling, the renewal warning, and the deliberate absence of an "inbound transfer" flow.

## Where to find it

Settings → Domains → **+ Add domain** button in the page header. The button opens the Add New Domain modal (`size="md"`) titled *"Add New Domain"* with subtitle *"Choose one of the options for adding a new domain"*. Closes via the top-right X icon or backdrop click.

## What the merchant can do here

### Add New Domain modal — two accordion options

Only one option can be expanded at a time. Opening the second collapses the first.

**Option 1 — Add existing domain** (collapsed by default):

- Browser-icon header. Description: *"Lorem ipsum dolor sit amet consectetur."* (placeholder copy not yet replaced).
- On expansion: *"Enter domain name here"* heading + styled input with a fixed `https://` prefix badge. The merchant types just the hostname.
- Inline validation: red error below the field for *"Domain is required"*, *"Invalid domain name"*, *"The domain already exists in the system"*. Errors are x-closable.
- **Cancel** clears the input and collapses the accordion.
- **Save** POSTs to `save-external` with `{domain: <value>}`. On success the new row is added; modal closes. On error `responseErrors.domain` shows inline.
- Below the buttons: *"Need help adding a domain?"* with a **Contact us** link to the help-center article.

**Option 2 — Purchase new domain** (collapsed by default):

- Globe-icon header. Description: *"Purchase new domain description"* (placeholder).
- On expansion: *"Search for your new domain here"* heading + search input with magnifying-glass icon + **Search** button.
- The merchant types a name (e.g., `mystore`); Enter or Search calls `POST /search` with `{keyword: <value>}`.
- Below the search input, an animated list of TLD variants from the registrar. Each row shows:
  - Check-circle icon (purchasable) OR ban icon (not available).
  - The full domain name (e.g., `mystore.com`).
  - For purchasable rows: a **"Promo price 1st year"** badge with first-year price, a *"Price for next year: {price}"* subtitle, and a **Buy** button.
  - For unavailable rows: *"This domain is not available for purchase."*.
- Clicking **Buy** emits `purchaseDomain` to the parent — opens the `CheckoutExternal` panel for WHOIS + payment.

### CheckoutExternal panel (domain purchase)

A separate side-panel that opens after the merchant clicks **Buy**. Implemented as `CheckoutExternal` (shared component used elsewhere for plan-pack purchases — not unique to Domains). The merchant:

- Sees the domain + price line item.
- Fills in WHOIS registrant contact: name, address, email, phone — required by **ICANN** registration rules.
- Confirms payment from the stored payment method on their plan subscription.
- On success the new domain appears in the table as Active.

### Per-domain row — renewal + WHOIS edit (CloudCart-purchased only)

- **Renew** CTA: shown when `expire_date <= now + 1 month` for CloudCart-purchased domains. Renewal is billed through the merchant's plan subscription.
- **WHOIS contacts edit**: lets the merchant update the registrant contact info that ICANN requires on file.

## Settings & fields

| Field | Where | Notes |
|---|---|---|
| Domain name (Add existing) | Input field, `https://` prefix badge | Stored lowercased + IDN-converted. |
| Search keyword (Buy new) | Search input | POST `/search` `{keyword}`. |
| WHOIS: registrant name, address, email, phone | CheckoutExternal panel | ICANN-required. Stored at the registrar. |
| Payment method | CheckoutExternal panel | Reuses the merchant's plan-subscription payment method. |

## Business rules

### Add existing — what the validation checks

- Domain format must be a valid hostname.
- The domain must NOT already exist anywhere on the platform's `hosts` table — see [[settings-domains-deletion]] for the platform-wide uniqueness rule (one domain → one store; the `www.` variant matches the bare form and vice versa).
- The merchant's plan-feature quota must have headroom. See [[settings-domains-plan-gates]].

On success the new row appears with DNS status **Pending** — the merchant must complete the nameserver change to activate it. See [[settings-domains-dns-cloudflare]] for the activation flow.

### Buy new — what happens on confirm

1. Merchant types a desired name; the platform queries Name.com for available TLD variants and pricing.
2. **Prices are shown in the merchant's display currency** (auto-converted from registrar pricing).
3. Merchant picks a result, fills in WHOIS contact, and confirms payment.
4. CloudCart pays the registrar on the merchant's behalf and creates the domain record on the platform side.
5. **WHOIS Privacy is automatically enabled** — the public WHOIS lookup shows the registrar's privacy proxy, not the merchant's real address.
6. Domain appears as Active typically within seconds (no DNS-propagation wait, because CloudCart already owns the registration).

### Renewal warning threshold = 1 month

For CloudCart-purchased domains only, the row shows a renewal warning when `expire_date <= now + 1 month`. Renewal price may differ from the initial purchase price — it reflects current registrar pricing at renewal time. This is independent of the SSL auto-renewal sweep (which triggers at 25 days before cert expiry — see [[settings-domains-ssl]]).

### Internationalised domain names (IDN) — Punycode under the hood

When the merchant types an IDN like `сайт.бг`, the platform lowercases it, converts to ASCII Punycode via `idn_to_ascii($name, 0, INTL_IDNA_VARIANT_UTS46)` (stored as e.g. `xn--80aswg.xn--90ae` in the `hosts.host` column), and converts back to UTF-8 via `idn_to_utf8(...)` when displaying. The certificate model uses the same conversion on its `common` column.

So the merchant sees the IDN in native characters but ACME requests, Cloudflare zone creation, and SSL certificate Subject all use the Punycode form. If the merchant exports settings or hits a CDN endpoint directly with the IDN form, the URL may show as the Punycode equivalent — that's normal.

### No inbound-transfer flow

CloudCart does NOT expose a "transfer a domain into Name.com from another registrar" path. The two options in the Add Domain modal are **only**:

1. **Add existing** — keep the domain at the original registrar, change its nameservers to point at CloudCart-managed Cloudflare.
2. **Buy new** — purchase a fresh registration through CloudCart's reseller.

Merchants who want to move their registration to be managed by CloudCart must either buy a fresh registration via *Buy new*, or contact CloudCart support to arrange a manual transfer.

### Domain purchase failed — what to tell the merchant

| Cause | Merchant guidance |
|---|---|
| Payment declined / insufficient funds | Check the billing details on the merchant's plan subscription. |
| Restricted TLD | Some TLDs (`.bank`, country-restricted ones, etc.) require eligibility proof. Try another TLD. |
| Registrar timeout | Retry after a moment. |

## Related

- [[settings-domains]] — hub.
- [[settings-domains-dns-cloudflare]] — what happens after a domain is added: Cloudflare zone activation, nameserver change.
- [[settings-domains-plan-gates]] — `domains` + `custom_hostname` quotas and the upsell flow when Add is blocked.
- [[settings-domains-deletion]] — platform-wide `hosts` uniqueness check that drives the "already exists" error.
- [[plan-vs-feature-pack]] — the pack-checkout UX used by `CheckoutExternal`.
- [[billing-cards]] — the stored payment method that funds the purchase.

## Open questions

None.
