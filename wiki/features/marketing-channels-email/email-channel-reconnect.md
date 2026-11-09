---
type: feature
nav_path: "Marketing → Channels → Channels setup → Email → Reconnect"
route_name: campaigns-channels
route_path: /admin/marketing/campaigns/channels
aliases: ["Reconnect", "Повторно свързване", "Email channel reconnect", "APIKey Expired", "Expired Elastic Email key", "Email campaigns not sending", "Campaign stuck executing", "Delete settings and configure", "Изтриване на настройките и конфигуриране"]
tags: [marketing, channels, email, elastic-email, reconnect, api-key, troubleshooting]
plan_gates: ["campaign.channel.email"]
created: 2026-11-09
updated: 2026-11-09
source_count: 1
---

> Part of [[marketing-channels-email]]. The account model this repairs is on [[email-channel-elastic-email-account]].

# Email channel — rejected key and Reconnect

## Purpose

Every campaign a store sends goes out through its own Elastic Email sub-account with **one API key the platform stores for the store**. When Elastic Email rejects that key, the store's campaigns, newsletters and automations stop sending **silently**, and the **Email** card offers a one-click repair, **Reconnect**. This page documents why a key gets rejected, how the failure looks to the merchant, and what Reconnect does (and what the reset next to it does instead).

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** → the **Email** card. When the store's key is rejected, the card shows two extra buttons next to Configuration / Settings / Reputation / Logs:

- **Reconnect** — *"Повторно свързване"*;
- **reset** — *"Изтриване на настройките и конфигуриране"*, with a confirmation.

In the new admin on 07.11.2026 both rendered in English inside a Bulgarian admin: *"Reconnect"* and *"Delete settings and configure"*.

## What the merchant can do here

- **Press Reconnect** — the store gets a new working key on the same sub-account; sending domain, DNS verifications and sender stay; the channel is switched back on. The first and usually the only step.
- **Reset** — only when Reconnect fails: wipes the whole Elastic Email binding and restarts the setup wizard, domain re-verification included — see [[email-channel-elastic-email-account]].
- **Re-send** — a campaign that ended without sending is not re-sent by the repair; the merchant starts it again (a copy of it, when it is no longer active).

## Settings & fields

| Control | What it does | Shown when | Notes |
|---|---|---|---|
| Reconnect | Re-issues the store's key in place. | The stored key is rejected as expired. | Success: *"Имейл каналът беше свързан отново. Изпращащият домейн и настройките остават непроменени."* Failure: *"Имейл каналът не можа да бъде свързан отново. Моля, свържете се с поддръжката."* |
| Reset | Deletes the channel's settings and credentials. | Same condition. | Destructive; keeps only the unverified-subscribers switch and a support override. |

## Business rules

### Why a key gets rejected: Elastic Email's 48-hour Default key

Elastic Email hands every new sub-account a **Default** API key that **expires 48 hours** after creation and cannot be renewed. Since late August 2026 the platform issues its own **permanent** key on the sub-account (named *"CloudCart Campaigns"*) and stores that one. A store still holding a Default key (set up or repaired before that change) stopped sending two days after setup and stays stopped until it is reconnected.

### A rejected key stops sending silently

When Elastic Email rejects the stored key ("APIKey Expired"):

- every message is dropped at hand-off: no retry, no bounce, no merchant notification;
- its log row stays **`NOT_SENT` with no reason** (see [[channels-logs-row-lifecycle]]), while *Total sent* still counts it, so the campaign shows its recipients as "sent" with zero successfully sent, and can stay "executing";
- the card keeps reading **Activated / Configured** until the next reputation sync switches the channel off without a suspend reason (see [[channels-reputation-auto-suspend]]);
- test sends keep working (they bypass the sub-account — see [[email-channel-send-pipeline]]), so a good test send proves nothing about the campaign path;
- it stops campaign mails and subscriber confirmation mails only; order notifications are unaffected (they do not use this channel — see [[marketing-channels-email]]).

### The buttons are the diagnosis

Whenever the store has a stored key — configured or not, active or not — loading the card checks that key live against Elastic Email. Only an "expired" failure adds Reconnect and the reset. So **the presence of Reconnect on the card means the store's campaigns cannot send**, whatever else the card says.

### Reconnect repairs in place

Reconnect creates a new permanent key on the **same** sub-account, checks that it authenticates, stores it, and switches the channel back on — **unless** it was suspended for reputation, which stays off ([[email-channel-suspend-thresholds]]). Repairing in place is what keeps the store sending: a sending domain belongs to exactly one sub-account and Elastic Email will not release it, so moving the store to a new sub-account would strand its domain. If the sub-account no longer exists in Elastic Email, Reconnect creates a new one under the same address.

The DNS verification step repairs the key the same way on its own: when its checks fail with "APIKey Expired", it re-issues the key and retries, so a dead key no longer shows correct DNS records as unverified.

## Related

- [[email-channel-elastic-email-account]] — the sub-account model and the reset.
- [[channels-logs-row-lifecycle]] — why the rows stay `NOT_SENT` with no reason.
- [[channels-reputation-auto-suspend]] — the sync that switches the channel off on a rejected key.
- [[email-channel-send-pipeline]] — hand-off, and why test sends don't use the sub-account.
- [[campaigns-stats-step-table]] — *Total sent* counts dispatches.
- [[marketing-channels-email]] — hub.

## Open questions

- Whether the new admin now renders the Bulgarian labels of the two buttons; describe them by both names.
