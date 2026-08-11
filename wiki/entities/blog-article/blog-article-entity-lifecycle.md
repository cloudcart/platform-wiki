---
type: entity
nav_path: "Entity → Blog Article → Lifecycle"
aliases: ["Blog Article lifecycle", "Blog Article states", "Article draft", "Article scheduled", "Article published", "Article deleted", "Scheduled publish", "Article publish_date", "Article auto-publish"]
tags: [entity, blog, marketing, content, lifecycle, status, scheduling]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[blog-article]]. See the hub for the other aspects (data model, business rules, storefront & modules, programmatic access).

# Blog Article — Lifecycle

## Identity

The lifecycle of a **[[blog-article|Blog Article]]** is the set of merchant-controlled visibility states an article moves through, from Draft to live on the storefront to deleted. There is **no `status` enum** on the article — visibility is driven by two fields working together: the `active` flag (`yes` / `no`) and `published_at` (the publish datetime). The article's effective state is computed from those two fields plus the current time.

Key point: there is **no platform-level "Archived" state** on Blog Articles. The wiki previously claimed a `draft / published / archived` enum — that is wrong. To retire an article without breaking links to it, the merchant flips `active = no`, which makes the storefront return 404 on the URL (the slug remains in the DB).

## Aliases

- **Article states** / **Article visibility** — informal phrasing for the same model.
- **Draft** — `active = no`; the unpublished state.
- **Scheduled** — `active = yes` with a future `published_at`.
- **Published** — `active = yes` with a past `published_at`; the live state.

## Key Attributes

A Blog Article moves through these merchant-controlled states:

1. **Draft** — `active = no`. Fully editable. Invisible on the storefront — the article URL returns 404. Listable in the admin Draft filter.
2. **Scheduled** — `active = yes` with `published_at` in the future. Treated as Draft until the scheduled time, then auto-flips Published.
3. **Published** — `active = yes`, `published_at` past. The standard live state — visible on the storefront blog index, category feed, tag feed, and direct URL. Indexed by search engines.
4. **Deleted** — Hard-deleted. Removed from listings, the article URL returns the storefront's 404, and any external links break. The slug is freed for re-use.

Save-time transitions worth noting:

- Saving an article re-renders any cached category / tag feeds it appears in.
- Slug changes auto-create an SEO redirect entry from the old slug to the new one (see [[blog-article-entity-business-rules]] for the full slug rule).
- The first publish (`active` flips from `no` to `yes`) sets `published_at` to now unless the merchant supplied a future time.

## Scheduled publish

When `published_at` is set in the future, the article behaves as Draft until that time. The storefront's blog index query excludes articles whose `published_at > now`. At the scheduled time, the article auto-appears in the feed — no merchant action required.

The auto-flip is **passive** — the article becomes visible because the date check finally passes, not because a job ran on a schedule. As a consequence, the platform does **not** emit a webhook or admin notification at the moment of auto-publish; the only "publish event" the platform records is the original save where the merchant set the future date.

The visibility check is timezone-aware: the storefront compares `publish_date` against the platform code — so an article scheduled for "14:00" goes live the moment the minute "14:00:00 → 14:00:59" begins (not just after 14:00 sharp).

Note: the modern admin editor does **not** expose the `publish_date` field — scheduled publishing is reachable only via the API and the legacy editor. See [[blog-article-entity-api]].

## Retire vs Delete

- **Retire (`active = no`)** — keeps the article record and the slug in the DB, but the storefront returns 404 on the URL. The merchant can re-publish later. This is the closest thing to an "archive".
- **Delete** — removes the article entirely and frees the slug for re-use. External links break permanently.

Merchants who fear losing old content should retire (flip `active = no`); only those certain they want the slug back should delete.

## Where it appears

- [[marketing-blog-articles]] — the list + editor where `active` and (via legacy/API) `published_at` are set.
- [[blog-article]] — entity hub.
- Storefront blog index / category feed / tag feed — all gated on the computed Published state.

## Related

- [[blog-article]] — hub.
- [[blog-article-entity-business-rules]] — slug-rename redirect + required-category-at-publish rules that interact with state changes.
- [[blog-article-entity-api]] — scheduled publishing is active only via the API / legacy editor.
- [[seo-redirect]] — slug-change redirects created on save.
- [[marketing-blog-articles]] — admin list + editor.

## Open Questions

None.
