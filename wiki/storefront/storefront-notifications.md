---
type: storefront-page
route_name: subscribers.missing.product.form / subscribers.subscriptions
route_path: /subscribe-for-missing-product/{url_handle}, /subscribers/subscriptions/{hash}
themes_using: [all]
tags: [storefront, customer, notifications, back-in-stock, subscribers]
created: 2026-06-08
updated: 2026-06-11
source_count: 4
---

# Customer notifications (back-in-stock & subscription manager)

## Purpose

Two cooperating storefront flows:

1. **Back-in-stock subscribe** — on an out-of-stock product (or variant), the "Notify me when available" CTA opens a popup form so the visitor can subscribe to a notification for that exact product / variant.
2. **Subscription manager** — the per-recipient page reached from the unsubscribe / manage-preferences link inside transactional emails. Lets the recipient unsubscribe per channel (email, phone, push…) or stop everything.

There is **no "My notifications" tab inside the signed-in account area** — neither the [[customer-account]] sidebar nor the account screens list one. Both surfaces are reached from the product page (subscribe form) or from email links (manager).

## URL & route

Subscribe form (per-product, opens in a popup or its own URL):

- `subscribers.missing.product.form` → `GET /subscribe-for-missing-product/{url_handle}`
- Same path `POST` → store subscription (`XSS` middleware). Optional query string `?variant_id=<id>` narrows the subscription to a specific variant.

Subscription manager (per-subscriber hash):

- `subscribers.subscriptions` → `GET /subscribers/subscriptions/{hash}`
- Same path `POST` → update subscriptions / unsubscribe.
- Sibling routes in the same module: `subscribers.verify` (double-opt-in verify), `subscribers.save-uuid` (cross-device subscriber identity binding), `subscribers.subscriptions.cart` (cart-recovery view), `subscribers.subscriptions.init` / `.forms` / `.form` / `.form.store` / `.form.embed` (embeddable subscription-form module).

Both groups are registered by the Segments marketing module, **not** the main site routes, and are explicitly **not** wrapped in the `customer` middleware: a guest can subscribe to a missing-product alert, and the unsubscribe link must work for any recipient.

## How it loads

Subscribe form:

1. The product is resolved from `{url_handle}` (active products only); 404 if not found.
2. If `?variant_id=` is present, the variant is fetched (404 if not on that product). For multi-attribute variants, the popup title gains a suffix like `Product name (Size: M; Colour: Red)` so the customer sees exactly what they are subscribing to.
3. The form pre-fills from existing identity: from a known Subscriber it fills `email`, `phone`, `first_name`, `last_name`, `subscriber_id`; a logged-in Customer additionally sets `customer_id` so the Subscriber links to the customer record.
4. The body renders inside a `_popup` container (opened from the product page "Notify me" button — see [[products-missing-product]]).
5. `POST` is idempotent: re-subscribing for the same product/variant updates the existing subscription rather than duplicating it.

Subscription manager:

1. The `{hash}` is the encrypted subscriber id (only the part before the first `-` is used); 404 if invalid.
2. The subscriber's channels are loaded, filtered to channels that are installed + configured + active.
3. Channels are grouped by type, with per-channel "active identifier" state and labels (green checkmark when active).

## What the customer sees

Subscribe popup (`_popup` shell):

- Title: `sf.title.subscribe_missing_product`.
- Form id `subscribe-form-for-missing-product`, class `js-form-submit-ajax`.
- First name + last name fields (always shown).
- Email field — only when the email channel is configured on the store.
- Phone field with the `js-phone-intl` international module — only when the phone channel is configured.
- GDPR consent block with `gdpr_form='segment_subscription_popup'` (see [[apps-gdpr-acceptance]]).
- Invisible Google reCAPTCHA v3 field (`subscribe_us_id`) — score-checked server-side.
- Submit: `_button js-loading` with arrow icon, label `sf.button.subscribe`.

Subscription manager: a list of the subscriber's channel identifiers (e.g. `you@example.com`, `+359 88…`) with per-row "unsubscribe" controls plus a global "unsubscribe from everything" action. (verify exact UI)

## Storefront behaviour

