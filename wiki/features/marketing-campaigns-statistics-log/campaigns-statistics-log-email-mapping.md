---
type: feature
nav_path: "Marketing → Campaigns → Statistics → Log → Email status mapping"
route_name: admin.api.campaigns.statistics.logs
route_path: /admin/api/core/marketing/campaigns/{campaign}/statistics/{action}/logs
aliases: ["Elastic Email status mapping", "Provider status to canonical status", "Soft bounce vs hard bounce categorisation", "Suppressed NoMailbox Spam NotDelivered", "BOUNCED auto-includes HARD_BOUNCED"]
tags: [marketing, campaigns, statistics, logs, email, elastic-email]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-statistics-log]]. See the hub for the other aspects (surfaces, status values, status archive, filters & table, view-message, side-effects, storage).

# Per-send log — Email status mapping (provider → canonical)

## Purpose

CloudCart uses **Elastic Email** as the underlying Email delivery provider. Elastic Email's webhook callbacks report delivery status using its own vocabulary (`Sent`, `Opened`, `Clicked`, `Error`, etc.), which the platform translates into its canonical status enum (SENT, SEEN, CLICKED, HARD_BOUNCED, BOUNCED, etc.) before storing on the log row. This mapping is non-trivial because Elastic Email's `Error` outcome covers BOTH soft bounces AND hard bounces — the distinction is in a separate `category` field. This page documents the mapping table the platform applies, the soft-vs-hard-bounce categorisation, and the filter-expansion behaviour that makes the merchant's life easier when searching for "all bounced messages".

## Where to find it

The mapping is **internal** — the merchant doesn't see Elastic Email's raw status strings anywhere in the admin. They see only the canonical platform status (BOUNCED / HARD_BOUNCED / SEEN / etc.) on each row in the [[campaigns-statistics-log-filters-table|log table]]. This page documents the translation layer for support / debugging context.

## What the merchant can do here

There are no merchant-editable settings for the mapping. Practical merchant effects:

- **Filter by BOUNCED** in the log to surface both soft and hard bounces in one go (the filter expansion does this automatically).
- **Interpret a HARD_BOUNCED row** as Elastic Email reporting `Error` with category Suppressed / NoMailbox / Spam / NotDelivered — typically a permanently bad email address.
- **Interpret a BOUNCED row** as Elastic Email reporting `Error` with any other category (e.g., temporary mailbox-full, greylist retry, transient SMTP error) — potentially recoverable.

## Settings & fields

### Elastic Email → platform-canonical status mapping

The Email channel's status-mapping function converts Elastic Email's provider status strings into the platform's canonical statuses:

| Elastic Email | Platform status |
|---------------|-----------------|
| `Sent` | `SENT` |
| `Opened` | `SEEN` |
| `Clicked` | `CLICKED` |
| `Unsubscribed` | `UNSUBSCRIBED` |
| `Error` (no category) | `ERROR` |
| `Error` + category `Suppressed` / `NoMailbox` / `Spam` / `NotDelivered` | `HARD_BOUNCED` |
| `Error` + any other category | `BOUNCED` (soft) |
| `AbuseReport` | `ABUSE_REPORT` |
| `WaitingToRetry` | `PENDING` |
| anything else | `NOT_SENT` |

So a single "Error" outcome from Elastic Email can land as either `BOUNCED` or `HARD_BOUNCED` depending on the failure category — the platform's bounce categorisation is finer-grained than the provider's status names suggest.

### Filter expansion — "Bounced" auto-includes "Hard Bounced"

In the [[campaigns-statistics-log-filters-table|log filter bar]], the Status multi-select has a `BOUNCED` option. When the merchant selects it, the underlying query expands to:

```
WHERE status IN ('BOUNCED', 'HARD_BOUNCED')
```

Soft AND hard bounces are returned together. The merchant doesn't have to know the distinction — selecting "Bounced" surfaces every email that failed delivery for either reason. There's no separate "Hard Bounced" filter option in the UI.

## Business rules

