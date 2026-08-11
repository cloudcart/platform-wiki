---
type: entity
nav_path: "Entity → Blog Comment → Data model"
aliases: ["Blog Comment data model", "Blog Comment fields", "Blog Comment attributes", "Comment cascade delete", "Comment author_id", "Comment admin_id", "Comment email not verified", "Guest stays guest"]
tags: [entity, blog, comments, data-model, fields]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[blog-comment]]. See the hub for the other aspects (lifecycle, moderation policy, validation, threading & visibility, spam protection).

# Blog Comment — Data model

## Identity

The Blog Comment record is small — 10 merchant-visible fields covering content, authorship, moderation state, and audit. The data model encodes three operational rules that recur across the other aspects of this entity:

1. **Author identity is locked at submission time** — guest comments stay guest forever (`author_id` is NULL and there is no admin-side relink action).
2. **Cascade delete on the parent article, parent comment, and author customer** — deleting any of those three wipes the comment row, which is the platform's primary cleanup mechanism (and a useful GDPR side-effect).
3. **The `admin_id` audit field survives admin churn** — `ON DELETE SET NULL` keeps the comment row when a staff account is deleted.

The data model carries no IP address, no browser fingerprint, no reply-count cache, no spam-score — every spam-related signal a merchant might want has to be read off the existing fields (typically `email` pattern matching) or supplied by a third-party platform — see [[blog-comment-spam-protection]].

## Aliases

- **Comment fields** / **Comment columns** / **Comment record** — informal phrasing for the same attribute set.
- **`author_id`** — the customer FK; appears in support tickets phrased as "the comment author".
- **`admin_id`** — the moderator FK; appears in support tickets as "who approved this".

## Key Attributes

| Field | What it stores | Notes |
|-------|----------------|-------|
| **item_id** | The parent [[blog-article|Blog Article]] this comment is attached to. | FK to the article. Cascading delete: deleting the article wipes all its comments — the merchant doesn't need to clean up the queue first. |
| **parent_id** | For threaded replies — points to the comment this one replies to. | Cascading delete: deleting a parent comment removes all replies under it. See [[blog-comment-threading-visibility]] for the storefront vs admin-queue difference. |
| **name** | Guest commenter's name. | Required when the commenter is NOT logged in. Empty for logged-in customers (their name comes from the [[customer|Customer]] record). Validation: *"Your name is required"* (storefront) / *"Name is required"* (admin). |
| **email** | Guest commenter's email. | Required when not logged in. Empty for logged-in customers. Email is **NOT verified** — no opt-in confirmation, no account required. Used for the gravatar avatar on the moderation queue and on the storefront. Validation: *"Your email address is required"* + a 191-char email format check. |
| **author_id** | FK to [[customer|Customer]]. | Set when the commenter is logged in. NULL for guest comments. Cascading delete: deleting the customer wipes their comments (GDPR-friendly). |
| **comment** | The comment text. | Required. Max **1,000 characters**. Plain text — no rich-text, no HTML. Rendered as escaped HTML on the storefront. Validation: *"You forgot to type a message"* (empty) / *"Comments can not be longer than 1000 characters"* (too long). |
| **status** | `approved` / `pending` / `spam`. | Initial value is decided by the parent category's `comments` setting — see [[blog-comment-moderation-policy]]. Merchant changes it manually via the queue or the Manage modal. |
| **date_added** | Timestamp the comment was submitted. | Set automatically when the comment is created. Displayed in the queue using the store's date+time format. |
| **date_status** | Timestamp of the last status change. | Updated when the merchant moves the comment between approved / pending / spam. |
| **admin_id** | FK to the staff member who last changed the status. | Records which admin performed the most recent status change. DB-level constraint is `ON DELETE SET NULL` — deleting the admin user clears `admin_id` on every comment they ever touched, but the comments themselves survive admin churn. |

The comment text is stored as plain text (no rich-text formatting, no HTML); the storefront renders it as escaped HTML.

### Cascade delete summary

| Parent | On delete | Effect on Blog Comment |
|--------|-----------|------------------------|
| [[blog-article]] (`item_id`) | cascade | Comment row is deleted. |
| Parent Blog Comment (`parent_id`) | cascade | Reply row is deleted. |
| [[customer]] (`author_id`) | cascade | Customer's comments are deleted (GDPR-friendly side effect). |
| [[staff-member]] (`admin_id`) | set NULL | Comment survives; audit field is cleared. |

### Fields the data model does NOT carry

- **Source IP** — not stored. The admin queue cannot identify repeat spammers by IP.
- **Browser fingerprint / User-Agent** — not stored.
- **Spam score** — not computed; no learned classifier exists.
- **Reply count** — computed live; not cached on the parent row.
- **Edit history** — comments are not editable from the admin queue (see [[blog-comment-threading-visibility]]), so there is no edit-log.
- **Verified-email flag** — emails are accepted at the format level only; see [[blog-comment-validation]].

### Author identity locks at submit time — the "guest stays guest" rule

The comment-create flow locks `author_id` at submission time: `NULL` for guest visitors, the customer's id for logged-in visitors. There is **no admin-side affordance to link a guest comment to an existing [[customer|Customer]] record after the fact**. If the merchant wants the comment associated with a Customer, the visitor must re-comment while logged in.

Practical consequence: when a customer comments while logged out and then later registers, the original comment retains `author_id = NULL` even if the registration email matches.

### Email field is captured but NOT validated / verified

The email is format-checked (must look like an email, ≤191 chars — see [[blog-comment-validation]]) but the platform does NOT send a confirmation link, verify the address (no MX / DNS check), or create a [[customer|Customer]] / [[subscriber|Subscriber]] record from it. The email is used only for the gravatar avatar and for display in the queue (so the merchant can identify repeat spammers by email pattern). Logged-in customers don't fill the email field — it's pulled from their [[customer|Customer]] record.

## Where it appears

- [[marketing-blog-comment]] — the moderation queue. Columns shown: name, email, comment text excerpt, article, status, `date_added`, `date_status`, admin who last changed status.
- [[marketing-blog-articles]] — exposes a derived "Comments (N)" count per article, linking to the queue pre-filtered by `item_id`.
- The storefront article page — pulls `name`, `comment`, `date_added`, and the gravatar derived from `email`. `author_id` (if set) is used to apply the "your own pending comment" visibility carve-out.
- [[apps-gdpr-requests]] — customer deletion request relies on the `author_id` cascade to remove the customer's comments.

## Related

- [[blog-comment]] — hub.
- [[blog-comment-lifecycle]] — what the `status` field moves through; how the row is created / hard-deleted.
- [[blog-comment-moderation-policy]] — what decides the initial `status` value.
- [[blog-comment-validation]] — the format / length checks on `name`, `email`, `comment`.
- [[blog-article]] — `item_id` FK target.
- [[blog-category]] — sets the policy that drives `status` at submit time.
- [[customer]] — `author_id` FK target.
- [[staff-member]] — `admin_id` FK target.
- [[apps-gdpr-requests]] — customer-deletion cascade.

## Open Questions

None.
