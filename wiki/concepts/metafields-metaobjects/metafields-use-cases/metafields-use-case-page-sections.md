---
type: concept
nav_path: "Concept → Metafields and metaobjects → Use cases → Homepage and landing-page sections"
aliases: ["Page sections metaobject", "Headless CMS metaobjects", "Homepage sections", "Landing page builder Nitrogen", "Section metaobject", "mixed_reference sections", "Секции на начална страница", "Лендинг страница в Nitrogen", "Съдържание без CMS"]
tags: [metafields, metaobjects, use-case, content, nitrogen, landing-pages]
plan_gates: []
created: 2026-10-20
updated: 2026-10-21
source_count: 5
---

# Use case: homepage and landing-page sections

> Part of [[metafields-use-cases]] in [[metafields-metaobjects]].

## Definition

On a classic theme, merchants arrange the homepage and landing pages with the page builder ([[design-modules-page-builder]]). A Nitrogen storefront is its own code, and the Storefront API does **not** serve page-builder pages, only plain CMS pages as HTML. Without another source, every new homepage block would need a developer.

**Metaobjects as a small content system** solve this:
- each kind of section (hero, product row, category tiles, text block) is a metaobject definition;
- each page is an entry that lists its sections **in order**, through a `mixed_reference` list.

The merchant composes and reorders pages in the admin. The storefront has one component per section type.

## Scope

### The data model

**Section definitions** (each with storefront access `PUBLIC_READ`):

| Type | Fields |
|---|---|
| `section_hero` | `heading` (single-line text, required), `subheading` (multi-line text), `image` (file, Image), `cta` (`link`) |
| `section_products` | `heading`, `products` (`list.product_reference`, `list.max` 12), `show_prices` (`boolean`) |
| `section_categories` | `heading`, `categories` (`list.collection_reference`) |
| `section_text` | `heading`, `body` (rich text) |
| `section_video` | `heading`, `video` (file, Video), `poster` (file, Image) |
| `section_testimonials` | `heading`, `items` (`list.metaobject_reference` → `testimonial`, see [[metafields-use-case-testimonials]]) |

**Page definition `landing_page`**:

| Field | Type | Notes |
|---|---|---|
| `title` | single-line text, required | Display name; the handle (`home`, `black-friday`) is the route. |
| `sections` | `list.mixed_reference` → all section definitions above | The page's sections, in order. Up to 1,024. |
| `seo_title`, `seo_description` | single-line / multi-line text | Set by the storefront in the page head. |

Active/draft status **on**: a new campaign page is built in draft and becomes visible when switched to active.

### On the Nitrogen storefront

- The home route reads `metaobject(handle: {type: "landing_page", handle: "home"})`, then `field(key: "sections") { references { nodes { ... on Metaobject { type fields { key value reference references } } } } }`.
- A switch on each section's `type` picks the component. Product and category references come back with their data.
- **Landing pages**: a route `/{handle}` reads the `landing_page` entry with that handle. A smart collection's page can be paired with an entry of the same handle for a hero above its grid ([[metafields-use-case-category-content]]).
- **Rich text** arrives as a tree of paragraphs, headings, lists and links ([[metafields-types]]). `<MetafieldRichText>` from `@cloudcart/nitrogen-react` renders it, with `headingStart` placing the section's headings under its own. Other values (a `boolean`, a list of links, a measurement) go through `parseMetafield` ([[metafields-nitrogen]]).

### Rules that keep it manageable

- A `mixed_reference` must name the definitions it accepts, so a page cannot pick up unrelated entries.
- A section entry can be **reused** on several pages: a "Free delivery over …" banner used on the homepage and three landing pages is edited once.
- Deleting a section entry removes it from every page that listed it.

## Contrasts

- **Page builder vs section entries**: the page builder is visual and works on classic themes, but its pages are not on the Storefront API. Section entries are form-based, and are what a Nitrogen storefront can read.
- **CMS pages** ([[page]]): fine for one HTML document such as terms or an about page. Not for structured, reorderable sections.
- **Metaobjects vs an external headless CMS**: no extra system, logins or sync. The trade-off is form-based editing without a visual preview of the page.

## Where it applies

- Every Nitrogen storefront: homepage, campaign pages, brand pages, seasonal landing pages.
- Up to 128 metaobject definitions per store and 40 fields per definition, ample for a section library ([[metafields-limits]]).
- Staff who build pages need the **Metaobjects** permission, not the definitions one ([[metafields-permissions]]).

## Related

- [[metafields-use-cases]]: all use cases.
- [[metafields-use-case-banners]]: scheduled banners and announcements.
- [[headless-storefront]]: Nitrogen storefronts.
- [[design-modules-page-builder]]: the classic-theme page builder.

## Open Questions

- None known.
