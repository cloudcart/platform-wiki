---
type: concept
nav_path: "Concept → JSON-API v2"
aliases: ["JSON-API v2", "JSON API v2", "REST API", "Public API", "/api/v2", "Programmatic access", "External API"]
tags: [api, json-api, rest, integrations, programmatic, concepts]
created: 2026-05-27
updated: 2026-06-10
source_count: 12
---

# JSON-API v2 (programmatic access to store data)

## Definition

**JSON-API v2** is CloudCart's public REST API that lets external software read and write a merchant's store data programmatically. It implements the [JSON:API specification](https://jsonapi.org/), exposing each business entity as a uniform resource with predictable URLs, attribute envelopes, relationships, filtering, sorting, sparse fieldsets, includes, and pagination. The API is designed for **server-to-server AND browser-side** integrations (CORS is open) and uses **per-store API keys** for authentication.

This page is the **hub** for the JSON-API v2 cluster. Each aspect of the contract lives on its own sub-page — drill into the aspect that matches the question rather than reading every page.

For per-resource attribute / validation / relationship detail, see the **API Resources** section of the wiki index — every resource has its own page under `wiki/api-resources/`.

## Sub-pages (in this cluster)

The concept is split into 9 aspect pages. Drill into the aspect that matches the question rather than reading every page.

- [[json-api-auth]] — required headers (`X-CloudCart-ApiKey` + `Host`), validation order, failure responses, API-key lifecycle via admin GraphQL.
- [[json-api-headers-envelope]] — full header inventory + JSON:API 1.0 envelope; `X-Show-Links` opt-in.
- [[json-api-pagination]] — `page[number]` + `page[size]`, 1–100 cap, `meta.page` block, export loop semantics.
- [[json-api-filtering-sorting]] — `filter[]` (no generic comparisons), per-resource `sort` allow-list, `fields[]`, `include=`, custom `append[]`.
- [[json-api-endpoints]] — the 47-resource catalogue + 1 helper; method matrix; 16 read-only resources; custom routes; app-gated and registered-but-not-callable resources.
- [[json-api-status-codes]] — 200 / 201 / 204 / 400 / 401 / 402 / 404 / 405 / 406 / 415 / 422 / 429 / 500 / 503; error envelope; framework quirks (app-gated 404 wrapped as 422; 403 unreachable).
- [[json-api-webhooks-integration]] — API writes fire the SAME webhooks as admin UI writes (model-layer dispatch); idempotency requirements.
- [[json-api-audit-log]] — per-resource matrix: orders (`namespace = "api2"`), products/variants (`initiator = "api"`), customers (`addApi`), everything else uncaptured.
- [[json-api-cors-soft-delete]] — open CORS with OPTIONS-preflight-401 quirk; soft-deletes return 404 (not 410 Gone); no public restore.
- [[json-api-atomic-operations]] — JSON:API Atomic Operations extension is **NOT** supported; alternatives: sequential calls, admin GraphQL `productsBulkCreate`, [[apps-csv-import]].

## Why it matters to the merchant

Six high-impact consequences (each links to its aspect):

- **One key, full access.** No per-key scopes — merchants limit blast radius via key-per-integration discipline. See [[json-api-auth]].
- **Tenant is from `Host`, not a header.** Wrong domain → 404; right domain + wrong/inactive key → 401. See [[json-api-auth]].
- **Orders cannot be created or deleted via API.** Orders go through storefront checkout or [[orders-add]]. The API can read, modify status, and trigger fulfillment side-effects. See [[json-api-endpoints]].
- **API writes fire the same webhooks as admin writes.** Subscribers can't distinguish origin from the payload alone. See [[json-api-webhooks-integration]] + [[json-api-audit-log]].
- **Audit-log capture is partial.** Only orders, products, variants, customers record the actor. Everything else records only timestamps. See [[json-api-audit-log]].
- **No bulk-write surface.** Bulk catalog imports go through admin GraphQL `productsBulkCreate` OR [[apps-csv-import]]. See [[json-api-atomic-operations]].

## Scope

What the cluster covers, across its 9 aspects: authentication contract; request/response headers and JSON:API envelope shape; pagination, filtering, sorting, sparse fieldsets, includes; the 47-resource endpoint catalogue + 1 helper; HTTP status codes and the JSON:API error envelope; webhook integration with model-layer dispatch; per-resource audit-log behaviour; open CORS with preflight quirk; soft-delete returning 404 (not 410); and explicit non-support of the Atomic Operations extension.

Out of scope (lives elsewhere):

- Concrete rate-limit values — see [[platform-rate-limits|Platform rate limits]] for the canonical per-plan numbers and pack-purchase mechanism.
- GraphQL endpoints (admin and storefront) — see the contrast table below and [[settings-pat-tokens]] for PAT-based auth.
- Per-resource field schemas, validation rules, and relationship details — those live on the per-resource wiki pages under `wiki/api-resources/`.

## Contrasts — the three platform endpoints

| | JSON-API v2 (this cluster) | Admin GraphQL (`/api/gql`) | Storefront GraphQL (`/api/sf`) |
|---|---|---|---|
| Audience | External integrations (ERP, Make, Zapier, custom scripts) | Admin SPA + automation (CloudCart CLI, scheduled jobs) | Headless storefronts (Nitrogen, Next.js / Nuxt) |
| Auth | `X-CloudCart-ApiKey` + tenant from `Host` | PAT OR admin session + `X-Site-Id` | Storefront access token + optional customer JWT |
| Spec | JSON:API 1.0 | GraphQL (Lighthouse) | GraphQL (Lighthouse) |
| Granularity | One resource per request | Multi-operation queries / mutations | Customer-facing queries |
| Audit trail | `namespace = "api2"` on orders; per-attribute change-log on products/variants; other resources untracked | Records PAT holder or admin user; full per-mutation audit | Customer-scoped |
| Bulk writes | Not supported | `productsBulkCreate` + bulk operations | Customer-cart mutations only |
| Rate limit | Per-store cap — [[platform-rate-limits]] | Separate admin throttle | Separate storefront throttle |
| Webhook side-effects | Same as admin UI (model-layer dispatch) | Same | Same (customer-context) |

The admin GraphQL endpoint is the **only** path to operations JSON-API v2 deliberately does not expose: `productsBulkCreate` and bulk-operation query / cancel (see [[json-api-atomic-operations]]); analytics reports via `analyticsMetadata` + `analyticsReport` (see [[analytics-pipeline]]); cart-rule mutations (see [[apps-cart-rules]]); and mutation-heavy admin surfaces (segment / campaign / blog / settings edits).

## Where it applies

JSON-API v2 spans every external-integration touch-point of the store: ERP product / inventory sync, marketing automation (campaign / subscriber sync), order export to fulfillment apps, customer-record sync to CRMs, and webhook-driven event integration. Authentication runs at the routing layer before any controller (see [[json-api-auth]]); webhooks fire from the model layer for every write (see [[json-api-webhooks-integration]]); and the CORS preflight quirk affects every browser-side integration that uses non-simple requests (see [[json-api-cors-soft-delete]]).

Common merchant-facing diagnostic questions (each links to the aspect with the answer):

| Merchant question | Aspect |
|---|---|
| *"Why am I getting 401 on every request?"* | [[json-api-auth]] |
| *"Why am I getting 404 on every request?"* | [[json-api-auth]] — `Host` mismatch |
| *"Why is my POST returning 415?"* | [[json-api-headers-envelope]] — `Content-Type` |
| *"Why is filtering on `price < 100` not working?"* | [[json-api-filtering-sorting]] — no generic comparison operators |
| *"Why can't I create an order via the API?"* | [[json-api-endpoints]] — orders POST is blocked |
| *"Why is the change I made via API not in the audit log?"* | [[json-api-audit-log]] |
| *"Can two integrations use different API keys with different permissions?"* | [[json-api-auth]] — no scopes |
| *"How do I do bulk product imports via API?"* | [[json-api-atomic-operations]] |
| *"Can my browser app call this API?"* | [[json-api-cors-soft-delete]] |

## Related

- [[settings-api-keys]] — admin UI to create / deactivate API keys.
- [[platform-rate-limits]] — per-plan rate-limit values + pack-purchase mechanism.
- [[settings-hooks]] — webhooks fired by API writes.
- [[settings-pat-tokens]] — PAT auth for admin GraphQL (API-key lifecycle).
- [[notification-delivery]] — webhook delivery, retries, failure handling.
- [[orders-history]] / [[products-change-log]] — per-resource audit surfaces.
- [[plan-vs-feature-pack]] — plan gating for app-bound resources and rate-limit packs.
- [[orders-add]] — admin manual-order flow (API order creation is blocked).
- [[apps-csv-import]] — admin-UI bulk import flow.
- **API Resources index** — `wiki/api-resources/` for per-resource pages.

## Open Questions

- **Bulk operations roadmap** — JSON:API Atomic Operations extension is not on the platform. See [[json-api-atomic-operations]] for the alternatives.
- **`linked-products` route** — registered but routes commented out. See [[json-api-endpoints]].
- **API key scopes** — every API key is unrestricted. See [[json-api-auth]].
- **Per-event actor metadata on webhooks** — payload does not carry actor identity. See [[json-api-webhooks-integration]] + [[json-api-audit-log]].
