---
type: concept
aliases: ["Subscriber segmentation", "How segments work", "Automated vs one-time segment", "Dynamic segment membership", "Segment re-evaluation", "Audience segment", "Static vs dynamic audience", "How a subscriber enters a segment", "Сегментиране на абонати", "Динамичен сегмент", "Как работят сегментите"]
tags: [marketing, subscribers, segments, campaigns, audience, concepts]
plan_gates: []
created: 2026-06-30
updated: 2026-06-30
source_count: 2
---

# Subscriber segmentation model

## Definition

A **segment** is a saved **audience** — a named set of subscribers defined by a tree of **conditions** — that a [[marketing-campaigns|campaign]] sends to. Segmentation is the model that turns the flat subscriber list into targetable groups, and its central distinction is **how membership is computed over time**:

- **Automated** (dynamic) — membership is a **live rule**: a subscriber is in the segment whenever it satisfies the conditions, and the platform **re-evaluates** it as subscribers change (a new capture, an order, a consent change, a tag). Members flow in and out automatically.
- **One-time** (snapshot) — membership is **frozen at creation**: the conditions are evaluated once, and the resulting list doesn't change as subscribers do.

The conditions themselves are a **nested AND/OR tree** built only in the visual [[marketing-segments-editor|editor]] — subscriber attributes, capture source ([[capture-source-attribution|`subscriber.from_form`]]), tags, RFM bucket, customer / order history, app-provided conditions, and more. The condition catalogue is on [[marketing-segments]].

## Scope

Covered: the **automated vs one-time** distinction; **dynamic membership** (how a subscriber enters / leaves an automated segment); re-evaluation as subscribers change; the AND/OR conditions tree as the audience definition; the handoff to campaigns; why segments can't be authored via API. NOT covered: the per-condition catalogue + editor UI (see [[marketing-segments]] / [[marketing-segments-editor]] / `segments-conditions`); the plan caps on segment count / RFM (see `segments-api-and-plan-gates`); the deliverability flags applied *after* segment membership (see [[subscriber-deliverability]]).

## Contrasts

- **Automated vs one-time** — automated = "everyone who currently matches" (a living audience for recurring sends); one-time = "everyone who matched on this date" (a fixed list for a single blast). Choosing wrong is a common mistake: a one-time segment will **not** pick up subscribers captured after it was built.
- **Segment membership vs deliverability** — being *in* a segment says the subscriber matches the audience; it does **not** guarantee a send. The campaign still applies the [[subscriber-deliverability|reachability predicate]] (verified / consent / unsubscribed / bounced) on top. A subscriber can be in the segment yet never receive the campaign.
- **Segment vs tag** — a **tag** is a manual / rule-applied label on a subscriber; a **segment** is a query that *uses* tags (and many other attributes) as conditions. Tags are inputs to segmentation, not segments themselves.
- **Visual-builder-only vs API** — segments are GET-readable via [[json-api-v2]] (including membership) but **not** creatable / editable via API — the nested conditions tree is authored only in the editor.

## Where it applies

### Dynamic re-evaluation

For an **automated** segment, the platform re-evaluates membership when a subscriber's data changes — including the moment a [[lead-capture-lifecycle|form capture]] creates / updates a subscriber (the submit cascade triggers a re-evaluation), and on subsequent subscriber/customer/order changes. A subscriber that newly satisfies the conditions joins; one that no longer satisfies them drops. Segments carry a `processing` state while membership is being recomputed. (verify: the full set of events that trigger re-evaluation and any batching delay.)

### Building an audience

In the editor the merchant composes conditions (AND/OR). Examples: "from the homepage popup" (`subscriber.from_form`), "has tag `vip`", "RFM = champions", "placed an order in the last 30 days". The condition picker only shows conditions the plan / installed apps allow.

### Handoff to campaigns

A campaign targets one or more segments; at send time it walks the segment members and applies the deliverability predicate per channel. So the segment decides **who is in scope**, and deliverability decides **who actually gets it** — see [[subscriber-deliverability]] and [[marketing-campaigns]].

## Related

- [[marketing-segments]] — the segments feature hub (list, types, conditions, editor).
- [[marketing-segments-editor]] — the visual conditions-tree builder.
- [[capture-source-attribution]] — the `subscriber.from_form` condition (segment by which form captured the lead).
- [[subscriber-deliverability]] — the reachability predicate applied AFTER segment membership.
- [[lead-capture-lifecycle]] — the capture event that triggers re-evaluation of automated segments.
- [[marketing-campaigns]] — the consumer that sends to a segment.
- [[subscriber]] — the entity whose attributes drive membership.

## Open Questions

- (verify) The exact event set + any delay/batching for automated-segment re-evaluation, and whether membership is materialised or computed live at send time.
