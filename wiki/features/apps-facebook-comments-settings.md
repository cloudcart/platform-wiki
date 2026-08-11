---
type: feature
nav_path: "Apps → Facebook Comments → Settings"
route_name: apps.facebook_comments.settings
route_path: /admin/apps/facebook_comments/settings
aliases: ["Facebook Comments Settings", "FB Comments config"]
tags: [apps, facebook, comments, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-05-26
source_count: 1
---
# Facebook Comments → Settings

## Purpose

The **Settings** tab is where the merchant configures the **comment count + activation** for the Facebook Comments module on storefront pages. See [[apps-facebook-comments]] for the full feature set.

## Where to find it

Sidebar → Apps → Facebook Comments → **Settings tab**. Route: `/admin/apps/facebook_comments/settings`.

## What the merchant can do here

### Configuration

| Field | Validation | Notes |
|---|---|---|
| **Comments count** (`facebook_comments_number`) | Required, integer, min 1, max 100 | How many comments to display per page before "Show more". |

Validation messages (per [[apps-facebook-comments]] the platform code):
- Required: *"Please add how many comments you would like to see on your website"*.
- Min 1: *"Please add different number from zero"*.
- Max 100: *"Maximum comments are 100"*.

### Save behaviour

The save action calls `settingsSaveCustom` (per the controller). On success, the storefront's Facebook Comments module re-renders with the new count.

### What the merchant CANNOT do here
- Change Facebook App ID (typically platform-wide).
- Configure individual comment moderation — handled in Facebook's Moderation Tool.
- Set per-page count (single store-wide value).

## Settings & fields

Per [[apps-facebook-comments]] Manager the configured check check: `facebook_comments_number` must be non-empty.

## Business rules

### Single configuration field

The Facebook Comments integration is intentionally minimal — only the comment count is configurable. The rest is controlled via Facebook's plugin defaults + their Moderation Tool.

### Permission
Standard apps permission scope.

## Related

- [[apps-facebook-comments]] — hub.
- [[apps-disqus-comments]] — alternative external comments platform.
- [[marketing-blog-comment]] — native comments (replaced when Facebook Comments is active).

## How it works (verified against backend)

### No theming controls in CloudCart

The Settings page exposes only the comment count and the on/off switch. There is no light/dark mode toggle, no color picker, no font selector — the storefront module renders with Facebook's plugin defaults. To customise the look, the merchant must use Facebook's Comments Plugin configurator.

### No per-page toggle

The merchant cannot choose to display FB Comments only on the blog or only on product pages. Per the storefront templates, the module is wired into the product detail page only; activating the app turns it on everywhere it is wired in. Blog articles continue to use the native [[marketing-blog-comment]] flow.

### Comment ordering is not configurable

CloudCart only passes `data-numposts` (count) to the Facebook plugin. Ordering (most recent vs. most relevant) is decided by Facebook's plugin and follows whatever ranking they currently default to. Merchants who need a specific order must configure it in Facebook's tooling, not in CloudCart.

### Save endpoint accepts exactly one field

The controller's `$only` whitelist is `['facebook_comments_number']` — anything else in the submission is discarded. So third-party automation that tries to set other Facebook-related fields (App ID, secret) will silently fail. Validation enforces integer, min 1, max 100.

## Open questions
