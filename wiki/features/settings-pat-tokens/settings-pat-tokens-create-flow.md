---
type: feature
nav_path: "Settings → PAT Tokens → Create / Edit modal"
route_name: pat-tokens.settings
route_path: /admin/settings/pat-tokens
aliases: ["Create PAT Token modal", "Edit PAT Token modal", "Token Created Successfully", "PAT one-shot reveal", "Generate Token button"]
tags: [settings, security, tokens, modal, create, edit]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-pat-tokens]]. See the hub for related aspects (list view, scopes, restrictions, security, permissions, endpoints).

# PAT Tokens — create / edit modal

## Purpose

The right-side slide-out modal (`CliTokensCreateOrEdit.vue`) used to create a new PAT token or edit an existing one. The same component handles both modes; the only differences are which sections are visible, which fields are editable, and what the primary button does. It also hosts the **one-shot token reveal** — the green success card that appears immediately after a successful create.

## Where to find it

- **Create:** Settings → PAT Tokens → **Create Token** header button (only when `meta.can_create=true`), OR the empty state's **Create Your First Token** button.
- **Edit:** Settings → PAT Tokens → click any row's Name cell. See [[settings-pat-tokens-list-view]] for the table.

## What the merchant can do here

### Modal-level behaviour

- The modal uses `modal-right` class, size `xl`, with `no-close-on-backdrop=true` — **backdrop click does NOT close it**. The merchant must explicitly click **Cancel** or **Done**.
- Header buttons (right-aligned, inline in header — no footer separator):
  - **Cancel** (secondary, disabled while saving).
  - **Generate Token** (create) / **Save** (edit) — primary; loading spinner while `isCreating || isUpdating`. HIDDEN once a token has just been generated in the same session (replaced with **Done**).
  - **Done** — only shown after a successful create; closes the modal.

### Body sections (`SettingsForm` with named slots)

The body is a `SettingsForm` using `DefaultLayout` with slots `general` / `permissions` / `advanced` / `tokenInfo`. Each slot renders a `SettingsCard` panel:

#### Section 1 — Token Details (`SettingsCard "Token Details"`)

- **Token Name** (`CcInput`) — required; placeholder *"e.g., CI Pipeline, Development"*; validation min 1, max 100 chars. Disabled after a token has been generated in the same modal session.
- **Description** (`CcTextarea`) — optional; placeholder *"Optional description for this token..."*; max 500 chars. Disabled after generation.

#### Section 2 — Permissions (`SettingsCard "Permissions"`)

Renders the **`CliTokensScopeSelector`** wizard — see [[settings-pat-tokens-scopes]] for the full sub-flow (Read Only / Full Access / Custom Permissions).

#### Section 3 — Advanced Settings (`SettingsCard "Advanced Settings"`, **collapsible**)

- **Token Validity** — `CcTimePeriod` date picker + "No expiration" toggle. See [[settings-pat-tokens-restrictions]].
- `<hr/>` separator.
- **IP Restrictions** — `CliTokensIpRestrictions` component. See [[settings-pat-tokens-restrictions]].

#### Section 4 — Token Information (Edit mode only)

Hidden in Create mode (until a token has been generated this session — see success state below). In Edit mode: shows the **masked token** in a grey code box (e.g., `cc_pat_a1b2c3d4*************************************************`). Helper text below: *"Token value is hidden for security. If you need a new token, create a new one."* See [[settings-pat-tokens-security]] for the masking format.

### Token-creation success state (one-shot reveal panel)

Immediately after a successful create, the modal body inserts a **green success card** at the top (above the form slots):

- `far fa-check-circle` green icon.
- Bold heading: *"Token Created Successfully!"*
- Sub-text: *"Copy your token now. You will not be able to see it again."*
- A white code-box containing the full `cc_pat_<64-hex>` value, with a **Copy** button on the right.

**Copy button**: clicking calls `navigator.clipboard.writeText`, shows toast *"Token copied to clipboard"*, then changes its own label to **Copied!** for 2 seconds before reverting. If the clipboard write fails (browser permission denied) it toasts *"Failed to copy token"*.

Once the success card is shown:

- All form fields become **disabled** (the modal body is locked).
- The **Generate Token** button is replaced by **Done**, which simply closes the modal.
- Closing the modal (either via Done or Cancel) resets `createdToken` to null — the value is GONE; the merchant cannot reopen the same modal to see it again. The new record now shows in the table with masked prefix only.

## Settings & fields

| Field | Required (create) | Required (edit) | Notes |
|-------|-------------------|-----------------|-------|
| Token Name | yes | optional (partial PUT) | 1–100 chars |
| Description | optional | optional | ≤ 500 chars, nullable |
| Scopes | yes (≥ 1) | optional (partial PUT) | See [[settings-pat-tokens-scopes]] |
| Allowed IPs | optional | optional | ≤ 20 entries; IPv4/IPv6/CIDR — see [[settings-pat-tokens-restrictions]] |
| Token Validity | optional (defaults to "No expiration") | optional | Date must be `after:now` if set |
| Active toggle | n/a (always on for new) | yes | Mirrors row toggle in [[settings-pat-tokens-list-view]] |

The Create endpoint is `POST /admin/api/core/account/cli-tokens/` and returns the full token value in a `CliTokenCreateResponse` payload. The Edit endpoint is `PUT /admin/api/core/account/cli-tokens/{id}` (partial updates allowed). See [[settings-pat-tokens-endpoints]] for the full schema.

## Business rules

- **Backdrop click does not close the modal.** Specifically to prevent accidental dismiss of the one-shot success card before the merchant has copied the token value.
- **One-shot reveal is final.** Once the modal closes after a Create, the full value is unrecoverable. The platform stores only the SHA-256 hash — no decrypt path exists. See [[settings-pat-tokens-security]].
- **Edit cannot mint a new value.** To rotate a token while keeping the same name / scopes / IPs / expiration, the merchant must DELETE the existing token and CREATE a fresh one. There is deliberately no "regenerate" button — rotating requires the merchant to acknowledge the destructive step.
- **Owner-only at save time.** Even if the UI lets a moderator open the Create modal (legacy code paths), the save call returns HTTP 403 *"Only store owners can create CLI tokens"* — enforced at four layers. See [[settings-pat-tokens-permissions]].
- **Cap-enforced disable.** The Create button on the parent screen is disabled when `meta.can_create=false` (i.e., 10 tokens already exist) — the modal is never opened in that state.
- **Form locks on success.** Once `createdToken` is set, all inputs become read-only. This prevents the merchant from accidentally editing the new token before copying its value.
- **No live-fire token test.** The modal does not include a "test this token now" path — the merchant verifies by invoking the CLI or GraphQL endpoint themselves.

## Related

- [[settings-pat-tokens]] — hub.
- [[settings-pat-tokens-list-view]] — table the create button lives on.
- [[settings-pat-tokens-scopes]] — Permissions section's `CliTokensScopeSelector` sub-flow.
- [[settings-pat-tokens-restrictions]] — Advanced Settings section (validity + IP allowlist).
- [[settings-pat-tokens-security]] — token format, masking, why the value is unrecoverable.
- [[settings-pat-tokens-endpoints]] — create / update validation rules and payloads.

## Open questions

_None._
