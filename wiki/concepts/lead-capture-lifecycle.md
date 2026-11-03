---
type: concept
aliases: ["Lead capture lifecycle", "Form to subscriber to campaign", "Lead capture pipeline", "Subscriber capture flow", "From form to campaign", "Capture source attribution", "subscriber.from_form", "Lead nurturing pipeline", "Жизнен цикъл на лийд", "От форма до кампания", "Улавяне на абонати"]
tags: [marketing, subscribers, forms, lead-capture, segments, campaigns, lifecycle, concepts]
plan_gates: []
created: 2026-06-30
updated: 2026-06-30
source_count: 2
---

# Lead capture lifecycle (form → subscriber → segment → campaign)

## Definition

The **lead-capture lifecycle** is the end-to-end path a marketing lead travels from the moment a visitor submits a [[marketing-subscribers-subscribe-forms|subscribe form]] to the moment they receive a campaign. A form is not an island — it is the **front door of the marketing system**: each submit feeds a pipeline that creates or matches a **subscriber**, stamps it with tags / custom fields / its capture source, sets its verification and consent state, re-evaluates **segments**, and hands the subscriber off to **campaigns**. Understanding this pipeline is what lets a merchant reason about "I collected 500 emails — why did only 300 get my newsletter?" (the answer is somewhere along this chain: channel, verification, consent, or segment membership).

## Scope

Covered: the capture cascade on submit; visitor→subscriber matching (no duplicate); channel extraction (only the store's configured campaign channels collect); tags + custom fields; **capture-source attribution** (`subscriber.from_form`); segment re-evaluation; the handoff to campaigns; the `subscriber.created` webhook for external CRM. NOT covered: *how* a form is shown (see [[subscribe-form-display-engine]]); *whether* a subscriber can be emailed — the verification gate (see [[subscriber-double-optin]]) and the consent gate (see [[subscriber-vs-customer-consent]]); the form builder UI itself.

## Contrasts

- **Capture vs activation** — *capture* is becoming a subscriber (the submit succeeds); *activation* is becoming **reachable** (verified + consented) and entering the segments a campaign targets. A captured lead that is never verified or never consents stays on the list but never receives a send.
- **Subscriber vs customer** — a captured lead is a **Subscriber**; it may or may not also be a **Customer** (someone who placed an order). The two records are distinct and can be linked — see [[subscriber-vs-customer]].
- **Form capture vs other capture sources** — subscribe forms are one source; checkout marketing opt-in, [[api-subscribers|API]], and import also create subscribers. The `subscriber.from_form` attribute records that a given subscriber came from a form (and which one), so the merchant can segment / attribute by capture source.

## Where it applies

### The capture cascade (on submit)

When a visitor submits, the platform runs, in order (full detail on [[subscribe-forms-submission-flow]]):

1. **Validate** — required fields + any required terms/policies.
2. **Match or create** — the visitor is matched to an existing subscriber by email / phone, or a new subscriber row is created (no duplicate).
3. **Channel extraction** — email and/or phone are captured **only for the store's configured campaign channels** (a channel the store doesn't run is not collected).
4. **Tags + custom fields** — the form's tag list is applied to the subscriber, custom-field values stored, and the **capture source** recorded (`from_form` + which form).
5. **Verification** — the initial `verified` state is set per the form's opt-in choice — see [[subscriber-double-optin]].
6. **Consent** — marketing consent is set from the ticked terms / marketing-policy — see [[subscribe-forms-gdpr-consent]] and [[subscriber-vs-customer-consent]].
7. **Segment re-evaluation** — the new / updated subscriber is re-matched into [[marketing-segments|segments]], so any segment whose conditions it now satisfies picks it up.
8. **Webhook** — `subscriber.created` fires for external CRM / automation sync — see [[settings-hooks]].

### Capture-source attribution — `from_form`

The `subscriber.from_form` condition on [[marketing-segments]] slices subscribers by **which form captured them** — e.g. a "Welcome 10%" segment of everyone from the homepage popup, targeted by a dedicated campaign. This is the platform's built-in capture-source attribution.

### Handoff to campaigns

Once a subscriber is **verified + consented + a member of a targeted segment**, it is an eligible [[marketing-campaigns|campaign]] recipient. The campaign's send step applies the same verified / consent / unsubscribed / bounced filters, so the lifecycle's earlier stages (verification, consent) directly determine reach — a gap at any stage is where captured leads "disappear" before the inbox.

## Related

- [[marketing-subscribers-subscribe-forms]] — the capture front door.
- [[subscribe-forms-submission-flow]] — the step-by-step submit cascade.
- [[subscriber-double-optin]] — the verification stage of the lifecycle.
- [[subscriber-vs-customer-consent]] — the consent stage + send-eligibility predicate.
- [[subscribe-form-display-engine]] — how the form got in front of the visitor in the first place.
- [[marketing-segments]] — `subscriber.from_form` + the re-evaluation that places leads into audiences.
- [[marketing-campaigns]] — the downstream consumer of captured, activated leads.
- [[subscriber]] / [[subscriber-vs-customer]] — the entity created and how it relates to a Customer.
- [[settings-hooks]] — `subscriber.created` webhook for external sync.

## Open Questions

None.
