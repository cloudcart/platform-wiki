---
type: entity
nav_path: "Entity → Category Property → JSON-API v2"
aliases: ["Category Property API", "Property JSON-API v2", "Property programmatic access", "Property API side effects", "Property type-surface gap"]
tags: [catalog, products, properties, api, json-api-v2, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[category-property]]. See the hub for the other aspects (attributes, types, business rules, storefront).

# Category Property — JSON-API v2

## Identity

How a [[category-property|Category Property]] is read, created, updated, or deleted programmatically through **JSON-API v2**, and what fires when it is. The API path is a peer of the admin Save — it triggers the **same side effects** (storefront search re-index, URL-handle cache invalidation) and enforces the **same validations** (type-locked-after-create, delete-blocked-while-in-use, Range-must-be-all-numeric, 191-character name, per-Property-unique URL handle). This page documents the two resources, the shared side effects, the type-surface gap, and the transactional merge endpoint.

## Aliases

- **Property JSON-API v2** — the programmatic surface.
- **Property programmatic access** — read / create / update / delete via API.
- **Property API side effects** — the search re-index + cache invalidation.
- **Property type-surface gap** — API exposes four types, admin only two.

## Key Attributes

**Two resources cover the Property model:**

- [[api-properties]] — the Property definition: `name`, `type`, `is_visible`, `active`, `sort`, `url_handle`, `dec_points`, image, and the M2M category attachment.
- [[api-property-options]] — the discrete option values under each Checkbox Property.

**Same side effects apply.** A POST / PATCH / DELETE through JSON-API v2 fires the same storefront search re-index and the `categories_properties.keys.v1` URL-handle cache invalidation as the admin Save. The re-index re-syncs every affected product to the storefront search engine; the cache invalidation refreshes the `url_handle → property_id` map used to parse storefront filter URLs.

**Same validations enforce.** The **type-locked-after-create**, **delete-blocked-while-in-use**, **Range-must-be-all-numeric**, **191-character-name**, and **per-Property-unique-url_handle** validations all enforce on the API path too. The delete-in-use block returns the same HTTP 422 messages documented on [[category-property-business-rules]].

**Type-surface gap worth noting.** The underlying table supports `checkbox`, `range`, `select`, and `radio` types, but the admin Vue wizard only exposes the first two. JSON-API v2 reads / writes all four — but new API-created properties should default to `checkbox` or `range` to match the admin edit surface; `select` and `radio` records lack a Vue management UI. See [[category-property-types]].

**Multi-property, multi-value merge IS transactional on both paths.** The merge endpoint accepts a survivor + values from different parent properties, re-points every product, dedupes the join table, carries integration metadata, and fires per-product search re-sync — all inside a single transaction (no partial merges). See [[category-property-business-rules]] for the full merge semantics.

**Detaching a category does NOT cascade-delete per-product values** on either path; orphan values remain in storage and reappear when the category is re-attached (see [[category-property-business-rules]]).

See [[json-api-v2]] for authentication, rate limit, and the side-effects principle shared across all resources.

## Where it appears

- [[api-properties]] — JSON-API v2 resource for the Property definition.
- [[api-property-options]] — JSON-API v2 resource for the option values.
- [[json-api-v2]] — the API hub: authentication, rate limit, side-effects principle.
- [[products-property]] — the admin equivalent; same side effects + validations.
- [[apps-csv-import]] — an alternate bulk-write path (CSV) that also creates Properties + values.

## Related

- [[category-property]] — hub.
- [[api-properties]] — Property definition resource.
- [[api-property-options]] — option-values resource.
- [[json-api-v2]] — API authentication, rate limit, side-effects principle.
- [[category-property-types]] — the four-vs-two type-surface gap.
- [[category-property-business-rules]] — the validations + merge semantics that enforce identically on the API path.
- [[category-property-attributes]] — the fields the API reads / writes + the URL-handle cache.

## Open Questions

None.
