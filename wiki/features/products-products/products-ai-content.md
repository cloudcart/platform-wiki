---
type: feature
nav_path: "Products → Products → AI content (Cloudio / ShopperPen)"
route_name: products-edit
route_path: "/admin/products/edit/:id (side panel)"
aliases: ["Cloudio side panel", "ShopperPen", "AI description generator", "AI SEO generator", "Product AI content", "Cloudio bar", "Cloudio token cost", "Кладио", "Описание с AI", "Шопър пен"]
tags: [catalog, products, ai, cloudio, shopperpen, content-generation]
plan_gates: []
created: 2026-06-10
updated: 2026-11-03
source_count: 2
---

> Part of [[products-products]]. See the hub for the other aspects (list view, editor, variants matrix, bulk actions, change log, known issues).

# Products — AI content (Cloudio / ShopperPen)

## Purpose
## Purpose

The product editor exposes an in-context AI assistant — **ShopperPen**, a skill of the **CloudIO** app. It generates three kinds of merchandising copy directly from the product's existing data:

- Full product **description** (rich-text body).
- **Short description** (the card / listing teaser).
- **Meta description** (the SEO description; each result is shown in a Google-style preview with a title and the product's URL).

The merchant triggers it from the **AI bar** below these three fields on [[products-editor]]. The side panel opens with its controls, generates results, lets the merchant **Keep** one into the field, and shows the earlier results for that product and field. Generation **consumes CC-tokens** from the store's plan allotment.

## Where to find it

[[products-editor]] → **Details** (Description, Short description) or **SEO Configuration** (SEO meta description) → the **AI bar** reads *"Write with ShopperPen by CloudIO app — Boost your sales with ShopperPen: Precision-crafted product descriptions, summaries, meta titles & descriptions!"* → **Generate text** button → the side panel **ShopperPen - AI Product description generator** opens. The bar shows when the store's ShopperPen skill is active.

## What the merchant can do here

### Side panel — controls

Which controls show depends on the field being generated:

- **Length slider** (description only) — *short* / *medium* / *long*.
- **Style** dropdown (description only) — **Descriptive** or **Option list**.
- **Enable RankMaster AI** switch — see "RankMaster AI" below.
- **Select which product details to include in the description** — checkboxes for the name, short description, description, category, properties, variant values, vendor and tags. **Name + category are mandatory and locked-on.**
- **Use emojis** (meta description).
- **Enable phone** (meta description) — shows a **Phone number** input when ON.
- **Free delivery** (short + meta description) — shows a **Price** currency input.
- **Enable additional information** (short + meta description) — shows a free-text box for facts such as warranty or returns.
- **Select which image is used for the description** (description + short description, when the product has images) — needs VisionSense AI; **Activate VisionSense AI** turns it on.
- **Approximate price**, **Estimated tokens count**, **Remaining tokens** and the **Generate text** button close the panel.

### Generation flow

1. Merchant sets the controls → the estimates update.
2. **Generate text** → the task starts and a loading box appears under **Results**. While it is still starting, **Cancel task** stops it: *"Task successfully cancelled. You are not charged for this task."*
3. The result appears at the top of **Results**, with its date, the tokens used and a warning to review the AI text before use.
4. Each result has **Keep**, **Copy text**, and thumbs up / down. **Keep** puts the text into the field and closes the panel; on a meta description it fills the SEO meta description.
5. The merchant continues editing the product manually; the text is part of the unsaved form until they hit Save.

### Results + errors

**Results** lists the earlier results for this product and field, newest first, the older ones collapsed until clicked. A failed generation shows *"There is an error with generating text. Please try again in a few moments..."* with **Retry**. Under a description result, **ShopperSense Insights** explains the text: **Analyze**, or **Activate ShopperSense** first. A banner, *"Generate descriptions in bulk? Try ShopperPen Advanced"*, leads to that skill.

## Settings & fields

### CC-token cost model

Generation consumes **cc_tokens** from the store's plan allotment. **There is no per-store-per-month quota for the feature itself** — the merchant uses whatever cc_tokens their plan provides. See [[apps-cloudio-overview]] for the wallet, top-up flow, and plan-allotment table.

Each checkbox, the length, RankMaster AI and each image add to the estimate before the merchant generates. A description over 3000 characters can't be used as context: its checkbox is disabled, with the tooltip *"The description is longer than 3000 characters. You can't use it."*

### Vision-augmented description generation

When the merchant picks product images with VisionSense AI active, those images are sent to a vision-capable model so the generated description references visual specifics ("matte black finish", "knurled grip"). Each picked image adds to the estimate.

### Mandatory context fields

Name + Category are **locked-on** in the details list.

### Results do NOT auto-save

A kept result goes into the editor field as draft text. **The product itself is not saved** until the merchant clicks the main Save and publish button. The merchant can hand-edit the AI's output before saving — the recommended workflow, since the copy is a starting point, not a final article.

## Business rules

### "ShopperPen" and "CloudIO"

The AI bar labels the feature *"Write with ShopperPen by CloudIO app"* — two layers of the same offering: CloudIO is the app, ShopperPen its writing skill. For support tickets, treat them as one feature.

### Activation and tokens

The AI bar shows when the ShopperPen skill is active. **Generate text** is then gated by the CC-token wallet, not a plan-feature flag: with too few tokens it is disabled and the panel shows *"You need to purchase more tokens, to continue!"* with **Buy tokens**. See [[apps-cloudio-overview]] for the top-up flow.

### RankMaster AI

RankMaster AI is a separate skill for keyword-led writing, on all three fields. **Enable RankMaster AI** stays off until **Activate RankMaster AI** turns the skill on. Once enabled, it adds **Keywords** (up to 5, with **Get suggestions** at 50 tokens after the first one) and, on the description and short description, **Add link: See more from the same brand**, **Add a link to the product category** and **Turn on E-E-A-T**. The panel still works without it.

### One task at a time

While a task runs for a field of a product, **Generate text** is disabled for it, and the panel picks up the running task when reopened.

### Results are kept with the product

Results stay after a reload or a closed panel, so an older one can still be kept when the panel next opens. A kept text lives in the editor field until the next save.

### Long-form fields are NOT in the Change log

The Change log ([[products-change-log]]) records the placeholder `"To long"` for `description` / `short_description` rather than the full text. So a generated description appears only as a *"description was changed"* marker without before / after content. The panel's **Results** keep the generated versions.

## Related

- [[products-products]] — hub.
- [[products-editor]] — the editor that hosts the AI bar + side panel.
- [[apps-cloudio-overview]] — CC-token wallet, plan allotment, top-up flow, and the cross-product feature catalogue (Cloudio is also used for category description, blog post generation, etc.).
- [[products-change-log]] — long-form fields show as `"To long"` placeholders rather than full diff.

## Open questions

- Whether the vision model reads every picked image or only the first few — verify.