- A back-in-stock subscription **belongs to a Subscriber**, not a Customer. A logged-in customer's subscription is still stored against the matching Subscriber row (linked via `customer_id`), which lets a guest's "notify me" later merge with their account on register / sign in (see `subscribers.save-uuid` for cross-device identity binding).
- Re-submitting the form for the same product/variant updates the existing subscription — no duplicates.
- Notification dispatch is async: when the product/variant flips to in-stock, the merchant's campaign machinery (see [[marketing-segments]]) sends the configured per-channel message to all matching subscribers.
- Channels on the form depend entirely on which campaign channels are installed/configured/active — disabling the email channel removes the email field; disabling the phone channel removes the phone field.
- reCAPTCHA v3 is mandatory; there is no toggle around it. (verify whether reCAPTCHA init no-ops when no key is configured)

## JavaScript behaviour

- Subscribe form uses `js-form-submit-ajax`. Inline script:
  - On global event `cc.subscribe.form.sent` → resets the form fields.
  - On `cc.ajax.error cc.ajax.success` → re-renders the reCAPTCHA target div and re-runs `onloadCallback` (200 ms timeout) so the next attempt gets a fresh token.
  - Wires the international-tel-input on the phone field.
- The product page "Notify me" button opens this form in a panel/popup — see [[products-missing-product]] for that side.
- The manager view reloads after each unsubscribe so the UI mirrors server state. (verify exact event names)
- Inline `<style>` patches `.w-100-tel.intl-tel-input { width: 100%; }` because the phone module defaults to `auto` width.

## Customisations available to the merchant

- Choose which channels are available for back-in-stock by enabling/disabling the matching campaign channel (see [[marketing-segments]]).
- Customise the notification email/SMS template per channel (the segments module's notification templates).
- Wire the unsubscribe URL into outgoing emails — most templates already include the `subscribers.subscriptions` route built from the encrypted subscriber id. (verify exact helper)
- Edit the popup GDPR copy via the GDPR app policies for context `segment_subscription_popup`.
- Re-skin the popup via CSS on `_popup`, `_popup-title`, `_popup-body`, `_contact-form`, `_form`, `_field` — the template uses underscore-prefixed legacy classes (not `cc-*`), so styling comes from the global module styling, not the cc-form theme.

## Theme variations

- The subscribe template lives **in the marketing-segments module**, not under `themes/`, so it is identical across every theme; visual differences come only from the CSS each theme ships for `_popup` / `_field` / `_button`. The manager view is bundled the same way. (verify manager path)
- This is unusual — most storefront pages live under the global theme templates. The module bundles its own views to keep the campaign experience consistent across stores.

## Known issues / by-design vs bug

- **By design**: no "My notifications" section in the [[customer-account]] sidebar; the only entry points are the per-product subscribe popup and the per-email manage link. Repeated support request.
- **By design**: re-submitting the same form updates the existing subscription, so customers occasionally see "subscription updated" instead of "subscription created" and assume something went wrong.
- **By design**: the `{hash}` is just the encrypted subscriber id, so any leaked unsubscribe URL is effectively a "manage this subscriber" capability — avoid forwarding unsubscribe links between inboxes.
- **Limitation**: there is no storefront UI to bulk-add or import "notify me" subscribers — that goes through admin → [[products-missing-product]] (the merchant-side view of who is waiting per product).
- **Limitation**: reCAPTCHA v3 is not gracefully degraded when no Google API key is configured — the form may fail silently. (verify)
- **Limitation**: the phone channel requires a fully configured campaign channel; without one, only the email field renders.

## Related

- [[storefront-architecture]]
- [[storefront-known-issues]]
- [[customer-account]]
- [[customer-orders]]
- [[products-missing-product]]
- [[marketing-segments]]
- [[apps-gdpr-acceptance]]
- [[apps-gdpr-policy]]
- [[products]]
- [[customers]]
- **settings-customers**

## Open questions

- What is the exact template path for the `/subscribers/subscriptions/{hash}` manager view?
- Does the manage page expose any "resubscribe" affordance, or is unsubscribe one-way?
- How does the `subscribers.save-uuid` cross-device flow interact with logged-in customers who switch devices?
- Is there a setting to surface the customer's active "notify me" subscriptions inside the account dashboard, or is that always email-driven?
- When a campaign channel is enabled but not yet configured (missing API key), does the channel field render and error on submit, or is it hidden?
