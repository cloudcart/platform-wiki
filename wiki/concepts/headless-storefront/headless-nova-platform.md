---
type: concept
nav_path: "Concept → Headless storefronts → Nova platform"
aliases: ["Nova", "Nova platform", "Nova hosting", "Storefront address", "cloudcart.dev address", "Production address", "Route a domain to a storefront", "Page cache", "createPageCache", "Адрес на витрината", "Домейн към витрината"]
tags: [nitrogen, headless, nova, hosting, domains, caching, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-11-03
source_count: 5
---

> Part of [[headless-storefront]]. See the hub for the other aspects (Nitrogen overview, deployment methods, Storefront API, customer accounts, environment variables, legacy-vs-Nitrogen surfaces).

# Headless — Nova platform

## Definition

**Nova** is CloudCart's managed hosting for Nitrogen storefronts, built on Cloudflare Workers. Each storefront is one worker. Every deploy, from the CLI or from GitHub, replaces it. The merchant manages no Cloudflare account: Nova creates the worker with the storefront and removes it with the storefront.

## Scope

Covered:

- The one environment Nova serves.
- The storefront's address, and routing a store domain to it.
- What is cached: assets and whole pages.
- What deleting a storefront removes.

Not covered:

- The deploy itself (CLI or GitHub) — see [[headless-deployment-methods]].
- Which paths stay on the platform on a routed domain — see [[headless-legacy-vs-nitrogen]].
- The GraphQL the worker calls — see [[headless-storefront-api]].
- The variables bound to the worker — see [[headless-environment-variables]].

## Contrasts

- **Storefront address vs routed domain** — `{slug}.cloudcart.dev` belongs to the storefront and answers every path from its worker. A routed store domain shows the same worker, while the platform keeps a fixed list of paths.
- **A deploy vs a build** — a pull request is built to check it and never reaches the live storefront. Only a deploy changes what visitors see.

## Where it applies

### Only production is served

A storefront has one live version. Preview deployments do not exist: there is no preview address, and a branch or a pull request gets none. The variables page has no Preview section, and its **Environment** select offers **All environments** and **Production**.

`PREVIEW` is still a value of the Admin GraphQL enum `NitrogenEnvironment`, the deploy endpoint still accepts it, and the CLI still has `cloudcart nitrogen deploy --preview` and `env push --env preview`. Nothing serves what they send, so a preview upload shows nowhere.

### The storefront's address

A storefront's address is `{slug}.cloudcart.dev`, with the slug described in [[headless-nitrogen-overview]]. A storefront made earlier at `{slug}.nova.cloudcart.dev` still resolves there.

From creation until the first deploy, the address shows a placeholder page: *"Your Nitrogen storefront has been created. Deploy your project to go live."* After the first deploy the admin says *"The storefront is uploaded. Its address can take a few minutes to answer the first time."* A later deploy is live at once. See [[nitrogen-deployments]].

The address does not change when a domain is routed, and stays reachable afterwards.

### Routing a store domain

The merchant does this on the storefront's **Domains** tab, not on [[settings-domains]]. See [[nitrogen-storefront-overview]] for the screen. **Route to this storefront** is offered for a domain the merchant brought whose DNS is managed by CloudCart. **Back to the store theme** undoes it.

Refusals:

| Message | Meaning |
|---|---|
| "Storefront must be active before it can serve a domain" | The storefront is paused. |
| "Domain is not a Cloudflare zone in the CloudCart account — move DNS to CloudCart first" | The domain's DNS is elsewhere. |
| "Another storefront already serves this site — remove it first" | One storefront at a time serves a store's domains. |
| "No domain is routed to this storefront" | **Back to the store theme** with nothing routed. |

On a routed domain:

- `www.` redirects with a 301 to the bare domain.
- `PUBLIC_STORE_DOMAIN` becomes the routed domain and `PUBLIC_API_ORIGIN` appears (see [[headless-environment-variables]]). Going back removes `PUBLIC_API_ORIGIN`.
- The confirmation asks the merchant to *"Make sure the storefront covers your store URLs (products, categories, pages) before switching, and deploy it again after switching so it picks up the new domain."*
- It also warns: *"Links in the store's e-mails that open the platform's pages, such as unsubscribing or an order's page, reach the storefront on this domain and do not work there yet."*

### Caching

**Assets.** A deploy with its build's assets sets `/assets/*` to `Cache-Control: public, max-age=31536000, immutable`. These files are named by their content's hash, so a browser may keep each for a year. Assets are served before the worker runs; any other path reaches the worker.

**Whole pages.** A built worker that exports `NitrogenPageCache`, which Nitrogen's `createPageCache` (Nitrogen 2.1 and later) adds, gets Cloudflare's cache on that entrypoint alone. Its default export, the gateway that sends pages there, is never cached. Any other worker is uploaded as before, and its pages are never cached. The export is read from the script itself, so an older Nitrogen or CLI changes nothing. A new deploy starts with an empty cache.

### Deleting a storefront

Deleting removes the storefront from Nova with its address, deployments and tokens. A domain routed to it goes back to the store's theme first. The repository on GitHub is not touched. See [[nitrogen-storefront-overview]] for the confirmation.

### What runs in the worker

The merchant's app is the worker's request handler, with Cloudflare's `nodejs_compat` flag on. It:

- calls `/api/sf` with its Storefront API tokens (see [[headless-storefront-api]]);
- reads its variables from `env`, bound at deploy (see [[headless-environment-variables]]);
- returns HTML, JSON or streams to the visitor.

## Related

- [[headless-storefront]] — hub.
- [[headless-nitrogen-overview]] — the slug and the platform's caps.
- [[headless-deployment-methods]] — how a deploy reaches Nova.
- [[headless-environment-variables]] — what the worker reads.
- [[headless-legacy-vs-nitrogen]] — what the platform keeps on a routed domain.
- [[headless-storefront-api]] — what the worker talks to.
- [[nitrogen-storefront-overview]] — the Domains and Deployments tabs.
- [[nitrogen-deployments]] — the deployment history.
- [[settings-domains]] — where a domain is added to the store before it can be routed.

## Open Questions

_None._
