---
type: feature
nav_path: "Apps → SEO Spinner → Settings"
route_name: apps.seo-spinner.settings
route_path: /admin/apps/seo-spinner/settings
aliases: ["SEO Spinner Settings", "Content spinner config"]
tags: [apps, marketing, seo-spinner, content-generation, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-10-21
source_count: 1
---
# SEO Spinner → Settings

## Purpose

The **Settings** tab is where the merchant writes **SEO title and SEO description templates** for three groups — **Products**, **Categories** and **Vendors** — in one or more **conditions** per group, each limited to chosen categories (or vendors) or covering all. The app then generates one SEO title and one SEO description per record from those templates, for the merchant to preview and apply. See [[apps-seo-spinner]] for the full feature set.

## Where to find it

Sidebar → Apps → SEO Spinner → **Settings tab**. Route: `/admin/apps/seo-spinner/settings`. The tab shows a notice that a new version is coming and a **Proceed to the old version of the application** button; that button opens the settings screen described below, on its **Products** tab.

## What the merchant can do here

### Group tabs

**Products**, **Categories**, **Vendors** — each tab has its own conditions and its own **Override old data** switch.

### Conditions

| Control | Notes |
|---|---|
| **+** | Adds an empty condition box. |
| **Categories** / **Vendors** select | Which records the condition covers: on **Products**, the categories whose products are covered; on **Categories**, the categories themselves; on **Vendors**, the vendors. Left empty, the condition covers every record of the group. |
| **Title's variations** | One or more SEO title templates (**Add variation** adds another). |
| **Description's variations** | One or more SEO description templates. |
| **Save condition** / **Duplicate** / **Delete condition** | Per condition box. |

Templates can use the variables listed above the conditions (click one to copy it) and groups such as `{word one|word two|word three}`, from which one word is picked at random for each record.

### Generate and apply

- **Override old data** — off: records whose SEO the spinner already wrote are skipped; on: they are generated again.
- **Generate all combinations** (appears after a condition is saved) — queues a background task that builds one title and one description per record.
- **Records** — the preview list of the generated titles and descriptions; each row can be edited or deleted, and **Finalize** writes them into the records' SEO fields.

Nothing runs automatically — there is no trigger on product create / update and no schedule.

### What the merchant CANNOT do here
- Have the text written for them — there is no AI, tone, length or variation-count setting; the output is only what the templates produce.
- Generate more records per group than the plan allows.

## Settings & fields

- **Counter** — "X from Y items with generated SEO": the group's records whose SEO the spinner wrote, against the plan's limit (∞ when the plan sets none).
- **Plan limit button** — when the plan sets a limit for the group, a button at the top ("You have a … of products to …") leads to the plan page for more records.
- The condition fields and switches listed above.

## Business rules

### Template-based, not AI

The spinner does not use [[apps-cloudio-overview]] or any other AI service and consumes no tokens — see *How it works* below.

### Quality control

The merchant should review generated content before publishing — auto-spun content may need light editing for brand voice.

### Permission
Standard apps permission scope.

## Related

- [[apps-seo-spinner]] — hub.
- [[apps-cloudio-overview]] — the AI content app; not used by the spinner.
- [[products-products]] — product SEO titles and descriptions.
- [[products-categories]] — category SEO titles and descriptions.
- [[products-vendors]] — vendor SEO titles and descriptions.
- [[marketing-seo-meta]] — meta-tag content.

## How it works (verified against backend)

### Not AI — pure template engine

This app is not connected to [[apps-cloudio-overview]] or any AI service. The "spinning" mechanism is purely string-replacement: random pick from `{a|b|c}` groups + substitution of `{$variable}` placeholders. There is no token cost, no API key, and no usage quota beyond the plan-gated record-count limit.

### The merchant writes the variations

Every variation is supplied by the merchant in the **Condition** form. The "quality" of the output equals the quality of the merchant's templates — there is no auto-rephrasing, no synonym dictionary, no tone control. If the merchant writes two title templates and three description templates against 1,000 products, every product will end up with one of the 2×3 = 6 combinations (with `{$name}`, `{$sku}` etc substituted to the per-product values).

### Available placeholders per entity

| Entity | Placeholders |
|---|---|
| Product | `{$name}`, `{$sku}`, `{$category}`, `{$shopName}`, `{$price}`, `{$vendor}`, `{$weight}` |
| Category | `{$name}`, `{$productsCount}`, `{$shopName}` |
| Vendor / Brand | `{$name}`, `{$productsCount}`, `{$shopName}` |

The settings UI displays a list of allowed variables for the current group; the merchant clicks one to copy it to the clipboard and pastes it into a template.

### Override-old-data per group

Each group tab (**Products**, **Categories**, **Vendors**) has its own **Override old data** switch. Off (default) skips records previously processed by the spinner. On includes them — the spinner will overwrite SEO it had generated on a past run. The switch does not protect manually-written SEO: records the spinner never processed are always included, and their SEO is overwritten when the merchant clicks **Finalize** on the **Records** page.

### No built-in rollback

There is no "Undo last spin" button. The platform does not snapshot the prior SEO before overwriting. The safety net is the **preview step** (the merchant inspects every generated row in the **Records** list and can edit or delete each row before pressing **Finalize**). After the override runs, only manual restoration from a backup recovers the previous SEO.

### Per-record limit comes from the plan

The settings page does not let the merchant pick a "max records to spin" number. The plan dictates how many records each group can spin (e.g., 1,000 products, 100 categories). When the limit is hit mid-run, the store owner is notified that the plan's limit was reached, and the remaining records are skipped.

### Single-language

The spinner reads / writes the SEO field directly on the model, which is single-string per record. It does not translate, and it does not read the admin's interface language — running it again overwrites the same SEO fields. The quality of the variations is whatever the merchant types — performance does not depend on language.

## Open questions

