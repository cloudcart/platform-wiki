---
type: api-resource
resource_path: /api/v2/subscribers
http_methods: [GET, POST, PATCH, DELETE]
related_entity: subscriber
related_features: [marketing-subscribers, marketing-channels]
aliases: ["Subscribers API attributes", "Subscribers API CRUD", "Subscriber attribute reference", "Subscribers POST PATCH DELETE"]
tags: [api, json-api-v2, marketing]
plan_gates: ["subscribers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[api-subscribers]]. See the hub for the other aspects (querying / filtering, write side-effects).

# Subscribers API — attributes, relationships & CRUD

## Purpose

The attribute reference + write-path mechanics for the [[subscriber|Subscribers]] JSON-API v2 resource: which fields exist, which are writable on POST vs PATCH, which are read-only, the two relationships (`channels`, `tags`), and the concrete POST / PATCH / DELETE request + response shapes. For read-side query parameters (filter / sort / include) see [[api-subscribers-list-querying]]; for what happens *after* a write (webhooks, cascade, plan cap) see [[api-subscribers-list-effects]].

## Endpoint

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/v2/subscribers` | Create a subscriber. The adapter force-sets `subscribed_from = "API"` when omitted. |
| PATCH | `/api/v2/subscribers/{id}` | Update a subscriber. |
| DELETE | `/api/v2/subscribers/{id}` | Delete a subscriber (cascades — see [[api-subscribers-list-effects]]). Returns **204 No Content**. |
| GET / POST / PATCH / DELETE | `/api/v2/subscribers/{id}/relationships/<rel>` | Manage the `channels` and `tags` relationships in linkage-only form. |

All requests use `Accept: application/vnd.api+json`; body-carrying requests add `Content-Type: application/vnd.api+json`. Authenticate via `X-API-KEY` (see [[settings-api-keys]]).

## Attributes

| Attribute | Type | Writable on POST? | Writable on PATCH? | Required? | Notes / validation |
|---|---|---|---|---|---|
| `country` | string (ISO-2) | yes | yes | **required on POST** | The validator enforces `required` on create — the field has no `email`-style format rule, but ISO-2 codes are the platform convention. Used in segment-rule filtering. Auto-detected via MaxMind on storefront signups; the API requires the caller to send it explicitly. |
| `first_name` | string | yes | yes | optional | Identity name. Falls back to the default channel identifier on display when empty. |
| `last_name` | string | yes | yes | optional | Identity name. |
| `customer_id` | integer | yes | yes | optional | Optional link to a [[customer\|Customer]] row (one-way pointer; deleting the Customer flips `deleted_customer` on the Subscriber but the Subscriber survives). |
| `subscribed_from` | string | yes | yes | optional | Audience-source bucket. If empty on POST, the adapter forces `"API"`. Other documented values include `customer_login`, `subscribe_form`, `import`, `customer_creating`, `order_creating`, `messenger`, `contacts_form`, `system`, `subscribe_from_missing_product`, `web_push`. See [[subscriber\|Subscriber entity]]. |
| `password` | string | yes | yes | optional | Subscriber's password hash (rarely used by integrations; subscribers are not typically authenticated themselves). Hidden from API responses. |
| `remember_token` | string | yes | yes | optional | Auth-related token. Hidden from API responses. |
| `deleted_customer` | integer | **read-only** | **read-only** | — | Auto-flipped when the linked Customer is deleted; the Subscriber row survives. Rejected on POST/PATCH with `"field is read only"`. |
| `total_sent` | integer | **read-only** | **read-only** | — | Cumulative message-sent count. Maintained by the campaign-send pipeline. |
| `opened_url` | integer | **read-only** | **read-only** | — | Cumulative link-open count. |
| `seen_message` | integer | **read-only** | **read-only** | — | Cumulative impressions. |
| `successfully_sent` | integer | **read-only** | **read-only** | — | Cumulative successful-delivery count. |
| `open_rate` | integer | **read-only** | **read-only** | — | Computed open-rate metric. |
| `click_rate` | integer | **read-only** | **read-only** | — | Computed click-rate metric. |
| `last_active_at` | datetime | **read-only** | **read-only** | — | Updated on every storefront interaction (the subscribe-form, campaign-link clicks, etc.). The model auto-touches it on update from the site app. |
| `form_id` | string | **read-only** | **read-only** | — | When the subscriber was created via `subscribed_from = subscribe_form`, references the [[marketing-subscribers-subscribe-forms\|subscribe form]] ID. `null` for API-created subscribers. |
| `last_order_id` | integer | **read-only** | **read-only** | — | Denormalised pointer to the subscriber's most recent order (when linked to a Customer who has ordered). |
| `created_at` / `updated_at` | datetime | — | — | — | Standard timestamps. |

**Not present on the Subscriber row itself:** `marketing` consent and `verified` / `bounced` deliverability flags live on the per-channel rows — see [[api-subscribers-channels]]. There is no row-level `marketing` toggle on the subscriber; opting out is done per channel.

**Hidden from API responses:** `password`, `remember_token`.

## Relationships

| Name | Cardinality | Target type | Writable? | Notes |
|---|---|---|---|---|
| `channels` | hasMany | `subscribers-channels` | writable (via relationship endpoints OR linked at create) | One row per channel the subscriber is reachable on. The API currently allows-lists **Email** and **Phone** channels only for direct CRUD via [[api-subscribers-channels]] (WebPush and Messenger rows are created internally by storefront flows, not by the API). |
| `tags` | hasMany | `subscribers-tags` | writable (via relationship endpoints) | Subscriber-side tags. Separate taxonomy from [[api-customer-tags\|customer tags]] — see [[api-subscribers-tags]]. |

The route registration declares `tags` as a hasMany relationship on this resource even though the adapter uses a `belongsTo` helper internally — the functional model is one Subscriber → many Tag pivot rows.

## Filtering & sorting

Query parameters (filter / sort / include) are documented on the read-side aspect — see [[api-subscribers-list-querying]]. In brief: `filter[segment]` is a custom join filter, all `subscribers` columns are equality-only filters, sort is limited to `id` / `first_name` / `last_name` / `country`, and includes are `channels` / `tags`.

## Side effects

Every write fires webhooks, applies the silent plan cap, and triggers segment re-evaluation; DELETE cascades broadly. The full catalogue (including the no-audit-log gap) is on [[api-subscribers-list-effects]]. The two write-path facts you need while reading the examples below:

- **POST force-sets `subscribed_from = "API"`** when the attribute is omitted.
- **DELETE returns 204** and removes the subscriber plus all of its channel rows, tag pivot rows, and segment memberships.

## Equivalent UI

- [[marketing-subscribers]] — the admin subscriber list; the merchant edits the same identity fields here that this resource writes.
- [[subscriber|Subscriber entity]] — full attribute reference for the underlying row.

## Example requests & responses

### POST subscriber with linked channels

`country` is the only required attribute. `subscribed_from` is force-set to `"API"` when omitted. The `channels` payload below uses JSON-API's relationship-payload form to atomically create two channel rows alongside the subscriber.

```bash
curl -sS -X POST \
  "https://<store-host>/api/v2/subscribers" \
  -H "Accept: application/vnd.api+json" \
  -H "Content-Type: application/vnd.api+json" \
  -H "X-API-KEY: <YOUR_API_KEY>" \
  -d '{
    "data": {
      "type": "subscribers",
      "attributes": {
        "country": "BG",
        "first_name": "Иван",
        "last_name": "Петров"
      }
    },
    "included": [
      {
        "type": "subscribers-channels",
        "attributes": {
          "channel": "Email",
          "channel_identifier": "ivan.petrov@example.com",
          "marketing": 1,
          "verified": 0,
          "bounced": 0
        }
      },
      {
        "type": "subscribers-channels",
        "attributes": {
          "channel": "Phone",
          "channel_identifier": "+359871234567",
          "marketing": 1,
          "verified": 0,
          "bounced": 0
        }
      }
    ]
  }'
