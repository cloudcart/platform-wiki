---
type: feature
nav_path: "Nitrogen → Storefronts → Create Storefront → Connect GitHub"
route_name: nitrogen.storefront.create
route_path: /admin/nitrogen/create
aliases: ["Connect GitHub for Nitrogen", "Nitrogen GitHub App", "Nitrogen GitHub OAuth", "github=connected return signal"]
tags: [nitrogen, storefronts, create, wizard, github, oauth, owner-only]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---
# Nitrogen → Create Storefront — GitHub connection

> Part of [[nitrogen-create-storefront]]. See the hub for the other aspects (setup, repository selection, provisioning).

## Purpose

When the merchant picks the **GitHub** deployment method on the setup step ([[nitrogen-create-storefront-setup]]) and clicks **Next**, the wizard must confirm the admin has a connected GitHub account before showing the repository picker. This aspect covers that connectivity check, the OAuth + GitHub App-install round-trip, how the typed storefront name survives the off-domain hop, the `?github=connected` return signal, disconnecting/switching accounts, and the auto-redo when the connection has silently broken.

## Where to find it

This logic runs on the same setup route (`nitrogen.storefront.create`, `/admin/nitrogen/create`) and on the repository route (`nitrogen.storefront.select-repo`, `/admin/nitrogen/create/repository`), which renders the **GitHub Account Card** at the top.

## What the merchant can do here

- **Authorise GitHub** — get redirected through GitHub's OAuth + App-install screens, then bounced back into the wizard.
- **See the connected account** — avatar + GitHub username + green "Connected" badge + sub-line "Connected via GitHub App".
- **Open Permissions** — a link (only on `sm:` and up) to `https://github.com/settings/installations` in a new tab.
- **Disconnect** — a ghost button that revokes the linkage; the merchant must re-authorise from scratch to reconnect.

## Settings & fields

This step has no merchant-entered fields — it is a connection gate. The relevant controls are on the GitHub Account Card (shown on the repository route):

| Control | What it does |
|---------|--------------|
| **Permissions** link | Opens `https://github.com/settings/installations` (manage which repos the App can access). `sm:` breakpoint and up only. |
| **Disconnect** (ghost) | POSTs `/admin/api/core/nitrogen/github/disconnect`; on success shows toast *"GitHub account disconnected"* and routes back to `nitrogen.storefront.create`. |

The GitHub API surface used at this step:

- `GET /admin/api/core/nitrogen/github/status` → `{ connected: boolean, username, avatar }`.
- `GET /admin/api/core/nitrogen/github/connect` → `{ url }` (the OAuth URL).
- `POST /admin/api/core/nitrogen/github/disconnect`.

## Business rules

### Connectivity check decides the next route

When the merchant clicks **Next** on the GitHub path, the wizard GETs `/admin/api/core/nitrogen/github/status`. If `connected === true`, it router-pushes to `nitrogen.storefront.select-repo` ([[nitrogen-create-storefront-repository]]). If not connected, it GETs `/admin/api/core/nitrogen/github/connect`, receives `{ url }`, and sets `window.location.href = url` to send the merchant through the GitHub OAuth / App-install flow.

### Storefront name persists through OAuth via sessionStorage

Before the OAuth redirect, the trimmed name is written to `sessionStorage.nitrogen_create_name`. On return, the repository page reads it back and shows *"Setting up repository for **{storefrontName}**"*. This survives the off-domain GitHub round-trip without any server-side state.

### `?github=connected` is the OAuth-return signal

GitHub bounces the merchant back to `/admin/nitrogen/create?github=connected`. The create page detects `github === 'connected'` (via the route query or URL search params) and immediately `router.replace`s to the repository page — so the merchant lands directly on the repo step instead of seeing step 1 flash again.

### GitHub-App-based, not personal access tokens

The integration uses the **CloudCart Nitrogen GitHub App** (installable per GitHub account / org). The merchant authorises the App via OAuth + App-install; CloudCart stores the installation token. Disconnecting revokes the installation linkage — re-authorising from scratch is required to reconnect.

### Repo-loading failure auto-redoes the OAuth flow

If loading repositories later throws (typically because the App installation was revoked or the token expired), the wizard auto-disconnects, re-saves the storefront name in sessionStorage, and re-routes through `/admin/api/core/nitrogen/github/connect`. The merchant does not see a "GitHub broken" error — they see the re-authorisation page. The repository-load mechanics are detailed on [[nitrogen-create-storefront-repository]].

### Owner-only

GitHub connection is part of the owner-only Create wizard (the pillar's `isOwner` group). Moderators cannot reach it. See the hub [[nitrogen-create-storefront]] and [[nitrogen]] for the pillar-wide rule; there is no delegation row in [[settings-staff]].

## Related

- [[nitrogen-create-storefront]] — hub.
- [[nitrogen-create-storefront-setup]] — the prior step that picks the GitHub method.
- [[nitrogen-create-storefront-repository]] — the step reached after a successful connection.
- [[nitrogen]] — pillar-wide owner-only rule.
- [[settings-staff]] — staff roles (no delegation row for this owner-only wizard).

## Open questions

_None._
