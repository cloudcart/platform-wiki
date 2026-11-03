---
type: feature
nav_path: "Design → Modules → Blog → Last comments"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Recent comments module", "Last comments module", "recentComments", "recentArticleComments", "blog.recentComments", "Последни коментари", "Модул коментари"]
tags: [design, modules, blog, comments]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Storefront Modules — Recent comments (`recentComments`)

> Part of [[design-modules-blog]]. See the category page for the other blog modules.

## Purpose

The **Recent comments** module (`blog.recentComments`, instance name typically `recentComments`) renders a short list of the most recently APPROVED customer comments on blog articles. Each row shows the commenter's name, the article they commented on, and a Gravatar avatar based on the commenter's email. Customers click a row to open the related article.

This module exists as social proof — it tells visitors that the store's blog has an active conversation around it. Moderation is upstream in [[marketing-blog-comment]]; this module is purely a display layer.

## Where to find it

Sidebar → **Design** → **Modules** → **Blogs, articles and comments** tab → click the **Last comments** card.

The form opens in a side panel with just two fields: enable + count.

If the active theme doesn't ship a `recentComments` instance, the card does not appear — most themes ship it, but a few omit it because their layout has no sidebar slot for it.

## What the merchant can do here

- **Set the count** of comments to show (2-10).
- **Disable** the module — when off, the block is hidden regardless of comments present.
- **Save** to persist; storefront cache regenerates on the next request.
- **Reset** to revert to the theme's shipped default (5).
- **Cancel** to close without saving.

What the merchant CANNOT do here:

- Filter by article or by blog category — the module pulls from the GLOBAL approved-comments pool.
- Choose a sort — always newest first (by comment date_added).
- Override the avatar source — always Gravatar, looked up by the commenter's email.
- Hide unapproved comments via this form — moderation status is set per-comment in [[marketing-blog-comment]] and the module already excludes anything not approved.

## Settings & fields

| Setting key | Type | Default | Allowed values | Validation | Notes |
|---|---|---|---|---|---|
| `enabled` | bool (switch) | `true` | on / off | `bool` | Hides the block when off |
| `count` | int | `5` | 2-10 | `int:2,10` | Number of comments to show |

### Validation behaviour

- `count` outside 2-10 triggers a field-level validation error.
- Unknown fields are silently dropped.

## Theme dependencies

- Most themes ship a `recentComments` instance — typically rendered in the blog sidebar (alongside Recent Articles) or in the storefront footer. Themes using the older alias `recentArticleComments` resolve to the same module.
- A few themes omit the instance entirely — the saved settings persist but no card appears on the Modules screen.
- The display name (**"Last comments"** / **"Recent comments"** / **"Последни коментари"**) and description shown on the card come from the active theme JSON.

Placement on the storefront is theme-controlled — the data is fetched the same way regardless of where the theme drops it.

## Business rules

### The module self-hides when there are no approved comments

When the store has zero approved comments, the block renders NOTHING — not even an empty-state notification. A merchant testing the module for the first time may believe it's broken when really the store just has no approved comments yet.

### Approved comments only

Comments with moderation status anything OTHER than approved (pending, spam, rejected) are excluded from the pool. Moderation lives in [[marketing-blog-comment]]; the merchant must approve comments there before they surface here.

### Global pool, no filter

The module pulls comments across ALL blog articles globally — there is no per-article, per-category, or per-tag filter exposed in the admin or the URL. To curate which comments surface, the merchant relies on moderation gating.

### Article-page comment thread is INDEPENDENT

Customers can still leave comments on a specific article even when this module is OFF. This module only controls the SIDEBAR / FOOTER aggregator — the comment form + thread on `/article/{slug}` is part of [[design-module-blog-article]] and continues to work.

### Third-party comment apps override the native pool

When Disqus ([[apps-disqus-comments]]) or Facebook Comments ([[apps-facebook-comments]]) is installed, article pages stop accepting NATIVE comments — the comment form on each article is replaced at the THEME level. The Recent Comments module still queries the native comment pool, but new approved comments stop arriving (because the form is gone). After installing a third-party comment app, this module gradually goes stale and the merchant should disable it.

### Gravatar lookup

Avatars are pulled live from Gravatar via the commenter's email. If the commenter has no Gravatar profile, Gravatar returns its default placeholder. There is no merchant control over the avatar source.

### Save / Reset / Cancel

| Button | Action | Confirmation | Success message |
|---|---|---|---|
| **Save module** | Persists settings; regenerates storefront cache | None | *"Module successfully edited"* |
| **Reset module** | Reverts to theme defaults | *"Are you sure you want to reset this module?"* | *"Module successfully reset"* |
| **Cancel** | Closes panel | None | — |

### Cache invalidation

Save / Reset bump the per-site modules cache key. New approved comments surface immediately on the next storefront request — the comment list is queried live, not cached at the module level.

### Plan gating

None — available on every plan that has blog comments enabled.

## Tips for merchants

- If the module appears empty on the storefront even with comments approved — confirm the theme has a slot for it (open the storefront and inspect the layout). Some themes ship the instance without a rendering slot; the module appears in the admin but never renders on the storefront.
- Approve comments in [[marketing-blog-comment]] in batches to keep this module feeling alive. Long-stale "last comment from 8 months ago" hurts more than helps.
- The module has no de-dup — if one customer leaves 5 comments in a day, all 5 may show. Moderation is the only filter.
- For stores with low comment volume, set `count` to a small number (3-4) so the row doesn't show old activity prominently.
- After switching to Disqus or Facebook Comments, disable this module — it'll progressively go stale because the native comment pipe is gone.

## Related

- [[design-modules-blog]] — hub.
- [[design-module-blog-listing]] — primary blog landing page; sibling.
- [[design-module-blog-recent-articles]] — Latest articles row; often paired with this module in the blog sidebar.
- [[design-module-blog-article]] — article-page module; hosts the per-article comment form + thread.
- [[marketing-blog-comment]] — comment moderation source of truth.
- [[marketing-blog-articles]] — per-article comment-allowed flag.
- [[apps-disqus-comments]] — third-party Disqus integration.
- [[apps-facebook-comments]] — third-party Facebook Comments integration.

## Open questions

- 📡 **Per-language comment text.** With `multylang`, comments are stored as the customer typed them (one language). The module displays them as-is — verify whether any per-language transliteration is applied (verify).
