---
type: feature
nav_path: "Marketing → Pages → Dynamic page → page builder → Social Feed block"
route_name: admin.pages.builder
route_path: /admin/marketing/pages/builder/{page_id?}
aliases: ["Social Feed block", "social-feed block", "Social Feed module in the page builder", "Instagram block on a landing page", "Heading (optional)", "As in the app settings", "All connected (tabs)", "Open Style settings", "Install and switch on the app", "Заглавие (по желание)", "Както в настройките на приложението", "Отвори настройките „Стил“", "Инсталирай и включи приложението", "Social Feed блок"]
tags: [apps, social-feed, page-builder, landing-pages, homepage]
plan_gates: [storefront_builder]
created: 2026-10-05
updated: 2026-10-05
source_count: 8
---

# Social Feed — page-builder block

> Part of [[apps-social-feed]]. See the hub for the other aspects (accounts, style, placement, the storefront, refresh).

## Purpose

The **Social Feed** block puts the feed at an exact spot on a Dynamic page: a landing page, or the Dynamic page assigned as the homepage. It can carry its own heading and its own network, layout, theme and effect. Everything else comes from the app's **Style** tab, so the feed is styled in one place.

## Where to find it

Sidebar → **Marketing → Pages** → open or create a **Dynamic page** → the page builder (`/admin/marketing/pages/builder/{page_id?}`) → add a block → **Social Feed**. The block list describes it as *"Your latest Instagram, Facebook and TikTok posts, anywhere on the page."* (*"Последните ти публикации от Instagram, Facebook и TikTok — навсякъде в страницата."*).

The block is offered only while the Social Feed app is **installed and enabled**. See [[design-modules-page-builder]] for the page builder itself.

## What the merchant can do here

- Add the feed anywhere on a Dynamic page, including next to other blocks in a row.
- Give it a heading.
- Show a different network, layout, theme or effect than the app's Style tab.
- Switch the block off without removing it.

## Settings & fields

A preview at the top of the block's settings follows every choice before saving.

| Field | Default | Options / limits |
|---|---|---|
| **Heading (optional)** (Заглавие (по желание)) | Empty | Up to 100 characters. Shown centred above the feed. |
| **Network** (Мрежа) | **As in the app settings** | **All connected (tabs)**, **Instagram**, **Facebook**, **TikTok** |
| **Layout** (Оформление) | **As in the app settings** | **Classic grid**, **Single line**, **Collage** |
| **Theme** (Тема) | **As in the app settings** | **Light**, **Dark** |
| **Effect** (Ефект) | **As in the app settings** | **Stationary**, **Moving**. Hidden when the layout is **Collage**. |
| On/off switch | On | The page builder's usual switch for a block. |

**As in the app settings** (Както в настройките на приложението) shows the app's current choice in brackets, for example *As in the app settings (Classic grid)*.

Under the fields:

- Info: *"The choices made here take priority over the app's Style settings. Drop this block exactly where you want the feed — on a page that has the block, the automatic section above the footer is not shown."*
- Help: *"Number of posts, show/hide toggles and button colour come from the app's Style settings."* followed by the link **Open Style settings** (Отвори настройките „Стил“), which opens the app's Style tab in a new tab.

## Business rules

### What the block can and cannot change

The block decides only **Network**, **Layout**, **Theme** and **Effect**. **Number of posts**, the five show/hide switches and **Button colour** always come from the Style tab ([[apps-social-feed-style]]).

### It hides the automatic section on its page

A page with a Social Feed block never shows the automatic section above the footer as well ([[apps-social-feed-placement]]).

### Network lists all three networks

Unlike the Style tab, the block offers **Instagram**, **Facebook** and **TikTok** even when they are not connected. A block set to a network that is not connected shows nothing on the storefront.

### The preview in the builder

Inside the page builder, the block is drawn from posts the store has already stored; it never asks the networks. Until the feed has been viewed once, the tiles are grey placeholders. Small labels under it name the layout, theme and effect in use.

### When the app is off or gone

- **Enabled, nothing connected:** the block can be added, but shows nothing on the storefront.
- **Disabled or uninstalled:** blocks already on pages stay there but show nothing to shoppers. The block's settings show *"Install and switch on the app"* (*"Инсталирай и включи приложението"*), with a **Social Feed** link to the app, and no save button.

### Plan

The page builder needs the `storefront_builder` plan feature ([[plan-gates]]). On a plan without it, the automatic section is the only way to show the feed.

## Related

- [[apps-social-feed]] — hub.
- [[design-modules-page-builder]] — the page builder's block catalogue.
- [[marketing-landing-pages]] — Dynamic pages.
- [[landing-pages-system-slots]] — making a Dynamic page the homepage.

## Open questions

- None specific to the block. See the hub for the app-wide questions.
