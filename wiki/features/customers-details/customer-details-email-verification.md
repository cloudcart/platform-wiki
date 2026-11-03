---
type: feature
nav_path: "Customers → Customer details → Email verification"
route_name: customers-details
route_path: /admin/customers/details/:id
aliases: ["Customer email verification", "Confirm email address", "Send confirmation email"]
tags: [customers, profile, detail, email, verification]
plan_gates: ["customers"]
created: 2026-06-10
updated: 2026-11-03
source_count: 4
---

> Part of [[customers-details]]. See the hub for the other aspects (identity card, tab strip, ban flow, default address, delete).

# Customer details — Email verification flow

## Purpose

The **email verification status indicator** + the two **manual override actions** on the identity-card dropdown. CloudCart customers register with an email that needs verification (a confirmation link sent to the address); when that link hasn't been clicked the email is in an *"unverified"* state and the storefront treats certain features (e.g., re-using a saved address, password reset) more cautiously.

The detail page surfaces both **read** (the red *"Email address not verified"* indicator) and **write** (manual confirm / re-send) sides of this flow. The two overrides exist because phone-verified customers shouldn't be blocked by an undelivered email, and because typo'd emails should still be recoverable.

## Where to find it

[[customers]] → click any row → opens `/admin/customers/details/:id`. The email-verification surfaces:

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

The first dropdown option. Manually marks the email as verified, **bypassing** the customer's confirmation flow entirely. On success the red indicator and both dropdown items disappear; no toast shows.

**When to use**: the merchant has already verified the customer's identity through another channel (e.g., phone call) and wants to skip the email round-trip.

### "Send confirmation email" — regenerate

The second dropdown option. Re-sends the verification email to the customer. On success nothing changes on screen and no toast shows; only a failure shows a message.

**When to use**: the customer never received the original confirmation email (spam folder / bounced / lost in inbox), or the original is too old. The customer must click the freshly-sent link to verify.

## Settings & fields

| Field | Role | Set by |
|-------|------|--------|
| `email` | Currently-active email address | Customer registration / merchant edit. |
| `email_confirmed` | enum `yes` / `no` | Confirmation-link click, OR the *Confirm email address* manual override. |
| `email_for_confirmation` | Pending new email address (during the email-change flow) | The customer's own email change on the storefront, or an email change through JSON-API v2. |
| `email_confirm_code` | 40-char random verification token | Regenerated on every *Send confirmation email* call. |
| `date_confirm_sent` | Timestamp of the most-recent confirmation send | Updated on *Send confirmation email*. |

None of these fields are directly editable from a form — they're driven by the dropdown actions and the customer's click on the email link.

## Business rules

### Editing the email in the panel applies at once

When the merchant edits the customer's email in the identity-card panel, the new address takes effect immediately. No confirmation email goes out, and the verification state stays as it was.

The customer's own email change on the storefront, and a change through JSON-API v2, work differently: the new address waits in `email_for_confirmation`, the current one stays, and a confirmation link goes to the new one. *Send confirmation email* sends to the pending address when there is one.

### "Confirm email address" needs no link

The *Confirm email address* override flips `email_confirmed` to `yes` directly (via `GET /admin/api/core/customers/verify-email/{id}`) without sending or requiring any link.

Useful when the merchant has verified the customer's identity by phone. For B2B / wholesale, *Send confirmation email* has the customer click the link themselves.

### "Send confirmation email" invalidates earlier codes

The *Send confirmation email* option generates a **NEW** `email_confirm_code` (40-char random string) and updates `date_confirm_sent`. So if a prior confirmation email is still in the customer's inbox, the link from the OLD email is now invalid — only the freshly-sent code works. This prevents accidental confirmation from stale links and is the right action when the merchant suspects the original email was intercepted.

### Both overrides are admin-only

Both dropdown options are admin-only — they are NOT exposed via [[json-api-v2]]. Merchants automating customer onboarding (e.g., from an ERP feed) cannot programmatically confirm emails through JSON-API v2; they must use the admin REST routes documented in the API reference, OR rely on the standard customer-click confirmation flow.

### Status indicator drives the dropdown visibility

The *Confirm email address* and *Send confirmation email* dropdown items are conditional on `email_confirmed = no`. When the customer's email is already verified, both items are hidden from the dropdown — only *Edit customer* and *Change password* remain.

### An email edit in the panel fires `customer.updated`

Saving the panel fires the `customer.updated` webhook with the new email. See [[settings-hooks]].

## Related

- [[customers-details]] — hub.
- [[customer-details-identity-card]] — identity card; hosts the status indicator and the dropdown.
- [[customer]] — entity page; carries `email`, `email_confirmed`, `email_for_confirmation`, `email_confirm_code`, `date_confirm_sent`.
- [[customers-sign-in]] — storefront sign-in flow that consumes the `email_confirmed` flag.
- [[settings-hooks]] — `customer.updated` webhook lifecycle.

## Open questions

None.
