---
type: feature
nav_path: "Settings → Webhooks"
route_name: hooks.settings
route_path: /admin/settings/hooks
aliases: ["Webhooks", "Hooks", "HTTP callbacks", "Event hooks", "Уебхукове", "Хукове", "Известия за събития"]
tags: [settings, webhooks, integrations, events, developer]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 8
---

# Webhooks

## Purpose

A configuration screen for **outgoing HTTP webhooks**: the merchant defines URLs that CloudCart POSTs to when store events happen (product created, order updated, customer signs up, etc.). Each webhook ties together a destination URL, an API key (auto-forwarded as the **`X-CloudCart-ApiKey`** header), an **event** from a fixed catalogue of 20 (theoretically 21 — `order.deleted` is disabled), optional custom HTTP headers, and an Active flag.

Delivery is a **queue-backed pipeline with built-in retry, auto-disable on permanent receiver failures, and a backend activity log**. Up to **6 attempts** (1 initial + 5 retries) span **20 minutes** before CloudCart gives up — at which point the webhook is **auto-disabled** and the merchant is emailed. Specific HTTP status codes mark the receiver as permanently broken and auto-disable the webhook (sometimes auto-delete it) instead of retrying. The biggest UX gap is the absence of a self-service activity-log viewer — see [[settings-hooks-activity-log]].

## Where to find it

Sidebar → Settings → **Webhooks**. Route `/admin/settings/hooks`. The store's **Site ID** is displayed as a chip in the page header (most webhook receivers want this for store identification).

## Sub-pages (in this cluster)

Drill into the aspect that matches the question, not every page.

- [[settings-hooks-events]] — the 20-event catalogue (7 groups × 3 actions, minus disabled `order.deleted`); payload shape; v1 vs v2 `new_version` toggle.
- [[settings-hooks-delivery]] — first-attempt timing (sync vs deferred 60 s for multi-webhook order events); the 5-second timeout (enforced three times); `order-events8` queue visibility.
- [[settings-hooks-retry]] — the 6-attempt retry timeline (delays 120 / 180 / 240 / 300 / 360 s = 20 min); final-attempt auto-disable + merchant email; retryable failures (5xx, 408, 429, timeouts, TLS).
- [[settings-hooks-auto-disable]] — permanent codes that skip retries (`400, 401, 403, 404, 405, 406, 410, 411` + DNS failures) + the `please unsubscribe me` auto-delete trigger.
- [[settings-hooks-modal]] — Create / Edit modal layout; field-by-field behaviour; inline row controls (Active toggle, delete, click-to-edit); bulk-delete; server-side validation.
- [[settings-hooks-activity-log]] — the Last-used count (increments on every attempt, not just success); backend activity log gated by `allowed_logging`; troubleshooting workflow.
- [[settings-hooks-auth-headers]] — auto-injection of `X-CloudCart-ApiKey`; merchant custom headers (Card 2 of the modal); replace-all-on-update semantics; FK-block on linked API key deletion.

## What the merchant can do here

- See the store's **Site ID** as a chip in the page header.
- Click **+ Add webhook** to open the create modal (see [[settings-hooks-modal]]).
- See the table of all defined webhooks with destination URL, event, API key reference, active status, last-used count, and per-row edit/delete actions.
- Click any row's Event or Destination URL cell to open the Edit modal.
- Toggle a webhook's **Active** flag inline. Inactive webhooks stay configured but are skipped entirely when their event fires.
- Delete a row per-row, or bulk-delete via the table's checkbox column.
- Filter, search, sort, paginate the webhooks table.

## Settings & fields

Table-level controls only — field-level detail (modal layout, validation, endpoints) lives on [[settings-hooks-modal]]. Visible columns:

- **Active** — inline toggle. OFF skips delivery entirely. Re-enabling after auto-disable resets the alert mute (see [[settings-hooks-auto-disable]]).
- **Destination URL** — full URL stored; cells > 25 chars truncate with `...`. Click to open Edit modal.
- **Event** — one of the 20 events. See [[settings-hooks-events]] for the catalogue.
- **API key** — name of the linked key; its VALUE is auto-injected as `X-CloudCart-ApiKey` on every delivery. See [[settings-hooks-auth-headers]].
- **Last-used count** — increments on every attempt (success AND failure). See [[settings-hooks-activity-log]].
- **Row actions** — Edit (click), Delete (confirm), bulk-Delete (checkbox column).

Header: **Site ID chip** + **+ Add webhook** button (opens [[settings-hooks-modal]]).

