---
type: feature
nav_path: "Apps → Multilang → Stores"
route_name: apps.multilang.stores
route_path: /admin/apps/multilang/stores
aliases: ["Multilang Stores", "Sister sites", "Language sites", "Multilang sites"]
tags: [apps, administration, multilang, stores, sister-sites]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 4
---

# Multilang → Stores

## Purpose

The **Stores** tab is where the merchant manages their **sister sites** — additional language-specific storefronts created via the Multilang app. Per [[apps-multilang]] the model is **one master site + N sister sites** (one per language). From this tab the merchant lists those sites, adds new ones, configures how each is fed from the master, and tears them down.

This topic is split into three aspect pages because each covers a distinct concept: the list view, the per-sister settings, and the structural network rules. The Assistant should drill into the aspect that matches the question, not read all three.

## Where to find it

Sidebar → Apps → Multilang → **Stores tab**. Route: `/admin/apps/multilang/stores`. For the full Multilang feature set, see [[apps-multilang]].

## What the merchant can do here

- **List + manage sister sites** — read each site's language, status, domain, sync state; add / edit / pause / delete; toggle the global "Show language versions on the site" switcher. See [[apps-multilang-stores-table]].
- **Configure how each sister is fed from the master** — copy toggle, 9 per-field translation toggles, price transform, approval method, URL handling, per-sister switcher visibility. See [[apps-multilang-stores-config-modal]].
- **Understand + control the network structure** — link an owned store, switch into a sister's admin via SSO, delete a sister, or uninstall (which cascades). See [[apps-multilang-stores-network]].

## Sub-pages (in this cluster)

- [[apps-multilang-stores-table]] — the sister-sites list view: columns, status / progress-state badges, empty state, the footer "Show language versions" toggle, row actions, per-site flag iconography.
- [[apps-multilang-stores-config-modal]] — the per-sister Configuration modal: the products copy toggle, 9 AI-translation field toggles, price multiplier + rounding, approval method, automatic delete, URL manipulation; instant save semantics; the two plan-quota gates.
- [[apps-multilang-stores-network]] — network mechanics: master-vs-sister identification (`main_site`), ownership-gated linking, per-sister currency / theme / catalog separability, auto-installed prerequisite apps, DNS/SSL provisioning, cross-site SSO, hard delete, and the master-uninstall cascade.

## Settings & fields

The two settings most asked about live on the aspect pages:

- **`settings.show_language`** (footer toggle) — storefront language-switcher visibility, stored per sister. See [[apps-multilang-stores-table]].
- **Per-sister Configuration modal** — `settings.products`, `settings.translate.*` (9 fields), `settings.price` / `settings.price_change` / `settings.price_round`, `settings.method`, `settings.delete`, `settings.show_version`, `settings.url_manipulation` / `settings.url_remove`. See [[apps-multilang-stores-config-modal]].

## Business rules

- **One master, N sisters.** A site is the master when its `main_site` setting is empty; sisters point at the master's site_id. See [[apps-multilang-stores-network]].
- **Sisters are independent CloudCart stores** — separable currency, theme, and catalog. See [[apps-multilang-stores-network]].
- **Translation sync is triggered per sister** — changing a product on the master fires the `multilang_product_translate` / `multilang_product_copy` queue tasks for each eligible sister; `last_sync` updates per successful run. See [[apps-multilang]].
- **Delete is a hard delete; master uninstall cascades to every sister.** See [[apps-multilang-stores-network]].

### Permission

Standard apps permission scope.

## Related

- [[apps-multilang]] — Multilang feature hub.
- [[apps-multilang-create-step]] — sister-site creation wizard.
- [[apps-multilang-products]] — per-product translation across sites.
- [[apps-multilang-progress]] — sync progress.
- [[apps-multilang-settings]] — master-level feature toggles.
- [[apps-lets-encrypt]] — SSL certs for sister-site domains.
- [[settings-domains]] — domain configuration.

## Open questions

None — uncertainties distributed to the aspect pages.
