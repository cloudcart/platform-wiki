---
type: entity
nav_path: "Entity → Marketing Campaign → Attribution & Statistics"
aliases: ["Campaign attribution", "Campaign statistics", "campaign_id on order", "campaign_action_id on order", "cc_campaign query parameter", "Hourly aggregation lag", "Campaign revenue rollup", "Click attribution", "Атрибуция кампания", "Статистика кампания"]
tags: [entity, marketing, campaigns, attribution, statistics, analytics]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[campaign]]. See the hub for the other aspects (types, attributes schema, lifecycle, relationships, consent gating).

# Campaign — Attribution & Statistics

## Identity

The campaign Statistics screen translates raw delivery events (sent, delivered, opened, clicked, unsubscribed, bounced) and downstream revenue events (a click became an order) into the per-action and per-campaign counters the merchant looks at. The pipeline has three legs:

1. **Per-recipient delivery log** — every (subscriber, action) delivery attempt records its outcome (delivered, opened, clicked).
2. **Order back-references** — Orders produced after a click on a campaign message carry `campaign_id` and `campaign_action_id` metadata, written at order-creation time.
3. **Hourly aggregation** — a background job rolls the per-recipient log + the Order back-references into the aggregate counter columns on the Campaign row, which the Statistics screen reads directly.

This page explains the click-attribution chain end-to-end and the timing semantics merchants encounter ("why don't my counts update immediately").

## Aliases

- **Attribution** = associating an Order with the Campaign that produced it via `campaign_id` / `campaign_action_id`.
- **`cc_campaign`** = the query parameter the storefront tracking middleware reads off the click URL to capture campaign context into the session.
- **`orders_meta`** = the order-metadata bag where the campaign back-references are stored (`cc_campaign_id`, `cc_campaign_name`, `cc_campaign_action_id`, `cc_campaign_action_order`, `cc_campaign_channel`, `cc_campaign_subscriber_name`).
- **Hourly aggregation lag** = the up-to-60-minute delay between an event happening and the Statistics screen showing the updated count.
- **Per-action rollup** = the per-(action) breakdown showing each channel / step's individual performance.

## Key Attributes

### What the Statistics screen shows

The Statistics screen surfaces these dimensions, all rolled up from the per-recipient log + Order back-references:

| Dimension | Per action | Per campaign |
|-----------|-----------|--------------|
| Total sent | ✓ | ✓ |
| Successfully sent | ✓ | ✓ |
| Opens (Email + Web Push) — `seen_message` | ✓ | ✓ |
| Clicks — `opened_url` | ✓ | ✓ |
| Unsubscribed | ✓ | ✓ |
| Abuse | ✓ | ✓ |
| Bounced | ✓ | ✓ |
| Distinct recipients reached | ✓ | ✓ |
| Orders count (attribution) | ✓ | ✓ |
| Revenue total | ✓ | ✓ |
| Conversion rate | ✓ | ✓ |

### The aggregate columns on the Campaign row (verified against backend)

These integer columns live on the `campaigns` row, NOT recomputed at view time — the merchant-facing Statistics page reads them directly. Updated by the hourly aggregation job:

- `total_sent`
- `successfully_sent`
- `seen_message`
- `opened_url`
- `unsubscribed`
- `abuse`
- `bounced`
- `reached`

The implication: a click that just happened at 12:05 won't show on Statistics until the next aggregation cycle completes — see [[marketing-campaigns-statistics#hourly-aggregation-lag|hourly aggregation lag]] for the merchant-facing wording.

## Where it appears

- [[marketing-campaigns-statistics]] — the per-campaign Statistics screen reading the aggregate counter columns directly.
- [[marketing-campaigns-statistics-log]] — the per-recipient delivery log view.
- [[marketing-campaigns-statistics-full]] — the full revenue-attribution screen reading the `orders_meta` campaign metadata.
- [[order]] — the entity carrying the `campaign_id` / `campaign_action_id` / full `orders_meta` campaign-attribution metadata.
- [[campaign-entity-attributes-schema]] — column-level reference for the aggregate counter columns.
- [[campaign-entity-relationships]] — for how the per-recipient log relates to the Campaign and Subscriber.

### Click attribution writes order metadata at order-creation time (verified against backend)

The attribution chain is:

1. Campaign message body contains a link with `?cc_campaign=...` query parameter (auto-generated when the merchant inserts a link from the editor).
2. Customer clicks the link → lands on the storefront.
3. Storefront tracking middleware reads `cc_campaign` query → resolves the campaign context (campaign id, action id, channel, subscriber identity).
4. Session stores the campaign context for the duration of the browsing session.
5. Customer adds to cart and places an order in the same session.
6. The order-creation job stamps the resulting Order's `orders_meta` with:
   - `cc_campaign_id`
   - `cc_campaign_name`
   - `cc_campaign_action_id`
   - `cc_campaign_action_order`
   - `cc_campaign_channel`
   - `cc_campaign_subscriber_name`

This metadata is what the per-campaign and full revenue dashboards read — see [[marketing-campaigns-statistics-full]] for the full mechanic.

The implication for the merchant: orders that come from clicks on campaign messages are **fully traceable** back to the originating campaign + action + channel + subscriber, for as long as the order record exists.

### Hourly aggregation lag

The aggregate counter columns are refreshed by a background job that runs hourly. The aggregation reads the per-recipient log (CampaignChannelLog) + the `orders_meta` campaign back-references on Orders placed since the last run, rolls them up, and writes the updated counter columns.

The merchant sees:

- Per-recipient log: updates effectively in real time (each delivery / open / click writes its own log row).
- Statistics screen counters: lag up to one hour behind the log.
- Auto-archive on Regular completion: triggered by the same hourly job — see [[campaign-entity-lifecycle]].

### Revenue attribution scope

The attribution is **session-bound** — if the customer clicks the campaign link, leaves the site, and comes back hours later via a different entry point (direct, organic search, paid ad), the new session has no `cc_campaign` context and the resulting order does not attribute to the campaign. Most platforms call this "last-click in-session" attribution.

The merchant who wants longer-window attribution must use external analytics — the native attribution model is session-based `(verify)`.

## Related

- [[campaign]] — hub.
- [[campaign-entity-attributes-schema]] — counter columns reference (`total_sent`, `successfully_sent`, `seen_message`, `opened_url`, `unsubscribed`, `abuse`, `bounced`, `reached`).
- [[campaign-entity-relationships]] — CampaignChannelLog and Order back-references.
- [[campaign-entity-consent-gating]] — what counts as a suppressed-not-sent vs a delivered.
- [[campaign-entity-lifecycle]] — auto-archive on completion is triggered by the same hourly job.
- [[order]] — carries `campaign_id` / `campaign_action_id` and the full `cc_campaign_*` `orders_meta` bag.
- [[marketing-campaigns-statistics]] — the per-campaign Statistics screen.
- [[marketing-campaigns-statistics-log]] — the per-recipient delivery log.
- [[marketing-campaigns-statistics-full]] — the full revenue-attribution screen.
- [[notification-delivery]] — the underlying delivery infrastructure that produces the per-recipient log events.

## Open Questions

- ⏸️ The exact attribution window for `cc_campaign` — whether the session expiry is the browser session, a cookie TTL, or a backend session-store TTL. `(verify)`
- ⏸️ Whether attribution to a campaign is destroyed by a customer clearing cookies between click and order. `(verify)`
- ⏸️ Whether multi-touch attribution is possible (a customer clicked Campaign A then Campaign B then ordered) or only single-source last-click. `(verify)`
