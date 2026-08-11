---
type: storefront-page
route_name: private-page
route_path: /private-page/{slug}
themes_using: [all]
tags: [storefront, cms, membership, gated-content]
created: 2026-06-08
updated: 2026-06-08
source_count: 3
---

# Private (membership-gated) page (storefront)

## Purpose

Same content type as a standard [[page]], but reachable only to logged-in customers with an active membership. Used for sales documentation, partner portals, paid downloads, member-only guides, etc. The distinct URL prefix `/private-page/` keeps the content out of search engines.

## URL & route

- **Route name:** `private-page`
- **Path:** `/private-page/{slug}`
- **Method:** `GET`.
- **Requires the Membership app installed** — the platform code is checked before any content is rendered.

## How it loads

1. Route resolves to the request handler.
2. **Auth check** — if no customer is logged in, a `before_page` cookie (24-hour lifetime) is set with the requested slug and the customer is redirected to `/login`. After login, the framework sends them back to the page.
3. **Lookup** — the page record is fetched by slug; missing → `404`.
4. **Membership gate** — both must be true:
   - The Membership app is installed.
   - `page->private == 'yes'`.
   Otherwise → `404` (deliberately, to avoid leaking the page's existence to non-members).
5. **Access check** — `checkAccess` looks up the `MembershipModel` for `(customer_id, page_id)`. Access is granted when an unexpired membership row exists. No row → HTTP `402 Payment Required` with the message `sf.page.no_access_msg`.
6. **Old-slug redirect** — the platform code handles 301s for renamed slugs.
7. **Type dispatch** — `builder` → `preview`; `landing` → raw HTML body; anything else → standard `page/page.tpl` render (`type = faq` works the same as in [[page-faq]]).
8. Inactive pages (`active != yes`) raise a not-found error with `sf.page.err.page_no_longer_active`.

## What the customer sees

- After login + membership check: identical visual layout to a regular [[page]] — breadcrumb, `<h1>`, rich-text body (or FAQ accordion / builder canvas, depending on type).
- Without login: bounced to `/login` (and returned after authentication).
- With login but no membership: `402` error page (themes typically show "Access denied — purchase a membership").

## Storefront behaviour

- **Login redirect cookie:** `before_page` (1 440 min ≈ 24 hours) — the framework uses it to bounce the customer back to the originally requested slug after a successful login.
- **AJAX render path:** if the request is AJAX, the controller returns a JSON envelope `{ status: success, html, dependency: { js, css } }` so a SPA-style overlay can pop the content without a full reload.
- **No SEO indexing** — the URL prefix `/private-page/` is deliberately different from `/page/` and is typically `Disallow`-ed in `robots.txt` (verify the storefront-shipped robots).
- **301 redirects** — renaming a private-page slug preserves backlinks via the platform code.

## JavaScript behaviour

- No private-page-specific JS hooks.
- The AJAX-render envelope assumes the calling overlay knows how to inject `html` + `dependency.js/css` into the DOM.

## Customisations available to the merchant

- **Mark a page private** — set `private = yes` on the page record (admin UI under Content / Pages — verify exact field label).
- **Grant access** — issue a `Membership` row per `(customer_id, page_id)` via the [[apps-membership]] app. Memberships can be unlimited or have an `expired` timestamp.
- **Pricing / paywall** — the page itself does not collect payment; the merchant ties membership grants to product purchases / subscriptions configured under [[apps-membership]].
- **Content type** — `standard`, `faq`, `builder`, `landing` all supported, same as a public [[page]].

## Theme variations

- Identical rendering pipeline to [[page]]; theme differences are limited to the styling of the `402` access-denied page (when shown).

## Known issues / by-design vs bug

- If the Membership app is uninstalled, every `/private-page/*` URL starts returning `404` — by design, not a bug.
- A page flipped from `private = yes` back to `private = no` becomes a `404` on `/private-page/{slug}`; the merchant must re-link customers to `/page/{slug}` instead.
- The `before_page` cookie is a single value — visiting multiple private pages while logged out and then logging in only returns the customer to the last requested page.
- A customer with an expired membership receives `402` rather than `403` — clients consuming the API/HTML should treat both as "denied".

## Related

- [[page]]
- [[page-faq]]
- [[apps-membership]]
- [[storefront-architecture]]
- [[storefront-known-issues]]

## Open questions

- Confirm whether `robots.txt` ships with `Disallow: /private-page/` out of the box.
- Confirm the admin field name that flips `private` on/off (verify exact label).
- Confirm whether the `402` response is themed per active theme or rendered from a shared error template.
