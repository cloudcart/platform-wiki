---
type: feature
nav_path: "Settings → Api keys → Rate limits"
route_name: api_keys.settings
route_path: /admin/settings/api_keys
aliases: ["API rate limit", "API requests per minute", "429 Too Many Requests", "X-RateLimit headers", "Лимит на API заявки"]
tags: [settings, api-keys, rate-limit, edge, json-api-v2]
plan_gates: ["api_requests"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Api keys — Rate limits

> Part of [[settings-api-keys]]. See the hub for related aspects (overview, modal, feature packs, delete protection, security).

## Purpose

What "API requests per minute" means in the rate-limit banner above the keys table, how the cap is enforced at the platform edge, and which response headers integration code should react to when it hits the limit. This is the page to read when a merchant reports `429 Too Many Requests`, when they ask "does adding another API key give me more capacity?", or when integration code needs to know which retry signals to honour.

## Where to find it

The cap is surfaced in the info banner above the table on [[settings-api-keys-overview]] (Sidebar → Settings → Api keys). The Upgrade button next to it is documented in [[settings-api-keys-feature-packs]].

## What the merchant can do here

- See the active per-minute cap on their plan in the banner.
- See the canonical API Base URL (`<store-host>/api/v2`).
- Diagnose `429` responses from integration logs against the cap shown here.
- Request a custom per-domain raise from CloudCart support (up to 800 req/min) for unusually high-volume integrations (verify).

## Settings & fields

The rate-limit value is **derived** — there is no editable field on this page. The displayed cap comes from `meta.api_requests_limit` on the page payload, which in turn reflects the `api_requests` plan-feature on the store's active plan + any active feature packs (see [[settings-api-keys-feature-packs]]).

| Banner element | Where the value comes from |
|----------------|----------------------------|
| Plan name | `meta.plan_name` (verify) |
| Requests-per-minute cap | `meta.api_requests_limit` |
| API Base URL | `<store-host>/api/v2` |

## Business rules

### Per-plan cap (authoritative source: cloudcart.com/pricing)

The API request-per-minute limit follows the store's active plan. Currently published values:

| Plan | API requests / minute |
|---|---|
| **Baby Pack** | No API access |
| **Starter Pack** | 50 |
| **CC Pro** | 100 |
| **CC Master** | 150 |

Backend default if a plan doesn't define `api_requests` explicitly: **60 req/min** (verify — used as a defensive fallback in middleware).

### Enforcement runs at the platform edge

The cap is enforced at the platform's edge layer (CDN / reverse proxy / load balancer in front of the application), NOT inside the storefront application. So:

- Any value visible in deeper application middleware is **not the authoritative limit** — it's a defensive fallback; the real cap is applied earlier in the request lifecycle.
- The Baby Pack plan does NOT include API access at all — calls are rejected before the application sees them.
- See [[platform-rate-limits]] for the full picture of every rate limit, bot policy, and timeout the platform applies.

### Bucket scope: per-domain, NOT per-key

Important: **all API keys for the same store share ONE bucket** — creating more keys does NOT raise the limit.

- Multiple stores on the same custom domain (rare — every CloudCart store has its own domain) would share the limit.
- The limit is per-store-domain (not per-IP, not per-key).

### Window: rolling 1-minute bucket

Counted as a rolling 1-minute window. On exceed, the API returns HTTP `429 Too Many Requests`.

### `429` response shape

When the limit is exceeded, the platform returns:

- HTTP status **429**.
- Headers:
  - `Retry-After: 60`
  - `X-RateLimit-Limit` — the current cap (= the value advertised in the banner).
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`
  - `X-RateLimit-Info` — carries the upgrade-pointer message.
- JSON body with an explanatory `message` field and `retry_after: 60` field.

Integration code should honour `Retry-After` (preferred) or back off based on `X-RateLimit-Reset`.

### Storefront routes are NOT covered by this cap

Only `/api/v2/*` paths use the per-domain per-plan cap. Storefront page requests fall under the platform's general abuse protection instead. So heavy storefront traffic does not exhaust API-key quota and vice versa. See [[platform-rate-limits]] for the storefront-side rules.

### Custom per-domain raises (up to 800 req/min)

The platform supports raising the cap up to **800 req/min** for a specific store on request (verify) — negotiated with CloudCart support out-of-band. The in-product Upgrade button typically goes through plan / feature-pack purchase first; see [[settings-api-keys-feature-packs]].

### Authentication still uses BOTH key value and Site ID

The rate-limit logic only kicks in for authenticated calls. Every API call must send the store's Site ID alongside the key value (header `X-CloudCart-ApiKey` — verify) against the `<store-host>/api/v2` base URL. The three pieces a developer needs: Site ID + API key + base URL.

## Related

- [[settings-api-keys]] — hub.
- [[settings-api-keys-overview]] — banner location + Upgrade button.
- [[settings-api-keys-feature-packs]] — buying extra `api_requests` capacity.
- [[settings-api-keys-security]] — Active=OFF latency vs rate-limit refusal.
- [[json-api-v2]] — auth + side-effects principle.
- [[platform-rate-limits]] — full platform-edge rate-limit reference.
- [[plan-features]] / [[plan-vs-feature-pack]] — base + pack stacking model.
- [[plan-gates]] — three plan-restriction shapes.

## Open questions

- Confirm authentication header name (`X-CloudCart-ApiKey` vs alternative) (verify).
- Confirm 800 req/min ceiling for custom raises (verify against latest platform policy).
