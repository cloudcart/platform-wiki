---
type: entity
nav_path: "Entity → Customer → Authentication & email confirmation"
aliases: ["Customer authentication", "Customer password", "Customer email confirmation", "Email change re-confirmation", "Customer saved cards", "Social login", "Password reset"]
tags: [entity, customers, auth, password, email, security]
plan_gates: ["customers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customer]]. See the hub for the other aspects (attributes, lifecycle, status flags, relationships, API + webhooks).

# Customer — Authentication & email confirmation

## Identity

The mechanics behind how a [[customer|Customer]] authenticates against the storefront — password rules (storefront vs admin), email-confirmation flow, the email-change re-confirmation handshake, social-account linking, and the saved-payment-token columns. Plus the `unconfirmed_accounts_restrict` setting that gates unverified accounts.

## Aliases

- **Customer authentication** — the storefront login path.
- **Email confirmation** — the verification-link flow.
- **Email change re-confirmation** — the pending-email handshake when the merchant updates `email`.
- **Saved payment tokens** — `epay_one_touch`, `stripe`, `mypos`, `raiffeisen`, `borica_way4`.
- **`unconfirmed_accounts_restrict`** — the setting that gates unverified accounts.

## Key Attributes

### Password rules (storefront vs admin)

Password length is bounded **3-20 characters** for both the registration form and password changes:

- `customer.err.password_min_chars_3` — too short.
- `customer.err.password_max_chars_20` — too long.

On the **storefront** the customer changing their own password MUST supply `password_old` (the current password). Without it, the change is rejected with *"Empty old password"* / *"Invalid old password"* / `customer.err.invalid_old_password`. The `password_repeat` field must match `password` when both are supplied (`customer.err.passwords_mismatch`).

From the **admin** side ([[customers-change-password]]) the moderator can set a new password **directly without supplying the old one** — useful for support tickets where the customer has lost access.

Password hashes are salted with a 5-character random `salt` per record and use a peppered hash. There is no admin-visible password (always hashed).

### Email confirmation flow

After registration, the platform:

1. Sets `email_confirmed = no`.
2. Generates a token in `email_confirm_code`.
3. Sends the confirmation email containing the link with that code.
4. Stores `date_confirm_sent` (used for resend rate-limiting).

When the customer clicks the link, `email_confirmed` flips to `yes` and the token is cleared.

### `unconfirmed_accounts_restrict` — two values only

The `unconfirmed_accounts_restrict` setting on [[settings-cart]] takes exactly **two values**:

| Value | Effect on customers with `email_confirmed = no` |
|-------|------------------------------------------------|
| `none` (default) | Unconfirmed-email accounts can do everything — browse, log in, add to cart, checkout. |
| `checkout` | Unconfirmed-email accounts can browse and add to cart but are **blocked at checkout** until they verify their email. |

No other gate values are supported. Validation errors:

- *"Setting 'Restrict unconfirmed accounts' is required"* — when the setting is empty.
- *"The selected unconfirmed accounts restrict is invalid"* — for any value other than `none` or `checkout`.

### Email-change re-confirmation flow

When the merchant changes `email` on an existing customer via admin edit (or the customer changes it on the storefront), the platform:

1. Stores the **NEW** email in `email_for_confirmation` and keeps the **ORIGINAL** `email` in place (so the customer can still log in with the old address until they confirm the new one).
2. Sets `email_confirmed = no` and triggers a new confirmation email.
3. When the customer clicks the confirmation link, the `email_for_confirmation` value is **promoted to** `email` and the field is cleared.

**Edge cases**:

- If the merchant changes the email a second time **BEFORE** the first confirmation lands, the new value overwrites `email_for_confirmation`.
- If the merchant re-saves the SAME email as `email_for_confirmation` (i.e. the customer hasn't confirmed yet), the platform **re-sends the confirmation email** instead of issuing a new pending change.

The two original-vs-confirmation paths converge automatically.

### Forgot-password / reset-link flow

The storefront's "Forgot password" flow generates a one-time reset link and emails it. Clicking the link lets the customer set a new password without supplying the old one (the link itself is the proof). The admin-side `customers-change-password` flow is a **different path** — it sets a specific value rather than emailing a reset link.

### Saved payment tokens — per-provider columns

The Customer model carries dedicated columns for each supported provider's tokenised payment:

- `epay_one_touch`
- `stripe`
- `mypos`
- `raiffeisen`
- `borica_way4`

Plus the `CustomerCard` relation for general saved cards.

These are populated by the customer accepting "remember my card" at checkout on a supporting provider. They are **NEVER exposed in API responses or admin exports** for security — the same exclusion applies to:

- JSON-API v2 reads (see [[customer-entity-api-and-webhooks]]).
- [[customers-export]] CSV exports.
- Webhook payloads on `customer.created` / `customer.updated`.

Empty for guest customers (guests do not have a checkout flow that stores tokens).

### Social-account linking

The `SocialAccount` relation links the customer to Facebook / Google / Apple login bindings. A customer can have multiple social accounts. The `is_activated` flag is used in social-account / magic-link flows to mark when activation completed end-to-end.

Customers who registered exclusively via social login may have an **empty password** field — they can only log in via the social provider until the merchant or the customer sets a password (see [[customers-change-password]]).

### Remember-me cookie

The `remember_token` column stores the persistent-login cookie value. It is rotated on each successful login when "remember me" is checked, and cleared on logout.

### Banned customers cannot authenticate

Banned customers (`banned = yes`) cannot log in regardless of password validity — the storefront throws `'sf.global.err.customer_banned'` with the embedded reason and date. See [[customer-entity-status-flags]] for the full ban semantics.

Inactive customers (`active = no`) cannot log in either — the storefront throws `'sf.err.account.inactive'`. The password check is reached only after the active + banned gates pass.

## Where it appears

- [[customers-change-password]] — admin path to set a specific password (no old-password check).
- [[customer-login]] — storefront login page.
- [[customer-register]] — storefront registration form.
- [[customer-account]] — storefront account preferences (password change, email change).
- [[settings-cart]] — `unconfirmed_accounts_restrict`, "Convert guests into members" toggle.

## Related

- [[customer]] — hub.
- [[customer-entity-attributes]] — the per-field schema (password, email, salt, etc.).
- [[customer-entity-status-flags]] — banned / inactive gates run before password check.
- [[customers-sign-in]] — admin impersonation (log in AS the customer).
- [[settings-cart]] — restrict-unconfirmed setting.

## Open Questions

- ⏸️ Whether storefront `password_repeat` is required at registration too, or only at password-change time (verify against the registration form on [[customer-register]]).
- ⏸️ Whether the email-change re-confirmation flow re-checks `unconfirmed_accounts_restrict` (i.e., does the customer get blocked at checkout while the new email is pending confirmation, even though the OLD email was confirmed?).
