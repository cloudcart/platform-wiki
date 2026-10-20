---
type: concept
nav_path: "Concept → Metafields and metaobjects → Use cases → FAQs"
aliases: ["FAQ metaobject", "Product FAQ", "Frequently asked questions entries", "Help centre content", "Questions and answers", "Често задавани въпроси", "Въпроси и отговори", "ЧЗВ"]
tags: [metafields, metaobjects, use-case, content, faq, support]
plan_gates: []
created: 2026-10-20
updated: 2026-10-20
source_count: 4
---

# Use case: FAQs on products, categories and a help centre

> Part of [[metafields-use-cases]] in [[metafields-metaobjects]].

## Definition

The same questions come up across many products and pages:
- *How long does delivery take?*
- *Can I return a sale item?*
- *Is this safe for children?*
- *How do I clean it?*

Classic themes have an FAQ page type, a CMS page whose questions show as an accordion ([[page-faq]]). The Storefront API returns a page only as its HTML body, one page with no structure to reuse. A **`faq` metaobject** makes each question an entry. Products and categories reference the questions that apply to them, and a help centre lists them by topic. One edit to an answer updates it everywhere.

## Scope

### The data model

**Metaobject definition `faq`**:

| Field | Type | Notes |
|---|---|---|
| `question` | single-line text, required | Display name. |
| `answer` | rich text, required | Paragraphs, lists and links. |
| `topic` | single-line text, `choices`: *Delivery, Returns, Payment, Product care, Sizing, Warranty* | **Admin filter** on. |
| `position` | `number_integer` | Order within its topic. |
| `show_in_help_centre` | `boolean` | **Admin filter** on. |

Active/draft status **on**, so a new answer can wait in draft until reviewed.

**Metafields**:

| Owner | `namespace.key` | Type |
|---|---|---|
| Product | `custom.faqs` | `list.metaobject_reference` → `faq` |
| Category | `custom.faqs` | `list.metaobject_reference` → `faq` |

An ordered page of questions can also be its own entry: a **`faq_page`** metaobject with `title` and `questions` (`list.metaobject_reference` → `faq`). The list keeps the merchant's order exactly.

### On the Nitrogen storefront

- **Product page**: the product's `custom.faqs`, and beneath them the category's, as an accordion.
- **Help centre**: one section per topic, each `metaobjects(type: "faq", query: "fields.topic:Delivery fields.show_in_help_centre:true")`. The Storefront API sorts entries only by id or last update, so the storefront orders each topic by `position` itself. Alternatively it reads a `faq_page` entry, whose list is already in order.
- **FAQ structured data**: the storefront can emit FAQ markup from the same entries, since question and answer are separate fields.
- Only **active** entries reach the storefront. Drafts are invisible to shoppers.

### Upkeep

- The entry's **Used in** list shows every product, category and other entry using a question, before it is changed or deleted ([[metaobjects-definitions]]).
- Deleting a question removes it from every list that referenced it.

## Contrasts

- **CMS FAQ page vs `faq` entries**: the FAQ page is ready on classic themes and needs no setup. Entries need setup, but give per-product questions, topics, drafts and structured data on Nitrogen.
- **FAQs vs product reviews** ([[apps-product-review]]): reviews come from shoppers. FAQ answers come from the store.
- **FAQs vs product content tabs**: a product's own tabs (`Product.tabs`) hold free HTML per product, suitable for one-off notes, not for answers shared across products.

## Where it applies

- Every store with recurring pre-sale questions: delivery and returns, sizing, care, compatibility, warranty.
- A product's or category's list holds up to 1,024 entries; the definition up to 1,000,000 ([[metafields-limits]]).

## Related

- [[metafields-use-cases]]: all use cases.
- [[page-faq]]: the classic-theme FAQ page.
- [[metafields-use-case-category-content]]: the category's other landing blocks.
- [[metaobjects-definitions]]: active/draft status, Used in.

## Open Questions

- None known.
