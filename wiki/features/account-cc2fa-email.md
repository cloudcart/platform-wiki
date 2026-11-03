---
type: feature
nav_path: "Account → Two-factor authentication → Email fallback"
route_name: admin.account.cc2fa-email.send
route_path: /admin/account/cc2fa-email
aliases: ["Email 2FA", "2FA Email", "Cc2fa email", "Email-based 2FA", "2FA code not arriving", "did not receive the login code", "verification code not received", "2FA email in spam", "cannot log in code not coming", "не получавам код за вход", "кодът за потвърждение не идва", "двуфакторен код по имейл", "как да ползвам приложение за кодове"]
tags: [account, security, 2fa, cc2factory, email-2fa]
plan_gates: []
created: 2026-05-22
updated: 2026-05-27
source_count: 4
---
# Two-factor authentication — Email fallback

## Purpose

The **Email 2FA** flow delivers the login code by e-mail instead of from an authenticator app ([[account-cc2fa]]). It is the channel used by an admin who has **not** set up an app.

Weaker security than authenticator-app 2FA (it is only as safe as the mailbox), but better than no 2FA.

> **It is not a rescue path for someone who already uses the app.** An account with an authenticator configured gets **no** e-mail code — see the first business rule below. Someone in that position who loses their device recovers with a [[account-cc2fa-codes|backup code]], which is why those must be saved at setup time.

## Where to find it

When the merchant is at the 2FA challenge during login AND has Email 2FA enabled, they see a "Send code via email" option. The code is sent via the `admin.account.cc2fa-email.send` route (GET `/admin/account/cc2fa-email/send`).

Setup of email-2FA may live alongside [[account-cc2fa]] (verify exact UI placement).

## What the merchant can do here

### Receive email 2FA code

When the merchant clicks "Send code to email" at the 2FA prompt:
1. The platform handles the request on route `admin.account.cc2fa-email.send`.
2. A code is generated + emailed to the admin's registered email.
3. The merchant enters the code at the prompt.
4. On valid code, login completes.

### Setup / activate email-2FA fallback

Email-2FA is **platform-level**, not per-admin self-service. It is activated by the `2fa_email` functionality flag. When that flag is ON for the store:

- The login form **hides the password input** (it becomes email-only).
- Submitting the email automatically logs the merchant in temporarily and sends a 6-digit code to their registered email.
- The merchant is redirected to the email-2FA code-entry page (the platform code).
- On the [[account]] page, an extra row appears confirming Email-2FA is enabled (green checkmark + envelope icon).

The merchant cannot toggle email-2FA from the admin UI — it's a platform-administrator override, typically used during account recovery scenarios.

### Code-entry page (what the merchant sees)

The code-entry page shows:

- Lock-icon header.
- Avatar + *"Signed in as `<email>`"* with **Exit** link → logout.
- **Envelope icon** centered.
- Page title: *"Two-factor authentication"*.
- Subtext: *"Your code expires at `<datetime>` `<timezone>`"* (rendered from `two_factor_expires_at` formatted in the store's date-time format).
- One **number input** for the 6-digit code (`name="code"`) — autocomplete off, spinner arrows hidden, displays as masked dots (`text-security: disc`).
- **Validate** button → `POST /admin/api/core/cc2fa-email/verify`.
- Footer hint: *"If you don't receive the code, check your spam folder."*

### What the merchant CANNOT do here
- Use email-2FA without a verified email address on the admin account.
- Use email-2FA if the merchant's email account is compromised — that defeats the purpose.

## Settings & fields

The available routes:
- `GET /account/cc2fa-email/send` — triggers email code dispatch.

## Business rules

### 🔴 Configuring the authenticator app stops the email code entirely

The email channel is **not** a parallel path that keeps running. The platform generates and sends an email code **only for an account with no authenticator secret configured**; once the app is set up, no email code is produced at all and the app's 6-digit code is what satisfies the challenge.

This is the answer when the email code is the problem — not arriving, landing in spam, delayed, or going to a mailbox the person can no longer open. **The app generates its codes on the device, with no message to deliver**, so nothing about mail routing, filtering or delivery delay can affect it. Setting it up removes the dependency rather than working around it.

Setup is a one-off: **Configure** in the 2FA section, scan the QR with any authenticator (Google Authenticator, Authy, 1Password and the rest), enter the confirming code. Per person, not per store — see [[settings-staff-2fa]]. Save the [[account-cc2fa-codes|backup codes]] at the same time, since they are the way back in if the device is lost.

### Lower security than authenticator-app

Email-2FA codes are easier to intercept (a compromised mailbox means full access). Authenticator-app codes are stronger because the secret never leaves the device.

So the app is the better channel on both counts — it is harder to intercept **and** it cannot fail to arrive.

### Time-limited codes

An email code is valid for **60 minutes** from the moment it is sent.

### Permission
Standard account permission scope.

## Related

- [[account-cc2fa]] — main 2FA setup (authenticator-app).
- [[account-cc2fa-codes]] — backup codes.
- [[account]] — account hub.

## How it works (verified against backend)

### Email code is a 6-digit number, valid for 60 minutes

The email-code flow:

- The platform generates a random 6-digit number (between 100000 and 999999) and stores it on the admin record as `two_factor_code`.
- The code is valid for **60 minutes** (`two_factor_expires_at = now + 60 minutes`).
- A notification email is queued and delivered to the admin's registered email address.

When the merchant enters the code, the platform clears both `two_factor_code` and `two_factor_expires_at` — codes are single-use.

### Send-by-email triggers automatic admin login first

The email-2FA send flow logs the merchant in BEFORE generating the code: the platform identifies them by the email address on the form, then sends the code to it.

Note that this is **not** a route around a lost authenticator. The generator exits without producing anything when the account has an authenticator secret, so an admin who set up the app and then lost the device gets no email however the send is triggered — the way back in is a [[account-cc2fa-codes|backup code]].

### Email 2FA is a fallback, not the primary mechanism

The code is generated only if the platform-side `2fa_email` feature flag is true. If the flag is OFF, the email-fallback path is bypassed and the merchant has to use the authenticator app or backup codes instead.

## Open questions
