---
type: feature
nav_path: "Marketing → Channels → Email notifications → Abandoned-cart recovery"
route_name: marketing-mails-list
route_path: /admin/marketing/omnichannel/mails/list
aliases: ["Abandoned cart recovery", "Abandoned cart email", "abandoned_restore_link", "abandoned_remainder", "abandoned_remainder_interval", "Cart restore link", "Изоставена количка", "Възстановяване на количка", "Имейл за изоставена количка"]
tags: [marketing, omnichannel, email, notifications, abandoned-cart, recovery]
plan_gates: ["abandoned_orders"]
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[marketing-omnichannel-mails-list]]. See the hub for related aspects (mail labels, editor modal, toggles & gating, variables, customisation limits).

# Email notifications — abandoned-cart recovery

## Purpose

The `abandoned_restore_link` mail is the **single highest-marketing-impact** transactional email in CloudCart. It sends a "come back to your cart" email with a one-click restore link to customers / subscribers whose carts went stale. Unlike the other labels, its delivery is owned by a **platform-level background job** with its own plan gate, settings, and eligibility rules.

## Where to find it

- The **template** is edited from the **Email notifications** list at `/admin/marketing/omnichannel/mails/list` (row labelled `abandoned_restore_link`). See [[omnichannel-mails-editor-modal]].
- The **send settings** (`abandoned_remainder`, `abandoned_remainder_interval`) live under **platform Settings**, NOT on this Vue page (verify exact admin route).
- The **plan gate** `abandoned_orders` is upsold at [[plan-features]].

## What the merchant can do here

- Edit the **template** (Name, Subject, HTML body, variables) like any other label.
- The Subject is the single highest-leverage edit — it drives the open rate, which drives recovery revenue.
- Use the **`{$link}`** variable to render the one-click restore URL (the most important variable in this template).
- Tune **`abandoned_remainder_interval`** in platform Settings — default 60 minutes, but stores with high checkout-completion latency may benefit from 90–120 minutes (less aggressive).

## Settings & fields

### Send-pipeline settings

| Field | Setting key | Default | Effect |
|---|---|---|---|
| **Abandoned-cart reminder on** | `abandoned_remainder` | `no` | When `yes`, the job runs against eligible carts |
| **Reminder interval (minutes)** | `abandoned_remainder_interval` | `60` | Cart is considered abandoned when `updated_at` is older than now minus this interval |

Both live in the central platform settings table — edited under platform Settings, not on the Email-notifications list page.

### Template variables (sampling)

The `abandoned_restore_link` label's `allowed_vars` includes (verify):

`{$link}` (the one-click restore URL), `{$shop_url}`, `{$shop_name}`, `{$logo}`, `{$customer_first_name}`, `{$customer_last_name}`, `{$customer_email}`, `{$product_list}` (cart contents).

The `{$link}` is what makes this email work — without it, the customer has nothing to click.

### UTM tagging on the link

The dispatched mail attaches `utm_campaign=abandoned_restore_link` to `{$link}` URLs. This lets the merchant slice abandoned-cart-driven revenue on the analytics side ([[analytics-pipeline]]).

## Business rules

### The `AbandonedCartSend` job — verified delivery path

- Runs on the **`system`** queue (NOT `campaigns`).
- Iterates abandoned carts where `date_sent IS NULL`.
- For each, calls `generateRestoreCode` which dispatches the actual email.
- For each e-mail that actually went out, increments the plan-year send counter `plan.count.email.abandoned_notification`.

### Job auto-destroy conditions

The job destroys itself (`EXECUTE_DESTROY`) at start if **any** are true:

- The merchant's plan does NOT include `abandoned_orders`.
- `abandoned_remainder` setting is NOT `yes`.
- No abandoned carts exist to send.

Mid-batch, if the plan-year allowance (`abandoned_notification`) is used up, the job stops processing further carts for that run. Within 12 hours the platform switches `abandoned_remainder` OFF and posts an Important alert in [[notifications]]; the remaining carts go out only after the allowance is restored AND the merchant turns the reminder back on.

### Eligibility — who actually receives the mail

A cart fires `abandoned_restore_link` only if **all** are true:

