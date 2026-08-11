---
type: concept
aliases: ["Subscriber deliverability", "Why didn't the subscriber receive the campaign", "Why didn't my email send", "Subscriber not receiving campaigns", "Reachability of a subscriber", "Bounced subscriber", "Unsubscribed subscriber", "Hard bounce handling", "Deliverability flags", "Защо абонатът не получи имейла", "Защо не се изпрати кампанията"]
tags: [marketing, subscribers, deliverability, campaigns, channels, troubleshooting, concepts]
plan_gates: []
created: 2026-06-30
updated: 2026-06-30
source_count: 2
---

# Subscriber deliverability — is this person reachable, and why not

## Definition

**Deliverability is the single question "can this campaign actually reach this subscriber right now?"** It is the synthesis of several independent flags that each, on their own, block a send — so the answer to the recurring support question *"I have them on my list, why didn't they get my email/SMS?"* is always *one* of these failing. A subscriber is reachable on a channel only when **all** of these hold (the platform's send query is literally `marketing = 1 AND verified = 1 AND unsubscribed = 0 AND bounced = 0`, plus the person-level Customer marketing flag):

| Flag | Set by | Meaning when it blocks |
|---|---|---|
| **channel exists** | the capture (form / order / import collected this identifier) | no email/phone on file for the channel → nothing to send to |
| **`verified`** | [[subscriber-double-optin\|opt-in]] (mark-as-verified or confirmed link) | address/number not confirmed → skipped (SMS logs *"The subscriber has not confirmed his phone number"*) |
| **`marketing`** | [[marketing-consent-collection\|consent]] (form / checkout / policy) | the person hasn't agreed to marketing |
| **`unsubscribed`** | the recipient clicking the unsubscribe footer | a **one-way latch** of explicit opt-out |
| **`bounced`** | the email subsystem detecting a hard bounce | the address doesn't exist / mailbox is permanently unavailable |

The per-flag data model lives on [[subscriber-vs-customer-channels]]; this concept is the **cross-cutting reachability + diagnostic** view that ties them together with verification and consent.

## Scope

Covered: the full reachability predicate as one picture; the **one-way latches** (`unsubscribed`, `bounced`) and why they don't auto-clear; the per-channel nature (reachable on Email ≠ reachable on SMS); the "why didn't X receive my campaign?" diagnostic walk. NOT covered: the raw flag storage / cascade mechanics (see [[subscriber-vs-customer-channels]]); the two-layer consent model (see [[subscriber-vs-customer-consent]]); the verification flow itself (see [[subscriber-double-optin]]); inbox placement / spam-folder rules on the receiving mail provider's side (outside the platform).

## Contrasts

- **Reachable vs subscribed** — being on the list (a subscriber) is necessary but not sufficient; reachability is the AND of the flags above. Most "they're on my list but didn't get it" cases are an unverified, unconsented, unsubscribed, or bounced channel.
- **Intent latches vs state flags** — `unsubscribed` (recipient said no) and `bounced` (address is dead) are **one-way**: the platform does not silently re-enable them; `marketing` and `verified` can move in both directions. An unsubscribe is a strong, durable signal — re-subscribing requires a fresh, explicit opt-in, not a merchant flip.
- **Per-channel, not per-person** — a subscriber bounced on Email can still be perfectly reachable on Web Push or SMS; reachability is asked per channel because each channel carries its own flags.
- **Platform reachability vs inbox placement** — passing every flag means the platform *sends*; whether it lands in the inbox vs spam is the receiving provider's call (sender reputation, content) and is not modelled here.

## Where it applies

### The "why didn't they receive it?" diagnostic

Walk the predicate for the channel in question:

1. **Is there a channel identifier?** No email/phone captured → nothing to send.
2. **`verified`?** Unconfirmed address/number → skipped — fix via the opt-in flow ([[subscriber-double-optin]]).
3. **`marketing` consent?** Not consented → blocked — see [[marketing-consent-collection]].
4. **`unsubscribed`?** They opted out → cannot be re-added by the merchant; needs a new opt-in.
5. **`bounced`?** Hard bounce → the address is dead; a typo capture is the common cause (a reason to prefer double opt-in).
6. **In the campaign's segment?** Even fully reachable, a subscriber only gets a campaign whose [[subscriber-segmentation\|segment]] they belong to.

The first failing step is the answer.

### At campaign send

Every channel (Email, Web Push, SMS) re-applies the predicate at send time, so a flag that flips *after* the campaign is scheduled (a late unsubscribe / bounce) still removes the recipient. See [[marketing-campaigns]].

## Related

- [[subscriber-vs-customer-channels]] — the per-channel flag data model (`marketing` / `verified` / `unsubscribed` / `bounced`).
- [[subscriber-vs-customer-consent]] — the two-layer consent gate (Customer flag + per-channel `marketing`).
- [[subscriber-double-optin]] — how `verified` is set / confirmed.
- [[marketing-consent-collection]] — how `marketing` consent is collected + proven.
- [[subscriber-segmentation]] — the segment-membership condition that also gates who receives a campaign.
- [[marketing-campaigns]] — the send pipeline that applies the predicate.

## Open Questions

- (verify) Whether soft bounces are tracked distinctly from hard bounces, and any retry/threshold before `bounced` latches.
