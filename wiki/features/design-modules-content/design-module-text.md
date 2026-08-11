---
type: feature
nav_path: "Design → Modules → Content → Text"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets
aliases: ["Text module", "extra.text", "Static text block", "Rich text module", "homeText1", "homeText2", "homeText3", "footerText", "headerText", "headerLeft", "headerRight", "cartText", "checkoutText", "checkoutPrice", "checkoutSideText", "productText", "homeWelcome", "homeVideoText", "homeTopBanner", "buttonToTop", "Текстов модул", "Текстов блок"]
tags: [design, modules, content, text, tinymce, richtext]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Text module (`extra.text`)

> Part of [[design-modules-content]]. See the category page for the other content modules.

## Purpose

The **Text** module is a static rich-text block — a TinyMCE editor whose output renders into a theme-defined slot. It is the merchant's go-to tool for short marketing copy: welcome paragraphs, free-shipping promises, footer disclaimers, payment-method explanations on checkout, "About us" blurbs, hero subtitles, and inline product-detail messaging.

Like every content module, the SAME module TYPE backs many INSTANCES — `homeText1`, `homeText2`, `footerText`, `cartText`, etc. — each pinned to its own theme slot, each saved independently.

## Where to find it

Sidebar → **Design** → **Modules** → **Others** tab → **Text fields** group on the left sidebar.

Each text instance has its own card. Common instances on default themes:

| Instance | Theme slot | Display name |
|----------|------------|--------------|
| `homeText1` / `homeText2` / `homeText3` | Three independent homepage text blocks | **Homepage text 1 / 2 / 3** |
| `homeWelcome` / `welcomeText` | Welcome / hero text on the homepage | **Welcome text** |
| `homeTopBanner` | Text at the top of the homepage | **Text at the top of the homepage** |
| `homeTopTextAfterCategoryShowcase` | Text after the homepage category showcase | **Text after the category window** |
| `homeVideoText` | Text overlaid on the homepage video section | **Homepage text and video** |
| `homeText` | Catch-all homepage text | **Homepage text** |
| `headerText` | Header text (e.g., "Free shipping over X") | **Heather Text** |
| `headerLeft` / `headerRight` | Text before / after the logo | **Text before / after the logo** |
| `footerText` / `footerContent` / `footerContacts` | Footer copy blocks | **Footer text / Text in footer / Footer contacts** |
| `cartText` | Cart sidebar text | **Text Cart** |
| `checkoutText` | Order completion text | **Complete order - text** |
| `checkoutPrice` | Price / delivery text on checkout | **Text for price and delivery when sending an order** |
| `checkoutSideText` | Text in the cart sidebar during checkout | **Text in the sidebar of the cart** |
| `checkoutSignInGuestText` / `checkoutSignInLoginText` / `checkoutSignInRegisterText` | Cart sign-in text per state | **Shopping cart text when Guest / Login / Register** |
| `productText` | Text on the product-detail page | **Text in product details** |
| `buttonToTop` | "Up" / back-to-top button (enable toggle only, no body editor) | **Up button** |

The exact list is theme-specific.

## What the merchant can do here

- Toggle the text block on / off.
- Enter a title (optional heading shown above the body).
- Enter rich-text body content in the TinyMCE editor — headings, lists, links, inline images, basic inline HTML.
- Save / Reset / Cancel.

What the merchant CANNOT do here:

- Change which theme slot the text renders in — the instance name decides the slot, not the merchant.
- Use the text module for very long content (about-us pages, policy text). Use a Static page in [[marketing-landing-pages]] instead.
- Embed `<script>` tags — TinyMCE strips them (see Business rules for the raw-HTML alternatives).

## Settings & fields

| Field | Type | Restriction | Default | What it controls |
|-------|------|-------------|---------|------------------|
| `enabled` | toggle | `bool` | on | Master on / off. When off, the slot renders empty. |
| `title` | text | `char:0,250` | "Example title" | Optional heading shown above the body. Most themes render this as an `<h3>` or `<h4>`. |
| `text` | rich text (TinyMCE) | `char:1,300000` | "Example text" | The body content. Supports headings, lists, links, inline images, tables, basic HTML. |

