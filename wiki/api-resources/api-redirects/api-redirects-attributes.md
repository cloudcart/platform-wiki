---
type: api-resource
resource_path: /api/v2/redirects
http_methods: [GET, POST, PATCH]
related_entity: seo-redirect
related_features: [marketing-seo-301-redirects, apps-domain-redirect]
aliases: ["Redirects API attributes", "redirect_type values", "redirect old_url new_url", "redirect item relationship", "full_new_url accessor", "redirects filtering sorting"]
tags: [api, json-api-v2, content, seo]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
# Redirects API — attributes, relationship & filtering

> Part of [[api-redirects]]. See the hub for the other aspects (side effects & plan gating, examples).

## Purpose

This aspect is the **schema reference** for the redirects resource: the full attribute table (which fields are writable on POST vs PATCH, which are read-only, which are hidden), the polymorphic `item` relationship that points entity-typed rules at their destination, and the complete filtering / sorting / include reference. For the write-time side effects those attributes trigger (e.g. `old_url` normalisation, `item` clearing), see [[api-redirects-side-effects]]; for worked request / response payloads, see [[api-redirects-examples]].

## Endpoint

- **URL base:** `<store-host>/api/v2/redirects`
- **Methods covered here:** GET (collection + single, read shape), POST (writable attributes), PATCH (writable attributes), plus the `item` relationship endpoint `/api/v2/redirects/{id}/relationships/item`.

Authentication, host resolution, common headers, status codes, and rate limits: see [[json-api-v2]].

## Attributes

| Attribute | Type | Writable on POST? | Writable on PATCH? | Required? | Notes / validation |
|---|---|---|---|---|---|
| `redirect_type` | enum | yes | yes | **yes** | One of `product`, `category`, `vendor`, `blog`, `article`, `page`, `section`, `manual`, `external`. Determines how the destination is stored. Aliased to the internal `location` column. |
| `old_url` | string | yes | yes | **yes** | Unique across `redirects` (URL-decoded on save). The path to match. Wildcards: literal `*` becomes SQL `%` for `LIKE` matching at lookup. The lookup also tries the URL with and without trailing slash. The path is pre-normalised before the uniqueness check — see the parsing side effect in [[api-redirects-side-effects]]. |
| `new_url` | string | yes | yes | **required when** `redirect_type ∈ {manual, external}` (validator rule `required_if`) | For `external`, the platform auto-prepends `http://` when the value isn't already prefixed. For `manual`, full URLs on the same store are stripped to relative paths on save (handles HTTP→HTTPS gracefully). |
| `item_type` | string | no (set via `item` relationship) | no | n/a | Listed in `readOnlyAttributes`. The polymorphic class name. |
| `item_id` | integer | no (set via `item` relationship) | no | n/a | Listed in `readOnlyAttributes`. |
| `full_new_url` | string | no | no | n/a | **Appended accessor** — computed destination URL at read time (resolves entity URLs to the entity's CURRENT `url_handle`, evaluates `section` route names, etc.). Listed in `readOnlyAttributes`. |
| `id` | integer | n/a | n/a | n/a | **Hidden** in the schema's `$hidden` array; JSON:API resource `id` still carries it. |
| `location` | string | n/a | n/a | n/a | **Hidden** — exposed via the friendlier `redirect_type` alias instead. |

The `redirect_type` value drives whether an `item` relationship or a `new_url` is meaningful: entity types (`product`, `category`, `vendor`, `blog`, `article`, `page`) point at an `item`; `manual` / `external` carry a free-form `new_url`; `section` resolves a storefront route name with neither.

## Relationships

| Name | Cardinality | Target types | Writable? | Notes |
|---|---|---|---|---|
| `item` | belongsTo (hasOne) | polymorphic — one of `products`, `categories`, `vendors`, `blogs`, `posts` | yes | **Required when** `redirect_type ∉ {manual, external, section}` (validator rule `required_unless`). Set this to point at the destination entity. Validated against the allowed-types list `products, categories, vendors, blogs, posts`. The destination URL resolves to the entity's CURRENT `url_handle` at read time, so renaming the target later transparently updates redirects pointing at it. |

`redirect_type` must match the relationship target: `product` → `products`, `category` → `categories`, `vendor` → `vendors`, `blog` → `blogs` (Blog Categories — see [[api-blogs]]), `article` → `posts` (Blog Articles — see [[api-posts]]). The relationship can also be read / replaced / cleared via the standard JSON:API relationship endpoint `/api/v2/redirects/{id}/relationships/item`.

## Filtering & sorting

**Allowed filtering parameters:**

- **None declared explicitly** — the resource's allowed-filtering list is empty.
- **However**, the framework auto-merges every column on the `redirects` table into the allowed-filters list. Practical examples: `filter[old_url]`, `filter[item_type]`, `filter[item_id]`, `filter[location]` (the internal name for `redirect_type`). Value-equality only.

**Allowed sort parameters:**

- `item_type`, `item_id`, `redirect_type` (prefix with `-` for descending).

**Allowed include paths:**

- `item` (auto-merged from the schema relationships). Include with `?include=item` to sideload the destination entity.

Worked filter / include queries (e.g. `filter[location]=product`, `include=item`) are in [[api-redirects-examples]].

## Side effects

Reading attributes has one notable behaviour: `full_new_url` is **computed at read time**, resolving entity-typed rules to their target's current `url_handle`, so a stored entity reference always reflects the live URL even after the target is renamed. The write-time side effects that attributes trigger on save — `old_url` normalisation, `item_id` / `item_type` clearing for `manual` / `external` / `section`, and the `has_301_redirects` / cache recomputes — are documented in [[api-redirects-side-effects]].

## Equivalent UI

- [[marketing-seo-301-redirects]] — the create/edit modal whose form fields map to these attributes (the type picker → `redirect_type`, the source field → `old_url`, the destination → `new_url` or the entity picker → `item`).
- [[seo-redirect|SEO 301 Redirect entity]] — full attribute reference at the entity level.

## Related

- [[api-redirects]] — hub.
- [[json-api-v2]] — API hub: auth, headers, include / filter / sort conventions.
- [[api-redirects-side-effects]] — write-time effects these attributes trigger.
- [[api-redirects-examples]] — worked queries using `filter[location]` and `include=item`.
- [[api-products]] — `products` relationship target (`redirect_type = product`).
- [[api-categories]] — `categories` relationship target (`redirect_type = category`).
- [[api-vendors]] — `vendors` relationship target (`redirect_type = vendor`).
- [[api-blogs]] — `blogs` relationship target (`redirect_type = blog`).
- [[api-posts]] — `posts` relationship target (`redirect_type = article`).
- [[seo-redirect|SEO 301 Redirect entity]] — entity attribute reference.

## Open questions

- Confirm whether POST with both `new_url` AND `item` (a `redirect_type` that allows only one of them) returns 422 or silently picks one. The `saving` callback nulls `item_id` for `manual` / `external` / `section`, but the validator may still accept the conflicting payload — see [[api-redirects-side-effects]] for the clearing behaviour.
