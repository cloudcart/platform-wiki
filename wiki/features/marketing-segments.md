---
type: feature
nav_path: "Marketing → Segments"
route_name: segments.core_new.list
route_path: /admin/marketing-new/segments
aliases: ["Segments", "Customer segments", "Subscriber segments", "Сегменти", "Клиентски сегменти"]
tags: [marketing, segments, subscribers, targeting]
plan_gates: ["segments", "subscribers", "subscribers-rfm"]
created: 2026-05-21
updated: 2026-06-10
source_count: 15
---

# Segments

## Purpose

A **Segment** is a named, rule-based grouping of subscribers (and through them, customers and visitors) the merchant uses to target campaigns, discounts, cross-sell offers, and analytics. The merchant declares a logical AND-chain of conditions ("subscribed in last 30 days" AND "viewed products from category 'Shoes'" AND "has not ordered") and the platform evaluates the subscriber population against them, attaching/detaching subscribers as they qualify or stop qualifying.

Segments are the **primary audience-selection object** in CloudCart marketing: every email/SMS/messenger campaign in [[marketing-campaigns]] targets a segment, the discounts in [[marketing-discounts]] can require a segment match, and recommendation engines in [[marketing-cross-sell]] use segment membership as a trigger. Two segment types coexist — **One-time** (`regular`, snapshot) and **Automated** (`automated`, continuously re-evaluated) — and the merchant can also add/remove individual subscribers manually on top of the rule output.

## Where to find it

Sidebar → **Marketing** → **Segments**.

Route `/admin/marketing-new/segments`. The page lists every segment with its subscriber count, campaign count, last-generated timestamp, and active state.

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages. Drill into the one matching the question.

- [[segments-list-page]] — the list view: columns, per-row actions, status/type icons, live auto-refresh, the Rename modal.
- [[segments-create-popup]] — the **Create new segment** popup: from scratch / Generate with AI / predefined template (6 templates).
- [[segments-types]] — `regular` (One-time, snapshot) vs `automated` (continuously synced); choice immutable after create.
- [[segments-conditions]] — the 60+ conditions; AND-only composition; allowed-combination restrictions; channel-aware filters; verified-email gate.
- [[segments-inactive-errors]] — auto-disable flow when a segment references something deleted; `inactive_errors`; banners and notifications.
- [[segments-rebuild-mechanics]] — when a segment recalculates: the 5-minute Automated sweep, on-save rebuild, per-event refresh, and the `subscribers.max_id` cap.
- [[segments-api-and-plan-gates]] — JSON-API v2 read-only access, the plan gates (`segments`, `subscribers`, `subscribers-rfm`), and the `rfm_interval` / `bestseller_period` settings panel.

The editor lives on [[marketing-segments-editor]]; the per-segment subscriber list on [[marketing-segments-subscribers]]; the audit log on [[marketing-segments-log]].

## What the merchant can do here

