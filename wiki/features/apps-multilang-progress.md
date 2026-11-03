---
type: feature
nav_path: "Apps → Multilang → Progress"
route_name: apps.multilang.progress
route_path: /admin/apps/multilang/progress
aliases: ["Multilang Progress", "Multilang sync progress", "Multilang queue status"]
tags: [apps, administration, multilang, progress, sync, queue]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 3
---
# Multilang → Progress

## Purpose

The **Progress** tab is the **overall sync progress + queue status view** for the Multilang app. Shows:
- How many translation jobs are pending across all sites.
- How many are in-flight.
- How many completed today / this week / total.
- Failed jobs with error reasons.
- ETA for full sync completion.

Different from [[apps-multilang-products]] (per-product detail) — this page is the AGGREGATE view of the translation pipeline.

For the full Multilang feature set, see [[apps-multilang]].

## Where to find it

Sidebar → Apps → Multilang → **Progress tab**. Route: `/admin/apps/multilang/progress`.

## What the merchant can do here

### Pipeline status summary

Top of page typically shows:
- **Pending jobs** count — items queued for translation/copy.
- **Active jobs** count — currently processing.
- **Failed jobs** count — drill into error details.
- **Completed today** count.

### Per-sister-site breakdown

For each sister site (from [[apps-multilang-stores]]):
- Pending / active / completed / failed counts.
- Last successful sync timestamp.
- ETA to clear current queue.

### Per-queue-task breakdown

Per [[apps-multilang]], two queue tasks handle the sync:
- `multilang_product_translate` — AI translation.
- `multilang_product_copy` — copy without translation.

The Progress page can show each queue's status independently.

### Failed-job drill-down

Failed jobs show:
- Which entity (product / category / etc.) failed.
- Which sister site.
- Error message (translation API error / network timeout / validation failure).
- Retry action per job.

### Bulk actions
- **Retry all failed** — re-queue all failed jobs.
- **Clear queue** — abandon all pending jobs (use carefully).
- **Pause sync** — halt processing without clearing.

### What the merchant CANNOT do here
- Configure which entities sync — that's [[apps-multilang-settings]].
- Manage sister sites — that's [[apps-multilang-stores]].

## Settings & fields

The Progress data is fetched async. Typical structure per the platform's job-tracking pattern:

| Field | Notes |
|---|---|
| **pending** | Count of queued jobs. |
| **active** | Count of currently-processing jobs. |
| **completed** | Count of successfully-completed jobs (per period). |
| **failed** | Count of failed jobs (with retry option). |
| **per_site_breakdown** | Map of site_id → status counts. |
| **last_completed_at** | Most recent successful job timestamp. |

## Business rules

### Real-time vs cached

The Progress page may poll for live updates OR require manual refresh — verify cadence.

### Job retention

Failed jobs are typically retained for some period (e.g., 7 days) before being purged. Within that window, the merchant can retry. After retention, failed jobs disappear from the queue.

### Cloudio token consumption visibility

Auto-translation consumes Cloudio AI tokens (per [[apps-cloudio-overview]]). The Progress page typically surfaces token-spend impact — useful for the merchant to monitor cost.

### Permission
Standard apps permission scope.

## Related

- [[apps-multilang]] — Multilang hub.
- [[apps-multilang-stores]] — sister sites.
- [[apps-multilang-products]] — per-product detail.
- [[apps-multilang-settings]] — feature toggles.
- [[apps-cloudio-overview]] — AI engine that consumes tokens during translation.
- [[settings-queue-view]] — global background queue (Multilang jobs surface here too).

## How it works (verified against backend)

### Translation cost is Google Cloud quota, not Cloudio tokens

Per [[apps-multilang]] verification: Multilang uses Google Cloud Translation API, not Cloudio. The Progress page shows the merchant's REMAINING `multilang_product_translate` symbols + `multilang_product_copy` units (NOT Cloudio `cc_tokens`). When the merchant runs out of translate-symbol quota, the sync halts until they purchase more via the plan-feature link.

