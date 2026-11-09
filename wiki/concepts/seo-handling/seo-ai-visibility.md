---
type: concept
nav_path: "Concept → SEO handling → Crawlers, AI assistants and verification"
aliases: ["AI visibility", "ChatGPT visibility", "GPTBot", "ClaudeBot", "PerplexityBot", "Block AI bots", "Bing Webmaster Tools", "Bing verification", "msvalidate", "ChatGPT product feed", "Microsoft Merchant Center", "CAPTCHA", "reCAPTCHA", "Core Web Vitals", "Page speed", "Staging store", "AI трафик", "Видимост в AI"]
tags: [seo, ai, crawlers, robots, verification, feeds, captcha, performance, concepts]
plan_gates: []
created: 2026-11-09
updated: 2026-11-09
source_count: 1
---

> Part of [[seo-handling]]. See the hub for related aspects (sitemap / robots, structured data, Search Console).

# SEO — crawlers, AI assistants and search-engine verification

## Definition

What a CloudCart store offers search engines and AI assistants, and what the merchant can control: per-bot robots.txt rules, llms.txt, how the storefront treats crawlers, verification with Bing, AI shopping feeds, CAPTCHA and page speed. Read from the code on `origin/master`, not run in a store.

## Scope

Covered: what the store's own code does. Not covered: rules of Google, Bing, OpenAI or other assistants, and the security layer in front of the store (bot challenges, blocks), which is outside the store's code and is checked per store by support.

## Contrasts

- **robots.txt vs blocking.** robots.txt is a request that well-behaved bots follow; the store's code does not block any bot by name.
- **llms.txt vs robots.txt.** llms.txt describes the store to AI assistants; it allows or blocks nothing ([[marketing-seo-llms]]).

## Where it applies

### Allowing or blocking specific bots

The robots.txt body on [[marketing-seo-robots]] is served as typed, so the merchant can write a group per bot, e.g. `User-agent: GPTBot` followed by `Disallow: /`. The platform then appends its own `Disallow` lines (checkout, cart, wishlist), `Crawl-Delay: 3` and, when the store serves an llms.txt, an `Llms:` line with its address ([[seo-robots-served-file]]). Because those lines come last, they belong to the last `User-agent` group in the merchant's text (verify how each crawler reads it). Changes show within 5 minutes. Trial, expired and development stores serve `Disallow: /` instead ([[seo-plan-overrides]]).

### How the storefront treats crawlers

The storefront recognises crawlers by their user agent (a standard crawler list, plus some uptime and speed-test tools). For them:

- `/search` answers 403 with `X-Robots-Tag: noindex`;
- the cart page and the order-return page answer 404, and cart actions 403;
- product, category and other catalogue pages are served normally, from the full-page cache.

Separately, the load balancer gives each known bot a request budget ([[platform-rate-limits]]), and the security layer in front of the store can challenge or block traffic. Neither is a merchant setting.

### CAPTCHA for shoppers

The store's code uses invisible Google reCAPTCHA v3 on two forms only: the contact form and the "notify me when back in stock" form. Sign-in, registration, checkout and reviews have none, and the merchant has no CAPTCHA setting. A challenge page a visitor sees on other pages comes from the security layer in front of the store, not from the storefront.

### Verifying the store with search engines

- **Google Search Console** — the native app adds its verification tag ([[apps-google-search-console]]).
- **Bing Webmaster Tools** — no native field. The merchant pastes Bing's `msvalidate.01` meta tag into [[design-custom-assets]], which is output in the `<head>` of every page. Uploading a verification file to the site root is not possible: the store serves no merchant files at the root. DNS verification depends on where the domain's DNS is hosted, and importing from Search Console is Bing's own feature.
- Both take the sitemap at `/sitemap.xml` ([[marketing-seo-sitemap]]).

### AI shopping and product feeds

There is no OpenAI / ChatGPT product feed, no agentic or instant-checkout integration, and no Microsoft Merchant Center, Bing Shopping or Perplexity feed in the code. The product feeds available are the XML Feed templates ([[apps-xml-feed]]): Google, Facebook, TikTok, Criteo, Skroutz, Glami, eMAG and the other marketplaces listed there. Whether another service accepts one of them (for example the Google-format feed) is that service's rule.

Analytics groups visits arriving from ChatGPT, Perplexity, Claude, Gemini, Copilot and Meta AI under a traffic source labelled **AI traffic**.

### Page speed and Core Web Vitals

What the platform does:

- images are served from the store's own image address, resized to the size the theme asks for;
- guests and crawlers get pages from a full-page cache;
- banners carry width and aspect-ratio and lazy-load (even at the top of the page); listing images lazy-load by script;
- the main product or banner image gets no preload hint, and the theme's core script loads before the page renders.

What the merchant controls: the theme, image sizes uploaded, the number of banners and sliders, and every script added through [[design-custom-assets]] or tracking apps. A storefront built on Nitrogen is the route to a fully custom, speed-tuned front end ([[nitrogen-vs-themes]]).

### Testing changes before publishing

There is no theme copy, draft theme or staging store. A theme can be previewed only on its public demo, and theme-editor changes go live on save ([[design-themes]]). Nitrogen storefronts have preview deployments ([[nitrogen-deployments]]).

### A paid SEO service

No SEO service is defined in the platform's code. Paid services live in the billing catalogue, so whether one exists and its price are checked there (verify). [[apps-seo-spinner]] generates meta titles and descriptions; it is an app, not a service.

## Related

- [[seo-handling]] — hub.
- [[seo-structured-data]] — what structured data the storefront outputs, and image alt text.
- [[seo-search-console-indexing]] — the Page indexing report.
- [[marketing-seo-robots]] / [[seo-robots-served-file]] — robots.txt editor and served file.
- [[marketing-seo-llms]] — llms.txt.
- [[design-custom-assets]] — head code, verification tags.
- [[apps-xml-feed]] — product feeds.

## Open Questions

- Whether a paid SEO service exists in the billing catalogue, and its price.