- **`Error` category drives the soft / hard split.** Elastic Email reports `status='Error'` for every delivery failure, then includes a `category` field carrying the failure class. The platform's mapping inspects `category`:
  - `Suppressed` — Elastic Email's internal suppression list blocked this send (the address has bounced for other senders too). **Hard bounce.**
  - `NoMailbox` — the recipient's mailbox doesn't exist. **Hard bounce.**
  - `Spam` — the recipient's server flagged the message as spam. **Hard bounce.**
  - `NotDelivered` — the provider gave up after retries. **Hard bounce.**
  - Anything else (e.g., `MailboxFull`, `GreylistRetry`, transient SMTP errors) → **soft bounce** (BOUNCED).
- **`Sent` does NOT mean delivered.** Elastic Email's `Sent` only confirms the platform handed off; the recipient's MX hasn't yet acknowledged receipt. The follow-up webhook with `Delivered` (mapping to DELIVERED) is what confirms inbox arrival. (verify Elastic Email's exact terminology — some providers conflate "sent" and "delivered".)
- **`Opened` → `SEEN`** is the tracking-pixel signal. Elastic Email reports `Opened` when the embedded tracking pixel in the email body loads. This is rough — image blockers, plain-text viewers, and pre-fetch caches all distort the signal. The platform stores it verbatim as SEEN.
- **`Clicked` → `CLICKED`** is the provider's own click-tracking signal, NOT the storefront-side `CampaignTrack` middleware. The provider rewrites links in outgoing email to route through its tracking domain; when the recipient clicks, the provider's tracking domain fires the webhook → SEEN / CLICKED mapping → status update. The storefront-side middleware additionally fires when the click eventually lands on the merchant's storefront (see [[campaigns-statistics-log-side-effects]]). So a single click can trigger TWO updates — provider-side first, storefront-side second — but the late-Sent idempotency rule (see [[campaigns-statistics-log-status-archive]]) prevents either from overwriting an engagement-positive state.
- **`WaitingToRetry` → `PENDING`** is Elastic Email's "queued for retry" state. The platform treats it as PENDING (no terminal decision yet); a follow-up webhook will resolve to `Sent` / `Error` / etc.
- **Unrecognised provider statuses fall to `NOT_SENT`.** Any string Elastic Email sends that doesn't match the above maps to NOT_SENT — a conservative default. The merchant sees these as "platform decided not to send", but they actually represent provider-side states the platform doesn't recognise.
- **The mapping is Email-channel-specific.** SMS (MsgHub, NTH) and Viber and Web Push each have their own provider-status → canonical-status mappings. This page covers Email only — see the per-channel pages for the others.

## How it works

When Elastic Email's webhook fires (POSTing the status callback to the platform's webhook endpoint), the channel-specific handler reads the provider `status` field (and `category` if present). It calls the channel's `statusMapping($providerStatus, $category)` function, which runs through the mapping table above and returns one of the canonical platform statuses.

The returned canonical status is then assigned to the log row's `status` field. The model boot hook handles appending to `status_archive` automatically (see [[campaigns-statistics-log-status-archive]]). Side-effects on the subscriber's channel (auto-bounce, auto-unsubscribe, auto-verify) fire from the same code path — see [[campaigns-statistics-log-side-effects]].

The category-driven soft / hard bounce split happens inside the mapping function via a simple set membership check: `if (category in {Suppressed, NoMailbox, Spam, NotDelivered}) → HARD_BOUNCED, else → BOUNCED`.

The "Bounced auto-includes Hard Bounced" filter expansion happens at the **query-build** layer of the log list, NOT at status-write time. The status field is stored as the precise BOUNCED or HARD_BOUNCED canonical value; only the filter UI displays them under a single label.

## Related

- [[marketing-campaigns-statistics-log]] — hub.
- [[campaigns-statistics-log-status-values]] — the canonical platform statuses this mapping targets.
- [[campaigns-statistics-log-status-archive]] — how each mapped status is appended to the history.
- [[campaigns-statistics-log-side-effects]] — what fires when a status becomes HARD_BOUNCED / ABUSE_REPORT / ERROR.
- [[campaigns-statistics-log-filters-table]] — where the BOUNCED filter expansion is exposed.
- [[marketing-channels-email]] — Email channel hub; broader Elastic Email integration.

## Open questions

- Verify Elastic Email's `Sent` semantics — does it confirm inbox delivery or only provider hand-off?
- Confirm whether the mapping has been updated since Elastic Email introduced newer category names.
