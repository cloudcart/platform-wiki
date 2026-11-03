---
type: feature
nav_path: "Apps → MicroBG → Settings → Registration"
route_name: apps.microbg.settings
route_path: /admin/apps/microbg/settings
aliases: ["MicroBG registration", "MicroBG settings form", "Micro.bg user types", "Existing user vs New registration", "MicroBG handshake form"]
tags: [apps, erp, bulgaria, registration, checkout, plan-gate]
plan_gates: ["microbg_subscription"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[apps-microbg]]. See the hub for the other aspects (architecture split, prerequisites, sync mechanics, partner matching, troubleshooting).

# MicroBG — registration handshake + Settings form

## Purpose

This aspect documents the Settings tab where the merchant fills in personal + company data, picks **Existing user** or **New registration**, and triggers the handshake with Micro.bg. The handshake is a one-time operation; once `is_registered = 1`, the form switches to read-only Info mode.

## Where to find it

- **CloudCart admin** → Sidebar → **Apps** → **MicroBG** → **Settings** tab.
- Route: `/admin/apps/microbg/settings`. The Settings tab calls **GET `/admin/api/microbg/info`** to load store info (used to pre-fill the form) and **GET `/admin/api/microbg/settings`** to load the current subscription state. On save, **POST `/admin/api/microbg/settings`** sends to Micro.bg.

## What the merchant can do here

- Pick between *Existing user* (`userType = exist`, default) and *New registration* (`userType = new`).
- For new registration: fill personal + company data, click Save, pay via CloudCart checkout if the `microbg_subscription` plan feature isn't enabled, get provisioned on Micro.bg.
- For existing user: see the read-only subscription Info (expiration, order ID, subdomain, API key) and copy the API key to paste into Micro.bg's CloudCart Control Panel.

### What the merchant CANNOT do here

- Re-trigger the handshake after `is_registered = 1`. The form goes read-only.
- Change the merchant's Micro.bg subdomain from CloudCart's side — provisioned at registration on Micro.bg's side.
- Rotate the API key from this screen specifically. Key rotation happens on [[settings-api-keys]]; the new key must be manually pasted into Micro.bg's CloudCart Control Panel.

## Settings & fields

### Existing user (`userType = exist`, default)

The Info sub-card shows four read-only rows:

| Row | What it shows |
|---|---|
| **Subscription validity** | Expiration date from Micro.bg's `PaymentToDate`, formatted `d.m.Y H:i:s`. |
| **Micro.bg Order Number** | The merchant's Micro.bg subscription `OrderId`. |
| **Domain at Micro.bg** | The merchant's micro.bg subdomain (provisioned at registration). |
| **API key** | The CloudCart API key Micro.bg uses to connect — copy-to-clipboard button. Source: the first key in [[settings-api-keys]]. |

### New registration (`userType = new`)

#### Personal Data card

| Field | Required | Notes |
|---|---|---|
| **First and last name** (`user.name`) | yes | Pre-filled from `company_mol` setting. |
| **Email address** (`user.email`) | yes | Pre-filled from `site_email`. Receives the Micro.bg login email. |
| **Phone number** (`user.phone`) | yes | Pre-filled from `site_phone`. |

Help text: *"We need your personal data for initial registration in micro.bg. You will receive your login details at the specified email address."*

#### Company Information card

| Field | Required | Notes |
|---|---|---|
| **Company Name** (`company.name`) | yes | Pre-filled from `company_name`. |
| **BULSTAT** (`company.eik`) | yes | Bulgarian company ID. Pre-filled from `company_bulstat`. |
| **VAT number** (`company.vat`) | no | Pre-filled from `company_vat`. |
| **Location** (`company.place`) | no | Pre-filled from `site_city`. |
| **Address** (`company.address`) | yes | Pre-filled from `site_street`. |
| **MOL** (`company.mol`) | yes | "Материално отговорно лице" — Bulgarian legal-responsible-person field. Pre-filled from `company_mol`. |
| **Phone number** (`company.phone`) | yes | Pre-filled from `site_phone`. |
| **Email Address** (`company.email`) | yes | Pre-filled from `site_email`. Placeholder: `example@cloudcart.com`. |

