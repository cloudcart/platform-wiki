---
type: feature
nav_path: "Orders → Abandoned → Restore link"
route_name: storefront.restoreAbandoned
route_path: /restore-abandoned/{code}/{source}/{discount_code?}
aliases: ["Restore link", "Cart recovery link", "Abandoned restore URL", "Recovery email link", "Restore code", "Линк за възстановяване на количка"]
tags: [orders, abandoned, restore-link, cart-recovery, attribution, utm]
plan_gates: ["abandoned_notification"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-abandoned]]. See the hub for the other aspects (list view, detail view, eligibility, auto-recovery, plan gates, cart lifecycle).

# Abandoned carts — Restore link

## Purpose

Documents the **restore-link** the customer receives in the abandoned-cart recovery email: how the URL is built, the unique-code generation, UTM stamping for attribution, the `date_sent` tracking that prevents bulk re-sends, and the two recognised recovery-source channels (`email` + `messenger`).

This is what the customer ACTUALLY clicks. When the click lands, the storefront restores the cart contents to a fresh checkout session and (if attached) applies the recovery discount code automatically. The resulting order's metadata captures the recovery source so it shows up in [[orders]] under the **Recovered source** filter.

## Where to find it

Not a screen the merchant configures directly — the merchant triggers it by clicking Send on [[orders-abandoned-list-view]] (bulk) or [[orders-abandoned-detail-view]] (per-cart), or it fires automatically via [[orders-abandoned-auto-recovery]]. The customer receives the URL in the recovery email.

## What the merchant can do here

Nothing on this page directly — the customer interacts with the link. The merchant observes the outcome via:

- **Recovered source filter on [[orders]]** — orders restored via the link surface with their `restore_source` meta set.
- **UTM attribution in [[marketing-dashboard]]** — recovered orders carry `utm_campaign=abandoned_restore_link` and the configured `utm_source`.
- **Per-cart "Restore link last sent: <date>" timestamp on [[orders-abandoned-detail-view]]** — visible after a successful send.

## Settings & fields

### Restore URL format

`/restore-abandoned/{code}/{source}/{discount_code?}?utm_source=...&utm_campaign=abandoned_restore_link`

- `{code}` — unique restore code, freshly generated on every Send (manual single-cart, bulk, or scheduled auto-recovery).
- `{source}` — the recovery channel. Two values supported in the platform's translation files:
  - `email` — restore link delivered via outbound email (the default flow this cluster drives).
  - `messenger` — restore link delivered via Facebook Messenger Bot integration.
  - **SMS, push, and manual restore sources are NOT currently emitted.** When a customer returns through one of these channels, the resulting order's `restore_source` meta is set to one of these two values only.
- `{discount_code?}` — optional recovery discount code attached at send time. When the customer clicks the link, the storefront auto-applies the code. See [[marketing-discounts]].

### UTM stamping

Every restore link is stamped with UTM parameters so the recovered order's source is attributable in [[marketing-dashboard]]. `utm_campaign=abandoned_restore_link` is constant; `utm_source` reflects the channel.

## Business rules

### Unique code per send

Each send generates a fresh restore code. The code is consumed when the customer clicks; subsequent clicks on the same URL won't restore a second time. If the merchant re-sends the same cart (via per-cart Send from [[orders-abandoned-detail-view]]), a new code is generated and the previous one is invalidated.

### `date_sent` tracking — bulk vs per-cart differ

After a successful send, the cart's `date_sent` timestamp is recorded. This is visible in the abandoned-cart detail view as *"Restore link last sent: <date>"* (`order.info.abandoned_restore_last_sent_date`).

- **Bulk Send restore link** (from [[orders-abandoned-list-view]]) → silently SKIPS carts that already have a `date_sent` value. The bulk query filter excludes already-sent carts. The merchant cannot bulk-resend.
- **Per-cart Send** (from [[orders-abandoned-detail-view]]) → the `date_sent` check is currently disabled in code, so a single-cart resend will succeed and overwrite the timestamp.
- **Scheduled auto-recovery** ([[orders-abandoned-auto-recovery]]) → also filters `whereNull('date_sent')` — auto-job sends ONCE per cart, ever.

### Per-cart Send response — JS DOM update

When the per-cart Send button succeeds, the response payload includes a `response` field with the localised string *"Restore link last sent: <datetime>"*. The detail view's JavaScript inserts this string into the `#js-sent-date` element so the merchant sees the updated timestamp without a full page reload.

### Recovery attribution in [[orders]]

When the customer returns through a restore link and places an order, the order's metadata records the source (`email` or `messenger`). This surfaces in the orders list under the **Recovered source** filter (see [[orders]] → filters). The UTM parameters surface in [[marketing-dashboard]] under the `abandoned_restore_link` campaign.

### Sends are queued — restore email arrives within minutes

The recovery email is dispatched onto the order-events queue with a **10-second delay** (same pipeline as status-change emails). Typical delivery: under 5 minutes from when the merchant clicks Send.

### Send response messages

The Send actions return these messages (verbatim, with translation keys):

- **Per-cart success** → *"Email sent to client"* (`order.succ.abandoned_email_sent_to_client`).
- **Bulk success** → *"X emails sent"* (`order.succ.abandoned_%d_emails_sent`).
- **Bulk zero-sent** → *"No emails were sent"* (`order.err.abandoned_no_emails_sent`).
- **Cart no longer exists** (404) → *"Order no longer exists"* (`order.err.order_no_longer_exists`).
- **Plan limit hit** → a plan-warning message naming the `abandoned_notification` feature and the current usage count, with a link to the plan-features upsell page.

### Side effect on Send

Every successful Send increments `plan.count.email.abandoned_notification` — the counter checked by the numeric cap. The counter is a permanent setting and does NOT reset on plan renewal — see [[orders-abandoned-plan-gates]].

## Plan gates

- `abandoned_notification` — numeric cap on sends per period; blocks the Send when the running counter exceeds the cap.

## Related

- [[orders-abandoned]] — hub.
- [[orders-abandoned-list-view]] — bulk Send context.
- [[orders-abandoned-detail-view]] — per-cart Send context.
- [[orders-abandoned-eligibility]] — what blocks a Send before this URL is generated.
- [[orders-abandoned-auto-recovery]] — the scheduled job that emits the same URL.
- [[orders-abandoned-plan-gates]] — `abandoned_notification` counter mechanics.
- [[orders]] — Recovered source filter.
- [[marketing-discounts]] — recovery discount codes carried in `{discount_code?}`.
- [[marketing-dashboard]] — UTM attribution surface.

## Open questions

None.
