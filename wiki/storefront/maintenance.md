---
type: storefront-page
route_name: (handled by the store resolver middleware)
route_path: (any storefront URL when site.maintenance is true)
themes_using: [all]
tags: [storefront, maintenance, downtime, admin]
created: 2026-06-08
updated: 2026-06-08
source_count: 3
---

# Maintenance mode (storefront)

## Purpose

When the merchant flips the store into maintenance, every public storefront URL renders a standalone "we'll be right back" page instead of the catalog. The admin panel and login flow stay reachable so the merchant can continue working.

## URL & route

- **Route:** none — maintenance is enforced by middleware on every storefront request.
- **Triggered by:** the platform code. When the site model's `maintenance` flag is true, the middleware throws the platform code.
- **Response:** the exception handler renders `exceptions.404` with the message `sf.module.global.nfy.site_in_maintenance` and HTTP `200`, plus two distinguishing headers:
  - `Retry-After: 3600`
  - `x-maintenance: true`

## How it loads

1. Every storefront request hits the platform code.
2. If `$site->maintenance` is true, `SiteMaintenance` is thrown and caught by the platform code.
3. The handler renders the view `exceptions.404` with `message = __('sf.module.global.nfy.site_in_maintenance')`. The same view is reused for the standalone "site not available" splash.
4. The view is a complete `<html>` document — NO header/footer/menu. It includes:
   - `<title>` of the store (`config('site_name')`).
   - Google fonts (when `google_fonts_info` is set).
   - The shared `helper_content.css` stylesheet.
   - A centred message block (`.back-soon` / `.back-image` / `.back-content`) rendering `{$message nofilter}`.
5. Per-theme `templates/notifications/maintenance.tpl` files exist and most contain only `{__('sf.module.global.nfy.site_in_maintenance')}` — used by storefront modules that want to render an inline "site in maintenance" message rather than the full splash (verify exact callers).
6. Admin / login URLs do NOT go through the platform code in the same way (they live under separate route prefixes), so the merchant can still reach the back office.

## What the customer sees

- A standalone branded splash (no header, no footer, no menu).
- Site name in the `<title>` and visually as the heading.
- A single short message: "The site is currently under maintenance" (or the merchant's translation of `sf.module.global.nfy.site_in_maintenance`).
- No countdown timer in the shipped template (verify whether any theme has added one).
- HTTP status is `200` (NOT `503`), which is intentional but worth noting — crawlers will treat this as a normal page during downtime. The `x-maintenance: true` and `Retry-After: 3600` headers are the machine-readable signals.

## Storefront behaviour

- **Catch-all** — every storefront URL (home, category, product, checkout, blog, etc.) renders the maintenance splash for as long as the flag is on.
- **Admin reachable** — the merchant can still log into the back office and turn maintenance back off.
- **Headers** — `x-maintenance: true` is a useful health-check / CDN signal; `Retry-After: 3600` tells well-behaved bots to come back in an hour.
- **No modules** — because the response is a standalone HTML document, none of the storefront modules (cart, search, navigation) execute during maintenance — keeps the splash cheap and reliable even when an underlying module is the reason the merchant flipped the switch.

## JavaScript behaviour

- None — the splash ships zero JavaScript.
- Per-theme `notifications/maintenance.tpl` files have no JS either; they are message-only.

## Customisations available to the merchant

- **Toggle maintenance on/off** — in admin, under [[settings-general]] (verify exact field label and section — typically a "Maintenance mode" toggle in the general / store settings panel).
- **Customise the splash copy** — by overriding the translation key `sf.module.global.nfy.site_in_maintenance` for the active locale.
- **Branding** — `config('site_name')` drives the title; the rest of the splash is hard-coded to the shared `helper_content.css`. Deeper branding requires overriding the theme templates in a custom theme (rare).
- **Whitelisting IPs / preview** — verify whether the platform supports an admin-IP bypass; the middleware itself does not expose one in the snippet above.

## Theme variations

- The maintenance splash is theme-INVARIANT — it always comes from the theme templates.
- Each theme additionally ships a `templates/notifications/maintenance.tpl` partial (one-liner with the same translation key) that is included by certain modules that need an inline "maintenance" notice (verify exact usage).

## Known issues / by-design vs bug

- The response status is `200`, not `503` — this is intentional (see the inline comment in `Exceptions/Handler.php` discussing `429`) but means SEO crawlers will index the splash as a normal page if maintenance is left on for long periods. Compensating signals are `x-maintenance: true` and `Retry-After: 3600`.
- The splash is a standalone HTML page — global storefront analytics (e.g., Google Analytics) bound to the regular layout will NOT fire during maintenance.
- Forgetting to disable maintenance after a deploy leaves the store down — the merchant should always re-check the flag.
- Per-theme `notifications/maintenance.tpl` files exist but only some module paths reference them; the canonical user-facing splash is always the global `exceptions/404.tpl`.

## Related

- [[settings-general]]
- [[storefront-error-404]]
- [[storefront-architecture]]
- [[storefront-known-issues]]

## Open questions

- Confirm the exact admin nav path + field label for the maintenance toggle (likely [[settings-general]] → Maintenance mode).
- Confirm whether the platform supports admin-IP bypass or a preview token to view the storefront during maintenance.
- Confirm which modules include `templates/notifications/maintenance.tpl` (inline message variant).
- Confirm whether any theme has extended the splash with a countdown timer or contact info.
