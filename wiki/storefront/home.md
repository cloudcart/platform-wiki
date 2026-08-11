---
type: storefront-page
route_name: site.home
route_path: /
themes_using: [all]
tags: [storefront, home, landing, customisation, modules]
created: 2026-06-08
updated: 2026-06-08
source_count: 3
---

# Storefront — Home page

## Purpose

The home page is the storefront's landing surface — the URL a customer hits when they type the shop's domain with no path. It is the single most merchant-customisable page in CloudCart: almost every visible block (hero carousel, free-text panels, featured-products showcase, featured-categories showcase, featured-brands showcase, banners) is rendered conditionally based on the theme's named module instances, and each instance can be turned on or off, re-ordered, and re-skinned from the admin's [[design-modules]] screen.

Because the home page is shipped by the theme, every theme decides for itself which blocks the home actually carries — `home/home.tpl` in the base `flair` theme is the canonical example; child themes (e.g., `flair-bmw`, `flair-electronicstore`) override it to rearrange or extend the block set.

## URL & route

- **Route name**: `site.home`
- **Route path**: `/`
- **Controller**: the home controller, the request handler
- **Middleware**: `CustomHomePage` (intercepts requests that have a custom home set), `uuid_generate`, `subscriber_uuid`, `TSStatistic:home`

The route also detects the `Paysera Bot` user agent and returns a Paysera-site-verification response instead of the storefront — invisible to humans.

## How it loads

1. The home controller runs the platform code. If the merchant has set a static page as the custom home (via [[marketing-landing-pages]]), the request is delegated to the page controller and rendered as a builder/page surface; the rest of this document does **not** apply in that case.
2. Otherwise, the controller returns the platform code — Smarty resolves that to `themes/<active-theme>/templates/home/home.tpl` (falling back to the theme templates if the theme has not overridden it — see [[storefront-architecture]]).
3. The template calls `$module->utilities->homeRedirect` first (some merchants force a redirect to a different URL on the home — usually used to redirect `/` to a campaign page) and `$module->setSeo("utilities")` to emit SEO meta.
4. Each home block is wrapped in an `{if $module-><name>->isEnabled}` guard so disabled module instances render nothing.

## What the customer sees

The base `flair` home (in order) renders:

1. **Carousel / slider** (hero) — the theme templates, driven by the `carousel` module instance.
2. **Text block 1** (`homeText1`) — a free-text panel above the showcases.
3. **Featured products showcase** (`showcaseProducts`) — either a slider (`productShowcaseSlider.tpl`) or a grid (`productShowcase.tpl`) depending on the module's `enable_slider` setting. Image srcset is `300x300` desktop, `600x600` mobile.
4. **Featured categories showcase** (`showcaseCategory`) — grid or slider of category cards.
5. **Text block 2** (`homeText2`).
6. **Featured brands / vendors showcase** (`showcaseBrand`) — grid or slider of vendor logos.
7. **Home banners** (`banners`) — the theme templates, a rectangular promo banner row.

Blocks that the merchant disables in [[design-modules]] simply drop out — the template renders no placeholder.

## Storefront behaviour

- The hero carousel auto-rotates if the merchant enabled auto-play; the rotation interval is a module setting.
- Showcase rows scroll horizontally on mobile via Slick / Owl carousel JS (the exact library depends on the theme).
- Product tiles inside a showcase carry the same `js-add-to-cart`, `js-add-to-wishlist`, `js-quick-view` hooks as on [[products-list]]; see [[product-detail]] for the click-to-buy flow.
- Carousel and banner clicks navigate via plain `<a href>` — there is no AJAX on the home for navigation.
- The home does NOT call `/ajax/*` endpoints in its base form — the page is fully server-rendered on first paint. Themes that add an AJAX "recently viewed" strip do call `/ajax/latest-viewed` (route name `latest.viewed.ajax`) (verify per theme).

## JavaScript behaviour

Home-specific hooks (from the `flair` base theme template):

