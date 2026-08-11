---
type: feature
nav_path: "Marketing → Channels → Channels setup → Email → Reputation & suspend"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Email channel reputation", "Email auto-suspend", "SUSPENDED_SPAM", "SUSPENDED_BOUNCED", "SUSPENDED_OPEN", "suspend recovery", "manual_allowed_suspended", "Reputation impact email"]
tags: [marketing, channels, email, reputation, suspend, deliverability]
plan_gates: ["campaign.channel.email"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-channels-email]]. See the hub for the other aspects (setup wizard, DNS records, Elastic Email sub-account, webhook feedback, send pipeline, settings pane).

# Email channel — Reputation thresholds & auto-suspend

## Purpose

The platform polls the merchant's Elastic Email sub-account for reputation metrics (`abusepercent`, `unknownuserspercent`, `openedpercent`, `clickedpercent`, `reputation`) on every reputation read. Three hard-coded thresholds map directly to three of the four auto-suspend triggers shared by all marketing channels. When any threshold trips, the Email channel auto-suspends with the matching reason (`spam` / `bounced` / `open`) and stops sending until support clears the suspension. A reputation reading ≥ 99 is exempt from auto-suspension regardless of any one threshold being briefly crossed.

## Where to find it

- The live values are displayed in the **Reputation** panel on the Email channel card. They come from Elastic Email's `Account.LoadReputationImpact`.
- The four cross-channel triggers (with `OUT_OF_FUNDS` being the fourth, non-reputation one) are documented on [[marketing-channels#The four auto-suspend triggers]].

## What the merchant can do here

- View live **spam%** / **bounce%** / **open%** / **click%** / **reputation%** values.
- (No self-service unsuspend.) Once auto-suspended, contact support to clear the `suspended_by` flag or set `manual_allowed_suspended`.

## Settings & fields

### Hard-coded thresholds (`EmailChannelManager`)

| Constant | Value | What it does |
|---|---|---|
| `API_URL` | `https://api.elasticemail.com/v2/` | Elastic Email API base URL — every reputation pull goes here. |
| `SUSPENDED_SPAM` | `0.5` | Spam-complaint percentage above which the channel auto-suspends with reason `spam`. |
| `SUSPENDED_BOUNCED` | `5` | Hard-bounce / unknown-user percentage above which the channel auto-suspends with reason `bounced`. |
| `SUSPENDED_OPEN` | `5` | Open-rate percentage **below** which the channel auto-suspends with reason `open`. |

These are read by the abstract `suspendedByReputation` check that runs against each reputation pull from Elastic Email.

### Reputation keys (from Elastic Email)

The reputation check pulls these keys back from Elastic Email and maps them directly to the three triggers:

| Elastic Email key | Maps to threshold | Trigger reason |
|---|---|---|
| `abusepercent` | `SUSPENDED_SPAM` | `spam` |
| `unknownuserspercent` | `SUSPENDED_BOUNCED` | `bounced` |
| `openedpercent` | `SUSPENDED_OPEN` (floor) | `open` |
| `clickedpercent` | (displayed only — not a trigger) | — |
| `reputation` | The ≥ 99 exemption | (exempt) |

### Suspend-related settings

| Setting | Value type | Effect |
|---|---|---|
| `suspended_by` | Array of reasons (`spam` / `bounced` / `open` / `OUT_OF_FUNDS`) | Each entry blocks sending; cleared by support when reputation recovers. |
| `manual_allowed_suspended` | Future-dated expiry | Support-granted override allowing sends during a suspension window. Persists across **Reset configuration** (see [[email-channel-elastic-email-account]]). |

## Business rules

### Reputation ≥ 99 is the global exemption

A reputation reading ≥ **99** is exempt from auto-suspension regardless of any one threshold being briefly crossed. This protects long-running healthy sender from a single bad campaign window — a merchant whose long-term reputation is excellent gets a one-shot tolerance before any of the three triggers fires.

### Spam complaints feed `SUSPENDED_SPAM` via two paths

The `abusepercent` value at Elastic Email is itself driven by Elastic Email's bounce + complaint feedback loop — AbuseReport events arriving at the [[email-channel-webhook-feedback|delivery webhook]] are forwarded to Elastic Email's reputation accounting. So a sudden spike in spam complaints causes both: (a) the per-subscriber side-effects on the webhook (subscriber marked rejecting marketing, removed from the campaign with `key = 'abuse'`), and (b) the eventual auto-suspend once `abusepercent > 0.5`.

### Hard-bounces feed `SUSPENDED_BOUNCED` via the error-category map

The `unknownuserspercent` value is driven by hard-bounce events from the webhook. The error-category map (see [[email-channel-webhook-feedback]]) decides which Error events count as HARD_BOUNCED — `Suppressed`, `NoMailbox`, `Spam`, `NotDelivered` all increment hard-bounce. Once `unknownuserspercent > 5`, the channel auto-suspends with reason `bounced`.

### Open-rate floor protects against list rot

Unlike the other two, `SUSPENDED_OPEN` is a **floor** — the channel auto-suspends when `openedpercent < 5`. This catches list rot: a merchant who keeps sending to an unengaged list will see open rates collapse, signalling that the IPs / domain risk being blacklisted by inbox providers.

### No merchant-self-service unsuspend

After an auto-suspend by spam / bounce / open thresholds, the merchant fixes the underlying problem — deletes bounced and unsubscribed subscribers, sends a re-engagement campaign to the active half, improves content quality, etc. — and then needs CloudCart support to clear the `suspended_by` flag. Currently there's **no merchant-self-service "I fixed it, unsuspend me" button**. The merchant contacts support to:

- Set `manual_allowed_suspended` with a future-dated expiry, OR
- Remove the `suspended_by` array entry once reputation recovers.

`manual_allowed_suspended` persists across **Reset configuration** (see [[email-channel-elastic-email-account]]) — so a support-granted override does not get wiped by accident.

### The three reasons share the same code path; only the reason string differs

All three reasons (`spam` / `bounced` / `open`) write the same `suspended_by` array entry shape — the `reason` string is the only differentiator. This means the suspend-recovery workflow is identical regardless of which trigger fired.

## Related

- [[marketing-channels-email]] — hub.
- [[marketing-channels]] — multi-channel framework + the four auto-suspend triggers (the fourth being `OUT_OF_FUNDS`, non-reputation).
- [[email-channel-webhook-feedback]] — AbuseReport + hard-bounce events that feed the reputation metrics.
- [[email-channel-elastic-email-account]] — `manual_allowed_suspended` persists across Reset configuration; reputation is read using the sub-account's API key.
- [[email-channel-send-pipeline]] — channel must not be auto-suspended for the send pipeline to run.
- [[marketing-campaigns-policy]] — anti-spam policy.

## Open questions

None.
