---
type: feature
nav_path: "Settings → Store settings → Maintenance status"
route_name: general.settings
route_path: /admin/settings/general
aliases: ["Maintenance mode", "Maintenance status", "Maintenance page", "IP whitelist", "Allowed IPs", "Поддръжка", "Режим на поддръжка", "Бяла листа IP"]
tags: [settings, general, maintenance, storefront-access, ip-whitelist]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[settings-general]]. See the hub for related aspects (store details, locale, language, security key, product badges, operational toggles, industry multi-select).

# Store settings — Maintenance status

## Purpose

The Maintenance status box gives the merchant a master switch to **temporarily close the storefront** to customers while leaving it accessible from a configurable set of IP addresses. Used during stock-takes, large bulk imports, theme swaps, or any work where exposing a half-built store would be embarrassing. Three fields: the master `maintenance` switch, a `maintenance_page` picker (which CMS page is shown to locked-out visitors), and `maintenance_ip_list` (comma-separated IPs that bypass the lock).

The single non-obvious quirk: **the maintenance page and IP whitelist are NOT stored in the main settings table**. They live in a separate Configuration group called `maintenance`. The `maintenance` switch itself flips a column on the Site record (`manual_maintenance`). This three-store split matters when support diagnoses "settings won't save" tickets — see Business rules.

> The right-side info panel reads: *"You can temporarily limit the access to your store. Choose who can access your website and show maintenance messages."*

Header label: "Security and maintenance".

## Where to find it

Sidebar → Settings → **Store settings** → Maintenance status box.

## What the merchant can do here

- Put the storefront into maintenance mode — visitors see the chosen CMS page instead of the live storefront.
- Choose which existing CMS page is shown as the maintenance landing.
- Whitelist a comma-separated list of IPs that bypass the maintenance lock (typically the merchant's office IP + any agency / consultant IPs).
- See their own current IP as a hint (so they can paste it into the whitelist without having to look it up).
- Turn maintenance off — the storefront is restored on the next request; no cache flush needed.

## Settings & fields

### Box: Maintenance status (`maintenance`)

| Field / Control | What it does | Notes |
|-----------------|--------------|-------|
| **Enable maintenance mode** (`maintenance`) | Master switch — when ON, storefront shows a maintenance page to everyone except whitelisted IPs. | The next two fields appear only when this is ON. Maps to `site.manual_maintenance` column. |
| **Select a landing page** (`maintenance_page`) | The page shown to visitors during maintenance. | Options come from the store's CMS pages (`meta.pages`). |
| **Allow IP addresses** (`maintenance_ip_list`) | Comma-separated list of IPs that bypass the maintenance lock. | The merchant's own current IP is shown as a hint (`meta.ip`). |

## Business rules

### Maintenance config is stored in three separate places

The maintenance fields fan out into three storage locations on save — knowing which holds what speeds up support investigation:

- **`maintenance` switch** — maps to a column on the **Site record** (`manual_maintenance`). Visible immediately everywhere.
- **`maintenance_page`** — lives in a **separate Configuration group** called `maintenance`, NOT in the main settings table.
- **`maintenance_ip_list`** — also lives in the same `maintenance` Configuration group (alongside the `allowed_ips` field) and is NOT in the main settings table either.

Practical merchant-visible effect: if a merchant reports *"the maintenance page won't save,"* that's likely a permission issue on the Configuration store, not on the main Setting store. The maintenance switch and the maintenance page can fail independently.

See the storage-split table on the hub [[settings-general]] for the full fan-out picture.

### Conditional fields — only visible when the switch is ON

The maintenance landing page picker and the IP whitelist input both render conditionally — they only appear when `maintenance` is set to ON. Turning the switch OFF hides them in the UI but does NOT clear the underlying values; turning it back ON brings the previously-saved page and IP list back.

### Customer sessions are NOT cleared on maintenance entry

Switching maintenance ON does not log out existing customer sessions — it only changes what happens on the **next request**. Any customer currently inside the checkout flow can complete their order as long as their request hits the server while the maintenance flag flips (race-window behaviour). For a deterministic "all customers locked out at moment T" semantic, the merchant should plan around the inherent eventual-consistency.

### IP whitelist matches the merchant's request IP exactly

The whitelist compares the visitor's incoming IP against the comma-separated list literally. CIDR ranges are NOT supported (verify). A merchant behind a dynamic ISP IP will need to update the list each time their IP rotates. The hint shown next to the input (`meta.ip`) is the IP the admin panel sees the merchant from at the moment the page loads — usually correct, but a merchant on a different network than the storefront visitor will need to enter that other IP.

### Maintenance page must be an existing CMS page

The dropdown options come from `meta.pages` — the store's current CMS pages. The merchant must have a page authored already; this screen does not create one. A common merchant flow is to create a "We'll be back soon" page in CMS first, then pick it here.

## How it works (verified against backend)

### Three-store transaction wrapping

All three maintenance fields save inside the same outer transaction as the rest of the store-settings page — so a failure in any one field rolls back the whole save (including unrelated fields like site name). The transaction boundary is the entire PUT request.

### `manual_maintenance` column is the source of truth at runtime

The middleware that intercepts storefront traffic reads the `manual_maintenance` column on the Site record (not the setting key) to decide whether to show the maintenance page. The settings-store `maintenance` key and the Site column are kept in sync by the save handler. If they drift (e.g., direct DB edit), the Site column wins.

### The storefront "maintenance" page documents the customer-facing side

For what the customer actually sees when they hit a maintenance'd store, see [[maintenance]] (storefront-page docs). That page documents the rendering side — this page documents the admin toggle that triggers it.

## Related

- [[settings-general]] — hub.
- [[maintenance]] — storefront-page entry documenting what the customer sees during maintenance.
- [[site]] — the Site record holding `manual_maintenance`.
- [[settings-general-security-key]] — sibling box under the same "Security and maintenance" header.

## Open questions

- Does the IP whitelist support CIDR ranges (`192.168.1.0/24`) or only exact match? (verify)
- Does a merchant lockout (e.g., wrong IP in whitelist, no other admin access) require CloudCart support to reset, or is there a self-service recovery? (verify)
