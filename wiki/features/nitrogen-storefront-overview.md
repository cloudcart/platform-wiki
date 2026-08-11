---
type: feature
nav_path: "Nitrogen (Headless)"
route_name: nitrogen.storefront.overview
route_path: /admin/nitrogen/:storefrontId
aliases: []
tags: [nitrogen, owner-only]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
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
| Customer Account | `nitrogen.storefront.customer-account` | `/admin/nitrogen/:storefrontId/customer-account` |
| Nova | `nitrogen.storefront.nova` | `/admin/nitrogen/:storefrontId/nova` |
| Environment | `nitrogen.storefront.environment` | `/admin/nitrogen/:storefrontId/environment` |

## Settings & fields

TODO — table of visible fields, what each one does, defaults, validation.

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| TODO | TODO | TODO | TODO |

## Business rules

### Owner-only — moderators are blocked

The storefront-overview page and all its sub-tabs (API, Customer Account, Nova, Environment) call API routes under `/admin/api/core/nitrogen/storefronts/{id}/*`, all wrapped in the `isOwner` middleware. **Only the store owner can read, update scopes, rotate tokens, or change environment variables.** Moderators get HTTP 403 and never see the Nitrogen sidebar entry. See [[nitrogen]] for the pillar-wide owner-only rule.

### Storefront API endpoint — GraphQL at `/api/sf`

The **API** tab shows the merchant's two Storefront API tokens (public + private) and the endpoint the deployed app calls back into:

- **POST `<store-host>/api/sf`** — GraphQL endpoint for queries and mutations.
- **GET `<store-host>/api/sf`** — same endpoint, for introspection clients.
- **GET `<store-host>/api/sf/downloads/{id}?signature=...`** — signed-URL streaming endpoint for digital files attached to customer orders (HMAC-verified, skips the storefront-token middleware).
- **GET `<store-host>/api/sf/playground`** (debug only) — built-in GraphQL playground; disabled in production.

Authentication: every request must carry `X-Storefront-Access-Token: <token>` (public or private, depending on whether the request is from a browser or from server-side code). Customer-scoped queries (orders, profile, wishlist, addresses) additionally need `Authorization: Bearer <customer-jwt>` issued via the `customerAccessTokenCreate` mutation against the Customer Account API.

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
