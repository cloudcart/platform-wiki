---
type: feature
nav_path: "Apps → OLX → Settings"
route_name: apps.olx.settings
route_path: /admin/apps/olx/settings
aliases: ["OLX Settings", "OLX credentials", "OLX country setup", "Connect to OLX"]
tags: [apps, olx, marketplace, settings, oauth]
plan_gates: []
created: 2026-05-21
updated: 2026-06-11
source_count: 2
---
# OLX → Settings

## Purpose

The **Settings** tab is where the merchant configures their OLX connection — picks **which country's OLX** to integrate with, sets who pays the shipping (buyer vs merchant), enters the seller contact + listing location, and authorizes CloudCart against the merchant's OLX account. Until credentials are validated and the required fields are filled, the rest of the OLX tabs (Configuration / Products / Adverts / Parameters / History) are gated.

For the OLX feature set, see [[apps-olx]].

## Where to find it

Sidebar → Apps → OLX → **Settings tab**. Route: `/admin/apps/olx/settings`.

## What the merchant can do here

### Before authorization (credentials not yet validated)

The page shows a credentials form. The merchant picks the **Country** and **Shipping is paid by** value, then clicks **Connect** — this starts the OAuth handshake against OLX. The merchant is redirected to OLX's authorization page, grants permission, and returns here; the platform then validates the returned token.

### After authorization (validated)

The Settings card collapses into a compact preview showing the connected **Country** and **Shipping is paid by** value. A separate card below shows the connected OLX user / shop info.

The merchant can **change credentials** (re-validate against a different OLX account) via the edit pencil — this re-shows the form, and while the new credentials are unvalidated the **Connect** button reappears.

The merchant can also **Disconnect** — see Business rules; this wipes all OLX data.

### What the merchant CANNOT do here

- Skip Country selection — OLX's API is country-specific; each country needs separate authorization.
- Change Country without re-authorizing — switching country forces a fresh OAuth handshake.
- Use OLX without an active seller account in the chosen country.
- Override the per-country currency.

## Settings & fields

### Connection fields

| Field | Setting key | Notes |
|---|---|---|
| **Country** | `endpoint_id` | Dropdown of OLX countries, searchable. Required. Only **Bulgaria (olx.bg)** and **Romania (olx.ro)** are enabled in production today. Poland, Ukraine, Portugal, Kazakhstan, Belarus, Angola, Mozambique appear in the language files but are not selectable (their credentials are disabled). |
| **Shipping is paid by** | `shipping_payer_id` | Dropdown — **Buyer** or **Merchant** (`shipping_payer_buyer` / `shipping_payer_merchant`). Required. Sent with every advert via the OLX `delivery_paid_by` attribute and shown to buyers on the listing. |

Per-country currency is fixed: Bulgaria (`endpoint_id` = 2) → `EUR`; Romania (`endpoint_id` = 3) → `RON`. The merchant cannot override it.

Validation errors surface per field as `responseErrors['endpoint_id']` / `responseErrors['shipping_payer_id']` (e.g. "Country is required", "Invalid OLX country").

### Seller contact + listing location

Beyond Country and shipping payer, the merchant fills the seller contact and location that appear on every OLX advert:

| Field | Setting key | Notes |
|---|---|---|
| First name | `first_name` | Required. |
| Last name | `last_name` | Required. |
| Phone | `phone` | Required. Stored raw, exactly as typed — only `/` characters are stripped before each publish. |
| Region | `region_id` | Required. Autocomplete; choosing a Region populates the Cities list. |
| City | `city_id` | Required. Autocomplete; choosing a City populates the Districts list. |
| District | `district_id` | Optional. Autocomplete. |

Region / City / District are an **autocomplete cascade**: each field depends on the one above it, the merchant types to filter by partial name, and the lists are paginated on the server (no full preload). This geography comes from **OLX's own region / city / district tables** specific to each OLX country — CloudCart's general address book is not used here.

### Other saved settings

- `download_category` — the default CloudCart category for products imported **from** OLX via the [[apps-olx-adverts]] tab's Download action. Optional; without it, an imported product may have no category.
- Sync flags `sync_status`, `sync_delete`, `sync_quantity`, plus `is_discount`, `title_trim` — control publish/sync behaviour.
- OAuth tokens (access + refresh) are stored separately on the app instance after Connect.

## Business rules

### OAuth handshake required

Before any other OLX tab works, the merchant must complete OAuth. The returned token is stored and used for all subsequent OLX calls.

### Configured gate — 6 required fields

The integration treats itself as **configured** (`is_configured`) only when all six are set: `endpoint_id`, `first_name`, `last_name`, `phone`, `region_id`, `city_id`. District is optional. Until all six are filled, the integration shows "not configured" and the other OLX tabs stay gated / may behave unpredictably.

### Automatic token refresh — refresh token valid 1 month

The access token auto-refreshes using the stored refresh token. The refresh token itself is valid for **one month** from issuance; after a month of inactivity the merchant must re-authorize.

### Changing Country is heavy

Once credentials are validated, switching Country means disconnect → change → re-authorize. On a store with existing OLX listings this risks orphaning those listings (verify exact behaviour).

### Disconnect wipes all OLX data

Clicking **Disconnect** removes every saved OLX setting (country, shipping payer, contact, location, sync flags, `is_discount`, `title_trim`, `download_category`, and the stored tokens) **and** clears all locally stored OLX adverts, category mappings, parameter mappings, value mappings, and the history log. So all prior configuration is wiped — the merchant must redo everything on reconnect. See [[apps-olx-history]] for the operation log that is also cleared.

### Permission

Standard apps permission scope.

## Related

- [[apps-olx]] — OLX hub.
- [[apps-olx-configuration]] — category mapping (next step after Settings).
- [[apps-olx-products]] — products to publish.
- [[apps-olx-adverts]] — publish / download listings (uses `download_category`).
- [[apps-olx-history]] — operation log (cleared on Disconnect).

## Open questions

- Exact behaviour for OLX listings already published when the merchant changes Country (orphaned vs removed).
