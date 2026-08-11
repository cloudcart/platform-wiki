---
type: feature
nav_path: "Marketing"
route_name: marketing
route_path: /admin/marketing-new
aliases: ["Marketing", "Marketing suite", "Маркетинг", "Маркетингова сюита"]
tags: [marketing, hub, navigation]
plan_gates: []
created: 2026-05-21
updated: 2026-05-28
source_count: 2
---
# Marketing

## Purpose

Top-level sidebar pillar that groups every revenue-growth tool in one place: the **Marketing Suite Dashboard** (KPIs), the outbound channels (Email, SMS, Viber, Web push), **Campaigns** (newsletter blasts and automated drip flows), **Segments**, **Subscribers**, **Discounts**, **Popup forms**, **SEO**, **Blog**, **Cross-sell / Upsell**, and the marketing apps (BumpCart, Reviews). The actual work happens inside the sub-screens; this page is the navigation hub. The sidebar icon is the bullhorn.

## Where to find it

Top-level sidebar entry **Marketing** (5th pillar after Dashboard / Orders / Products / Customers, depending on enabled apps).

Clicking the pillar opens its dropdown of sub-entries; clicking the "Marketing" label itself routes to `admin.marketing.dashboard` (the legacy marketing dashboard). The new Marketing Suite is reached via the first child link, **Marketing suite** (`/admin/marketing-new/dashboard`) — the merchant-recommended surface (see [[marketing-dashboard]]). Both dashboards are wired and reachable; the legacy one is soft-deprecated, not removed.

## What the merchant can do here

The Marketing pillar exposes the following groups of sub-screens (in this order in the sidebar dropdown):

- **Marketing suite** — KPI dashboard for everything marketing-related ([[marketing-dashboard]]).
- **Channels** — outbound delivery setup:
  - **Channels setup** — activate / configure Email, SMS (msghub, NTH Message), Viber, and Web Push channels for campaigns.
  - **Email notifications** — per-event customer email templates (welcome, order confirmation, abandoned cart, etc.); see [[marketing-omnichannel-mails-list]].
- **Campaigns** — newsletter & automation tooling:
  - **Campaigns** — list / create / start / archive campaigns, regular and automated ([[marketing-campaigns]]).
  - **Segments** — subscriber slices used as a campaign's audience ([[marketing-segments]]).
  - **Subscribers** — the marketing subscriber CRM ([[marketing-subscribers]]).
  - **Custom fields** — extra attributes attached to subscribers.
  - **Popup forms** — subscription-collection popups ([[marketing-subscribers-subscribe-forms]]).
  - **Saved templates** — re-usable email templates.
  - **Templates groups**.
  - **Predefined campaigns** — CloudCart-supplied automated starting points.
  - **Predefined email templates**.
- **SEO** — site-wide search optimisation ([[marketing-seo]]):
  - **Meta information** — per-page meta titles / descriptions ([[marketing-seo-meta]]).
  - **301 redirects** — URL change manager ([[marketing-seo-301-redirects]]).
  - **SEO spinner** — bulk meta generation tool ([[apps-seo-spinner]]).
- **Discounts** — discount / coupon / cart-rule management ([[marketing-discounts]]).
- **Buy button** — embeddable storefront module for external sites.
- **Blog** — built-in CMS for marketing content:
  - **Articles** ([[marketing-blog-articles]]).
  - **Categories** ([[marketing-blog-category]]).
  - **Comments** ([[marketing-blog-comment]]).
- **Applications** (dropdown group title):
  - **Cross Sell & UpSell** ([[marketing-cross-sell]]).
  - **Bumpcart** — checkout-page bump offers (app).
  - **CloudCart Reviews** — product review collection (shown only if the `product_review` app is installed).

## Settings & fields

Not applicable — this is a navigation hub, not a screen with its own form fields.

## Business rules

### Visibility — driven by staff permissions

The Marketing pillar is shown to a staff member whose role grants any of these permission keys: `marketing`, `marketing.*`, `marketing.discounts`, `marketing.cross_sell_upsell`, `marketing.seo`, `marketing.saleschannels`, `marketing.communications`, `marketing.messenger`, `marketing.blog_articles`, `marketing.blog_categories`, `marketing.blog_comments`. A staff member with none never sees the pillar.

Each sub-screen then has its own gate that cascades down — e.g. the **Blog** dropdown needs `marketing` / `marketing.blog_articles` / `marketing.blog_categories` / `marketing.blog_comments`; **Subscribers** needs `marketing` / `marketing.subscribers.all` / `marketing.subscribers`. So a marketing role can be narrowed to "Blog only" or "Newsletter only" by gating the deeper keys.

### Two parallel UIs — legacy vs new

Several sub-screens have BOTH a legacy version AND a new version under `/admin/marketing-new/...`. The merchant lands on the new version by default; a per-section cookie set to `old` provides an opt-back-to-legacy escape hatch — keys `marketing-campaigns`, `marketing-channels`, `marketing-discounts`, `marketing-segments`, `marketing-subscribers`. Each is toggled by the "Switch to old version" / "Try the new version" link at the top of the new page. **No persistent server-side preference** stores the choice — clearing cookies resets to the new UI.

