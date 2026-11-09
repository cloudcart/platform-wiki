---
type: feature
nav_path: "Design → Static pages → Dynamic page → Page Builder → Rows and row settings"
route_name: admin.pages.builder
route_path: /admin/marketing/pages/builder/{page_id?}
aliases: ["Row settings", "Page Builder rows", "Page Builder row settings", "Full width row", "Row padding", "Row margin", "Show in desktop mobile", "Move block to another row", "Добави нов ред", "Добави нов модул", "От край до край", "Покажи в", "Отстояние отстрани", "Външно отстояние"]
tags: [marketing, pages, builder, rows, layout, mobile]
plan_gates: ["storefront_builder"]
created: 2026-11-09
updated: 2026-11-09
source_count: 1
---

# Landing Pages — Page Builder rows and row settings

> Part of [[marketing-landing-pages]]. Publishing, drafts and history are on [[landing-pages-builder-rules]]; the blocks are on [[design-modules-page-builder]].

## Purpose

A page built with the page builder (a Dynamic page, or the Homepage, Thank-you or 404 page built with it) is a stack of **rows**. Each row has one or more columns, and each column holds blocks. This page covers the row and block controls on the canvas, the row settings panel (spacing, full width, background, device visibility) with its Bulgarian labels, and how those settings behave on phones.

## Where to find it

Open the page in the builder: `/admin/marketing/pages/builder/{page_id}`. A row's round buttons sit above it; the pencil (tooltip *Row settings*) opens the row settings panel. The button tooltips and the panel's title (*Row Settings*) are in English in every admin language; the field labels are translated.

## What the merchant can do here

- **+ Добави нов ред** (Add new row): pick a column layout for a new row, placed where the button is.
- Per row: *Row settings*, *Copy row*, *Reorder row* (drag handle to move the row up or down) and *Remove row*.
- **+ Добави нов модул** (Add new widget), at the bottom of each column, opens the block picker.
- Per block: *Edit widget*, *Copy widget*, *Reorder widget* and *Remove widget*. The reorder handle drags a block within its column, to another column, or into another row.
- The page-level **Header** and **Footer** switches show or hide the store's header and footer on this page.

## Settings & fields

The row settings panel:

| Label (BG) | EN | What it does |
|---|---|---|
| **Фон** | Background type | **Прозрачен** (none), **Изображение от мястото за съхранение** (with **Добави изображение за фон**), **Външно изображение за фон** (an image address), **Цвят за фона** (a colour), **Приложи фонa от предишния ред** (continue the previous row's background). |
| **Хоризонтална позиция** / **Вертикална позиция** | Background position | Where the background image sits. |
| **Стил на фона** | Background style | cover, contain or stretch. |
| **Ефект паралакс** | Parallax effect | scroll, or fixed for a parallax effect; iPhones and iPads always get scroll. |
| **Отстояние от горе (px)** / **Отстояние от долу (px)** | Padding Top / Bottom | Inner space above and below the row's content. |
| **Отстояние отстрани (px)** | Padding Lateral | Inner space on the left and the right (one value for both). Default 0. |
| **Външно отст. от горе (px)** / **от долу (px)** / **отстрани (px)** | Margin Top / Bottom / Lateral | Outer space above, below and on both sides. Side default 0. |
| **От край до край** | Full width | The row spans the whole screen instead of the store's centred content width. |
| **CSS клас** | CSS class name | An extra class on the row, for custom CSS ([[design-custom-assets]]). |
| **Подравняване на съдържанието** | Content alignment | Vertical alignment of the columns' content: top, middle or bottom. |
| **Покажи в** | Show in | Which screens show the row: empty (**Избери**) for all, desktop, or mobile. |
| **Размени колоните за настолна версия** | Reverse column order on desktop | On a two-column row, swaps the two columns on wide screens. |

The choices inside the position, style, parallax, alignment and **Покажи в** lists (center, cover, desktop, mobile…) are English in every admin language.

## Business rules

### Spacing is in pixels and the same on every device

Padding and margin are applied exactly as entered, in px, on phones as on desktop; a row has no separate mobile spacing. The values are not range-checked.

### Full width vs the store's content width (Grid settings)

A normal row sits inside the store's centred content area, so it follows **Grid settings** ([[design-module-grid-settings]]): the content width and the side offset. A row with **От край до край** uses neither and spans the screen, so with the default side padding of 0 its text touches the screen edges; give it **Отстояние отстрани** to keep text off them.

### Device visibility (**Покажи в**)

- Empty (**Избери**): every screen.
- **desktop**: shown from 768 px screen width up (tablets and computers), hidden on phones.
- **mobile**: shown only below 768 px.

768 px is the storefront grid's standard breakpoint (verify on themes that change it). A row set to desktop is the usual reason a block "is missing on mobile".

### Columns stack on narrower screens

Column widths apply from 992 px up; below that the columns of a row stack at full width, in order. **Размени колоните за настолна версия** swaps the two columns only from 992 px up; on phones they keep their order.

### Row settings are part of the draft until published

Saving the row settings panel updates the canvas and auto-saves a draft. Shoppers see the change only after **Publish changes** ([[landing-pages-builder-rules]]); after that, guests may still get the cached page for up to 20 minutes, and crawlers for 1–2 days ([[storefront-arch-caching-invalidation]]).

## Related

- [[marketing-landing-pages]] — hub.
- [[landing-pages-builder-rules]] — publishing, drafts, history and the plan gate.
- [[design-modules-page-builder]] — the blocks a column holds.
- [[design-module-banner]] — the **Изображения** (Images) block.
- [[design-module-grid-settings]] — the store's content width and side offset.
- [[design-custom-assets]] — custom CSS for a row's CSS class.

## Open questions

- Breakpoints on a theme that overrides the standard storefront grid. (verify)
