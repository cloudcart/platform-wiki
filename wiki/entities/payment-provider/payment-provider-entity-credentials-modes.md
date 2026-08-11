---
type: entity
nav_path: "Entity → Payment Provider → Credentials & modes"
aliases: ["Payment Provider credentials", "Live vs test mode", "Provider mode toggle", "Credential encryption at rest"]
tags: [entity, payments, payment-providers, credentials, security, modes]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

# Payment Provider — Credentials & modes

> Part of [[payment-provider]]. See the hub for related aspects (attributes, relationships, lifecycle, integration styles, plan gating, side effects).

## Identity

Every Payment Provider stores **two parallel credential sets on a single configuration row** — one for live transactions, one for test. The merchant flips between them via the **Mode** toggle on the per-provider settings page. Credentials are encrypted at rest, validated against the gateway on save where the gateway supports it, and never leak through database inspection.

## Aliases

- **Live vs test mode** — the merchant-facing framing of the Mode toggle.
- **Provider mode toggle** — the UI control.
- **Credential encryption at rest** — when discussing the security guarantee.

## Key Attributes

| Aspect | Behavior |
|--------|----------|
| **Two credential sets per row** | Every credential field exists in TWO variants — `<credential_name>` for live, `test_<credential_name>` for test (e.g., `secret_key` + `test_secret_key`, `merchant_id` + `test_merchant_id`, `private_key` + `test_private_key`). The merchant saves BOTH sets simultaneously. |
| **Mode toggle** | Instant — flips live ↔ test on a saved provider without re-entering credentials; the non-active set is preserved. Only one set is "active" at any time. |
| **No separate test row** | There is no separate provider entry for test mode. One row, two credential sets. |
| **Credential field set varies wildly** | Mokka needs 3 fields × 2 modes. iCard / Borica Way4 need 6+ credential fields × 2 modes plus uploaded certificates. CloudCart Pay needs the fewest because onboarding handles it server-side. Stripe needs publishable + secret key + webhook signing secret × 2 modes. |
| **Save-time gateway validation** | For providers with strict gateway-side check-on-save, the platform calls the gateway during the save: Stripe verifies the secret key resolves to an account; Borica Way4 verifies the uploaded certificate matches the private key; iCard validates numeric format on IDs. If the credentials are rejected, the save fails with a provider-specific error inline on the relevant field — the merchant cannot save a broken key. |
| **Encryption at rest** | When the merchant clicks Save, the platform runs the credentials blob (API key, merchant ID, secret, certificate IDs, terminal ID, etc.) through **AES encryption** before persisting. A leak of the underlying database table does NOT reveal the gateway credentials. When the platform later reads the row to call the gateway, it decrypts in-memory only. |
| **Activation gate for some providers** | Some providers (Borica Way4) refuse to activate in live mode until the live certificate is uploaded; the activate switch is greyed out until the file is set. |

## Why this matters to the merchant

Two practical implications:

- **Testing is non-destructive.** The merchant can keep test credentials installed indefinitely. Flipping Mode to `test` lets them run end-to-end checkout against the gateway's sandbox without losing the live credentials.
- **A live credential rotation is a single Save.** The merchant pastes the new key, clicks Save, the platform re-validates against the gateway, and (assuming the new key resolves) the provider keeps running. There is no separate "rotate keys" workflow.

## Where it appears

- Every per-provider settings page (e.g., [[payment-providers-stripe]], [[payment-providers-borica-way4]], [[payment-providers-icard]], [[payment-providers-mokka]], [[payment-providers-cloudcart-pay-settings]]) — both credential sets rendered in two columns or two tabs, with the Mode toggle at the top.
- [[settings-payment-providers]] — Mode badge on each row indicates whether the provider is currently in `live` or `test` mode.

## Related

- [[payment-provider]] — hub.
- [[payment-provider-entity-attributes]] — the full field catalogue.
- [[payment-provider-entity-lifecycle]] — the Configured (Test mode) and Active (Live mode) states.
- [[payment-provider-entity-side-effects]] — what fires when the merchant clicks Save (cache invalidate + app-catalog upsert + audit log).
- [[payment-provider-configuration]] — cross-cutting configuration-flow concept.
- [[payment-providers-borica-way4]] — canonical example of certificate-gated activation.
- [[payment-providers-stripe]] — canonical example of save-time gateway validation.

## Open Questions

None.
