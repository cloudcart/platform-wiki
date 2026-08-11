---
type: feature
nav_path: "Settings → Webhooks → Auto-disable & auto-delete"
route_name: hooks.settings
route_path: /admin/settings/hooks
aliases: ["Webhook auto-disable", "Auto-disable webhook", "Permanent failure", "please unsubscribe me", "Webhook auto-delete", "Webhook permanent codes"]
tags: [settings, webhooks, failures, integrations]
plan_gates: []
created: 2026-06-10
updated: 2026-06-11
source_count: 3
---

> Part of [[settings-hooks]]. See the hub for the other aspects (events, delivery, retry, modal, activity log, auth & headers).

# Webhooks — auto-disable & auto-delete

## Purpose

The webhook pipeline tries hard to deliver — see [[settings-hooks-retry]] for the 7-attempt budget — but some failures signal *"this receiver fundamentally cannot handle this request"* and retrying is pointless. In those cases the platform takes a definitive action instead of retrying: either **auto-disable** the webhook (toggled OFF; requires manual re-enable) or **auto-delete** it (the row is removed entirely).

## Where to find it

Auto-disable and auto-delete decisions are made automatically by the delivery pipeline. Their consequences surface in two places:

- The webhook's **Active** column flips OFF on this page (auto-disable), or the row vanishes (auto-delete).
- [[settings-admin-notifications]] surfaces an alert describing the disable reason and the affected webhook URL.

## What the merchant can do here

- After an auto-disable: fix the receiver, then **manually toggle the webhook Active switch back ON** from the table row (see [[settings-hooks-modal]]). The platform does NOT auto-re-enable.
- After an auto-delete: the merchant must **create the webhook again from scratch** — there is no "restore" affordance.
- Read the alert text on [[settings-admin-notifications]] to learn why the disable happened (the alert includes the disable reason + URL).

## Settings & fields

### Auto-disable on permanent HTTP failure

The webhook is **immediately deactivated** (toggled OFF) and the retry pipeline is **skipped** when the failure is one of these "permanent" cases:

- **HTTP status from this fixed list: `400, 401, 403, 404, 405, 406, 410, 411`.** Interpreted as *"the receiver knows it can't handle this — retrying is pointless."* Covers URL doesn't exist (404), wrong HTTP method (405), permission denied (401/403), resource gone (410), bad request (400), not acceptable (406), length required (411).
- **DNS error: "Could not resolve host"** — the destination domain doesn't exist or DNS is broken (the request can't even be sent).

After auto-disable:
- The webhook row's `active` flag flips from 1 → 0.
- A persistent alert appears in the [[notifications]] inbox (bell icon → "View all notifications", route `/admin/notifications`) describing the disable reason + the affected webhook URL **plus the verbatim receiver error message** — see "Where the merchant reads the error message" below.
- An email is sent to the store's `site_email` via the always-on `alert_notification` channel — see [[admin-notifications-mandatory-three]].
- The alert is **grouped per webhook** so one broken webhook does not spam infinite alerts.

### Where the merchant reads the error message — closing the loop

The webhook auto-disable alert is NOT just a "your webhook broke" notice — it carries the receiver's actual error text so the merchant can fix the integration without leaving the admin. The full message rendering is documented on [[notifications]] (the bell-icon inbox at `/admin/notifications`).

Rendered text (the auto-disable message):

- **EN**: *"The Webhook (`<event> - <url>`) has been deactivate because we received an error from the receiver with message: `<receiver-response-body>`"*.
- **BG**: *"Webhook (`<event> - <url>`) е деактивиран, защото получихме грешка от получателя със съобщение: `<receiver-response-body>`"*.

The `<receiver-response-body>` is the receiver's response text; for JSON bodies the platform extracts the `error` / `message` field, otherwise the raw body. The DNS-failure case uses a separate, shorter message that just names the URL.

