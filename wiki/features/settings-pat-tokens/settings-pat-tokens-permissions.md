---
type: feature
nav_path: "Settings → PAT Tokens → Owner-only enforcement"
route_name: pat-tokens.settings
route_path: /admin/settings/pat-tokens
aliases: ["PAT owner-only", "Only store owners can manage CLI tokens", "PAT 403", "PAT moderator", "PAT max tokens", "10-token cap", "PAT cascade delete"]
tags: [settings, security, tokens, permissions, owner-only]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-pat-tokens]]. See the hub for related aspects (list view, create flow, scopes, restrictions, security, endpoints).

# PAT Tokens — owner-only enforcement and limits

## Purpose

PAT token management is **gated to the store owner**, full stop. This page documents the four-layer enforcement (route middleware, controller method, Form Request authorize, service layer), the hardcoded 10-token-per-store cap, and the cascade behaviour when a Moderator account is removed. It corrects an earlier wiki claim that moderators could create scoped tokens — that is wrong; moderators cannot create tokens at all.

## Where to find it

The enforcement is invisible by design: Moderators / Administrators never see the **PAT Tokens** sidebar entry, and direct navigation to `/admin/settings/pat-tokens` returns HTTP 403. Only the store owner sees the screen at all.

## What the merchant can do here

### As the store owner

- See and manage all PAT tokens (list, create, edit, revoke, toggle).
- Create up to **10 tokens total** across the entire store (the hardcoded cap).
- Grant **any** scope from the full catalog regardless of any internal "permission" tree — owner is the highest authority.

### As a Moderator or Administrator

- See nothing related to PAT tokens. No sidebar entry. No API access. No "request access" flow.
- If they attempt direct API calls (e.g., from a script), get HTTP 403 with the message *"Only store owners can manage CLI tokens"*.

## Settings & fields

### Per-store cap

The page's `meta.max_tokens` defines the maximum number of tokens this admin can have active. **Hardcoded to 10**, NOT plan-based. The "`<N>` of 10 tokens" chip in the page header always shows the second number as 10. Since only the owner can create, this is effectively a **10-tokens-per-store limit**.

To free a slot when at the cap, the merchant deletes an existing token from the list. There is no "request more tokens" path; the cap is fixed.

### Permission enforcement layers (defence in depth)

| Layer | Location | Behaviour |
|-------|----------|-----------|
| **Route middleware** | The `cli-tokens` route group is wrapped in the `isOwner` middleware. | Moderator hits any PAT endpoint → HTTP 403 **before any controller code runs**. |
| **Controller method** | Every action method (index, store, show, update, destroy, toggleStatus) starts with `if (!$admin?->isOwner) return 403`. | Belt-and-suspenders even if the middleware is misconfigured. |
| **Form Request authorize** | the platform code returns false unless the caller is owner. | Triggers a 403 **before validation rules even run**. |
| **Service layer** | the platform code re-checks `if ($admin->type !== 'owner') throw Error(...)`. | Last line of defence; any internal code that bypasses the HTTP stack still cannot create a token for a non-owner admin. |

So even a future bug at one layer wouldn't grant moderator access. Read-only operations (list, show) are **also** gated by owner-only — moderators cannot even see what PAT tokens exist on the store.

## Business rules

### Owner-only is binary — no delegation possible

There is **no permission row** in the [[settings-staff]] permission tree to delegate PAT-token management. The gate is binary (owner vs everyone else). A merchant who wants their developer to manage tokens has two options:

1. **Promote the developer to owner** (single-owner-per-store; only practical for tightly-held stores).
2. **Have the owner create the token** and share the value securely with the developer.

There is no "PAT manager" role.

### Moderator UI may show, but save will fail

The page UI may let moderators see the form in some code paths (legacy / cached client state), but the save action **always** fails. A moderator clicking the Create button gets an error message: *"Only store owners can create CLI tokens"*. This means an earlier wiki version's statement about "moderators granting a subset of their permissions" was **incorrect** — there is no scope-filtering logic that intersects requested scopes with the creating user's permissions, because the path is never reached for moderators.

### Permission inheritance is NOT how this works

Earlier wiki text suggested: *"moderators creating a PAT token can only grant scopes from the subset of permissions THEIR admin account has been given"*. This is wrong on two counts:

1. Moderators cannot create tokens at all.
2. The owner can grant ANY scope from the full catalog regardless of any internal permission grants on their own account.

The simpler reality: owner-only creates tokens with any allowed scopes; moderators can never create tokens.

### Cascade delete on Moderator removal

When a Moderator account is deleted from [[settings-staff]], **all their PAT tokens are automatically removed** along with the account. No orphaning, no manual cleanup needed. This matters for legacy tokens created before owner-only was enforced — they get swept up automatically when the moderator's account is removed.

(In current state, only owner-created tokens exist, so this cascade is mostly defensive — the owner account is rarely deleted.)

### Per-user cap reasoning

The `meta.max_tokens = 10` cap exists to limit blast radius if the owner's session is compromised — even an attacker with full owner session can only create 10 tokens before the cap kicks in. Combined with the hashing model ([[settings-pat-tokens-security]]) and the per-token IP allowlist ([[settings-pat-tokens-restrictions]]), this gives a reasonable defence in depth without overly constraining legitimate use (10 long-lived CI tokens covers most stores comfortably).

### Owner-only also gates the read endpoints

This is worth highlighting: not only Create / Update / Delete are owner-gated — **the GET endpoints (list, show) are too**. So Moderators cannot enumerate token names, scopes, IPs, or `last_used_at` timestamps. The PAT subsystem is fully opaque to non-owners.

## Related

- [[settings-pat-tokens]] — hub.
- [[settings-pat-tokens-list-view]] — what the owner sees (and moderators do not).
- [[settings-pat-tokens-create-flow]] — the create modal (which moderators never reach).
- [[settings-pat-tokens-endpoints]] — endpoint catalogue; every endpoint is owner-gated.
- [[settings-staff]] — admin / moderator permission tree; note the **absence** of any PAT-related permission row.
- [[merchant-roles]] — store owner vs administrator vs moderator distinctions.
- [[staff-member]] — entity page for staff records; PAT tokens are notionally per-staff but in practice owner-only.

## Open questions

- If ownership of a store is transferred (rare), are the previous owner's PAT tokens migrated, cascaded, or orphaned? `(verify)`
- Is the per-store cap of 10 ever expected to become plan-tier configurable, or is the hardcode permanent? `(verify)`
