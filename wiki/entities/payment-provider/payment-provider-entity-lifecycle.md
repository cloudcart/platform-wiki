---
type: entity
nav_path: "Entity → Payment Provider → Lifecycle"
aliases: ["Payment Provider lifecycle", "Provider install / activate / uninstall", "Auto-deactivation", "Provider states"]
tags: [entity, payments, payment-providers, lifecycle, states]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

# Payment Provider — Lifecycle

> Part of [[payment-provider]]. See the hub for related aspects (attributes, credentials + modes, relationships, integration styles, plan gating, side effects).

## Identity

The seven merchant-controlled states a [[payment-provider|Payment Provider]] moves through, from "appears in the Add Payment Method modal" to "fully removed from the store". Most of the time the merchant lives in **Active (Live mode)**; the other states are entry / exit transitions.

## Aliases

- **Provider install / activate / uninstall** — how merchants describe the lifecycle informally.
- **Auto-deactivation** — the specific case where the platform flips a provider off without merchant action.
- **Provider states** — when the merchant is debugging "why isn't this showing up at checkout".

## Key Attributes

The seven states:

1. **Available (not installed)** — appears in the Add Payment Method modal on [[settings-payment-providers]] for the merchant's operation country. The merchant hasn't installed it yet. No configuration row exists.
2. **Installed (Inactive)** — the merchant added it from the Add Payment Method modal. A configuration row exists but the Active toggle is OFF. Credentials may be partially or fully entered. The provider does NOT appear at checkout.
3. **Configured (Test mode)** — credentials saved, Mode = `test`. The provider can be activated; live credentials may or may not be present. The customer-facing storefront shows this provider in test runs only.
4. **Active (Live mode)** — Mode = `live`, Active = `yes`, live credentials validated. The provider appears at checkout for matching carts (within `min_price` / `max_price`, allowed country, currency match, shipping method allows it). See [[payment-provider-checkout-visibility]].
5. **Suspended (Active = OFF)** — the merchant or the platform deactivated the provider. Credentials remain on the row. The provider is hidden from checkout. The merchant flips Active back ON to resume.
6. **Auto-deactivated** — for providers with strict credential validation (**Stripe, Revolut, and CloudCart Pay** are the canonical examples — see [[payment-provider-entity-side-effects]]), when CloudCart catches a credential-rejection error mid-transaction, the platform fires an admin notification, dispatches an alert to the bell-icon notification feed (see [[notification-delivery]]), and flips Active to OFF automatically. The merchant must fix the keys and re-enable.
7. **Uninstalled** — the merchant removed the provider via the per-provider settings page. The configuration row is deleted, credentials are gone. The merchant must re-onboard from scratch to bring it back. Destructive — typically used only for true removals. An audit-log entry is written (see [[payment-provider-entity-side-effects]]).

## Save-time transitions

- **Save triggers credential validation** for providers with strict gateway-side check-on-save (Stripe verifies the secret key against the gateway account; Borica Way4 verifies the certificate matches the private key; iCard validates numeric format on IDs). If the credentials are rejected, the save fails with a provider-specific error inline on the relevant field — the merchant cannot save a broken key. See [[payment-provider-entity-credentials-modes]].
- **Mode toggle is instant** — the merchant can flip live ↔ test on a saved provider without re-entering credentials; the non-active set is preserved.
- **Activation gate** — some providers (Borica Way4) refuse to activate in live mode until the live certificate is uploaded; the activate switch is greyed out until the file is set.
- **Uninstall is destructive** — credentials are wiped. The audit log preserves the install / uninstall history, but the row itself is gone.

## How the merchant moves between states

| From → To | How |
|-----------|-----|
| Available → Installed | Click Add Payment Method on [[settings-payment-providers]], pick the provider, confirm. |
| Installed → Configured (Test) | Open the per-provider settings page, paste test credentials, Mode = `test`, Save. |
| Configured → Active (Live) | Paste live credentials, flip Mode = `live`, flip Active = `yes`, Save. |
| Active → Suspended | Flip Active = `no` (instant — credentials retained). |
| Suspended → Active | Flip Active = `yes` (instant). |
| Active → Auto-deactivated | Triggered by the platform on persistent credential rejection — Stripe / Revolut / CloudCart Pay only. The merchant sees a notification bell alert. |
| Any → Uninstalled | Click Uninstall on the per-provider settings page (destructive; confirmation prompt). |

## Where it appears

- [[settings-payment-providers]] — list view shows the current state (Active badge or "Inactive" / "Test mode" chip per row); Add Payment Method modal exposes the Available state.
- Per-provider settings pages — the Active toggle and Mode toggle drive most state transitions.
- [[notification-delivery]] — auto-deactivation alerts surface here.
- The install / uninstall audit-log entries are surfaced to support investigations — see [[payment-provider-entity-side-effects]] for the audit trail.

## Related

- [[payment-provider]] — hub.
- [[payment-provider-entity-credentials-modes]] — Mode toggle + save-time validation.
- [[payment-provider-entity-side-effects]] — what fires on save / install / uninstall + the auto-deactivation safety net.
- [[payment-provider-checkout-visibility]] — runtime visibility rules that depend on Active = `yes`.
- [[notification-delivery]] — the bell-icon alert path for auto-deactivation.
- [[payment-provider-configuration]] — cross-cutting configuration concept.
- [[settings-payment-providers]] — the merchant's home base for all state transitions.

## Open Questions

None.
