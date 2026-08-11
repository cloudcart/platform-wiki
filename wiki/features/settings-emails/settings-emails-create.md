---
type: feature
nav_path: "Settings → Emails → Create new email"
route_name: emails.settings
route_path: /admin/settings/emails
aliases: ["Create mailbox", "Add new email", "New mailbox", "Mailbox create modal", "Email account create"]
tags: [settings, emails, mailbox, create, modoboa, discontinued]
plan_gates: []
status: DISCONTINUED
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-emails]] (DISCONTINUED). See the hub for related aspects (management, billing, DNS records, vs-other-mail, discontinued context).

# Emails — Create new email

## Purpose

The Create new email side modal is the entry point for **provisioning a new hosted mailbox** on one of the merchant's attached domains. It collects the mailbox local-part, the parent domain, a password (twice), display name (first + last), and a quota tier — then POSTs to create the mailbox in Modoboa, register a paid-subscription service order, and redirect the merchant to `/admin/services/purchase` to pay before the mailbox becomes active.

## Where to find it

Settings → Emails → **+ Add new email** button in the page header. The button surface is currently commented out in the live UI; when active it opens the **Create new email** side modal. The modal has a custom header (no default footer) with the title *"Create new email"* + Cancel / Save buttons.

## What the merchant can do here

### Create new email side modal — fields

The modal uses the `modal-right` class — slides in from the right side on desktop. Body is a multi-row grid b-card:

- **Row 1 — Name (username)**: single-line input, required. The local-part of the email address.
- **Row 2 — Domain**: searchable AJAX-fed dropdown from `/admin/api/core/settings/emails/domains`. Required.
- **Row 3 — Password + Confirm your password**: two columns, both PasswordInputComponent with eye toggle to reveal / hide. Both required.
- **Row 4 — First name + Last name**: two columns. Both required. Shown in the From header on outgoing mail.
- **Row 5 — Quota**: full-width AJAX-fed `SelectWithAjax` from `/admin/api/core/settings/emails/services` (returns the 5 service tiers + per-tier names + prices — see [[settings-emails-billing]] for the tier table).

### Save flow

POSTs to `/admin/api/core/settings/emails`. On success:

1. Emits `success(item)` so the parent unshifts the new row into the table.
2. Triggers a hidden anchor click that navigates to `/admin/services/purchase` for payment.
3. **The mailbox stays `active=no` until the subscription is paid** — see [[settings-emails-billing]].

## Settings & fields

### Create new email — modal fields

| Field | Required | Validation |
|-------|----------|------------|
| **Name** (username) | YES | Becomes the local-part of the email address. |
| **Domain** | YES | Picked from the merchant's attached external domains. |
| **Password** | YES | Pattern target (UI shows the policy text — see below). |
| **Confirm your password** | YES | Must match Password. Error: *"Passwords don't match"*. |
| **First name** | YES | Display name. |
| **Last name** | YES | Display name. |
| **Quota** | YES | Picks the storage tier (and thus the per-mailbox price). |

### Field validation messages

| Trigger | Exact message |
|---------|---------------|
| Empty required field | *"This field is required"* |
| Password mismatch | *"Passwords don't match"* |
| Weak password (policy hint shown) | *"Your password must be at least 8 characters long, contain at least 1 uppercase letter, 1 lowercase letter, 1 number and 1 special character."* |
| Server-side error | Generic error toast; specific messages from Modoboa surface inline. |

### Client-side validation behaviour

- Passwords must match — error *"Passwords don't match"* binds to the `password_confirmation` field.
- Each of `username`, `domain`, `first_name`, `last_name`, `password`, `password_confirmation`, `quota` must be non-empty — empty fields show *"This field is required"*.
- The strict client-side regex (min 8 chars, 1 upper, 1 lower, 1 digit, 1 special) is currently **commented out** in the live code — the policy string is loaded into translations but the check is bypassed. The server enforces its own policy.

## Business rules

### Domain must be attached + DNS-active before the modal can save successfully

The **Domain** dropdown is populated only from the merchant's **attached external domains** (those with `external=yes` in [[settings-domains]]). The default CloudCart subdomain (`*.cloudcart.net`) is excluded.

The merchant must:

1. Attach a custom domain via [[settings-domains]] (either externally-owned via "Add existing" or CloudCart-purchased via "Buy new" — see [[settings-domains-add-flow]]).
2. Wait for DNS to propagate so the domain is `active` in Cloudflare.
3. Then come here to create mailboxes on that domain.

Creating a mailbox on a domain that is still DNS-pending may succeed at the Modoboa level but emails won't actually be deliverable until DNS / MX records propagate. The auto-set MX / SPF / DMARC / DKIM records are written when the first mailbox is created on the domain — see [[settings-emails-dns-records]].

### Account creation flow (verified backend behaviour)

The Create endpoint:

1. Calls Modoboa's create-domain API — creates the domain on Modoboa's side, OR retrieves the existing one if it's already present.
2. Calls Modoboa's create-account API with the username, `SimpleUsers` role, password, quota, and first name — creates the mailbox account.
3. Inserts a local `ModoboaEmail` record linking the merchant's site to the Modoboa account.
4. Calls the service-order setup to create the recurring subscription.
5. Returns the new mailbox plus a redirect URL to `/admin/services/purchase`.

If the create-domain call fails with a non-conflict ClientException, the backend lists all existing Modoboa domains and tries to find one with a matching name. If neither succeeds, the merchant sees the original Modoboa error inline. A domain-already-exists race condition is handled gracefully; a network error on domain creation cascades visibly.

### Save → immediate redirect → mailbox is `active=no` until paid

On a successful POST, the parent table optimistically unshifts the new row, but the row's actions show **Activate** (not Webmail / Password / etc.) until the subscription is paid. See [[settings-emails-billing]] for the activation gate and [[settings-emails-management]] for the post-activation row actions.

### Password policy enforcement is server-side

The client-side regex is commented out, so weak passwords accepted by the browser will be rejected by Modoboa with a 400 — the merchant sees a generic error inline. Recommendation in support tickets: have the merchant set a password matching the displayed policy text.

## Related

- [[settings-emails]] — hub.
- [[settings-emails-billing]] — what happens after Save: subscription order, redirect to purchase, activation gate, tier table.
- [[settings-emails-dns-records]] — DNS auto-config that runs on the first mailbox per domain.
- [[settings-emails-management]] — the per-row actions that appear after activation.
- [[settings-domains]] — the parent screen where domains are attached + DNS-activated before they show up in this modal's Domain dropdown.
- [[settings-domains-add-flow]] — Add existing / Buy new flow that populates the merchant's external domain pool.

## Open questions

None.
