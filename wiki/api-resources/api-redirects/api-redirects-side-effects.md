---
type: api-resource
resource_path: /api/v2/redirects
http_methods: [POST, PATCH, DELETE]
related_entity: seo-redirect
related_features: [marketing-seo-301-redirects, apps-domain-redirect]
aliases: ["Redirects API side effects", "has_301_redirects setting", "redirects301 cache flush", "redirect 7-prefix lookup", "redirect marketing pass-through", "redirect cascade delete", "redirects 422 errors", "no redirect webhook"]
tags: [api, json-api-v2, content, seo]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
# Redirects API — side effects, plan gating & errors

> Part of [[api-redirects]]. See the hub for the other aspects (attributes & relationship, examples).

## Purpose

This aspect covers everything a write to the redirects resource **triggers beyond the row itself**: the `old_url` normalisation, the `item` clearing for non-entity types, the `has_301_redirects` site-setting flip that gates the whole storefront redirect middleware, the `redirects301` cache flush, the storefront-lookup 7-prefix optimisation, the marketing-tracking query-parameter pass-through, the cascade-on-entity-delete behaviour, the absence of a 302 option, and the absence of any `redirect.*` webhook. It also documents the plan-feature gating (there is none) and the common 422 error shapes. For the attribute table itself, see [[api-redirects-attributes]]; for worked payloads, see [[api-redirects-examples]].

## Endpoint

- **URL base:** `<store-host>/api/v2/redirects`
- **Methods covered here:** POST, PATCH, DELETE — the write paths that trigger the side effects below.

Base URL, auth, headers, status codes, and rate limits: see [[json-api-v2]].

## Attributes

The side effects below are keyed off two attributes from [[api-redirects-attributes]]: `redirect_type` (drives whether `item_id` / `item_type` are cleared) and `old_url` (normalised on every save). No new attributes are introduced here.

## Relationships

The `item` relationship interacts with the clearing side effect: when `redirect_type` is `manual`, `external`, or `section`, any `item` sent in the payload is discarded on save (`item_id` / `item_type` forced to `null`). Full relationship reference: see [[api-redirects-attributes]].

## Filtering & sorting

Not applicable to this aspect (write-time behaviour only). For the filter / sort / include reference, see [[api-redirects-attributes]].

## Side effects

- **`old_url` parsing on save** — both the adapter and the validator normalise `old_url` on every save (URL-decode, leading-slash, etc.). The stored value may differ from the value sent in the request — read the response to confirm.
- **`item_id` + `item_type` cleared for manual / external / section** — when `redirect_type` is `manual`, `external`, or `section`, the adapter forces `item_id = null` and `item_type = null` in the `saving` callback, even if a relationship was sent. The redirect type drives whether an entity reference is meaningful.
- **`has_301_redirects` site setting flipped on every save / delete** — the adapter recomputes `setting('has_301_redirects')` to reflect whether any rule exists. This setting is read by the storefront's redirect middleware as a short-circuit: when `false`, the middleware skips all DB lookups, avoiding redirect-machinery overhead on stores with no rules. Saving the first rule flips this to `true`; deleting the last rule flips it back to `false`.
- **`redirects301` cache flush** — every save / delete invalidates the `redirects301` cache tag (24-hour per-URI memoization). The next storefront request for any URL re-runs the DB lookup and re-caches. **External CDN / browser caches may serve stale 301s longer** — out of the platform's direct control.
- **Lookup performance — 7-prefix optimization** — the storefront redirect lookup short-circuits the query for these path-first-segment prefixes: `product`, `category`, `vendor`, `blog`, `article`, `page`, `selection`. When the requested path's first segment is one of these, the lookup narrows candidates to rules whose `old_url` starts with `/<prefix>/`. **For every other first segment, the full-table scan happens with the wildcard-substituted `LIKE` on every row's `old_url`.** Stores with thousands of rules + custom prefixes (`/old-shop/`, `/blog-2/`) may see slower 301 lookup latency. Stick to the 7 conventional prefixes for best performance.
- **Marketing-tracking pass-through** — when the rule fires at storefront request time, the middleware re-attaches a hardcoded whitelist of query parameters to the redirect target: `fbclid`, `gclid`, `gclsrc`, `msclkid`, `utm`, `utm_source`, `utm_medium`, `utm_campaign`, `dclid`, `zanpid`. Notable omissions: `utm_term` / `utm_content` are NOT passed through.
- **Cascade on entity delete** — when an entity-typed redirect's target (Product / Category / Vendor / Blog / Article / Page) is deleted, the rule is **auto-deleted** via the entity's delete callback. Manual / External / Section rules are NEVER auto-deleted. Integrations that auto-create entity-typed redirects should be aware that target deletion silently removes their rules.
- **No 302 / temporary option** — the platform does NOT expose a status-code attribute. Every rule is permanent (301). To pause a rule, the merchant deletes it; there is no "temporary forward" API path.
- **Webhooks** — there is **no `redirect.*` event** in the platform's webhook catalogue (the supported events on [[api-webhooks]] do NOT include redirects). Integrations cannot subscribe to redirect-change events.

