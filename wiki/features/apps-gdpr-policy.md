---
type: feature
nav_path: "Apps → GDPR → Policy"
route_name: apps.gdpr.policies
route_path: /admin/apps/gdpr/policy
aliases: ["GDPR Policy", "Privacy policy", "Terms and conditions", "Legal policies"]
tags: [apps, gdpr, compliance, policy, legal, privacy]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 7
---
# GDPR → Policy

## Purpose

The **Policy** tab is where the merchant manages their **privacy / legal policy documents** — Privacy Policy, Terms of Service, Cookie Policy, Return Policy, etc. Each policy has a title, rich-text body, and active/inactive status. Customers see required and optional policies as accept checkboxes on storefront forms (registration, checkout, popups) and as standalone storefront legal pages. The acceptance log ([[apps-gdpr-acceptance]]) records exactly which customer accepted which policy text at what time — the GDPR audit trail.

This page is the **hub** for the policy cluster. It is intentionally slim — definition + a catalogue of the aspect pages below. Drill into the aspect that matches the question rather than reading every page. For overall GDPR coverage, see [[apps-gdpr-overview]].

## Sub-pages (in this cluster)

This feature is split into 4 aspect pages, each covering one well-scoped slice:

- [[apps-gdpr-policy-editor]] — the policy list + the minimal 3-field Add/Edit modal (`pol.name`, `marketing_policy` toggle, `pol.content`); validation (name min 2 / max 191, content min 2); one-click status toggle; hard delete; autocomplete; name uniqueness against the entire pages table.
- [[apps-gdpr-policy-forms]] — the many-to-many policy-to-form mapping (required vs optional per form); the "optional first" render order; the single marketing-policy designation that flips `customer.marketing`; the silent skip of inactive policies on the storefront.
- [[apps-gdpr-policy-storefront]] — policy-as-Page model; HTML rendering at `/page/{handle}`; no PDF export; the `{cookies_table}` dynamic placeholder; the acceptance-time content snapshot (implicit versioning); per-site Multilang copies.
- [[apps-gdpr-policy-seeding]] — install seeds 4 starter policies (privacy / marketing / terms / cookie); store-language-aware text in 6 languages with English fallback; placeholder-variable substitution from store settings; no jurisdiction presets.

## Where to find it

Sidebar → Apps → GDPR → **Policy tab**. Route: `/admin/apps/gdpr/policy` (`apps.gdpr.policies`). The tab is available when the GDPR app is active.

API endpoints under `/api/gdpr/policy/`:
- `GET /api/gdpr/policy/` — list all policies (`gdpr.api.policies.list`).
- `POST /api/gdpr/policy/` — create new (`gdpr.api.policy.create`).
- `GET /api/gdpr/policy/get/{policy_id}` — fetch single (`gdpr.api.policy.edit`).
- `PATCH /api/gdpr/policy/{policy_id}` — update (`gdpr.api.policy.update`).
- `DELETE /api/gdpr/policy/{id}` — delete (`gdpr.api.policy.delete`).
- `GET /api/gdpr/policy/auto-complete` — autocomplete (`gdpr.api.auto_complete.policies`).
- `GET /api/gdpr/policy/status/{policy_id}/{status?}` — toggle status (`gdpr.api.policy.status`).

## What the merchant can do here

- Create, edit, and delete policy documents — see [[apps-gdpr-policy-editor]].
- Toggle each policy active / inactive (one click, instant) — see [[apps-gdpr-policy-editor]].
- Attach policies to storefront forms as required or optional, and designate one as the marketing-consent policy — see [[apps-gdpr-policy-forms]].
- Rely on the seeded starter policies created at install in the store's language — see [[apps-gdpr-policy-seeding]].

The merchant CANNOT: modify the acceptance log retroactively (it is immutable per GDPR audit requirement — see [[apps-gdpr-acceptance]]); display a policy on the storefront without setting it Active; or restore a deleted policy (delete is a hard delete — see [[apps-gdpr-policy-editor]]).

## Settings & fields

The merchant-facing fields live on the Add/Edit modal (three fields only) and the per-row status toggle — both documented on [[apps-gdpr-policy-editor]]. Form-attachment settings (required/optional per form, marketing designation) are documented on [[apps-gdpr-policy-forms]] and configured under the form-section saves in [[apps-gdpr-settings]].

## Business rules

- A policy record is a specialized **Page** filtered to policy-typed records, so it shares the full page content editor and page fields. Implications for storefront rendering, versioning, and Multilang are on [[apps-gdpr-policy-storefront]].
- Each policy maps many-to-many to the 5 form types from [[apps-gdpr-overview]], each attachment marked required or optional. Render order is "optional first, then by id". See [[apps-gdpr-policy-forms]].
- At most ONE policy per store can be the marketing policy; accepting/rejecting it flips `customer.marketing` and fires a customer-marketing-changed event. See [[apps-gdpr-policy-forms]].
- Install seeds 4 starter policies in the store language (English fallback). See [[apps-gdpr-policy-seeding]].

## Related

- [[apps-gdpr-overview]] — GDPR hub.
- [[apps-gdpr-acceptance]] — acceptance log of these policies.
- [[apps-gdpr-cookies]] — cookies + cookie consent (sister cluster).
- [[apps-gdpr-settings]] — where form-attachment of policies is saved.
- [[apps-gdpr-address]] — store address referenced in seeded policy text.
- [[checkout-flow]] — where customers accept policies.

## Open questions

None.