```

If the relationship-payload form is rejected by your integration's JSON-API client, POST the subscriber first, then create each channel row via [[api-subscribers-channels]] using the returned subscriber id.

### POST 201 Created — `subscribed_from` auto-set to `"API"`

```
HTTP/1.1 201 Created
Location: https://<store-host>/api/v2/subscribers/12345
Content-Type: application/vnd.api+json
```

```json
{
  "data": {
    "type": "subscribers",
    "id": "12345",
    "attributes": {
      "country": "BG",
      "first_name": "Ivan",
      "last_name": "Petrov",
      "subscribed_from": "API",
      "created_at": "2026-06-05T09:12:44+00:00",
      "updated_at": "2026-06-05T09:12:44+00:00"
    }
  }
}
```

### PATCH (update name)

```bash
curl -sS -X PATCH \
  "https://<store-host>/api/v2/subscribers/12345" \
  -H "Accept: application/vnd.api+json" \
  -H "Content-Type: application/vnd.api+json" \
  -H "X-API-KEY: <YOUR_API_KEY>" \
  -d '{
    "data": {
      "type": "subscribers",
      "id": "12345",
      "attributes": {
        "first_name": "Ivan"
      }
    }
  }'
```

### DELETE

```bash
curl -sS -i -X DELETE \
  "https://<store-host>/api/v2/subscribers/12345" \
  -H "Accept: application/vnd.api+json" \
  -H "X-API-KEY: <YOUR_API_KEY>"
```

DELETE cascades — see [[api-subscribers-list-effects]]. Returns **204 No Content** on success.

### 422 — missing required `country`

```json
{
  "errors": [
    {
      "status": "422",
      "title": "Unprocessable Entity",
      "detail": "The country field is required",
      "source": { "pointer": "/data/attributes/country" }
    }
  ]
}
```

### 422 — read-only attribute on POST/PATCH

Sending `total_sent`, `open_rate`, `click_rate`, `deleted_customer`, etc. → `"The <field> field is read only"`. The validator errors on the FIRST read-only field it encounters.

## Related

- [[api-subscribers]] — hub.
- [[api-subscribers-list-querying]] — read-side filter / sort / include parameters + GET examples.
- [[api-subscribers-list-effects]] — write side-effects, plan cap, DELETE cascade, testing checklist.
- [[api-subscribers-channels]] — per-channel deliverability + consent rows; the `channels` relationship target.
- [[api-subscribers-tags]] — subscriber-tag pivot; the `tags` relationship target.
- [[subscriber]] — Subscriber entity; underlying attribute reference.
- [[settings-api-keys]] — authentication setup.

## Open questions

- Verify whether `marketing` / `gdpr_accepted` consent state is ever needed at the subscriber-row level for any integration use case. Today both consents are managed exclusively via channel rows ([[api-subscribers-channels]] `marketing` field) — the subscriber row itself has no consent flag.
