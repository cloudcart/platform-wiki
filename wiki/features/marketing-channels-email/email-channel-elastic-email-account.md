---
type: feature
nav_path: "Marketing → Channels → Channels setup → Email → Elastic Email account"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Elastic Email sub-account", "Email channel master account", "account_token", "Reset configuration", "Email channel credentials", "Sub-account provisioning"]
tags: [marketing, channels, email, elastic-email, sub-account, credentials, reset]
plan_gates: ["campaign.channel.email"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels-email]]. See the hub for the other aspects (setup wizard, DNS records, webhook feedback, send pipeline, suspend thresholds, settings pane).

# Email channel — Elastic Email account model

## Purpose

CloudCart owns the relationship with Elastic Email centrally — merchants do **not** bring their own Elastic Email contract. The platform maintains a single **master Elastic Email account** and, when a merchant configures the Email channel, provisions a dedicated **sub-account per store**. The sub-account isolates the merchant's sender reputation, bounce list, and statistics from every other CloudCart store. This page documents the account model and the **Reset configuration** flow that wipes the sub-account binding when something goes wrong.

## Where to find it

- **Sub-account provisioning** happens transparently during Step 2 of the [[email-channel-setup-wizard]] (Domain selection). The merchant never sees their `account_token`.
- **Reset configuration** is exposed as an auto-injected button on the **Reputation** panel of the Email channel card — visible only when an `expired` error fires from a reputation check.

## What the merchant can do here

- (Transparently) Have the sub-account provisioned on first domain pick — no merchant action required.
- View live reputation / spam% / bounce% / open% / click% — values that come from the sub-account via `Account.LoadReputationImpact` (see [[email-channel-suspend-thresholds]]).
- **Reset configuration** — nuclear wipe of the entire Elastic Email binding, when prompted by an `expired` error. Confirmation prompt: *"Are you sure?"* (via `data-confirm`).

## Settings & fields

### Sub-account credentials (server-side only; merchant never sees them)

| Setting | Stored value | What it does |
|---|---|---|
| `account_email` | `{primary-host}@cloudcart.net` (or development pendant) | Sub-account email — auto-generated, NOT the merchant's own email. |
| `account_password` | 32-char random string | Sub-account password. |
| `account_token` | Elastic Email sub-account API key | Auth header on every Elastic Email API call. |

Hard-coded API base URL (`EmailChannelManager`):

| Constant | Value | What it does |
|---|---|---|
| `API_URL` | `https://api.elasticemail.com/v2/` | The Elastic Email API base — every email send and every reputation pull goes through this endpoint. |

### Reset configuration route

| Action | Route | Effect |
|---|---|---|
| Reset configuration | `campaigns.channels.channel.reset` | Wipes the credentials triple + verify / domain / configured settings. |

## Business rules

### CloudCart owns the master account; merchant pays via plan-cap

The merchant doesn't pay Elastic Email directly. CloudCart bills the merchant via the plan-cap `campaign.channel.email`. The 80%-plan-cap pre-emit fires before a campaign send if the merchant is approaching the cap — see [[email-channel-send-pipeline]].

### Sub-account email uses a host-based convention, not the merchant's email

The Elastic Email sub-account email is auto-generated as `{primary-host}@cloudcart.net`. The password is a 32-char random string. The merchant never enters either value. If a sub-account for that email already exists in CloudCart's master Elastic Email account, the platform pulls the existing API key + force-resets the password. Otherwise it creates a new sub-account in the `Campaigns` package.

### Credentials are persisted twice for recovery

The credentials triple (`account_email`, `account_password`, `account_token`) is persisted to:

1. The channel's settings (where the runtime reads them on every API call).
2. The `application_history` table with `type = 'credentials'` — durable audit log so support can recover credentials even if the channel settings are reset.

This makes the Reset action safe — the audit copy is not wiped, so support can still reconstruct the binding if needed.

### Per-store isolation of reputation and bounce list

Per-store sub-accounts mean: one merchant's bad sending behaviour does not pollute another merchant's sender reputation. The reputation thresholds in [[email-channel-suspend-thresholds]] apply per-store. The bounce / unsubscribe list is per-store.

### Reset configuration wipes selectively — two settings persist across reset

The Reset path removes all per-channel settings **EXCEPT** `unconfirmed_send` and `manual_allowed_suspended` — those persist across a reset so a merchant's send-to-unverified preference and a support-granted override don't get wiped by accident. All other settings (`account_token`, `account_email`, `account_password`, `firstName`, `domain`, `verify`, `email`, `send_email`, `configured`) are removed and the merchant restarts from Step 1 of [[email-channel-setup-wizard]].

### Reputation panel auto-injects the Reset button on `expired` errors

When `getLinks` is called and reputation is fetched, any thrown exception whose message contains "expired" (case-insensitive) injects an extra **Reset configuration** action button into the channel's `actions` set with a `data-confirm` confirmation. This is how the merchant discovers their sub-account credentials have expired — they see a clear "Reset configuration" call-to-action instead of a raw API error.

### The sender domain belongs to the merchant, not the sub-account

In contrast to the API account (CloudCart-owned), the **sender domain** must be a domain the merchant owns and has added to [[settings-domains]]. The merchant cannot send from `*.cloudcart.com` for campaigns — that would damage CloudCart's shared reputation. See [[email-channel-dns-records]] for the verify flow that proves ownership.

If the merchant adds a new domain to the store later but wants to send from it, they go back to **Edit Domain**, pick the new domain, and re-run verification. The old domain's verification stays intact in Elastic Email but the channel switches to send from the new one.

## Related

- [[marketing-channels-email]] — hub.
- [[email-channel-setup-wizard]] — provisioning happens transparently during Step 2; Reset returns the merchant to Step 1.
- [[email-channel-dns-records]] — the sender domain attached to the sub-account.
- [[email-channel-suspend-thresholds]] — reputation reads use the sub-account's API key.
- [[email-channel-send-pipeline]] — every send goes through `API_URL` with the sub-account `account_token`.
- [[settings-domains]] — sender domains are merchant-owned, attached to this sub-account.
- [[marketing-channels]] — multi-channel framework.

## Open questions

None.
