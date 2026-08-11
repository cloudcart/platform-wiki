---
type: entity
nav_path: "Entity → Blog Comment → Threading & visibility"
aliases: ["Blog Comment threading", "Blog Comment parent_id", "Blog Comment replies", "Comment threaded view", "Comment storefront visibility", "Author sees own pending comment", "No admin reply", "No comment edit"]
tags: [entity, blog, comments, threading, visibility]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[blog-comment]]. See the hub for the other aspects (data model, lifecycle, moderation policy, validation, spam protection).

# Blog Comment — Threading & visibility

## Identity

Threading and storefront visibility govern **who sees which comments and how they're arranged**. The platform supports threaded replies at the data level (`parent_id` FK) but **does NOT expose a threaded view in the admin moderation queue** — the queue renders comments as a flat date-ordered list. The storefront renders the threading if the theme implements it; otherwise the storefront also goes flat.

Storefront visibility is gated on `status='approved'` with one exception: a logged-in author always sees their own `pending` comments (the author-sees-own-pending carve-out). The merchant cannot edit a comment's text from the queue and cannot post replies from the admin panel — both are deliberate constraints.

## Aliases

- **`parent_id`** — the comment FK that encodes a reply.
- **Threaded replies** / **Nested comments** — the conceptual model `parent_id` supports.
- **Author-sees-own-pending** — the carve-out that prevents the logged-in author's just-submitted moderated comment from "vanishing".
- **Flat admin queue** — the current admin UI for comments.

## Key Attributes

### Threading at the data layer — `parent_id` with cascade delete

The Blog Comment data model carries a `parent_id` FK to another Blog Comment. When set, the row is a **reply** to that parent. The relationship supports arbitrary depth at the schema level — a reply can have its own replies, and so on — but the storefront and admin surfaces typically render only one level (parent + direct replies).

Cascade delete is wired on `parent_id`: deleting a parent comment removes all replies under it in a single operation. The merchant doesn't need to traverse the tree manually. See [[blog-comment-data-model]] for the full cascade table.

### The admin queue does NOT expose a threaded view

The `parent_id` field supports replies — one comment can be a reply to another. The data model preserves the relationship and cascading delete works correctly (deleting a parent removes the replies). But the **admin queue does NOT currently expose a threaded view** — comments render as a **flat list ordered by date**. To see the conversation structure, the merchant must look at the storefront article page where the threading is rendered.

Practical consequence for moderation:

- A merchant moderating a contentious thread sees individual comments out of context — they may have to open the storefront in another tab to follow who replied to whom.
- A bulk Approve / Mark-as-spam action doesn't know about the tree — selecting a reply doesn't automatically pull in the parent (and vice versa).
- The Pending filter on [[marketing-blog-comment]] surfaces individual replies as separate entries; deciding on a reply may require the merchant to also locate and act on the parent.

### Storefront visibility rule

The storefront's comment module on `/blog/<slug>` shows only comments where `status='approved'`. Comments with `status='pending'` or `status='spam'` are invisible to anonymous visitors and to other logged-in customers.

The query is run live on each page render — there is no per-comment cache and no explicit cache flush on status change. A status change on [[marketing-blog-comment]] becomes visible on the storefront at the next request to the article page.

### The author-sees-own-pending exception

There is one subtlety to the visibility rule: when the visitor IS the comment's own author (logged in as the same [[customer|Customer]] whose `author_id` is on the row), their `pending` comments ARE shown to THEM. The intent is so a customer doesn't see their just-submitted moderated comment vanish — they see it sitting in "pending" with a note, which keeps the UX clear.

The carve-out applies only to the comment's own author, only when logged in, and only to `pending` status:

- A guest author who closed the browser cannot come back and see their own pending comment (they have no `author_id`).
- A different logged-in customer sees the pending comment as invisible (not their `author_id`).
- A `spam` comment is invisible even to its own author (no carve-out — the merchant decision is final).

### No edit affordance

The merchant CANNOT edit a comment's text from the queue — only approve, mark spam, or delete. There is no "fix typo" inline action.

Practical workarounds:

- **Delete + repost as merchant** — the merchant deletes the comment, then comments themselves from the storefront as a logged-in customer / staff identity. The replacement is signed by the merchant's customer record (not the original visitor).
- **Live with the typo / problematic text** — for cosmetic issues most merchants accept the visitor's wording.
- **Delete and let the visitor resubmit** — practical only if the merchant can reach the visitor outside the platform.

### No admin-side reply affordance

The merchant cannot post replies from the admin panel — replies come from visitors on the storefront. To respond to a comment as the merchant, the merchant must comment from the storefront as a logged-in customer / staff identity (typically a "store team" customer account).

The reply will then carry that account's `author_id`, will appear in the queue with that account's name + email, and (under `moderator` mode) must be self-approved by the moderating staff — no auto-approval for "merchant accounts".

### No source IP or browser fingerprint surfaced

The native moderation queue does NOT expose the commenter's source IP or browser fingerprint. Only commenter name, email, comment text, dates, status, and the admin who last changed status are stored. This limits the merchant's ability to identify repeat spammers beyond email pattern matching — and prevents IP-based banning from the queue UI. See [[blog-comment-spam-protection]] for the practical mitigations.

To ban a spam commenter's IP, the merchant must do it manually via [[settings-banned-ip|Banned IPs]] — there is no "ban this commenter" action in the queue.

## Where it appears

- [[marketing-blog-comment]] — flat date-ordered list with status filters; no threaded view; no edit; no reply.
- The storefront `/blog/<slug>` article page — renders approved comments with threading if the theme supports it; renders the author's own pending comment in a "pending" state.
- The Manage modal on [[marketing-blog-comment]] — approve / mark spam / delete; no edit.

## Related

- [[blog-comment]] — hub.
- [[blog-comment-data-model]] — `parent_id` field + cascade rules.
- [[blog-comment-lifecycle]] — phases that the `status` field travels through; relevant to which comments are visible.
- [[blog-comment-moderation-policy]] — `pending` is invisible to anonymous visitors; the author-sees-own-pending exception only applies to authors.
- [[blog-comment-spam-protection]] — what the queue does NOT expose (IP, fingerprint) and how to mitigate.
- [[customer]] — the `author_id` that drives the author-sees-own-pending carve-out.
- [[settings-banned-ip]] — manual IP banning surface (no queue shortcut).

## Open Questions

None.
