---
type: entity
aliases: ["Subscribe form eligibility", "Subscribe form visibility", "When a subscribe form shows", "Popup display rules", "Subscribe form GDPR cookie gate", "Subscribe form dismissal cookie", "Видимост на форма за абонамент"]
tags: [marketing, customers, gdpr, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Subscribe Form — Eligibility & visibility

> Part of [[subscriber-form]]. See the hub for the other aspects (model, submission, lifecycle).

## Identity

**Eligibility** is the set of conditions the storefront evaluates to decide whether a given [[subscriber-form|Subscribe Form]] is shown to the current visitor on the current page-load. It is the single most common source of "my popup isn't appearing" support tickets — a form can be perfectly built and Active yet still be suppressed by the GDPR cookie gate, a per-visitor dismissal cookie, or the already-subscribed rule. This aspect documents the fetch-time filter chain (popup mode), the embedded-mode shortcut, and the two GDPR-related fields whose semantics trip merchants up.

## Aliases

- **Subscribe form eligibility** / **Subscribe form visibility** — the show/hide decision.
- **When a subscribe form shows** — the merchant's phrasing.
- **Popup display rules** — the popup-mode filter chain.
- **Subscribe form GDPR cookie gate** / **Subscribe form dismissal cookie** — the two suppression mechanisms.
- **Видимост на форма за абонамент** — Bulgarian.

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Display for all** (`displayForAll`) | Show even to already-subscribed visitors | Boolean (default false). When false, identified subscribers don't see the popup. When true, every page-load can render it. |
| **Cookies consent** (`cookies_consent`) | **Inverted semantic.** | Boolean. When `true`, the form is treated as already-handling consent and is shown regardless of the GDPR `targeting` cookie group. When `false` (or null = unset, the default), the form is suppressed until the visitor accepts the `targeting` cookie group (see [[apps-gdpr-cookies]]). The storefront filter keeps only `cookies_consent = true OR null` while `targeting` is unaccepted. |
| **Dismissal cookie** (`popup-subscription-displayed_<form-id>`) | (auto, set by the visitor) | Browser cookie written `= false` when the visitor closes the popup; subsequent fetches exclude that form id. See below. |
| **`includedUrls[]` / `excludedUrls[]`** | URL allow / block lists | Stored under `pages.form`; restrict the form to (or away from) specific storefront URLs. |

## Eligibility filters at fetch time (popup mode)

A popup-mode form (`embedded = false`) is included in the bulk `GET /subscribers/forms/` fetch only if ALL hold:

1. `site_id = current store` (multi-tenant).
2. `active = true` AND `draft != true`.
3. `type = 'form'`.
4. `embedded != true` (`false` or `null`).
5. If the visitor is identified (already a known subscriber): `displayForAll = true`. Anonymous visitors get all eligible forms regardless.
6. If GDPR `targeting` cookie group has NOT been accepted: only forms with `cookies_consent = false` (or null) are returned.
7. No `popup-subscription-displayed_<form-id> = 'false'` cookie is set for that form (dismissal cookie).
8. Hard cap of **5 results**.

> Note the inverted semantic in filter 6: a form left at the **default** `cookies_consent = null`/`false` is the one that is **suppressed** until the visitor accepts the `targeting` cookie group. To show a form before cookie consent, the merchant must explicitly set `cookies_consent = true`.

## Embedded-mode shortcut

For embedded mode (`embedded = true`), the single-fetch `GET /subscribers/forms/embed/<id>` applies only conditions 1, 2, 3, the explicit `_id = <requested id>`, and `embedded = true`. The `displayForAll`, `cookies_consent`, and dismissal-cookie checks are evaluated **client-side AFTER the fetch** (to decide whether to actually render), not as a server-side filter. So an embedded form is always returned to its own snippet; the module JS then decides whether to paint it.

## Per-visitor dismissal via cookies

The module JS writes `popup-subscription-displayed_<form-id> = false` to the browser cookies when the visitor dismisses the popup. The storefront fetch then excludes that form id on subsequent page-loads (filter 7 above). This is per-form and per-browser — clearing cookies or switching browsers re-arms the popup. There is **no server-side rate limit / captcha** on form submissions; the only "anti-spam" is this dismissal cookie plus channel-identifier uniqueness (the same email maps to one [[subscriber|Subscriber]] row, so duplicate submissions update the existing row rather than creating duplicates — see [[subscriber-form-submission]]).

## CORS for storefront calls

All public `/subscribers/forms/*` endpoints carry CORS middleware, because:

- The embed JSONP (`CcForm_<id>`) works cross-origin.
- The module script runs cross-origin when forms are embedded on third-party pages (rare but supported).

## Where it appears

- [[marketing-subscribers-subscribe-forms]] — where `displayForAll`, `cookies_consent`, and URL include/exclude lists are configured.
- [[apps-gdpr-cookies]] — the `targeting` cookie group whose acceptance gates `cookies_consent = false`/null forms.
- [[marketing-subscribers]] — destination of subscribers who get past the eligibility gate and submit.

## Related

- [[subscriber-form]] — hub.
- [[apps-gdpr-cookies]] — the `targeting` cookie-group gate.
- [[subscriber]] — the audience record a shown form ultimately creates.
- [[marketing-subscribers-subscribe-forms]] — the admin builder screen.

## Open Questions

None.
