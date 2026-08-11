---
type: feature
nav_path: "Marketing → Dynamic Pages → Page-builder modules → Title"
route_name: admin.pages.builder
route_path: /admin/marketing/pages/builder/{page_id?}
aliases: ["Title module", "Heading block", "Section title block", "H1 block", "Модул заглавие"]
tags: [design, modules, page-builder, title, seo, marketing]
plan_gates: [storefront_builder]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Title block (`title`)

> Part of [[design-modules-page-builder]]. See the category page for the other page-builder modules.

## Purpose

The **Title** block renders a section heading on a Dynamic page — an HTML heading tag (`h1` through `h6`) with the merchant's text. Used for the hero title of a landing page, section headers in long-form content, and SEO-relevant headings the merchant wants to control independently of the page's `<title>` meta.

## Where to find it

Open a Dynamic page in [[marketing-landing-pages]] → click **+ Add block** → pick **Title** from the block picker.

## What the merchant can do here

- Pick the HTML heading tag — `h1`, `h2`, `h3`, `h4`, `h5`, or `h6`.
- Set the heading text.
- Toggle the master enable switch.

## What the merchant cannot do here

- The merchant cannot pick the heading colour, font-size, or alignment from this block — those are theme-controlled via CSS targeting the `_section-title` wrapping `<div>`.
- The merchant cannot use HTML inside the heading text (e.g., a `<span>` for inline styling) — the text renders as-is. For rich text, use the [[design-modules]] `extra.text` module on a Dynamic page instead.
- The merchant cannot use a custom tag (e.g., `<strong>`) — the tag picker is limited to `h1`-`h6`.

## Settings & fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `enabled` | toggle | `true` | Master on/off. |
| `title` | text input | `''` | Heading text. |
| `tag` | select | `h1` | HTML tag: `h1` / `h2` / `h3` / `h4` / `h5` / `h6`. |

### Save / Reset / Cancel

Page-builder side panel — see [[marketing-landing-pages]].

## Business rules

### Storefront output

The block renders as:

```
<div class="_section-title">
  <h1>Some title here</h1>
</div>
```

The wrapping `<div class="_section-title">` is the theme's CSS hook for spacing / colour / alignment.

### Pick `h1` carefully — only once per page

For SEO, a page should have exactly one `<h1>`. If the merchant uses the Title block multiple times on the same page, they should set the FIRST instance to `h1` and the rest to `h2` / `h3` / etc. Otherwise the page has duplicate `<h1>` tags which hurts SEO. The block doesn't enforce this — the merchant is responsible.

### Title text is plain — no HTML

The merchant pastes plain text into the input. HTML characters are rendered as text (e.g., `<span>` shows up literally rather than being parsed). For rich-text headings, use an `extra.text` block.

### Per-language title

With the `multylang` app, the title accepts per-language entries via the language switcher in the editor.

### Empty title hides the block

When the merchant leaves the title blank, the storefront template still wraps the empty heading — it renders `<h1></h1>` which is invalid SEO. The merchant should fill the text or remove the block entirely. (verify the storefront output for empty title)

## Related

- [[design-modules-page-builder]] — hub.
- [[design-module-pb-separator]] — sibling: horizontal separator (often used to underline titles).
- [[design-modules]] — theme-wide `extra.text` module (for rich-text headings).
- [[marketing-seo-meta]] — page-level `<title>` meta (separate from heading text).
- [[marketing-landing-pages]] — Dynamic pages — the surface this module appears in.

## Open questions

- 📡 **Empty-title behaviour.** Confirm whether the storefront skips the block when `title` is blank, or renders an empty heading. (verify)
- 📡 **Theme CSS hooks.** Each theme provides its own `_section-title` styling — confirm the standard class hierarchy for merchant CSS overrides. (verify per theme)
