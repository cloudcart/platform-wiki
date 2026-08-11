---
type: concept
nav_path: "Concept → Headless storefronts → Nitrogen overview"
aliases: ["Nitrogen overview", "Nitrogen storefront limits", "Handle hash", "Storefronts per site limit", "Headless permissions", "Headless plan gates"]
tags: [nitrogen, headless, storefront-api, limits, permissions, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[headless-storefront]]. See the hub for the other aspects (deployment methods, Nova platform, Storefront API, customer accounts, environment variables, legacy-vs-Nitrogen surfaces).

# Headless — Nitrogen overview

## Definition

**Nitrogen** is CloudCart's official headless system: an end-to-end stack that lets a merchant ship a custom frontend (Next.js, Nuxt, SvelteKit, Remix, Astro, etc.) against the same CloudCart backend that powers legacy themes. This page documents the **shape of the Nitrogen storefront object** (handle, limits, coexistence rules) — NOT the deploy flow or the API surface (those live in sibling aspects).

A single CloudCart site can host **multiple Nitrogen storefronts** side-by-side, each with its own codebase, framework, deployment branch, scope set, and environment variables. They all read from the same product / customer / order tables — the merchant manages catalog from a single admin regardless of how many Nitrogen storefronts they run.

## Scope

Covered here:

- Handle format and the 16-character hex hash.
- The three platform-wide caps (storefronts per site, custom env vars per storefront, Nova deploy tokens per storefront).
- Coexistence with legacy themes on the same site.
- Permission gating + plan-gate situation.
- The admin surfaces that expose Nitrogen to the merchant.

Not covered here:

- Deployment mode (CLI vs GitHub) — see [[headless-deployment-methods]].
- Nova/Cloudflare runtime and provisioning — see [[headless-nova-platform]].
- The `/api/sf` GraphQL endpoint + tokens — see [[headless-storefront-api]].
- Customer-account login — see [[headless-customer-accounts]].
- Env-var production/preview model — see [[headless-environment-variables]].
- What legacy-only endpoints (`/robots.txt`, `/sitemap.xml`, 301 redirects) do NOT auto-serve on Nitrogen — see [[headless-legacy-vs-nitrogen]].

## Contrasts

- **Nitrogen vs legacy theme** — legacy themes are Smarty-rendered, fully managed by CloudCart, working out of the box. Nitrogen storefronts are custom apps the merchant builds and maintains, with full UI / framework control. The two **coexist** on the same CloudCart backend; DNS / domain attachment on [[settings-domains]] decides which serves which hostname.
- **Nitrogen vs Stores** — Nitrogen is a different STOREFRONT for the **same** catalog. [[apps-stores]] is a multi-business feature for **different** catalogs / brands.

## Where it applies

### Handle format — slug + 16-character hex hash

The storefront's handle (used as the Nova subdomain) is generated at creation as `{slug}-{16-char hex hash}` (e.g., `my-store-a3f8b2c1d4e59f01`). The 16-character random hash is `bin2hex(random_bytes(8))` — guaranteed unique (verify). This prevents subdomain-hijack attempts via name collision and means even two merchants with the same storefront name get different Nova URLs.

### Three platform caps — NOT per-plan-tier

The platform enforces THREE hard caps via the platform code (verify):

- **`limits.max_storefronts_per_site`** — default **10**. The "Create Storefront" button on [[nitrogen-storefronts]] is disabled when the merchant reaches the limit, with a counter showing "X of N storefronts" in the header.
- **`limits.max_env_variables_per_storefront`** — default **50** custom env vars per storefront; system variables don't count. See [[headless-environment-variables]].
- **`limits.max_nova_tokens_per_storefront`** — default **10**; attempting to create an 11th raises an error. See [[headless-nova-platform]].

All three are **global platform config**, NOT per-plan-tier. Plans that have Nitrogen access all see the same caps.

### Coexistence with legacy themes

A CloudCart site can run a legacy storefront AND one or more Nitrogen storefronts at the same time. The legacy theme serves the primary store URL by default; each Nitrogen storefront serves either its Nova hostname or a custom-attached domain. Customers visiting different domains see different storefronts (legacy or Nitrogen) all powered by the same products / orders / customers.

When the merchant moves a custom domain from legacy to Nitrogen (or vice versa), DNS / domain attachment on [[settings-domains]] determines which storefront serves that domain. The Nova hostname (`<handle>.nova.cloudcart.dev`) stays unchanged so existing deployments keep working even if the merchant repoints the customer-facing domain.

### Same CloudCart data backs every storefront

Products, categories, customers, orders, settings, content (CMS pages, blog) all live in the merchant's CloudCart admin. Whether a customer browses via the legacy theme or via a Nitrogen storefront, they see the same catalog and place orders into the same order list.

### Permissions

Access to the entire Nitrogen system is gated behind the standard staff-permission tree. Moderators without the relevant permission don't see the Nitrogen sidebar entry. Within Nitrogen, the merchant grants scoped permissions to individual storefronts via the Storefront API scope picker — see [[headless-storefront-api]] — but those scopes govern what the deployed APP can do, not what the merchant's staff can do in the admin UI.

### Plan gates

Nitrogen itself does NOT have a published `plan_gate` key in the codebase (verify) — but the per-site storefront cap is configurable per plan, and certain scopes (`write_customers`, `read_orders`, `read_bulk_operations`) may be implicitly gated by the merchant's plan capabilities. Trial / `plan_expired` stores still have access to the admin screens but their deployed Nitrogen storefronts inherit the same SEO restrictions as the legacy storefront (e.g., `Disallow: /` in robots.txt is enforced by the legacy storefront only — see [[headless-legacy-vs-nitrogen]] for the carve-out).

### Deletion — full teardown

Deleting a storefront from [[nitrogen-storefronts]]:

- Deprovisions the Cloudflare Worker (the Nova hostname stops resolving) — see [[headless-nova-platform]] for the exact API calls.
- Revokes the Storefront API tokens.
- Deletes the deployment history, environment variables, and Nova deploy tokens.
- Removes the Customer Account API credentials if present.

The merchant sees a confirmation modal: *"Are you sure you want to delete this storefront? All tokens and deployments will be removed."* Deletion is immediate and irreversible.

### Admin surfaces

- [[nitrogen]] — hub page for the Nitrogen feature.
- [[nitrogen-storefronts]] — list of all Nitrogen storefronts with Create / Delete actions and the per-site limit counter.
- [[nitrogen-create-storefront]] — creation wizard (name + deployment method).
- [[nitrogen-storefront-overview]] — per-storefront detail screen with the Overview banner (live URL, screenshot, deployment status) plus tabs for Storefront API / Customer Account API / Nova Deployments / Environments & Variables.
- [[nitrogen-deployments]] — full deployment history per storefront.
- [[settings-domains]] — where the merchant attaches a custom domain to a Nitrogen storefront's Nova hostname.

## Related

- [[headless-storefront]] — hub.
- [[nitrogen]] — Nitrogen admin hub.
- [[nitrogen-storefronts]] — storefront list with the per-site limit counter.
- [[nitrogen-create-storefront]] — creation wizard.
- [[nitrogen-storefront-overview]] — per-storefront detail and tabs.
- [[settings-domains]] — domain attachment.
- [[apps-stores]] — different-catalogs multi-business (contrast).
- [[plan-gates]] — how implicit scope-gating relates to the merchant's plan.

## Open Questions

- `limits.*` config keys — verify exact path under the platform code and confirm defaults (10 / 50 / 10) against current code.
- Whether any storefront-creation surface enforces a plan-feature key (not just per-site config cap).
