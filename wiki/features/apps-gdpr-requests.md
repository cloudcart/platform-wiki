---
type: feature
nav_path: "Apps → GDPR → Requests"
route_name: apps.gdpr.requests
route_path: /admin/apps/gdpr/requests
aliases: ["GDPR Requests", "Data subject requests", "DSR", "Right to access", "Right to erasure", "Right to portability"]
tags: [apps, gdpr, compliance, requests, data-subject-rights]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 6
---
# GDPR → Requests

## Purpose

The **Requests** tab is where the merchant manages **data subject requests** (DSRs) — formal requests under GDPR for a customer to access, download, or erase the data the store holds about them, or to unsubscribe from marketing. GDPR requires the merchant to respond within **30 days** of receiving a request. This tab lists incoming requests and is the merchant's workspace for resolving each one.

This page is the **hub** for the GDPR Requests cluster. It is intentionally slim — definition plus a catalogue of the aspect pages below. Drill into the aspect that matches the question rather than reading every page. For overall GDPR coverage (cookies, policy popups, consent logging), see [[apps-gdpr-overview]].

## Sub-pages (in this cluster)

This feature is split into 3 aspect pages, each covering one well-scoped slice:

- [[apps-gdpr-requests-types-channels]] — the **4** customer-initiated request types (`info`, `download`, `delete`, `marketing_unsubscribe`), why rectification and restriction are NOT request types, the storefront form routes (page + popup), the invalid-type fallback to `info`, the self-service download endpoints, and why the storefront form is the only submission channel.
- [[apps-gdpr-requests-data-model]] — the `gdpr_requests` row fields, the binary `processed_at` workflow (no status / approve / reject / close enum), the storefront form validation split (popup vs full page), the 191-char `message` cap, automatic IP capture, the DB-transaction insert, and the vestigial empty `requestsList` endpoint.
- [[apps-gdpr-requests-processing]] — the merchant workflow: the 30-day window (no built-in deadline indicator), identity verification, erasure scope and legal retention, manual anonymisation via [[customers-details]] with no rollback, portability format, no customer-side status notification, and the absent type-filter dropdown.

## Where to find it

Sidebar → Apps → GDPR → **Requests tab**. Route: `/admin/apps/gdpr/requests` (`apps.gdpr.requests`). The tab is available when the GDPR app is active. The data table uses `app-name="gdpr_requests"` for table state. The listing endpoint that actually returns data is the nested `/api/gdpr/requests/` (see [[apps-gdpr-requests-data-model]] for the endpoint detail).

## What the merchant can do here

- **View incoming requests** — a standard data table with search / pagination, one row per request, showing customer, request type, submission date, and processed-at timestamp. See [[apps-gdpr-requests-data-model]] for the stored fields and [[apps-gdpr-requests-processing]] for the missing type-filter dropdown.
- **Process a request** — generate a data export (Access / Portability), anonymise personal fields (Erasure), or unsubscribe from marketing. The actual data actions happen on the related customer record; the merchant marks the request done by setting `processed_at`. See [[apps-gdpr-requests-processing]].
- **Track completion** — the workflow is binary: a request is either *open* (`processed_at` NULL) or *processed* (`processed_at` set). See [[apps-gdpr-requests-data-model]].

What the merchant **cannot** do here: auto-process requests, fully delete a customer's financial / tax history (legal retention applies), undo an anonymisation, or rely on a built-in 30-day overdue badge. See [[apps-gdpr-requests-processing]].

## Settings & fields

There are no setting keys unique to the hub. The request-row fields, validation rules, and request-type slugs are documented on the aspect pages:

- Request-type slugs (`info`, `download`, `delete`, `marketing_unsubscribe`) and the storefront form routes — see [[apps-gdpr-requests-types-channels]].
- Stored row fields (`customer_id`, `email`, `name`, `message`, `type`, `client_ip`, `created_at`, `processed_at`) and validation — see [[apps-gdpr-requests-data-model]].

## Business rules

The cluster-wide rule: **the storefront form is the only intake channel, the workflow is binary processed/not-processed, and the actual data actions are manual.** The platform stores the request and a single `processed_at` timestamp; it does not anonymise data, notify the customer, or track a 30-day deadline for the merchant. Those operational rules — identity verification, erasure scope, legal retention, portability format — all live on [[apps-gdpr-requests-processing]].

## Related

- [[apps-gdpr-overview]] — GDPR hub.
- [[apps-gdpr-acceptance]] — acceptance / consent log (records preserved through Erasure).
- [[apps-gdpr-overview-data-requests]] — the overview-level summary of the data-request flow.
- [[customers]] / [[customers-details]] — customer records being processed.
- [[orders]] — orders typically retained under financial retention even after Erasure.

## Open questions

None.
