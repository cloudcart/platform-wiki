---
type: feature
nav_path: "Settings → Webhooks → Authentication & headers"
route_name: hooks.settings
route_path: /admin/settings/hooks
aliases: ["Webhook authentication", "X-CloudCart-ApiKey", "Webhook headers", "Custom headers", "Webhook auth header", "Header replacement"]
tags: [settings, webhooks, authentication, headers, integrations]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-hooks]]. See the hub for the other aspects (events, delivery, retry, auto-disable, modal, activity log).

# Webhooks — authentication & custom headers

## Purpose

Every outgoing webhook carries an authentication header **`X-CloudCart-ApiKey`** that the platform **auto-injects** from the API key the merchant linked when creating the webhook. The receiver uses this to prove the request came from this specific CloudCart store and not from a forger spoofing the URL. The merchant can additionally attach arbitrary **custom headers** (HMAC signatures, Bearer tokens, environment markers, etc.) via the modal's Headers editor — these are sent alongside the platform-injected auth header.

## Where to find it

- Sidebar → Settings → **Webhooks** → **+ Add webhook** → **API key** field (links the auth credential).
- Same modal → **Card 2** → Headers editor (adds the merchant's custom headers).
- Source of API keys: [[settings-api-keys]].

## What the merchant can do here

- Pick the **API key** the receiver will use to authenticate inbound webhooks. The key value is automatically sent as `X-CloudCart-ApiKey` — the merchant does NOT add this header manually.
- Add any number of **custom headers** (Key / Value pairs) in the modal's Headers editor. Common uses:
  - HMAC signature header (e.g. `X-Signature: <hmac-sha256-of-body>`).
  - Bearer token (e.g. `Authorization: Bearer <token>`).
  - Environment markers (e.g. `X-CloudCart-Env: production`).
- Remove individual header rows via the per-row remove icon.
- Edit / replace headers on save — see Header replacement semantics below.

## Settings & fields

### Auto-injected `X-CloudCart-ApiKey` header

On every webhook delivery the platform adds this exact header:

```
X-CloudCart-ApiKey: <api-key value>
```

Where `<api-key value>` is the value of the API key the merchant linked in the webhook's **API key** field (see [[settings-api-keys]] for where keys are created and rotated). The merchant does NOT see this header in the Headers editor — it is invisible at the UI level but ALWAYS present on the wire.

**The receiver should validate this header before processing.** It proves the request came from this specific CloudCart store and not from a forger who knows the URL. If the receiver's CloudCart-side key gets rotated or revoked, the receiver should reject the request.

### Outgoing request header layout

```
POST <hook.url>
Headers:
  X-CloudCart-ApiKey: <api-key value, auto-added>
  <each merchant-configured custom header>
  Content-Type: application/json
Body:
  [{ ...payload... }]
```

The merchant-configured custom headers are sent **alongside** the platform-added `X-CloudCart-ApiKey` header — they do NOT replace it. Receivers see both.

### Custom headers — storage & "replace-all on update" semantics

Each merchant-configured custom header is stored as one row in a related table. When the merchant updates a webhook, the platform **deletes ALL existing header rows** for that webhook and creates fresh ones from the request payload. Consequences:

- **Header order** is whatever order the merchant submitted in the form (sequential by creation).
- **There is no merge** — headers omitted from an update request are removed. To add a header without losing existing ones, the merchant must re-submit the full list.
- **Empty key OR empty value pairs are filtered out.** A header with key=`"X-Foo"` and value=`""` is skipped, NOT saved. Same for empty key + any value.

### Combining custom headers with the auto-injected key

Receivers needing more than the platform-provided auth (e.g. HMAC over the body) can layer custom auth on top:

- `X-CloudCart-ApiKey: <key>` — platform-injected, NOT in the Headers editor.
- `X-Signature: <hmac-sha256(body, shared-secret)>` — merchant-configured, in the Headers editor.

The receiver validates BOTH: the API key proves CloudCart origin; the HMAC proves the body has not been tampered with in transit. This is the recommended pattern for high-security integrations.

### What the merchant cannot do

- **Override `X-CloudCart-ApiKey`.** Adding a custom header with key `X-CloudCart-ApiKey` either gets overwritten by the auto-injection or stacked — the platform-injected value wins. (verify the exact behaviour on collision)
- **Override `Content-Type`.** All deliveries are `application/json`. Custom `Content-Type` headers are ignored / overridden.
- **Send headers conditionally per event.** Custom headers attach to the webhook row, not to individual events. A webhook for `order.created` and another for `order.updated` need separate Headers editors.

## Business rules

- **API key deletion is blocked while a webhook uses it.** Deleting an API key from [[settings-api-keys]] is FK-blocked if any webhook references it. The merchant must reassign or delete the dependent webhooks first.
- **Rotating an API key takes effect on the NEXT delivery.** No re-save of the webhook is required — the platform reads the current key value at delivery time. Receivers should treat key rotation as a coordinated handoff.
- **Headers are case-preserving but case-insensitive at the HTTP level.** A header saved as `x-signature` is sent verbatim but the receiver should match case-insensitively per HTTP spec.
- **No size limit enforced in UI.** The modal allows unbounded custom headers (verify backend cap). Practical limit is dictated by what the receiver's HTTP stack accepts. (verify)

## Related

- [[settings-hooks]] — hub.
- [[settings-hooks-modal]] — the create / edit form where the API key + custom headers are configured.
- [[settings-hooks-events]] — the payload that ships with these headers.
- [[settings-api-keys]] — source of the API key value injected as `X-CloudCart-ApiKey`; FK-blocks deletion while in use here.
- [[api-webhooks]] — programmatic equivalent (same header semantics on the wire).
- [[api-key]] — entity page.

## Open questions

- Confirm exact collision behaviour if the merchant adds a custom `X-CloudCart-ApiKey` header (overwrite vs stack vs reject). (verify)
- Confirm whether there is a backend cap on the number of custom headers per webhook. (verify)