- The cart has at least one item.
- The cart's `updated_at` is older than `now - abandoned_remainder_interval`.
- The cart's `date_sent IS NULL` (never previously reminded).
- The recipient is either:
  - A **registered customer** ([[customer]]) on the cart, OR
  - An **email-channel subscriber** ([[subscriber]]) linked to the cart who is **verified** — unless the channel's `unconfirmed_send` setting is `true`, in which case unverified subscribers are also eligible.
- The cart's `updated_at` is **after** the subscriber's email-identification timestamp (prevents sending to subscribers whose identification post-dates the cart activity).

### Sent as promotional mail

Through the platform's Elastic Email transport, `abandoned_restore_link` goes out as promotional: the service adds its unsubscribe link and skips contacts who unsubscribed. Every other customer notification goes out as transactional. See [[abandoned-cart-channels]].

### Plan-billing accounting

Every e-mail sent by the job increments `plan.count.email.abandoned_notification`, a tally per plan year on every billing period ([[abandoned-cart-plan-quota]]). When the store hits the allowance ceiling, the job stops and the reminder is later switched off. The merchant either waits for the next plan year or extends the allowance at [[plan-features]], then turns the reminder back on.

### `date_sent` is set after one send — no spam

Once the platform sends `abandoned_restore_link` for a cart, the platform code is timestamped. The cart will **not** be re-sent — even if the customer continues to edit the cart and abandon it again. There is **no second reminder** in CloudCart's native flow (only one mail per cart instance) (verify whether a fresh cart for the same customer is treated as a new abandonment).

### Independent of the global toggle? NO — it's gated

The global `customer_email_notifications` toggle (see [[omnichannel-mails-toggles-gating]]) **DOES** gate this label like every other. Turning OFF the global switch suppresses abandoned-cart recovery alongside everything else.

### NOT a campaign — anti-spam policy not required

Despite being marketing-impactful, `abandoned_restore_link` is a **transactional** email (cart event triggered by customer action), not a campaign. The anti-spam policy (see [[marketing-campaigns-policy]]) does NOT gate it.

### Subscriber + customer routing

When the cart's identifier is a [[subscriber]] (subscribed via popup / form to the Email channel), the abandoned-cart mail is sent to the subscriber's verified email. When the cart's identifier is a registered customer, it's sent to the customer's account email. This is the only label in the catalogue with subscriber-based routing (verify).

## Recommended merchant use

- **Test the subject line.** A/B test recovery subjects in a non-platform A/B framework — CloudCart doesn't natively split-test transactional templates (verify).
- **Tune `abandoned_remainder_interval`.** 60 min is aggressive — good for impulse buys, bad for considered purchases. 90–120 min suits boutique / B2B stores.
- **Use `{$product_list}` in the body.** Listing the actual cart contents has measurable lift over generic "you left something" copy.
- **Add a discount in the template body.** Hardcoding a discount code in the body (e.g., `COMEBACK10`) is the highest-ROI tweak after subject-line testing.

## Related

- [[marketing-omnichannel-mails-list]] — hub.
- [[omnichannel-mails-labels]] — full label catalogue (this is one entry).
- [[omnichannel-mails-toggles-gating]] — the global toggle that gates this too.
- [[omnichannel-mails-variables]] — `{$link}` and cart-context variables.
- [[omnichannel-mails-editor-modal]] — editing the template.
- [[cart]] — the cart entity carrying `date_sent`.
- [[cart-vs-order-lifecycle]] — abandonment as a cart-lifecycle event.
- [[checkout-flow]] — where the cart's `updated_at` last bumps.
- [[subscriber]] — recipient when the cart is identifier-by-subscriber.
- [[customer]] — recipient when the cart is identifier-by-customer.
- [[marketing-channels-email]] — the channel hosting the `unconfirmed_send` flag.
- [[plan-features]] — `abandoned_orders` upsell screen.
- [[analytics-pipeline]] — UTM-driven abandoned-cart revenue attribution.

## Open questions

- 📡 **Second-reminder logic.** Whether a re-edited (post-restore) cart becomes eligible again (verify whether `date_sent` resets on edit).
- 📡 **Native A/B test of subjects.** Whether CloudCart will ever split-test transactional templates (verify roadmap).
