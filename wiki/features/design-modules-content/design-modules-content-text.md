---
type: feature
nav_path: "Design → Modules → Content → Text"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Text module", "Text block module", "TinyMCE module", "Static text module", "homeText module", "footerText module", "cartText module", "checkoutText module", "headerText module", "Text carousel module", "Rotating text module", "Testimonials module", "Модул текст", "Модул текстов карусел", "Текстова кутийка", "Текстова кутийка - подсказка", "Текст на началната страница - фон"]
tags: [design, modules, content, text, tinymce, testimonials]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

# Content modules — Text blocks + Text carousel

> Part of [[design-modules-content]]. See the hub for the carousel hero, banners, video, page-builder modules, and storage mechanics.

## Purpose

The text modules are the **rich-text editorial slots** of the storefront — every theme exposes a handful of named slots (e.g., `homeText1`, `footerText`, `cartText`) where the merchant types marketing copy, disclaimers, welcome messages, or shipping policy via a TinyMCE editor.

The `textCarousel` module extends this into a rotating multi-slide variant — typically used for testimonials, customer quotes, or rotating taglines.

Both module types are backed by the same underlying maps (`extra.text` and `extra.textCarousel`) but each named INSTANCE is an independent stored row.

## Where to find it

Sidebar → **Design** → **Modules** → **Others** tab:

- **Text fields** group — the `extra.text` instances the theme assigns to it; the others sit in the tab outside any group (`productText` does on every built-in theme).
- **Slider** group — the `textCarousel` instance(s).

Click the card to open the edit panel.

## What the merchant can do here

- Edit the rich-text body of each text instance (TinyMCE, up to 300 000 chars).
- Set the optional title heading shown above the text.
- For `textCarousel`, configure 1-20 rotating slides with HTML body, captions, schedule.
- Save / Reset / Cancel — full pipeline in [[design-modules-content-storage]].

The merchant CANNOT add a NEW text instance — only instances declared by the active theme have cards. For brand-new copy slots, build a Dynamic page in [[marketing-landing-pages]].

## Settings & fields

### Text block (`extra.text`) — fields

| Field | Type | Description / Validation | Default |
|-------|------|--------------------------|---------|
| `enabled` | toggle | Master on/off | on |
| `title` | text (0-250 chars) | Optional heading shown above the text content | "Example title" |
| `text` | rich text (TinyMCE, 1-300000 chars) | The block's main content — supports headings, lists, images, links, basic HTML | "Example text" |

For the `buttonToTop` INSTANCE (also internally an `extra.text` module), the title and text fields are HIDDEN — only the enable toggle is shown. See the back-to-top module in [[design-modules-navigation]].

### Known text-module instances by slot

The instance name is the slot identifier. The active theme decides which ones exist:

- `homeText1` / `homeText2` / `homeText3` — three independent text blocks on the homepage (each with its own slot).
- `welcomeText` / `homeWelcome` — welcome / hero text on the homepage.
- `headerText` — text in the header (e.g., *"Free shipping over X"*).
- `headerLeft` / `headerRight` — text before / after the logo.
- `footerText` / `footerContent` / `footerContacts` — text in the footer.
- `cartText` / `checkoutText` / `checkoutPrice` / `checkoutSideText` — text on the cart / checkout pages.
- `checkoutSignInGuestText` / `checkoutSignInLoginText` / `checkoutSignInRegisterText` — text shown during checkout based on the customer's sign-in state.
- `productText` — one store-wide text shown on **every** product page, in the side column under the buy button, after the labels' and banners' texts and before the category properties and the wishlist / compare actions (verify per theme). It cannot differ per product: per-product text goes in the product's description tabs ([[products-editor]]). The theme names its card: *Product details page text* / *Текст в детайлната страница* (Knowledge, Motivation, Summer, Jobs, Technoarena) or *Product details text* / *Текст в детайлите на продукта* (Flair, Echappe, MDL).
- `textbox1`–`textbox4` (**Текстова кутийка 1–4**) and `textbox1_tooltip`–`textbox4_tooltip` (**Текстова кутийка N - подсказка**) — `knowledge`, `motivation`, `jobs`, `summer` and `technoarena` themes: a row of up to four boxes on the homepage (on `knowledge`, after the second homepage text section; position varies per theme, verify). A box shows when its main card is on; its **- подсказка** card holds a pop-up shown above the box when a mouse hovers it (none on touch screens). On these themes `text1`–`text3` (**Текст на началната страница 1–3**) are full-width homepage text sections whose background image is the matching **Текст на началната страница N - фон** card ([[design-module-background-image]]). None of these cards has a group: they show under **Покажи всички**.
- `homeTopBanner` / `homeTopTextAfterCategoryShowcase` — text at specific homepage anchors.
- `homeVideoText` — text overlaid on the homepage video section.