On Save the controller calls Micro.bg's `Check` endpoint first; if the merchant lacks the `microbg_subscription` plan feature, Cart is initialised from a promo + the merchant is redirected to **`/admin/checkout`** to pay. After payment, the `Create` endpoint provisions the merchant on Micro.bg's side and returns the `OrderId` + `PaymentToDate`.

### Plan gates

The integration depends on the `microbg_subscription` plan feature (a paid add-on bought through CloudCart's checkout). Without it, the registration flow always redirects to checkout, never to the live form.

## Business rules

### Two install paths

1. **New Micro.bg customer** (no existing Micro.bg account) — installs the CloudCart MicroBG app, fills the registration form, pays via CloudCart checkout, gets provisioned on Micro.bg automatically.
2. **Existing Micro.bg customer** (already has a Micro.bg license) — **does NOT install the CloudCart app**. Instead:
   - Goes to CloudCart **Settings → API** and copies the API key.
   - In Micro.bg: **Администриране → Връзка с ел.магазини** → **Регистриране на ново приложение** → name `CloudCart`, type `CloudCart`, status `приложението се използва`, Save.
   - Then in Micro.bg's CloudCart Control Panel: pastes the API key + the storefront URL (e.g. `https://sampleshop.cloudcart.net`) and starts the sync.

### Handshake flow

When the merchant clicks Save on the Settings tab:

1. The controller calls Micro.bg's `Check` endpoint with the merchant's user + company data.
2. **Success** (`response.Success == 1`):
   - If the `microbg_subscription` plan feature is NOT enabled → adds the feature pack to the merchant's cart via a promo + redirects to `/admin/checkout`. After payment, the registration runs automatically on the next visit.
   - If already subscribed → calls Micro.bg's `Create` endpoint, stores `is_registered = 1` + `PaymentToDate` + `OrderId` in app settings, returns JSON.
3. **Failure** (`response.Success != 1`) → returns HTTP **503** with the first Micro.bg error message (typical reasons: invalid EIK, EIK already registered, missing required field — see [[apps-microbg-troubleshooting]]).

### Why the merchant sees the API key in CloudCart's Settings tab

The Info card pulls the API key from the **first** key in the merchant's [[settings-api-keys]] list. If the merchant has multiple keys, only the first one is shown here. To rotate keys for Micro.bg, the merchant must update the key value inside Micro.bg's CloudCart Control Panel manually — the CloudCart UI doesn't have a key-rotation action for Micro.bg specifically.

## Related

- [[apps-microbg]] — hub.
- [[settings-api-keys]] — source of the API key shown in the Info card.
- [[settings-general]] — `site_email` / `site_phone` / `site_city` / `site_street` used to pre-fill the form.
- [[settings-invoicing]] — `company_name` / `company_bulstat` / `company_vat` / `company_mol` used to pre-fill the form.
- [[plans-purchase]] — the `/admin/checkout` page the registration flow redirects to when the `microbg_subscription` feature is missing.

## How it works (verified against backend)

The Settings tab's GET / POST cycle is the entire CloudCart-side surface for the integration. On Save:

- The handshake controller is `saveSettingsCustom`.
- A successful `Check` + `Create` cycle writes `is_registered`, `PaymentToDate`, and `OrderId` into the app's persistent settings. On every subsequent load, the Existing-user view reads these back into the Info card.
- The Guzzle base URL is `https://micro.bg/ExtApps/CloudCart/Company/`; auth header `X-CloudCart-Key` is the merchant's first API key; action header is `X-CloudCart-Action: Check` or `Create`.

## Open questions

None.
