---
type: feature
nav_path: "Marketing → Segments → Subscribers → Detail & log modals"
route_name: segments.core_new.subscribers
route_path: /admin/marketing-new/segments/:id/subscribers
aliases: ["Subscriber details modal", "Subscriber logs modal", "Subscriber log in segment", "View subscriber from segment", "Модал с детайли за абонат"]
tags: [marketing, segments, subscribers, modals, log]
plan_gates: ["segments"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
> Part of [[marketing-segments-subscribers]]. See the hub for the other aspects (list, add, remove, shared data source).

# Subscribers in segment — detail & log modals

## Purpose

Two read-only modals let the merchant inspect a single subscriber without leaving the Subscribers-in-segment page. The **Subscriber details modal** answers "who is this person, in full?" (CRM record). The **Subscriber logs modal** answers "what marketing changes have happened to this person?" (per-subscriber audit feed). Together they let the merchant verify why a subscriber is — or isn't — in the segment, without switching to another screen.

## Where to find it

Both open from rows in the subscriber table (see [[segments-subscribers-list]]) on `/admin/marketing-new/segments/:id/subscribers`:

- **Subscriber details modal** — click the subscriber's **name**.
- **Subscriber logs modal** — click the **Log** button on the row.

## What the merchant can do here

- Open a full **read-only CRM record** for any subscriber from the name link.
- Open a paginated **marketing-change log** for any subscriber from the Log button.
- Close either modal and return to the table unchanged.

## What the merchant cannot do here

- **Cannot edit** the subscriber from the details modal — it is strictly read-only (only a "Close" button; the `hide-save` flag is set). To edit, go through [[marketing-subscribers]].
- **Cannot deep-link** to the details modal — opening / closing it pushes **no** query params into the URL; the modal state is purely local. (Contrast with [[marketing-segments-log]], where the equivalent modal does push `?modal=view&id=<id>`.)

## Settings & fields

### Subscriber details modal (read-only)

Clicking a subscriber's name opens a `CcModal` (size `xll`, title "Subscriber details"):

- Renders the same component as the modal on [[marketing-subscribers]].
- Shows the full CRM record — channels, RFM bucket, country, customer linkage, orders, segments membership, last-active, custom fields (see [[marketing-subscribers-custom-fields]]).
- **Read-only** — no edit / save controls; only a "Close" button in the footer.

### Subscriber logs modal

Clicking **Log** on a row opens a paginated modal with the subscriber's marketing-change log entries:

| Column | What it shows |
|--------|---------------|
| **Action** | Event type (added/removed channel, subscribed, unsubscribed, confirmed email, attach customer, added/removed tags, etc. — see [[marketing-segments-log]] for the full vocabulary). |
| **Info** | Free-form details (channel + identifier, etc.). |
| **Created at** | Event timestamp. |
| **Updated at** | Last-update timestamp. |

The modal paginates at **25 rows per page**. Closing it resets the subscriber id.

## Business rules

### Log modal is the same feed as the segment log, scoped to one subscriber

The Log modal uses the same marketing-change log feed that powers [[marketing-segments-log]], but filtered to a single subscriber within this segment context. So the vocabulary of Action values is identical between the two — the difference is scope: the segment log shows all subscribers' events for the segment; this modal shows one subscriber's events.

### Details modal is local-only state

Opening / closing the details modal does not touch the URL. The merchant cannot bookmark or share a link that re-opens the modal — it always opens fresh from a row click. This is a deliberate contrast with the segment-log page, where the view modal is deep-linkable.

## Related

- [[marketing-segments-subscribers]] — hub.
- [[segments-subscribers-list]] — the table rows these modals open from.
- [[marketing-subscribers]] — the page whose detail modal component is reused here.
- [[marketing-subscribers-custom-fields]] — custom fields shown in the details modal.
- [[marketing-segments-log]] — the segment-wide log feed; same Action vocabulary, deep-linkable view modal.
- [[subscriber]] — entity page.

## Open questions

No outstanding questions.
