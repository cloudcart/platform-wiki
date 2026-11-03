---
type: feature
nav_path: "Apps → Private Store → Settings"
route_name: apps.private-store.settings
route_path: /admin/apps/private-store/settings
aliases: ["Private Store Settings", "B2B store config", "Login-required mode config"]
tags: [apps, administration, private-store, b2b, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-05-26
source_count: 1
---
# Private Store → Settings

## Purpose

The **Settings** tab is where the merchant configures the **redirect page for unauthenticated visitors** + access-approval policy. See [[apps-private-store]] for the full feature set.

## Where to find it

Sidebar → Apps → Private Store → **Settings tab**. Route: `/admin/apps/private-store/settings`.

## What the merchant can do here

### Redirect page configuration

| Field | Notes |
|---|---|
| **Redirect destination** | Where unauthenticated visitors land. Options: |
| - **Login page** (default) | Standard sign-in. |
| - **Custom landing / marketing page** | Pre-login informational page (e.g., "Apply for access"). |
| - **Account-creation page** | Sign-up. |
| - **External URL** | Redirect away from CloudCart. |

Per [[apps-private-store]] Manager: `getRedirectPage` returns the configured destination (cached for 1 hour).

### Access approval policy

| Setting | Notes |
|---|---|
| **Auto-approve registrations** | Anyone can sign up + access (just friction). |
| **Manual approval** | Merchant reviews each registration before granting access (true B2B gating). |
| **Per-group default access** | Which customer group new users land in. |
| **Approval notification** | Email merchant when registration pends. |

### What the merchant CANNOT do here
- Make parts of the catalog public — Private Store is all-or-nothing.
- Skip the redirect step (visitors must land somewhere).
- Allow guest checkout — Private Store requires login by definition.

## Settings & fields

Per [[apps-private-store]]: cached `getRedirectPage` returns the destination.

## Business rules

### 1-hour cache on redirect page

The redirect destination is cached for 1 hour to avoid hitting settings storage on every request. Changes may take up to 1 hour to fully propagate.

### Permission
Standard apps permission scope.

## Related

- [[apps-private-store]] — hub.
- [[customers]] — gated customer base.
- [[customers-custom-groups]] — groups for access tiering.
- [[apps-membership]] — sister storefront-mode for paid membership.

## How it works (verified against backend)

### The exact settings persisted by this page

Clicking Save on this tab writes these specific keys to the app's settings table:

| Setting key | Purpose |
|---|---|
| `active` | Master active/inactive flag. |
| `require_registration` | Boolean — when ON, the `UserAccessRestrict` middleware enforces login on the protected route list. |
| `registration_approving` | Boolean — when ON, new registrations get `active=0` and need merchant approval before they can log in. |
| `page_redirect` | The Page ID where unauthenticated visitors are redirected (only saved when `registration_approving` is ON in the form, per the controller logic). |
| `allow_pages` | Toggle: whether to allow specific public Pages to bypass the login wall. |
| `allow_blog` | Toggle: whether to keep the blog publicly visible. |
| `allow_pages_ids` | Array of Page IDs the merchant has selected to whitelist for public access. |

The Page-id-based whitelist is the key control: for a B2B catalog that still needs a public About / Contact / Privacy page, the merchant selects those pages here. They're stored as IDs and translated at request time to URL patterns checked by the access middleware — per [[apps-private-store]].

### Public-pages and blog whitelists answer "exempt URLs"

The merchant CAN keep specific URLs public:
- Individual Pages (Privacy Policy, About Us, Contact) via `allow_pages_ids`.
- The entire blog via `allow_blog`.

The middleware's `$allowed_routes` list (per [[apps-private-store]]) is the universe of routes that GET gated; routes not in that list (login, register, account, GDPR forms, etc.) are always public so customers can actually log in.

### No customisable approval-email template at this page

Per the controller: the settings only persist on/off toggles and IDs. There is NO field for "approval email body" or "rejection email body" on this page — because the platform doesn't send approval emails (see [[apps-private-store]]). To notify customers when their account is approved, the merchant would need to use a workflow rule ([[apps-workflow]]) or send manual emails.

### `page_redirect` only persisted when `registration_approving` is ON
Per the controller logic, the `page_redirect` setting (which Page to redirect unauthenticated visitors to) is only saved when `registration_approving = 1` is also being saved. Switching off approval-mode silently clears the redirect-page choice on the next save. The merchant who wants a custom landing page must keep registration-approval ON.

### `allow_pages_ids` is an array of integer Page IDs
The whitelist is stored as a serialized array of integer IDs — the merchant adds whole Pages, not URLs or regex patterns. To whitelist a URL that's not a CMS Page (e.g., a marketplace listing), the merchant would have to convert it into a Page first.

## Open questions

