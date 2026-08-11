---
type: storefront-page
route_name: (catch-all)
route_path: (any unmatched URL)
themes_using: [all]
tags: [storefront, errors, 404]
created: 2026-06-08
updated: 2026-06-08
source_count: 3
---

# 404 / generic error page (storefront)

## Purpose

The fallback page rendered when no storefront route matches the requested URL, when the controller explicitly throws the platform code, or when the framework's error handler maps an HTTP exception to a status-code page. Also used for the 402/403/500 family in the same template, distinguished by `$code` and `$message`.

## URL & route

- **Route name:** none — the page is the application framework error-handler fallback.
- **Path:** any URL that does not match a registered route.
- **HTTP status:** `404` when the route is unmatched; the same template handles other HTTP errors with their own `$code` / `$message`.

## How it loads

1. the application framework's exception renderer catches the unmatched-route exception (or an explicit the platform code, `PaymentRequired`, etc.).
2. The site error handler resolves the active theme's `error.tpl`.
3. the theme templates is a one-line include of `notifications/error.tpl`.
4. `templates/notifications/error.tpl` wraps the error in the standard `header.tpl` + `footer.tpl` and branches:
   - `$type === 'http'` → renders the styled error block with `$code`, the apology copy (`sf.global.err.page.title`), the `$message` (or fallback `sf.global.err.page_not_found`), and a "Back to shop" CTA.
   - Otherwise → includes `notifications/error-include.tpl` for a generic inline notification, plus the same back-to-shop button.

## What the customer sees

- Full site chrome — header, footer, navigation — wrap the error block.
- A big `$code` (e.g. `404`).
- Apology line (`sf.global.err.page.title`).
- Either the custom `$message` (when the controller passed one) or the generic "page not found" copy.
- A primary CTA button: "Back to shop" (`sf.checkout.act.back_to_shop`) linking to `route('site.home')`.

## Storefront behaviour

- The page is rendered with the merchant's full layout, so menus, cart icon, wishlist heart, search, and footer all remain functional — customers do not get bounced out of the catalog.
- Same template handles deliberate non-found cases — e.g., an inactive category aborts with `404` and the custom message `sf.global.err.category_no_longer_exists`.
- Status code `404` is preserved on the response, so search engines correctly treat the URL as not found.
- No search box is hard-coded inside `error.tpl`; the header's search remains usable for navigation away from the error.

## JavaScript behaviour

- No error-page-specific JS hooks — only the global header/footer scripts run.

## Customisations available to the merchant

- The visible copy is driven by the translation strings `sf.global.err.page.title`, `sf.global.err.page_not_found`, and `sf.checkout.act.back_to_shop` — editable in the storefront's translation overrides (verify exact admin path).
- The "Back to shop" target is hard-coded to `route('site.home')`.
- Replacing the design requires overriding `error.tpl` or `notifications/error.tpl` in a custom theme.
- The "Suggested links" or "Search box" sections seen in some screenshots are theme-specific additions (verify which themes ship them).

## Theme variations

- Every Smarty theme includes a `templates/error.tpl` shim that delegates to its own `notifications/error.tpl`.
- Visual treatment of the `_error-page` block (typography, illustration, CTA placement) is purely CSS — some themes pin an illustration above the code, others put the number front and centre.
- Themes that customise the error page often add a search box and/or top-categories grid below the `_error-page` block.

## Known issues / by-design vs bug

- The template still loads the full layout — header and footer modules that hit external services (e.g. live menu) run on every 404. On high-bot-traffic stores this can add load.
- A controller that throws an exception with no `$message` falls back to `sf.global.err.page_not_found`; missing translations leave the raw key visible — verify the merchant's locale has it.
- The same template renders `402`, `403`, `500` etc. — distinguishing them is up to the merchant's CSS / copy customisation.

## Related

- [[storefront-architecture]]
- [[storefront-known-issues]]
- [[maintenance]]

## Open questions

- Confirm whether headless / Liquid themes share this fallback or supply their own.
- Confirm the admin nav path for editing the translation strings on the 404 page.
- Confirm which shipped themes inject a search box or suggested-links section below the `_error-page` block.
