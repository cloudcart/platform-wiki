---
type: feature
nav_path: "Apps → GDPR → Requests → Types & channels"
route_name: gdpr.request
route_path: /gdpr/request/{type}
aliases: ["GDPR request types", "Data subject request types", "info request", "download request", "delete request", "marketing_unsubscribe", "GDPR storefront form", "Right to erasure type"]
tags: [apps, gdpr, compliance, requests, storefront]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
# GDPR → Requests: types & channels

> Part of [[apps-gdpr-requests]]. See the hub for the other aspects (data model, processing workflow).

## Purpose

This aspect documents **which** data subject requests a customer can submit and **how** they submit them. It covers the 4 customer-initiated request types, the two request types that are commonly assumed to exist but do NOT (rectification and restriction), the storefront form routes (full page + popup), the invalid-type fallback behaviour, the self-service download endpoints that bypass the formal request system, and the rule that the storefront form is the only submission channel.

## Where to find it

The customer initiates a request on the **storefront**, not the admin. The merchant sees the resulting rows in the admin Requests tab (`/admin/apps/gdpr/requests` — see [[apps-gdpr-requests]]). The customer-facing routes are:

- `GET /gdpr/request/{type}` — show the form page (route `gdpr.request`).
- `POST /gdpr/request/{type}` — submit the form.
- `GET /gdpr/request/{type}/popup` — show the form as a modal (route `gdpr.request.popup`).

The storefront customer GDPR page (`/gdpr`) links to these forms (Right-to-Information popup, Right-to-Erasure popup).

## What the merchant can do here

The merchant does not choose the request type — the customer does, by visiting the matching route. The merchant's role downstream is to read the `type` on each request row and process it accordingly (see [[apps-gdpr-requests-processing]]). What the merchant should know about types:

- Only **4** types ever reach the requests table.
- An unknown type in the URL does not error — it silently becomes `info`, so the merchant cannot rely on the URL type matching a real type.
- Marketing unsubscribe (`marketing_unsubscribe`) arrives through the same channel as data requests, so it shows up in the same Requests list.

## Settings & fields

### The 4 customer-initiated request types (verified)

Customers can submit only these 4 request types via the storefront form:

| Type | What it means |
|---|---|
| `info` | Request information (Article 15 access). |
| `download` | Request data export (Article 20 portability). |
| `delete` | Right to erasure (Article 17). |
| `marketing_unsubscribe` | Unsubscribe from marketing. |

**Rectification (Article 16) is NOT a request type.** Customers correct their own data via storefront self-edit; there is no merchant-managed rectification queue.

**Restriction (Article 18) is NOT a request type.** It is not implemented in the CloudCart request system.

### Request type from the URL — invalid types fall back to `info`

When the customer hits `/gdpr/request/{type}` with an unknown type string (e.g., `/gdpr/request/foo`), the controller silently coerces it to `info`. **No 404 is returned for invalid request types** — the storefront just shows the info-request form. The request type stored is the URL `{type}` when valid, `info` otherwise.

## Business rules

### Storefront form is the ONLY submission channel

There is no email-parsing and no external-integration submission path. Customers submit ONLY via `/gdpr/request/{type}` on the storefront. Email-based requests a merchant receives outside the platform must be entered manually by the merchant or they never enter the requests system at all.

### Self-service downloads bypass the formal request system

A logged-in customer can download their own data directly, WITHOUT filing a formal `download` request, via:

- `/gdpr/download/personal-information`
- `/gdpr/download/orders`
- `/gdpr/download/addresses`

These endpoints serve the data immediately to the authenticated customer. They do NOT create a `gdpr_requests` row, so self-served downloads will not appear in the admin Requests list. The formal `download` request type is for cases where the customer wants the merchant to act (e.g., a guest with no login). See [[apps-gdpr-overview]] for the self-service download details.

### `marketing_unsubscribe` arrives as a request, not a list edit

Because unsubscribe is one of the 4 types, a customer's marketing opt-out can land in the Requests tab rather than only flowing through the subscriber list. The merchant should treat these like any other request row and process them.

## Related

- [[apps-gdpr-requests]] — hub.
- [[apps-gdpr-requests-data-model]] — what each submission writes to the `gdpr_requests` row and the validation rules (referenced inline above).
- [[apps-gdpr-requests-processing]] — how the merchant resolves each type once it arrives (referenced inline above).
- [[apps-gdpr-overview]] — GDPR hub; self-service download details.

## Open questions

None.
