---
type: concept
nav_path: "Concept → Merchant roles → Force sign out + 2FA"
aliases: ["Force sign out", "Mass logout", "sessionKeyGuard rotation", "Two-factor authentication admin", "Email two-factor", "Authenticator app TOTP", "cc2fa_secret", "cc2fa_verify", "2FA challenge create_moderator"]
tags: [access, security, 2fa, sessions, admin, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[merchant-roles]]. See the hub for the other aspects (owner, moderator, permissions tree, API access, notifications + audit, storefront contrast).

# Merchant roles — Force sign out + 2FA

## Definition

Two mechanisms protect admin sessions from credential leaks and unauthorised access:

1. **Force sign out** — an Owner-only button on [[settings-staff]] that mass-invalidates **every** admin session in one click. Immediate, audit-friendly. Deletes session records, invalidates the 2FA session layer, and signs the Owner out as a side effect.
2. **Two-factor authentication (2FA)** — per-admin-account verification on sensitive actions. Two channels: **email two-factor** (always-on after first login) and **authenticator-app TOTP** (opt-in via `cc2fa_secret`).

A third, lower-friction option — `sessionKeyGuard` cookie-name rotation on [[settings-general]] — achieves a similar end-result by making existing cookies stop being recognised. Less immediate, but useful when the merchant doesn't want to sign the Owner out.

## Scope

What this page covers:

- Force sign out — what it kills, what it doesn't.
- `sessionKeyGuard` rotation as a softer alternative.
- The two 2FA channels (email vs authenticator app).
- Which sensitive actions trigger a 2FA challenge.
- The `cc2fa_verify` session flag that lets a fresh challenge cover the next action.

Not covered here:

- The 2FA setup UI (QR code scan, recovery codes) — see [[account-cc2fa]], [[account-cc2fa-email]], [[account-cc2fa-codes]].
- The Moderator Edit modal's dynamic 2FA gate — covered in [[merchant-roles-moderator]] (the contrast between self / Owner-on-other / Moderator-on-Moderator).
- API-Key / PAT revocation (not affected by Force sign out) — see [[merchant-roles-api-access]].

## Contrasts

- **Force sign out vs `sessionKeyGuard` rotation** — both invalidate admin sessions. Force sign out is **Owner-only, immediate, audit-friendly** (button on [[settings-staff]] header). Session key rotation is on [[settings-general]] (Security box) and **rotates the cookie name pattern** so existing cookies stop being recognised — less immediate but doesn't require signing the Owner out.
- **Force sign out vs API-Key revocation** — Force sign out only kills human-facing browser sessions. It does **NOT** revoke API Keys or PAT Tokens — those are separate credentials with their own revocation surfaces ([[settings-api-keys]] / [[settings-pat-tokens]]). See [[merchant-roles-api-access]].
- **Email two-factor vs authenticator-app TOTP** — email two-factor is the default channel, **always active** for any admin who has logged in once. Authenticator-app TOTP is **opt-in** via the Configure button in the Edit modal; once configured (`cc2fa_secret` set), login defaults to the authenticator-app code (faster than email).
- **Fresh `cc2fa_verify` session flag vs every-action challenge** — once an admin passes a 2FA challenge in the current session, the `cc2fa_verify` flag lets the next sensitive action consume the flag instead of triggering a new challenge.

## Where it applies

### Force sign out — Owner-only mass logout

The Owner clicks Force sign out on [[settings-staff]] header. The action:

- Deletes every admin session record from the store's session storage.
- Invalidates the 2FA session layer (every admin must re-pass 2FA on next login).
- Forces a page reload that signs the Owner out too — they re-enter the login flow on next click.

This is the right button to use after a suspected credential leak, when a Moderator leaves the company in a hurry, or after a shared-laptop scenario. The audit signal is clean — one timestamp, all sessions gone.

**What Force sign out does NOT do:**

