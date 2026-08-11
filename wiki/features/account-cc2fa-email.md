---
type: feature
nav_path: "Account → Two-factor authentication → Email fallback"
route_name: admin.account.cc2fa-email.send
route_path: /admin/account/cc2fa-email
aliases: ["Email 2FA", "2FA Email", "Cc2fa email", "Email-based 2FA"]
tags: [account, security, 2fa, cc2factory, email-2fa]
plan_gates: []
created: 2026-05-22
updated: 2026-05-27
source_count: 4
---
# Two-factor authentication — Email fallback

## Purpose

The **Email 2FA** flow is the **fallback alternative to authenticator-app TOTP** ([[account-cc2fa]]) for admins who cannot use an authenticator app (e.g., lost their phone, no auth-app installed). Instead of a 6-digit TOTP from Google Authenticator / 1Password / etc., the merchant receives a one-time code via email.

Weaker security than authenticator-app 2FA (gated by email-account security), but better than no 2FA.

## Where to find it

When the merchant is at the 2FA challenge during login AND has Email 2FA enabled, they see a "Send code via email" option. The code is sent via the `admin.account.cc2fa-email.send` route (GET `/admin/account/cc2fa-email/send`).

Setup of email-2FA may live alongside [[account-cc2fa]] (verify exact UI placement).

## What the merchant can do here

### Receive email 2FA code

When the merchant clicks "Send code to email" at the 2FA prompt:
1. The platform calls the request handler (route `admin.account.cc2fa-email.send`).
2. A code is generated + emailed to the admin's registered email.
3. The merchant enters the code at the prompt.
4. On valid code, login completes.

### Setup / activate email-2FA fallback

Email-2FA is **platform-level**, not per-admin self-service. It is activated by toggling the `2fa_email` functionality flag (the platform code). When that flag is ON for the store:

- The login form **hides the password input** (it becomes email-only).
- Submitting the email automatically logs the merchant in temporarily and sends a 6-digit code to their registered email.
- The merchant is redirected to the email-2FA code-entry page (the platform code).
- On the [[account]] page, an extra row appears confirming Email-2FA is enabled (green checkmark + envelope icon).

The merchant cannot toggle email-2FA from the admin UI — it's a platform-administrator override, typically used during account recovery scenarios.

### Code-entry page (what the merchant sees)

The OTP entry view (`Cc2FactoryEmail/the platform code`):

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

### Lower security than authenticator-app

Email-2FA codes are easier to intercept (compromised email account = full access). Authenticator-app TOTP is more secure because the secret never leaves the device.

Recommendation: use authenticator-app 2FA whenever possible; email-2FA only as fallback.

### Time-limited codes

Email codes typically have a 5-15 minute validity window (verify exact duration).

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

The email-2FA send flow logs the merchant in BEFORE generating the code. This is because the email-2FA send route is what the platform uses as a recovery path — the merchant who can't access their authenticator clicks "Send code via email" at the 2FA challenge, the platform identifies them by their email address from the form, and then sends the code.

### Email 2FA is a fallback, not the primary mechanism

The code is generated only if the platform-side `2fa_email` feature flag is true. If the flag is OFF, the email-fallback path is bypassed and the merchant has to use the authenticator app or backup codes instead.

## Open questions
