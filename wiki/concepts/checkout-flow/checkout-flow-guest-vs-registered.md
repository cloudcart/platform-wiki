---
type: concept
nav_path: "Concept → Checkout flow → Guest vs registered"
aliases: ["Guest checkout", "Registered checkout", "Guest vs member", "Convert guests into members", "Customer accounts setting", "registered", "guests", "both"]
tags: [orders, checkout, customer, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[checkout-flow]]. See the hub for the other aspects (cart entity, abandoned detection, submit-to-order, lifecycle overview, discounts & rules, events & webhooks).

# Checkout flow — Guest vs registered

## Definition

Every storefront checkout runs in one of two modes: **guest** (customer is not signed in) or **registered** (customer is signed in). The store's **Customer accounts** setting on [[settings-cart]] decides which modes are allowed (stored values `member` — sign-in required, `guest` — guest only, `both` — default, both allowed). The mode affects which Customer record the order is linked to, which discounts are eligible, whether saved addresses persist, and whether the guest becomes a registered Customer.

## Scope

Covered:

- The guest-vs-registered behaviour matrix at submit time.
- The three values of the **Customer accounts** setting (`member` / `guest` / `both`).
- The **Convert guests into members** setting and what happens when it's ON.
- Per-customer discount caps under each mode.

Not covered here:

- The full submit pipeline — see [[checkout-flow-submit-order-creation]].
- The `PreOrderCreated` listener that runs the guest-to-customer conversion — see [[checkout-flow-submit-order-creation]].
- Subscriber vs Customer distinction (marketing-consent surface) — see [[subscriber-vs-customer]].

## Contrasts

- **Guest record vs registered record** — a guest checkout is **not** anonymous: it finds or creates a Customer in the **Guests** group by the entered email (no password) and links the order to it. Later guest orders with the same email attach to the same record. So guests appear in the [[customers]] list and export; filter by group to separate them.
- **Convert guests into members OFF vs ON** — OFF keeps the buyer as a guest record that cannot sign in; ON turns that same record into a registered Customer when the order is placed, emails a generated password, and the customer can sign in to view their history.
- **Customer accounts = `member` vs `guest` vs `both`** — the storefront-side gate. `member` redirects unsigned-in visitors to register/sign in; `guest` allows guest checkout AND ALSO places orders as guests when a signed-in customer checks out (the order is NOT linked to the signed-in customer) (verify); `both` (default) allows both modes.
- **A digital product or a subscription in the cart overrides the setting** — such a cart never offers guest checkout, because the downloads (or the subscription) are reached from the buyer's account ([[digital-products]]). With `both` or `member` the customer step shows the **register form with a password** and the sign-in link; with `guest` it shows no form, only *"Only registered customers can purchase digital products"* (bg *"Само регистрирани клиенти могат да поръчват дигитални продукти"*; a subscription gets its own wording). A guest submit for such a cart is refused with the same message. A cart of physical products only follows the setting as usual.

## Where it applies

### Behaviour matrix at submit

| Behaviour | Guest checkout | Registered checkout |
|-----------|----------------|---------------------|
| Customer association | Linked to the guest Customer record (Guests group) found or created by email | Linked to the logged-in customer |
| Customer group | **Guests** (moved to the default group if converted) | Customer's existing group |
| Saved addresses | Not saved to a profile (snapshot lives only on the order) | Address can be saved to the customer's profile depending on the order-side checkbox |
| Discounts gated by `only_customer` | Blocked — *"Only registered customers can use this discount"* | Allowed |
| Per-customer cap on discount | Counted against the email address (anonymous) | Counted against `customer_id` |
| Customer accounts setting `member` | Blocked entirely — the storefront redirects to register / sign in | Allowed |
| Customer accounts setting `guest` | Allowed | Order is placed as guest (NOT linked to the signed-in customer) |
| Customer accounts setting `both` (default) | Allowed | Allowed |

### Convert guests into members

When **Convert guests into members** (`guest_to_customer`) is ON, the guest record itself is converted just before the order is saved: it moves to the default group, gets a generated password (sent in the welcome email), its email counts as confirmed, the buyer is signed in, and `customer.created` fires. It happens at the first order placed while the setting is ON; turning the setting on converts nobody retroactively, and earlier guest orders with that email are already on the same record, so the history is complete. Skipped when Customer accounts is `guest`. The marketing-consent flag stays on the record. Separately, a guest who signs in with a social account under the same email is converted (no password email). See [[checkout-flow-submit-order-creation]] for the placement of this step in the pipeline.

### Per-customer caps under each mode

A discount with a per-customer usage cap counts uses differently per mode:

- **Guest** — counted against `customer_email`. Two guest orders from the same email count against the same cap.
- **Registered** — counted against `customer_id`. Email changes don't bypass the cap.

This means a customer with an old guest order PLUS a new registered order against the same email can effectively get two uses of a "1 per customer" discount unless the merchant also has **Convert guests into members** ON (which retroactively unifies the rows).

## Related

- [[checkout-flow]] — hub.
- [[checkout-flow-submit-order-creation]] — the submit pipeline this mode-split applies to.
- [[customer]] — Customer entity that registered checkout attaches to.
- [[subscriber-vs-customer]] — the parallel Subscriber row carrying marketing consent.
- [[discount]] — the `only_customer` + per-customer-cap fields that depend on this mode.
- [[settings-cart]] — **Customer accounts** + **Convert guests into members** settings.
- [[customers]] — admin list of Customer rows.

## Open Questions

- Confirm the storefront message string for the blocked-guest discount case ("Only registered customers can use this discount") matches current translations (verify).
