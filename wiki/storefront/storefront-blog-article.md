---
type: storefront-page
route_name: blog.article.view
route_path: /article/{slug}
themes_using: [all]
tags: [storefront, blog, article, comments]
created: 2026-06-08
updated: 2026-06-08
source_count: 3
---

# Blog article (storefront)

## Purpose

Full page for a single blog article. Renders the cover, body, metadata, tags, related-article sidebar, and (optionally) the comments thread and submission form. Reached from any article card on [[blog-list]] / [[blog-filter]], from the recent-articles sidebar module, from in-content links, or from search engines.

## URL & route

- **Route name:** `blog.article.view`
- **Path:** `/article/{slug}`
- **Middleware:** `uuid_generate`, `subscriber_uuid`.
- **Method:** `GET`.
- **Comment submission:** `POST /blog/article/create-comment/{article_id}` — route name `article.create.comment`, throttled by a submission throttle (5 posts / minute).

## How it loads

1. Route resolves to the request handler (verify).
2. The article module loads the platform code, plus author, tags, and parent blog.
3. If a parent blog exists, the platform code is called so the sidebar context matches.
4. `$module->setSeo('article')` populates per-article SEO; per-article schema.org `Article` markup is emitted via the theme templates.
5. If `$article->active != 'yes'` the template prints the error notification `sf.module.blog.article.err.article_no_longer_active` instead of the body.

## What the customer sees

- Breadcrumb: **Home › Blog › <Blog name> › <Article title>**.
- Cover image (`800x800`, lazy-loaded, orientation class `lazyload-<portrait|landscape>`).
- Publish date in the corner of the cover (or above the title if no image).
- `<h2>` article title.
- Rich-text body (`{$article->content nofilter}`).
- Comments section when the article allows comments (the platform code):
  - List of approved comments, AJAX-refreshed.
  - Submission form — see below.
- Falls back to the notification `sf.article.warn.comments_disabled` when comments are turned off.
- Right-hand sidebar identical to [[blog-list]] (categories, recent articles, recent comments, tag cloud).
- Breadcrumb microdata.

## Storefront behaviour

- **Comment submission:**
  - Form ID: `#comment-form`, classes `blog-articles-comment-form-js js-form-submit-ajax`.
  - Action: `route('article.create.comment', $article->id)`.
  - Fields: `name` (only when not logged in), `email` (only when not logged in), `comment` (required textarea).
  - Submits via AJAX (no full reload). On success a `cc.blog.article.comment.posted` event fires; the handler resets the form.
  - GDPR/captcha not embedded in the form template by default (verify whether reCAPTCHA is injected at the form-component level on stores that enable it).
- **Schema.org:** `Article` JSON-LD-equivalent microdata is emitted; recommended for SEO and rich snippets.
- **Share buttons:** Many themes inject share buttons (Facebook, Twitter, LinkedIn, Email) via a separate include — verify presence in the active theme.

## JavaScript behaviour

- `js-form-submit-ajax` — generic AJAX form submitter (storefront framework).
- Event `cc.blog.article.comment.posted` — fired after a successful post; the inline `<script>` in `comment_form.tpl` resets the form.
- Comment list is wrapped in `data-ajax-box="{$article->url}"` so a successful post can trigger a partial refresh of the comments block.
- `js-loading` on the submit button shows a spinner while posting.

## Customisations available to the merchant

- **Comments globally / per-article** — toggled via the article record and the blog record (see [[marketing-blog-comment]]).
- **Article cover / SEO title / SEO description / slug** — editable per article in [[marketing-blog-articles]].
- **Tags & category** — assigned per article; drive the related-articles sidebar.
- **Body content** — full WYSIWYG, rendered via `nofilter` so all admin-side HTML is preserved.

## Theme variations

- All themes share the same controller + module contract; differences are CSS (typography, image ratios) and whether a share-buttons strip is present.
- Some themes show an author bio block beneath the article (verify per theme).

## Known issues / by-design vs bug

- Comment submission rate-limit is a submission throttle — 5 posts per minute per session/IP; exceeding it returns the throttle error.
- Inactive articles (`active != yes`) still return `200` with an inline notification, not `404` (by design — avoids breaking external links during temporary unpublish).
- Anonymous comments require `name` + `email` filled in; logged-in customers skip these fields and inherit the account identity.
- Comments are NOT auto-published — moderation happens in admin under [[marketing-blog-comment]].

## Related

- [[blog-list]]
- [[blog-filter]]
- [[marketing-blog-articles]]
- [[marketing-blog-comment]]
- [[marketing-blog-category]]
- [[marketing-blog-tags]]
- [[storefront-architecture]]

## Open questions

- Confirm whether reCAPTCHA is bound to the comment form on stores with the **apps-google-recaptcha**-style app enabled.
- Verify the share-buttons block — present in all themes or theme-specific?
- Confirm controller class path (the request handler).
