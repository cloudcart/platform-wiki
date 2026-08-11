---
type: feature
nav_path: "Apps → Request an App"
route_name: apps.requested_app.overview
route_path: /admin/apps/request/:appKey
aliases: ["Request app", "Apps request", "Requested app", "Request an integration"]
tags: [apps, request, roadmap]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 1
---
# Request an App

## Purpose

The **Request an App** view is where the platform surfaces apps that are **announced / roadmapped but not yet available**. The merchant can express interest (typically via a "Request this app" / "Notify me when available" CTA), which signals demand to the CloudCart team for prioritising the integration's actual implementation.

The `:appKey` URL parameter identifies which specific upcoming app's request view to render. Used by:
- The App Store catalog showing "Coming soon" tiles that link here.
- Direct navigation from marketing emails / blog posts announcing roadmap items.
- Search results when a merchant searches for an integration that doesn't exist yet.

## Where to find it

The route `/admin/apps/request/:appKey`. Reached through the App Store when the merchant clicks a "Coming soon" / "Request" tile.

## What the merchant can do here

- **Read** the upcoming app's planned description + capabilities.
- **Request / express interest** — typically a CTA button signals demand to CloudCart's product team.
- **Sign up for notifications** — get notified when the integration ships.

### What the merchant CANNOT do here
- Install / activate the app (it doesn't exist yet).
- See an exact ETA — the request system collects demand, not delivery commitments.

## Settings & fields

The view renders the standard `AppOverview` component customised for request scenarios:
- App description (planned).
- Capabilities list (intended).
- "Request" / "Notify me" CTA (instead of "Install").
- (Possibly) ratings + comment thread to gauge demand.

## Business rules

### Demand-signal aggregation

Each request increments a counter for the underlying app. Apps with the highest demand get prioritised by CloudCart's roadmap planning. The merchant doesn't see request counts directly (verify) — that's internal data for product prioritisation.

### Notification on launch

When the requested app eventually ships, all merchants who clicked "Notify me" are alerted (typically via email + in-admin notification).

### Distinct from Deprecated

[[apps-deprecated]] is for retired apps (past). **Request** is for upcoming apps (future). Both render via `AppOverview` but with different banners + actions.

### Permission
Standard apps permission scope.

## How it works (verified against backend)

### What the merchant signals
When the merchant clicks **Request this app**, CloudCart records:
- The app key + name they're interested in.
- Their store domain + site ID.
- The admin's name + email (so CloudCart can contact them).
- The CloudCart user / sales rep assigned to the store (`cc_user_id`).
- A timestamp.

This row is saved in the `applications_request` table and a notification is automatically sent to:
- A configured webhook (event: `app.request`).
- The assigned CloudCart user's Slack channel.

### Duplicate prevention
The merchant can only request a given app once per store per admin. If they try again, the platform returns: *"You have already requested the app."* This means: **the merchant cannot click "Request" repeatedly to inflate demand**, and there is no separate **unrequest** flow exposed to merchants.

### Request count visibility
The merchant **does not see the demand count** for an app. The request data flows to CloudCart's internal channels (webhook + Slack) for product / sales follow-up, not to the merchant UI. Other merchants' interest is not surfaced as social proof.

### Comment / feedback channel
The merchant **cannot leave a free-text comment** through the standard request flow — only the structured identification fields are captured. To explain a use case, the merchant relies on the follow-up email / Slack conversation initiated by their CloudCart contact after the request is submitted.

### ETA communication
Roadmap dates are not displayed on the request view. CloudCart's product / sales team contacts the merchant directly when the requested integration becomes available — typically via the email / Slack channel where the request was originally relayed.

### Duplicate check is per (app, site, admin) triple — different admins can re-request
The duplicate prevention checks `(app_id, site_id, admin_id)` — so if the same store has multiple admin accounts, EACH admin can submit ONE request for the same app independently. This means a merchant with 3 admin accounts can register 3 requests for the same upcoming integration (signalling stronger demand from CloudCart's perspective).

### App name in request is the English translation
When the request is created, the app name stored on the request row is the **English-locale translation** of the application name (the platform code), not the merchant's current admin language. This ensures CloudCart staff see consistent app names in Slack notifications regardless of the merchant's locale.

### Request row fields persisted
Each successful request writes these fields to the `applications_request` table: `app_id`, `app_key`, `app_name` (English), `site_id`, `user_id` (store owner), `admin_id` (requesting admin), `admin_name`, `admin_mail`, `domain` (site URL), `cc_user_id` (assigned CloudCart sales rep), and `created_at`. No `updated_at` field — requests are write-once.

### Generic error response on validation failure
The controller catches all exceptions and returns `{ message: 'An error occurred while processing your request.' }` with HTTP 422. So merchants don't see the underlying error (e.g., missing English translation for the app, or app key not found). The merchant has to contact support to debug.

## Related

- [[apps]] — App Store hub.
- [[apps-deprecated]] — sister view for retired apps (past).
- [[settings-admin-notifications]] — "App available" notification setup.

## Open questions

_None — all questions answered above._
