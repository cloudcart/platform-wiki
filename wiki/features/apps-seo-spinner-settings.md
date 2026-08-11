---
type: feature
nav_path: "Apps → SEO Spinner → Settings"
route_name: apps.seo-spinner.settings
route_path: /admin/apps/seo-spinner/settings
aliases: ["SEO Spinner Settings", "Content spinner config"]
tags: [apps, marketing, seo-spinner, content-generation, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 1
---
# SEO Spinner → Settings

## Purpose

The **Settings** tab is where the merchant configures **content sources** (which entities to spin descriptions for), **spinning parameters** (variation count, tone, language), and trigger preferences. See [[apps-seo-spinner]] for the full feature set.

## Where to find it

Sidebar → Apps → SEO Spinner → **Settings tab**. Route: `/admin/apps/seo-spinner/settings`.

## What the merchant can do here

### Content sources

| Field | Notes |
|---|---|
| **Entity types to spin** | Products / Categories / Blog articles / Meta-tag fields / Custom pages. Multi-select. |
| **Filter rules** | Per entity-type filter (e.g., "products in category X only"). |
| **Skip already-spun** | Avoid re-spinning content the spinner already produced. |

### Spinning parameters

| Field | Notes |
|---|---|
| **Number of variations** | How many variations to generate per record (3 / 5 / 10). |
| **Tone** | Professional / Conversational / Marketing / Technical. |
| **Length** | Short / Medium / Long. |
| **Language** | Per-storefront-language generation. |

### Trigger

| Setting | Notes |
|---|---|
| **Trigger mode** | On-demand (merchant clicks) / Auto (on product create / update). |
| **Schedule** | When auto, the cadence (immediate / hourly / daily). |

### What the merchant CANNOT do here
- Edit the prompt template directly — platform-managed.
- Use without a subscription / available token quota (if AI-powered).

## Settings & fields

Per [[apps-seo-spinner]] Manager:
- `appInfo` — App Store metadata.
- `getMoreRecordsUrl($group)` — pagination for spun records.

## Business rules

### AI-powered (likely Cloudio)

The spinner likely uses Cloudio AI ([[apps-cloudio-overview]]) under the hood — consumes tokens per generation. The relationship between Spinner + Cloudio is not yet fully verified.

### Quality control

The merchant should review generated content before publishing — auto-spun content may need light editing for brand voice.

### Permission
Standard apps permission scope.

## Related

- [[apps-seo-spinner]] — hub.
- [[apps-cloudio-overview]] — likely underlying AI engine.
- [[products-products]] — product descriptions targeted.
- [[products-categories]] — category descriptions.
- [[marketing-blog-articles]] — blog article spinning.
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

The settings UI displays a list of allowed variables for the current group; the merchant clicks one to copy it into the template field.

### Override-old-data per group

Each group (`product`, `category`, `vendor`) has its own `replace_<group>_seo` setting. Off (default) skips records previously processed by the spinner. On includes them — the spinner will overwrite SEO it had generated on a past run. The setting does not unlock manually-written SEO; that is always overwritten when the merchant clicks **Override old data**.

### No built-in rollback

There is no "Undo last spin" button. The platform does not snapshot the prior SEO before overwriting. The safety net is the **preview step** (the merchant inspects every generated row in the temp-data table and can delete or edit each row before pressing **Override old data**). After the override runs, only manual restoration from a backup recovers the previous SEO.

### Per-record limit comes from the plan

The settings page does not let the merchant pick a "max records to spin" number. The plan dictates how many records each group can spin (e.g., 1,000 products, 100 categories). When the limit is hit mid-run, an a plan-restriction error notification fires with an upgrade prompt, and the remaining records are skipped.

### Single-language

The spinner reads / writes the SEO field directly on the model, which is single-string per record. It does not translate. Merchants running multiple storefront languages spin once per language by switching the admin UI language and re-running. The quality of the variations is whatever the merchant types — performance does not depend on language.

## Open questions

