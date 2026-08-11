---
type: feature
nav_path: "Marketing → Landing Pages → FAQ editor"
route_name: admin.pages.edit
route_path: /admin/marketing/pages/edit/{page_id}
aliases: ["FAQ page", "FAQ editor", "Q&A editor", "Shifting rows", "Question/answer pairs", "FAQ страница", "Често задавани въпроси"]
tags: [marketing, content, pages, faq, editor, shifting-rows]
plan_gates: ["faq_page"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-landing-pages]]. See the hub for the other aspects (list view, page types, editor, system slots, builder rules, plan gates).

# Landing Pages — FAQ shifting-rows editor

## Purpose

A page of type `faq` (one of the four types from [[landing-pages-types]]) does **not** use TinyMCE for the page body. Instead it uses a custom **shifting-rows** module — each Q&A pair is a separate row of (Question input + Answer TinyMCE editor) that can be added, removed, and reordered. The merchant builds a "Frequently asked questions" page by stacking Q&A pairs; the storefront renders them as an accordion.

FAQ pages are plan-gated by the `faq_page` plan feature (see [[landing-pages-plan-gates]]) — lower plans can't pick the FAQ type from the type-picker modal at all.

## Where to find it

Sidebar → **Marketing** → **Pages** → **+ Add new page** → pick **FAQ page** (label: `help.faq_page`).

Direct routes:

| Action | Route name | Path |
|--------|------------|------|
| Add FAQ page | `admin.pages.add` | `/admin/marketing/pages/add/faq` |
| Edit FAQ page | `admin.pages.edit` | `/admin/marketing/pages/edit/{page_id}` (when the page's type is `faq`) |

## What the merchant can do here

In the FAQ-type editor body, the merchant manages a list of Q&A pairs via the shifting-rows module — each pair lives in its own `.shifting-row-js` block. Per row:

- **Question** input — `input[type=text]`, name `content[i][questions]`.
- **Answer** TinyMCE rich-text editor — textarea, name `content[i][answers]`.
- **Add row** button (`add-row-js`, `+` icon) — inserts a new empty Q&A pair below the current one. Clones the TinyMCE setup so the new row has its own editor instance.
- **Remove row** button (`remove-row-js`) — removes the row. Only enabled when there's more than one Q&A pair (the editor enforces **at least one** row).
- **Move up** (`up-row-js`) / **Move down** (`down-row-js`) — reorder the Q&A pairs. The module tears down and re-initialises the TinyMCE editor for the moved row to preserve its state across the DOM move.

The rest of the form (Page name, URL handler, Featured image, SEO title / description, Active toggle, Private toggle) is the same as the regular editor — see [[landing-pages-editor]].

## Settings & fields

### Per-row inputs

| Input | Field name | Type | Notes |
|-------|------------|------|-------|
| Question | `content[i][questions]` | Plain text input | Required if the row exists. |
| Answer | `content[i][answers]` | TinyMCE rich text | Required if the row exists. |

The `[i]` index is auto-recalculated after every add / remove / reorder (the JS module's `addRowNumber` walks the `.shifting-row-js` blocks and re-stamps the `name` attribute on the input/textarea with the new index). The merchant never sees the index directly.

### Storage shape

FAQ pages store their Q&A pairs in a separate database table (one row per question), **not** in the main page's `content` column. On save, the controller iterates the submitted content array and creates one row per item with `name = questions[i]` and `content = answers[i]`. The main page's `content` column is forced to an empty string for FAQ-type pages.

## Business rules

### At least one Q&A row is enforced

The Remove-row button is disabled when only one row remains. Saving with zero rows would fail the content validation (*"You have to provide any content"*).

### Full-replacement save model — no delta updates

On every save of an existing FAQ page, the controller **deletes** all existing Q&A rows for that page first, then **re-inserts** the submitted rows from scratch. There is no delta-based update. Practical implications:

- Reordering rows is implemented as delete-and-reinsert in the new order.
- Any per-row foreign keys (e.g., translation rows from `multylang`) tied to the original row IDs will be lost on save — IDs are not stable across edits. (verify — `multylang` interaction)
- If the save fails partway, the rows in the new order may end up partially written. (verify — wrapped in a transaction?)

### TinyMCE re-initialisation on Move

Because Move up / Move down moves the DOM node out and back in, the TinyMCE editor instance attached to that row is **torn down and re-initialised** automatically by the module. The merchant sees a brief flash but no data loss — the editor's content is read before the move and re-applied after.

### FAQ pages allow a Featured image and SEO fields

Unlike `landing`-type pages, FAQ pages get the full Open Graph + SEO stack — featured image, SEO title, SEO description, canonical override. See [[landing-pages-editor]] for the field-level details.

### The `content` field validation applies to the combined Q&A text

The "max content chars" cap (10 000 000 chars) applies to the **sum** of all Q&A pairs (`questions[i]` + `answers[i]` across all rows). Effectively unlimited for any reasonable FAQ. (verify)

## Related

- [[marketing-landing-pages]] — hub.
- [[landing-pages-types]] — the FAQ type card on the **Choose page type** modal.
- [[landing-pages-editor]] — common form fields (Page name, URL handler, Active, Private, etc.).
- [[landing-pages-plan-gates]] — the `faq_page` plan-feature access gate.

## Open questions

- 📡 **Translation rows on `multylang`.** With the `multylang` app installed, each Q&A row presumably has translations — does the delete-and-reinsert save model preserve translation rows, or does the merchant have to re-enter translations on every edit? (verify)
- 📡 **Save transaction scope.** Is the delete-and-reinsert wrapped in a DB transaction? If the save partially fails, what's the recovery state? (verify)
