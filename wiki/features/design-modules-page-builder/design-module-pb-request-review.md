---
type: feature
nav_path: "Marketing → Dynamic Pages → Page-builder modules → Request review"
route_name: admin.pages.builder
route_path: /admin/marketing/pages/builder/{page_id?}
aliases: ["Request review module", "Leave a review form", "Review submission form", "Модул заяви отзив"]
tags: [design, modules, page-builder, product-review, marketing, reviews]
plan_gates: [storefront_builder]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Request review block (`request_review`)

> Part of [[design-modules-page-builder]]. See the category page for the other page-builder modules.

## Purpose

The **Request review** block renders a form / CTA that invites the customer to submit a product review on a Dynamic page. Used after a purchase ("How was your order?"), on a Thank-you page ("Leave a review and earn 10% off"), or on a campaign page that recruits brand advocates. The submitted review lands in the Product Review app's moderation queue — see [[apps-product-review]].

## Where to find it

Open a Dynamic page in [[marketing-landing-pages]] → click **+ Add block** → pick **Request review** from the block picker.

The block only appears in the picker when the Product Review app is installed AND enabled. On stores without it, the picker hides the block; if already added, the storefront renders the "Application not installed" notice.

## What the merchant can do here

- Toggle **Enable slider** — when ON, the form renders in a carousel-style container (when paired with multiple instances); when OFF, as a static block.
- Set the section **Title** (heading above the form).
- Set the section **Description** (intro paragraph above the form).
- Set the accent **Color** (hex / colour picker) — used for the icon / accents.
- Set **Per row** — when multiple instances are stacked, how many forms per row (default 3).
- Toggle the master enable switch.

## What the merchant cannot do here

- The merchant cannot customise the form fields (rating, comment, photo upload) — the form schema lives in the Product Review app.
- The merchant cannot pre-fill the form with a specific product — the form picks up the product context from the page (when on a product-bound page) or asks the customer to pick.
- The merchant cannot send the review directly to the storefront — submissions go to the moderation queue first.

## Settings & fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `enabled` | toggle | `true` | Master on/off. |
| `enable_slider` | toggle | `true` | Render in carousel container vs. static. |
| `title` | text input | `''` | Section title above the form. |
| `description` | textarea | `''` | Intro paragraph above the form. |
| `color` | colour picker (hex) | `#bab1b1` | Accent colour for icon / borders. |
| `per_row` | number | `3` | Forms per row when stacked. |

### Save / Reset / Cancel

Page-builder side panel — see [[marketing-landing-pages]]. The `saveSettings` method coerces `enabled` and `enable_slider` to `int(0|1)` and parses the icon picker into a JSON blob if set.

## Business rules

### App-gated

The block only registers when the Product Review app is installed AND enabled. On stores without it, the block is absent from the picker, and on the storefront the legacy fallback notice "Application 'Product Review' is not installed" renders in place of the form.

### Submissions go to the moderation queue

Submitted reviews are NOT immediately published — they land in the Product Review app's moderation queue where the merchant approves or rejects them. Approved reviews then surface in [[design-module-pb-product-review]] and on individual product pages.

### Product context

When the page itself binds to a product (e.g., a single-product launch page), the form can pre-fill the product context. On generic Dynamic pages, the form asks the customer to pick the product they want to review. (verify the exact UX per theme)

### Theme dependencies for icon picker

Some themes ship an icon picker for the form (a custom badge / star icon shown alongside the title). The block surfaces an `icon` setting (parsed by `_getIconData`); themes without icon-picker support hide it.

### Color accent

The `color` field controls the accent colour for the form's icon / border. It's a free-form hex value defaulting to `#bab1b1` — the merchant can change it to match the page's palette.

## Related

- [[design-modules-page-builder]] — hub.
- [[design-module-pb-product-review]] — sibling: product review listing block (consumes the submissions this form creates).
- [[apps-product-review]] — Product Review app (gates this module; review moderation lives here).
- [[marketing-landing-pages]] — Dynamic pages — the surface this module appears in.

## Open questions

- 📡 **Product picker UX.** On non-product-bound Dynamic pages, how does the customer pick which product to review — autocomplete, dropdown, or order-based picker? (verify per theme)
- 📡 **Email reminder integration.** Does this block integrate with the Product Review app's email-reminder flow (e.g., a customer clicks an email link → lands on a Dynamic page hosting this form, with the order context pre-filled)? (verify)
