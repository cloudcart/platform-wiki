---
type: api-resource
resource_path: /api/v2/subscribers
http_methods: [POST, PATCH, DELETE]
related_entity: subscriber
related_features: [marketing-subscribers, marketing-segments]
aliases: ["Subscribers API side effects", "Subscribers API webhooks", "subscribers.max_id silent cap", "Subscriber DELETE cascade", "Subscribers API plan gating", "Subscribers API testing checklist"]
tags: [api, json-api-v2, marketing]
plan_gates: ["subscribers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[api-subscribers]]. See the hub for the other aspects (attributes / CRUD, querying / filtering).

# Subscribers API — write side-effects, plan cap & testing

## Purpose

What happens *after* a write to the [[subscriber|Subscribers]] JSON-API v2 resource: webhooks, the silent `subscribers.max_id` plan cap, segment re-evaluation, the DELETE cascade, plan-feature gating, the missing audit trail, and an end-to-end CRUD testing checklist. For the attribute set + request examples see [[api-subscribers-list-crud]]; for read-side query parameters see [[api-subscribers-list-querying]].

## Endpoint

Side effects below apply to the write methods on `/api/v2/subscribers` and `/api/v2/subscribers/{id}` (POST / PATCH / DELETE) and to relationship writes on `/api/v2/subscribers/{id}/relationships/<rel>`. GET is side-effect-free — see [[api-subscribers-list-querying]].

## Attributes

The attribute that matters most for side effects is `subscribed_from` (auto-filled to `"API"` on POST when omitted). The read-only campaign-metric fields are never settable. Full attribute table: [[api-subscribers-list-crud]].

## Relationships

Changes to the `channels` and `tags` relationships are treated as writes to the subscriber for webhook + segment-recompute purposes (see below). Relationship CRUD shapes are on [[api-subscribers-list-crud]]; channel/tag specifics on [[api-subscribers-channels]] / [[api-subscribers-tags]].

## Filtering & sorting

Read-side query parameters are documented on [[api-subscribers-list-querying]]. The one filter that interacts with side effects is `filter[segment]` — it is how an integration *detects* the silent plan-cap overflow described below (an over-cap subscriber will not appear in any segment).

## Side effects

- **`subscribed_from` auto-set to `"API"`** — when the caller doesn't supply a source on POST, the adapter's `creating` hook force-fills `subscribed_from = "API"`. This drives the *"Subscribed from"* filter on [[marketing-subscribers]] and the `subscriber.from` segment condition. Callers that want a different bucket must explicitly send it in `attributes.subscribed_from`.
- **Webhooks fire** — `subscriber.created` on POST (registered as a `register_shutdown_function` after the save completes), `subscriber.updated` on PATCH (same shutdown handler — fires on every save touching the subscriber, including channel/tag changes done as side-effects of the same request), and `subscriber.deleted` on DELETE. Delivered to subscribed [[settings-hooks]] endpoints — see [[notification-delivery]] for retry semantics.
- **Plan-tier subscriber cap (silent)** — the merchant's `subscribers` plan-feature limit applies to API-created subscribers the same way as imports. **The cap is enforced via the `subscribers.max_id` setting** (chronological — see [[marketing-subscribers]] business rules). A recurring background job re-computes the cap; segment-evaluator queries then add `WHERE subscribers.id <= subscribers.max_id`. **Implication**: subscribers POSTed past the cap land in the DB, but they're silently excluded from every segment / campaign until the merchant prunes earlier rows or upgrades the plan. **There is NO HTTP 402 returned by the API in the silent-cap case** — the side effect is invisible to the integration unless the integration queries segment membership.
- **Automated-segment incremental re-evaluation** — every Subscriber create/update fires an incremental segment-evaluator job that re-evaluates every active Automated segment for that one subscriber. Within seconds, the subscriber appears in (or disappears from) the right segments. **Full-population rebuild** of Automated segments runs on a separate 300-second (5-minute) cadence — see [[marketing-segments]] business rules.
- **DELETE cascade** — removes the subscriber row, ALL of the subscriber's channel rows ([[api-subscribers-channels]]), ALL of the subscriber's tag pivot rows ([[api-subscribers-tags]]), detaches from every segment (`subscriber_to_segments`), drops segment-event log entries, and nulls out `subscriber_id` on any pre-existing orders / carts that pointed at the subscriber. To remove ONE channel only (not the whole subscriber), use [[api-subscribers-channels]] DELETE instead.
- **Tag-membership recompute** — changes to the `tags` relationship trigger segment re-evaluation for `subscriber.has_tag` rules on the subscriber's segments.
- **No dedicated audit-log capture** — unlike orders (`namespace = "api2"` on `order_history`) or products / variants (per-attribute change-log with `initiator = "api"`), subscriber writes through this resource have no dedicated actor-identity capture. The only record is the row's `updated_at` / `created_at` timestamps. Merchants who need compliance trails on subscriber changes should log on their own integration side.

### Plan-feature gating

- **`subscribers` plan-feature cap** — applied silently as described above (chronological cap via `subscribers.max_id`; no HTTP 402 on overflow at this layer).
- **HTTP 402 (Payment Required)** — emitted only when the merchant's plan is expired / past-due / trial-ended. NOT emitted when the subscriber cap overflows.
- **HTTP 403** — not emitted by this resource (the framework's default authorizer is a permissive no-op; once auth passes, an API key has full access to this resource).

### Silent-cap worked scenario

Merchant is on a plan with `subscribers = 1000` and already has 1000 contacts. POST a new subscriber via this API → the resource returns **201 Created** with a real id (e.g., `1042`). However, `subscribers.max_id` remains at the id of the 1000th contact. Every segment evaluator adds `WHERE subscribers.id <= subscribers.max_id`, so subscriber `1042` is **silently excluded from every segment and every campaign** until the merchant prunes earlier rows or upgrades. There is **no warning header**, **no 402**, and no programmatic way to detect the overflow from this endpoint — the integration only notices when `GET /api/v2/subscribers?filter[segment]=<id>` does not include the new contact. See [[marketing-subscribers]] for cap-management.

## Equivalent UI

- [[marketing-subscribers]] — the admin subscriber list; the silent cap, the *"Subscribed from"* bucket, and deletion all surface here in merchant terms.
- [[settings-hooks]] — where the merchant subscribes to the `subscriber.*` webhook events triggered by writes.

## Testing checklist

End-to-end CRUD verification:

```
1. GET /api/v2/subscribers?page[size]=5
   — confirm 200 and that `meta.page` is populated.
2. POST /api/v2/subscribers with:
     attributes.country = "BG"
     attributes.first_name = "Test"
     included[0] = { type:"subscribers-channels",
                     attributes:{ channel:"Email",
                                  channel_identifier:"test+api@example.com",
                                  marketing:1, verified:0, bounced:0 } }
   — capture `data.id` as {SUB_ID}.
   — verify response `data.attributes.subscribed_from == "API"`.
3. GET /api/v2/subscribers/{SUB_ID}?include=channels,tags
   — verify the Email channel is sideloaded under `included[]`.
4. PATCH /api/v2/subscribers/{SUB_ID}
     attributes.first_name = "TestUpdated"
   — expect 200; verify the change on a follow-up GET.
5. POST /api/v2/subscribers-channels with:
     attributes.subscriber_id = {SUB_ID}
     attributes.channel = "WebPush"
     attributes.channel_identifier = "ignored"
     attributes.marketing = 1, verified = 0, bounced = 0
   — expect 422 with the `CHANNELS_API` allow-list error on /data/attributes/channel.
6. POST /api/v2/subscribers-channels with:
     attributes.subscriber_id = {SUB_ID}
     attributes.channel = "Phone"
     attributes.channel_identifier = "+359 87 123 4567"
     attributes.marketing = 1, verified = 0, bounced = 0
   — expect 201; on GET the stored value is normalised to "+359871234567" (E.164).
7. GET /api/v2/subscribers?filter[segment]=<segment_id>
   — verify the join works (returns members of the segment, or `[]` for an empty/non-existent id).
8. DELETE /api/v2/subscribers/{SUB_ID}
   — expect 204. Verify cascade: GET /api/v2/subscribers-channels?filter[subscriber_id]={SUB_ID}
     should return `[]`.
9. GET /api/v2/subscribers/{SUB_ID}
   — expect 404.
```

### Edge cases

- **`subscribers.max_id` silent cap** — see the worked scenario above; no warning header, no 402, detectable only via segment membership.
- **`subscribed_from` auto-fill** — omit the attribute and the adapter forces `"API"`. To use a different bucket (e.g., `"import"`), send it explicitly.
- **Channel write surface** — the `channels` relationship is API-writable only for `Email` and `Phone` rows. WebPush / Messenger rows are storefront-only — see [[api-subscribers-channels]] for the allow-list error.

## Related

- [[api-subscribers]] — hub.
- [[api-subscribers-list-crud]] — attribute reference + write examples that produce these effects.
- [[api-subscribers-list-querying]] — read-side parameters; `filter[segment]` is how the silent cap is detected.
- [[marketing-subscribers]] — cap management + the *"Subscribed from"* bucket in the admin UI.
- [[marketing-segments]] — Automated-segment re-evaluation cadence.
- [[api-subscribers-channels]] — channel rows removed by the DELETE cascade.
- [[api-subscribers-tags]] — tag pivot rows removed by the DELETE cascade.
- [[settings-hooks]] — `subscriber.*` webhook subscriptions.
- [[notification-delivery]] — webhook retry semantics.
- [[settings-api-keys]] — authentication setup.

## Open questions

- Confirm whether `subscriber.created` / `subscriber.updated` webhooks fire reliably from JSON-API v2 writes end-to-end (the events are wired through `register_shutdown_function` from the model layer; admin-panel saves and storefront subscribe-form submits both fire them, but the API path's shutdown-hook delivery should be verified under load).
- Verify whether the silent `subscribers.max_id` cap is reflected in any header or warning that the API caller could surface to the merchant proactively, or whether the only signal is "subscriber created but missing from segments". Today the integrator has no programmatic way to detect "I am over the cap".
