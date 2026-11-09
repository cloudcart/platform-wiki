---
type: feature
nav_path: "Settings → Domains → Add domain flow"
route_name: domains.settings
route_path: /admin/settings/domains
aliases: ["Add domain", "Buy a domain", "Add existing domain", "Purchase new domain", "WHOIS contacts", "Domain renewal warning", "IDN domains", "Punycode domain", "No inbound transfer"]
tags: [settings, domains, namecom, whois, idn, registrar]
plan_gates: ["domains", "custom_hostname"]
created: 2026-06-10
updated: 2026-11-09
source_count: 5
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

**Option 1 — Add existing domain** (collapsed by default; its description is still placeholder copy):

- *"Enter domain name here"* + an input with a fixed `https://` prefix; the merchant types just the hostname.
- Inline errors: *"Domain is required"*, *"Invalid domain name"*, *"The domain already exists in the system"*.
- **Save** adds the row and opens the Activate Domain modal ([[settings-domains-dns-cloudflare]]); **Cancel** clears the input. *"Need help adding a domain?"* links to the help center.

**Option 2 — Purchase new domain** (collapsed by default):

- *"Search for your new domain here"* + a search input and **Search**.
- A list of TLD variants from the registrar. Purchasable rows show a **"Promo price 1st year"** badge, *"Price for next year: {price}"* and **Buy**; others say *"This domain is not available for purchase."*.
- **Buy** opens the checkout panel for WHOIS + payment.

### CheckoutExternal panel (domain purchase)

A side-panel (the same checkout used for plan packs). The merchant sees the domain and price, fills in the WHOIS registrant contact (name, address, email, phone — required by **ICANN**), and pays with the plan's stored payment method. On success the new domain appears in the table as Active.

### Per-domain row — renewal + WHOIS edit (CloudCart-purchased only)

- **Renew** link: under **Expires on** on every CloudCart-purchased domain, whatever the date. It opens the checkout with the renewal price; paying charges the plan's card at once (an invoice for the domain service) and extends the registration by one year at the registrar.
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

### Renewal and expiry

- **Only Renew renews.** No CloudCart job renews or charges a registration by itself. A daily job posts an Important admin alert for each CloudCart-purchased domain from one month before to one month after its expiry date: *"Domain {domain} is paid to {date}. You can renew it from HERE"* (*"Домейн {domain} е платен до {date}. Можете да го подновите от ТУК"*).
- The renewal price is the registrar's current price plus CloudCart's margin, so it can differ from the first year. It is independent of the SSL sweep at 25 days ([[settings-domains-ssl]]).
- Whether the registrar still accepts a renewal after the expiry date, and at what price, is the registrar's rule; whether the registrar account renews on its own is not set in CloudCart's code (verify).
- A lapsed registration stops resolving. The store stays on its `*.cloudcart.net` address, but a lapsed **primary** keeps the other addresses redirecting to it — see [[settings-domains-primary]].

### Internationalised domain names (IDN) — Punycode under the hood

When the merchant types an IDN like `сайт.бг`, the platform lowercases it and stores it in Punycode (e.g. `xn--80aswg.xn--90ae`), converting back to native characters for display. ACME requests, Cloudflare zones and the certificate Subject use the Punycode form, so a URL may show that form elsewhere — that's normal.

### No inbound-transfer flow

CloudCart does NOT expose a "transfer a domain into Name.com from another registrar" path. The two options in the Add Domain modal are **only**:

1. **Add existing** — keep the domain at the original registrar, change its nameservers to point at CloudCart-managed Cloudflare.
2. **Buy new** — purchase a fresh registration through CloudCart's reseller.

The registrar integration has no transfer call, and the admin shows no unlock or transfer (EPP) code for a domain bought here. Pointing a domain's nameservers at CloudCart is not a transfer; what it copies is on [[settings-domains-external-dns]]. A merchant who wants CloudCart to hold the registration buys it with *Buy new* or asks CloudCart support about a manual transfer (verify the procedure and price).

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
