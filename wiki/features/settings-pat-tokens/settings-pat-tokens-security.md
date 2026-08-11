---
type: feature
nav_path: "Settings → PAT Tokens → Security model"
route_name: pat-tokens.settings
route_path: /admin/settings/pat-tokens
aliases: ["PAT token format", "cc_pat_ prefix", "PAT hashing", "PAT masking", "PAT one-shot reveal", "PAT brute-force", "findByRawToken", "token_hash"]
tags: [settings, security, tokens, hashing, sha256, brute-force]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-pat-tokens]]. See the hub for related aspects (list view, create flow, scopes, restrictions, permissions, endpoints).

# PAT Tokens — security model

## Purpose

How PAT tokens are generated, stored, masked, and authenticated. This page explains why a lost token is unrecoverable, why a full database breach exposes only hashes, and why CloudCart deliberately does not implement per-token brute-force throttling. It's the page the support Assistant cites for "we lost the token", "can you regenerate", and "is it safe to use a long-lived token" questions.

## Where to find it

This page documents behaviour spread across the create flow, the list view, and the API gateway middleware. The merchant doesn't see most of it directly — they see only the masked prefix in [[settings-pat-tokens-list-view]] and the one-shot reveal in [[settings-pat-tokens-create-flow]].

## What the merchant can do here

The security model is largely invisible to the merchant. The few touch points:

- **Copy the token value once**, immediately after creation, from the green success card. See [[settings-pat-tokens-create-flow]].
- **Identify which token is which** via the masked prefix in the list table.
- **Revoke immediately** by deleting the token (preferred) or toggling `active=false` (reversible). See [[settings-pat-tokens-list-view]].
- **Audit recent activity** via `last_used_at` and `last_used_ip` columns to spot suspicious use.

## Settings & fields

### Token format

- Every token has the form `cc_pat_` + 64 random hex characters = **71 characters total**.
- The random portion is generated with cryptographically secure randomness (`random_bytes(32)` then hex-encoded) — **256 bits of entropy**, so guessing a valid token is computationally infeasible.

### Hashing and storage

- The platform stores **only the SHA-256 hash** of the token in the `token_hash` column, never the original value.
- The first 8 chars of the random portion are stored separately in the `token_prefix` column to support the masked display.
- **At authentication time** the platform hashes the incoming token (`hash('sha256', $rawToken)`) and looks up by hash. So losing the original value is unrecoverable — there's no decrypt path. Even a full database breach exposes only hashes.

### Masking format

The masked-token display in the list table is precisely:

```
cc_pat_ (7 chars — the prefix)
+ first 8 hex chars of the random portion (the token_prefix column, stable per token)
+ 49 asterisks
```

So the merchant sees something like `cc_pat_a1b2c3d4*************************************************`. This is enough to identify which token is which (the first 8 hex chars are stable per token and reasonably unique within a store) without revealing enough to reconstruct the original value.

### Per-token tracking columns

| Column | What it stores | Update trigger |
|--------|----------------|----------------|
| `token_hash` | SHA-256 of the original value | Set at create; never updated |
| `token_prefix` | First 8 hex chars of the random portion | Set at create; never updated |
| `last_used_at` | Timestamp of the most recent **successful** authentication | `recordUsage` on every accepted request |
| `last_used_ip` | Client IP from the most recent **successful** authentication; supports IPv4 + IPv6 | `recordUsage` on every accepted request |
| `revoked_at` | Timestamp set when the token is revoked | Set on Delete or explicit Revoke |

The `revoked_at` column lets the audit trail distinguish "never used" from "used and then revoked". `last_used_at = null` means the token was created but never authenticated; `last_used_at != null && revoked_at != null` means it was used in the past and then revoked.

## Business rules

### One-shot revelation is structural, not just UX

The "you can only see the value once" rule isn't enforced just at the modal layer — it's structural. The original value is never persisted; only the SHA-256 hash. Once the create modal closes, the in-memory value is GONE.

- No "show the value again" path exists. The Edit modal shows only the masked prefix.
- No support team / admin tool can recover a lost token — the database itself doesn't have the value.
- To "rotate" a token, the merchant must DELETE the old one and CREATE a new one. The Edit modal cannot mint a new value.

This is a deliberate design choice: a merchant who lets the token leak (in a screenshot, a config file in a repo, a Slack message) cannot blame the platform — the value's lifetime is bounded by the merchant's own copy.

### Brute-force resistance

**There is no explicit brute-force protection at the PAT auth layer.** `findByRawToken` simply validates format, hashes the input, and does a single indexed lookup against `token_hash`. There is no failed-attempt counter, no account lockout, no incremental backoff.

The two mitigations relied upon are:

1. **API gateway rate limit** — the `60 req/min` default per-domain rate limit constrains the attempt rate (this is shared across all callers on the domain, not per-token).
2. **256-bit entropy** — guessing one valid token out of 2^256 is computationally infeasible. Even at the gateway's theoretical 60 req/min, the expected time to a successful guess by random brute-force is on the order of 10^70 years.

Practical exposure is **negligible from random guessing**, but a **leaked token has no automatic revocation trigger**. The merchant must manually delete (or toggle off) any token they suspect is compromised. There is no anomaly detection (unusual IP, unusual hour, unusual scope use) that revokes the token automatically.

### Authentication path

A typical authenticated request runs through: format check → hash lookup with `valid` scope → IP allowlist check → scope check → `recordUsage`. Malformed tokens never hit the DB; only well-formed strings consume the indexed `token_hash` lookup. `recordUsage` ONLY runs on full success — so `last_used_at` reflects successful requests only, not attempted ones. See [[settings-pat-tokens-endpoints]] for the full middleware chain.

### Why this matters to the merchant

- **Treat the create-modal value like a password.** Copy it to a secret store (CI vault, password manager) the moment it's revealed.
- **Use expiration for CI tokens** — a 90-day token that auto-expires is safer than a permanent one. See [[settings-pat-tokens-restrictions]].
- **Lock to an IP range when possible** — leaked tokens outside the allowlist can't be used.
- **Audit `last_used_at`** to spot dormant tokens worth revoking, or anomalously-active ones worth investigating.
- **Rotate on staff offboarding** — when a developer leaves, delete every PAT they had access to.

## Related

- [[settings-pat-tokens]] — hub.
- [[settings-pat-tokens-create-flow]] — the one-shot reveal UX.
- [[settings-pat-tokens-list-view]] — masked prefix + `last_used_at` columns.
- [[settings-pat-tokens-restrictions]] — expiration and IP allowlist (the defence-in-depth layers).
- [[settings-pat-tokens-endpoints]] — `findByRawToken`, `recordUsage`, the full middleware chain.
- [[settings-pat-tokens-permissions]] — owner-only enforcement (additional defence layer beyond hashing).
- [[settings-api-keys]] — store-level API keys; different storage and revocation model.

## Open questions

- Is there any anomaly-detection or auto-revocation hook on suspicious PAT use (unusual IP, unusual hour)? Current understanding: no. `(verify)`
- Is `last_used_ip` exposed in the list view UI, or only stored in the DB? `(verify)`
