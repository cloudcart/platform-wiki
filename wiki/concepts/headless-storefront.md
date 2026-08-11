---
type: concept
nav_path: "Concept → Headless storefronts"
route_name: ""
route_path: ""
aliases: ["Headless", "Headless storefront", "Headless commerce", "Decoupled storefront", "Nitrogen", "Nitrogen storefronts", "CloudCart Nitrogen", "Custom storefront", "API-driven storefront", "Headless e-commerce", "Безглав магазин", "Хедлес магазин", "Хедлес"]
tags: [nitrogen, headless, storefront-api, customer-account-api, deployments, concepts]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 7
---

# Headless storefronts (Nitrogen)

## Definition

A **headless storefront** is a customer-facing storefront where the frontend is built and deployed independently from the CloudCart admin panel — the merchant's store backend (products, categories, customers, orders, checkout, payments, settings) remains in CloudCart, but the customer's actual shopping experience runs on a custom application written in Next.js, Nuxt, SvelteKit, Remix, Astro, or any other frontend framework. The frontend fetches data from CloudCart's APIs at runtime, renders its own HTML / CSS / JavaScript, and handles everything the customer sees.

**Nitrogen** is CloudCart's official headless system. It bundles:

- A managed deployment platform called **Nova** that hosts the merchant's storefront app on a `*.nova.cloudcart.dev` subdomain (Cloudflare Workers-for-Platforms backend) — see [[headless-nova-platform]].
- Per-storefront **Storefront API tokens** (public + private) authenticating calls to the `/api/sf` GraphQL endpoint — see [[headless-storefront-api]].
- A scoped permissions model (`read_products`, `read_customers`, `read_checkouts`, `write_checkouts`, etc.) — see [[headless-storefront-api]].
- A **Customer Account API** for passwordless 6-digit email-code login — see [[headless-customer-accounts]].
- Two locked-at-creation deployment methods — **CloudCart CLI / manual CI-CD** or **GitHub integration** — see [[headless-deployment-methods]].
- Per-environment env vars (production + preview; system + custom + secret kinds) — see [[headless-environment-variables]].
- Per-storefront deployment history with commit SHA, branch, status, deployed URL, and live screenshot — see [[nitrogen-deployments]].

This is **decoupled commerce** — the merchant runs the storefront codebase as their own application with full UI / framework / performance control, while CloudCart handles catalog, orders, payments, and inventory.

## Sub-pages (in this cluster)

This concept is split into 7 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[headless-nitrogen-overview]] — handle format + 16-hex hash; the three platform caps (storefronts / env vars / deploy tokens); coexistence with legacy themes; permissions; plan-gate situation; admin surfaces.
- [[headless-deployment-methods]] — CLI vs GitHub modes; `cloudcart nitrogen deploy`; GitHub App + repo secrets + workflow YAML; new-repo direct-commit vs existing-repo PR; non-Nitrogen-project skip step; Nova deploy tokens; refresh-token rotation.
- [[headless-nova-platform]] — Cloudflare Workers-for-Platforms backend; production + preview namespaces; provisioning (two Cloudflare API calls); deletion teardown (Worker delete + KV bulk-delete + custom-domain unmap); custom-domain attachment.
- [[headless-storefront-api]] — `/api/sf` GraphQL endpoint (POST + GET + downloads + playground); required headers; public vs private tokens (`cc_nit_` prefix, SHA-256 hash storage); default + full scope catalogue.
- [[headless-customer-accounts]] — the active 6-digit email-code login flow; the customer JWT; `nitro_customer_accounts` record with OAuth scaffold fields (stored, not yet enforced); default `customer_*` scopes.
- [[headless-environment-variables]] — production + preview environments; system / custom / secret kinds; auto-populated system vars (`PUBLIC_STOREFRONT_API_TOKEN`, `PUBLIC_STORE_DOMAIN`, `PUBLIC_STOREFRONT_ID`, `SHOP_ID`, `SESSION_SECRET`); the 50-var cap; why `SESSION_SECRET` is NEVER rotated.
- [[headless-legacy-vs-nitrogen]] — the gap map: `/robots.txt`, `/sitemap.xml`, 301 redirects, plan-expired `Disallow: /` override, cart-bubble JS, payment-provider redirect, hosted `/orders/<id>` confirmation, multi-domain language pinning — what legacy serves and what Nitrogen must re-implement.

## Why it matters to the merchant

Two scenarios push merchants from legacy CloudCart themes toward Nitrogen:

