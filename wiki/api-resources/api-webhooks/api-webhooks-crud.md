---
type: api-resource
resource_path: /api/v2/webhooks
http_methods: [GET, POST, PATCH, DELETE]
related_entity: webhook
related_features: [settings-hooks, settings-api-keys]
aliases: ["Webhooks API CRUD", "Webhooks API attributes", "Webhook create/update/delete", "Webhook request_headers replace", "Webhook api_key_id read-only"]
tags: [api, json-api-v2, infra, webhooks, crud]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

> Part of [[api-webhooks]]. See the hub for the other aspects (event catalog, delivery contract, examples).

# Webhooks API — CRUD surface (JSON-API v2)

## Purpose

The REST surface for managing webhook subscriptions: the HTTP method table, the complete writable / read-only attribute reference, the (non-)relationship to the API key, and the on-write side effects. This is the aspect to read for *"what fields can I send, what's required, what's read-only, what gets clobbered on save."* The accepted `event` values live in [[api-webhooks-event-catalog]]; what happens after a webhook is saved (retries, auto-disable) lives in [[api-webhooks-delivery-contract]].

## Endpoint

- **URL base:** `<store-host>/api/v2/webhooks`
- **HTTP methods:** GET (collection + single), POST, PATCH, DELETE — **full CRUD**
- **Read-only?** No
- **Custom routes:** none
- **App requirements:** none — every CloudCart store with at least one API key can subscribe webhooks.

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v2/webhooks` | List webhooks. Supports sort / page. |
| GET | `/api/v2/webhooks/{id}` | Fetch one webhook by ID. |
| POST | `/api/v2/webhooks` | Create a webhook. Requires `url` + `event`. Optional `api_key_id` (auto-filled with first API key when omitted), `active`, `new_version`, `request_headers`. |
| PATCH | `/api/v2/webhooks/{id}` | Update a webhook. `sometimes` modifier on each rule means the caller can update one field at a time. |
| DELETE | `/api/v2/webhooks/{id}` | Delete a webhook. On underlying-row delete failure, returns 422 `"Not Deletable"` with the underlying exception message. |

Authentication, host resolution, common headers, status codes, and rate limits: see [[json-api-v2]].

## Attributes

| Attribute | Type | Writable on POST? | Writable on PATCH? | Required? | Notes / validation |
|---|---|---|---|---|---|
| `url` | string | yes | yes | **yes** on POST; `sometimes` on PATCH | Must be a valid URL (http(s) schemes only). Where CloudCart POSTs the event payload. **No reachability check at save time** — typos / dead domains save fine and fail on first delivery (which then auto-disables the webhook — see [[api-webhooks-delivery-contract]]). |
| `event` | string | yes | yes | **yes** on POST; `sometimes` on PATCH | Must be one of the **20 supported events** — see [[api-webhooks-event-catalog]]. One webhook = one event. To subscribe to multiple events, POST multiple webhook rows. |
| `active` | enum / integer (`yes` / `no` / `1` / `0`) | yes | yes | no | Subscription on/off. Defaults to active on create. The platform auto-flips this to `0` on permanent-failure deliveries (see [[api-webhooks-delivery-contract]]). |
| `new_version` | integer (`0` / `1`) | yes | yes | no | Selects the v2 vs legacy payload shape — applies (in current behaviour) to `order.created` and `order.updated`. The column is set on every webhook (even non-order events). To pin a webhook to the legacy v1 shape, explicitly send `new_version: 0` on create. |
| `request_headers` | object | yes | yes | no | Key-value map. Empty keys / values are filtered out. Custom HTTP headers added to every delivery alongside the auto-added `X-CloudCart-ApiKey`. Use for HMAC signatures, Bearer tokens, content-routing hints. **On every save (POST AND PATCH), headers are FULLY REPLACED** — all existing header rows for the webhook are deleted and fresh ones created from the request payload. To preserve existing headers, the caller must re-send them; omitted headers are dropped. |
| `api_key_id` | integer | yes (on POST only) | **no — read-only on PATCH** | no | Listed in `readOnlyAttributes`. Defaults to the first API key on the site when omitted on create. **To change the linked API key after create, DELETE + POST** — PATCH cannot rebind. **Hidden** in the schema serialiser (the relationship is implicit, not surfaced as a JSON:API relationship). |
| `created_at` / `updated_at` | datetime | no | no | n/a | Read-only timestamps. |
| `id` | integer | n/a | n/a | n/a | **Hidden** in the schema's `$hidden` array; JSON:API resource `id` still carries it. |

**Read-only attributes** (cannot be set on PATCH): `api_key_id`, `created_at`, `updated_at`, `id`.

The schema appends the `request_headers` accessor — GET responses include it as the resolved map of `key => value` pairs from the related header rows.

## Relationships

None exposed via this endpoint. The underlying webhook row references an [[api-key|API Key]] (foreign key `api_key_id`), but the relationship is **not surfaced as a JSON-API relationship**. The API key is referenced implicitly — its key value is auto-forwarded as the `X-CloudCart-ApiKey` header on every delivery (see [[api-webhooks-delivery-contract]]). There are no `$allowedIncludePaths`, so `?include=` returns nothing.

## Filtering & sorting

**Allowed filtering parameters:**

- **None declared explicitly** — `$allowedFilteringParameters = []`.
- **However**, the framework auto-merges every column on the `hooks` table into the allowed-filters list. Practical examples: `filter[event]`, `filter[active]`, `filter[url]`, `filter[api_key_id]`. Value-equality only.

**Allowed sort parameters:** `id`, `url`, `event` (prefix with `-` for descending).

**Allowed include paths:** none (no `$relationships` declared, no `$allowedIncludePaths`).

## Side effects

On a successful write, webhook CRUD here behaves **identically to the admin-panel form** on [[settings-hooks]]:

- **Auto-fill `api_key_id` on create** — when the caller omits `api_key_id`, it is set to the **first** API key on the site. For multi-key stores this may not be the intended key — integrators should explicitly POST the desired API key ID.
- **`api_key_id` is read-only on PATCH** — listed in `readOnlyAttributes`. To rebind a webhook to a different API key, DELETE + POST.
- **Header rows are persisted as separate rows AND fully replaced on every save** — each entry in the `request_headers` map becomes one row in the underlying header table. On every POST and PATCH, **all existing header rows are deleted** and fresh ones created from the request payload. Empty-key OR empty-value pairs are filtered out (not saved). **Implication:** PATCHing one header in isolation removes all the others — always re-send the full headers map on update.
- **No reachability check at save time** — a webhook to a typo'd domain saves successfully. The failure surfaces only on the FIRST delivery attempt, which then triggers the auto-disable rules in [[api-webhooks-delivery-contract]].
- **Delete may return 422** — if the model layer rejects deletion, the API returns HTTP 422 `"Not Deletable"` with the underlying domain message.

The full runtime delivery contract (retry schedule, auto-disable codes, auto-delete, queueing) kicks in only on actual event fires — see [[api-webhooks-delivery-contract]].

## Equivalent UI

- [[settings-hooks]] — the admin-panel CRUD page; same row shape, same validation, same full-replace header behaviour.
- [[settings-api-keys]] — API keys page; deleting a key referenced by a webhook is blocked.

## Related

- [[api-webhooks]] — hub.
- [[json-api-v2]] — API hub (auth, pagination, status codes).
- [[webhook]] — full entity reference with lifecycle states.
- [[settings-hooks]] — admin-panel management surface.
- [[settings-api-keys]] — API keys; the implicit `api_key_id` reference.
- [[api-key]] — API key entity.

## Open questions

- **Webhook firing from JSON-API v2 writes** — whether REST API writes fire `product.*` / `customer.*` / `category.*` webhooks is still unconfirmed; order events are well-established as firing on every save. (verify)
- **`new_version` default** — defaults to `1` even when omitted; for non-order events it is ignored at delivery today, but a future v2-shape extension could auto-opt-in existing webhooks. Pin to v1 by sending `new_version: 0` at create.
