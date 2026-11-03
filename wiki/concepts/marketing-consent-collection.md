---
type: concept
aliases: ["Marketing consent collection", "How marketing consent is collected", "Consent capture surfaces", "Marketing opt-in checkbox", "Terms checkbox subscribe form", "Marketing policy", "PolicyAcceptanceLog", "Consent audit log", "GDPR consent proof", "Second marketing rule", "Събиране на маркетингово съгласие", "Отметка съгласие маркетинг"]
tags: [marketing, subscribers, consent, gdpr, compliance, forms, checkout, concepts]
plan_gates: []
created: 2026-06-30
updated: 2026-06-30
source_count: 2
---

# Marketing consent collection & compliance

## Definition

This concept is the **collection** side of marketing consent: **where and how a store gathers a person's agreement to receive marketing, and how it proves it later.** It is the counterpart to [[subscriber-vs-customer-consent]], which is the **gate** (the eligibility predicate that decides whether a given send is allowed). Consent is collected at several independent surfaces, and each accepted policy is written to an **audit log** so the merchant can demonstrate, per person, *what* they agreed to, *when*, and *from where* — the compliance backbone for GDPR-style regimes.

The surfaces that collect consent:

- **Subscribe forms** — attached **terms / legal Page checkboxes** (required-flagged ones become submit-time validation), and a **marketing-policy checkbox** whose ticking **forces marketing consent on** for the captured subscriber (a deliberate override of per-channel defaults). See [[subscribe-forms-gdpr-consent]].
- **Checkout** — the marketing opt-in checkbox at order placement, plus the **"second marketing" rule** (when a returning person orders without re-ticking marketing, the platform can auto-reset their marketing flag — see [[subscriber-vs-customer-consent]]).
- **GDPR app** — the `marketing_policy` setting and the legal **Page** entities ([[apps-gdpr-policy]]) that forms and checkout attach, plus the cookie-consent groups ([[apps-gdpr-cookies]]).

## Scope

Covered: the consent-collection surfaces (form terms + marketing-policy, checkout opt-in, the second-marketing reset); the **forced-consent override** when a marketing policy is ticked; the **audit row** written per accepted policy (IP / user-agent / timestamp / content reference) as compliance proof. NOT covered: the **send-eligibility gate** that consumes consent — see [[subscriber-vs-customer-consent]]; the per-channel deliverability flags — see [[subscriber-vs-customer-channels]] / [[subscriber-deliverability]]; the cookie-consent display gate on the form (a *display* decision, not marketing consent) — see [[subscribe-forms-gdpr-consent]].

## Contrasts

- **Collection vs gate** — this concept is "how consent was obtained and proven"; [[subscriber-vs-customer-consent]] is "is a send allowed right now." A merchant auditing a complaint reads the *collection* (the audit row); a campaign send reads the *gate*.
- **Marketing consent vs cookie consent** — the form's terms / marketing-policy checkbox captures **marketing** consent (may we email you); the `cookies_consent` flag is about the **targeting-cookie** group and only governs whether the form is *shown* — different consent, different purpose. The two are routinely conflated; see [[subscribe-forms-gdpr-consent]].
- **Required vs optional terms** — a term flagged **required** blocks submit until ticked (hard consent); an optional marketing checkbox is captured if ticked but doesn't block.
- **Forced-on vs default** — ticking a marketing policy forces the subscriber's marketing flag ON regardless of per-channel default; an un-ticked optional checkbox leaves the default behaviour.

## Where it applies

### At a subscribe form

Attached **terms** render as checkboxes (each with `required` + custom label styling). Required terms become submit validation. A **marketing-policy** tick forces marketing consent on for the new subscriber. Every accepted policy writes an audit row. See [[subscribe-forms-gdpr-consent]] and [[lead-capture-lifecycle]].

### At checkout

The marketing opt-in is captured with the order; the **second-marketing** rule governs what happens when a consenting person later orders without re-ticking. See [[subscriber-vs-customer-consent]].

### The audit log (compliance proof)

Each accepted policy is recorded with the actor's IP, user-agent, time, and a reference to the exact policy content/version — so months later the merchant can answer "prove this person agreed". No admin screen surfaces the raw log directly (verify); it exists for compliance / dispute handling.

### Programmatic captures

Subscribers created via [[api-subscribers]] / import carry whatever consent the integrator sets — there is no checkbox surface, so the merchant is responsible for having collected consent out-of-band before importing.

## Related

- [[subscriber-vs-customer-consent]] — the consent **gate** (eligibility predicate) this collection feeds.
- [[subscribe-forms-gdpr-consent]] — the form's terms + marketing-policy + the inverted cookie gate + the audit row.
- [[apps-gdpr-policy]] — the legal Page entities attached as terms.
- [[apps-gdpr-cookies]] — cookie-consent groups (the *display* gate, not marketing consent).
- [[subscriber-deliverability]] — what consent (plus verification + bounce/unsubscribe) adds up to at send time.
- [[lead-capture-lifecycle]] — where consent collection sits in the form-to-campaign pipeline.

## Open Questions

- (verify) Whether any admin screen surfaces the per-person consent audit log, or whether it is back-office / export-only.
