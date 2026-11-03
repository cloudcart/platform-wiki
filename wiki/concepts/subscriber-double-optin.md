---
type: concept
aliases: ["Double opt-in", "Single opt-in", "Subscriber verification", "Verify subscriber email", "Mark as verified", "Send validation email link", "Email confirmation for subscription", "Confirmed opt-in", "Unverified subscriber", "verified flag subscriber", "Двойно потвърждение на абонамент", "Потвърждение на имейл за абонат"]
tags: [marketing, subscribers, forms, opt-in, verification, deliverability, concepts]
plan_gates: []
created: 2026-06-30
updated: 2026-06-30
source_count: 2
---

# Subscriber double opt-in & verification

## Definition

Every captured subscriber is, per channel, either **verified** or **unverified**. **Verification is the platform's proof that the email (or phone) really belongs to the person — and it is the deliverability gate: campaign sends only go to `verified = 1` subscribers.** A [[marketing-subscribers-subscribe-forms|subscribe form]] decides the *starting* verification state through two **mutually-exclusive** toggles in the builder:

- **Mark as verified** (`markAsVerified`) — **single opt-in**: trust the capture and set `verified = 1` immediately on submit.
- **Send validation email link** (`emailConfirm`) — **double opt-in**: set `verified = 0`, email the person a confirmation link ("Email confirmation for subscription in store:site_name"), and only flip to `verified = 1` after they click it.

If neither is on, the subscriber is created `verified = 0` and no confirmation email is sent — they sit unverified until something else verifies them. The two toggles are mutually exclusive in the UI; if both were somehow set, **`markAsVerified` wins** (the backend checks it first) — see [[subscribe-forms-submission-flow]].

This is the classic **single-vs-double opt-in** choice, surfaced per form: speed and volume (mark-as-verified) versus list hygiene and proven consent (email confirmation).

## Scope

What this concept covers:

- The two form toggles and their precedence (mark-as-verified before email-confirm).
- The double-opt-in email-confirmation flow (the verify link, the "Email confirmation…" mail).
- **Non-email channels are verified by default** — there is no e-mail-style confirmation step for them; the email-confirmation flow is email-only.
- The downstream payoff: **only `verified = 1` subscribers receive campaign sends** (Email, Web Push, SMS all filter on `verified`).

What it does NOT cover:

- The **marketing-consent** flag (person-level "agreed to marketing") — a *separate* gate from verification; see [[subscriber-vs-customer-consent]].
- The per-channel **unsubscribed / bounced** flags — see [[subscriber-vs-customer-channels]].
- Form-level GDPR / cookie consent at display time — see [[subscribe-forms-gdpr-consent]].

## Contrasts

- **Verification vs marketing consent** — different gates that BOTH must pass to send. `verified` = "the address is real and confirmed" (channel-level); marketing consent = "the person agreed to receive marketing" (person-level). A subscriber can be verified but not consented, or consented but unverified — either way, no send. The full eligibility predicate lives on [[subscriber-vs-customer-consent]].
- **Single vs double opt-in** — mark-as-verified trusts the submit (faster list growth, but unconfirmed addresses can be typos / fake / spam-trap); email-confirmation proves the address works before a single campaign reaches it (cleaner list, higher deliverability, lower bounce/complaint rate — but a confirmation step the visitor must complete, so some never confirm and stay unverified).
- **Verified vs subscribed** — submitting the form makes someone a *subscriber* immediately; being *verified* is a separate state that determines whether they can actually be emailed. An unverified subscriber still counts toward the list and segments, but campaigns skip them.

## Where it applies

- **The form builder** — the Mark-as-verified / Send-validation-email-link toggles ([[subscribe-forms-builder]]).
- **The submit cascade** — sets the initial `verified` state per the precedence above ([[subscribe-forms-submission-flow]]).
- **The confirmation email + verify link** — sent only on the email-confirm path; clicking it flips `verified = 1`.
- **Campaign sending** — every channel filters recipients to `verified = 1`; an unverified subscriber is silently skipped (the SMS channel even logs *"The subscriber has not confirmed his phone number"*). See [[marketing-campaigns]].
- **Programmatic capture** — subscribers created via [[api-subscribers]] / import set `verified` directly; a bulk import of an existing, already-confirmed list is the usual reason to mark verified without an email step.

## Related

- [[marketing-subscribers-subscribe-forms]] — the form that sets the initial verification state.
- [[subscribe-forms-submission-flow]] — the submit cascade + verify-action precedence.
- [[subscriber-vs-customer-consent]] — the **other** gate (marketing consent) that pairs with verification for the full send-eligibility predicate.
- [[subscriber-vs-customer-channels]] — per-channel `verified` / `unsubscribed` / `bounced` deliverability flags.
- [[marketing-campaigns]] — the consumer that only sends to verified subscribers.
- [[subscriber]] — the entity carrying the verified state.
- [[lead-capture-lifecycle]] — where verification sits in the form-to-campaign pipeline.

## Open Questions

- (verify) Whether re-submitting an unverified email re-sends the confirmation link, and whether a verify link expires.
