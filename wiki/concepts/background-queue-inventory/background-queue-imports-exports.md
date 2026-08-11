---
type: concept
nav_path: "Concept → Background processes → Imports, exports, image fetch"
aliases: ["Background imports", "CSV import queue", "XML import queue", "ERP feed sync", "Background exports", "Image fetch from URL", "On-demand merchant processes"]
tags: [background, async, imports, exports, images, support, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[background-queue-inventory]]. See the hub for related aspects (recurring platform jobs, the search index sync, order side-effects, Queue View, process catalogue).

# Background processes — imports, exports, image fetch

## Definition

**On-demand merchant-triggered background processes** are the async jobs that fire when the merchant uploads a file, clicks **Export**, triggers an ERP sync, or pastes a remote image URL. They run on the platform's shared queues — visible imports show up on [[settings-queue-view]] with progress; most other on-demand work runs silently and the merchant sees the result on the surface that triggered it ([[settings-import-history]] for imports, the email arrival for exports, the product detail page for the fetched image).

Plan tier decides priority on shared queues: higher-tier merchants are processed before lower-tier merchants in the same queue. There is no merchant-configurable override — the priority follows the plan tier (see [[background-queue-view-and-stuck]] for details).

## Scope

Covered:

- CSV imports for products, customers, subscribers, blog articles, URL redirects.
- XML / JSON imports from ERP and vendor-catalogue feeds (manual *Sync now* and recurring).
- Missing-product de-activation on recurring feed sync.
- Async exports of customer / order / product / subscriber lists to CSV / XLSX / PDF.
- Subscription-statement PDF generation.
- Image processing: remote-URL image fetch, auto-generated variant images, dominant-colour detection, text-overlay placeholder generation.

Not covered:

- The search index sync that follows every import row — see [[background-queue-search-sync]].
- Recurring platform jobs (cart cleanup, billing, SSL) — see [[background-queue-recurring-platform]].
- Order-driven async (discount counters, webhooks, campaign send) — see [[background-queue-order-side-effects]].
- Per-import field mapping and column rules — see each import feature page (e.g. [[apps-csv-import]], [[apps-xml-sync]]).

## Contrasts

- **CSV import vs ERP feed sync.** CSV import is a single one-off upload the merchant initiates manually. ERP feed sync (XML / JSON) is a connector configured once that runs on a recurring schedule — typically every few minutes for high-volume integrations (see [[apps-microbg]] every 3 min) — or whenever the merchant clicks **Sync now**.
- **Visible vs hidden on-demand.** Imports and ERP syncs are visible on Queue View because the merchant needs progress feedback for large files. Exports, image fetches, and overlay generation run silently because they complete in seconds and surface their result directly (downloaded file, image on product page).
- **Recurring ERP sync vs missing-product de-activation.** When a recurring feed no longer includes a product that was previously synced, the platform fires a separate "disable missing products" job after the main sync completes. The merchant configures this behaviour per feed.

## Where it applies

### Imports

The merchant uploads a CSV on the corresponding screen (or the ERP connector posts a feed); the platform processes the file in the background.

| What happens | When | Visible on Queue View |
|---|---|---|
| CSV import of products | Merchant uploads file on [[products]] → Import | Yes |
| CSV import of customers | Merchant uploads file on [[customers]] → Import | Yes |
| CSV import of subscribers | Merchant uploads file on [[marketing-subscribers]] → Import | Yes |
| CSV import of blog articles | Merchant uploads file on [[marketing-blog-articles]] → Import | Yes |
| CSV import of URL redirects | Merchant uploads file on [[marketing-seo-301-redirects]] → Import | Yes |
| XML / JSON import (ERP, vendor catalog feed) | ERP integration triggers it on a recurring schedule, OR merchant clicks **Sync now** | Yes |
| Disable products missing from a recurring XML / JSON feed | Recurring ERP / XML sync detects deletion | No |

Per-import field-mapping, error reporting, and the row-level outcome are surfaced on [[settings-import-history]] — the drill-down that lets the merchant audit which rows failed and why. Imports do **not** trigger the per-product low-stock email — bulk writes are intentionally exempt to avoid blasting the merchant with thousands of alert emails on a single feed run. See [[inventory-in-stock-badge]].

### Exports

| What happens | When | Visible on Queue View |
|---|---|---|
| Customer / order / product / subscriber export to CSV / XLSX / PDF | Merchant clicks **Export** on the relevant screen | No |
| Subscription-statement PDF generation | Merchant requests an invoice from [[subscriptions]] | No |

The merchant typically receives the exported file by email or via a download link in the admin panel. Large exports may take a few minutes for the file to arrive; the merchant can re-trigger the export if they didn't receive it.

### Image processing

| What happens | When | Visible on Queue View |
|---|---|---|
| Product image fetched from a remote URL (during ERP import or manual paste of an image URL) | At import time, or when merchant pastes a URL | No |
| Auto-generated product variant images | Merchant or import creates / updates a product variant that needs a placeholder image | No |
| Product image dominant-colour detection (used by filters and theme accents) | After image upload | No |
| Text-overlay image generated for placeholder-card displays | After product save without an image | No |

The dominant-colour detection feeds the storefront colour filter; if the merchant complains *"my colour filter shows the wrong tile"* shortly after upload, the detection job may not have run yet. Re-saving the image usually re-queues it.

**Failed on-demand processes stay failed.** Unlike recurring processes that auto-retry on the next schedule, a failed import or image fetch does not retry on its own. The merchant must re-upload the CSV / re-trigger the sync / re-save the product image. The Failed row on Queue View carries the one-line error message — see [[background-queue-view-and-stuck]].

## Related

- [[background-queue-inventory]] — hub.
- [[settings-queue-view]] — progress for visible imports.
- [[settings-import-history]] — per-import outcome drill-down.
- [[apps-csv-import]] — CSV import feature page.
- [[apps-xml-import]] / [[apps-xml-sync]] — XML / JSON feed sync.
- [[apps-microbg]] — example high-frequency ERP feed (3-min recurring).
- [[inventory-in-stock-badge]] — why bulk imports bypass low-stock email.
- [[background-queue-search-sync]] — search-index sync that follows every import row.
- [[background-queue-process-catalogue]] — internal-identifier mapping.

## Open Questions

None.
