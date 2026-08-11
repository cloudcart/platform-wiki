---
type: feature
nav_path: "Apps → Facebook Comments"
route_name: apps.facebook_comments.overview
route_path: /admin/apps/facebook_comments
aliases: ["Facebook Comments", "FB Comments", "Facebook Comment Plugin", "Социални коментари"]
tags: [apps, facebook, comments, social, plugin]
plan_gates: ["facebook_comments"]
created: 2026-05-22
updated: 2026-05-27
source_count: 1
---
# Facebook Comments

## Purpose

**Facebook Comments** integration — embeds the **Facebook Comments Plugin** on the storefront's blog articles + product pages. Visitors comment using their Facebook account (instant social-login), comments threading through Facebook's social graph (visible to commenters' friends).

Alternative to:
- Native CloudCart blog comments ([[marketing-blog-comment]]).
- [[apps-disqus-comments]] (Disqus is the more popular alternative).

Used by merchants who:
- Want social-login frictionless commenting (no separate account creation).
- Benefit from FB's spam moderation (built into the plugin).
- Want comments to spread virally via commenters' FB feeds.

## Where to find it

Sidebar → Apps → install → **Facebook Comments**. See [[apps-facebook-comments-settings]] for configuration.

## What the merchant can do here

### Settings
- **Comments count** (required, 1-100) — how many comments to display per page before "Show more". Default likely 10. Validation messages:
  - Required: *"Please add how many comments you would like to see on your website"*.
  - Min 1: *"Please add different number from zero"*.
  - Max 100: *"Maximum comments are 100"*.
- Activate to inject the FB Comments module on storefront pages.

### What the merchant CANNOT do here
- Manage individual comments from CloudCart — moderation happens in Facebook's admin (the merchant connects the FB Comments Mod to their FB account).
- Set Facebook App ID per store (verify — typically a global App ID per CloudCart instance).
- Disable per specific page (it's storefront-wide once activated).

## Settings & fields

Manager (`Comment` class, `APP_KEY = 'facebook_comments'`):
- `appInfo` — App Store metadata.
- the configured check — checks `facebook_comments_number` setting is non-empty.

Single required setting: `facebook_comments_number` (integer 1-100).

## Business rules

### Single primary setting

The integration is intentionally minimalist — only ONE configuration field (comment count). The rest of the plugin behaviour is controlled through Facebook's plugin defaults (commenter avatars, threading depth, ordering by FB's algorithm).

### Facebook account required for commenters

Visitors comment using their FB account. Customers without an FB account can't comment (some markets where FB usage is low may find this limiting).

### Moderation via Facebook

The merchant moderates comments via Facebook's Moderation Tool (developers.facebook.com/tools/comments). CloudCart doesn't expose moderation UI.

### Cookie consent integration

The plugin sets Facebook cookies. When [[apps-gdpr-overview]] is active and the customer rejects social cookies, the plugin should NOT load. Verify the platform's loader respects consent state.

### Replaces native comments when active

When Facebook Comments is active, the storefront's blog + product comment modules render the FB plugin INSTEAD of CloudCart's native [[marketing-blog-comment]]. Existing native comments stay in DB but aren't displayed.

### Multi-language support

The integration ships translations for 6 languages: en, bg, ro, mk, el, sq (English, Bulgarian, Romanian, Macedonian, Greek, Albanian).

### Permission

Standard apps permission scope.

## Plan gates

This app is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `facebook_comments` | Access gate (install URL) | The install URL `/admin/apps/facebook_comments/install` is blocked when the plan lacks the feature. The app is hidden from the Apps catalog for those plans. |

Behaviour: lower plans cannot install the app. Existing installs continue working on plan downgrade until the merchant cancels — see [[plan-vs-feature-pack]] for downgrade rules.

## Related

- [[apps]] — App Store.
- [[apps-facebook-comments-settings]] — settings sub-page.
- [[apps-disqus-comments]] — alternative external comment platform.
- [[marketing-blog-comment]] — native comments (replaced when this app is active).
- [[apps-product-review]] — native reviews (different concept).
- [[apps-gdpr-overview]] — cookie consent integration.
- [[marketing-blog-articles]] — articles where comments may render.

## How it works (verified against backend)

### Renders on product detail pages only

Per the storefront template the theme templates, the Facebook Comments module is included only on the **product detail page**. The platform's blog templates do not include the Facebook Comments include, so blog articles continue to use the native blog-comment module (or another active comments app).

When active, the product detail page shows a tab/section "Comments" that hosts the FB plugin alongside any of the alternatives ([[apps-disqus-comments]], `yotpo`). If multiple are active, FB Comments + Disqus + Yotpo can all render in the same Comments tab.

### Module href is the product URL

The `data-href` attribute is built from the product's URL handle (e.g. `https://yourstore.com/product/<handle>`). Each product gets its own thread on Facebook's side — comments do not bleed across products.

### Default comments count is 5

If the merchant has not yet saved a value, the module falls back to **5 comments per page**. Once they save a value (1–100 integer), that value is used by Facebook's plugin as `data-numposts`. Facebook itself decides ordering (its social-relevance ranking), so when more comments exist than the count, FB chooses which to surface — CloudCart does not control "newest vs. most relevant".

### Single comment-count field is the entire configuration

There is no theming, no per-page toggle, no per-language toggle on the CloudCart side. Light/dark mode and color scheme are not exposed — they follow whatever Facebook's plugin default is. To change them, the merchant must use Facebook's own moderation/plugin tools.

### Moderation lives on Facebook

CloudCart provides no comment moderation UI for FB Comments. Merchants moderate via Facebook's Moderation Tool. There is no in-platform notification when a new FB comment is posted on a product.

### No migration path from native comments

There is no merchant-facing tool to migrate existing [[marketing-blog-comment]] entries into Facebook threads. Native comments remain in the database but are not displayed on the product page while FB Comments is active.

### Storefront i18n: 6 languages

Translation files ship for `en`, `bg`, `el`, `mk`, `ro`, `sq` (English, Bulgarian, Greek, Macedonian, Romanian, Albanian) — these only cover admin labels and validation messages. The visitor-facing UI (comment form, "Reply", "Like", timestamps) is rendered by Facebook's own plugin in whichever language Facebook detects for the visitor.

### Save controller whitelist — single field

The save controller writes exactly `facebook_comments_number` from the form. The save action runs `settingsSaveCustom` which delegates to the abstract save handler. Validation rules: required, integer, min 1, max 100. Submission errors return a JSON error with the relevant code.

### No Facebook App ID field exposed — relies on platform-wide FB integration

There is no per-store Facebook App ID setting in this module. The Facebook Comments plugin loads with whatever Facebook SDK initialization the storefront theme provides. So the merchant cannot use their OWN Facebook App for comment moderation — they rely on whatever app key the CloudCart instance is using globally.

## Open questions