- No `.js-*` hooks live in `home.tpl` itself — the home delegates entirely to module templates included from `modules/extra/*.tpl` and `modules/product/*.tpl`.
- Carousel uses whichever slider library the theme bundles (Slick is the most common, but another custom theme and `motion` use Swiper) (verify per theme).
- The product-tile hooks (`js-add-to-cart`, `js-quick-view`, `js-add-to-wishlist`) trigger the standard cart-drawer events documented under [[storefront-cart]].

## Customisations available to the merchant

| Block | Admin screen | Module instance name |
|-------|--------------|----------------------|
| Hero carousel | [[design-modules]] → Slider group | `carousel` |
| Text block 1 (above showcases) | [[design-modules]] → Text fields group | `homeText1` |
| Featured products | [[design-modules]] → Products group | `showcaseProducts` |
| Featured categories | [[design-modules]] → Categories group | `showcaseCategory` |
| Text block 2 (below first showcase) | [[design-modules]] → Text fields group | `homeText2` |
| Featured brands | [[design-modules]] → Vendors group | `showcaseBrand` |
| Home banners | [[design-modules]] → Images group | `banners` |
| SEO title / description | [[marketing-seo-meta]] (page-level home SEO) | n/a (`$module->setSeo("utilities")`) |
| Replace whole home with a custom landing page | [[marketing-landing-pages]] (set page as home) | n/a (`CustomHomePage` middleware kicks in) |
| Theme variables (colours, fonts, button styles) | [[design-theme-editor]] | n/a (via theme.css) |
| Inject custom JS / CSS | [[design-custom-assets]] | n/a |

## Theme variations

- All themes register a `home.home` view; whether they actually have a `home/home.tpl` of their own determines whether the merchant gets the theme-specific block layout. Themes that don't override `home/home.tpl` fall back to the theme templates (if present) — see [[storefront-architecture]].
- Child themes (`flair-bmw`, `flair-electronicstore`, `flair-clothesforyou`, `flair-religiousandceremonial`, `flair-diel`, `flair-camerasandoptics`) inherit the `flair` home structure and customise via theme.css overrides; their module catalogue is identical (verify).
- The `wonderland`, `properties`, and `jobs` themes use radically different home layouts (real-estate listings, job postings) — the module set in [[design-modules]] reflects this.
- See [[storefront-themes-catalog]] for the full catalogue.

## Known issues / by-design vs bug

- **By design**: the order of blocks in `home/home.tpl` is hard-coded in the template — the merchant cannot drag-and-drop reorder them via [[design-modules]]. To reorder, the merchant must either build a custom landing page with [[marketing-landing-pages]] and set it as the home, or hire a developer to fork the theme.
- **By design**: if every module on the home is disabled, the customer sees an empty `<div class="_content">` between header and footer — no warning is rendered.
- **By design**: the `Paysera Bot` user agent is short-circuited to a payment-gateway verification handshake — this is a one-time check Paysera runs when the merchant activates the Paysera integration, not a permanent override.
- See [[storefront-known-issues]] for cross-page bugs.

## Related

- [[storefront-architecture]] — request lifecycle and theme rendering.
- [[storefront-themes-catalog]] — full list of themes shipping a custom home.
- [[design-modules]] — the screen the merchant uses to configure each home block.
- [[design-theme-editor]] — colours / fonts / global look.
- [[design-custom-assets]] — custom JS / CSS injection.
- [[marketing-landing-pages]] — replace the home with a custom page-builder page.
- [[marketing-seo-meta]] — home SEO meta tags.
- [[products-list]] — full catalogue listing.
- [[storefront-category]] — single category landing.
- [[storefront-cart]] — cart drawer surfaced from product-tile add-to-cart.
- [[storefront-known-issues]] — cross-storefront issue register.

## Open questions

- The base `flair` `home/home.tpl` does not include a "recently viewed" strip out of the box — is that always a child-theme override, or does some shared partial inject it? (`/ajax/latest-viewed` exists as a route.)
- When the merchant sets a custom home page via [[marketing-landing-pages]], does the `TSStatistic:home` middleware still record the hit as a home view, or does the page controller switch the channel?
- What is the contractual list of module instance names the platform guarantees every theme exposes on the home? (The base set above is observed in `flair`, but a definitive contract list could not be found.)
