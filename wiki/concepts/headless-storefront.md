---
type: concept
nav_path: "Concept → Headless storefronts"
route_name: ""
route_path: ""
aliases: ["Headless", "Headless storefront", "Headless commerce", "Decoupled storefront", "Nitrogen", "Nitrogen storefronts", "CloudCart Nitrogen", "Custom storefront", "API-driven storefront", "Headless e-commerce", "Безглав магазин", "Хедлес магазин", "Хедлес"]
tags: [nitrogen, headless, storefront-api, customer-account-api, deployments, concepts]
plan_gates: []
created: 2026-05-23
updated: 2026-11-03
source_count: 12
---

# Headless storefronts (Nitrogen)

## Definition

A **headless storefront** is a customer-facing storefront where the frontend is built and deployed independently from the CloudCart admin panel. The merchant's store backend (products, categories, customers, orders, checkout, payments, settings) remains in CloudCart, while the customer's shopping experience runs on a custom application that fetches data from CloudCart's APIs at runtime and renders everything the customer sees.

**Nitrogen** is CloudCart's official headless system: a React Router library and starter (`@cloudcart/nitrogen`), the `cloudcart` CLI, and:

- A managed hosting platform called **Nova** that serves the storefront at `{slug}.cloudcart.dev`, and on a store domain routed to it — see [[headless-nova-platform]].
- Per-storefront **Storefront API tokens** (public + private) for the `/api/sf` GraphQL endpoint — see [[headless-storefront-api]].
- Customer sign-in by a 6-digit e-mail code — see [[headless-customer-accounts]].
- Two locked-at-creation deployment methods, **Command line or CI/CD** and **GitHub** — see [[headless-deployment-methods]].
- Variables bound at deploy (read-only, custom, secret) — see [[headless-environment-variables]].
- A deployment history with commit, branch, status and address — see [[nitrogen-deployments]].

This is **decoupled commerce**: the merchant runs the storefront codebase as their own application, while CloudCart handles catalog, orders, payments, and inventory.

## Sub-pages (in this cluster)

This concept is split into 15 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

**The storefront and its hosting**

- [[headless-nitrogen-overview]] — handle format; the three platform caps (storefronts, variables, deployment tokens); coexistence with the store's theme; permissions; plan-gate situation; admin surfaces.
- [[headless-deployment-methods]] — command line vs GitHub; what is written to the repository; the `nova-deploy.yml` workflow; new vs existing repository; deployment tokens; the GitHub account row.
- [[headless-nova-platform]] — only production is served; the `{slug}.cloudcart.dev` address; routing a store domain and its refusals; asset and page caching; deleting a storefront.
- [[headless-environment-variables]] — read-only names (`PUBLIC_STOREFRONT_API_TOKEN`, `PRIVATE_STOREFRONT_API_TOKEN`, `PUBLIC_STORE_DOMAIN`, `PUBLIC_API_ORIGIN`, `SESSION_SECRET`); key rules; the 50-variable cap; `batchSetNitrogenEnvironmentVariables` and `env push`.
- [[headless-legacy-vs-nitrogen]] — the paths the platform keeps on a routed domain (`/robots.txt`, `/llms.txt`, sitemap, feeds, checkout, payments); 301 redirects; e-mail links; languages; the private store.

**The Storefront API**

- [[headless-storefront-api]] — `/api/sf` GraphQL endpoint (POST + GET + downloads + playground); required headers; public vs private tokens; scope catalogue.
- [[headless-storefront-limits]] — per-visitor limits and `THROTTLED`; list caps and their refusals; page sizes; the return flow's code; `X-Request-Id`.
- [[headless-customer-accounts]] — the 6-digit e-mail code; the customer token; registration through the API; sign-in refusals.
- [[headless-catalogue-reads]] — linked and related products, product tabs, quantity tiers, categories, `node`; what is left out; the private store and prices for signed-in customers.
- [[headless-product-listing-order]] — the default order of product listings, what each `sortKey` does, listing smart collections.
- [[headless-cart-rules]] — warnings; required and measured customizations; swaps; the 50-line rule; a customization's file; who the buyer is; discounts on the cart.
- [[headless-offers]] — cross-sell and up-sell: `offerHistory`, taking an offer, counting views and dismissals.
- [[headless-checkout-submit]] — `checkoutUrl`, `cartSubmitForCompletion`, consents, retries; CloudCart Pay's embedded form and its repeated `form_validation`; fast order.
- [[headless-cloudcart-pay]] — CloudCart Pay's express buttons: when to show them, Apple Pay and `X-Storefront-Host`, the wallet e-mail rule, settling a cart.
- [[headless-analytics-consent]] — `analyticsEventPublish`, event ids, what a refusal stops, the `cookieConsent` banner.

