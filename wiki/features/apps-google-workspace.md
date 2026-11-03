---
type: feature
nav_path: "Apps → Google Workspace"
route_name: apps.google_workspace.settings
route_path: /admin/apps/google_workspace
aliases: ["Google Workspace", "G Suite", "Google for Business"]
tags: [apps, google, email, workspace, marketing-only]
plan_gates: []
created: 2026-05-22
updated: 2026-05-28
source_count: 4
---
# Google Workspace

## Purpose

The **Google Workspace** app in CloudCart is a **marketing landing page / lead-gen** — it advertises Google Workspace subscriptions (resold via CloudOffice) and links the merchant to `cloudoffice.bg/pricing` to sign up. It is **NOT** an actual email integration: there is no OAuth, no SMTP routing, no token storage, no sender configuration.

To actually route the store's outbound email through Google's mail servers, the merchant subscribes to Workspace separately and configures [[apps-smtp]] with Gmail's SMTP credentials.

## Where to find it

Sidebar → Apps → install → **Google Workspace**.

## What the merchant can do here

- Browse the marketing layout describing Workspace plans (Business Starter / Standard / Plus).
- Click the **Get started Google Workspace** button — opens `https://cloudoffice.bg/pricing/` in a new tab.

There are no form fields and no save endpoint.

### What the merchant CANNOT do here
- Connect a Google account via OAuth — the integration does not implement OAuth.
- Set sender address, display name, SMTP credentials, or DKIM/SPF settings — none of those exist here.
- Use this app to actually send store emails — install does nothing functional.

## Settings & fields

The Manager exposes only `appInfo` (App Store metadata) plus install/uninstall. There are no saveable settings.

## Business rules

### Marketing-only app

The app's only behaviour is to render the promo page and record install/uninstall. Installing has no functional effect on email routing.

### For real Workspace-routed email, use SMTP

Merchants who want Workspace-routed transactional email:
1. Subscribe to Google Workspace separately (via CloudOffice or directly).
2. Configure [[apps-smtp]] with `smtp.gmail.com` credentials.

### Permission

Standard apps permission scope.

## Related

- [[apps]] — App Store.
- [[apps-google-connect]] — OAuth foundation.
- [[apps-smtp]] — alternative SMTP-based custom email sending.
- [[settings-domains]] — sender domain DNS configuration.
- [[marketing-campaigns]] — campaign emails (different system, may also benefit from Workspace setup).

## How it works (verified against backend)

### The app is a marketing landing page — not an actual email integration

The `google_workspace` app inside CloudCart is a **promotional / upsell page** that markets Google Workspace plans (Business Starter, Business Standard, Business Plus) and points the merchant to `cloudoffice.bg/pricing` to sign up. The integration only exposes basic app info; the install / uninstall actions plus an index view render the marketing page. There is **NO** OAuth, **NO** mailbox integration, **NO** sender configuration, and **NO** SMTP routing logic in this app.

For actually routing the store's outbound email through Workspace / Gmail, the merchant subscribes to Google Workspace separately (outside CloudCart), then configures SMTP via [[apps-smtp]] using Gmail's SMTP server credentials. CloudCart's role in this app is purely lead-gen to CloudOffice's Workspace reselling.

### Send-as, DNS, rate limits — handled outside CloudCart

Because the app doesn't actually send email, configuration like multiple sender addresses (`support@`, `orders@`), SPF/DKIM/DMARC DNS records, and Google Workspace's daily sending limits are entirely managed by the merchant inside Google's Workspace Admin console — none of these are exposed in CloudCart. The store's transactional emails continue to go through CloudCart's default sending (or through a separately configured [[apps-smtp]]).

### Vue page is a static promo landing pointing to cloudoffice.bg/pricing

The Vue settings component renders a marketing layout (hero image, plan cards "Business Starter / Standard / Plus / Enterprise") with a single CTA linking to `https://cloudoffice.bg/pricing/`. There are no form fields. The merchant cannot configure anything from inside CloudCart — clicking the CTA opens an external CloudOffice signup flow.

### Install / uninstall flow only

The backend routes expose just `install` and `uninstall` actions — no settings endpoint, no OAuth endpoint. Installing the app is equivalent to "I'm interested in Google Workspace" — CloudCart records the install but does nothing else. There is no token storage, no email routing, no integration whatsoever.

### Wiki advice: do NOT promise OAuth/sender features in this app

Verified: the wiki's earlier mentions of "OAuth via Google Connect" and "Set sender address / display name" for this app are NOT backed by code. Those features simply do not exist in CloudCart's Google Workspace app. Merchants who want Google-routed transactional email must:
1. Subscribe to Google Workspace separately (via CloudOffice or directly with Google).
2. Configure [[apps-smtp]] with Gmail's SMTP server credentials (`smtp.gmail.com`).

### Marketing-page structure (full UI inventory)

The Vue Settings page is a static promotional layout, NOT a settings form. Top to bottom:

1. **Hero block** — animated GIF of "Workspace" + headline *"How teams of all sizes connect, create, and collaborate."* + subhead.
2. **Four feature blocks** in a wrapper, each with an icon image + title + 3-bullet description:
   - *"Flexible, helpful business collaboration solutions."* (Meet icon).
   - *"Real-time collaboration, wherever you are."* (Sheets icon).
   - *"Store, access and share your files in one place."* (Cloud Search icon).
   - *"Protect your business."* (security icon).
3. **Three pricing cards** under the header *"Choose the best Google Workspace edition for your business."*:
   - **Business Starter** — €5.75 / user / month annual (€6.90 flex). Bullets: Custom secure business email, 100-participant video, 30 GB cloud per user, security/management controls, 30-day free trial.
   - **Business Standard** (labeled **Most popular**, raised) — €11.50 / user / month annual (€13.80 flex). Bullets: secure email, 150-participant video + recording + noise cancellation, 2 TB pooled cloud, Shared Drives, security controls, Data Regions, 30-day trial.
   - **Business Plus** — €17.25 / user / month annual (€20.70 flex). Bullets: email + eDiscovery + retention, 500-participant video + attendance tracking, 5 TB pooled cloud, Shared Drives, enhanced security + Vault + advanced endpoint management, Data Regions, 30-day trial.
4. **Get started Google Workspace** button — external link to `https://cloudoffice.bg/pricing/` (opens in new tab). This is the ONLY interactive control on the page.
5. **Every plan includes:** strip — 13 icons (Gmail, Drive, Meet, Chat, Calendar, Sites, Keep, Docs, Sheets, Slides, Forms, Admin, Cloud Search).

No CSRF-protected form, no save endpoint, no setting fields. The page is wholly read-only marketing content.

## Open questions

(None currently outstanding for this page.)
