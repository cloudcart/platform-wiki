---
type: concept
nav_path: "Concept → Headless storefronts → Nitrogen overview"
aliases: ["Nitrogen overview", "Nitrogen storefront limits", "Handle hash", "Storefronts per site limit", "Headless permissions", "Headless plan gates"]
tags: [nitrogen, headless, storefront-api, limits, permissions, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-11-04
source_count: 3
---

> Part of [[headless-storefront]]. See the hub for the other aspects (deployment methods, Nova platform, Storefront API, customer accounts, environment variables, legacy-vs-Nitrogen surfaces).

# Headless — Nitrogen overview

## Definition

**Nitrogen** is CloudCart's official headless system: an end-to-end stack that lets a merchant ship a custom frontend against the same CloudCart backend that powers legacy themes. Its library, `@cloudcart/nitrogen`, and its starter are a React Router app, and the GitHub workflow builds with `npx react-router build`. This page documents the **shape of the Nitrogen storefront object** (handle, limits, coexistence rules) — NOT the deploy flow or the API surface (those live in sibling aspects).

A single CloudCart site can host **multiple Nitrogen storefronts** side-by-side, each with its own codebase, deployment branch and environment variables. They all read from the same product / customer / order tables — the merchant manages catalog from a single admin regardless of how many Nitrogen storefronts they run.

## Scope

Covered here:

- Handle format and the 16-character hex hash.
- The three platform-wide caps (storefronts per site, custom variables per storefront, deployment tokens per storefront).
- Coexistence with legacy themes on the same site.
- Permission gating + plan-gate situation.
- The admin surfaces that expose Nitrogen to the merchant.

Not covered here:

- Deployment mode (CLI vs GitHub) — see [[headless-deployment-methods]].
- Nova/Cloudflare runtime and provisioning — see [[headless-nova-platform]].
- The `/api/sf` GraphQL endpoint + tokens — see [[headless-storefront-api]].
- Customer-account login — see [[headless-customer-accounts]].
- Variables — see [[headless-environment-variables]].
- Which paths stay on the platform on a routed domain — see [[headless-legacy-vs-nitrogen]].

## Contrasts

- **Nitrogen vs legacy theme** — legacy themes are fully managed by CloudCart and work out of the box. Nitrogen storefronts are custom apps the merchant builds and maintains, with full UI / framework control. The two **coexist** on the same CloudCart backend; the storefront's **Domains** tab decides which serves a domain. The full comparison is on [[nitrogen-vs-themes]].

## Where it applies

### Handle format — slug + 16-character hex hash

The storefront's handle is generated at creation as `{slug}-{16-char hex hash}` (e.g., `my-store-a3f8b2c1d4e59f01`), and its address is `{handle}.cloudcart.dev`. Two storefronts with the same name therefore get different addresses. See [[headless-nova-platform]].

### Three platform caps — NOT per-plan-tier

- **Storefronts per site** — **10**. The list on [[nitrogen-storefronts]] shows `Storefronts: {total} / {max}` and disables **Create storefront** at the limit. The refusal: *"Maximum of 10 storefronts allowed per site"*.
- **Custom variables per storefront** — **50**; read-only variables don't count. See [[headless-environment-variables]].
- **Deployment tokens per storefront** — **10**. The refusal: *"Maximum of 10 deployment tokens allowed per storefront"*. See [[headless-deployment-methods]].

All three are platform-wide. Plans that have Nitrogen access all see the same caps.

### Coexistence with legacy themes

A store can run its theme and up to 10 Nitrogen storefronts at the same time. The theme serves the store's domains by default. Every storefront answers on its own `{handle}.cloudcart.dev` address. One storefront at a time may serve the store's domains: routing a domain is done on that storefront's **Domains** tab, and a second storefront is refused with *"Another storefront already serves this site — remove it first"*. See [[headless-nova-platform]].

**Back to the store theme** on that tab returns a domain to the theme. The storefront's own address does not change either way.

### Same CloudCart data backs every storefront

Products, categories, customers, orders, settings, content (CMS pages, blog) all live in the merchant's CloudCart admin. Whether a customer browses via the legacy theme or via a Nitrogen storefront, they see the same catalog and place orders into the same order list. Metafields and metaobjects reach customers only through a Nitrogen storefront ([[metafields-nitrogen]]).

### Permissions

Access to the whole Nitrogen area needs the **Nitrogen Storefronts** permission (see [[nitrogen]]): the store owner always has it, a moderator only when it is granted in [[settings-staff]].

### Plan gates

Nitrogen itself does not have a published `plan_gate` key (verify). Certain scopes (`write_customers`, `read_orders`, `read_bulk_operations`) may be implicitly gated by the merchant's plan capabilities (verify). Trial and expired stores still reach the admin screens. On a domain routed to a storefront the platform answers `/robots.txt`, so the `Disallow: /` block applies there as on any store — see [[headless-legacy-vs-nitrogen]].

### Deletion — full teardown

Deleting a storefront, from [[nitrogen-storefronts]] or its General tab:

- Removes it from Nova with its address, and sends a domain routed to it back to the store's theme — see [[headless-nova-platform]].
- Revokes its Storefront API tokens.
- Deletes its deployment history, variables and deployment tokens.
- Leaves the repository on GitHub untouched.

The list's confirmation reads: *"Delete this storefront? It is removed from Nova with its address, deployments and tokens, and a domain routed to it shows the store's theme again."* On the General tab the merchant types the storefront's name to confirm. Deletion is immediate and irreversible.

### Admin surfaces

- [[nitrogen]] — hub page for the Nitrogen feature.
- [[nitrogen-storefronts]] — list of all Nitrogen storefronts with Create / Delete actions and the per-site limit counter.
- [[nitrogen-create-storefront]] — creation wizard (name + deployment method).
- [[nitrogen-storefront-overview]] — per-storefront page with tabs Overview, General, Environments and variables, Deployments, Storefront API, Domains.
- [[nitrogen-deployments]] — full deployment history per storefront.
- [[settings-domains]] — where a domain joins the store, before the storefront's Domains tab can route it.

## Related

- [[headless-storefront]] — hub.
- [[nitrogen-vs-themes]] — Nitrogen compared with a standard theme.
- [[metafields-metaobjects]] — the store's own fields and content types.
- [[nitrogen]] — Nitrogen admin hub.
- [[nitrogen-storefronts]] — storefront list with the per-site limit counter.
- [[nitrogen-create-storefront]] — creation wizard.
- [[nitrogen-storefront-overview]] — per-storefront detail and tabs.
- [[settings-domains]] — where a domain joins the store.
- [[plan-gates]] — how implicit scope-gating relates to the merchant's plan.

## Open Questions

- Whether any storefront-creation surface enforces a plan-feature key (not just the per-site cap).
