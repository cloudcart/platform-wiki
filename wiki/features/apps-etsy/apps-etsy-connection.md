---
type: feature
nav_path: "Apps → Etsy → Connection"
route_name: apps.etsy.settings
route_path: /admin/apps/etsy
aliases: ["Etsy connection", "Connect Etsy", "Etsy OAuth", "Etsy shop selection", "Etsy settings", "Etsy account", "Sale on Etsy install"]
tags: [apps, marketplace, etsy, oauth, connection, plan-gates]
plan_gates: ["etsy", "etsy_total_products"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[apps-etsy]]. See the hub for the other aspects (listing config, sync mechanics, variants + states).

# Etsy — connection, OAuth + multi-shop

## Purpose

Before any product can sync, the merchant has to connect a CloudCart store to an Etsy shop. This aspect covers the install + OAuth handshake, picking which Etsy shop syncs, the Settings form fields, the error-message reference, and the plan gates. Nothing here pushes a single listing — it's the gate every other Etsy aspect depends on.

## Where to find it

Sidebar → **Apps** → install → **Etsy** (titled *"Sale on Etsy"*) → Settings tab (Header: *"Etsy Settings"*). Route `/admin/apps/etsy` / `apps.etsy.settings`.

## What the merchant can do here

### Installation flow
- Header: *"Install Etsy"*.
- Help text: *"This application will sync your Etsy products and your CloudCart store products. You can push your CloudCart products to Etsy and vise versa."*
- Install description (`info.install`): *"When you install this application you will need to give permission with your Etsy account. Once the permissions are granted you will need to setup few configurations. In no more than 5 minutes you will be able to push all your CloudCart products to your Etsy store. You can also pull your Etsy products to your CloudCart store. And the best thing is that all your Etsy and CloudCart product quantities and prices are synced in real time."*

### Connection settings (Header: "Etsy Settings")
- **Connect your CloudCart store with Etsy** button (`action.connect_with_etsy`) — initiates the OAuth flow.
- **Choose your Etsy store** dropdown (`select_etsy_store`) — when the account has multiple Etsy shops, picks the one to sync.
- **Etsy username** (`username`) — populated post-OAuth.
- **Password in Etsy** (`password`) — a leftover label; not wired to any input (see Business rules).
- *"You do not have any shops in Etsy"* (`info.no_shops`) — error when the connected Etsy account has no shops.

### What the merchant CANNOT do here
- Sync without OAuth-connecting first — the platform throws `err.settings_not_saved` until connected.
- Sync more than **one** Etsy shop per CloudCart store. Multi-shop merchants who want parallel sync need separate CloudCart stores.

## Settings & fields

### Error messages reference
| Error key | When it fires |
|---|---|
| `err.category_not_choosen` | Etsy category not selected for a listing. |
| `err.listing_not_upload_in_store` | Product isn't in the CloudCart store yet. |
| `err.missing_product_id` | Etsy didn't return the sync parameters needed. |
| `err.not_existing_listing` | Product doesn't exist in Etsy. |
| `err.params_not_mapped` | Parameters not synchronised — see [[apps-etsy-listing-config]]. |
| `err.same_params_mapping` | Same Etsy parameter mapped twice. |
| `err.settings_not_saved` | Settings not yet configured (no OAuth connection). |

### Plan gates
This app is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `etsy` | Access gate (install URL) | The install URL `/admin/apps/etsy/install` is blocked when the plan lacks the feature. The app is hidden from the Apps catalog for those plans. |
| `etsy_total_products` | Numeric (global cap) | App-specific cross-task cap on products synced to Etsy. When the cap is hit, additional listings cannot be pushed. |

Lower plans cannot install the app. Existing installs continue working on plan downgrade until the merchant cancels — see [[plan-vs-feature-pack]] for downgrade rules.

## Business rules

### Authentication is OAuth — the "password" field is a leftover label
The only real auth path is OAuth via Etsy. The merchant clicks *"Connect your CloudCart store with Etsy"*, goes through Etsy's OAuth flow, and CloudCart stores the access token + secret. There is no password field in the connection process — the password label visible on screen is not wired to any input.

### Multi-shop — one Etsy account, merchant picks one shop per CloudCart store
After OAuth, CloudCart calls Etsy to list the merchant's shops and surfaces them in a dropdown. The merchant picks ONE shop, and that shop is used for every subsequent sync. To switch shops, the merchant updates this setting — but only one shop is active per CloudCart store at a time.

### Etsy is a trademark
The trademark disclaimer: *"The term 'Etsy' is a trademark of Etsy, Inc. This application uses the Etsy API but is not endorsed or certified by Etsy, Inc."* Merchants should understand they are using a third-party Etsy API client, not an Etsy-built integration.

### Permission
Standard apps permission scope.

## Related

- [[apps-etsy]] — hub.
- [[apps]] — App Store catalogue.
- [[apps-etsy-listing-config]] — what happens after connection: per-listing Etsy metadata + parameter mapping.
- [[apps-etsy-sync-mechanics]] — the runtime sync the connection enables.
- [[settings-api-keys]] — the store API key concept; Etsy connection uses OAuth tokens instead.
- [[plan-gates]] / [[plan-vs-feature-pack]] / [[plan-features]] — the `etsy` + `etsy_total_products` gates.

## Open questions

- Whether the `password` label is fully removed in newer builds or just orphaned in the template (verify).
