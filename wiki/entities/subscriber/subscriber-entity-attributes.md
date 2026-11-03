---
type: entity
nav_path: "Entity → Subscriber → Attributes"
aliases: ["Subscriber attributes", "Subscriber fields", "Subscriber-row schema", "Subscriber identity fields", "subscriber_from sources", "RFM bucket", "Force-marketing tokens"]
tags: [entity, marketing, subscribers, attributes]
plan_gates: ["subscribers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[subscriber]]. See the hub for the other aspects (channels, lifecycle, consent rules, relationships, API + plan).

# Subscriber — Attributes

## Identity

The per-field schema of the **Subscriber row itself** — the identity, consent, source, tenure, tagging, and analytics fields stored on the parent record. Per-channel data (email / phone / PSID identifiers, verification, unsubscribed, bounced) lives on **SubscriberChannel** rows and is documented separately on [[subscriber-entity-channels]].

## Aliases

- **Subscriber-row fields** — the identity-side schema (not the per-channel side).
- **`subscriber_from` sources** — the 13-value enum that records HOW the Subscriber entered the audience.
- **RFM bucket** — the recency / frequency / monetary analytics bucket attached to every Subscriber.
- **Force-marketing tokens** — the `force-1` / `force-0` sentinel values used at storefront subscribe time.

## Key Attributes

### Subscriber identity

| Field | What it stores | Notes |
|-------|----------------|-------|
| **First name** / **Last name** | Identity name | Both optional. Displayed concatenated as `full_name` in the list and detail view. Falls back to the default channel's identifier when both empty. |
| **Country** | ISO-2 country code → resolved to country name | Detected at signup via geo-lookup, or set explicitly on import. Used in segment filtering. |
| **Marketing consent** (`marketing`) | yes / no | The Subscriber-row-level marketing flag. Bulk-togglable on [[marketing-subscribers]]. Distinct from the per-channel marketing flag — both are checked at send time. See [[subscriber-entity-consent-rules]]. |
| **GDPR accepted** (`gdpr_accepted`) | yes / no | Records whether the Subscriber consented to the store's GDPR / marketing policy. Used in compliance audit. |
| **Subscribed from** (`subscriber_from`) | One of 13 sources (see below) | Set at creation; **immutable** afterwards. Drives the "Subscribed by" filter on [[marketing-subscribers]] and the `subscriber.from` segment condition. |
| **Subscribed on** (`created_at`) | Datetime | When the Subscriber row was first created. Used by RFM and tenure-based segments. |
| **Last active on** (`last_active_at`) | Datetime | Auto-updated on every storefront write — see [[subscriber-entity-lifecycle]] for the storefront-vs-admin namespace rule. Drives the `last_active` segment condition. |
| **Identified on** (per-channel `identified_at`) | Datetime | When each per-channel identifier was first matched. Used to distinguish anonymous tracking from a known-identifier audience. |
| **Tags** | Custom Subscriber tags (separate taxonomy from Customer tags) | Merchant-managed; used in segments and reports. |
| **Custom fields** | Per-merchant custom field values | Defined on [[marketing-subscribers-custom-fields]] (e.g., "Birthday", "Industry", "T-shirt size"). Distinct from Customer custom fields. |
| **UUIDs** | Identified-device tracking cookies | Tracking-cookie UUIDs attached to the Subscriber. Drives device-level analytics. |
| **RFM bucket** | One of 17 categorical buckets | Recency / Frequency / Monetary analytics bucket — Champ, Active Loyal, New, Loyal, Potential, Occasional, Churned, *Without RFM Analysis*, etc. Re-computed on a configurable interval (default 90 days, range 30 – 3652). |
| **`form_id`** | Subscribe-form reference (24-char string) | Set when `subscriber_from = 'subscribe_form'`. Captures which specific subscribe form created this subscriber. Used by the `subscriber.from_form` segment condition. Stored as a denormalised string. |
| **Force-marketing tokens** | `force-1` / `force-0` | Special sentinel values for `marketing` that bypass the per-channel default behaviour at storefront subscribe time. Parsed via `FORCE_MARKETING_REGEX = '/^force-(?<marketing>\d)$/'` and resolved to the integer 1 or 0 before the channel row is saved. Used when the storefront explicitly captured (or denied) marketing consent and the merchant doesn't want fallback logic to override the choice. |

### Subscriber sources (`subscriber_from`)

| Source constant | Label |
|-----------------|-------|
| `customer_login` | Customer login |
| `subscribe_form` | Popup and Form builder |
| `subscribe_from_missing_product` | Subscribe to an in-stock product |
| `import` | Import |
| `system` | From system |
| `customer_address_creating` | Customer address creating |
| `customer_address_deleting` | Customer address deleting |
| `customer_creating` | Customer creating |
| `order_creating` | Order creating |
| `messenger` | Facebook messenger |
| `contacts_form` | Contacts form |
| `web_push` | Web push |
| `API` | API |

Note: `subscribe_form` is intentionally excluded from the `FROM_ALL` constant array used for some filter dropdowns — meaning some merchant-facing pickers list sources EXCLUDING `subscribe_form`. The full 13-source set still applies internally and to the `subscriber.from` segment condition.

### Source-set immutability

`subscriber_from` is set at creation and **cannot be edited later** — the field captures HOW the Subscriber entered the audience, and rewriting it would corrupt the audit trail and segment-targeting accuracy. Migrations between sources require deleting and recreating the Subscriber.

### Custom fields are distinct from Customer custom fields

The Subscriber has its own custom-field set defined on [[marketing-subscribers-custom-fields]] — totally separate from Customer custom fields on [[customers-custom-fields]]. The two field catalogs do not share definitions; the same conceptual field would have to be defined on both surfaces independently if the merchant wants it on both records.

### Tags are a separate taxonomy

Subscriber tags are managed in their own taxonomy (separate from Customer tags). The same word may exist as a Customer tag and a Subscriber tag with no overlap or shared definition — they are independent.

### RFM bucket recomputation

Every Subscriber is scored into one of 17 RFM buckets (Champ, Active Loyal, New, Loyal, Potential, Occasional, Churned, etc., plus *Without RFM Analysis* for new or insufficient-history Subscribers). The recompute interval is configurable on [[marketing-subscribers]] → Settings (default 90 days, range 30 – 3652). The merchant can review the recompute history on the RFM Log screen.

## Where it appears

- [[marketing-subscribers]] — list view shows `first_name`, `last_name`, the default-channel identifier, `subscriber_from`, RFM bucket, `marketing`, tags, `last_active_at`.
- [[marketing-subscribers]] → detail page — full Subscriber-row edit (names, country, tags, custom fields, `marketing`, `gdpr_accepted`).
- [[marketing-subscribers-custom-fields]] — custom-field definitions.
- [[marketing-segments]] — segment conditions reference `subscriber.from`, `last_active`, tag-membership, RFM bucket, custom-field values.
- [[customers-import]] — when "Mark as subscriber" is enabled, the import creates Subscriber rows with `subscriber_from = 'import'`.

## Related

- [[subscriber]] — hub.
- [[subscriber-entity-channels]] — per-channel identifiers and deliverability flags.
- [[subscriber-entity-consent-rules]] — how the `marketing` flag combines with per-channel state at send time.
- [[marketing-subscribers]] — the list / settings screen.
- [[marketing-subscribers-custom-fields]] — Subscriber-specific custom-field catalog.

## Open Questions

None.