### Allowed HTML tags

A default install allows: `<b>`, `<a>`, `<p>`, `<br>`, `<s>`, `<em>`, `<hr>`, `<strong>`, `<small>`, `<code>`, `<kbd>`, `<samp>`, `<var>`, `<del>`, `<ins>`, `<cite>`, `<q>`, `<span>`, `<div>`, `<blockquote>`, `<ul>`, `<ol>`, `<li>`, `<font>`, `<pre>`, `<h1>` through `<h6>`, `<table>` / `<tbody>` / `<tr>` / `<td>`, `<img>`. `<script>` and `<iframe>` are stripped on save. (verify — historically these were the allowed tags.)

### Save / Reset / Cancel

| Button | Action | Confirmation | Success message |
|--------|--------|--------------|------------------|
| **Save module** | Persists title + body | None | *"Module successfully edited"* |
| **Reset module** | Reverts to theme defaults ("Example title" / "Example text") | *"Are you sure you want to reset this module?"* | *"Module successfully reset"* |
| **Cancel** | Closes the panel without saving | None | — |

## Business rules

### Each INSTANCE is an independent slot

`homeText1`, `homeText2`, `homeText3` are three SEPARATE instances. Editing one does NOT change the others — the instance name decides which slot fills. The merchant cannot move text from one instance to another; they edit one OR the other.

### Hard 300 000-char body cap

The `text` field is restricted to 1–300 000 characters — enough for several pages of marketing copy, but not for long-form policy text. For long content, use Static pages in [[marketing-landing-pages]] and link to them from a text block.

### Title is independent of body

The `title` field is a separate text input (max 250 chars). Leave it blank and most themes render the body without any heading.

### Body supports inline images via file manager

The TinyMCE "image" button opens the file manager — the merchant picks or uploads an image and it is inserted at the proper storage URL. Useful for "as seen on TV" badges, payment-method icons, and small inline graphics.

### `<script>` and `<iframe>` are stripped

TinyMCE strips dangerous tags (script, iframe, embed, object) on save. For raw HTML / JS, use [[design-module-code]] (page builder) or the `script` slot on [[design-module-banner]] — those bypass sanitisation.

### `buttonToTop` instance hides the editor

`buttonToTop` is an `extra.text` instance, but its edit panel hides the title / text fields and shows only the enable toggle. See [[design-modules-navigation]] for that surface.

### Variable replacement on read

On render, the body runs through a "text variables replace" pass — placeholders like `{store_name}` or `{customer_email}` are substituted with runtime values. This is theme- and instance-dependent.

### Cache invalidation on save / reset

Both **Save** and **Reset** regenerate the per-site cache key. The new text shows up on the next storefront request.

### Multi-language bodies

Multi-language stores (with the `multylang` app) get a language switcher inside the editor — each language has its own stored body. Without `multylang`, only one body is stored.

### Theme decides the instance catalogue

Every theme uses text modules, but the INSTANCE list varies wildly — older themes ship a handful, newer marketing themes ship 15+. A theme can also override the body wrapper without breaking the merchant's saved content.

## Related

- [[design-modules-content]] — hub.
- [[design-modules]] — parent module catalogue.
- [[design-themes]] — theme picker; theme decides which text instances exist.
- [[design-module-banner]] — for image-driven marketing blocks with links; use the `script` slot for raw HTML / JS.
- [[design-module-code]] — page-builder raw HTML / JS block (no sanitisation).
- [[design-modules-navigation]] — for the `buttonToTop` (back-to-top) instance.
- [[marketing-landing-pages]] — long-form content lives in Static pages, not text modules.

## Open questions

- 📡 **Per-language text content.** With `multylang`, `footerText` / `headerText` / `cartText` / etc. accept per-language bodies via the language switcher. GraphQL-resolvable: query whether the `multylang` app is installed.
- 📡 **Exact TinyMCE allowed-tag list.** Sanitisation is enforced by the TinyMCE editor's client-side config, not on save (verify) — a hand-crafted POST could in theory bypass the tag whitelist.