- Revoke API Keys or PAT Tokens. See [[merchant-roles-api-access]] — the merchant must walk each list and revoke individually.
- Change passwords. The Owner still has the same password after Force sign out; they just log back in.
- Affect storefront-customer sessions. Those are on a separate cookie / session mechanism — see [[customer]].

### `sessionKeyGuard` rotation — softer alternative

[[settings-general]] has a Security box with a session-key-rotation action (`sessionKeyGuard`). This rotates the cookie name pattern so any existing session cookie on a remote browser stops being recognised by the server. Effect:

- Existing sessions silently stop working on the next request.
- The acting Owner can keep their current session (depending on which path the rotation flow takes — verify).
- No "everyone is signed out right now" page-reload event.

Use this when the merchant wants to invalidate stray sessions without the disruption of the Owner getting kicked out.

### 2FA channels — email vs authenticator app

The platform supports two 2FA channels for each admin account:

- **Email two-factor** — codes sent to the admin's email on demand. **Always active** for any admin who has logged in once; the Edit modal shows it as *"Email two factor authentication is active."*
- **Authenticator-app TOTP** — the admin scans a QR code with Google Authenticator / Authy / 1Password / etc. Set up via the Configure button in the Edit modal. Once configured, login defaults to the authenticator-app code (faster than email). The `cc2fa_secret` field on the admin record stores the shared secret.

The configuration screens live on [[account-cc2fa]], [[account-cc2fa-email]], [[account-cc2fa-codes]].

### Sensitive actions that trigger 2FA

Certain actions trigger an extra 2FA prompt above the standard login challenge:

- **Creating a Moderator** — action `create_moderator`. The Owner (or delegating Moderator) must pass a 2FA challenge; on success, a one-time hash is issued and the create endpoint verifies it. See [[merchant-roles-moderator]] for the full 3-gate Create flow.
- **Editing a Moderator** (in many cases) — the gate is decided dynamically based on who's editing whom. See [[merchant-roles-moderator]] § Edit modal — 2FA gate decided dynamically.
- **Changing an admin's password** — typically gated by 2FA on the acting user's side if they have `cc2fa_secret` configured.

If the acting user has a fresh `cc2fa_verify` session flag (just passed a challenge in the current session), the gate is consumed and skipped for the immediately-following sensitive action.

### The `cc2fa_secret` and `cc2fa_verify` fields

- **`cc2fa_secret`** — per-admin field storing the TOTP shared secret. Set when the admin configures the authenticator app; cleared when they remove it.
- **`cc2fa_verify`** — session-level flag set when a 2FA challenge passes successfully. Consumed on the next sensitive action; without this flag, the action triggers a fresh challenge.

## Why this matters to the merchant

- **Operating without 2FA configured on the Owner account is risky for routine staff management.** Without an authenticator-app on the Owner, every Moderator-create / Moderator-edit falls back to email-only 2FA — slower, and vulnerable to a compromised email account.
- **Force sign out is the right blast-radius for credential leaks.** Don't rely on telling staff to "log out and back in" — use the button.
- **After Force sign out, walk the API-Key + PAT-Token lists too.** Programmatic credentials are unaffected by the button. See [[merchant-roles-api-access]].
- **`sessionKeyGuard` rotation is the low-friction periodic-hygiene option.** Rotate it on a schedule (e.g., quarterly) to invalidate stale sessions without disrupting the Owner.

## Related

- [[merchant-roles]] — hub.
- [[merchant-roles-owner]] — Force sign out is Owner-only.
- [[merchant-roles-moderator]] — Create / Edit flow's 2FA gates.
- [[merchant-roles-api-access]] — explicit note that Force sign out does NOT revoke API Keys / PATs.
- [[settings-staff]] — Force sign out button location (header).
- [[settings-general]] — `sessionKeyGuard` rotation under the Security box.
- [[account-cc2fa]] / [[account-cc2fa-email]] / [[account-cc2fa-codes]] — 2FA configuration screens.

## Open Questions

- ⏸️ Whether the Owner's own session survives a `sessionKeyGuard` rotation depends on which path the rotation flow takes (verify).
