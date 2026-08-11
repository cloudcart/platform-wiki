---
type: entity
nav_path: "Entity → Blog Comment → Lifecycle"
aliases: ["Blog Comment lifecycle", "Blog Comment status transitions", "Blog Comment phases", "Comment approved pending spam deleted", "Comment delete vs spam", "Comment status flow"]
tags: [entity, blog, comments, lifecycle, status, transitions]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[blog-comment]]. See the hub for the other aspects (data model, moderation policy, validation, threading & visibility, spam protection).

# Blog Comment — Lifecycle

## Identity

A Blog Comment's lifecycle is the path the row travels from storefront submission to one of its terminal admin-controlled states. The lifecycle has **seven phases** (submitted → initial status assigned → in queue → approved / pending / spam / deleted) and a small **manual transition matrix** between the three live statuses. There is no automatic transition between statuses — no spam-learning model, no time-based auto-approval, no external spam-service consult. Every status move is a merchant action recorded with `date_status` + `admin_id` on the row.

Delete is the only **destructive** terminal — it removes the row from the database. Spam is a **non-destructive** hide — the row stays for audit and accidental restoration. The distinction matters for retention, GDPR, and "I clicked the wrong button" recovery.

## Aliases

- **Comment phases** / **Comment status flow** — informal phrasing.
- **Approve a comment** / **Mark as spam** / **Delete a comment** — the three queue actions that drive the transitions.
- **Pending queue** — the implicit queue formed by all comments with `status='pending'`.

## Key Attributes

### The seven phases

1. **Submitted** — a visitor (guest or logged-in customer) posts the comment from the storefront's article page. Submission validation runs — see [[blog-comment-validation]].
2. **Initial status assigned** — the platform looks up the parent [[blog-category|Blog Category]]'s `comments` setting (`automatic` / `moderator` / `no`) to decide the starting value. Full rules on [[blog-comment-moderation-policy]]:
   - `automatic` → `status='approved'`, visible on storefront immediately.
   - `moderator` → `status='pending'`, invisible on storefront, appears in the queue with "Pending" badge.
   - `no` → submission is rejected outright with *"The comments for this post are disabled"*. Nothing is persisted.
3. **In queue** — moderator surface lists the comment on [[marketing-blog-comment]] with filters by article / blog / status / search. Bulk and per-row actions are available.
4. **Approved** — `status='approved'`. Renders on the storefront's article page. The merchant can flip it back to `pending` or `spam` later.
5. **Pending** — `status='pending'`. Invisible on the storefront EXCEPT to the comment's own author when they're logged in (the author-sees-own-pending carve-out — see [[blog-comment-threading-visibility]]).
6. **Spam** — `status='spam'`. Invisible on the storefront. The row stays in the queue for audit / accidental restoration.
7. **Deleted** — hard-deleted by the merchant. Removed from the queue and the database. Use for clearly malicious / illegal content the merchant doesn't want kept on file.

### Status transition matrix

All transitions are merchant-controlled via the queue's bulk actions or the Manage modal. There is **no automatic transition**.

| From | To | Typical reason |
|------|-----|----------------|
| pending | approved | The typical "approve a queued comment". |
| pending | spam | Reject a queued spam comment without keeping it visible. |
| approved | spam | A posted comment turned out to be spam after the fact. |
| spam | approved | False positive — bring it back. |
| spam | pending | Review again later. |
| any | (deleted) | Permanent removal — see Delete vs Spam below. |

When the merchant changes status:

- `status` is updated to the new value.
- `date_status` is set to the current timestamp.
- `admin_id` is set to the staff member who clicked the action.

See [[blog-comment-data-model]] for the field-level definitions.

### Delete vs Spam — both hide from storefront, only Delete frees the row

- **Mark as spam** keeps the comment row in the database with `status='spam'`. Invisible on the storefront. Useful for routine spam — the merchant retains the record for volume auditing or accidental restoration.
- **Delete** permanently removes the row from the database. Use for clearly malicious / illegal content (libel, doxxing, CSAM) the merchant doesn't want kept on file at all.

The Manage modal exposes both buttons. Bulk actions also expose both — bulk delete is irreversible and confirms before running.

### Cascade deletion paths

Beyond the merchant's explicit Delete action, comment rows are also removed when:

- The parent [[blog-article|Blog Article]] is deleted (cascade on `item_id`).
- The parent Blog Comment is deleted (cascade on `parent_id` — removes all replies under it).
- The author [[customer|Customer]] is deleted (cascade on `author_id` — useful GDPR side-effect, separate from the explicit [[apps-gdpr-requests]] flow).

The `admin_id` set-NULL rule means deleting a staff account does NOT remove the comments they moderated — only the audit trail of who-did-what is cleared. See [[blog-comment-data-model]] for the full cascade table.

### No edit, no admin-side reply

The merchant CANNOT edit a comment's text from the queue — only approve, mark spam, or delete. There is no "fix typo" inline action. The merchant also cannot post replies from the admin panel — replies come from visitors on the storefront. To respond to a comment as the merchant, the merchant must comment from the storefront as a logged-in customer / staff identity. See [[blog-comment-threading-visibility]] for the threading model.

### Cache + side effects on status change

Status changes write to the comment row's `status` + `date_status` + `admin_id`. The storefront's article page is rebuilt at the next request (no explicit cache flush is fired). When an article is rendered, its comment list is queried live — there's no per-comment cache.

## Where it appears

- [[marketing-blog-comment]] — the moderation queue surfaces every live status filter (Approved / Pending / Spam) plus a search-all view. Bulk action bar exposes "Approve" / "Mark as spam" / "Delete" / "Set status to pending".
- The Manage modal on [[marketing-blog-comment]] — per-row status flip + delete.
- The storefront article page — renders only `status='approved'` comments to anonymous visitors and the author-sees-own-pending carve-out to the comment's logged-in author.
- The admin sidebar / dashboard "Pending approval" badge — driven by the count of rows in the `pending` phase. See [[blog-comment-moderation-policy]].

## Related

- [[blog-comment]] — hub.
- [[blog-comment-moderation-policy]] — the per-category setting that decides the initial status.
- [[blog-comment-data-model]] — the underlying field definitions (`status`, `date_status`, `admin_id`, cascade rules).
- [[blog-comment-threading-visibility]] — how the `pending` phase interacts with the logged-in author's view.
- [[marketing-blog-comment]] — admin moderation queue.
- [[apps-gdpr-requests]] — customer-deletion cascade.

## Open Questions

None.
