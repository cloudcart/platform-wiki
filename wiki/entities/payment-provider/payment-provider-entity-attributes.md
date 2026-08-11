---
type: entity
nav_path: "Entity → Payment Provider → Attributes"
aliases: ["Payment Provider fields", "Payment Provider attributes", "Payment Provider schema", "Payment Provider configuration fields"]
tags: [entity, payments, payment-providers, integrations, fields, settings]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

# Payment Provider — Attributes

> Part of [[payment-provider]]. See the hub for related aspects (credentials + modes, relationships, lifecycle, integration styles, plan gating, side effects).

## Identity

The verbatim attribute catalogue for the [[payment-provider|Payment Provider]] entity — every operator-level field the merchant edits on the per-provider settings page (e.g. [[payment-providers-icard]], [[payment-providers-stripe]], [[payment-providers-borica-way4]]) plus the JSON `configuration` blob that carries per-provider credentials and flags.

## Aliases

- **Payment Provider fields** / **attributes** — common references in merchant support tickets.
- **Payment Provider configuration fields** — when the merchant is editing the per-provider settings page.

## Key Attributes

| Field | What it stores | Notes |
|-------|----------------|-------|
| **Provider code** (`name` / internal key) | Stable identifier (e.g., `stripe`, `icard`, `borica_way4`, `mokka`, `mypos`, `cod`) | Used internally to pick the right integration; never edited by the merchant. |
| **Storefront name** | Customer-facing label at checkout | Editable per provider — e.g., the merchant can rename internal `borica_way4` to "Pay with card". |
| **Logo** | Provider-logo image | Defaults to the gateway's logo; merchant can upload a custom override. |
| **Description** | Short customer-facing explainer | Shown below the provider row in the checkout payment-method picker. |
| **Mode** | `live` / `test` | The Mode toggle — flips which credential set is active at runtime. The non-active set stays stored on the same row. See [[payment-provider-entity-credentials-modes]]. |
| **Active** | yes / no | Master on/off. When `no`, the provider is hidden at checkout; when `yes`, it appears (subject to other scoping). |
| **Credentials (per-provider)** | API keys, merchant ID, terminal ID, private/public keys, certificates, store endpoint | Each credential field exists in TWO variants — `<name>` for live, `test_<name>` for test. Both saved simultaneously on one row. Field set varies wildly: Mokka needs 3 fields × 2 modes, iCard / Borica Way4 need 6+ credential fields × 2 modes plus uploaded certificates, CloudCart Pay needs the fewest because onboarding handles it. See [[payment-provider-entity-credentials-modes]]. |
| **Min order amount** / **Max order amount** (`min_price` / `max_price`) | Order-amount range | The provider only appears at checkout when the cart subtotal is within this range. Common gate across all providers. |
| **Allowed countries** | Country list | Restricts which customer countries see this provider. Empty = all countries. |
| **Sort order** | Display position at checkout | Lower = earlier in the checkout payment-method list. |
| **Discount** | Flat / percent / free-shipping | Optional incentive applied when the customer picks this provider (e.g., -2% when paying with CloudCart Pay). |
| **Surcharge / fee** | Flat / percent | Optional fee added when the customer picks this provider (e.g., +1.50 BGN for COD). |
| **Save Customer Card** | yes / no (per mode) | For tokenizing providers (Stripe, Borica Way4, CloudCart Pay, etc.) — controls whether the customer's card is stored on the gateway vault for one-click repeat purchases. Only applies to signed-in customers, never guests. See [[payment-provider-tokenization-3ds]]. |
| **Authorization mode** | `auto-capture` / `authorize-then-capture` | For providers that support pre-auth (Borica Way4, Stripe with capture-later, Klarna). Gated by the `authorize_payment` plan-feature — see [[payment-provider-entity-plan-gating]]. |
| **3DS** | enforced / issuer-driven / N/A | Set by the provider and card-network rules — most BG bank gateways enforce 3DS 2.x mandatorily; global multi-currency gateways defer to the issuer. The merchant cannot disable it. |
| **Webhook callback URL** | The URL the merchant pastes into the gateway's portal | Provider-side configuration — the merchant copies this from the CloudCart settings page and pastes into the gateway's onboarding form so the gateway can POST payment results back. See [[payment-provider-confirmation]]. |
| **Currency support** | Provider-specific | Set by the gateway's commercial scope: BG bank gateways = BGN / EUR; global card gateways = 100+ currencies; BNPL = domestic-currency-only. Not validated at save time — see [[payment-provider-entity-plan-gating]] for the currency-mismatch failure mode. |

The two large clusters of variation across providers are the **credentials field set** (covered in detail on [[payment-provider-entity-credentials-modes]]) and **which operational flags are exposed** (e.g., Save Customer Card only renders for tokenizing providers; Authorization Mode only renders where the gateway supports pre-auth; the webhook callback URL is read-only for the merchant and only appears when the provider uses webhook confirmation).

## Where it appears

- [[settings-payment-providers]] — the list view shows Storefront Name, Logo, Active toggle, Mode badge, Discount / Surcharge chips, country / amount chips.
- Per-provider settings pages — every field above is editable here (e.g., [[payment-providers-stripe]], [[payment-providers-icard]], [[payment-providers-borica-way4]], [[payment-providers-cod]]).
- [[checkout-flow]] — Storefront Name, Logo, Description, Discount / Fee badges, Sort Order all surface in the customer payment-method picker.

## Related

- [[payment-provider]] — hub.
- [[payment-provider-entity-credentials-modes]] — live + test credential storage rules.
- [[payment-provider-entity-relationships]] — how scoping fields (countries, shipping methods, categories, customer groups) interact with other entities.
- [[payment-provider-entity-plan-gating]] — the `authorize_payment` gate on Authorization Mode + currency mismatch behavior.
- [[payment-provider-tokenization-3ds]] — Save Customer Card + 3DS deep dive.
- [[payment-provider-confirmation]] — webhook callback URL usage.
- [[payment-status]] — the enum every provider's response codes map to.

## Open Questions

None.
