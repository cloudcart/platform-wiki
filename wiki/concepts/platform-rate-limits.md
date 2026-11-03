---
type: concept
aliases: ["Platform rate limits", "API rate limits", "429 responses", "Webhook receiver burst", "Storefront timeout", "API requests per minute"]
tags: [rate-limits, api, integrations, support, troubleshooting, concepts]
created: 2026-05-28
updated: 2026-08-11
source_count: 4
---
# Platform rate limits

## Definition

CloudCart enforces **request limits before a request reaches** the storefront, admin panel, or JSON API. What matters to a merchant or integrator is what their integration **sees** — so this page documents the merchant-facing limits, the HTTP responses, and the options to react.

## Scope

Covers: the **API v2 per-domain rate limit** (every 429 on `/api/v2/*`); the **webhook receiver burst**; the **storefront and API timeouts** (504); and the **HTTP responses** on each limit hit.

Out of scope: the platform's anti-abuse protections (flood, crawler and bot handling). Those exist, and a client that trips them receives a 429 or 403, but their thresholds are not published. Also out of scope: protections in front of CloudCart such as geo blocks or JS challenges — they fire *before* CloudCart sees the request, so the merchant gets that provider's branded page rather than a CloudCart response. In-application plan-feature quotas are separate — see [[plan-gates]].

## Contrasts

Three layers can return 429 / 403 / 504; distinguishing which helps decide what to do:

| | In front of CloudCart | Platform edge (this page) | Application backend |
|---|---|---|---|
| Source | That provider's page / challenge | CloudCart 429 / 403 / 504 page or JSON | Standard JSON error |
| Visible cue | Third-party branding | `X-RateLimit-*` headers | Plain JSON error |
| Typical cause | Geo block, firewall rule, bot challenge | Rate limit, timeout | Validation, plan quota |
| What to do | Contact support if false positive | Upgrade / buy a pack / fix the integration | Fix validation or upgrade |

Plan-feature quotas (e.g. *"max products on this plan"*) are NOT enforced here — they live in the application via [[plan-gates]].

## Where it applies

Every request to a CloudCart-hosted store passes the edge: storefront pages, admin panel, JSON API (`<store>/api/v2/*`), webhooks, short URLs, and image / CDN paths.

### API v2 per-domain rate limit (the canonical merchant-facing limit)

Calls to `<store>/api/v2/*` (any method) get a **per-minute budget keyed on the request's `Host` domain** (lower-cased) — advertised on [[settings-api-keys]]:

| Plan | API requests per minute |
|---|---|
| **Baby Pack** | ❌ No API access — every request fails immediately |
| **Starter Pack** | 50 |
| **CC Pro** | 100 |
| **CC Master** | 150 |
| **Custom (negotiated)** | up to 800 (the hard ceiling) |

A domain whose plan is **not found** in the limit map is treated as **0**, not "unlimited" — see *Known gotchas* below.

The base value can be raised by buying `api_requests` feature packs — see [[plan-features]] and [[plan-vs-feature-pack]]. Effective limit = plan base + active packs, **capped at 800**. **All API keys for a store share one bucket** (more keys ≠ more limit). The limit is recomputed from the plan + active packs **about every 5 minutes**, so a plan change or a new pack takes up to ~5 min to take effect. The window is a **sliding 60-second average**, not a bucket that resets at the top of each minute — so the quota **recovers gradually**, not all at once.

