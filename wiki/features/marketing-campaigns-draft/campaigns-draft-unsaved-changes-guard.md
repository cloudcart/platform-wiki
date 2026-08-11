---
type: feature
nav_path: "Marketing → Campaigns → Draft → Unsaved-changes guard"
route_name: campaigns-draft
route_path: /admin/marketing-new/campaigns/draft
aliases: ["CampaignDraftGuard modal", "Leave draft campaign modal", "Draft auto-save", "Save draft button", "beforeunload dialog", "Draft snapshot diff"]
tags: [marketing, campaigns, draft, unsaved-changes]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-draft]]. See the hub for the other aspects (Draft tab, Inactive tab, entry paths, pre-flight checks, lifecycle actions).

# Draft campaigns — unsaved-changes guard and Save draft flow

## Purpose

The Draft editor has **no auto-save** — no timer, no blur-based save, no recovery feature. Every change in the editor stays in the merchant's browser memory until they explicitly click **Save draft**. To prevent silent data loss, the platform layers three protections:

1. The **Save draft** button in the editor header (persists state via a draft payload, then redirects to the Draft tab with a toast).
2. The in-app **`CampaignDraftGuard`** modal that intercepts Vue-router navigation when there are unsaved changes.
3. The native browser **`beforeunload`** dialog that fires on tab close / reload / external navigation.

If the merchant chooses **Leave anyway** or dismisses the browser dialog, all edits since the last save are **lost forever**.

## Where to find it

- **Save draft** button — header of the **Edit campaign** screen ([[marketing-campaigns-edit]]); visible only when `isDraft=true` AND not read-only.
- **`CampaignDraftGuard` modal** — fires automatically on any `router.push` away from the editor with unsaved Draft changes.
- **`beforeunload` dialog** — fires automatically on tab close / refresh / external navigation with unsaved Draft changes.

## What the merchant can do here

- **Click Save draft** → persists current form state, redirects to `campaigns-draft`, toast *"Draft saved successfully."*
- **Try to navigate away with unsaved changes** → in-app modal *"Leave draft campaign?"* surfaces with two options:
  - **Save changes** — persists, then navigates.
  - **Leave anyway** — discards edits, navigates.
- **Try to close the tab / reload / hit external URL with unsaved changes** → browser-native dialog (e.g., *"Changes you made may not be saved"* in Chrome). **Leave** discards; **Cancel** keeps the merchant on the page.

## Settings & fields

### Save draft button behaviour

Clicking **Save draft** in the editor header:

1. Calls `submitDraft` which targets the draft-save endpoint on the campaigns API with `buildPayload(true)` (`draft=true` flag).
2. On success: toast *"Draft saved successfully."* and navigates to `campaigns-draft` (the Draft list tab). The draft guard's `allowLeave` is called so the navigation skips the leave-confirm modal.
3. On error: stays on the editor page; errors surface via the global error store.

Save draft skips most pre-flight validation — only schema-level checks (title required, segment required, ≥1 action with `action_type`) run. Channel-availability / credit-balance / message-set / segment-finished checks are deferred to the **Start campaign** flow — see [[campaigns-draft-preflight-checks]].

### `CampaignDraftGuard` modal (in-app navigation)

`CcPopup` size `md`, titled *"Leave draft campaign?"*. Opens when **all three** conditions are met:

1. The campaign is in Draft state (`isDraft = true`).
2. The form's current state **differs from the snapshot** captured on first render (see snapshot logic below).
3. The merchant triggers an in-app navigation (any `router.push` away from the editor).

**Body content:**

- Amber warning box with triangle icon: *"This campaign is saved as a draft. Any unsaved changes will be lost if you leave."*
- Body text: *"Would you like to save your changes before leaving?"*

**Footer buttons:**

| Button | Style | Behaviour |
|--------|-------|-----------|
| **Leave anyway** | Ghost | Sets `acceptLeave=true`, closes modal, navigates to the pending route. Unsaved changes lost forever. |
| **Save changes** | Primary (with loading state) | Calls the draft-save endpoint with `draft=true`. On success: toast *"Draft saved successfully."*, closes modal, navigates. On error: modal stays open, error toast *"Could not save draft. Please fix the errors and try again."* — merchant must fix and retry. |

### Snapshot diff — how "unsaved changes" is detected

The guard snapshots `formData` on first render when `isDraft=true`. The `hasChanges` check is a **deep-equal** comparison of current `formData` against the snapshot, after stripping:

- All `_`-prefixed UI-only fields.
- The `template` key.
- The `mapping` key.

If equal → guard does NOT fire (navigation proceeds silently). If different → guard fires.

The snapshot is taken **only on first render** of a Draft campaign — not refreshed on save (the guard relies on the save endpoint's `allowLeave` call to bypass).

### Browser `beforeunload` dialog

Independent of the in-app modal, a native `beforeunload` listener fires when the merchant tries to:

- Close the browser tab.
- Navigate to an external URL via the address bar.
- Click a link outside the SPA.
- Hit the browser's back / refresh buttons.

The dialog text is browser-controlled and varies (typically *"Changes you made may not be saved"* in Chrome). **Leave** discards; **Cancel** keeps the merchant.

The browser dialog runs **before** the in-app guard. A merchant who confirms "Leave" in the browser dialog also bypasses the in-app modal.

## Business rules

### Guard scope: Drafts only

Both the in-app modal and the `beforeunload` listener only fire when `isDraft = true`. Edits to an Active or Inactive campaign (which are typically read-only or in a different flow) do not show the modal.

### Guard does NOT fire for sibling editor sub-routes

The guard hooks `onBeforeRouteLeave` from this specific page only. Navigating between sibling editor sub-routes (e.g., between editor tabs that share the same parent route) does NOT trigger the modal — the snapshot is preserved.

### `beforeunload` runs first

The native browser dialog fires before any Vue-side logic. A merchant who confirms "Leave" in the browser dialog skips the in-app modal entirely.

### No recovery feature

There is no "recover unsaved draft" mechanism. Once edits are lost (via **Leave anyway** or browser-dialog dismiss), they cannot be retrieved. The merchant must rebuild from the last saved state.

### Save draft does NOT run full pre-flight

Only basic schema validation runs on Save draft (title required, segment required, ≥1 action with `action_type`). The full pre-flight (channel configured + active + credits + messages set + segment finished) only runs on **Start campaign** — see [[campaigns-draft-preflight-checks]]. This means a merchant can save a Draft that would fail to activate, then debug the pre-flight failures incrementally.

### The "differs from snapshot" check ignores three field families

UI-only `_`-prefixed fields, `template`, and `mapping` keys are stripped before diffing. This prevents false positives from transient render-state mutations (e.g., the template picker re-evaluating).

### Anti-spam policy gate

Required for every campaign endpoint — see [[marketing-campaigns-policy]].

## Related

- [[marketing-campaigns-draft]] — hub.
- [[marketing-campaigns-edit]] — editor; hosts the **Save draft** button and the `CampaignDraftGuard` mount point.
- [[campaigns-edit-launch-flow]] — the **Start campaign** sibling flow + the same guard semantics from the activation side.
- [[campaigns-draft-tab]] — landing tab after a successful Save draft.
- [[campaigns-draft-preflight-checks]] — the validators that DO run on **Start campaign** (but NOT on Save draft).
- [[marketing-campaigns-policy]] — anti-spam policy required for every campaign endpoint.

## Open questions

No outstanding questions.
