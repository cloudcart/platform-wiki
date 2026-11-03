---
type: feature
nav_path: "Apps → Multilang → Stores → Network mechanics"
route_name: apps.multilang.stores
route_path: /admin/apps/multilang/stores
aliases: ["Multilang network mechanics", "Master vs sister site", "Multilang cross-site login", "Multilang uninstall cascade", "Sister site provisioning", "Multilang bundled apps"]
tags: [apps, administration, multilang, stores, sister-sites, provisioning]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[apps-multilang-stores]]. See the hub for the other aspects (sister-sites table, Configuration modal).

# Multilang → Stores — network mechanics

## Purpose

This page documents the **structural rules of a Multilang network** — what makes a site the master vs a sister, how sister sites are provisioned (domain / SSL / bundled apps), how the merchant moves between sites via cross-site login, what is and isn't shared between master and sister (currency, theme, catalog), and what happens on delete / uninstall. These are the behaviours behind the buttons on the [[apps-multilang-stores-table|Stores table]] — verified against the backend — that the merchant must understand before tearing down or restructuring a network.

## Where to find it

The actions described here are triggered from Sidebar → Apps → Multilang → **Stores tab** (`/admin/apps/multilang/stores`) — the add, switch, delete, and uninstall controls. The rules themselves are platform behaviour, not a separate screen.

## What the merchant can do here

- Add a sister site by linking an existing CloudCart store they own, or provisioning a new one.
- Switch into a sister site's own admin without re-entering credentials (cross-site SSO).
- Delete a single sister site (detaches + removes it).
- Uninstall Multilang on the master (tears down the whole network).

## Settings & fields

This aspect has no form fields of its own — the configurable per-sister fields live in the [[apps-multilang-stores-config-modal|Configuration modal]]. The structural state the platform tracks per network:

| State | Meaning |
|---|---|
| `main_site` (empty) | This site is the **master**. |
| `main_site` (= master's site_id) | This site is a **sister** pointing at that master. |
| `@app_multylanguage_sites` row | One row per sister in the master's Sites table. |

## Business rules

### Master site identifies itself by ABSENCE of `main_site`

A site is the **master** when its Multilang `main_site` setting is empty. Sisters have `main_site` set to the master's site_id. This is the only way the platform distinguishes which site is the master. Two sister sites in one chain can't both think they're master — the `main_site` setting must point to exactly one master for the network to function.

### Linking an existing store requires merchant ownership

The existing-site picker shows only the CURRENT merchant's own sites. The merchant can only link sister sites that already belong to them (under the same user account); they can't link someone else's CloudCart store. This ownership check is driven at the user-account level, not by domain DNS verification.

### Currency CAN differ per sister site

The create-new-site flow accepts a `currency` field independent of the master's currency. Each sister site is provisioned as a CloudCart store with its own currency setting — so a Bulgarian sister can use BGN while a Romanian sister uses RON. Per-site currency is stored as part of the standard site settings, not as a Multilang-specific override.

### Theme is seeded from the master, then independent

When a new sister site is provisioned, it copies the master's theme/template ID as its starting template. After install, the sister is an independent CloudCart site with its own theme — the merchant can switch the sister's theme via its own admin (using cross-site login) without affecting the master.

### Sister catalogs are fully separable from the master's

The sister site is a separate CloudCart store; its catalog is fully separable from the master's — same engine, different products allowed. The per-sister `products` setting (in the [[apps-multilang-stores-config-modal|Configuration modal]]) controls whether new master products are copied automatically. With copy OFF the sister catalog stays manually curated, and the merchant can add/remove specific products via [[apps-multilang-products]].

### New sisters auto-install a bundle of prerequisite apps

The integration installs a bundle of related apps on each sister: `gdpr`, `lets_encrypt`, `stores-sync`, `domain_redirect`, `bumper_offer`. A new sister gets these auto-installed alongside Multilang — the merchant doesn't opt in; they're prerequisites for the sister's operation (`lets_encrypt` for SSL, `domain_redirect` for canonical-domain handling, `stores-sync` for quantity sync between master + sister).

### Domain not auto-verified at submit; checked when LetsEncrypt provisions

The submitted domain is stored on the new site record and the install job is dispatched. DNS is **NOT** auto-checked at submit time. The downstream install workflow (including [[apps-lets-encrypt]] for SSL) verifies DNS during cert provisioning. If DNS isn't pointing yet, the sister site lands in a Pending state on the Stores tab; the merchant fixes DNS and the cert workflow retries. Each sister typically has its own domain or subdomain (e.g., `en.merchant.com`, `merchant.ro`) — see [[settings-domains]].

### Cross-site admin SSO via one-time login code

The "Switch to this sister" admin button mints a one-time code and redirects to `<sister_url>/admin/login?code=<code>&target=<deep-link>`. The sister site recognises the code, authenticates the same owner without re-entering credentials, and lands them on the deep-link target. If the master admin is a moderator (not owner), the platform looks up the same moderator's email on the sister site and generates the code for THAT admin if it exists.

### Delete is a HARD delete — no grace period

The delete action removes the `@app_multylanguage_sites` row immediately, then queues `multylang_sites` to propagate the removal. There is no "trash" / "restore within 30 days" UI flow on Multilang's side. The underlying CloudCart Site record (the sister storefront itself) follows its own deletion lifecycle (per [[apps-stores]] and the broader platform). Side effects of delete: the sister's domain stops resolving; translation data is retained for some period (verify) then purged; customers who bookmarked the sister domain land on a 404.

### Master uninstall cascades to every sister; sister uninstall just detaches

The master's uninstall flow iterates EVERY sister site and runs the uninstall + queues `multylang_sites` cleanup on each. **One uninstall click on the master tears down the whole network.** A sister site uninstalling Multilang independently just removes its row from the master's Sites table — the master remains operational, other sisters remain operational, and only that one sister disconnects from sync.

## Related

- [[apps-multilang-stores]] — hub.
- [[apps-multilang-stores-table]] — the list view these actions are triggered from.
- [[apps-multilang]] — Multilang feature hub; translation queue tasks.
- [[apps-multilang-products]] — per-product translation / manual catalog curation.
- [[apps-lets-encrypt]] — SSL certs for sister-site domains; the DNS-verification gate.
- [[apps-stores]] — underlying CloudCart Site lifecycle.
- [[settings-domains]] — sister-site domain configuration.

## Open questions

- Confirm the retention period before deleted-sister translation data is purged.
