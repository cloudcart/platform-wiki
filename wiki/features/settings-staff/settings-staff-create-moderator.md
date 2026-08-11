---
type: feature
nav_path: "Settings → Staff → Add moderator"
route_name: staff.settings.new
route_path: /admin/settings-new/staff
aliases: ["Add moderator", "Create moderator", "Add staff", "Moderator creation flow"]
tags: [settings, staff, create, 2fa, plan-gate]
plan_gates: ["administrators"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[settings-staff]]. See the hub for the other aspects (roles & list, edit, permissions, 2FA, delete, force sign out).

# Staff — add moderator (Create flow)

## Purpose

Documents the three-step chain triggered by the **Add moderator** button: plan-limit check → two-factor verification → Create modal. Also covers the one-time hash that ties the 2FA step to the create step, the hash's short shelf life, and the upsell modal shown when the seat cap is hit.

## Where to find it

Sidebar → Settings → **Staff** → header → **Add moderator** (button with `+` icon).

## What the merchant can do here

- Trigger the three-step Create flow from the page header.
- On a seat-capped plan, see the upsell modal and either purchase additional seats or cancel.
- Pass 2FA verification (authenticator-app or email-code channel) to obtain a one-time hash.
- Fill the Profile + Contacts + Permissions sections in the Create modal and submit to create the moderator.
- Optionally arrive on the Create modal directly via the `#create-<hash>` URL hash (skips the 2FA modal UI but the hash is still server-validated on submit).

## Settings & fields

### Page header — Add moderator button

| Control | Visible to | What it does |
|---------|------------|--------------|
| **Add moderator** (with `+` icon) | Everyone who can access the page | Loads form options (moderator types, permissions tree, current plan usage). If the plan limit is reached, opens the upgrade modal instead. Otherwise opens the 2FA prompt for the `create_moderator` action, then the Create modal with the obtained hash. |

### Step 1 — 2FA Action modal

Opened by **Add moderator** when the plan allows another seat. Action key: `create_moderator`.

| Element | Content |
|---------|---------|
| **Title** | *"Two-factor authentication"* (can vary by the user's configured method). |
| **Body** | Either (a) "Enter the 6-digit code from your authenticator app" (authenticator channel), OR (b) "We sent a verification code to your email — paste it below" (email channel). |
| **Code input** | 6-digit numeric input (8 chars for email-channel codes). |
| **Resend** link | (Email channel only) re-queues the code email. |
| **Verify** button | Submits the code. On success, a one-time hash is issued. |
| **Cancel** | Closes the modal without verifying — the Add flow is aborted. |

After successful verification the Create modal opens with the hash attached. See [[account-cc2fa]] for the generic 2FA-action mechanics.

### Step 2 — Create modal

Opens after successful 2FA verification. Title: *"Add moderator"*.

The new moderator type is fixed at `moderator`; only the single per-store owner can be `owner`.

**Sections** (same as Edit modal — see [[settings-staff-edit-profile]] for field-by-field details):

- **Profile** — Username (required, unique platform-wide), Email (required, RFC format, max 100 chars, unique), First name (required, max 100), Last name (required, max 100).
- **Contacts** — Country / City / Street address / Postal code / Phone number (all optional, max 100 chars each).
- **Access permissions** — a checkbox tree — see [[settings-staff-permissions-tree]] for delegate-only-what-you-have and `backups` plan-gating.

**Footer:**
- **Cancel** (closes — discards changes).
- **Save** (primary) — submits the create request with the one-time hash.

Validation errors surface inline per-field (red border + message). A toast also fires on global errors.

### Step 3 (optional) — Plan-limit upsell modal

Opens when the merchant clicks **Add moderator** but the plan's allowed `administrators` count is already reached.

| Element | Content |
|---------|---------|
| **Info banner** | Red error-box: *"You have reached the maximum number of administrators allowed, you need to purchase more to continue."* |
| **Plan-panel message** | *"You have reached the maximum number of administrators allowed, you need to upgrade your plan."* |
| **Body** | Standard plan-pack purchase module — shows the per-seat price and quantity selector. |
| **Buy** button | Submits payment via the merchant's stored billing method. |
| **Cancel** | Closes — Add flow aborted. |

On successful purchase the seat count increases by the purchased amount. The merchant must then click **Add moderator** AGAIN to start the 2FA flow — the modal does **NOT** auto-advance after the purchase.

## Business rules

### Three sequential gates

A moderator cannot be created without passing all three:

1. **Plan limit.** Allowed `administrators` seats vs the current admin count. If reached → upsell modal, not 2FA.
2. **2FA.** Complete a 2FA challenge with action key `create_moderator`. A one-time hash is issued on success.
3. **Server hash validation.** The create endpoint verifies the hash. Missing / expired / wrong-action hashes are rejected. On success, the hash is marked `used` so it cannot create a second moderator.

### One-time hash shelf life

The hash issued by the `create_moderator` 2FA action expires quickly:

- **Authenticator-app 2FA** — hash valid for **2 minutes** after the user completes the challenge.
- **Email-code 2FA** — hash valid for **60 minutes** after the email code is sent.

If the merchant completes verification then waits past the expiry before submitting the Create form, the server rejects with the hash-mismatch error and the merchant must redo 2FA. The hash is also single-use — once a moderator is created with it, the same hash can never create a second one.

### Username and email are globally unique within the platform

Username and email are checked for uniqueness across **all stores on the platform**, not just this store. A second admin with the same username or email anywhere returns 422 *"An admin with this name already exists"* or *"Email already exists"*. So a generic username like "admin" may already be taken on another store — the merchant must pick a unique handle.

### Plan downgrade does NOT auto-remove existing moderators

If the merchant downgrades to a plan that allows fewer moderator seats than they currently have, **existing moderators are NOT auto-deleted or suspended** — they keep their accounts and continue to log in. The plan limit is only enforced at creation: the Add moderator button stays disabled until the merchant either deletes excess moderators OR purchases extra seats. A downgrade leaves the merchant over-quota until they prune the list themselves.

### `new_admin_account` admin notification fires on success

On successful create, the `new_admin_account` admin notification is queued via [[settings-admin-notifications]]. Delivery is asynchronous (a background task). Recipient: `site_email` (from [[settings-general]]). Delivery is gated by the master `administrator_email_notifications` toggle AND the per-type toggle.

### Deep-link `#create-<hash>` bypasses Step 1 client-side only

The `#create-<hash>` URL hash opens the Create modal directly with that hash, skipping the 2FA modal UI. The server still validates the hash against the `create_moderator` action, so a forged / expired hash fails at submit. This supports email links like *"finish creating moderator X"* sent during multi-step onboarding.

### `settings.admins.create` permission carve-out

A `settings.admins.create` permission node exists but is **disabled** — in practice today only the owner sees the **Add moderator** button, regardless of what permissions a moderator holds on the staff section. A moderator without this allowance won't see the button. See [[settings-staff-permissions-tree]].

## Related

- [[settings-staff]] — hub.
- [[account-cc2fa]] — the generic Cc2FaAction modal mechanics.
- [[settings-admin-notifications]] — `new_admin_account` notification gating.
- [[settings-general]] — `site_email` recipient.
- [[plan-features]] — upsell modal.
- [[plan-vs-feature-pack]] — buying additional `administrators` seats as a pack.

## Open questions

None.
