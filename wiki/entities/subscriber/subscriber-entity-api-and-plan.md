---
type: entity
nav_path: "Entity → Subscriber → API + plan"
aliases: ["Subscriber API", "JSON-API subscribers", "api-subscribers", "api-subscribers-channels", "api-subscribers-tags", "Subscribers plan cap", "subscribers plan feature", "CSV import truncation", "Segment self-limit", "planLimit", "subscriber webhook events"]
tags: [entity, marketing, subscribers, api, plan-gates, webhooks]
plan_gates: ["subscribers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[subscriber]]. See the hub for the other aspects (attributes, channels, lifecycle, consent rules, relationships).

# Subscriber — API & plan limits

## Identity

How the [[subscriber|Subscriber]] entity is accessed programmatically (JSON-API v2), how the `subscribers` plan cap shapes what the merchant can store and what campaigns can reach, what side effects an API or import write triggers (same as an admin save), and how segments react to the cap. This is the reference for integrations and bulk-data flows.

## Aliases

- **JSON-API v2 subscribers** — the programmatic endpoint surface.
- **`subscribers` plan-feature** — the per-store cap on Subscriber count.
- **Subscribers plan cap** — informal name.
- **CSV import truncation** — what happens when an import would exceed the cap.
- **Segment self-limit** / **`planLimit`** — how segments cap themselves when the population exceeds the plan's reach.
- **`subscriber.*` webhook events** — `subscriber.created`, `subscriber.updated`, `subscriber.deleted`.

## Key Attributes

### Programmatic access via JSON-API v2

A Subscriber row, its per-channel rows, and its tags can be managed via **JSON-API v2**:

- [[api-subscribers]] — POST / PATCH / DELETE the Subscriber row. API-created subscribers land with `subscribed_from = 'API'` (one of 13 sources — see [[subscriber-entity-attributes]]).
- [[api-subscribers-channels]] — POST / PATCH / DELETE per-channel rows (`Email` / `Phone` / `WebPush` / `Messenger`) with their own `marketing` / `verified` / `unsubscribed` / `bounced` flags. See [[subscriber-entity-channels]] for the per-channel state model.
- [[api-subscribers-tags]] — Subscriber-side tags (separate taxonomy from Customer tags).

### Same side effects apply

A POST / PATCH triggers the **same pipeline** as the admin save:

- **Plan-cap check** — the `subscribers.max_id` chronological count is checked; over-cap rows are silently invisible to campaigns (recomputed every 10 minutes — verify).
- **Automated-segment re-evaluation** — 300-second sweep plus per-Subscriber incremental updates re-evaluate segment membership.
- **Customer marketing-flag one-way propagation** — Customer `marketing` flips `yes → no` cascade to per-channel `marketing` on every linked Subscriber; the reverse does NOT auto-flip. See [[subscriber-entity-consent-rules]].
- **Phone-number normalisation** — phone-channel identifiers are normalised to E.164 (international format) before save.
- **Webhook dispatch** — `subscriber.created` / `updated` / `deleted` events fire to [[settings-hooks]] subscribers.
- **`last_active_at` refresh** — API writes are treated as **admin-namespace** updates and do NOT auto-refresh `last_active_at` (storefront-only behaviour — see [[subscriber-entity-lifecycle]]).

The two-layer consent check at send time (Customer-level `marketing` AND per-channel `marketing` AND `verified` AND `!unsubscribed` AND `!bounced`) applies identically — see [[subscriber-entity-consent-rules]].

### Segments are read-only via API

Segments are **read-only** at [[api-segments]] — cannot create or edit segments via API. To build an audience programmatically, integrations POST Subscribers + tags, then a merchant-defined Automated segment filters by tag. This is the canonical pattern for "external system tagged these emails as VIP, now target them in a campaign."

See [[json-api-v2]] for authentication, rate limits, and the side-effects principle.

### The `subscribers` plan-feature cap

The `subscribers` plan-feature caps the total Subscriber count per store. The cap is set per plan; merchants exceed it by upgrading plan or purchasing a feature pack.

When the store approaches the cap, the alert reads:

> *"You reached the limit of feature **Subscribers - :limit** — To continue you should purchase a feature pack or upgrade to a plan with higher limits!"*

See [[plan-gates]] for the cross-cutting plan-feature model.

### CSV import respects the plan cap

Bulk subscriber import via CSV is plan-gated. When the import would exceed the cap, the import **truncates** (stops at the cap) and the merchant sees:

> *"You have:has subscribers. Your limit is:limit"*

…and is directed to upgrade. The truncation is deterministic: the import processes rows top-down and stops at the cap, leaving the remainder unimported.

### Segments self-limit when the cap restricts the audience

When the cap restricts the deliverable population, some segments **self-limit** to the first `:limit` of the population — exposed as the **"Active for segments"** / `planLimit` condition on [[marketing-segments]]. This prevents the merchant from defining a 50,000-Subscriber segment when their plan only includes 10,000 deliverable Subscribers; the segment caps itself at 10,000 to keep the campaign reach honest.

### Webhook event catalogue

| Event | When it fires | Common use |
|-------|---------------|------------|
| `subscriber.created` | New Subscriber row created (any of 13 sources). | Mirror to external CRM / ESP on creation. |
| `subscriber.updated` | Channel data, marketing consent, tags, or custom fields changed. | Re-sync the downstream record. |
| `subscriber.deleted` | Subscriber removed (any path — admin delete, GDPR erasure, Customer-cascade delete). | Remove the downstream record. |

Configured on [[settings-hooks]]. Same payload regardless of WHICH source created / updated / deleted the Subscriber. Receivers must respect the two-layer consent gate themselves on re-send (see [[subscriber-entity-consent-rules]]).

### Customer counts and Subscriber counts are independent caps

This is the most-confused metric in the admin panel. The Customer count caps the `customers` plan-feature; the Subscriber count caps the `subscribers` plan-feature. A store can hit one without the other. **Campaign reach is the Subscriber count, NOT the Customer count.** A merchant with 10,000 Customers and 1,200 Subscribers will see campaigns reach only 1,200.

### Force-marketing tokens at the API

The `force-1` / `force-0` sentinel values for the `marketing` field also work via API — useful for integrations that need to set marketing explicitly without the default fallback logic running. Parsed via `FORCE_MARKETING_REGEX = '/^force-(?<marketing>\d)$/'` and resolved to the integer 1 or 0 before the channel row is saved. See [[subscriber-entity-attributes]] for the storefront use case.

## Where it appears

- [[api-subscribers]] / [[api-subscribers-channels]] / [[api-subscribers-tags]] — the JSON-API v2 endpoints.
- [[json-api-v2]] — auth, rate limits, side-effects principle.
- [[api-segments]] — read-only segment access.
- [[plan-gates]] — `subscribers` plan-feature definition.
- [[marketing-subscribers]] — admin list; surface for the plan-cap alert and CSV import.
- [[marketing-segments]] — segment list; surface for the `planLimit` / "Active for segments" condition.
- [[settings-hooks]] — webhook subscriptions.
- [[apps-mailchimp]] — concrete integration consuming `subscriber.*` webhook events.

## Related

- [[subscriber]] — hub.
- [[subscriber-entity-attributes]] — Subscriber-row fields written by the API (including force-marketing tokens).
- [[subscriber-entity-channels]] — per-channel rows written via `api-subscribers-channels`.
- [[subscriber-entity-consent-rules]] — two-layer consent gate that applies to API writes identically.
- [[subscriber-entity-lifecycle]] — webhook events fire on each lifecycle transition.
- [[json-api-v2]] — cross-cutting JSON-API v2 concept.
- [[plan-gates]] — `subscribers` plan-feature.
- [[settings-hooks]] — webhook configuration.

## Open Questions

- ⏸️ The "recomputed every 10 minutes" cadence for the plan-cap check (verify against current ingestion pipeline).