## Why it matters to the merchant

Two scenarios push merchants from legacy CloudCart themes toward Nitrogen:

- **Custom UX requirements legacy themes cannot deliver** — non-standard catalog layouts, custom interactive components (configurator, builder, comparison tool), heavy frontend integrations (custom search, AR product viewers, complex personalization), image-heavy / mobile-first PWAs, or design requiring a modern frontend stack (React, Vue) the merchant's team already uses.
- **Multi-touchpoint commerce** — the merchant wants the SAME CloudCart backend to power multiple consumer-facing surfaces: a website, a native mobile app, a smart-mirror in a physical store, a chatbot. Each surface consumes the same Storefront API — see [[headless-storefront-api]].

The trade-off is operational: the merchant BUILDS and MAINTAINS the storefront application themselves (or hires a developer). With legacy themes the merchant gets a working storefront out of the box; with Nitrogen they get API tokens and a deployment platform, but must build the storefront from scratch.

A merchant who just wants a working online store should use a legacy CloudCart theme. A merchant whose business model requires bespoke frontend, multi-surface delivery, or developer-team frontend ownership should use Nitrogen.

## Scope

What this cluster covers:

- Nitrogen as CloudCart's official headless system, and Nova hosting.
- The Storefront API: tokens, sign-in, limits, and the rules of its catalogue, cart, offers, checkout and analytics.
- Deployment methods, variables and deployment history.
- Coexistence with the store's theme, and what a routed domain keeps on the platform.

What it does NOT cover:

- The frontend codebase the merchant writes — that's the merchant's responsibility.
- The Storefront API's GraphQL types and field lists — introspection answers those.

## Contrasts

- **Nitrogen vs legacy theme** — see [[headless-nitrogen-overview]] for coexistence rules and [[headless-legacy-vs-nitrogen]] for the surface gap map.
- **Storefront API tokens vs deployment tokens** — different tabs, different rules. See [[headless-storefront-api]] vs [[headless-deployment-methods]].
- **Public vs private Storefront API token** — see [[headless-storefront-api]].
- **Command line vs GitHub** — locked at creation, can't switch. See [[headless-deployment-methods]].
- **A pull request vs a deploy** — only production is served, and a pull request is built, never deployed. See [[headless-nova-platform]].

## Where it applies

- **Admin surfaces** — [[nitrogen]], [[nitrogen-storefronts]], [[nitrogen-create-storefront]], [[nitrogen-storefront-overview]], [[nitrogen-deployments]].
- **Outside the admin** — the `cloudcart` CLI, the merchant's GitHub repository, the storefront's `{slug}.cloudcart.dev` address or a routed domain, the merchant's local environment.
- **Cross-feature** — [[customer]] (sign-in), [[domain]] and [[settings-domains]] (a domain joins the store before it is routed), [[seo-handling]], [[plan-gates]], [[multi-language]] (each language is its own store).

## Related

- [[nitrogen]] — Nitrogen admin hub.
- [[nitrogen-storefronts]] — storefront list + creation.
- [[nitrogen-create-storefront]] — creation wizard.
- [[nitrogen-storefront-overview]] — one storefront's page and tabs.
- [[nitrogen-deployments]] — deployment history.
- [[settings-domains]] — where a domain joins the store.
- [[customer]] — the customer behind a sign-in.
- [[domain]] — the domain entity.
- [[seo-handling]] — SEO mechanics.
- [[multi-language]] — languages across stores.
- [[metafields-nitrogen]] — reading metafields and metaobjects on a Nitrogen storefront.
- [[plan-gates]] — plan-feature gating.
- [[json-api-v2]] — the OTHER GraphQL endpoint and how it differs.

## Open Questions

- ⏸️ Pricing for Nitrogen / Nova — whether deployments / bandwidth / Worker CPU time are billed separately from the base CloudCart plan. This is a billing-policy decision (not in code) and merchants on Nitrogen should check current pricing at https://cloudcart.com/pricing or with their account manager.

Aspect-specific Open Questions are documented on each sub-page.
