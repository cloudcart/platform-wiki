---
type: concept
nav_path: "Concept → Headless storefronts → Nova platform"
aliases: ["Nova", "Nova platform", "Cloudflare Workers backend", "Nova hostname", "Nova namespaces", "Preview namespace", "Production namespace", "KV asset cleanup", "Workers for Platforms"]
tags: [nitrogen, headless, nova, cloudflare, workers, provisioning, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[headless-storefront]]. See the hub for the other aspects (Nitrogen overview, deployment methods, Storefront API, customer accounts, environment variables, legacy-vs-Nitrogen surfaces).

# Headless — Nova platform

## Definition

**Nova** is CloudCart's managed deployment platform built on Cloudflare's **Workers-for-Platforms** infrastructure. Every Nitrogen storefront becomes a Cloudflare Worker; every deployment is a new Worker version; the `*.nova.cloudcart.dev` hostname is a Cloudflare-managed domain.

The merchant doesn't directly manage Cloudflare — Nova provisions and deprovisions Workers automatically when storefronts are created or deleted, and pushes new Worker versions on every deploy command (CLI or GitHub-triggered).

## Scope

Covered:

- The two namespaces (production + preview) and what each serves.
- Provisioning on create — two Cloudflare API calls.
- Deletion teardown — Worker delete + KV bulk-delete + custom-domain unmap.
- The Nova hostname (`<handle>.nova.cloudcart.dev`).
- Custom-domain attachment via [[settings-domains]].

Not covered:

- The deploy command itself (CLI vs GitHub) — see [[headless-deployment-methods]].
- Deploy-token semantics — see [[headless-deployment-methods]].
- The GraphQL surface the Worker talks back to — see [[headless-storefront-api]].
- Env-var injection into the Worker — see [[headless-environment-variables]].

## Contrasts

- **Production namespace vs preview namespace** — production serves the merchant's main customer-facing URL; preview serves per-branch / per-PR staging URLs. Different Cloudflare namespaces, different worker versions live in each.
- **Nova hostname vs custom domain** — Nova hostname (`<handle>.nova.cloudcart.dev`) is live immediately after the first successful deployment. Custom domain attached via [[settings-domains]] routes to the same Worker but with the merchant's branding. The Nova hostname is **always reachable** even after a custom domain is attached.

## Where it applies

### One Worker per storefront, one new version per deployment

Each Nitrogen storefront maps to one Cloudflare Worker. Every successful deploy uploads a new version of that Worker. Static assets are stored separately in a Cloudflare KV namespace, keyed by `<worker-name>/<path>`.

### Two namespaces — production + preview

- **Production namespace** — the main deployed URL the merchant points their customers at. Only deployments from the production branch (typically `main`) reach this namespace.
- **Preview namespace** — every non-production branch / pull-request push gets its own preview URL for staging / QA, separate from the production storefront. The Environment tab on [[nitrogen-storefront-overview]] describes preview URLs as *"generated for each deployment — all other branches"*.

Each namespace has its own env-var set; see [[headless-environment-variables]] for the production-vs-preview split.

### Provisioning on create — two Cloudflare API calls

When the merchant creates a new Nitrogen storefront, the platform makes two Cloudflare API calls (verify exact endpoint paths):

1. **PUT custom-domain registration** — maps `{handle}.nova.cloudcart.dev` → the Nova dispatch service (Workers-for-Platforms).
2. **PUT placeholder Worker script** — renders a branded HTML page: *"Your Nitrogen storefront has been created. Deploy your project to go live."* with `cloudcart nitrogen deploy` instructions. This means the Nova hostname **resolves immediately** after create, even before the first real deployment.

### Deletion — full teardown with KV bulk-delete

On delete, the platform:

1. **DELETE the Worker from BOTH production AND preview namespaces** — the Nova hostname stops resolving.
2. **DELETE the custom-domain mapping** for `{handle}.nova.cloudcart.dev`.
3. **Iterate ALL KV-namespace keys prefixed `<worker-name>/`** and bulk-delete them — this purges static-asset bytes the deployed app uploaded.

Cloudflare failures during DELETE **don't block the storefront-record deletion** (best-effort cleanup) so the admin row goes away even if Cloudflare is misbehaving. If Cloudflare leaves orphan assets the merchant doesn't pay for them (they're on CloudCart's account), but CloudCart staff may need to manually purge.

### Nova hostname — `<handle>.nova.cloudcart.dev`

Each storefront gets a unique Nova-managed hostname `<handle>.nova.cloudcart.dev` where `<handle>` is the slug-plus-16-hex-hash described in [[headless-nitrogen-overview]]. This URL is fine for testing and is the default `PUBLIC_STORE_DOMAIN` (see [[headless-environment-variables]]) but most merchants want a branded domain on production.

The Nova hostname stays unchanged even when the merchant attaches a custom domain — so existing deployments keep working regardless of domain changes.

### Custom-domain attachment via [[settings-domains]]

The merchant attaches their custom domain to the storefront via [[settings-domains]] (the same screen used for legacy-storefront domains). Nova then routes the custom domain to the deployed Worker.

When the merchant changes the primary domain in [[settings-domains]], the storefront's Storefront API and Customer Account API endpoints update to use the new host — but the Nova hostname stays unchanged so existing deployments keep working.

### What runs in the Worker

The merchant's app code (Next.js, Remix on Cloudflare adapter, plain Workers script, etc.) runs as the Worker's request handler. It:

- Fetches data from `/api/sf` GraphQL (see [[headless-storefront-api]]) using the public or private Storefront API token.
- Reads its env vars at runtime (production or preview set, depending on which namespace the Worker version lives in).
- Reads static assets from KV at the `<worker-name>/` prefix.
- Returns HTML / JSON / streams to the customer.

Cloudflare's Workers-for-Platforms model means multiple merchants' Workers run isolated in the same dispatch service — Nova is the dispatch namespace owner.

### Best-effort failure model on provisioning errors

If the first Cloudflare API call succeeds but the second fails (custom domain registered but no placeholder Worker), the storefront-record creation **rolls back** — the merchant doesn't get a half-created storefront. (verify the exact rollback behaviour against current code.)

## Related

- [[headless-storefront]] — hub.
- [[headless-nitrogen-overview]] — handle format, the 16-hex-hash, per-site cap.
- [[headless-deployment-methods]] — how new Worker versions get uploaded.
- [[headless-environment-variables]] — what runtime variables the Worker reads.
- [[headless-storefront-api]] — what the Worker talks to.
- [[nitrogen-storefront-overview]] — Nova Deployments tab.
- [[nitrogen-deployments]] — per-deployment detail (commit, branch, status, URL, screenshot).
- [[settings-domains]] — custom-domain attachment.

## Open Questions

- Exact Cloudflare API endpoints (custom-domain PUT, Worker PUT, KV bulk-delete) — verify against current code.
- The dispatch-namespace name CloudCart uses for Workers-for-Platforms (likely environment-dependent).
- Behaviour when Cloudflare's KV bulk-delete encounters > 1000 keys (paginated cursor).
