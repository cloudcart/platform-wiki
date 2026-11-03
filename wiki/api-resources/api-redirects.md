---
type: api-resource
resource_path: /api/v2/redirects
http_methods: [GET, POST, PATCH, DELETE]
related_entity: seo-redirect
related_features: [marketing-seo-301-redirects, apps-domain-redirect]
aliases: ["Redirects API", "301 Redirects API", "JSON-API v2 redirects", "API 301 пренасочвания", "/redirects"]
tags: [api, json-api-v2, content, seo]
plan_gates: []
created: 2026-05-26
updated: 2026-06-10
source_count: 4
---
# Redirects (JSON-API v2)

## Purpose

Programmatic CRUD on the merchant's **301 (permanent) URL redirect rules** — the per-URL forwarding table that powers SEO preservation during migrations, slug restructures, and product / page removals. The API is the **bulk-friendly parallel** to the admin-panel screen at [[marketing-seo-301-redirects]].

Integrators use this endpoint to **bulk-import redirect rules from a migration spreadsheet**, **auto-create rules** when an external CMS publishes new content with restructured URLs, **read the current redirect table** for audit / sitemap diff, and **delete obsolete rules**. Each rule pairs an `old_url` (the path to match — supports `*` wildcards) with a destination (free-form URL, external URL, or a picker-selected entity — Product / Category / Vendor / Page / Blog / Article / Section).

Every rule on this endpoint is **always 301** — the platform does not expose 302 (temporary) redirects through the API. A 301 Redirect here operates at the **URL / path layer** within the merchant's storefront host (DNS-level whole-domain forwarding is a separate concern handled by [[apps-domain-redirect]]).

## Sub-pages (in this cluster)

This resource is split into 3 aspect pages. Drill into the one that matches the question.

- [[api-redirects-attributes]] — the full attribute table (`redirect_type`, `old_url`, `new_url`, the read-only `item_type` / `item_id` / `full_new_url`, hidden `id` / `location`), the polymorphic `item` relationship, and the filtering / sorting / include reference.
- [[api-redirects-side-effects]] — the write-time side effects (`old_url` parsing, `item` clearing, the `has_301_redirects` setting flip, the `redirects301` cache flush, the 7-prefix lookup optimisation, marketing-tracking pass-through, cascade-on-entity-delete, no-302, no-webhook), plan-feature gating, and the common 422 error shapes.
- [[api-redirects-examples]] — worked curl requests + JSON responses for entity-typed and plain URL rules, and the end-to-end CRUD testing checklist.

## Endpoint

- **URL base:** `<store-host>/api/v2/redirects`
- **HTTP methods:** GET (collection + single), POST, PATCH, DELETE — **full CRUD**
- **Read-only?** No
- **Custom routes:** none. Standard JSON:API relationship endpoints are registered for `item` (`/api/v2/redirects/{id}/relationships/item`).
- **App requirements:** none

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v2/redirects` | List redirect rules. Supports filter / sort / include / page. |
| GET | `/api/v2/redirects/{id}` | Fetch one rule. |
| POST | `/api/v2/redirects` | Create a rule. Requires `redirect_type` + `old_url`, plus either `new_url` (for `manual` / `external`) or the `item` relationship. |
| PATCH | `/api/v2/redirects/{id}` | Update a rule. |
| DELETE | `/api/v2/redirects/{id}` | Delete a rule. Returns 204. |
| GET / PATCH / DELETE | `/api/v2/redirects/{id}/relationships/item` | Manage the polymorphic target entity. |

Authentication, host resolution, common headers, status codes, and rate limits: see [[json-api-v2]].

## Attributes

Each rule carries a `redirect_type` (one of `product`, `category`, `vendor`, `blog`, `article`, `page`, `section`, `manual`, `external`), a unique `old_url` (the path to match — `*` wildcards supported), and a `new_url` (required for `manual` / `external`). The read-only `item_type` / `item_id` mirror the polymorphic relationship; the appended `full_new_url` accessor returns the resolved destination at read time. `id` and `location` are hidden. Full table + validation: see [[api-redirects-attributes]].

## Relationships

The resource declares one relationship — `item`, a polymorphic `belongsTo` pointing at one of `products`, `categories`, `vendors`, `blogs`, `posts`. It is **required when** `redirect_type ∉ {manual, external, section}`. The destination URL resolves to the target's CURRENT `url_handle` at read time. Full detail: see [[api-redirects-attributes]].

## Filtering & sorting

No filters are declared explicitly, but the framework auto-merges every column on the `redirects` table into the allowed filters (`filter[old_url]`, `filter[location]`, `filter[item_type]`, `filter[item_id]` — equality only). Sortable: `item_type`, `item_id`, `redirect_type`. Include: `?include=item` to sideload the destination entity. Worked queries: see [[api-redirects-attributes]].

## Side effects

Writes are not silent. Saving normalises `old_url` (the stored value may differ from the request); the `has_301_redirects` site setting is recomputed on every save / delete (short-circuits the storefront redirect middleware when no rules exist); the `redirects301` cache is flushed; entity-typed rules are auto-deleted when their target entity is deleted; and there is **no `redirect.*` webhook**. Full catalogue + plan gating + 422 errors: see [[api-redirects-side-effects]].

## Equivalent UI

- [[marketing-seo-301-redirects]] — the master list + create/edit modal (Marketing → SEO → 301 Redirects).
- [[apps-domain-redirect]] — **distinct** whole-domain DNS-level forwarding (different app; not managed via this API).
- [[apps-blog-csv-import]] — CSV import that auto-creates redirects for renamed blog content.
- [[seo-redirect|SEO 301 Redirect entity]] — full attribute reference.

## Related

- [[json-api-v2]] — API hub: auth, headers, status codes, webhook side-effect principle.
- [[api-redirects-attributes]] — attribute table + polymorphic `item` + filtering reference.
- [[api-redirects-side-effects]] — write-time side effects + plan gating + 422 errors.
- [[api-redirects-examples]] — worked curl requests + responses + testing checklist.
- [[api-products]] — entity target for `redirect_type = product`.
- [[api-categories]] — entity target for `redirect_type = category`.
- [[api-vendors]] — entity target for `redirect_type = vendor`.
- [[api-blogs]] — entity target for `redirect_type = blog`.
- [[api-posts]] — entity target for `redirect_type = article`.
- [[marketing-seo-301-redirects]] — admin UI.
- [[seo-handling]] — concept page on URL handles + redirects + URL-handle-history (the 30-day TTL auto-tracking on slug rename, a separate mechanism from this endpoint).
- [[settings-api-keys]] — authentication setup.

## Open questions

None at the hub level — see each aspect's own Open questions.
