---
type: entity
aliases: ["Email merge tags", "Email template variables", "Merge variables", "Magic URLs", "Dynamic discount code variable", "Merge tag dropdown", "Променливи в имейл шаблон"]
tags: [marketing, email, templates, variables, merge-tags, entity]
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[email-template]]. See the hub for the other aspects (transactional family, campaign authoring, channel delivery).

# Email Template — merge variables & magic URLs

## Identity

**Merge variables** (merge tags) are the `{$...}` placeholders an Email Template can embed in its subject and HTML body; the platform substitutes them against the actual recipient's data at send time. The merchant inserts them via the editor's **variable dropdown** — they never type raw placeholders blind.

The allow-list is **per-template**:

- **Transactional templates** ([[email-template-transactional]]) have a fixed allowed-vars set per event label. The set is served by the platform when the editor opens (the variables endpoint `/admin/api/core/marketing/customer-mails/{id}/variables` returns the list for that template).
- **Campaign templates** ([[email-template-campaign-authoring]]) additionally support dynamic-discount variables (`{$dynamic_discount_code}`, `{$discount_code:CODE}`) and segment-bound variables (`{$triggered_products:N}`).

## Aliases

- **Merge tags** / **merge variables** — the canonical terms for the `{$...}` placeholders.
- **Magic URLs** — the encrypted one-time links (cart, checkout, unsubscribe, verify) exposed as variables.
- **Variable dropdown** — the editor control the merchant uses to insert them.
- **Променливи в имейл шаблон** — Bulgarian phrasing.

## Key Attributes

### Content & catalogue variables

| Variable | Resolves to | Notes |
|----------|-------------|-------|
| `{$customer_first_name}`, `{$order_id}`, `{$tracking_link}`, … | Recipient / order fields | Per-event allow-list on transactional templates. Some events require certain vars in the subject (order events require `{$order_id}`). |
| `{$triggered_products:N}` | The first N products that triggered the campaign | N is **1–12**; any larger requested count is silently clamped to 12 (`triggerProductsLimit` override). Resolves against the campaign's [[segment]]. |
| `{$discount_code:CODE}` | A **link to the cart with that discount applied** (not the code text) | The dropdown is populated with one entry per active [[discount|Discount]] whose code is **not** EAN8/EAN13. |
| `{$dynamic_discount_code}` | A new code per recipient | Campaign-only. Needs the `discount-code-pro` plan feature and a segment with triggered products; each recipient gets a fresh Code PRO code valid only for their triggered products. `{$generate_discount_code:N%}` is never replaced (removed at send). |

The store itself is available only as `{$shop_name}`, `{$shop_url}` and `{$logo}`. There is **no variable for the store's phone or address**; to show them, type them into the template text (they are kept on Settings → Invoicing, [[settings-invoicing-issuer-block]]). `{$contact_phone}` exists only in the admin's contact-form notification and is the phone the visitor entered.

### Magic URLs (encrypted one-time links)

| Variable | Resolves to | Behaviour |
|----------|-------------|-----------|
| `{$cart_url}` | `/subscribers/cart/{encrypted_id-cart.list}` | One-time-encrypted URL that auto-logs the subscriber in to their cart without a password. Used for abandoned-cart recovery. |
| `{$checkout_url}` | `/subscribers/cart/{encrypted_id-checkout}` | Same as above but lands on checkout. |
| `{$unsubscribe_url}` | `/subscribers/subscriptions/{encrypted_id-timestamp}` | Per subscriber. The token carries the send time, but the page reads only the subscriber part, so the link keeps working after the campaign. **Campaign-only**: notification templates neither offer nor fill it in (typed into one, it stays as literal text). Opens the subscription page on [[storefront-notifications]]. |
| `{$verify_url}` | `/subscribers/verify/{encrypted_id}` | The email-verification link is exposed as a merge tag **ONLY on the Email channel** — SMS, Viber, and Web Push do not surface this variable. |

The `{$cart_url}` / `{$checkout_url}` links power [[abandoned-cart-recovery]]: the subscriber clicks and is auto-logged-in to resume their session.

## Where it appears

- [[marketing-campaigns-message-template]] — the campaign editor's variable dropdown where most of these are inserted.
- [[marketing-omnichannel-mails-list]] — transactional templates expose their per-event allowed-vars list in the same editor.
- [[abandoned-cart-recovery]] — relies on the `{$cart_url}` / `{$checkout_url}` magic URLs.
- [[marketing-channels-email]] — the channel that surfaces `{$verify_url}` (Email-only).

## Related

- [[email-template]] — hub.
- [[email-template-transactional]] — per-event allowed-vars lists.
- [[email-template-campaign-authoring]] — where dynamic-discount and triggered-products vars are authored.
- [[discount]] — the source of `{$discount_code:CODE}` / `{$dynamic_discount_code}` entries.
- [[marketing-discounts-code-pro]] — the code type `{$dynamic_discount_code}` generates.
- [[segment]] — the audience that `{$triggered_products:N}` resolves against.
- [[subscriber]] — the identity the encrypted magic URLs auto-log-in.
- [[cart]] — the object the `{$cart_url}` / `abandoned_restore_link` send recovers.

## Open Questions

- ⏸️ Whether the per-event transactional allowed-vars list is documented anywhere merchant-facing, or is only discoverable through the editor's dropdown. `(verify)`
