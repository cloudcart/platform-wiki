---
type: feature
nav_path: "Apps → Subscriptions → Settings → What the customer may do"
route_name: apps.subscriptions.settings
route_path: /admin/apps/subscriptions/settings
aliases: ["customer subscription management", "customer cancel subscription", "skip a delivery", "pause subscription", "my subscriptions page", "customer account subscriptions", "клиентът да спре абонамент", "пропускане на доставка", "пауза на абонамент", "моите абонаменти"]
tags: [apps, subscriptions, storefront, customer-account, permissions]
plan_gates: ["subscriptions"]
created: 2026-08-28
updated: 2026-08-28
source_count: 5
---

> Part of [[apps-subscriptions]]. See the hub for the other aspects (setup, plans, billing cycle, failed payments, managing).

# Subscriptions — what the customer can do

## Purpose

Subscriptions are designed to be run by the customer, from their own account, without contacting the shop. The merchant decides how much of that self-service to allow. This aspect covers the customer's side and the four switches that shape it.

## Where to find it

**Merchant:** Apps → Subscriptions → Settings → the customer-permission switches.

**Customer:** their storefront account, under **My subscriptions** — a list of their subscriptions and a detail page for each. See [[customer-account]].

## What the merchant can do here

Turn each of the customer's four abilities on or off, store-wide. There is no per-plan or per-customer variation.

## Settings & fields

| Switch | What it allows the customer to do |
|---|---|
| **Skip a delivery** (`allow_customer_skip`) | Pass over the next delivery. The schedule moves on; nothing is charged for it. |
| **Pause the subscription** (`allow_customer_pause`) | Stop it indefinitely, then resume when ready. |
| **Cancel the subscription** (`allow_customer_cancel`) | End it for good. |
| **Change the delivery address** (`allow_customer_edit_address`) | Redirect future deliveries. |

Switching one off removes the action from the customer's account entirely, and the platform refuses it if attempted — *"This action is not available for your subscription."*

## Business rules

### Skipping and pausing are different things

Both stop the next charge, and merchants use the words interchangeably, but they behave differently:

- **Skip** passes over **one** delivery. The subscription stays `active` and the schedule continues from the following one.
- **Pause** stops the schedule **indefinitely**. The subscription becomes `paused`, nothing is due, and it only restarts when someone resumes it.

Steering a customer who wants a break to **skip** rather than **pause** keeps the subscription running by itself, which is usually what both sides want — a paused subscription that nobody resumes is a lost customer that nobody notices.

### Actions are refused when the state does not allow them

Each action applies to a specific state, and the platform names the mismatch rather than failing silently:

| Attempt | Refusal |
|---|---|
| Pausing something not running | *"This subscription is not active."* |
| Resuming something not paused | *"This subscription is not paused."* |
| Skipping a delivery already processed | *"This delivery can no longer be skipped."* |
| Charging a contract in a state that cannot be billed | *"This subscription cannot be charged in its current state."* |

A skip has to be requested **before** its cycle is processed; once the charge has been taken the delivery is bought and skipping it is a return, not a skip ([[orders-returns]]).

### A minimum commitment limits cancelling

A plan can require a minimum number of payments before it may be cancelled ([[apps-subscriptions-plans]]). Until the customer reaches it, the cancel action is refused with the same *not available* message.

This is the usual explanation for *"the cancel button does not work for this customer"* when it works for others — check the plan's minimum before treating it as a fault.

### Turning off cancellation does not remove the merchant's obligation

The switch controls the **storefront**, not the contract. A customer who cannot cancel in their account will ask the shop to do it, and the merchant can always cancel from the admin ([[apps-subscriptions-managing]]).

Consider what the store's own terms and its consumer-protection obligations require before switching self-service cancellation off — the merchant remains obliged to honour a cancellation request whichever way it arrives. See [[apps-aftercare]] for the withdrawal rules that apply separately.

### The address change applies from the next delivery

Changing the delivery address affects deliveries still to come. Orders already raised keep the address they were created with, and are changed — if at all — on the order itself ([[orders-address-edit]]).

## Related

- [[apps-subscriptions]] — hub.
- [[apps-subscriptions-managing]] — the same actions from the merchant's side, plus **Charge now**.
- [[apps-subscriptions-plans]] — the minimum-payments commitment.
- [[customer-account]] — the account area holding the subscription pages.
- [[orders-address-edit]] — changing an address on an order already raised.
- [[apps-aftercare]] — the separate withdrawal-from-contract rules.

## Open questions

- Whether a customer who has hit the plan's maximum number of payments sees the subscription end in their account, or simply stops seeing it.