The SAME text is sent in:
- The email body to `site_email` (the merchant's inbox).
- The Message column of the [[notifications]] inbox row.
- The bell-icon dropdown preview at the top of every admin page.

So the merchant has three concurrent surfaces showing the same actual error text. No separate "webhook log viewer" exists in the admin UI (see [[settings-hooks-activity-log]]); the alert message IS the user-facing error surface.

### Auto-delete on the literal phrase "please unsubscribe me"

If a failed delivery's error text contains the literal substring **`please unsubscribe me`**, the webhook row is **deleted entirely** — not just deactivated. This is a graceful opt-out mechanism. The match is:

- **Substring**, not full-string. An exception message that includes `"... please unsubscribe me from this hook"` triggers auto-delete.
- **ERROR responses only — not status-code-agnostic.** Auto-delete is evaluated only when the delivery **fails** (4xx / 5xx / connection / TLS error). **A 200 OK whose body contains `please unsubscribe me` does NOT trigger auto-delete** — successful responses are never inspected for the phrase.
- On a failed response the matched text includes the status line **and** a snippet of the receiver's body, so an unsubscribe phrase in an error-response body is effectively matched.

This means receivers **should not echo back the request payload verbatim in 4xx / 5xx error responses** — if the merchant's data contains "please unsubscribe me" (e.g. an order's customer note), echoing it in an error response body would self-trigger auto-delete. In **200 OK** responses the merchant can safely echo anything — the phrase is ignored.

After auto-delete:
- The row is gone — no manual re-enable path.
- No further alerts about this webhook (because there's no row to alert about).
- The merchant must add the webhook again from scratch via the create modal — see [[settings-hooks-modal]].

### Auto-re-enable behaviour (manual flip back ON)

When the merchant manually toggles an auto-disabled webhook back ON, the platform's `saving` hook detects the active flag flipped from 0 → 1 and **resets the alert's notification suppression flags**. So if the webhook breaks again later, the merchant WILL get a fresh email notification — they are **NOT permanently muted**.

### Each retry re-evaluates the auto-disable rules

If a transient 503 turns into a 404 mid-retry (e.g. the receiver redeploys with the endpoint removed during the 21-minute retry window), retries stop immediately and the webhook is auto-disabled. The pipeline does NOT keep retrying past a now-permanent failure. See [[settings-hooks-retry]] for the retryable failure catalogue.

## Business rules

- **Permanent codes are a fixed list — not "any 4xx".** HTTP **408** (Request Timeout) and **429** (Too Many Requests) are explicitly NOT in the permanent list — they trigger retries instead. A receiver wanting to throttle CloudCart should return 429.
- **Receivers can opt themselves out without admin access.** Returning the `please unsubscribe me` phrase in a 4xx / 5xx error response deletes the webhook on CloudCart's side without the merchant ever logging in. This is intentional but caught out merchants in the past when their developer added the phrase to a generic error template. Note that the phrase must travel through the exception message (any non-2xx response qualifies); a 200 OK with the phrase in body does NOT trigger it.
- **Auto-disable triggers a fresh notification chain on re-enable.** Merchants who silenced past alerts should know that re-enabling resets the suppression — they will get pinged again on the next break.
- **Auto-disable after 6 transient failures sends an email too**, not just a panel alert — the email fires when the webhook actually flips to disabled. See [[settings-hooks-retry]] "Final give-up" for the full mechanism.

## Related

- [[settings-hooks]] — hub.
- [[settings-hooks-retry]] — the alternative path: retryable failures and the 21-minute timeline.
- [[settings-hooks-delivery]] — initial-attempt timing and the 5-second timeout that produces many retry-class failures.
- [[settings-hooks-modal]] — where the merchant flips the Active switch back ON after auto-disable.
- [[settings-admin-notifications]] — the alert surface for auto-disable + final give-up.

## Open questions

- HTTP codes **402 / 451 / 414** (and other 4xx not in the fixed list `[400, 401, 403, 404, 405, 406, 410, 411]`) are **retried** — only codes in that exact list trigger auto-disable; every other 4xx flows through the retry pipeline.