- **Custom UX requirements legacy themes cannot deliver** — non-standard catalog layouts, custom interactive components (configurator, builder, comparison tool), heavy frontend integrations (custom search, AR product viewers, complex personalization), image-heavy / mobile-first PWAs, or design requiring a modern frontend stack (React, Vue) the merchant's team already uses.
- **Multi-touchpoint commerce** — the merchant wants the SAME CloudCart backend to power multiple consumer-facing surfaces: a website, a native mobile app, a smart-mirror in a physical store, a chatbot. Each surface consumes the same Storefront API — see [[headless-storefront-api]].

The trade-off is operational: the merchant BUILDS and MAINTAINS the storefront application themselves (or hires a developer). With legacy themes the merchant gets a working storefront out of the box; with Nitrogen they get API tokens and a deployment platform, but must build the storefront from scratch.

A merchant who just wants a working online store should use a legacy CloudCart theme. A merchant whose business model requires bespoke frontend, multi-surface delivery, or developer-team frontend ownership should use Nitrogen.

## Scope

What this cluster covers (across the 7 sub-pages):

- Nitrogen as CloudCart's official headless system.
- Nova managed deployment platform on Cloudflare Workers.
- Per-storefront Storefront API tokens (public + private) and scope set.
- Customer Account API + the passwordless email-code flow.
- The two deployment methods (CLI / CI-CD vs GitHub).
- Environment variables (production + preview; system + custom + secret).
- Per-storefront deployment history with commit / branch / status / URL / screenshot.
- Coexistence with legacy themes on the same CloudCart site.
- Which legacy-only endpoints do NOT auto-appear on a Nitrogen custom domain.

What it does NOT cover:

- The frontend codebase the merchant writes — that's the merchant's responsibility.
- Cloudflare Workers low-level infrastructure beyond what Nova abstracts.
- The Storefront API's specific GraphQL types and payload shapes — see external API docs.
- Multi-storefront / multi-business with different catalogs — see [[apps-stores]].

## Contrasts

- **Nitrogen vs legacy theme** — see [[headless-nitrogen-overview]] for coexistence rules and [[headless-legacy-vs-nitrogen]] for the surface gap map.
- **Nitrogen vs Stores** — Nitrogen = different STOREFRONT for same catalog; [[apps-stores]] = different CATALOGS / brands.
- **Storefront API tokens vs Nova deploy tokens** — different tabs, different rotation. See [[headless-storefront-api]] vs [[headless-deployment-methods]].
- **Public vs private Storefront API token** — see [[headless-storefront-api]].
- **CLI mode vs GitHub mode** — locked at creation, can't switch. See [[headless-deployment-methods]].
- **Production vs preview environments** — separate Cloudflare namespaces, separate env-var sets. See [[headless-nova-platform]] + [[headless-environment-variables]].

## Where it applies

Nitrogen spans dedicated admin screens, deployment surfaces external to CloudCart (CLI, GitHub), and integrates with other admin features. Each sub-page documents its own surface in detail. The cross-cutting touch-points are:

- **Admin surfaces** — [[nitrogen]], [[nitrogen-storefronts]], [[nitrogen-create-storefront]], [[nitrogen-storefront-overview]], [[nitrogen-deployments]], [[settings-domains]].
- **CLI / external surfaces** — the `cloudcart` command-line tool, the merchant's GitHub repository (workflow YAML + secrets), the Nova-hosted URL (`<handle>.nova.cloudcart.dev` or custom domain), the merchant's local dev environment.
- **Cross-feature** — [[customer]] (Customer Account API), [[domain]] + [[settings-domains]] (custom domain attachment), [[seo-handling]] (legacy-only override doesn't propagate), [[plan-gates]] (implicit scope gating), [[multi-language]] (per-domain language is legacy-only).

## Related

- [[nitrogen]] — Nitrogen admin hub.
- [[nitrogen-storefronts]] — storefront list + creation.
- [[nitrogen-create-storefront]] — creation wizard.
- [[nitrogen-storefront-overview]] — per-storefront detail with the four tabs.
- [[nitrogen-deployments]] — deployment history.
- [[settings-domains]] — custom-domain attachment.
- [[apps-stores]] — multi-business multi-catalog (contrast).
- [[customer]] — Customer Account API authenticates customers.
- [[domain]] — custom domain entity.
- [[seo-handling]] — SEO mechanics; legacy-only override does NOT propagate to Nitrogen.
- [[multi-language]] — multi-language content delivery; per-domain language pinning is legacy-only.
- [[plan-gates]] — plan-feature gating that affects some scopes.
- [[json-api-v2]] — the OTHER GraphQL endpoint and how it differs.

## Open Questions

- ⏸️ Pricing for Nitrogen / Nova — whether deployments / bandwidth / Worker CPU time are billed separately from the base CloudCart plan. This is a billing-policy decision (not in code) and merchants on Nitrogen should check current pricing at https://cloudcart.com/pricing or with their account manager.

Aspect-specific Open Questions are documented on each sub-page.
