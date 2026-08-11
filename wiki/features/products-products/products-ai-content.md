---
type: feature
nav_path: "Products → Products → AI content (Cloudio / ShopperPen)"
route_name: products-edit.new
route_path: "/admin/products/products-new/edit/:id (side panel)"
aliases: ["Cloudio side panel", "ShopperPen", "AI description generator", "AI SEO generator", "Product AI content", "Cloudio bar", "Cloudio token cost", "Кладио", "Описание с AI", "Шопър пен"]
tags: [catalog, products, ai, cloudio, shopperpen, content-generation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[products-products]]. See the hub for the other aspects (list view, editor, variants matrix, bulk actions, change log, known issues).

# Products — AI content (Cloudio / ShopperPen)

## Purpose

The product editor exposes an in-context AI assistant — branded **Cloudio** in the platform UI and powered by the **ShopperPen** product of the CloudIO app. It generates four kinds of merchandising copy directly from the product's existing data:

- Full product **description** (rich-text body).
- **Short description** (the card / listing teaser).
- **SEO description** + **SEO title** (the `<meta>` block).
- **URL handle** (the slug).

The merchant triggers it from the **Cloudio bar** below each rich-text editor on [[products-editor]]. The side panel opens with a token-aware controls strip, generates a proposal, lets the merchant Accept it into the editor field, and keeps a per-session history. Generation **consumes CC-tokens** from the store's plan allotment.

## Where to find it

[[products-editor]] → any rich-text editor (Description, Short description, SEO description) → the **Cloudio bar** below the editor reads *"Write with ShopperPen by CloudIO app — Boost your sales with ShopperPen: Precision-crafted product descriptions, summaries, meta titles & descriptions!"* → **Generate text** button → side panel opens.

## What the merchant can do here

### Cloudio side panel — controls strip

The side panel opens with these controls (available controls depend on which field is being generated):

- **Range** (description only) — target description length.
- **Style** dropdown (description only) — description tone / style from a server-provided list.
- **RankMaster** subscription state indicator.
- **Product detail checkboxes** — each feeds a piece of context to the AI (name, category, price, vendor, etc.). **Name + category are mandatory and locked-on.** Each checkbox shows its CC-token cost in the live counter.
- **Use emojis** toggle (meta_description only).
- **Enable phone** toggle (meta_description) — shows a phone input when ON.
- **Free delivery** toggle (short_description + meta_description) — shows a Price currency input.
- **Enable additional information** toggle — shows a free-text textarea for arbitrary facts.
- **Images** picker (description only) — pick product images for the AI to "look at" (vision-augmented generation).

### Generation flow

1. Merchant configures the controls strip → the live **token counter** updates with the projected cost.
2. Merchant clicks Generate → the request is dispatched to the CloudIO ShopperPen backend.
3. The proposal renders in the right column of the side panel, alongside the **history** + **error log** of earlier attempts in the session.
4. Each historical result has **Accept** / **Reject** buttons. Accepting pastes the result into the editor field. Rejecting keeps it in history without applying.
5. The merchant continues editing the product manually; the proposal becomes part of the unsaved-form state until they hit Save.

### History + error log

The right column of the panel shows every proposal generated in this session (newest first), plus any error messages from the backend (e.g. *"insufficient cc_tokens"*, *"image-vision endpoint timeout"*). The merchant can re-Accept an older proposal at any time, or re-Generate with adjusted controls.

## Settings & fields

### CC-token cost model

Cloudio descriptions / SEO / handle generation consume **cc_tokens** from the store's plan allotment. **There is no per-store-per-month quota for the Cloudio feature itself** — the merchant uses whatever cc_tokens their plan provides. See [[apps-cloudio-overview]] for the wallet, top-up flow, and plan-allotment table.

Each checkbox + each image contributes to the projected cost; the live counter reflects this before the merchant generates. Empty checkboxes whose underlying field is over 3000 chars are auto-disabled (they would silently inflate cost without adding useful context).

### Vision-augmented description generation

When the merchant picks product images in the **Images** picker (description-only), those images are sent to a vision-capable model so the generated description references visual specifics ("matte black finish", "knurled grip"). Vision tokens cost more than text tokens — reflected in the live counter.

### Mandatory context fields

Name + Category are **locked-on**: a product with no name or no category is too underspecified for usable copy, and the panel disables Generate until both are set.

### Proposals do NOT auto-save

An accepted proposal is pasted into the editor field as draft text. **The product itself is not saved** until the merchant clicks the main Save and publish button. The merchant can hand-edit the AI's output before saving — the recommended workflow, since Cloudio's copy is a starting point, not a final article.

## Business rules

### "ShopperPen" branding vs "Cloudio" branding

The Cloudio bar labels the feature *"Write with ShopperPen by CloudIO app"* — two layers of the same offering. The side-panel feature name is **Cloudio**; ShopperPen is the description-quality engine behind it. For support tickets, treat them as one feature.

### Cloudio activation gating

The Cloudio bar and side panel appear for every store. **Generation is gated by the CC-token wallet**, not a plan-feature flag. A store with zero cc_tokens sees the panel, but Generate surfaces an "insufficient cc_tokens" error. See [[apps-cloudio-overview]] for the top-up flow.

### RankMaster — separate subscription indicator

RankMaster is the SEO-quality variant of the same engine. With an active RankMaster subscription, SEO description / title generation uses a prompt tuned for SERP-friendly copy. The controls-strip indicator surfaces whether the store has it; the panel still works without it, using the default prompt.

### Per-image cost — large galleries get expensive fast

Picking 5 images is materially more expensive than 1 (vision tokens scale with image count). The live counter is the merchant's guard; there is no hard cap beyond the per-product image limit, but Cloudio reads only the first N images (verify N) when more are picked.

### History is per-session

The right-column proposal history is per browser session — refreshing or closing the editor discards it. The merchant should Accept proposals they want to keep BEFORE leaving the editor. Once Accepted, the proposal lives in the editor field and survives reloads (until next save).

### Long-form fields are NOT in the Change log

The Change log ([[products-change-log]]) records the placeholder `"To long"` for `description` / `short_description` rather than the full text. So a Cloudio-generated description appears only as a *"description was changed"* marker without before / after content. Use the editor's undo / browser history to compare drafts.

## Related

- [[products-products]] — hub.
- [[products-editor]] — the editor that hosts the Cloudio bar + side panel.
- [[apps-cloudio-overview]] — CC-token wallet, plan allotment, top-up flow, and the cross-product feature catalogue (Cloudio is also used for category description, blog post generation, etc.).
- [[products-change-log]] — long-form fields show as `"To long"` placeholders rather than full diff.

## Open questions

- The exact image-count cap that Cloudio vision-mode reads when the merchant picks > N images — verify.
- Whether RankMaster's SEO model is also used for the URL-handle generator or only for `meta_title` / `meta_description` — verify.
