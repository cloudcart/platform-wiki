---
type: feature
nav_path: "Apps → Disqus Comments"
route_name: apps.disqus_comments.settings
route_path: /admin/apps/disqus_comments
aliases: ["Disqus", "Disqus Comments", "Disqus module", "enable disable button", "app active toggle"]
tags: [apps, marketing, comments, blog, community]
plan_gates: ["disqus_comments"]
created: 2026-05-22
updated: 2026-08-06
source_count: 2
---
# Disqus Comments

## Purpose

**Disqus Comments** integration — adds the Disqus comment module to the storefront's blog articles + product pages. Disqus is a hosted commenting platform with built-in spam filtering, social-login (Facebook / Twitter / Google), threaded replies, and moderation tools.

Alternative to CloudCart's native blog-comments feature ([[marketing-blog-comment]]). Used by merchants who:
- Want richer commenting UX (threaded replies, voting, social login).
- Already manage other sites via Disqus (consolidated moderation queue).
- Don't want to manage spam moderation themselves (Disqus auto-filters).

> **Has an on/off control.** The app screen carries an **Enable / Disable** button, so the merchant can switch it off without uninstalling it. A disabled app stops working while keeping its settings — so *"the app is disabled"* IS a valid explanation to check here.

## Where to find it

Sidebar → Apps → install → **Disqus Comments**.

This integration has a **single page** — the settings page IS the only screen. There is no separate Overview tab; the router exposes one route `apps.disqus_comments.settings` mapped to the Settings Vue component.

## What the merchant can do here

- Configure Disqus shortname (the unique identifier from the merchant's Disqus account, e.g., `merchant-store`).
- Activate to inject the Disqus module on storefront comment-enabled pages.

### What the merchant CANNOT do here
- Manage comments from CloudCart — Disqus's moderation happens at disqus.com.
- Migrate existing CloudCart native comments to Disqus automatically — manual export/import would be needed.

## Settings & fields

Manager exposes:
- the configured check — verifies the Disqus shortname is set.

The shortname format is the merchant's Disqus site identifier (lowercase, hyphen-separated). Configured via settings.

## Business rules

### Replaces native comments

When Disqus is active, the storefront's blog articles + product detail pages render the Disqus module INSTEAD of CloudCart's native comments. Existing native comments stay in the database but aren't displayed.

### Disqus account required

The merchant must register a Disqus site first (free for low-traffic stores; paid for ads-free / branded). The shortname comes from there.

### Moderation external

All comment management (moderation, banning, deletion) happens in Disqus's admin at disqus.com — NOT in CloudCart.

### Permission

Standard apps permission scope.

## Plan gates

This app is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `disqus_comments` | Access gate (install URL) | The install URL `/admin/apps/disqus_comments/install` is blocked when the plan lacks the feature. The app is hidden from the Apps catalog for those plans. |

Behaviour: lower plans cannot install the app. Existing installs continue working on plan downgrade until the merchant cancels — see [[plan-vs-feature-pack]] for downgrade rules.

## Related

- [[apps]] — App Store.
- [[marketing-blog-articles]] — articles where comments may render.
- [[marketing-blog-comment]] — native comments (disabled when Disqus is active).
- [[settings-cart]] — verify if there's a per-page enable / disable.

## How it works (verified against backend)

### Single required setting: the Disqus admin URL

The merchant pastes their **Disqus admin URL** (e.g. `https://mystore-disqus.disqus.com/`) into the single configuration field. The controller validates the URL against the regex `~https?:\/\/([^/]*)\.disqus\.com\/?~i` and extracts the shortname automatically (the `mystore-disqus` portion). Both the original URL (`url_help`) and the extracted shortname (`url`) are stored.

Validation messages:
- *"Please, add link from Disqus"* — if URL is missing or fails URL validator.
- *"Please, add valid link from Disqus"* — if the regex does not match (URL must end in `.disqus.com`).

The merchant must therefore have a Disqus site already created at disqus.com before activating the app.

### Renders only on product detail pages

The Disqus include the theme templates is wired into the product detail page comments tab — alongside (or instead of) [[apps-facebook-comments]] and `yotpo`. Blog articles continue to use the native [[marketing-blog-comment]] flow; activating Disqus does **not** route blog comments through Disqus.

### Each product is a unique Disqus thread

The module sets `page.url` to the product's full storefront URL and `page.identifier` to `md5('cloudcart' + product.id)`. So each product is a stable, distinct thread on Disqus, and renaming the product (URL change) does not split the thread — Disqus keys off the MD5 identifier.

### No comment-count on listing pages

CloudCart only embeds the full Disqus thread on the product detail page. There is no integration that pulls Disqus's comment counter onto product listing or category pages — visitors see comment counts only when they reach the product page.

### No SSO with the storefront

CloudCart only stores the shortname. It does not store a Disqus secret key, and there is no SSO-payload signing in the embed snippet. Visitors who comment must log into Disqus (or use Disqus's social sign-in providers) — being logged into the CloudCart storefront does not auto-authenticate them on Disqus.

### No migration tool for native comments

There is no merchant-facing tool to import existing native [[marketing-blog-comment]] entries into Disqus. The native comments remain in the database but are not displayed while Disqus is active on a page that supports both.

### No CloudCart-side moderation

All moderation, banning, deletion, and spam handling happen at disqus.com. CloudCart does not provide an admin view of Disqus comments and does not send notifications when a new Disqus comment is posted.

### Two-field storage — both URL and extracted shortname saved

The controller stores BOTH the raw URL (`url_help`) and the regex-extracted shortname (`url`) atomically in a DB transaction. The shortname is what the storefront module uses for `data-disqus-shortname`. The full URL is kept for the merchant to verify what they pasted. The same transaction also writes the `active` flag.

### Configured check uses the URL field, not the extracted shortname

The `isConfigured` method checks `url_help` (the raw URL the merchant pasted), not the extracted `url` (shortname). So if the regex extraction failed but the URL field is non-empty, the app reports as configured even though the storefront module won't have a valid shortname. The regex enforces `.disqus.com` ending, so this edge case is rare but possible.

### Validation enforces the disqus.com domain

The `url_help` field has 3 validations: `required_if:active=1` (only required when the merchant tries to activate), `url` (valid URL format), and a regex requiring `.disqus.com` somewhere in the host. A merchant trying to point at a custom domain or self-hosted Disqus alternative is rejected.

### Validation message duplication — "url" rule vs "regex" rule

Both `url_help.url` and `url_help.required_if` show "Please, add link from Disqus" but `url_help.regex` shows "Please, add VALID link from Disqus". So the merchant gets a slightly different message depending on whether they left it empty, pasted non-URL gibberish, or pasted a URL that's not on.disqus.com.

## Open questions