- Click **Create segment** and choose a type, or pick **Generate with AI** / **Predefined template** — see [[segments-create-popup]].
- Edit a segment's **Segmentation conditions** in [[marketing-segments-editor]].
- Click the subscriber count to open the per-segment subscriber list ([[marketing-segments-subscribers]]) — see who qualifies, manually add a subscriber, or manually remove only the manually-added entries.
- Click the **Log** link to open the segment change log ([[marketing-segments-log]]) — an audit trail of attach/detach over time.
- Toggle a segment **Active**/Inactive. Inactive segments stop being recalculated and can't be selected as a campaign target.
- Delete one or many segments — blocked if a campaign is attached (see Business rules).
- Generate a **CSV file** of the segment's subscribers via the per-row export.
- **Rename** a segment via a dedicated modal (the editor itself doesn't expose a name field).

## Settings & fields

### Create / Edit form fields (top-level)

| Field | What it does | Validation |
|-------|--------------|------------|
| **Segment name** | Merchant-facing label shown in campaign pickers and reports. | Required ("The segment must have a name"). |
| **Type** | `regular` (One-time) or `automated` — chosen at create, immutable after. See [[segments-types]]. | Required ("You must choose a segment type"). |
| **Segmentation conditions** | AND-list of rules that define the segment. At least one required. See [[segments-conditions]]. | "You must choose at least one condition". Tooltip: *"You can add up to 4 conditions"*. |
| **Active** | Whether the segment is currently being evaluated. | Inactive segments are excluded from sweeps and can't be targeted by campaigns. |

List-view columns, the Rename modal rules, and the template list live on [[segments-list-page]] and [[segments-create-popup]].

### RFM / bestseller settings panel (adjacent to the list)

- `rfm_interval` — required integer, **min 7, max 360 days**. Lookback window for RFM bucketing.
- `bestseller_period` — required integer, **min 7, max 360 days**. Window used for "bestseller" tagging.

Defaults work for most catalogs — only tune when adjusting RFM cohorts. Full validation on [[segments-api-and-plan-gates]].

## Business rules

These rules apply across the cluster — aspect-specific rules live on each sub-page.

### Type is immutable after create

The merchant picks `regular` or `automated` on [[segments-create-popup]]; that choice is set in stone. To change, the merchant must duplicate-and-recreate. The difference is whether membership refreshes automatically as subscribers change (Automated) or only on manual regenerate / save (One-time). See [[segments-types]].

### AND-only composition

The help text reads exactly: **"All conditions have a logical 'AND'"**. There is no merchant-visible OR composition — every condition row must match. To express OR, the merchant creates separate segments. See [[segments-conditions]] for the full vocabulary and the `subscriber.missing_product` allowed-combinations carve-out.

### Manual add/remove sits on top of rules

From the per-segment subscriber list, the merchant can **manually add** a subscriber — this creates a pivot row with `manual = 1`. Manual additions are NOT removed when the subscriber stops matching. **Removal** acts only on manual entries: *"Only those that were manually added to it will be removed."* Rule-matched subscribers detach themselves when they stop qualifying.

### Segment-deletion guard — campaign attachment blocks delete

A segment cannot be deleted while one or more campaigns target it. Exact messages:

- Single: *"You can't delete the segment because it is used in campaigns: :names"*
- Bulk: *"You cannot delete segments that have campaigns attached to them. To delete segments, you must first delete a campaign."*

### Auto-disable mid-rebuild

A segment can self-disable between scheduled rebuilds without any merchant action — when it references a deleted customer custom field, an uninstalled app's condition, etc. Full triggers, the `inactive_errors` field, banners, and the notification path live on [[segments-inactive-errors]].

### Plan-gated with subscriber-count limit

Three plan features control segments: `segments` (Automated-segment cap), `subscribers` (max evaluated subscribers, enforced via `subscribers.max_id`), and `subscribers-rfm` (whether the RFM condition is available). One-time (`regular`) segments do NOT count toward the `segments` cap. See [[segments-api-and-plan-gates]] for the mapping and upgrade paths.

### Read-only via JSON-API v2

Segments are exposed at [[api-segments]] but are **read-only** — POST / PATCH / DELETE are not supported. Integrations can enumerate, monitor, and poll, but cannot create or edit segments (the `conditions` rule tree can only be authored in the visual builder). See [[segments-api-and-plan-gates]].

## Related

- [[marketing]] — parent hub.
- [[marketing-subscribers]] — the people who get filtered into segments.
- [[marketing-subscribers-subscribe-forms]] — storefront forms that produce new subscribers + can be filtered via the `from_form` condition.
- [[marketing-campaigns]] — primary consumer; every campaign targets a segment.
- [[marketing-discounts]] — discounts can require a segment match (audience-targeted promotions).
- [[marketing-cross-sell]] — segment membership can trigger cross-sell offers.
- [[marketing-segments-editor]] — the conditions-tree builder modal.
- [[marketing-segments-subscribers]] — per-segment subscriber list + manual add/remove.
- [[marketing-segments-log]] — attach/detach audit log.
- [[apps-cart-rules]] — uses the same condition family.
- [[apps-product-review]] — contributes `apps.others.product_review.subscriber_segments.*` conditions.
- [[apps-mailchimp]] — segments can be exported as Mailchimp lists.
- [[customer-group]] — customer-group membership is a segment condition.
- [[segment]] — entity page.
- [[subscriber]] — entity page.
- [[subscriber-vs-customer]] — segments target subscribers, who may or may not be customers.
- [[subscriber-segmentation]] — concept: automated (dynamic) vs one-time (snapshot) audiences + how a subscriber enters / leaves a segment.
- [[capture-source-attribution]] — concept: the `subscriber.from_form` source the segment condition filters on.
- [[subscriber-deliverability]] — concept: the reachability predicate applied AFTER segment membership at send time.
- [[plan-features]] / [[plan-gates]] / [[plan-vs-feature-pack]] — plan-feature model.
- [[json-api-v2]] — API conventions for the read-only endpoint.
- [[background-queue-inventory]] — covers the 300-second automated-segment rebuild and the 10-minute subscriber-cap recomputation.

## Open questions

- 📡 **Membership-app conditions visibility.** `apps.administration.membership.*` conditions appear in the condition picker only when the Membership app is installed and active on the merchant's store.
