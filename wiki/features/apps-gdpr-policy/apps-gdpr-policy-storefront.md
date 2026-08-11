---
type: feature
nav_path: "Apps → GDPR → Policy → Storefront rendering"
route_name: apps.gdpr.policies
route_path: /admin/apps/gdpr/policy
aliases: ["Policy as page", "Policy storefront page", "Policy HTML rendering", "No PDF export", "cookies_table placeholder", "Policy content snapshot", "Policy versioning", "Multilang policy", "Cookie Policy page"]
tags: [apps, gdpr, compliance, policy, storefront, multilang]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---
# GDPR — Policy: storefront rendering

> Part of [[apps-gdpr-policy]]. See the hub for the other aspects (editor, form mapping, seeding).

## Purpose

This aspect documents how a policy **lives as a storefront page and is presented to customers** — the policy-as-Page data model, HTML rendering at `/page/{handle}`, the absence of PDF export, the `{cookies_table}` dynamic placeholder, the acceptance-time content snapshot that gives policies implicit version history, and how Multilang produces per-language copies. The edit modal is on [[apps-gdpr-policy-editor]]; form attachment is on [[apps-gdpr-policy-forms]].

## Where to find it

A policy is created and edited from the Policy tab (`/admin/apps/gdpr/policy`), but customers see it as a storefront page at `/page/{url_handle}` (e.g., `/page/privacy-policy`) and as accept checkboxes inside the GDPR forms.

## What the merchant can do here

- Write full HTML / rich-text policy bodies (same editor as regular storefront pages).
- Embed the `{cookies_table}` placeholder to surface a live cookie table inside a policy.
- Maintain per-language policy copies when [[apps-multilang]] is active.

## Settings & fields

### Policy is a Page with a global scope

A policy record is a specialized **page** filtered to policy-typed records. **It uses the same content editor as regular pages** — full HTML / rich text, image embedding, etc. — and carries all standard Page fields (name, content, slug, SEO, status). The URL handle is auto-derived from the title (e.g., `privacy-policy`), which is why the edit modal exposes no separate handle / SEO field (see [[apps-gdpr-policy-editor]]).

### `{cookies_table}` placeholder

The merchant can insert `{cookies_table}` anywhere in a policy body. At storefront render time the placeholder is replaced with a dynamic table of all active cookie groups + their cookies, reflecting the visitor's current consent state. So a policy is a hybrid: static prose with one optional dynamic table. Cookie definitions come from [[apps-gdpr-cookies]].

## Business rules

### No PDF export — policies are rendered as HTML pages

Each policy renders as an HTML page using the merchant's theme template. **There is no built-in PDF export endpoint.** To share a PDF, the merchant must print-to-PDF from the browser or use a third-party tool.

### Policy content snapshot at acceptance time — implicit versioning

When a customer accepts a policy, the platform writes a snapshot of the policy's name + content to the acceptance content store, keyed by an MD5 hash of the name plus content. If the merchant later edits the policy text, future acceptances use a new hash — past acceptances still reference the original snapshot. **This gives policies implicit version history**: the merchant sees no "Versions" UI tab, but [[apps-gdpr-acceptance]] preserves the exact text each customer accepted. This is also why deleting a policy does not erase past acceptance snapshots (see [[apps-gdpr-policy-editor]]).

### Cookie Policy is a static seeded page — NOT auto-generated from cookie definitions

The seeded `cookie-policy` page ships with a fixed HTML template describing typical cookies (CSRF, Session, CloudCart Analytics, Google Analytics, AddThis, Remember-me) plus a placeholder block `{data_provider} - {description} - {cookie_name}` that the merchant manually fills in. **The page does NOT auto-rebuild from the [[apps-gdpr-cookies]] cookie definitions.** The merchant CAN insert `{cookies_table}` to embed the dynamic table (above) — but the surrounding prose stays static. The seeding of this page is covered on [[apps-gdpr-policy-seeding]].

### Multi-language policies via Multilang — per-site copies

Policies use the same data model as regular storefront pages. **When [[apps-multilang]] is active and configured to translate pages, each sister site holds its own per-language policy record** — the merchant can edit them independently or auto-translate from the master. Without Multilang, there is one policy per store; the merchant must embed multiple language versions in the same body or rely on the storefront's built-in language switcher.

## Related

- [[apps-gdpr-policy]] — hub.
- [[apps-gdpr-policy-editor]] — the edit modal; why there is no separate handle/version field.
- [[apps-gdpr-policy-seeding]] — how the seeded Cookie Policy page is created.
- [[apps-gdpr-acceptance]] — acceptance log that stores the content snapshots.
- [[apps-gdpr-cookies]] — cookie definitions surfaced by `{cookies_table}`.
- [[apps-multilang]] — per-site language copies of policy pages.

## Open questions

None.
