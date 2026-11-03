---
type: feature
nav_path: "Payment Providers → CIB Bank → Save-card & refunds"
route_name: apps.cib_bank.settings
route_path: /admin/payment-providers/cib_bank
aliases: ["CIB Bank save card", "CIB OCID", "CIB tokenised card", "CIB refund", "CIB retransfer", "CIB HUF currency", "CIB Forint conversion"]
tags: [paymentproviders, payment-providers, cib-bank, hungary, card, save-card, refund, huf]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# CIB Bank — save-card, refunds & currency

> Part of [[payment-providers-cib-bank]]. See the hub for the other aspects (settings & DES file, payment flow).

## Purpose

This page covers the [[payment-providers-cib-bank|CIB Bank]] features that act on a *completed* payment or a *returning* customer: the **save-card** mechanism (tokenised cards for signed-in shoppers), the **refund** flow with its automatic `refund` → `retransfer` fallback, and the **forced HUF currency** with auto-conversion. The config switch lives on [[cib-bank-settings]]; the core charge flow on [[cib-bank-payment-flow]].

## Where to find it

- **Save customer card** is a switch on Sidebar → **Payment Providers** → **CIB Bank** (`/admin/payment-providers/cib_bank`) — see [[cib-bank-settings]].
- **Refunds** are initiated from the order page via **Refund payment** — see [[orders-payment-refund]].
- **Saved cards** appear on the customer profile — see [[customers-details-payments]].

## What the merchant can do here

- **Enable Save customer card** so returning signed-in customers pay with a stored card without re-entering details.
- **Refund a completed CIB payment** from the order page; the platform handles the `refund` → `retransfer` fallback automatically — the merchant does not choose which method to call.
- **View a customer's saved CIB cards** on their profile (only shown when at least one card is on file).

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Save customer card** (`configuration.save_card`) | When `yes` and the customer is signed in, the next payment can run with a stored CIB token (OCID) without re-entering card details. | `no` | Switch (`trueValue: 'yes'`, `falseValue: 'no'`). Global — applies to both Test and Live. See [[cib-bank-settings]]. |

The refund action and the HUF conversion have no merchant-facing settings — they are automatic.

## Business rules

### Forced currency: HUF

CIB Bank's market.saki gateway settles in **Hungarian Forint (HUF)** only. If the customer's order is in another currency, the platform converts the payment amount before redirect — the payment's amount and currency are updated and persisted, and the customer sees the HUF total on the CIB page. See [[multi-currency]] for the conversion context.

### Save customer card flow

When **Save customer card = yes**:

- On checkout, if the signed-in customer already has a CIB **OCID** (Order Card ID) on file, the platform **bypasses the redirect** and uses CIB's pay-with-saved-card flow to charge the saved card directly. The customer sees an immediate result. Status flips to Completed (or Failed) without leaving the store — contrast the full redirect on [[cib-bank-payment-flow]].
- If no saved card exists, the platform adds `saveCard=true` to the redirect request — CIB's hosted page asks the customer if they want to save the card.
- On a successful payment, the platform stores the OCID, the original amount (AMOORIG), the original currency (CURORIG), the original ANUM, and the masked card number (CNUM) against the customer. **Guest customers are skipped** — only signed-in shoppers get cards saved.

### Saved-card UI on the customer profile

The saved-card panel on [[customers-details-payments]] is only rendered when the customer has at least one OCID on file. If the customer has never paid with CIB (no saved OCID), the integration returns an empty string for the customer-details panel — the merchant sees nothing CIB-specific on the customer profile.

### Refunds — with retransfer fallback

Calling **Refund payment** on a completed CIB order (see [[orders-payment-refund]]) runs the refund flow:

1. The platform sends a `refund` request with the transaction ID and the full payment amount.
2. **On success → Refunded** status, response stored.
3. **On error code `01`** (refund window expired — typical CIB behaviour for older charges), the platform automatically retries with a `retransfer` call instead of refund. If retransfer succeeds, the payment flips to Refunded.
4. **Any other error throws** an exception — the merchant sees the CIB error message in the admin UI.

This auto-fallback between `refund` and `retransfer` is specific to CIB's bank-business rules and is not exposed as a setting — the merchant doesn't need to know which method to call.

## Related

- [[payment-providers-cib-bank]] — hub.
- [[cib-bank-settings]] — where the Save-card switch lives (cross-aspect reference).
- [[orders-payment-refund]] — refund initiation (with auto-fallback to retransfer).
- [[customers-details-payments]] — saved customer cards visible on the customer profile.
- [[payment-status]] — Refunded status mapping.
- [[multi-currency]] — context for the HUF auto-conversion behaviour.

## Open questions

(none)