### Anti-spam policy gates outbound marketing

Before the merchant can open the **Channels** screen, the **Saved email templates** screen, or send any campaign, they must accept the **anti-spam policy** (see [[marketing-campaigns-policy]]). It is a one-time accept that persists in the `campaigns` app's `anti_spam_policy` setting; until accepted, opening those screens redirects to `/admin/marketing-new/campaigns/policy`.

### The Marketing Suite is plan-aware

The KPI tiles and RFM analysis on the **Marketing suite** dashboard depend on the merchant's plan and on which apps / channels are installed. A merchant who hasn't activated Email/Viber/SMS channels sees an "Activate" call-to-action instead of stats in the Channel performance module; merchants on plans without RFM see a blurred-out RFM section with an upsell.

### CloudCart Reviews is conditional; Bumpcart is always shown

**CloudCart Reviews** appears in the **Applications** dropdown only when the `product_review` app is installed for the store. **Bumpcart** is always shown.

### Buy button is a single builder screen, not a saved list

The **Buy button** entry opens a snippet builder/generator, NOT a list of saved buttons. Each snippet lives only in whatever HTML the merchant pasted it into — there is no "my Buy Buttons" list and no edit-by-ID flow; re-clicking always starts a fresh session. See [[marketing-buy-button]].

### Cross-sell and Up-sell share one visual diagram editor

Both **Cross-Sell** and **UpSell** under **Applications** open the same visual diagram editor — a list row opens that record in the diagram view, not a flat form. A chain can mix both types (a Cross-Sell can have UpSell children and vice versa). See [[marketing-up-sell-diagram]].

## Related

- [[marketing-dashboard]] — the Marketing Suite landing dashboard.
- [[marketing-campaigns]] — newsletter & automation hub.
- [[marketing-campaigns-policy]] — the anti-spam policy gate.
- [[marketing-omnichannel-mails-list]] — per-event customer email templates.
- [[marketing-segments]] — subscriber slices.
- [[marketing-subscribers]] — subscriber CRM.
- [[marketing-subscribers-subscribe-forms]] — popup signup forms.
- [[marketing-discounts]] — discount manager.
- [[marketing-cross-sell]] — cross-sell / upsell offers.
- [[marketing-seo]] — SEO hub.
- [[marketing-seo-meta]] — per-page meta editor.
- [[marketing-seo-301-redirects]] — redirect manager.
- [[marketing-blog-articles]] — blog articles.
- [[marketing-blog-category]] — blog categories.
- [[marketing-blog-comment]] — blog comments.
- [[marketing-blog-tags]] — blog tags.
- [[campaign]] — Campaign entity.
- [[subscriber]] — Subscriber entity.
- [[segment]] — Segment entity.
- [[discount]] — Discount entity.
- [[channel]] — Channel entity.
- [[email-template]] — Email template entity.
- [[notification-delivery]] — the platform-wide outbound notification mechanism.
- [[discount-stacking]] — how discounts / coupons / cart-rules combine (the model behind [[marketing-discounts]]).
- [[abandoned-cart-recovery]] — the abandoned-cart detection + recovery-email mechanism driven from Campaigns.
- [[subscriber-vs-customer]] — the marketing-subscriber vs store-customer distinction behind Subscribers / Segments.
- [[seo-handling]] — the SEO mechanism behind the Marketing → SEO sub-pillar.
- [[plan-gates]] — plan-tier limits that shape what's visible inside Marketing.

## Plan gates

The Marketing hub itself is **not gated** — every plan tier sees the pillar (subject to staff permissions). The plan-feature gates live on the individual sub-screens (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Sub-screen | Plan-feature mappings |
|---|---|
| [[marketing-blog-articles]] | `blog_articles` (numeric + access), `blog_categories` |
| [[marketing-blog-category]] | `blog_categories` (numeric + access) |
| [[marketing-blog-comment]] | `blog_comments` (access) |
| [[marketing-landing-pages]] | `static_pages` (numeric), `faq_page` (access), `landing_page` (access), `storefront_builder` (access + callback) |
| [[marketing-discounts]] | `discount_global`, `discount_coupon`, `discount_fixed`, `discount_quantity`, `discount_banner`, `total_discounts`, `discount-code-pro`, `discount-code-pro-generator` |
| [[marketing-cross-sell]] | `cross_sells` (numeric) |
| [[marketing-up-sell-list]] | `upsells` (numeric) |
| [[marketing-reviews]] | `product_reviews_added_rating` (numeric, restricted by default) |
| [[marketing-omnichannel-mails-list]] | `change_email_notifications` (access), `abandoned_orders` (access for the abandoned-cart job) |

When a cap is hit or the tier is below the access threshold, the merchant is redirected to the upsell at [[plan-features]]. Numeric gates extend via packs ([[plan-vs-feature-pack]]); access gates require a plan upgrade.

## Open questions

(none)
