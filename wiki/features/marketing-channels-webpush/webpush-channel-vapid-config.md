---
type: feature
nav_path: "Marketing → Channels → Channels setup → Web Push → VAPID configuration"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["VAPID keys", "VAPID identity", "Voluntary Application Server Identification", "webpush:vapid", "VAPID_PUBLIC_KEY", "VAPID_PRIVATE_KEY", "Платформа VAPID ключове"]
tags: [marketing, channels, web-push, vapid, platform-config, signing]
plan_gates: ["campaign.channel.web_push"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-channels-webpush]]. See the hub for the other aspects (storefront prompt, subscription flow, send pipeline, DLR webhook, system messages, browser support).

# Web Push channel — VAPID configuration

## Purpose

**VAPID** (Voluntary Application Server Identification) is the IETF mechanism for proving to a browser-vendor push service (Mozilla Autopush, Google FCM, Apple WebPush gateway) that a push sender is who it claims to be. Every outgoing Web Push payload is signed with a VAPID private key, and the browser's push service verifies the signature against the matching public key (which the browser saw when it issued the subscription).

CloudCart manages a **single platform-wide VAPID key pair** — one identity that signs every Web Push from every CloudCart storefront. Merchants do NOT supply their own keys. The pair lives in environment variables and the public key is injected into every storefront via the [[webpush-channel-storefront-prompt|`renderSf` init block]] as `VapKey`.

## Where to find it

There is **no merchant-facing UI** for VAPID keys — the Web Push **Settings** modal does not surface, generate, or rotate them. They are platform-only, managed by CloudCart infrastructure operators via the `php artisan webpush:vapid` Artisan command and the `.env` file on the server.

If a merchant asks "where is my VAPID key" — the answer is: there isn't one per-merchant, the platform key signs all storefronts.

## What the merchant can do here

Nothing directly. Indirectly:

- The merchant sees the **public** half of the key on every storefront page via the `VapKey` field in the storefront init payload (browser-readable, deliberately — the browser needs it to bind to the subscription).
- The merchant cannot rotate, regenerate, or override the key.

CloudCart operators can:

- Run `php artisan webpush:vapid --show` to inspect the current keys.
- Run `php artisan webpush:vapid` (without `--show`) to generate a fresh pair and write it into `.env` — gated by a confirmation prompt in production.

## Settings & fields

### Platform-level VAPID env (the platform code)

| Setting key | Env source | Notes |
|---|---|---|
| `vapid.subject` | `env('VAPID_SUBJECT')` | Contact URL or `mailto:` for the VAPID identity. Required by the spec so the push service has a way to contact the sender if there's an abuse issue. |
| `vapid.public_key` | `env('VAPID_PUBLIC_KEY')` | Public ECDSA P-256 key. Shared with browsers via the storefront's service-worker initialization as the `VapKey` field. |
| `vapid.private_key` | `env('VAPID_PRIVATE_KEY')` | Private key. Used to sign each outgoing push payload server-side. Never leaves the backend. |
| `vapid.pem_file` | `env('VAPID_PEM_FILE')` | Optional PEM file path — alternative to inline keys. |
| `client_options.timeout` | `3` (default) | Guzzle client timeout (in seconds) for the push-service HTTP call. Short — so a slow push service doesn't hang the queue worker. |

### `webpush:vapid` Artisan command

| Flag | Behaviour |
|---|---|
| `--show` | Prints the current keys to stdout. Read-only. |
| (no flag) | Generates a fresh key pair via the platform code and overwrites the `.env` values. In production, prompts for confirmation first. |

## Business rules

### One platform key, all merchants

The platform's identity (the `subject`) is CloudCart's, not the merchant's. The browser-vendor push service sees `mailto:<cloudcart-contact>` (or similar) as the sender across every CloudCart store. This is fine — VAPID identity is about abuse-reporting routing, not about identifying the brand to the customer. The customer's notification still shows the merchant's storefront title + icon + image.

This model means:

- Merchants don't need to know what VAPID is.
- Merchants don't generate keys, don't manage `.env`, don't expose secrets.
- One CloudCart store's bad behaviour CAN affect VAPID identity reputation for all stores — push services rate-limit / penalise the VAPID identity, not the per-store endpoint. This is why the [[marketing-campaigns-policy|anti-spam policy]] is enforced at the campaign-content level: a single noisy merchant degrades the channel for everyone.

### VAPID keys rarely rotate

Every existing subscriber's browser-issued `endpoint` is **bound to the VAPID public key** that was active when the subscription was created — the browser remembers which sender identity it trusted. Rotating the VAPID key pair would invalidate every existing subscription on every CloudCart store. The `webpush:vapid` command exists for one-off platform setup, not ongoing rotation.

If CloudCart ever does rotate, every storefront's existing Web Push subscribers would silently stop receiving messages (the push service would reject the new VAPID JWT for old subscriptions). The platform-level guarantee is: keys are stable for the long term.

### Public key is intentionally browser-readable

The `VapKey` field in the storefront's `renderSf` init block contains the **public** key — it's safe to expose. The browser uses it at subscribe time to bind the subscription to the sender identity. Leaking it to the world is fine; only the private key is sensitive.

### Signing pipeline — what happens per send

The Web Push send job hands the message + the recipient's `endpoint` / `p256dh` / `auth` to Minishlink's WebPush library, which:

1. Builds a Subscription object from the endpoint + keys.
2. Encrypts the JSON payload (title / body / icon / image / data / dlrUrl) using ECIES with the recipient's `p256dh` public key — only the recipient device's private key can decrypt.
3. Signs a VAPID JWT with the platform's `VAPID_PRIVATE_KEY`.
4. POSTs the encrypted body + the VAPID `Authorization` header to the recipient's `endpoint` URL.

See [[webpush-channel-send-pipeline]] for the full HTTP shape of the outgoing request.

### Subject field — for abuse contact only

`vapid.subject` should be a `mailto:` or a URL that the push-service vendor can use to reach CloudCart if they need to flag abuse. It does NOT appear in any customer-visible UI and is independent of the merchant's contact email.

## Related

- [[marketing-channels-webpush]] — hub.
- [[webpush-channel-storefront-prompt]] — injects the public key as `VapKey` into the storefront init block.
- [[webpush-channel-send-pipeline]] — uses the private key to sign each outgoing send.
- [[webpush-channel-subscription-flow]] — the browser binds the subscription to the public key at subscribe time, which is why rotation is destructive.
- [[marketing-campaigns-policy]] — anti-spam policy that protects the shared VAPID identity.

## Open questions

None outstanding for the merchant-facing view. (Operator-side rotation procedure is platform infra, out of scope for the merchant wiki.)
