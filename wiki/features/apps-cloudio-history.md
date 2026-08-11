---
type: feature
nav_path: "Apps → Cloudio → History"
route_name: apps.cloudio.history
route_path: /admin/apps/cloudio/:type
aliases: ["Cloudio History", "Cloudio job log", "AI job history"]
tags: [apps, ai, cloudio, history, log]
plan_gates: ["cloudio_ai"]
created: 2026-05-22
updated: 2026-05-28
source_count: 3
---
# Cloudio → History

## Purpose

The **Cloudio History** view shows the merchant a per-skill log of past AI runs — what was generated, when, with how many tokens consumed, and what rating the merchant gave. Used to audit token spending, find previously-generated content, and identify which skills produce the highest-quality output (via accumulated ratings).

For the engine + skills overview, see [[apps-cloudio-overview]].

## Where to find it

Sidebar → Apps → Cloudio → **History tab**.

Per-skill log endpoints:
- `GET /api/cloudio/shopper-pen/log` — Shopper Pen log.
- `GET /api/cloudio/shopper-sense/log` — Shopper Sense log.
- `GET /api/cloudio/rank-master/log` — Rank Master log.
- `GET /api/cloudio/vision-sense/log` — Vision Sense log.
- Per-product Shopper Pen history: `GET /api/cloudio/shopper-pen/history/{type}/{productId}`.

Each skill writes to its own `log` identifier (per the skill catalogue — `shopper_pen`, `system_shopper_sense`, `rank_master`, `vision_sense`, etc.).

## What the merchant can do here

- Filter the log by skill type.
- Filter by date range.
- See per-entry data:
  - Skill name + icon.
  - Timestamp.
  - Input that triggered the job (product ID, prompt, etc.).
  - Token cost (`cc_tokens` + `original_tokens`).
  - Output text / generated content.
  - Status (Success / Failed / Cancelled).
  - Merchant's rating (1-5 stars).
- Rate any entry retroactively (`GET /api/cloudio/rating/{log_id}/{rating}`).
- Re-run a failed job (POST `/api/cloudio/restart`).
- Publish a generated output (e.g., set a product description) — POST `/api/cloudio/shopper-pen/publish`.

### What the merchant CANNOT do here
- Delete individual log entries (logs are immutable for audit / billing reconciliation).
- Refund tokens for past failed runs (failed runs already consumed tokens; if you re-run, that costs more).
- Modify the generated output inline — the merchant must edit the entity (product / category) and use the result.

## Settings & fields

### Log entry columns

| Column | Source |
|---|---|
| **Skill** | Skill key (`shopper_pen`, `vision_sense`, etc.). |
| **Date** | Job creation timestamp. |
| **Target** | The entity (product, category) the skill was run against. |
| **Status** | Pending / Active / Success / Failed / Cancelled. |
| **CC tokens** | CloudCart-billed tokens consumed. |
| **Original tokens** | Upstream AI provider tokens (GPT). |
| **Output** | Truncated preview of the generated content (click to expand). |
| **Rating** | Star rating the merchant gave. |
| **Actions** | Restart, Rate, Publish (where applicable). |

### Per-skill history vs system-wide log

Some skills have BOTH:
- A per-skill log (`shopper_pen` log) — all merchant-invoked runs.
- A system log (`shopper_pen_system`, `system_shopper_sense`) — platform-initiated runs (background tasks, automatic suggestions).

This separation exposes both merchant-direct calls AND platform-managed automations.

## Business rules

### Logs are append-only

Job logs cannot be deleted. They serve as audit trail for:
- Token billing reconciliation.
- Quality improvement feedback (via ratings).
- Compliance (if a merchant disputes a charge or output).

### Rating feedback loop

When the merchant rates an output, the rating contributes to the platform's quality metrics. Low ratings may trigger:
- Prompt re-tuning by the platform team.
- Model adjustments (which upstream model is used for which skill).
- The merchant seeing fewer of that skill's outputs in catalog suggestions.

