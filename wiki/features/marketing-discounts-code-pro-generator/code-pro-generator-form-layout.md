---
type: feature
nav_path: "Marketing → Discounts → Code PRO → Generator → Form layout"
route_name: discounts-code_pro-generator
route_path: /admin/marketing-new/discounts/code-pro/:id/generator
aliases: ["Code PRO generator form", "Generator page layout", "Generator settings boxes"]
tags: [marketing, discounts, coupons, code-pro, bulk-generation]
plan_gates: ["discount-code-pro", "discount-code-pro-generator"]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

# Code PRO generator — form layout

> Part of [[marketing-discounts-code-pro-generator]]. See the hub for related aspects (modes, fields, validation, business rules, API).

## Purpose

This aspect documents the **on-screen layout** of the Code PRO bulk-generator page: how to reach it, which settings boxes render in which order, the code-config sub-block that switches between Range and Random parameter sets, and the post-save redirect. The generator is a **full Vue page** (not a modal wizard) so every input is visible at once and the merchant scrolls through the settings boxes top to bottom before clicking Save.

## Where to find it

From the [[marketing-discounts-code-pro]] list inside any Code PRO discount, click "Generate codes" (the toolbar button labelled with a list icon — `fa-list`). The breadcrumb reads **"Marketing → Discounts → Code PRO → Generator"**. The route name is `discounts-code_pro-generator`, the path is `/admin/marketing-new/discounts/code-pro/:id/generator`.

The generator is the only way to produce more than a few Code PRO codes efficiently — the per-code form (see [[code-pro-form]]) creates one code per save and is intended for crafted, individually-named codes.

## What the merchant can do here

- See every batch-level setting on one Vue page (no modal stepper) and configure it before submitting.
- Switch between **Range** and **Random** code-string strategies — see [[code-pro-generator-modes]] for the logic behind each.
- Apply discount terms (conditions, dates, customer groups, region, limits, stacking flags) that propagate to every generated code — see [[code-pro-generator-fields]].
- Cancel (returns to the codes list without saving) or Save (kicks off generation; the button shows a loader spinner while the request is in flight).

## Settings & fields

### Settings boxes rendered, in order

The page uses the standard `CcSettingsBox` framework and renders these boxes top-to-bottom (verify):

| Section box | Fields rendered |
|-------------|-----------------|
| **General settings** | Discount `active` switch (yes/no). |
| **Code settings** | The code-config sub-block (Generator type + Range/Random parameters — see below), then `code_apply` switch ("Apply even on discounted products"), then a conditional `apply_regular_price` switch ("Apply to regular price", only visible when `code_apply = 1`). |
| **Registered users only** | `only_customer` switch — "Discount available only to registered users". This whole box is conditionally visible based on customer-related conditions being present. |
| **Customer groups** | `customer_groups_target` switch ("All groups" yes/no); when "no", a multi-select customer-groups picker appears (searchable, request-on-search, queried against `/admin/api/core/customers/groups`). |
| **Regions** | `all_regions` switch ("Make it Global" yes/no); when "no", a single-select region picker appears (searchable, request-on-search, queried against `/admin/api/core/settings/geo-zones/search`). |
| **Date range** | `date_start` (required) + `date_end`, with a `no_expire` toggle that disables the end-date field. The campaign-countdown timer sub-feature is **HIDDEN** on this page (`hide-timer: true`) — the generator's terms do not include the storefront countdown banner that the standard discount form exposes. |
| **Discount limits** | `max_uses` (per discount) and `maxused_user` (per-customer), each with their own "Unlimited" toggle that nulls the number. |
| **Conditions settings** | The repeating conditions builder — same UI as the per-code form's conditions; lets the merchant build up to 5 condition rows applied to every generated code. |

The bottom of the page is the standard `SubmitChanges` bar with **Cancel** and **Save**.

### Code config sub-block (the generator-mode picker)

Inside the "Code settings" box, this sub-component renders the mode picker:

1. **Generator type** — a non-clearable single-select dropdown with two options:
   - "Range" (`range`)
   - "Random" (`random`)
2. **Range parameters** (slides down when generator type = `range`, 130 ms animation):
   - "Code from the generator will start" — number input (`code.from`).
   - "Code from the generator will end" — number input (`code.to`).
3. **Random parameters** (slides down when generator type = `random`):
   - **Code structure** — non-clearable single-select dropdown with three options:
     - "Letters" → `structure = ['alpha']`
     - "Numbers" → `structure = ['numeric']`
     - "Letters and numbers" → `structure = ['alpha', 'numeric']` (the default)
   - **Count of codes to generate** — number input (`code.limit`); the Vue-side `:max="10000"` cap is on the input UX only — the **plan-feature cap is the real bound** (default 5,000 per request).
   - **Count of characters in code** — number input (`code.length`); the help block reads *"If blank, each code will be generated with a random length between 6 and 18 chars."*. The Vue-side `:max="10000"` is loose; the backend enforces 6-18.

The Range / Random parameter blocks are wrapped in a slide-up/down container so switching generator type smoothly swaps one parameter set for the other (no full page reload).

### Post-save redirect

On success the page waits **1.5 seconds** (giving the success toast / banner time to display) and routes the merchant back to the codes list (`discounts-code_pro-list` named route with the same `:id` param). The merchant lands on the populated list with the freshly-generated batch at the top of the date-sorted view. Success message: *"Discount was successfully added"*.

## Business rules

- The hidden timer toggle is intentional — generator batches never carry a countdown banner; only the standard per-discount form exposes that sub-feature.
- The conditional visibility of the "Apply to regular price" switch (only when `code_apply = 1`) prevents nonsensical combinations from being saved.
- The "Customer groups" picker fires a search request on every keystroke (request-on-search) — large group catalogues never load the full list upfront.

## Related

- [[marketing-discounts-code-pro-generator]] — hub.
- [[code-pro-generator-modes]] — what Range vs Random actually do once the form is submitted.
- [[code-pro-generator-fields]] — the full settings & fields tables (per-code shared terms + generator-type fields).
- [[code-pro-generator-validation]] — client-side date checks before submit; server-side validation messages.
- [[marketing-discounts-code-pro]] — the parent Code PRO discount and per-code form.
- [[code-pro-form]] — per-code editor sharing the conditions sub-component.

## Open questions

None.