### Text carousel (`extra.textCarousel`) — top-level controls

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `enabled` | toggle | Master on/off | on |
| `amount` | dropdown 1-20 | Number of slides | 1 |
| `full_width` | dropdown — **yes** / **no** | Stretch to viewport edges | yes |
| `slides_per_view` | dropdown 1-8 | Number of slides visible at once | 1 |
| `caption` | dropdown — **yes** / **no** | Show per-slide caption | yes |
| `controls` | dropdown — **yes** / **no** | Show prev / next arrows | yes |
| `indicators` | dropdown — **yes** / **no** | Show pagination dots | yes |
| `autoplay` | dropdown — **yes** / **no** | Auto-advance | yes |
| `interval` | number (ms) | Time between advances | 5000 |
| `cycle` | dropdown — **yes** / **no** | Loop back to first after last | yes |
| `pause` | dropdown — **yes** / **no** | Pause on hover | yes |
| `space_between` | number (px) | Margin between slides | 0 |

### Text carousel — per-slide fields (1-20)

| Field | Description |
|-------|-------------|
| `caption` | Short caption / heading for the slide |
| `html` | Rich-text content (TinyMCE) — the main text body |
| `sorting` | Sort order (ascending) |
| `from` / `to` | Schedule the slide (auto-show / auto-hide based on date range) |

## Business rules

### Each instance is independent

`homeText1`, `homeText2`, `homeText3` are separate stored instances; saving one does not change the others.

### Slot semantics from the name

The instance name signals where the text renders: `cartText` in the cart, `footerText` in the footer.

### Inline images are supported

TinyMCE allows inline images uploaded to the file manager and referenced inline. Useful for "as seen on" badges, small inline icons, or trust logos beside copy.

### When to use a Static page instead

Long-form content (about-us, terms) belongs on a Static page in [[marketing-landing-pages]], linked from a text module.

### Text carousel — pairs with testimonials

The most common `textCarousel` use is a "what our customers say" row on the homepage. Set `slides_per_view=3` and `space_between=30` for a clean three-up testimonials layout. Per-slide `from` / `to` lets the merchant rotate post-event customer feedback in / out automatically.

### Plan-gating

Neither text modules nor `textCarousel` are plan-gated — universally available.

### Per-language content via multylang

When the `multylang` app is installed, the body field stores per-language sub-keys (one body per language). Without the app, only one body is stored regardless of the storefront's language switcher. See [[design-modules-content-storage]] for the translation-merge mechanics.

## Tips

- Use the per-slide schedule on `textCarousel` to time-limit post-event feedback (e.g., trade-show quotes from last month).
- The `title` field is optional — leave it blank if the slot doesn't have a heading.

## Related

- [[design-modules-content]] — hub.
- [[design-modules-content-carousel]] — image hero slider (shares scheduling shape with `textCarousel`).
- [[design-modules-content-banners]] — banner grids (shares the link-picker model).
- [[design-modules-content-storage]] — TinyMCE save pipeline + multylang translation merge.
- [[design-modules-navigation]] — `buttonToTop` (an `extra.text` module with hidden fields) and `htmlLine` (promo strip).
- [[marketing-landing-pages]] — Static / Dynamic pages for long-form copy.
- [[design-themes]] — theme decides which text instances exist.

## Open questions

None.
