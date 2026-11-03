---
type: feature
nav_path: "Apps → GDPR → Store Address"
route_name: apps.gdpr.address
route_path: /admin/apps/gdpr/address
aliases: ["GDPR Address", "Store Address", "Legal entity address", "GDPR company info"]
tags: [apps, gdpr, compliance, store-address, legal-entity]
plan_gates: []
created: 2026-05-21
updated: 2026-06-11
source_count: 4
---
# GDPR → Store Address

## Purpose

The **Store Address** tab is where the merchant records the **legal entity's identification details** — the company name, registration number, owner name, contact phone, and physical address. This data appears on:
- **Privacy policy pages** (so customers know who's responsible for their data).
- **Cookie consent dialogs** (legal entity disclosure).
- **Invoices / receipts** (if invoicing isn't handled separately by [[apps-szamlazz]] / [[apps-fgo]] / [[apps-smart-bill]]).
- **Email footers** and **legal pages** rendered on the storefront.

GDPR Articles 13-14 require visible business identification when collecting personal data. This page is where that identification lives. For Bulgarian merchants, this is also where BULSTAT + MOL data goes for compliance with local commerce law.

For overall GDPR coverage, see [[apps-gdpr-overview]].

## Where to find it

Sidebar → Apps → GDPR → **Store Address tab**. Route: `/admin/apps/gdpr/address`.

## What the merchant can do here

- Fill in the legal entity's company name, registration number (BULSTAT), phone, owner (MOL), and physical address.
- Save changes with the **Save** button. A loading spinner shows while the form loads and while saving.

### What the merchant CANNOT do here
- Use this address for COURIER pickups — that's [[apps-econt]]/[[apps-dpdbulgaria-speedy|Speedy]] sender-address territory.
- Have multiple legal entities per storefront — single legal entity per store.

## Settings & fields

| Field | Setting key | Placeholder / hint | Required |
|---|---|---|---|
| **Company or business name** | `company_name` | "Company or business name are optional" | No |
| **Company registration number** | `company_bulstat` | "Company registration number (optional)" — BULSTAT for Bulgarian merchants | No |
| **Phone** | `site_phone` | "e.g. +359 888 888 888" | No |
| **Company owner** | `company_mol` | "Ivan Ivanov" — MOL (Bulgarian: "материално отговорно лице") | No |
| **Country** | `country` | Searchable dropdown of countries | No |
| **City** | `site_city` | "Sofia" | No |
| **Address** | `site_street` | "Sofia 1000" | No |
| **Postal code** | `postal_code` | "1000" | No |

**No field is enforced as required.** The address fields are saved directly from the form with **no server-side validation** — the merchant can save an empty BULSTAT, MOL, postal code, or any other field and the platform accepts it. Client-side hints may flag missing fields, but the backend imposes no minimum required set. Treat any "required" label as a compliance recommendation, not an enforced constraint.

**No format validation** on postal code or phone: both are stored as plain text with no country-aware pattern check (no "Bulgaria 4 digits", no E.164 phone formatting). The merchant is responsible for the correct format for their jurisdiction.

**No separate VAT field.** Bulgarian merchants use `company_bulstat` (ЕИК / BULSTAT), which serves the dual purpose of business registration AND tax identification in Bulgaria. For other jurisdictions, a separate VAT field may be needed elsewhere — verify per [[settings-general]].

**Country dropdown** is populated from the platform's master country list (the same list used by customer addresses and shipping zones). Labels are translated to the admin's panel language. The chosen country is stored as its **ISO code** (e.g., "BG", "DE"), not a numeric id; the form resolves the stored code back to a name on load.

## Business rules

### One source of truth — propagates everywhere

These are the **same setting keys used across the platform** — by [[settings-general]], by invoicing apps, by receipt/invoice templates, and by the storefront footer. They are not stored in a separate GDPR table. Editing the address here updates everywhere those settings are read, so **there is no cross-page sync issue** — there is only one source of truth. On save:
- The storefront's Privacy Policy page re-renders with updated entity info.
- The cookie consent dialog updates its company-name reference.
- Email footers / legal pages refresh.

### Per-storefront, not shared across stores

The address is stored per storefront. **Multi-storefront merchants have a separate address per store** — editing the Store Address on Store A does not propagate to Store B. Each storefront keeps its own `company_name`, `company_bulstat`, `site_phone`, etc., letting the merchant operate different legal entities or addresses per market. This matches the per-site override model in [[apps-multilang-stores]].

### Editing AFTER install does NOT rewrite existing policy text

When the merchant first installs GDPR, the seeded policy documents have the address values substituted into their body **once, at install time** — `{company_name}`, `{store_name}`, `{address}` (city + postal code + street), `{phone}`, `{email}`, `{mol}`, `{company_eik}` (BULSTAT), `{domain}`, and links to terms / policy / `/gdpr`. **Editing the Store Address afterwards does NOT retroactively rewrite the already-created policy documents.** The merchant must manually edit the policy text in [[apps-gdpr-policy]] to reflect any later address change.

### Legal entity disclosure

GDPR Articles 13-14 require the data controller (merchant's legal entity) to be identifiable to data subjects (customers). This page manages those identification details. While the fields are technically optional in the form, leaving them empty may violate GDPR / local commerce laws — the merchant should fill the full record.

### Bulgarian context

For Bulgarian merchants:
- **BULSTAT** = "ЕИК" / Bulgarian unified business identifier.
- **MOL** = "материално отговорно лице" = company owner / responsible person.

These fields are reused by [[apps-szamlazz]] / [[apps-fgo]] / [[apps-n18-audit]] / invoice templates when displaying merchant identity.

## Related

- [[apps-gdpr-overview]] — GDPR hub.
- [[apps-gdpr-policy]] — privacy policies that reference this entity (and must be hand-edited after an address change).
- [[apps-szamlazz]] / [[apps-fgo]] / [[apps-smart-bill]] / [[apps-n18-audit]] — invoicing apps reuse this entity data.
- [[settings-general]] — basic store info; reads the same setting keys.
- [[settings-brand]] — branding may reuse entity name.
- [[customers-details-billing-addresses]] — separate B2B-customer address concept.

## Open questions
