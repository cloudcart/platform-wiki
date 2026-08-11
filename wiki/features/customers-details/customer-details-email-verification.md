---
type: feature
nav_path: "Customers → Customer details → Email verification"
route_name: customers-details.new
route_path: /admin/customers-new/details/:id
aliases: ["Customer email verification", "Confirm email address", "Send confirmation email", "Email pending confirmation"]
tags: [customers, profile, detail, email, verification]
plan_gates: ["customers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[customers-details]]. See the hub for the other aspects (identity card, tab strip, ban flow, default address, delete).

# Customer details — Email verification flow

## Purpose

The **email verification status indicator** + the two **manual override actions** on the identity-card dropdown. CloudCart customers register with an email that needs verification (a confirmation link sent to the address); when that link hasn't been clicked the email is in an *"unverified"* state and the storefront treats certain features (e.g., re-using a saved address, password reset) more cautiously.

The detail page surfaces both **read** (the red *"Email address not verified"* indicator) and **write** (manual confirm / re-send) sides of this flow. The two overrides exist because phone-verified customers shouldn't be blocked by an undelivered email, and because typo'd emails should still be recoverable.

## Where to find it

[[customers]] → click any row → opens `/admin/customers-new/details/:id`. The email-verification surfaces:

- **Status indicator** — on the [[customer-details-identity-card|identity card]], directly under the email field. Red text + red X when unverified; standard text when verified.
- **Confirm email address** — dropdown item on the identity-card pencil. Visible only when `email_confirmed = no`.
- **Send confirmation email** — dropdown item on the identity-card pencil. Visible only when `email_confirmed = no`.

## What the merchant can do here

### Status indicator (read-only)

The email row of the identity card has two visual states:

| State | Display |
|-------|---------|
| `email_confirmed = no` | Red text *"Email address not verified"* + red X icon. |
| `email_confirmed = yes` | Email rendered in standard text — no extra indicator. |

The indicator is the merchant's signal to either ask the customer to click their confirmation link, or to use one of the two manual overrides below.

### "Confirm email address" — bypass

The first dropdown option. Manually marks the email as verified by calling the `verify-email` action on the admin customer endpoint, **bypassing** the customer's confirmation flow entirely. Toast on success: *"Email confirmed successfully"*.

**When to use**: the merchant has already verified the customer's identity through another channel (e.g., phone call) and wants to skip the email round-trip.

### "Send confirmation email" — regenerate

The second dropdown option. Re-sends the verification email to the customer via the `send-verification-email` action. Toast on success: *"Verification email sent"*.

**When to use**: the customer never received the original confirmation email (spam folder / bounced / lost in inbox), or the original is too old. The customer must click the freshly-sent link to verify.

## Settings & fields

| Field | Role | Set by |
|-------|------|--------|
| `email` | Currently-active email address | Customer registration / merchant edit (after confirmation). |
| `email_confirmed` | enum `yes` / `no` | Confirmation-link click, OR the *Confirm email address* manual override. |
| `email_for_confirmation` | Pending new email address (during email-change flow) | Merchant edits email via the identity-card modal. |
| `email_confirm_code` | 40-char random verification token | Regenerated on every *Send confirmation email* call. |
| `date_confirm_sent` | Timestamp of the most-recent confirmation send | Updated on *Send confirmation email*. |

None of these fields are directly editable from a form — they're driven by the dropdown actions and the customer's click on the email link.

## Business rules

### Email-change flow goes through pending-confirmation state

When the merchant edits the customer's email to a NEW address via the identity-card modal, the platform does **NOT** immediately update the `email` field. Instead it:

1. Stores the new address in `email_for_confirmation`.
2. Keeps the OLD address as the customer's current `email`.
3. Flips `email_confirmed` to `no`.
4. Sends a confirmation link email to the NEW address.

The customer must click the link in the new-address email for the change to take effect. So a typo in an email change doesn't lock the customer out — they still log in with the old email until they confirm the new one. The *"Email address not verified"* indicator is the merchant's signal that the change is pending.

### "Confirm email address" has NO audit trail

The *Confirm email address* override flips `email_confirmed` to `yes` directly (via `GET /admin/api/core/customers/verify-email/{id}`) without sending or requiring any link. There's **NO** audit log of who confirmed it or when `(verify)`.

Useful when the merchant has verified the customer's identity by phone — but it bypasses the email round-trip and leaves no trace. For B2B / wholesale where audit matters, prefer *Send confirmation email* and have the customer click the link.

### "Send confirmation email" invalidates earlier codes

The *Send confirmation email* option generates a **NEW** `email_confirm_code` (40-char random string) and updates `date_confirm_sent`. So if a prior confirmation email is still in the customer's inbox, the link from the OLD email is now invalid — only the freshly-sent code works. This prevents accidental confirmation from stale links and is the right action when the merchant suspects the original email was intercepted.

### Both overrides are admin-only

Both dropdown options are admin-only — they are NOT exposed via [[json-api-v2]]. Merchants automating customer onboarding (e.g., from an ERP feed) cannot programmatically confirm emails through JSON-API v2; they must use the admin REST routes documented in the API reference, OR rely on the standard customer-click confirmation flow.

### Status indicator drives the dropdown visibility

The *Confirm email address* and *Send confirmation email* dropdown items are conditional on `email_confirmed = no`. When the customer's email is already verified, both items are hidden from the dropdown — only *Edit customer* and *Change password* remain.

### Email-change does NOT fire `customer.updated` until confirmed

The `customer.updated` webhook fires on the field change, but the actual `email` field doesn't change until the customer clicks the link — so subscribers to the webhook see the unchanged email until confirmation lands `(verify)`. Receivers needing the new email should react to a subsequent `customer.updated` event after confirmation.

## Related

- [[customers-details]] — hub.
- [[customer-details-identity-card]] — identity card; hosts the status indicator and the dropdown.
- [[customer]] — entity page; carries `email`, `email_confirmed`, `email_for_confirmation`, `email_confirm_code`, `date_confirm_sent`.
- [[customers]] — list page; also surfaces verification status via list-column filters.
- [[customers-sign-in]] — storefront sign-in flow that consumes the `email_confirmed` flag.
- [[settings-hooks]] — `customer.updated` webhook lifecycle.

## Open questions

- Confirm whether *Confirm email address* leaves any audit log (admin-action history table, etc.).
- Confirm whether the `customer.updated` webhook fires both at email-change-request time and at confirmation time, or only once.
