---
type: feature
nav_path: "Apps → Cloudio → Execution model"
route_name: apps.cloudio.overview
route_path: /admin/apps/cloudio
aliases: ["Cloudio execution", "Cloudio jobs", "Cloudio retry policy", "Cloudio cancel", "Cloudio rebuild jobs", "Cloudio job lifecycle"]
tags: [apps, ai, cloudio, jobs, plan-gated]
plan_gates: ["cloudio_ai"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[apps-cloudio-overview]]. See the hub for the other aspects (skills, tokens/billing, upstream providers, translator).

# Cloudio — execution model

## Purpose

Every Cloudio skill runs as an asynchronous background job. This page covers the run lifecycle (enqueue → run → deduct → rate), the retry policy, what cancel does to reserved tokens, the auto-retry of token-starved jobs, and how failures surface to the merchant.

## Where to find it

Sidebar → Apps → **Cloudio** (`/admin/apps/cloudio`). The merchant triggers a skill from its context (e.g., the Cloudio side panel on the product editor), then watches / manages runs in [[apps-cloudio-history]]. Management endpoints: POST `/api/cloudio/restart` (retry), POST `/api/cloudio/cancel`, GET `/api/cloudio/rating/{log_id}/{rating}`.

## What the merchant can do here

- Trigger a skill run from its context surface.
- Restart a failed job (POST `/api/cloudio/restart`).
- Cancel an in-flight job (POST `/api/cloudio/cancel`).
- Rate a completed result 1–5 stars (GET `/api/cloudio/rating/{log_id}/{rating}`).

## Settings & fields

### Skill execution lifecycle

1. Merchant triggers a skill (e.g., from the product editor's Cloudio side panel).
2. Token cost calculated from the skill `multiply` + input size — see [[apps-cloudio-tokens-billing]].
3. If sufficient `cc_tokens` available → job enqueued (background queue) for async processing; tokens **reserved**.
4. If insufficient tokens → the request is rejected immediately with a tokens-unavailable error.
5. Job runs (calls the upstream AI service, parses the response — see [[apps-cloudio-upstream-providers]]).
6. Result written to the log + returned to the merchant via polling or webhook.
7. Tokens deducted on completion.
8. Merchant can rate the result (1–5 stars).

### Job types

The platform's background jobs implement specific skills:

- Product description (short + long), short-description-only, and product meta description generators.
- Category description generation (single-pass and a multi-pass "complete" variant).
- Text analysis (classification / sentiment).
- Translation jobs (auto-translate, collect, info) — see [[apps-cloudio-translator]].
- Bulk / advanced Shopper Pen content generation.
- A rebuild job that re-processes previously-failed jobs.

## Business rules

### Retry policy — 5 attempts

Each Cloudio job retries up to **5 times** (`attempts = 5`) on **transient** failures. **Permanent** failures (e.g., bad prompt structure, a provider policy block) fail immediately without consuming retry attempts. Retries skip token deduction until success.

### Cancel releases reserved tokens

Cloudio jobs reserve tokens when enqueued and deduct on success. When the merchant cancels via POST `/api/cloudio/cancel`, the job is destroyed before completion — the **reserved tokens are released back to the balance** (no deduction is logged for cancelled jobs). See [[apps-cloudio-tokens-billing]].

### Token-starved jobs auto-retry once tokens return

When a job fails specifically because of insufficient tokens, it is marked with a tokens wait-event. When the merchant tops up (via plan renewal or pack purchase), the platform queues a one-shot **rebuild** job that scans for those token-starved logs and re-queues them with their original settings. So failed-due-to-no-tokens jobs **auto-retry once tokens are available** — the merchant doesn't have to manually re-trigger each.

### Failures surface the raw upstream message

When the upstream service is unreachable / returns 5xx / the API key is wrong, the request handler **catches the exception and returns a status-false result with the upstream message** rather than throwing. The Cloudio job then marks the log as an error with that underlying message.

**The merchant SEES the raw upstream error text in their UI** for these failures — e.g., OpenAI errors like `rate_limit_exceeded`, `context_length_exceeded`, or `invalid_request_error` appear as English-language technical messages. There is **no** localised "AI service temporarily unavailable, try again" wrapper. See [[apps-cloudio-upstream-providers]] for the timeout behaviour that can leave a job appearing stuck.

### Job ratings improve quality

The merchant rates each output (GET `/api/cloudio/rating/{log_id}/{rating}`). Low ratings feed back into the platform's prompt tuning, improving subsequent quality. Ratings are advisory feedback only — they don't refund tokens.

### Side effects

- Token balance decremented per **successful** job; released on cancel.
- A per-skill log entry + per-call accounting row created — surfaced in [[apps-cloudio-history]].
- Job result written to the relevant entity (product description updated, category description set, etc.).
- No webhooks fire automatically per Cloudio job (verify).

### Permission

Standard apps permission scope.

## Related

- [[apps-cloudio-overview]] — hub.
- [[apps-cloudio-tokens-billing]] — reservation, deduction, and the tokens-unavailable rejection.
- [[apps-cloudio-upstream-providers]] — the upstream call inside step 5 + timeout behaviour.
- [[apps-cloudio-skills-catalogue]] — the active-skill gate that precedes execution.
- [[apps-cloudio-history]] — where runs, ratings, and errors are listed.

## Open questions

None.