### Failed jobs still log

Failed jobs are written to the log with status = Failed. The merchant sees the error message + can choose to retry (POST `/api/cloudio/restart`). Retries follow the platform's `attempts = 5` retry policy.

### Permission

Standard apps permission scope.

## Related

- [[apps-cloudio-overview]] — engine + skill catalogue.
- [[apps-cloudio-settings]] — skill activation.
- [[apps-cloudio-details]] — per-skill detail.

## How it works (verified against backend)

### Two-store audit trail — content + billing joined

Each run writes to two storage layers, and the History tab joins them:
- A per-skill log entry — input, output text, status (`progress`), `tokens`, `site_id`, plus a `wait_event` marker — holds the textual history.
- A per-call accounting row — `cc_tokens` / `cc_price` / `original_tokens` / `original_price` — holds the billing reconciliation. This is owned by [[apps-cloudio-tokens-billing]].

Log entries are **append-only**; **failed jobs still write a log** (`progress` = failed) so the merchant can see what went wrong. If the content store is unavailable, the merchant can still see token-consumption rows but not the generated content; if the billing store is unavailable, they see content but not the cost breakdown.

### Logs are STORE-scoped, not per-admin

The History query filters by `site_id` (the current store). **All admins of the same store see the SAME history** — there is no per-admin filter. When multiple team members use Cloudio, everyone sees every run regardless of who triggered it. Good for collaborative review, but no individual privacy.

### No retention pruning — logs persist indefinitely

There is no automated cleanup that removes old log entries; logs survive for the lifetime of the store. The only deletions happen via `POST /api/cloudio/cancel` (removes the in-flight entry for the cancelled run only), `POST /api/cloudio/restart` (replaces a failed entry on retry), and Shopper-Pen-Advanced cancel/restart (deletes specific job-related logs). There is no "Delete old logs" button and no scheduled-retention config — History grows unbounded.

### Search is limited to product/item name; no full-text search across output

The merchant can filter by `query`, a substring match on the related item's `name` (e.g., the product's name). There is NO full-text index on the generated `response` field — the merchant cannot search for "all generations that mention 'wireless'". They can only filter by the entity the skill was run against, status (success/failed), and date.

### No log export endpoint

There is no `/api/cloudio/export` or CSV-export action — the merchant cannot download the token-consumption log as a spreadsheet for accounting. They can read the per-call accounting data inline in the History tab, but cannot bulk-export it.

### No bulk rating / bulk publish in the History list

Rating is per-entry (`GET /api/cloudio/rating/{log_id}/{rating}`) and publish is per-entry (`POST /api/cloudio/shopper-pen/publish` takes one `log_id`). There is no multi-select bulk action — the merchant rates and publishes one entry at a time. (Shopper Pen Advanced has its own bulk-create flow at `POST /api/cloudio/shopper-pen-advanced/create` for queuing many generations, but that's forward creation, not a bulk action on existing history.)

### The pending list surfaces token-waiting jobs

A job that fails for insufficient tokens is flagged with `wait_event = 'tokens'`; successful completions clear `wait_event` to null. So the History tab's pending list reliably surfaces the runs the merchant should attend to. These token-starved jobs **auto-retry once tokens return** — the merchant need not re-click Restart for each; see [[apps-cloudio-execution-model]] for the retry policy and the rebuild mechanism.

### Sub-logs — one click can produce several linked rows

Some Shopper Pen runs spawn child runs that each get their own log entry, linked to the parent via `system_id`, so the merchant sees more than one History row for a single click:
- Shopper Pen **with an image** adds a Vision Sense image-analysis row.
- Shopper Pen with `seo.enable = 1` adds a Rank Master row.

Each sub-log carries its own token cost (the parent's cost is the remainder). For the per-image and SEO cost figures and the upstream services involved, see [[apps-cloudio-upstream-providers]].

## Open questions

