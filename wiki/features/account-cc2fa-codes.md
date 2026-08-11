---
type: feature
nav_path: "Account → Two-factor authentication → Backup codes"
route_name: cc2fa.qr.codes
route_path: /admin/account/cc2fa/codes
aliases: ["2FA codes", "Backup codes", "Recovery codes", "Cc2fa codes"]
tags: [account, security, 2fa, backup-codes, recovery]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 4
---
# Two-factor authentication — backup codes

## Purpose

The **backup codes** sub-page lists the one-time-use recovery codes generated during [[account-cc2fa]] setup. Each code can substitute for the authenticator app's 6-digit TOTP ONCE — used when the merchant loses access to their authenticator (phone lost, app reinstalled, switched devices).

Critical security artifact — the merchant should **save these codes somewhere safe BEFORE losing authenticator access** (password manager, printed and locked away). Without them AND without authenticator access, recovery requires CloudCart support.

## Where to find it

Sidebar → Profile → Two-factor authentication → **Backup codes** OR direct route `/admin/account/cc2fa/codes`.

Breadcrumb: "Profile → Two-factor authentication → Backup codes".

## What the merchant can do here

- See the list of backup codes still available (used codes are typically removed or marked used).
- Download / print / copy codes for safekeeping.
- Regenerate codes — invalidates all current ones and creates a fresh batch (verify exact behaviour).

### What the merchant CANNOT do here
- Use a code more than once. After consumption, it's permanently invalid.
- Recover a lost code — once gone, the merchant has fewer codes available; regenerate to start fresh.
- View the codes without 2FA being already set up (this page assumes 2FA is active).

## Settings & fields

The page displays the codes as a list. Each code is typically a short alphanumeric string (8-10 characters).

Actions available on the page (bottom-right of the codes card):

- **Download** (`fa-arrow-to-bottom` icon) — exports codes as a CSV file named `cc2fa.csv` with two columns: `code` and `used` (Yes/No). The download is triggered via the shared `downloadCSV` helper.
- **Print** (`fa-print` icon) — opens a new browser window with the codes-card HTML cloned, attaches all current stylesheets, and immediately calls `window.print`.
- **Copy** (`fa-copy` icon) — joins all codes with newlines, copies to the clipboard via `vue3-clipboard`, toast confirms *"The text has been successfully copied to the clipboard"* (or *"Copying text error"* on failure).

After any of the three actions, `isCompleted` flips to true and the **Finish** button becomes available at the top — clicking it pushes the router to `dashboard`. The page also auto-scrolls to the Steps indicator so the merchant sees the Finish CTA.

### What each code row shows

The page renders codes in a two-column grid (`xl="6"` per code, full-width on mobile). Each row is a `<pre>` element. **Used codes** appear with `text-danger` colour + `text-decoration: line-through` — visible but greyed/struck. **Unused codes** display in normal black.

### No explicit "Regenerate" button on the page itself

The page does NOT expose a manual regenerate action. Instead, the **pool auto-replenishes to 12 unused codes** every time the merchant lands on this page. So if the merchant burned through 3 codes, just re-visiting the page tops them up. The platform-side the platform code exists but is wired to admin support flows (CloudCart staff resets) — not surfaced to the merchant directly.

## Business rules

### One-time use per code
Each code is invalidated immediately on use. The platform tracks consumed codes.

### Number generated
Typically 8-10 codes per regeneration (verify exact count).

### Regeneration invalidates all
Generating a new set invalidates the entire previous set — all codes are replaced. The merchant must save the new set.

### Code format
Short alphanumeric strings, intentionally short for easy manual entry at the login prompt. Typically NOT case-sensitive.

### Cannot recover via codes alone
Backup codes work IN ADDITION to the authenticator app — they let the merchant log in WITHOUT the authenticator, but only N times. After all codes are consumed AND the authenticator is gone → support is the only recovery path.

### Permission
Standard account permission scope (per-admin).

## Related

- [[account-cc2fa]] — main 2FA setup page.
- [[account]] — account hub.

## How it works (verified against backend)

### Pool size: 12 unused codes, auto-topped-up

Per the platform code method: every time the merchant opens the backup-codes page, the platform checks how many UNUSED codes exist. If fewer than 12, it generates new ones to top up to 12. So after the merchant uses 3 codes (e.g., to log in 3 times without their authenticator), the next visit to this page replenishes to 12 — the merchant always sees up to 12 fresh codes available.

### Code format: two blocks of 10 random alphanumeric characters

Each code is `XXXXXXXXXX-XXXXXXXXXX` (two blocks of 10 alphanumeric characters separated by a hyphen, 21 characters total including the hyphen). The character set is mixed-case letters and digits.

### One-time use, consumed codes preserved

Per the `validateBackupCode` controller: when the merchant uses a code, the platform sets `used = 1` on that code row — the code is permanently invalidated for future use. Used codes are NOT deleted (the row is kept for audit), but they don't show on the merchant's list of available codes.

### Codes are admin-specific

The codes are stored in the `admins_2fa_codes` table with an `admin_id` foreign key. Each admin sees only their own codes — there is no shared pool. If a multi-admin store has 3 staff with 2FA enabled, each has their own independent 12-code pool.

### Codes work alongside the authenticator app

The merchant can use a backup code OR a current TOTP from the authenticator app to satisfy the 2FA challenge at login. The backup code path doesn't require the authenticator to be disabled — codes are a parallel recovery mechanism, not a replacement.

## Open questions
