---
type: feature
nav_path: "Marketing → Subscribers → Channels"
route_name: subscribers.channels
route_path: /admin/marketing-new/subscribers/:id/channels
aliases: ["Subscriber channels", "Subscriber channel identifiers", "Channel merge", "Subscriber merge", "Subscriber identity resolution"]
tags: [marketing, subscribers, channels, merge, identity]
plan_gates: ["subscribers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-subscribers]]. See the hub for related aspects (list view, bulk actions, detail modal, import, settings, lifecycle).

# Subscribers — channels and identity resolution

## Purpose

Every subscriber is a wrapper around 1+ per-channel rows. The channels aspect documents the 4 channel types, the identifier-uniqueness rule per channel, the merge flow that resolves duplicates, and the 4-step identity-resolution cascade that decides whether a new contact merges into an existing subscriber or creates a fresh row.

## Where to find it

- The Channels card on the [[subscribers-detail-modal]] (route `admin.subscribers.channels`).
- The per-channel edit side modal, opened by clicking a channel-name link.
- The merge flow at route `admin.subscribers.channels.merge`.

## What the merchant can do here

- Add a channel to a subscriber (Email / Phone / Messenger / WebPush).
- Edit an existing channel's identifier and flags.
- Delete a channel row from a subscriber (leaves the subscriber alive, possibly as a ghost).
- Merge two subscribers when the merchant tries to set a duplicate channel-identifier.

## Settings & fields

### The 4 channel types

Every subscriber has one or more **channel** rows, one per channel they're subscribed to:

| Constant | Label | Purpose |
|----------|-------|---------|
| `Email` | "Emails" | Default — `channel_identifier` is the email address. |
| `Phone` | "Phone" | SMS sends; `channel_identifier` is the phone number. Also covers Viber (`channel.Viber` label). |
| `Messenger` | "Messenger" | Facebook Messenger sends; `channel_identifier` is the FB Page-Scoped User ID (PSID). |
| `WebPush` | "Web Push" | Browser push notifications; `channel_identifier` is the push subscription identifier. |

### Per-channel editable fields

Per channel, the merchant can edit (subscriber detail → Channels → row):

- `channel_identifier` (the email / phone / PSID itself).
- `marketing` (accept-marketing toggle for this channel).
- `verified` (only meaningful for Email).
- `bounced` (set by the email subsystem on a hard bounce).
- `unsubscribed` (set when the subscriber clicks unsubscribe in an email footer).

## Business rules

### Channel-identifier uniqueness is enforced per channel

Duplicate-identifier collision is caught at save time and surfaced as the merge prompt:

> *"This identifier is already in use by another subscriber. Do you want to merge the subscribers?"*

With a link to the merge flow (`admin.subscribers.channels.merge`). The uniqueness scope is **(channel, channel_identifier)** — meaning the same email address can't appear as Email on two subscribers, but it CAN appear as Email on subscriber A and as some other channel's identifier (unrelated) on subscriber B.

### The merge flow — duplicate-channel resolution

When the merchant triggers the merge prompt:

- The platform identifies the duplicate channel + any non-duplicate channels on the OTHER subscriber.
- The merchant picks which fields to keep, including matched-this-subscriber, matched-other-channels, and non-matched-other-channels.
- The platform folds the second subscriber's history into the first (orders, carts, segments, tags, custom fields, events) then deletes the second row.

**This is the only safe way to combine two records that ended up representing the same person.** Directly editing the duplicate identifier without using the merge UI would lose the second row's history.

A separate **background merge sweep** (runs every 24 hours, one run at a time) identifies and merges duplicate subscribers detected across channels — this is NOT the user-triggered flow above; it catches cases the merchant hasn't manually resolved.

### Identity resolution — 4-step cascade

When saving a contact by channel, the platform looks up an existing subscriber in this fallback order before creating a new row:

1. **Channel match** — look for a channel row matching the same `(channel, channel_identifier)` pair. The most specific lookup.
2. **Customer match** — if step 1 failed AND a `customer_id` is provided, find a subscriber linked to the same customer.
3. **UUID match** — if the browser-tracking cookie `uuid` is provided, look up the subscriber carrying that uuid.
4. **Parent subscriber id** — if explicitly passed (e.g., to chain multiple channel additions to one subscriber row).

Only if all four fail does the platform create a brand-new subscriber row.

**Practical implication:** an anonymous visitor browsing with a cookie, who then types an email into a popup, gets merged with the cookie-tracked subscriber row — NOT created as a separate subscriber. The merge fires an `identified_by` log entry with the channel that did the matching.

### Deleted channel logs an event

Whenever a channel is deleted (single or cascade), the platform writes a `remove_channel` entry to the subscriber's marketing activity log with the channel + identifier + flags. So a hard-delete cascade produces N `remove_channel` events plus the subscriber's own `subscriber.deleted` webhook (see [[settings-hooks]] + [[subscribers-lifecycle]]).

### Email verification gates campaign sends

When a subscriber's Email channel has `verified = 0`, most campaigns will NOT send to that address. Three ways to verify:

1. Send the verification email via the "Send email with link to verify" action ("Email confirmation for subscription in store:site_name").
2. Mark verified on import ("Mark all as verified" or "Email verification" on import dialog — see [[subscribers-import]]).
3. Manually toggling `verified = 1` on the channel edit form.

Clicking the verification email link returns the storefront with the success message *"You have successfully verified your email address."* Unverified addresses show a tooltip on the channel row: *"No message will be sent to this email because it has not been verified."*

### Ghost subscribers — zero channels

A subscriber with all channels removed becomes a "ghost" — queryable via `no_channels = Yes` on the [[subscribers-list-view]] filter. Ghosts cannot receive any campaign send. They usually arise when:

- A merchant deletes all per-channel rows but not the subscriber.
- A uuid-tracked anonymous visitor never typed any identifier.
- GDPR erasure stripped identifying data but the subscriber id was retained as a no-PII marker.

## Related

- [[marketing-subscribers]] — hub.
- [[subscribers-detail-modal]] — surfaces the channels card + edit modal.
- [[subscribers-import]] — verification toggles on import; identifier normalisation (E.164).
- [[subscribers-lifecycle]] — cascade delete + the marketing-flip asymmetry that affects channel rows.
- [[notification-delivery]] — how per-channel sends are dispatched.
- [[settings-hooks]] — `subscriber.updated` / `subscriber.deleted` webhook on channel changes.
- [[subscriber]] — entity.
- [[customer]] — Step 2 of the resolution cascade matches on the linked customer.

## Open questions

None.