### What the Progress endpoint returns

The Progress endpoint returns:

| Returned field | Meaning |
|---|---|
| `step` | Current wizard step (always 6 when sync has started). |
| `settings.progress` | Map of `progress_element → completion_count` per category (products, blog, categories, etc.). |
| `remaining` | Count of progress elements with `value == 0` (i.e., not yet complete). |
| `main_url` | The master site's URL. |
| `other_data` (only for internal CloudCart sessions) | Debug counters: total translated symbols vs. budget, total products vs. translated count. |

Standard merchants see `remaining` and `progress` but NOT `other_data` — that's gated to CloudCart's internal team session.

### No manual prioritisation — queue is FIFO

Multilang `multylang_copy` queue tasks run on the platform's standard queue infrastructure with no priority field. The merchant cannot tell the platform "translate THIS product before the others." If they need a specific product translated urgently, the only option is to halt the bulk sync (wait for it to complete or contact support for a force-stop), translate the urgent product manually, then restart.

### Unpaid-feature warning halts sync

When the merchant has an unpaid plan upgrade or unpaid copy/translate feature pack pending, the Progress endpoint returns HTTP 402 with a price-summary detail block. **The merchant must pay before Multilang sync proceeds.** The page surfaces the exact prices for plan + features needed.

### No completion-email notification

Per the codebase: there is no Multilang-specific email template fired when `remaining == 0`. The merchant must check the Progress page manually to know the sync is done.

### Auto-start on first progress query

On first call, when `started` is empty, the platform initialises `started = 1`, sets `progress` to a zero-filled map of progress elements, and queues the `multylang_copy` task. **Loading the Progress page is what kicks off the sync** the first time — it's not an automatic background trigger that starts when the merchant saves settings.

### Step-redirect on incomplete wizard

If the merchant lands on `/admin/apps/multilang/progress` while their setup is still mid-wizard (`step > 0` in settings), the endpoint returns a redirect to `/admin/apps/multilang/create/step/<step>`. The merchant has to complete the wizard's checkout step before Progress can be viewed.

### Machine-translation high-watermark flag — "almost out"

When the merchant's translated-tokens count gets within **3000 symbols** of the total purchased translation quota (`tokens >= total_translate - 3000`), the Translate job sets `progress.machine_translation = 1` on settings. This flag is what surfaces the "machine translation almost exhausted" warning on Progress — at 3k symbols remaining, the merchant is alerted to buy more before sync halts.

### Sync progresses by entity-type buckets

Per the `progress` field returned by the endpoint, sync runs in named buckets (e.g., `products`, `blog`, `pages`, `categories`, `properties`, `tags`, `images`, `vendor`, etc. — exact set determined by the master's `copy` and `copy_product` settings). The `remaining` count is the number of buckets whose value is still `0` (not yet started/completed). Each bucket reaches a non-zero value when the platform has fully processed all entities of that type.

### Console-only debug payload

When the merchant viewing the page is logged in via CloudCart's internal support console (`cc_console_login.auth_id`), the Progress response includes a `debug` block with:
- `copy`, `copy_products` — the master's per-field copy settings.
- `symbols` — actual symbols translated so far / total budget.
- `products` — total / translated.
- `console_id` — the staff member's auth ID.

Standard merchants don't see this block.

### `force_stop` cleared on first Progress hit

If the sync was previously force-stopped (by CloudCart support), the Progress endpoint REMOVES the `force_stop` setting on first call after the merchant returns to the page. This effectively auto-restarts the sync queue. The merchant cannot toggle `force_stop` themselves — only CloudCart support can set it via the restricted endpoint.

### Site-status flip when remaining hits zero

When `remaining == 0` (every bucket complete), the platform updates the corresponding sister site row's `progress_status` to `4` (completed) and pushes the sister's site name back to the master's tracking table. This is what changes the Active/Pending badge in [[apps-multilang-stores]] from in-progress to active.

## Open questions

