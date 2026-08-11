---
type: feature
nav_path: "Marketing → Campaigns → Policy → Redirect"
route_name: campaigns-policy
route_path: /admin/marketing-new/campaigns/policy
aliases: ["Policy redirect", "Anti spam policy redirect preservation", "Policy open-redirect protection", "Post-accept redirect", "Policy redirect param", "Policy hash param"]
tags: [marketing, campaigns, policy, compliance, anti-spam, security]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Policy — redirect & open-redirect protection

> Part of [[marketing-campaigns-policy]]. See the hub for the other aspects (overview, page UI, enforcement, acceptance log, versioning).

## Purpose

This page documents **how the merchant's original destination is preserved** when they're bounced to the policy page, and the **open-redirect guard** that prevents the post-accept redirect from being tampered to point outside the campaigns admin area.

## Where to find it

Invisible to the merchant — it determines where they land after clicking Accept on `/admin/marketing-new/campaigns/policy` (see [[campaigns-policy-page-ui]]).

## What the merchant can do here

Nothing interactive. The merchant simply ends up on the screen they were originally trying to reach (or the campaigns landing / dashboard) after accepting.

## Settings & fields

Two query parameters carry the destination:

- **`redirect`** — a route NAME (e.g. `campaigns-channels`), set by the Vue router guard.
- **`hash`** — an encrypted blob of the original full URL, set by the legacy / Smarty backend middleware.

## Business rules

### Redirect preservation

When the merchant is bounced to the policy page, the original URL they were trying to reach is preserved in two ways depending on the path that triggered the redirect:

- **Legacy / Smarty flows** — the backend middleware `encrypt($request->fullUrl)` and passes the encrypted blob as `?hash=`; it's decrypted on accept and used as the post-accept redirect.
- **Vue flows** — the router guard passes `?redirect=campaigns-channels` (a route name); it's resolved to that route after accept.

On accept, the client reads the `redirect` route name; if present AND different from the current route name (so it can't loop back onto `campaigns-policy`), the merchant is navigated there; otherwise they're sent to `dashboard`.

### Open-redirect protection (verified against backend)

The backend Accept handler validates the post-accept redirect URL with a **strict prefix match** — `str_starts_with($redirect, site_url. '/admin/campaigns/')`. Anything outside this prefix (a tampered `redirect` pointing to an external site or a non-campaigns admin area) is replaced with `route('campaigns')` (the Campaigns list landing). The check runs **both** on GET render (decrypting the `hash` query param) AND on POST submit (validating the form's `redirect` hidden field). This is the platform's open-redirect guard.

### Encryption uses the app key (verified against backend)

The `?hash=` blob is encrypted with the application framework's app key, so a tampered `hash` value fails to decrypt and falls back to `route('campaigns')` (campaigns landing). The decrypted URL is then prefix-validated as above.

### Validation key uses the legacy path prefix (verified against backend)

The prefix check uses `'/admin/campaigns/'` (the legacy path), **not** `/admin/marketing-new/campaigns/`. Vue-router redirects honour the legacy URL as the validation key because the backend was wired before the marketing-new route prefix existed; the actual landing-page redirect still resolves to the modern Vue route via `route('campaigns')`.

## Related

- [[marketing-campaigns-policy]] — hub.
- [[campaigns-policy-page-ui]] — the Accept handler that consumes the `redirect` value.
- [[campaigns-policy-enforcement]] — the middleware / router guard that sets `redirect` / `hash`.
- [[marketing-campaigns]] — the `route('campaigns')` landing the guard falls back to.

## Open questions

No outstanding questions.
