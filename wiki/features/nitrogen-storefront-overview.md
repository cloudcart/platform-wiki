---
type: feature
nav_path: "Nitrogen (Headless)"
route_name: nitrogen.storefront.overview
route_path: /admin/nitrogen/:storefrontId
aliases: []
tags: [nitrogen, staff-permission]
plan_gates: []
created: 2026-05-21
updated: 2026-10-21
source_count: 1
---
# Nitrogen

## Purpose

TODO — one paragraph: what this screen lets the merchant do.

## Where to find it

Nitrogen (Headless)

## What the merchant can do here

TODO — bulleted list of actions a merchant can take on this screen.

## Sub-screens

Distinct routes within this feature, captured from `vuejs-sitecp/` route files.

| Label | Route name | Route path |
|-------|------------|------------|
| Nitrogen | `nitrogen.storefront.overview` | `/admin/nitrogen/:storefrontId` |
| Api | `nitrogen.storefront.api` | `/admin/nitrogen/:storefrontId/api` |
| General | `nitrogen.storefront.general` | `/admin/nitrogen/:storefrontId/general` |
| Domains | `nitrogen.storefront.domains` | `/admin/nitrogen/:storefrontId/domains` |
| Nova | `nitrogen.storefront.nova` | `/admin/nitrogen/:storefrontId/nova` |
| Environment | `nitrogen.storefront.environment` | `/admin/nitrogen/:storefrontId/environment` |

## Settings & fields

TODO — table of visible fields, what each one does, defaults, validation.

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| TODO | TODO | TODO | TODO |

## Business rules

### The Nitrogen Storefronts permission is required

The storefront page and all its sub-tabs (General, API, Nova, Environment, Domains) call API routes under `/admin/api/core/nitrogen/storefronts/{id}/*` that require the **Nitrogen Storefronts** permission. The store owner always has it; a moderator has it only when it is granted in their staff permissions. Without it, the calls get HTTP 403 — reading the storefront, generating a new private token, changing environment variables. See [[nitrogen]].

### Storefront API endpoint — GraphQL at `/api/sf`

The **API** tab shows the storefront's two Storefront API tokens: the public token in full with a Copy button, and the private token masked, with **Generate new token**, which replaces it at once and shows the new token once. The public token cannot be replaced here. The deployed app calls back into these endpoints:

- **POST `<store-host>/api/sf`** — GraphQL endpoint for queries and mutations.
- **GET `<store-host>/api/sf`** — same endpoint, for introspection clients.
- **GET `<store-host>/api/sf/downloads/{id}?signature=...`** — signed-URL streaming endpoint for digital files attached to customer orders (HMAC-verified, skips the storefront-token middleware).
- **GET `<store-host>/api/sf/playground`** (debug only) — built-in GraphQL playground; disabled in production.

Authentication: a request names the store with the public token in `X-Storefront-Access-Token` (optional on the store's own domain); the storefront's server may also send the private token, in its own header `X-Storefront-Private-Token`. The customer operations (orders, profile, wishlist, addresses) also need the customer's access token, which the Storefront API's `customerLoginCodeVerify` issues after `customerLoginCodeSend`. The storefront's scopes are not checked — see [[headless-storefront-api]].

See [[headless-storefront]] for the full Storefront API model + token rotation rules and [[json-api-v2]] for the cross-API comparison between `/api/v2`, `/api/gql`, and `/api/sf`.

TODO — non-obvious behavior, dependencies, plan-tier gates.

## Related

- [[nitrogen]] — Nitrogen hub.
- [[nitrogen-storefronts]] — storefront list and creation.
- [[nitrogen-deployments]] — deployment history.
- [[headless-storefront]] — full Nitrogen / Storefront API model and `/api/sf` endpoint reference.
- [[json-api-v2]] — cross-API comparison (REST `/api/v2` vs admin `/api/gql` vs storefront `/api/sf`).
- [[settings-domains]] — custom domain attachment.
- TODO — add more wikilinks to related feature, entity, and concept pages.

## Open questions

- ⏸️ Nitrogen Storefront overview page is a stub — full Purpose / Settings / Business rules pending first-pass ingest.