## Plan-feature gating

- **No per-rule plan-feature counter** — redirect rules are not capped by a plan-feature limit on this resource. The merchant may create unlimited rules subject to the rate limit.
- **No SEO plan-feature gate** — the redirects endpoint is available on every plan. The admin-side surface at [[marketing-seo-301-redirects]] is gated by the `marketing.seo` permission for staff role visibility, but the JSON-API v2 endpoint inherits the standard API key auth contract.

## Error examples (common 422 cases)

| Condition | `source.pointer` | `detail` |
|---|---|---|
| Missing `redirect_type` on POST | `/data/attributes/redirect_type` | *"The redirect type field is required"* |
| `redirect_type` value not in the enum | `/data/attributes/redirect_type` | *"The selected redirect type is invalid"* |
| Missing `old_url` on POST | `/data/attributes/old_url` | *"The old url field is required"* |
| Duplicate `old_url` | `/data/attributes/old_url` | *"The old url has already been taken"* |
| `redirect_type = manual` without `new_url` | `/data/attributes/new_url` | *"The new url field is required when redirect type is manual"* |
| `redirect_type = product` without `item` relationship | `/data/relationships/item` | *"The item field is required unless redirect type is in manual, external"* |
| `item` references an entity not in the allowed types | `/data/relationships/item` | *"The item field must be a to-one relationship containing products, categories, vendors, blogs, posts resources"* |
| Plan-expired (402, not 422) | n/a | *"Payment Required"* — the merchant's plan is past-due. |

Worked 422 response bodies are in [[api-redirects-examples]].

## Equivalent UI

- [[marketing-seo-301-redirects]] — the admin create/edit modal runs the same `saving` callbacks, so the same `old_url` normalisation, `item` clearing, `has_301_redirects` flip, and `redirects301` cache flush apply to admin-panel writes.
- [[apps-domain-redirect]] — **distinct** whole-domain DNS-level forwarding (does NOT trigger these per-rule side effects).

## Related

- [[api-redirects]] — hub.
- [[json-api-v2]] — API hub: status-code conventions (402 vs 422), webhook side-effect principle.
- [[api-redirects-attributes]] — the `redirect_type` / `old_url` / `item` attributes these effects key off.
- [[api-redirects-examples]] — worked 422 response bodies + the DELETE flow that flips `has_301_redirects`.
- [[api-webhooks]] — webhook catalogue (confirms no `redirect.*` event exists).
- [[marketing-seo-301-redirects]] — admin UI that shares the same write callbacks.
- [[seo-handling]] — concept page on URL handles + the separate URL-handle-history auto-tracking (30-day TTL on slug rename).

## Open questions

- Verify behaviour on bulk-import of redirects whose entity targets don't yet exist (e.g., `redirect_type=product`, `item_id=<non-existent product ID>`). The relationship validator should reject these, but bulk-import integrations need to confirm the error message and HTTP status.
- Document whether there's an upper bound on the number of redirect rules per store before storefront lookup latency degrades meaningfully — the 7-prefix optimisation helps, but stores migrating from another platform with tens of thousands of rules may want a benchmark.