Every `/api/v2/*` response (allowed AND denied) carries: `X-RateLimit-Limit` (current cap — **`0` when the plan has no API access, or the domain isn't in the limit map**), `X-RateLimit-Remaining` (0 when blocked), `X-RateLimit-Reset`, `X-RateLimit-Info` (message + upgrade pointer), and `Retry-After: 60` on denial. Note: `X-RateLimit-Reset` is always **now + 60 s** — a constant offset, **not** the real recovery moment (a sliding window has no exact reset point).

The 429 body when the merchant has API access but exceeded the cap:

```json
{
  "error": "Too Many Requests",
  "message": "API rate limit exceeded. Please wait and retry later, or upgrade your current plan to a higher level for increased API limits.",
  "retry_after": 60
}
```

The Baby Pack variant (no API access at all) instead sends `"message": "API rate limit exceeded. You do not have API access on your current plan. Please upgrade your subscription plan to enable API access."`. The merchant should quote these messages to support — they identify the exact denial type. A `limit: 0` denial fires on the **very first request**, no matter the traffic — and it reads **identically** whether the plan has no API access OR the domain simply isn't in the limit map (see *Known gotchas*).

### API v2 rate limit — known gotchas

- **🔴 Only the store's PRIMARY domain carries the limit.** The limit map holds **one entry per store — its primary host**. Calls to the store's service subdomain, the `www.` variant, or any **secondary / additional domain** are treated as **limit 0** and get a `429` on the **very first request** — even when the store is fully paid and has API access. **Integrators must call `/api/v2/*` on the store's primary domain.** Tell-tale: the same store answers with its real limit on the primary domain but returns the *"no API access"* 429 on the `www.` or service subdomain.
- **The quota is per DOMAIN, not per store** — currently moot because only the primary domain works, but if a store is ever mapped on several domains each would get its own independent counter.
- **Off-by-one:** effectively **`limit − 1`** requests pass per sliding window (the counter includes the current request).
- **Which 429 fired?** The per-domain API limit returns **JSON** with the `X-RateLimit-*` headers. A 429 that arrives as an **HTML** page came from a different protection layer, not from the API quota — that body difference is the fastest way to tell them apart.

### Webhook receiver burst

When the merchant configures a webhook destination on [[settings-hooks]], outbound delivery can send a high burst of requests to a single receiver during large events (catalog change, segment recalculation, bulk action firing many `order.*` events). The receiver MUST tolerate this — the platform does not throttle outbound delivery. A 5xx or timeout triggers the standard retry — see [[notification-delivery]].

### Storefront and API timeouts (504)

| Surface | Max duration before 504 |
|---|---|
| Admin panel (most endpoints) | 30 seconds |
| JSON API v2 | 30 seconds |
| Storefront page render (builder) | 600 seconds (10 min — cold-cache page generation) |
| Image processing | 40 seconds |
| WebSocket (admin notifications, builder previews) | 60 minutes idle window |
| Webhook delivery (outbound) | 30 seconds per attempt |

A 504 means the request was accepted but didn't finish in time. On the storefront it almost always means the page does too much work (large listing, no caching); on the API it usually means too much data in one call — paginate.

### Merchant-facing scenarios

| Scenario | What to do |
|---|---|
| *"ERP integration getting 429"* (API v2 cap) | Upgrade or buy an `api_requests` pack on [[settings-api-keys]] → **Upgrade**; quote `X-RateLimit-Limit`. |
| *"Baby Pack — every API call returns 429"* | Upgrade to Starter Pack+; no pack path on Baby Pack. |
| *"Paid plan but the API returns `429` / `X-RateLimit-Limit: 0` on the very first call"* | Almost always the **wrong domain** — the integration is hitting `www.` or the service subdomain instead of the store's **primary** domain (only the primary carries the limit). Point the integration at the primary domain. |
| *"My crawler gets blocked"* | The client is tripping an anti-abuse protection rather than the API quota. Identify the crawler with a proper User-Agent, pull data from the store's feeds where possible, or ask support to review it. |
| *"Webhook receiver hammered on bulk action"* | Receiver must scale itself; 5xx triggers retries — see [[notification-delivery]]. |
| *"Storefront 504 on first visit"* | Reduce per-page products, fewer listing relations, enable caching; ticket if cause unclear. |
| *"Large GET /api/v2/products timed out (504)"* | Reduce `?page[size]`, narrow `?fields[products]`, or paginate. |

## Related

- [[settings-api-keys]] — merchant surface where the API rate limit is advertised + **Upgrade** button.
- [[json-api-v2]] — JSON API v2 hub (rate-limit + auth model).
- [[plan-features]] — the `api_requests` feature that drives the per-domain cap.
- [[plan-vs-feature-pack]] — plan vs feature-pack stacking for limit extension.
- [[plan-gates]] — in-application plan-feature quotas (NOT enforced at the edge).
- [[notification-delivery]] — outbound webhook retries when the receiver fails.
- [[settings-hooks]] — where the merchant configures webhook destinations.

## Open Questions

- Whether the merchant can buy a pack raising the limit all the way to 800 req/min directly from [[settings-api-keys]] **Upgrade**, or whether values above the highest plan tier require a support-negotiated request. The 429 says 800 is the maximum, but the in-product upsell ladder may stop earlier.
