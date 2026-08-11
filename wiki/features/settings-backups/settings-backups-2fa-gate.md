---
type: feature
nav_path: "Settings → Backup & Restore → 2FA gate"
route_name: backups.settings
route_path: /admin/settings/backups
aliases: ["Backups 2FA", "Restore 2FA challenge", "restore_backup action", "partial_restore_backup action", "Cc2FaAction restore", "Two-factor verification required"]
tags: [settings, backups, 2fa, security, restore]
plan_gates: ["backups"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-backups]]. See the hub for the other aspects (subscription gates, list view, full restore, partial restore, safety backup, restore progress).

# Backups — 2FA gate

## Purpose

Every restore call — full or partial — routes through a **mandatory 2FA challenge** before the API will accept it. The merchant has to complete the platform's 2FA flow on the spot, the page collects a single-use hash from the challenge, and the restore API call must carry that hash. A merchant without 2FA configured cannot start a restore at all.

This is a hidden but hard gate: the buttons render, the confirmation modal shows, but the actual restore is blocked by 2FA at the API layer.

## Where to find it

The 2FA challenge modal opens automatically after the merchant clicks **Yes, restore** on either:

- The full-restore confirmation modal at Sidebar → Settings → **Backup & Restore** ([[settings-backups-full-restore]]).
- The partial-restore confirmation modal at the per-backup partial-restore page ([[settings-backups-partial-restore]]).

The merchant's underlying 2FA configuration lives at [[account-cc2fa]].

## What the merchant can do here

- Complete the 2FA challenge by entering the code from their authenticator app (or whatever 2FA channel they have configured) → restore proceeds.
- Dismiss the modal → restore is NOT submitted; the merchant returns to the previous screen.

### What the merchant CANNOT do

- Skip 2FA. There is no bypass — without 2FA configured, the restore cannot run.
- Reuse a 2FA hash. The hash is single-use; the controller marks it `STATUS_USED` immediately after consuming it.

## Settings & fields

### The 2FA challenge modal (Cc2FaAction)

Both full and partial restores route through a `Cc2FaAction` modal. The modal is anchored to one of two action keys:

| Restore type | Action key |
|---|---|
| Full restore | `restore_backup` |
| Partial restore | `partial_restore_backup` |

The merchant completes the platform's 2FA flow on the spot — typically by entering a code from their authenticator app (or whatever 2FA channel they have configured in [[account-cc2fa]]). The modal returns a single-use hash, which the page then submits with the restore API call.

If the merchant doesn't have 2FA configured, the modal still appears but cannot be passed — the restore cannot run, and the merchant has to set up 2FA first at [[account-cc2fa]] before they can use the Backup & Restore feature at all.

### What the API expects on the restore call

Both `POST /backups/{id}/restore` and `POST /backups/{id}/partial-restore` require:

- A valid VERIFIED-but-not-yet-USED 2FA task hash for the appropriate action (`restore_backup` / `partial_restore_backup`).
- The hash is submitted with the request body (the page UI obtains it from the 2FA modal and posts it).

Validation errors returned by the API when 2FA is missing or wrong:

- *"Two-factor verification required"* — no hash supplied or task not verified.
- *"Invalid or expired verification"* — hash refers to a missing / already-used / expired 2FA task.

Both come back with HTTP 422 (verify).

## Business rules

### 2FA is hard-enforced on EVERY restore call

Both endpoints check the 2FA task hash on every call. This is not a "remembered" gate — even if the merchant just completed 2FA for another action, the next restore call requires a fresh challenge. The hash is single-use:

- The controller marks the task `STATUS_USED` immediately after consuming it.
- A second restore call with the same hash is rejected as *"Invalid or expired verification"*.

So a merchant who wants to do two restores back-to-back has to complete the 2FA challenge twice.

### No-2FA-no-restore — the restore button is effectively gated by 2FA setup

A merchant who has never configured 2FA on their account cannot start a restore at all. The modal still opens (it's part of the standard `Cc2FaAction` flow), but the merchant has nothing to enter into the challenge field — they have to set up an authenticator at [[account-cc2fa]] first, then come back.

For support: when a merchant says "I clicked Restore but nothing happened" or "I get a Two-factor verification required error", the first diagnostic is whether they have 2FA configured on their account.

### Different action keys for full vs partial

The 2FA task is scoped to its action key. A hash issued for `restore_backup` does NOT satisfy a `partial_restore_backup` call (and vice versa). This means the merchant can't pre-generate a "general restore" 2FA challenge and reuse it across both modes — each mode requires its own challenge.

### Practical implication for support tickets

The 2FA gate makes restore effectively require an admin user who can complete 2FA challenges. If the store's primary admin has lost 2FA access (phone wiped, authenticator app uninstalled), they cannot perform a restore until 2FA is recovered via the standard account-recovery process at [[account-cc2fa]]. Granting `settings.backups` permission to a moderator does NOT bypass 2FA — the moderator still has to complete their own 2FA challenge.

## Related

- [[settings-backups]] — hub.
- [[settings-backups-full-restore]] — fires the `restore_backup` 2FA action.
- [[settings-backups-partial-restore]] — fires the `partial_restore_backup` 2FA action.
- [[account-cc2fa]] — where the merchant configures their 2FA channel.
- [[settings-staff]] — `settings.backups` permission row; granting it does NOT bypass 2FA.

## Open questions

- Confirmed task lifetime (TTL) of an issued-but-unused 2FA hash for restore actions (verify).
- Whether SMS or email 2FA channels are accepted equivalently to authenticator-app codes (verify).
