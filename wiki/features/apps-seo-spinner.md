---
type: feature
nav_path: "Apps → SEO Spinner"
route_name: apps.seo-spinner.overview
route_path: /admin/apps/seo-spinner
aliases: ["SEO Spinner", "Seo Spinner", "Content spinner", "no enable disable button", "app has no active toggle"]
tags: [apps, marketing, seo, content-generation]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 1
---
# SEO Spinner (content variation generator)

## Purpose

**SEO Spinner** generates **SEO title + meta description variations** for products, categories, and vendors/brands. It helps the merchant:

- Avoid duplicate-content SEO penalties when many similar records (variations, brands) need distinct text for Google.
- Bulk-create SEO content for large catalogs where manual writing isn't feasible.

The "spinner" name refers to content-spinning — producing multiple unique variants of the same source text. **It is template-based, not AI.** The merchant writes title/description templates with built-in alternatives, and the spinner picks randomly per record. There is no synonym dictionary and no AI — the merchant supplies the alternatives themselves.

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.

## Where to find it

Sidebar → Apps → install → **SEO Spinner**. See [[apps-seo-spinner-settings]] for configuration.

## What the merchant can do here

- Pick which records to spin: specific categories / vendors, or "all", per entity type.
- Write **title variations** and **description variations** as templates (spin syntax below).
- Generate a preview, edit any individual preview row, bulk-delete rows, or re-generate.
- Finalize by clicking **Override old data** to write the previews into the live SEO fields.

### What the merchant CANNOT do here

- Spin blog articles, custom pages, or general meta-tag content — only products, categories, and vendors.
- Roll back after **Override old data** — there is no per-spin history or undo; the previous SEO title/description are overwritten in place and gone unless saved elsewhere. The only safety net is the preview step.

## Settings & fields

### Spin syntax (used in title and description templates)

1. **Random choice — `{a|b|c}` group.** Anywhere in a template the merchant writes e.g. `{product|item|article}`; the spinner picks one option at random per record. The braces-with-pipes pattern is the entire spinning mechanism.
2. **Placeholders — `{$var}`.** Replaced with the record's actual data. Available per entity type:
   - **Products:** `{$name}`, `{$sku}`, `{$category}`, `{$shopName}`, `{$price}`, `{$vendor}`, `{$weight}`.
   - **Categories:** `{$name}`, `{$productsCount}`, `{$shopName}`.
   - **Vendors / brands:** `{$name}`, `{$productsCount}`, `{$shopName}`.

Example: `This {product|item} is at a great price of {$price}` becomes *"This product is at a great price of BGN 16"* or *"This item is at a great price of BGN 16"*.

### Length warning (not enforced)

The UI shows a warning that the title should stay under **65 symbols** and the description under **155 symbols**. These limits are **not enforced** — the spinner writes the full templated text without clipping, so the merchant is responsible for keeping templates within Google's recommended limits.

### "Replace existing spun records" toggle (`replace_<group>_seo`)

By default the spinner only touches records whose SEO has **never** been spun. The `replace_<group>_seo` setting (one per entity type) tells the spinner to also override records it had spun previously.

## Business rules

### Workflow: conditions → preview → finalize

1. **Conditions step** — define one or more conditions: pick the models (specific categories / vendors / "all"), then add title and description variations using the spin syntax.
2. **Preview step** — the spinner generates a temporary preview row for every matching record. The merchant can edit any row, bulk-delete, or re-generate. Until finalize runs, the live storefront SEO is unchanged — full preview-before-apply safety net.
3. **Finalize ("Override old data")** — writes the previews into the actual product / category / vendor SEO `title` and `meta description` fields. There is no built-in undo. After override, the preview rows are cleared so the next run starts clean.

### Plan-gated by record count, per entity type

Each entity type is its own plan feature, in the format `seo-spinner.<group>` — `seo-spinner.product`, `seo-spinner.category`, `seo-spinner.vendor`. Each group has its own record-count meter: a merchant with `seo-spinner.product = 1000` and `seo-spinner.category = 100` can spin 1,000 products and 100 categories independently. When a group's limit is reached during generation, the merchant gets an in-platform notification with an upgrade link.

The upgrade-CTA button appears **only** when the plan feature for that group is registered AND active AND its limit is a positive number. If the plan has unlimited records or the feature is disabled, no upgrade prompt appears.

### Marked as "generated through spinner"

Every record the spinner touches gets flagged as spinner-generated (`seo_generated_through_spinner = 1`). This lets the spinner skip already-spun records on the next run (unless **Override old data** / `replace_<group>_seo` is on) and is how the platform knows the SEO came from the spinner.

### Not language-aware

The spinner runs against the record's main SEO `title` / `meta description` fields — there is no "spin only Bulgarian" toggle. Multi-language stores must run the spinner once per language by switching the admin language, or hand-translate the spun output.

### Preview rows auto-clean on record delete

When the merchant deletes a product, category, or vendor, any matching spinner preview rows for it are auto-deleted, so record cleanup leaves no orphan preview rows behind.

## Related

- [[apps]] — App Store.
- [[apps-seo-spinner-settings]] — settings sub-page.
- [[products-products]] — product SEO targeted by spinner.
- [[products-categories]] — category SEO.
- [[marketing-seo]] — SEO landing.
- [[marketing-seo-meta]] — meta-tag content (note: not directly spinnable).

## Open questions
