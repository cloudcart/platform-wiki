---
type: feature
nav_path: "Apps → GDPR → Data-subject requests"
route_name: apps.gdpr.requests
route_path: /admin/apps/gdpr/requests
aliases: ["GDPR data-subject requests", "Right to access", "Right to erasure", "Right to portability", "GDPR self-service download", "GDPR request types"]
tags: [apps, gdpr, compliance, privacy, requests, storefront]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
# GDPR — Data-subject requests + self-service downloads

> Part of [[apps-gdpr-overview]]. See the hub for the other aspects (consent UX, script gating, consent logging) and the GDPR tab pages.

## Purpose

This aspect documents the **customer-initiated data-subject request system** (GDPR Articles 15-17, 20): the four supported request types, why rectification is not one of them, the storefront URLs where requests are submitted, the three self-service download endpoints (right-to-portability), and the merchant-driven right-to-erasure flow. The admin Requests tab where the merchant processes incoming requests is documented on [[apps-gdpr-requests]].

## Where to find it

The merchant processes requests from the GDPR app's **Requests** tab (`/admin/apps/gdpr/requests`, route `apps.gdpr.requests`). Customers submit requests from the storefront at `/gdpr/request/{type?}`.

## What the merchant can do here

- Review incoming customer data-subject requests (open / processed / closed).
- Act on each request type — typically anonymise the customer record for an erasure request, or confirm the data export for an access/portability request.
- Mark requests Processed; the system tracks `processed_at`.

## Settings & fields

### Request types — 4 distinct GDPR data-subject-request types

The platform supports these customer-initiated request types:

| Type key | Translation key | What it does |
|---|---|---|
| `info` | the platform code | Request for information about what data is held (GDPR Article 15). |
| `download` | the platform code | Right-to-portability — receive a structured machine-readable export (Article 20). |
| `delete` | the platform code | Right-to-erasure (Article 17). |
| `marketing_unsubscribe` | the platform code | Unsubscribe from marketing communications. |

This is the **FULL list** of customer-initiated request types. (Commented-out form types `marketing` and `mailchimp_newsletter` are likely deprecated.)

### Rectification (Article 16) is NOT a request type

The system supports exactly 4 request types — info, download, delete, marketing_unsubscribe. **Rectification is not in the request system because customers correct their own data via their storefront account profile** (self-edit pattern, not a request workflow).

### Storefront request URLs — explicit storefront routes

The customer-facing request form lives at `/gdpr/request/{type?}`. Variants:

| Route | Route name | Purpose |
|---|---|---|
| `GET /gdpr/request/{type}` | — | Show the request form (page). |
| `GET /gdpr/request/{type}/popup` | `gdpr.request.popup` | Show the form in a modal popup. |
| `POST /gdpr/request/{type}` | — | Submit the request. |
| `GET /gdpr` | `site.gdpr` | Main GDPR landing page. |

`{type}` must be one of the four request types (info, download, delete, marketing_unsubscribe) — invalid types fall back to `info`.

### Self-service downloads — 3 customer endpoints (right-to-portability)

The storefront exposes three download endpoints under `/gdpr/download/*` (require a logged-in customer). Each returns a CSV file with the customer's data:

| Endpoint | Route name | Returns |
|---|---|---|
| `GET /gdpr/download/personal-information` | `site.gdpr.download.personal_information` | Customer's id, first/last name, email (CSV). |
| `GET /gdpr/download/orders` | `site.gdpr.download.orders` | All the customer's orders (CSV) — order id, name, email, status, total, products, shipping address, billing address. |
| `GET /gdpr/download/addresses` | `site.gdpr.download.addresses` | All shipping/billing addresses from the customer's orders (CSV). |

This is the right-to-portability implementation — a logged-in customer can immediately download their data without filing a request, so the merchant doesn't have to handle most "download" requests manually.

## Business rules

### Right-to-erasure flow (Requests tab)

When a customer submits a Right-to-Erasure request:
1. Request lands in the Requests tab as Open.
2. The merchant reviews + acts (typically: anonymise the customer record, delete personal data, retain financial / audit data per legal retention).
3. The merchant marks the request Processed.

GDPR requires response within 30 days of request submission.

### Anonymisation on right-to-erasure is merchant-driven

There is no automated customer-erase action in the GDPR module — the Requests tab marks a `delete` request and tracks `processed_at`, but the actual customer-data anonymisation is performed by the merchant via the [[customers-details]] page (or, for older platforms, manually by support). The acceptance log itself is append-only — entries are created or touched, never deleted — so the FACT of consent is retained even after the customer's personal record is anonymised (see [[apps-gdpr-overview-consent-logging]]).

## Related

- [[apps-gdpr-overview]] — hub.
- [[apps-gdpr-requests]] — admin Requests tab where the merchant processes requests.
- [[customers-details]] — where the merchant performs the actual anonymisation on erasure.
- [[apps-gdpr-overview-consent-logging]] — append-only acceptance log retained after anonymisation.

## Open questions

None.
