---
type: entity
nav_path: "Entity → Blog Comment → Validation"
aliases: ["Blog Comment validation", "Blog Comment submission validation", "Comment form rate limit", "postThrottle 5 1", "Comment validation order", "Comment 1000 character limit", "Email format check 191"]
tags: [entity, blog, comments, validation, rate-limit]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[blog-comment]]. See the hub for the other aspects (data model, lifecycle, moderation policy, threading & visibility, spam protection).

# Blog Comment — Validation

## Identity

Submission of a Blog Comment from the storefront goes through a fixed set of validation checks, run in a **deterministic order**, with the FIRST failure short-circuiting the request and surfacing as a field-level error on the storefront form. Beyond the field-level checks, the endpoint is rate-limited to **5 submissions per 1 minute per IP** — the only platform-enforced anti-spam guard at the validation layer. There is no CAPTCHA, no Akismet, no MX lookup, no disposable-domain filter (see [[blog-comment-spam-protection]] for the full list of missing protections).

The validation rules differ slightly between **guest** and **logged-in** commenters — guests must supply `name` + `email`, logged-in customers do not (those fields are pulled from the [[customer|Customer]] record and the form hides them).

## Aliases

- **Comment form validation** / **Submission validation** — the field checks.
- **a submission throttle** — the verbatim middleware name applied to the submit endpoint.
- **Format-only email validation** — the rule that the email is checked for shape + length only, NOT for deliverability.

## Key Attributes

### Submission validation order

The storefront comment-submit endpoint walks the validation checks in a **deterministic order** and returns the FIRST failure:

1. **Article exists.** If `item_id` doesn't resolve to a live [[blog-article|Blog Article]], the endpoint returns *"No longer exists"*.
2. **Parent [[blog-category|Blog Category]]'s `comments` setting is not `no`.** If the category disables comments, the endpoint returns *"The comments for this post are disabled"*. See [[blog-comment-moderation-policy]] for the full per-category gating.
3. **For guests: name is present.** If empty, *"Your name is required"* (storefront) / *"Name is required"* (admin).
4. **For guests: email is present + passes `FILTER_VALIDATE_EMAIL` + ≤191 chars.** If missing or malformed, *"Your email address is required"*.
5. **Comment text is non-empty.** *"You forgot to type a message"*.
6. **Comment text ≤ 1000 chars.** *"Comments can not be longer than 1000 characters"*.

Because the order is deterministic and the response includes only the first failure, a merchant testing the form will see "name required" before any email-format error appears. This matters when triaging a "the form is broken" support ticket — the visitor's quoted error message identifies how far up the validation chain they got.

### Failure-message reference

| Check | Failure message |
|-------|-----------------|
| Article exists | *"No longer exists"* |
| Comments enabled on parent category | *"The comments for this post are disabled"* |
| Name (guest only) | *"Your name is required"* (storefront) / *"Name is required"* (admin) |
| Email (guest only, format + length ≤191) | *"Your email address is required"* |
| Comment text not empty | *"You forgot to type a message"* |
| Comment text ≤1,000 chars | *"Comments can not be longer than 1000 characters"* |

### Email validation is format-only

The platform validates the commenter email for **format + length only**:

- Must match `FILTER_VALIDATE_EMAIL` shape (`local@domain.tld`).
- Length ≤ 191 chars (matches the DB column width).

There is **no disposable-domain blocklist, no DNS / MX-record check, and no integration with external spam-email databases** — any well-formed address (`name@example.com` shape) is accepted. Merchants who want stricter validation should use a third-party comment platform — see [[blog-comment-spam-protection]] for [[apps-disqus-comments|Disqus]] / [[apps-facebook-comments|Facebook Comments]] alternatives.

The email is also not used as a uniqueness key — the same address can post unlimited comments (subject to the rate-limit below). The merchant's only deduplication signal is "same name + email + similar text" pattern matching done by eye in the queue.

### Storefront comment-submit rate-limit

The `POST /blog/article/create-comment/{article_id}` endpoint is throttled at a submission throttle. HTTP 429 errors are mapped back to the `comment` field on the storefront form. This is the only platform-enforced rate-limit; there is no CAPTCHA, no Akismet, no learned spam filter.

Practical consequences:

- A single IP submitting 6 comments inside 60 seconds will see the 6th rejected.
- Shared NAT (e.g. an office, a school network) is rate-limited per-IP, not per-user — a busy classroom of commenters can hit the limit.
- Mobile commenters whose IP changes between submissions get a fresh rate-limit each time.

The rate-limit does NOT distinguish between successful and failed submissions — a botted form spamming validation errors still consumes the IP's budget.

### Storefront success messaging

The endpoint returns two distinct success messages based on the parent category's `comments` setting (see [[blog-comment-moderation-policy]]):

- `automatic` → *"Comment posted"*.
- `moderator` → *"Comment posted (pending moderation)"*.

The endpoint also fires the `cc.blog.article.comment.posted` event so storefront templates can hook UI updates (e.g. success toast, refresh the comment list, scroll to the new comment).

### Plain-text only — HTML stripping and escaped rendering

The `comment` field is stored as plain text. The storefront renders it as escaped HTML — any HTML the visitor types appears literally (`<b>` shows as `&lt;b&gt;`). This is the platform's XSS protection on the comment surface: there is no rich-text editor, no markdown processing, no link auto-detection.

A practical merchant consequence: visitors cannot include clickable links in comments. Link-shortener URLs are accepted in the text but render as inert strings.

### Length boundary: 1000 characters, NOT bytes

The 1000-char check uses character count (`mb_strlen`), not bytes — Cyrillic / multibyte content is not penalised. The 191-char check on the email field is also character-based.

## Where it appears

- The storefront `/blog/<slug>` article page — the comment-submit form runs the visible validation client-side as a hint and the authoritative server-side validation on submit.
- The `POST /blog/article/create-comment/{article_id}` endpoint — applies a submission throttle middleware and the deterministic validation chain.
- [[marketing-blog-comment]] — admin-side form (Manage modal status change, not new-comment creation) uses a different label set (*"Name is required"* admin variant).

## Related

- [[blog-comment]] — hub.
- [[blog-comment-moderation-policy]] — what happens AFTER validation passes (initial status assignment, success message variant).
- [[blog-comment-data-model]] — the field definitions the checks validate against.
- [[blog-comment-spam-protection]] — the list of protections the platform does NOT provide; why the validation surface is shallow.
- [[blog-comment-lifecycle]] — the seven phases starting from a successful submission.

## Open Questions

None.
