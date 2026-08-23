---
type: feature
nav_path: "Marketing → SEO → Sharing"
route_name: seo-main
route_path: /admin/marketing-new/seo
aliases: ["Share a product", "Social sharing", "AddThis", "AddThis share", "Sharing module", "Share module", "Cover image for sharing", "Open Graph image", "og:image default", "Споделяне на продукт", "Социално споделяне", "Споделяй продукт", "Снимка за споделяне", "OG изображение"]
tags: [marketing, seo, sharing, distribution]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 4
---
# Social sharing module & default Open Graph image

## Purpose

> **The Sharing card is no longer part of the Marketing → SEO screen.** It was removed when the [[marketing-seo-llms|Llms.txt]] card took its place. The default Open Graph image is now uploaded on **Settings → Brand** ([[settings-brand]]). Where the social-share toolbar is configured today is unconfirmed — see *Open questions*. The behaviour described below still applies to the storefront; only the admin location changed.

This was the **"Share a product"** card on the [[marketing-seo]] screen. It bundles two unrelated outcomes into one admin card and one save call:

1. A built-in **social-sharing toolbar** (an AddThis-style module that historically sat on product detail pages) — visual layout, which counters/buttons show, custom HTML override. **Disabled on every modern theme** — see [[seo-sharing-toolbar]].
2. The **default `og:image`** — the fallback Open Graph cover image used in link previews on Facebook / LinkedIn / X / Viber when a shared storefront page has no image of its own. **This is the only field that matters on modern themes** — see [[seo-sharing-og-image]].

Practical guidance: on any modern storefront theme, ignore every toolbar toggle on this card and just set the **Main sharing picture** (the `og:image`) and Save. The toolbar toggles are stored but do nothing on the storefront.

## Where to find it

Sidebar → Marketing → **SEO** → scroll to the **"Share a product"** card. Route is `/admin/marketing-new/seo`. The card has its own inline Save / Revert bar that appears only after the merchant changes a field.

## What the merchant can do here

- Upload, replace, or delete the **Main sharing picture** (default `og:image`) via the Filemanager picker — see [[seo-sharing-og-image]].
- Toggle the social-share module on/off and configure its layout, visual options, and custom HTML — see [[seo-sharing-toolbar]].

What the merchant CANNOT do here: pick which networks appear in the toolbar; set a per-product `og:image` (that lives on the [[product]] editor); set an AddThis pubid; set `og:title` / `og:description` defaults (those come from [[marketing-seo-meta]]); change the module colour palette or `ui_language` (stored with defaults but not exposed in the UI). Details per aspect.

## Settings & fields

The card has three groups separated by horizontal rules: the master enable + visual switches, the layout selects, and the cover-image picker. The full field reference is split by concern:

- **Cover-image field** (`Main sharing picture` → `og_image_url`) — see [[seo-sharing-og-image]].
- **Toolbar fields** (`Share product`, `Format`, `Show share count`, `Show button for other social networks`, `Show top networks`, `UI click`, `Dropdown direction`, `Toolbar code`) — see [[seo-sharing-toolbar]].
- **Where each field is persisted + the validation map** — see [[seo-sharing-storage-save]].

The card uses the shared **Save / Revert** wrapper — both buttons appear in an inline action bar at the bottom of the card only after the merchant changes any field. Save toast: "Saved Successfully".

## Business rules

- **Toolbar render is hard-disabled on every modern theme.** The "Share product" switch and all its visual sub-options have no visible storefront effect. See [[seo-sharing-toolbar]].
- **`og_image_url` is the only field that actually matters** — it is the fallback cover image everywhere a storefront page has no per-entity OG image. See [[seo-sharing-og-image]].
- **Sharing settings and `og:image` are stored in two different places**: the toolbar config in a theme-scoped module settings row (so it can reset on theme change), `og_image_url` in the global settings table (survives theme change). The save also hits a legacy endpoint and has an `enabled = 0` strip quirk. See [[seo-sharing-storage-save]].
- **Permission:** the endpoint sits behind `hasApiPermission:marketing.seo`.
- **Plan gates:** none — included on every plan.

## Sub-pages (in this cluster)

- [[seo-sharing-og-image]] — the default `og:image` (`Main sharing picture`): what it falls back for, where it kicks in, the "broken Facebook preview" support pattern, the 1200 × 630 recommendation.
- [[seo-sharing-toolbar]] — the AddThis-style social-share toolbar: every toggle, Custom-format HTML override, and why the toolbar is hard-disabled on every modern theme.
- [[seo-sharing-storage-save]] — storage + save mechanics: the two-store split, the legacy `/add-this` endpoint, the validation map, the `enabled = 0` strip quirk, the non-UI colour/language defaults.

## Related

- [[marketing-seo]] — Main SEO settings (parent screen / hub).
- [[marketing-seo-meta]] — per-section meta titles & descriptions; source of the `og:title` / `og:description` defaults the storefront renders (not this card).
- [[marketing-seo-rss]] — RSS feed configuration (sibling card on the same SEO screen).
- [[marketing-seo-canonical]] — canonical-tag setting (sibling card).
- [[marketing-seo-deindex]] — noindex on filtered/sorted pages (sibling card).
- [[marketing-seo-sitemap]] — sitemap.xml URL display (sibling card).
- [[marketing-seo-robots]] — robots.txt editor (sibling card).
- [[marketing-seo-meta-title]] — pagination word in meta titles (sibling card).
- [[product]] — per-product Open Graph image override.
- [[category]] — per-category OG image override.

## Open questions

- Where the product social-share toolbar is configured now that the card has been removed from the SEO screen — whether it moved to another screen, or the toolbar is driven only by the theme.

No outstanding questions.
