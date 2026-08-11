---
type: entity
aliases: ["Smart Collection storefront page", "Selection landing page", "/selection URL", "Smart Collection SEO", "Collection image and thumbnail", "Страница на колекция"]
tags: [catalog, products, collections, smart-grouping, storefront, seo, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[smart-collection]]. See the hub for the other aspects (rule builder, evaluation, discount link, vs category, management).

# Smart Collection — storefront page, SEO & image

## Identity

Every [[smart-collection|Smart Collection]] has an **auto-generated storefront landing page** at `/selection/<url-handle>` that lists the products currently matching its rules. This aspect covers that page: the fixed URL pattern, the AJAX endpoints that load products, the Advanced SEO section the merchant fills in, and the collection image / thumbnail handling.

## Aliases

- "Landing page" / "collection page" — the storefront page at `/selection/<slug>`.
- "URL handle" / "slug" — the merchant-set part of the URL.
- "SEO section" / "Advanced section" — the part of the edit modal holding URL handle + SEO overrides.
- Bulgarian: "Страница на колекция".

## Key Attributes

### Storefront URL is fixed at `/selection/<slug>`

Smart Collection storefront URLs are always `/selection/<url-handle>`. The `/selection/` prefix is part of the platform's storefront routes and is **NOT merchant-configurable** — only the slug (the URL handle) is. So handle `summer-sale` → `/selection/summer-sale`. Time-series-statistic middleware on every `/selection/` route also records visits for time-series analytics.

### AJAX endpoints power the page

Endpoints under `/selection/` drive the landing page without full reloads:

- `ajax.selection` — lazy product loading (pagination / infinite scroll).
- `ajax.products.selection` — products-only render.
- `ajax.filters-ts.selection` — the filter sidebar.

The page reads the **cached product list**, not the rules — see [[smart-collection-entity-evaluation]] for why the storefront never re-evaluates conditions per request.

### Advanced SEO section

The Advanced section of the edit modal carries the storefront-facing metadata:

| Field | Effect on the storefront landing page |
|-------|---------------------------------------|
| **URL handle** | The slug after `/selection/`. |
| **SEO title** | `<title>` tag override. |
| **SEO description** | `<meta name="description">` override. |
| **Canonical URL** | Optional `rel="canonical"`, for when the same collection content appears under multiple URLs. |

The **Name** and **Description** (set on the main part of the modal) render as the page heading and the long-form text above the product grid.

### Image and thumbnail handling

The collection's single uploaded **Image** is shown on collection cards and storefront listings. The storefront **theme controls thumbnail dimensions** — the record stores `max_thumb_size` (the cap for thumbnail generation), but the recommended source-image dimensions are theme-controlled (different themes have different aspect ratios and resolutions). Guidance: the merchant should upload a high-resolution image (1200×800 or larger); the platform's the image delivery service generates theme-appropriate thumbnails on demand.

## Where it appears

- Storefront landing page at `/selection/<url-handle>` — the page this aspect describes.
- [[products-smart-collections]] — the Advanced section + image upload live on the edit modal here.
- Menu navigation entries can link to `/selection/<url-handle>`.

## Related

- [[smart-collection]] — hub.
- [[smart-collection-entity-evaluation]] — the cached list the page renders.
- [[smart-collection-entity-rule-builder]] — the rules that determine which products appear.
- [[products-smart-collections]] — the management screen with the Advanced + image controls.

## Open Questions

None.
