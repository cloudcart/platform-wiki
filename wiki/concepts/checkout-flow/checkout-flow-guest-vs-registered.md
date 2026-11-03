---
type: concept
nav_path: "Concept → Checkout flow → Guest vs registered"
aliases: ["Guest checkout", "Registered checkout", "Guest vs member", "Convert guests into members", "Customer accounts setting", "registered", "guests", "both"]
tags: [orders, checkout, customer, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[checkout-flow]]. See the hub for the other aspects (cart entity, abandoned detection, submit-to-order, lifecycle overview, discounts & rules, events & webhooks).

# Checkout flow — Guest vs registered

## Definition

Every storefront checkout runs in one of two modes: **guest** (customer is not signed in) or **registered** (customer is signed in). The store's **Customer accounts** setting on [[settings-cart]] decides which modes are allowed (`registered` — sign-in required, `guests` — guest only, `both` — default, both allowed). The mode affects how the customer is linked to the resulting order, which discounts are eligible, whether saved addresses persist, and whether a Customer account is auto-created post-checkout.

## Scope

Covered:

- The guest-vs-registered behaviour matrix at submit time.
- The three values of the **Customer accounts** setting (`registered` / `guests` / `both`).
- The **Convert guests into members** setting and what happens when it's ON.
- Per-customer discount caps under each mode.

Not covered here:

- The full submit pipeline — see [[checkout-flow-submit-order-creation]].
- The `PreOrderCreated` listener that runs the guest-to-customer conversion — see [[checkout-flow-submit-order-creation]].
- Subscriber vs Customer distinction (marketing-consent surface) — see [[subscriber-vs-customer]].

## Contrasts

- **Guest mode `customer_id = NULL` vs registered mode `customer_id` set** — the most consequential field difference. Guest orders aggregate by `customer_email`; registered orders aggregate by `customer_id`. Per-customer discount caps follow this split.
- **Convert guests into members OFF vs ON** — OFF leaves guest orders unattached to any Customer row; ON creates a Customer account post-checkout, emails a generated password, and the customer can sign in later to view their history.
- **Customer accounts = `registered` vs `guests` vs `both`** — the storefront-side gate. `registered` redirects unsigned-in visitors to register/sign in; `guests` allows guest checkout AND ALSO places orders as guests when a signed-in customer checks out (the order is NOT linked to the signed-in customer); `both` (default) allows both modes.

## Where it applies

### Behaviour matrix at submit

| Behaviour | Guest checkout | Registered checkout |
|-----------|----------------|---------------------|
| Customer association | `customer_id = NULL`, email + first / last name still captured | `customer_id` set to the logged-in customer |
| Customer group | Default group (or guest-group ID if configured) | Customer's existing group |
| Saved addresses | Not saved to a profile (snapshot lives only on the order) | Address can be saved to the customer's profile depending on the order-side checkbox |
| Discounts gated by `only_customer` | Blocked — *"Only registered customers can use this discount"* | Allowed |
| Per-customer cap on discount | Counted against the email address (anonymous) | Counted against `customer_id` |
| Customer accounts setting `registered` | Blocked entirely — the storefront redirects to register / sign in | Allowed |
| Customer accounts setting `guests` | Allowed | Order is placed as guest (NOT linked to the signed-in customer) |
| Customer accounts setting `both` (default) | Allowed | Allowed |

### Convert guests into members

When **Convert guests into members** (`guest_to_customer`) is ON, guest orders also create a Customer account post-checkout — the customer receives an email with a generated password and can sign in to view their order history. The conversion runs inside the `PreOrderCreated` listener BEFORE the order row is persisted, so the resulting order is born linked to the freshly-promoted Customer record. The marketing-consent flag from the guest row is preserved on the new Customer. See [[checkout-flow-submit-order-creation]] for the placement of this step in the pipeline.

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

- Confirm `guest_to_customer` is the exact setting key for **Convert guests into members** (verify).
- Confirm the storefront message string for the blocked-guest discount case ("Only registered customers can use this discount") matches current translations (verify).
