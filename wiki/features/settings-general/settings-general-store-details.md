---
type: feature
nav_path: "Settings → Store settings → Store Details"
route_name: general.settings
route_path: /admin/settings/general
aliases: ["Store details", "Store name", "Store email", "Primary email", "Site email", "Footer copyright", "Powered by CloudCart", "Brand removal", "Email change confirmation"]
tags: [settings, general, store-details, email, branding, plan-gate]
plan_gates: ["brand_removal"]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

> Part of [[settings-general]]. See the hub for related aspects (locale, language, maintenance, security key, product badges, operational toggles, industry multi-select).

# Store settings — Store Details box

## Purpose

The Store Details box holds the **store identity** that surfaces on outgoing transactional emails, invoices, meta titles, and the storefront footer. Four fields: `site_email`, `site_name`, `copyright`, and the plan-gated `show_powered_by_info` switch. The single complex behaviour is the **email-change confirmation flow** — changing the email is a two-step double-handshake (one code to the old address, one to the new) that runs inline in the same box.

> The right-side info panel reads: *"Store details are used for general purposes like generating invoices, email signatures and other."*

## Where to find it

Sidebar → Settings → **Store settings** → first box (top of the page).

## What the merchant can do here

- Change the store's primary email address (with a two-code double-confirmation flow — see Business rules).
- Change the store name (used in transactional emails, meta titles, invoices).
- Edit the footer copyright text shown on the storefront footer.
- Toggle whether "Powered by CloudCart" shows in the footer (paid feature).

## Settings & fields

| Field / Control | What it does | Notes |
|-----------------|--------------|-------|
| **Email** (`site_email`) | The store's primary email. Used for outgoing transactional mail to customers and as the recipient for admin notifications. | Required. Must be syntactically valid (`required\|email`). Changing it triggers the two-step confirmation flow below. |
| **Store name** (`site_name`) | The display name of the store. Appears in email signatures, invoices, meta titles. | Required. **Max 100 characters** on the modern endpoint (max 191 on the legacy endpoint). Submitting longer text returns "The site name may not be greater than 100 characters." |
| **Footer Copyright** (`copyright`) | Free-text copyright line shown in the storefront footer. | Defaults to `Copyright © <current year>`. Multi-line allowed. |
| **Show CloudCart information in the footer** (`show_powered_by_info`) | Switch. When ON, the storefront footer shows "Powered by CloudCart". When OFF, that line is hidden. | **Plan-gated** by the `brand_removal` feature. Turning it OFF prompts a paid-feature upgrade modal — see Business rules. |

## Modals and sub-flows

### Email-change warning panel (inline in this box)

Not a separate modal — an inline panel that appears INSIDE the Store Details box as soon as the merchant types a new email and saves while a confirmation is pending. Contains:

- A warning describing the pending change: *"A change to <new email> is pending — confirm with the two codes sent."*
- Two **Code 1** / **Code 2** text inputs (8-character codes — Code 1 received on the OLD address, Code 2 on the NEW address).
- Three buttons: **Cancel** (clears `new_site_email` + both codes — keeps OLD email), **Resend emails** (re-queues both code emails with the existing codes — no regeneration), **Confirm** (replaces `site_email` with `new_site_email` and clears codes).
- Inline validation: `code1 ≠ code2`; mismatch returns *"Code is invalid."*

This panel is the merchant's only way to complete the email-change handshake — there is no separate "confirm email change" page.

### Plan-upgrade modal (Powered-by-CloudCart toggle)

A `PlanFeature` modal that opens when the merchant flips the **Show CloudCart information in the footer** switch from ON → OFF and the store does NOT have the `brand_removal` plan-feature. The feature record's `current` flag is read on page load — if `current=true` the toggle works normally; if `current=false` the modal opens and the switch reverts to ON until the merchant either pays for the upgrade (success callback re-runs with `current=true` and the toggle stays OFF) or cancels the modal (switch stays ON).

This is **NOT a confirm-discard modal**. It's a paid-feature upsell. The merchant either pays to disable Powered-by-CloudCart or keeps it visible.

## Business rules

### Email change is a two-step double-confirmation flow

When the merchant types a new value into the **Email** field and saves:

1. The system stores the new value in a separate `new_site_email` field. **`site_email` is NOT changed yet** — the store still uses the old address for outgoing notifications.
2. Two cryptographically random 8-character codes are generated (drawn until unique) and stored under settings keys `_code1` and `_code2` (underscore prefix marks them internal). Two emails are then queued on the `admin_notify` background queue: one to the OLD address with code 1, one to the NEW address with code 2.
3. The warning panel renders inline with the two code inputs and three buttons (**Cancel**, **Resend emails**, **Confirm**) — actions described in the Modals section above.
4. While the change is pending, `new_site_email` is populated AND visible to the merchant. Once Confirm completes, `new_site_email` and both codes are cleared. **Diagnostic answer:** "did my email change apply?" → yes iff the warning panel is gone and the Email field shows the new address; no if the warning panel is still showing.
5. **Important: email confirmation codes are NOT suppressed by the Admin Notifications master toggle.** Even with "Send notifications to administrators" turned OFF in [[settings-admin-notifications]], the two confirmation codes still go out — the `email_confirmation` notification is always-enabled there (toggle disabled in the UI, API rejects attempts to disable it, AND the dispatch helper enqueues directly, bypassing the master-toggle gate). If a merchant says "I never got the codes," it is NOT the admin notifications setting.
6. **CloudCart staff bypass:** when a CloudCart support agent is logged into the store via console-login (detected via `session('cc_console_login.auth_id')`), saving a new email **applies immediately** with no codes, no confirmation step, no `new_site_email` placeholder. The merchant is not notified.

### Email confirmation delivery is queued

Both confirmation emails are dispatched to the `admin_notify` background queue. Expected delivery: within a minute under normal load, longer if the queue is backed up. If the emails don't arrive after a few minutes: check spam / promotions on both addresses, re-trigger via **Resend emails** (uses the same codes — useful if the queue dropped the original), and verify the OLD address is still receivable. The Admin Notifications master toggle does NOT suppress these emails (rule 5 above).

### Legacy admin endpoint does NOT enqueue confirmation emails

The legacy controller (still used by the old admin UI) has its email-confirmation dispatch commented out. Only the modern Vue endpoint (`/admin/api/core/settings/general`) reliably triggers code emails. Merchants on the older admin path may need to retry via the new UI.

### "Show CloudCart information in the footer" is plan-gated

Turning the switch OFF prompts a `brand_removal` paid-feature upgrade modal. Without the feature, the switch reverts to ON. After a successful upgrade, the switch can stay OFF and the storefront footer hides "Powered by CloudCart".

### `site_email` is consumed by many downstream pages

The same `site_email` value feeds [[settings-admin-notifications]] (recipient of all admin emails), [[settings-invoicing]] (invoice defaults), [[settings-ssl]] (CSR contact email), and the outgoing-mail "From" header on transactional emails to customers. Changing it here propagates everywhere on next read.

## Related

- [[settings-general]] — hub.
- [[settings-admin-notifications]] — `site_email` is the single recipient address; the master toggle does NOT suppress email confirmation codes.
- [[settings-emails]] — outgoing mailbox / hosted-mail config (separate concept from `site_email` as sender).
- [[settings-invoicing]] — uses `site_email`, `site_name`, `copyright` as invoice defaults.
- [[settings-ssl]] — pre-fills CSR fields from `company_name`, `site_email`.
- [[plan-gates]] — concept page on plan-feature gates; `brand_removal` lives here.

## Open questions

None.
