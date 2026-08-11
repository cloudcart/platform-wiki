---
type: feature
nav_path: "Apps → Cloudio → Upstream providers"
route_name: apps.cloudio.overview
route_path: /admin/apps/cloudio
aliases: ["Cloudio upstream", "Cloudio AI provider", "Cloudio OpenAI", "Cloudio GPT model", "Cloudio Astica", "Cloudio RankMath", "Cloudio provider lock-in"]
tags: [apps, ai, cloudio, integrations, plan-gated]
plan_gates: ["cloudio_ai"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[apps-cloudio-overview]]. See the hub for the other aspects (skills, tokens/billing, execution model, translator).

# Cloudio — upstream AI providers

## Purpose

Cloudio is a front-end over several external AI services. This page documents which upstream service powers each skill, the mini-vs-full GPT model split, the provider lock-in, and the timeout behaviour that affects how failures present.

## Where to find it

The merchant never picks a provider — there is no provider/model selector in the Cloudio UI. This page documents platform-managed behaviour behind `/admin/apps/cloudio`; it explains why a Cloudio run might be slow, expensive, or show a particular upstream error.

## What the merchant can do here

- Nothing configurable — model and provider selection are entirely platform-managed.
- Understand (for support) which vendor a given skill calls and why a skill's cost or error message looks the way it does.

## Settings & fields

### Default OpenAI request parameters

For GPT skills the default request parameters are `temperature = 0.3`, `max_tokens = 250`, `type = 'text'`. The merchant **cannot override** these — they're platform-managed.

### OpenAI HTTP client timeout

The OpenAI HTTP client is configured with `connect_timeout = 10` seconds (the TCP/TLS handshake limit) but **no total request timeout** (the `timeout` line is commented out / disabled). A slow OpenAI response can therefore hang the job worker until the queue worker's own job-timeout fires — so a Cloudio job may appear stuck in "in_progress" during a very slow upstream response. See [[apps-cloudio-execution-model]].

## Business rules

### Mini vs Full model assignment per skill

- **`gpt-5-mini` (MINI_MODEL)** — `shopper_pen` (product description), `shopper_pen_advanced`, `shopper_pen_category`, product short description, product meta description (with `json_object` response format), text analysis, and translate-info.
- **`gpt-5.1` (FULL_MODEL)** — category description generation (multi-pass; 8+ FULL_MODEL calls in sequence). Category description is the most token-expensive skill because it runs the full model through several internal stages.
- **`gpt-4-vision-preview`** — image-aware extensions to Shopper Pen (legacy model, pre-dates the GPT-5 transition).

### Vision Sense uses TWO upstream services (Astica AI + OpenAI Vision)

The image-analysis path calls TWO services:

- **Astica AI** (`vision.astica.ai/describe`) — model `2.1_full`, returns descriptive text + read text. This is the primary Vision Sense skill.
- **OpenAI `gpt-4-vision-preview`** — used by the Shopper Pen flow when image-aware product description generation is enabled (`max_tokens = 2000`).

Token cost: each Astica image = **1500 cc_tokens** logged (matches the catalogue `multiply: 1500`). For Shopper Pen with an image: 500 cc_tokens per image (subtracted from the overall description cost). See [[apps-cloudio-skills-catalogue]].

**No merchant-side image limits in CloudCart code.** The platform sends the product's image URL(s) directly to the vision endpoint without validating size, format, or count first — those constraints are whatever the upstream API imposes (currently for OpenAI vision: PNG/JPEG/WebP/non-animated-GIF, max 20 MB per image, max ~768×2000 px for high-detail mode). Processing more images costs proportionally more.

### Rank Master uses THREE upstream services (not just OpenAI)

Rank Master calls THREE different upstream APIs depending on the sub-output:

- **RankMath API** (`api.rankmath.com/ltkw/v1/`) — keyword research. Cost: 50 cc_tokens per call.
- **OpenAI GPT-5.1** — description generation. Cost: 400 cc_tokens.
- **Internal logic** — the "addition" output. Cost: 100 cc_tokens.

So the merchant's keyword research **bypasses OpenAI entirely**; outbound traffic from the platform splits across vendors per skill type.

### Provider lock-in — OpenAI only (no Claude / Gemini option)

Every Cloudio skill except Vision Sense runs on the GPT-5 / GPT-5-mini model on OpenAI; Vision Sense uses `gpt-4-vision-preview` (also OpenAI) plus Astica. There is **no abstraction layer** for switching to Anthropic Claude, Google Gemini, or any other provider — the API URL, request format, and auth header are hard-coded for OpenAI. **The merchant cannot pick a model or provider** — it's whatever CloudCart's platform team has wired into the codebase at the time.

### Connection failure returns status-false, not a thrown exception

When OpenAI is unreachable / returns 5xx / the API key is wrong, the request helper catches the exception and returns a status-false result carrying the upstream message + code. The job then marks its log as an error with that message — and the **raw upstream error text is shown to the merchant** (no friendly fallback). See [[apps-cloudio-execution-model]] for how this surfaces in History.

### Side effects

- Outbound calls to OpenAI, Astica, and/or RankMath per skill run.
- `original_tokens` accounting tracks the upstream spend at the hardcoded GPT rate — see [[apps-cloudio-tokens-billing]].

### Permission

Standard apps permission scope.

## Related

- [[apps-cloudio-overview]] — hub.
- [[apps-cloudio-skills-catalogue]] — which skill maps to which provider + cost.
- [[apps-cloudio-execution-model]] — how upstream failures + timeouts present to the merchant.
- [[apps-cloudio-tokens-billing]] — `original_tokens` / GPT-side cost accounting.

## Open questions

None.
