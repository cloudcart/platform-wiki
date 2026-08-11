---
type: feature
nav_path: "Payment Providers → Voucher"
route_name: apps.voucher.settings
route_path: /admin/payment-providers/voucher
aliases: ["Voucher", "Gift card payment", "Store credit", "Ваучер"]
tags: [paymentproviders, payment-providers, voucher, gift-card, store-credit, offline]
plan_gates: []
created: 2026-05-22
updated: 2026-05-22
source_count: 0
---
# Voucher

## Purpose

**Voucher** is a manual / offline payment method letting the merchant accept gift cards, store credit, vouchers, coupons, or any other "paid via printed slip" arrangement. Different from automated gateways — Voucher doesn't talk to any external API. The customer picks Voucher at checkout, sees the merchant's description (e.g., *"Pay with a voucher you have received via promotion"*), submits the order, and the merchant manually verifies + accepts the voucher offline (e.g., scans / reads the voucher code from the customer's email).

Used by merchants who:
- Run a separate gift-card / loyalty-points system not integrated with CloudCart.
- Accept promotional vouchers customers redeem manually.
- Want a "Pay with store credit" option for VIP customers (combined with [[customers-custom-groups]] restriction).

## Where to find it

Sidebar → **Settings → Payment methods** → **Voucher** row → **Settings**.

The page's breadcrumb reads "Payment providers → Voucher". The route is `/admin/payment-providers/voucher`.

## What the merchant can do here

- Set a **description** (the only configurable field) — the text the customer sees at checkout explaining how the voucher payment works.
- Activate / deactivate the method via [[settings-payment-providers]].
- Restrict to specific customer groups via [[settings-payment-providers]] common per-method settings (e.g., only VIP customers see Voucher).
- Set per-method min / max order amount via [[settings-payment-providers]] common fields.

What the merchant **cannot** do here:
- Auto-validate voucher codes — the integration has no validation logic, no code lookup, no balance tracking. The merchant verifies vouchers manually (offline).
- Track voucher usage / remaining balance per code.
- Integrate with an external gift-card system from this page.

## Settings & fields

There's exactly ONE configurable field on the Voucher integration:

| Field | Required | Max | What it is |
|-------|----------|-----|------------|
| **Description** (`description`) | yes | 50,000 chars | The customer-facing explanation shown at checkout when the customer picks Voucher. Supports HTML for richer formatting. |

### Validation messages (exact strings)

- *"Cash on delivery: description is required."* — when `description` is empty. (The message text reuses the Cash on delivery wording — a code-level quirk; the merchant should still set a Voucher-specific description.)
- *"Cash on delivery: description should be less than 50000 characters long."* — when description exceeds 50k characters. (Same wording quirk.)

So Voucher is the **simplest payment integration to configure** — just a description.

## Business rules

### No automated processing — order is created in 'pending' status

When the customer picks Voucher and submits the order:
1. The order is created with payment status `pending`.
2. The merchant receives the order notification.
3. The merchant verifies the voucher offline (e.g., asks the customer for the code, looks it up in their gift-card system).
4. Once verified, the merchant manually marks the order as paid via [[orders-payment-mark-paid]].

There's no automatic capture, no callback, no webhook — Voucher is a fully manual flow.

### Description is the merchant's instruction text

The description shown at checkout is the merchant's communication channel. Best practices:
- Explain what kind of voucher is accepted ("gift card", "promo code", "store credit").
- Tell the customer what to do next ("you'll receive an email with instructions to redeem").
- Set expectations on timing ("we'll verify within 24 hours").

### Restrict to specific customer groups for store-credit use cases

A common pattern: the merchant creates a VIP customer group (via [[customers-custom-groups]]), restricts Voucher to that group, and uses Voucher as a "store credit" option for repeat customers. Regular customers don't see Voucher at checkout.

### No refund logic

Refunding a Voucher payment is fully manual. The merchant marks the CloudCart order as refunded via [[orders-payment-refund]]; they then re-issue the voucher (or refund the customer separately) outside CloudCart.

### Permission

Standard payment-providers permission scope.

## Related

- [[settings-payment-providers]] — payment methods landing page.
- [[payment-providers]] — payment providers hub.
- [[payment-providers-cod]] — Cash on delivery (similar manual-confirm pattern).
- [[payment-providers-bwt]] — Bank wire transfer (also offline / manual confirmation).
- [[orders-payment-mark-paid]] — manual paid action used after voucher verification.
- [[orders-payment-refund]] — manual refund flow when reversing a voucher payment.
- [[customers-custom-groups]] — typical group-restriction use case for Voucher as store credit.
- [[marketing-discounts]] — alternative if the goal is automated coupon redemption (use Discount codes, not Voucher).

## How it works (verified against backend)

### Single-field integration

The Voucher integration is a thin shell. No external API calls, no signature validation, no callback handling — purely a checkout-side payment method that creates a pending order.

### Validation message text is a copy-paste from COD

The validation strings literally start with *"Cash on delivery: ..."* — this is leftover wording from when the Voucher integration was forked from the Cash on Delivery integration. The merchant sees these messages only if they leave the description empty; the runtime customer experience uses the merchant's own description text.

### 50000-character description ceiling

The description max length is **50,000 characters** — generous enough for the merchant to include HTML formatting, links to a separate gift-card portal, multiple paragraphs of legal text, etc. Most merchants use 100-500 characters.

## Open questions

(none)

## Verified — Voucher vs Discount + multi-payment

- **Voucher vs Discount codes**: pick **Voucher** when the redemption is OFFLINE / handled by an external system (gift-card store, manual verification, paper voucher) — the payment row stays Requested until the merchant manually marks it paid. Pick **Discount codes** ([[marketing-discounts]]) when the redemption is fully automated inside CloudCart (the discount is applied at checkout and the customer pays the discounted total via a normal payment provider).
- **Combined with other payment methods**: NOT supported. CloudCart's order model has exactly one payment per order (the platform code). A customer whose voucher covers only part of the order cannot pair Voucher with another payment method in CloudCart — the merchant must either accept the entire order as Voucher (and reconcile the difference offline) or have the customer place a separate order for the remainder using a different method.
