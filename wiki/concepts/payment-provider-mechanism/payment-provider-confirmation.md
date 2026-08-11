---
type: concept
nav_path: "Concept → Payment provider mechanism → Confirmation & status mapping"
aliases: ["Payment provider confirmation", "Webhook callback", "Sync action", "Pull-based payment provider", "Webhook-based payment provider", "Status mapping", "Status code mapping", "EGW_MERCH_BACKREF", "Потвърждение на плащане", "Sync бутон"]
tags: [payments, payment-providers, webhooks, sync, status-mapping, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-provider-mechanism]]. See the hub for the other aspects (configuration, integration patterns, tokenization & 3DS, refunds, checkout visibility).

# Payment provider — confirmation & status mapping

## Definition

After the customer completes payment at the gateway, CloudCart needs to know the final result. Two confirmation styles do this: **webhook-based** (the gateway POSTs the outcome to a CloudCart callback URL) and **pull-based / sync** (CloudCart calls the gateway's status-fetch API to check). Either way, each gateway's native response codes are then **mapped** to the canonical 13-value [[payment-status]] enum. This aspect covers both halves: the confirmation transport (webhook vs sync) and the status-code translation step.

## Scope

Covered:

- Webhook-based providers — callback URL pattern (`/return/provider/<provider-key>`), signature validation, the `EGW_MERCH_BACKREF` field for Borica Way4.
- Pull-based providers — periodic Sync + on-return Sync.
- The universal Sync recovery button on [[orders-details]] when a webhook is lost.
- The 13-value canonical [[payment-status]] enum (`initiated`, `requested`, `pending`, `authorized`, `held`, `completed`, `failed`, `refunded`, `voided`, `cancelled`, `timeouted`, `chargebacked`, `disputed`).
- Status-mapping examples per major provider.

Not covered here:

- The customer's experience during payment (redirect / embedded / manual) — see [[payment-provider-integration-patterns]].
- What each status enum value means semantically — see [[payment-status]].
- The order's overall status lifecycle (driven partly by these transitions) — see [[order-status-workflow]].
- Refund-side status flips — see [[payment-provider-refunds]].

## Contrasts

- **Webhook-based vs pull-based** — webhook providers push results on their own schedule (latency = network only); pull-based providers depend on CloudCart calling the gateway, so latency = polling interval. The merchant doesn't see this difference in normal operation — both produce the same `completed` end state.
- **Webhook lost vs status genuinely pending** — when a customer's webhook never arrives (network issue, gateway outage), the payment sits in `initiated` / `requested` longer than expected. The fix is to click **Sync** on the order's payment row — the universal recovery action across providers. Sync is also what pull-based providers use as their normal confirmation method.
- **Canonical enum vs provider-native codes** — every provider has its OWN response codes (Borica `00` / TRTYPE numbers, Stripe `succeeded` / `requires_action`, Cardlink `isSuccessful`, etc.). The platform translates them into the 13-value [[payment-status]] enum the rest of CloudCart understands. Two different gateways' "success" both land at `completed`.

## Where it applies

### Webhook-based providers

The gateway POSTs the result back to a CloudCart callback URL (typically `/return/provider/<provider-key>`). The platform:

1. **Validates the callback's signature** — using the merchant's secret / certificate stored in [[settings-payment-providers]].
2. **Finds the payment by reference ID** — matches gateway transaction ID against the platform's payment record.
3. **Updates the status** — applies the per-provider code mapping (see below).

The merchant gives the gateway the callback URL during onboarding (e.g., the **`EGW_MERCH_BACKREF`** field for Borica Way4 — the URL the merchant pastes into their bank's terminal configuration). Webhook providers include Borica Way4, CloudCart Pay, most BNPL gateways.

### Pull-based (sync) providers

The gateway doesn't push results; CloudCart calls the gateway's status-fetch API to check. Used when the platform's current integration doesn't subscribe to webhooks (**Stripe** in CloudCart's integration is pull-based today). The platform calls Sync on the customer's return and again on a periodic schedule for still-pending payments.

### The Sync recovery button (universal)

When a customer's gateway callback is lost (network issue, transient gateway outage), the merchant can manually click **Sync** on the order's payment row in [[orders-details]] to re-fetch the latest status. **Sync is the universal recovery action across providers** — works on both webhook-based and pull-based integrations.

### The canonical [[payment-status]] enum

13 platform-defined values: `initiated`, `requested`, `pending`, `authorized`, `held`, `completed`, `failed`, `refunded`, `voided`, `cancelled`, `timeouted`, `chargebacked`, `disputed`.

The merchant can rename the **labels** for these statuses on [[settings-statuses]] (Payment tab) — the underlying enum value is unchanged, only the display string.

### Status-mapping examples

Each provider's native codes map to one of the canonical values. Examples:

- **Borica Way4** ([[payment-providers-borica-way4]]):
  - `00` + TRTYPE 1 → `completed`
  - `00` + TRTYPE 12 → `authorized`
  - `-25` → `cancelled`
  - `-31` / `-33` / `-39` / `-40` → `pending`
  - anything else → `failed`
- **Stripe** ([[payment-providers-stripe]]):
  - `succeeded` → `completed`
  - `requires_action` → `cancelled`
  - other failures → `failed`
- **Cardlink** ([[payment-providers-cardlink]]):
  - `isSuccessful = true` → `completed`
  - `isCancelled = true` → `cancelled`
  - otherwise → `failed`
- **COD** ([[payment-providers-cod]]):
  - always starts `pending`; merchant flips manually to `completed`.

Each per-provider page documents its specific mapping in a "Status code mapping" section.

## Related

- [[payment-provider-mechanism]] — hub.
- [[payment-status]] — the canonical 13-value enum.
- [[payment-provider-integration-patterns]] — the redirect / embedded / manual classification; confirmation transport is orthogonal to this.
- [[payment-provider-refunds]] — refund-side status flips also use this confirmation infrastructure.
- [[orders-details]] — where the Sync button lives.
- [[orders-payment-mark-paid]] — manual override when no automatic confirmation comes.
- [[settings-statuses]] — Payment tab; rename status labels (enum unchanged).
- [[settings-payment-providers]] — where the merchant gives the callback URL (e.g., `EGW_MERCH_BACKREF`) to the gateway.
- [[order-status-workflow]] — order-level status driven partly by these transitions.
- [[order-processing-pipeline]] — downstream side-effects when a payment-status flip occurs.
- [[payment-providers-borica-way4]] / [[payment-providers-stripe]] / [[payment-providers-cardlink]] / [[payment-providers-cod]] — providers with documented mappings.

## Open Questions

- ⏸️ Exact per-provider sync polling intervals (verify) — schedule may vary per integration; documented on individual provider pages.
- ⏸️ Full per-provider list of webhook vs pull-based classification (verify) — confirmed for Borica Way4 (webhook), CloudCart Pay (webhook), Stripe (pull); others vary.
