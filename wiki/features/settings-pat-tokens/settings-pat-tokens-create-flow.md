---
type: feature
nav_path: "Settings → PAT Tokens → Create / Edit modal"
route_name: pat-tokens.settings
route_path: /admin/settings/pat-tokens
aliases: ["Create PAT Token modal", "Edit PAT Token modal", "Token Created Successfully", "PAT one-shot reveal", "Generate Token button"]
tags: [settings, security, tokens, modal, create, edit]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 3
---

> Part of [[settings-pat-tokens]]. See the hub for related aspects (list view, scopes, restrictions, security, permissions, endpoints).

# PAT Tokens — create / edit modal

## Purpose

The right-side modal for creating a PAT token or editing one. The two modes differ only in the visible sections, the editable fields and the primary button. It also hosts the **one-shot token reveal**, the green card shown right after a create.

## Where to find it

- **Create:** Settings → PAT Tokens → **Create Token** header button (only when `meta.can_create=true`), OR the empty state's **Create Your First Token** button.
- **Edit:** Settings → PAT Tokens → click any row's Name cell. See [[settings-pat-tokens-list-view]] for the table.

## What the merchant can do here

### Modal-level behaviour

- **A click outside does NOT close it**; the merchant clicks **Cancel** or **Done**.
- Header buttons (right-aligned, inline in header — no footer separator):
  - **Cancel** (secondary, disabled while saving).
  - **Generate Token** (create) / **Save** (edit) — primary; loading spinner while `isCreating || isUpdating`. HIDDEN once a token has just been generated in the same session (replaced with **Done**).
  - **Done** — only shown after a successful create; closes the modal.

### Body sections (`SettingsForm` with named slots)

The body has four cards:

#### Section 1 — Token Details (`SettingsCard "Token Details"`)

- **Token Name** (`CcInput`) — required; placeholder *"e.g., CI Pipeline, Development"*; up to 100 characters, any characters allowed, spaces at the ends trimmed. Names need not be unique: two tokens may share one. Disabled after a token has been generated in the same modal session.
- **Description** (`CcTextarea`) — optional; placeholder *"Optional description for this token..."*; max 500 chars. Disabled after generation.

#### Section 2 — Permissions (`SettingsCard "Permissions"`)

Renders the **`CliTokensScopeSelector`** wizard — see [[settings-pat-tokens-scopes]] for the full sub-flow (Read Only / Full Access / Custom Permissions).

#### Section 3 — Advanced Settings (`SettingsCard "Advanced Settings"`, **collapsible**)

- **Token Validity** — `CcTimePeriod` date picker + "No expiration" toggle. See [[settings-pat-tokens-restrictions]].
- `<hr/>` separator.
- **IP Restrictions** — `CliTokensIpRestrictions` component. See [[settings-pat-tokens-restrictions]].

#### Section 4 — Token Information (Edit mode only)

Hidden in Create mode (until a token has been generated this session — see success state below). In Edit mode: shows the **masked token** in a grey code box (e.g., `cc_pat_a1b2c3d4*************************************************`). Helper text below: *"Token value is hidden for security.

### Token-creation success state (one-shot reveal panel)

Immediately after a successful create, the modal body inserts a **green success card** at the top (above the form slots):

- `far fa-check-circle` green icon.
- Bold heading: *"Token Created Successfully!"*
- Sub-text: *"Copy your token now. You will not be able to see it again."*
- A white code-box containing the full `cc_pat_<64-hex>` value, with a **Copy** button on the right.

**Copy** shows the toast *"Token copied to clipboard"*, then changes its own label to **Copied!** for 2 seconds before reverting. If the clipboard write fails (browser permission denied) it toasts *"Failed to copy token"*.

Once the success card is shown:

- All form fields become **disabled** (the modal body is locked).
- The **Generate Token** button is replaced by **Done**, which simply closes the modal.
- Closing the modal discards the value for good; the table shows the new token masked.

## Settings & fields

| Field | Required (create) | Required (edit) | Notes |
|-------|-------------------|-----------------|-------|
| Token Name | yes | optional (partial PUT) | 1–100 chars |
| Description | optional | optional | ≤ 500 chars, nullable |
| Scopes | yes (≥ 1) | optional (partial PUT) | See [[settings-pat-tokens-scopes]] |
| Allowed IPs | optional | optional | ≤ 20 entries; IPv4/IPv6/CIDR — see [[settings-pat-tokens-restrictions]] |
| Token Validity | optional (defaults to "No expiration") | optional | Date must be `after:now` if set |
| Active toggle | n/a (always on for new) | yes | Mirrors row toggle in [[settings-pat-tokens-list-view]] |

Create and edit endpoints and payloads: [[settings-pat-tokens-endpoints]].

## Business rules

- **Backdrop click does not close the modal.** Specifically to prevent accidental dismiss of the one-shot success card before the merchant has copied the token value.
- **One-shot reveal is final.** Once the modal closes after a Create, the full value is unrecoverable. The platform stores only the SHA-256 hash — no decrypt path exists.
- **Edit cannot mint a new value.** To rotate a token while keeping the same name / scopes / IPs / expiration, the merchant must DELETE the existing token and CREATE a fresh one. There is deliberately no "regenerate" button — rotating requires the merchant to acknowledge the destructive step.
- **Owner-only at save time.** Even if the UI lets a moderator open the Create modal (legacy code paths), the save call returns HTTP 403 *"Only store owners can create CLI tokens"* — enforced at four layers. See [[settings-pat-tokens-permissions]].
- **Cap-enforced disable.** The Create button on the parent screen is disabled when `meta.can_create=false` (i.e., 100 tokens already exist) — the modal is never opened in that state.
- **No live-fire token test.** The modal does not include a "test this token now" path — the merchant verifies by invoking the CLI or GraphQL endpoint themselves.

### When Generate Token fails: *"The given data was invalid."*

Every rejected create shows this toast, in English. Where the cause belongs to a field, its own message also appears under that field; some causes give the toast alone.

| Cause | Shown under a field |
|---|---|
| Name empty, or over 100 characters | Token Name: *"Token name is required"* / *"Token name must be 100 characters or less"* |
| Description over 500 characters | Description |
| **Read** picked for **Inventory** or **Discounts** under Custom Permissions | none: toast only. These two have no read-only scope ([[settings-pat-tokens-scopes]]); pick **Read & Write** or **None** |
| An IP that is not an address or CIDR range | *"Invalid IP address or CIDR range"* under that IP, as it is typed |
| More than 20 IPs | IP Restrictions: *"Maximum 20 IP addresses allowed"* |
| End date not in the future | Token Validity: *"Expiration date must be in the future"* |
| 100 tokens already exist (a page not refreshed still offers **Create Token**) | none: toast only. Delete unused tokens; inactive and expired ones count |

A toast with no field message points at the scopes or the cap.

## Related

- [[settings-pat-tokens]] — hub.
- [[settings-pat-tokens-list-view]] — table the create button lives on.
- [[settings-pat-tokens-scopes]] — Permissions section's `CliTokensScopeSelector` sub-flow.
- [[settings-pat-tokens-restrictions]] — Advanced Settings section (validity + IP allowlist).
- [[settings-pat-tokens-endpoints]] — create / update validation rules and payloads.

## Open questions

_None._
