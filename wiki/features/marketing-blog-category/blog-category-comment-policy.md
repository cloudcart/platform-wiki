---
type: feature
nav_path: "Marketing → Blog → Category → Comment policy"
route_name: blog-categories
route_path: /admin/marketing-new/blog/category
aliases: ["Blog category comment policy", "Blog comment policy", "Automatic comments approval", "Comments need approval", "Turn off comments", "Политика за коментари на блог категория"]
tags: [marketing, blog, content, categories, comments]
plan_gates: ["blog_categories"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-blog-category]]. See the hub for the other aspects (list & modal, lifecycle, SEO, API/plan/permissions).

# Blog Categories — Comment policy

## Purpose

Each blog category carries its own **comment policy** — one of `no` (off), `moderator` (pre-moderation), or `automatic` (auto-publish). This single setting decides whether visitors can comment on the articles inside the category, and whether their comments appear immediately or wait for approval. The policy is **per-category, not per-article**: every article inside the category inherits it. This aspect documents the control in the modal and the effect at comment-submission time.

## Where to find it

Sidebar → **Marketing** → **Blog** → **Category** → open a category's create/edit modal → **Comments settings** card. The modal itself is documented on [[blog-category-list]].

## What the merchant can do here

- Toggle **Automatic comments approval** ON to auto-publish all comments in the category.
- With auto-approval OFF, pick between **Turn off comments** (no comments at all) and **Comments need approval** (pre-moderation).
- Filter the category list by the resulting policy (Automatic / Modified / Not modified — see [[blog-category-list]]).

## Settings & fields

### The switch + radio share one value

The **Comments settings** card has two controls that **share the same v-model** (`category.comments`):

- **Automatic comments approval** switch (reverse-positioned label) — uses `true-value="automatic"` + `false-value="no"`. When ON, `category.comments = 'automatic'`. When it flips OFF, `category.comments = 'no'` (default), but the merchant can then re-pick the radio.
- An **HR divider** separates the switch from the radio group.
- **Comments radio** (`name="comments"`, non-stacked horizontal layout) — disabled when `category.comments === 'automatic'` or while saving. Two mutually exclusive options:
  - **Turn off comments** → `comments='no'` (storefront refuses submissions outright).
  - **Comments need approval** → `comments='moderator'` (pre-moderation queue).

Because the switch and radio share `category.comments`, toggling the switch ON auto-disables the radio group; toggling it OFF lands on `no` (the radio's first option). So **there is no "I want pre-moderation" default** — the merchant must explicitly pick the moderator radio after switching off auto-approval. The switch tooltip reads: *"If checked, all comments on articles within this category will be automatically posted."*

### Comment field values + validation

| Field | Validation | Notes |
|---|---|---|
| **Comments** (`comments`) | Required. One of `no`, `moderator`, `automatic`. | *"Comments is required"* / *"Invalid comments type. Types: no,moderator,automatic"*. Drives every article inside this category. |

The save button validates the resulting `comments` value against the enum `{no, moderator, automatic}`.

### Storefront effect per value

| Value | Storefront UI | Comment lifecycle |
|-------|----------------|-------------------|
| `no` | The comment form is hidden; "Turn off comments" displayed. | Articles accept no new comments. Existing comments still display. |
| `moderator` | Form visible; comments need approval. | New comments enter [[marketing-blog-comment]] as `pending` and are invisible on the storefront until a moderator approves them. |
| `automatic` | Form visible; comments auto-publish immediately. | New comments enter as `approved` and appear on submission. Useful for low-spam or trusted-audience contexts. |

## Business rules

### Comment policy is **per-category**, not per-article

The decision "comments on / off / moderated" is set on the category, and every article inside inherits it. When a visitor posts a comment, the platform reads the parent category's policy and stamps the new comment:

- `automatic` → comment created with `status=approved`, immediately visible.
- `moderator` → comment created with `status=pending`, hidden until approved in [[marketing-blog-comment]].
- `no` → submission rejected outright with *"The comments for this post are disabled"*.

To change comment policy for a single article only, the merchant has to **move the article into a differently-configured category** — there is no per-article override.

### Comments field uses a separate error path

When the merchant submits an invalid `comments` value (anything outside `no` / `moderator` / `automatic`), the validation error is keyed to `comments_error` rather than `comments` — the modal's radio group binds to `comments`, so an unknown value surfaces via a separate field name. In practice merchants only see the three legit options via the switch + radio, so this rarely surfaces.

### Auto-created categories default to `automatic`

When [[apps-blog-csv-import]] auto-creates a category on import, the new category defaults to `comments=automatic` unless overridden. See [[blog-category-lifecycle]] for the auto-create-on-import flow.

### Third-party commenting overrides this setting

Installing [[apps-disqus-comments]] or [[apps-facebook-comments]] swaps the native comment form on the storefront, which overrides this category's `comments` setting for visitors.

## Related

- [[marketing-blog-category]] — hub.
- [[marketing-blog-comment]] — moderation queue; reads the policy stamped onto each comment.
- [[blog-category-list]] — the modal that hosts the switch + radio.
- [[blog-category-lifecycle]] — auto-create-on-import defaults the policy to `automatic`.
- [[apps-disqus-comments]] — third-party commenting that overrides this setting.
- [[apps-facebook-comments]] — Facebook Comments Plugin alternative.

## Open questions

No outstanding questions.