## Business rules

Cross-cutting rules; each aspect page holds the full detail.

- **20 events, not 21.** `order.deleted` is disabled. Merchants who delete orders cannot subscribe to a webhook for it. See [[settings-hooks-events]].
- **First attempt is sync for single-webhook setups.** A slow receiver makes the merchant's save spinner hang up to 5 seconds. For 2+ active webhooks on `order.created` / `order.updated`, the first attempt is deferred 60 s on the `order-events8` queue. See [[settings-hooks-delivery]].
- **Retries are linear, not exponential.** 5 retries over 20 minutes with growing 60-second-multiple delays (`(retries + 1) × 60` seconds). On the 6th failed attempt, the webhook is **auto-disabled** and the merchant gets an email — see [[settings-hooks-retry]] "Final give-up". Each retry re-evaluates the auto-disable rules — a transient 503 turning into a 404 mid-retry stops the pipeline immediately.
- **Auto-disable on permanent HTTP codes** (`400, 401, 403, 404, 405, 406, 410, 411`) and on `Could not resolve host` DNS errors. Re-enable is manual; the alert mute resets on re-enable. See [[settings-hooks-auto-disable]].
- **Auto-delete on the literal substring `please unsubscribe me`** inside an ERROR-response (4xx / 5xx / connection-error) exception message. **A 200 OK with the phrase in the body does NOT trigger auto-delete** — the catch block isn't entered on success. Receivers must not echo merchant payloads verbatim in error responses. See [[settings-hooks-auto-disable]].
- **`X-CloudCart-ApiKey` is auto-injected** from the linked API key on every delivery. Custom headers (Card 2 of the modal) layer alongside; update replaces all custom headers atomically. See [[settings-hooks-auth-headers]].
- **Last-used count increments on every attempt (success AND failure)**, not just success. A high counter on a webhook the receiver claims never saw is consistent — those are failed attempts. See [[settings-hooks-activity-log]].
- **Activity log is OFF by default for production stores.** The backend log is gated by an `allowed_logging` list that contains only an internal CloudCart test site; enabling it for a merchant requires CloudCart support. This is the biggest webhook UX gap today. See [[settings-hooks-activity-log]].
- **Permission gate.** A moderator needs the Settings or Webhooks permission, configured under [[settings-staff]].
- **The OTHER webhook system.** A separate, internal-use webhook system handles internal platform events outside merchant control. This is NOT what Settings → Webhooks configures.

## Programmatic access

Webhook subscriptions can be managed via **JSON-API v2** — see [[api-webhooks]] for the endpoint, validation, and event list. The API exposes the SAME subscription model as the admin panel (same 20 events, same `X-CloudCart-ApiKey` injection, same retry policy). Integrations that ship a CloudCart connector typically self-register their subscriptions through the API rather than asking the merchant to configure them by hand. See [[json-api-v2]] for authentication, rate limit, and the side-effects principle.

## Related

- [[settings]] — parent hub.
- [[settings-api-keys]] — webhook authentication credential source; the linked API key value is auto-sent as `X-CloudCart-ApiKey`; FK-blocks key deletion when in use here.
- [[settings-queue-view]] — webhook delivery jobs (first-attempt and retry) run on the `order-events8` queue; visible there.
- [[settings-admin-notifications]] — webhook failure alerts surface in the admin notification panel via the platform's alert helper.
- [[settings-statuses]] — `order.updated` events fire on status changes; the order's status CODE is sent in the payload (not the renamed label).
- [[settings-staff]] — moderator permission tree containing the Webhooks permission.
- [[product]] / [[category]] / [[order]] / [[customer]] / [[subscriber]] / [[discount]] / [[vendor]] — entities that fan out the corresponding `<entity>.*` events.
- [[webhook]] — entity page.
- [[api-key]] — entity page.
- [[api-webhooks]] — JSON-API v2 surface for managing webhook subscriptions programmatically.
- [[json-api-v2]] — JSON-API v2 conventions, auth, rate limit, side-effects principle.
- [[notification-delivery]] — concept page on platform-wide outbound notification mechanisms.
- [[background-queue-inventory]] — catalogue of all background processes; covers webhook-delivery cadence, retries, and visibility on Queue View when a webhook is stuck.
- [[order-processing-pipeline]] — which `order.*` webhooks fan out at which lifecycle stages, with the retry policy explained.
- [[inventory-tracking]] — `product.updated` webhook fires on stock changes.

## Open questions

None — previously-flagged items moved to the aspect pages where they have full context.
