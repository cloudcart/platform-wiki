---
type: feature
nav_path: "Marketing → Campaigns → Draft → Pre-flight checks"
route_name: campaigns-draft
route_path: /admin/marketing-new/campaigns/draft
aliases: ["Draft activation pre-flight", "Start campaign validators", "Inactive to Active checks", "Channel-suspension cascade", "Campaign was not started", "Status toggle bypass"]
tags: [marketing, campaigns, draft, validation, activation]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-draft]]. See the hub for the other aspects (Draft tab, Inactive tab, entry paths, unsaved-changes guard, lifecycle actions).

# Draft / Inactive campaigns — activation pre-flight checks

## Purpose

Two transitions move a campaign into the running state: **Draft → Active** (clicking **Start campaign** in the editor) and **Inactive → Active** (flipping the row Status toggle on the Inactive tab). Both transitions run through the same activation pipeline and the same family of pre-flight validators. The validators block activation when the campaign is misconfigured or when the runtime environment (channel state, credit balance, segment filtering progress) isn't ready.

This page catalogues:

- The full check matrix that fires on activation.
- The error strings the merchant sees on failure.
- The **toggle-endpoint trust gap** — what the toggle does NOT re-validate, and why the Vue UI routes through the editor for Drafts.
- The **channel-suspension cascade** that flips Active → Inactive automatically.

## Where to find it

- **Draft → Active**: triggered from [[marketing-campaigns-edit|the editor]] via the **Start campaign** button (and its **Review and launch** confirmation modal — see [[campaigns-edit-launch-flow]]).
- **Inactive → Active**: triggered from the Status toggle column on [[campaigns-draft-inactive-tab|the Inactive tab]].

## What the merchant can do here

- **See activation block reasons** — failing pre-flight surfaces a specific error message; the campaign stays in its prior state.
- **Resume after fixing the failure** — once the blocking condition is resolved (channel installed, credits topped up, messages set, segment finished), retry activation.
- **Investigate channel-suspension auto-flips** — campaigns on the Inactive tab with banned-reason badges link to [[marketing-campaigns-banned-info]] showing why the cascade fired.

## Settings & fields

### Activation pre-flight check matrix

When the merchant clicks **Start campaign** on a Draft (or flips a row Status toggle on Inactive), the platform runs the following checks in order. The first failing check returns its error string; the campaign stays in its prior state.

| # | Check | Error message |
|---|-------|---------------|
| 1 | All steps saved (Start campaign only) | *"You must save all steps and conditions first!"* |
| 2 | All required fields filled | *"You haven't filled all the settings!"* |
| 3 | All step messages set | *"You need to set all the messages"* |
| 4 | Referenced channels configured (installed) | *"Channel ':name' is not configured"* |
| 5 | Referenced channels active (not suspended) | *"Channel ':name' is not active"* |
| 6 | Sufficient channel credits available | *"You do not have enough credits for:name"* |
| 7 | Trigger segment finished filtering | *"Subscribers are still being filtered"* |
| 8 | Generic catch-all | *"Campaign was not started"* |

A failing check keeps the campaign in its starting state (Draft stays Draft; Inactive stays Inactive). Once all checks pass and the merchant confirms the **Review and launch** modal, the campaign flips to `active=1` and the activation cascade dispatches — see [[campaigns-edit-launch-flow]] for the queue side-effects.

### Toggle-endpoint trust gap

The status-toggle endpoint (`campaigns.update_active`) runs a **subset** of the full pre-flight: channel installed, channel active, sufficient credits, not-Draft (previously started). It does **NOT** re-validate that every action template still has a message body — the toggle trusts existing data.

This is fine for normal merchants because the Vue UI routes Draft activations through the editor's full save flow (which runs the messages check). But **raw API calls bypass** the editor: a merchant who edits a Draft via API, removes messages, saves, then activates via toggle would land Active with empty messages. The Vue UI's own protection: row-level Status toggle is hidden on the Draft tab (see [[campaigns-draft-tab]]).

### Toggle endpoint refuses raw Draft activation

If the merchant attempts to flip a Draft directly via the status-toggle endpoint (bypassing the editor's **Start campaign** flow), the platform returns:

> *"Campaign was not started"*

This protects against UI-bypass: the editor's pre-flight is the only legitimate path out of Draft.

### Channel-suspension cascade (Active → Inactive)

When a channel auto-suspends or the merchant manually disables it, the cascade flips campaigns referencing that channel from `active=1` to `active=0`. Cascade triggers:

- `spam` — too many spam complaints
- `bounce` — too many hard bounces
- `open` — open-rate below threshold
- `cc_denied` — channel-specific compliance denial

(See [[marketing-channels]] for the per-channel suspension matrix.)

Scope and side-effects:

- **Only campaigns with `active=1` are flipped.** Drafts (`active=2`) and already-Inactive (`active=0`) campaigns are untouched.
- **The campaign carries a banned-reason badge** on the [[campaigns-draft-inactive-tab|Inactive tab]] — clicking it opens [[marketing-campaigns-banned-info]].
- **No auto-reactivation.** When the channel comes back, the merchant must manually flip the campaign back to Active (after also clearing the banned reason).
- **Enrolled subscribers are retained.** Mid-funnel resume on re-activation — see [[campaigns-draft-lifecycle-actions]].

## Business rules

### Start campaign pre-flight is comprehensive; Save draft is minimal

**Save draft** skips most pre-flight (only schema-level checks: title required, segment required, ≥1 action with `action_type`). The full pre-flight defers to **Start campaign**. This lets the merchant save partial progress without satisfying the harder validators yet. See [[campaigns-draft-unsaved-changes-guard]].

### Inactive → Active runs the same checks (minus check #1)

When the merchant flips the Inactive Status toggle, checks #2–#8 fire (check #1 "all steps saved" is editor-specific). Failures keep the campaign Inactive and surface the same error strings.

### Drafts using a suspended channel stay in Draft

The cascade scope is `active=1` only — a Draft referencing a suspended channel is untouched by the cascade. The merchant hits the channel pre-flight failure (check #4 or #5) only when they try to **Start campaign**.

### Pre-flight failure messages also surface on the banned-info screen

When channel-related pre-flight fails on Inactive → Active, the badge on the row links to [[marketing-campaigns-banned-info]] with a human-readable explanation of the suspension trigger.

### Trigger-segment deletion fails silently before pre-flight

If a Draft (or Inactive) campaign's trigger segment is deleted, the campaign's `segment` relation returns null and the enrol / execute jobs early-return without touching subscribers. The merchant sees the campaign in its existing state with no automatic toast. On **Start campaign**, the missing-segment failure surfaces via [[marketing-campaigns-banned-info]].

### Anti-spam policy gate fires before pre-flight

Every campaign endpoint — including activation — requires [[marketing-campaigns-policy|anti-spam policy]] acceptance. The policy gate runs first; if not accepted, the merchant is redirected to the policy screen before any pre-flight check fires.

## Related

- [[marketing-campaigns-draft]] — hub.
- [[campaigns-edit-launch-flow]] — **Start campaign** flow + the activation queue cascade after the pre-flight passes.
- [[campaigns-edit-validation-rules]] — full editor-side validator ordering.
- [[campaigns-draft-tab]] — Draft tab; Status toggle column hidden because Drafts cannot bypass pre-flight.
- [[campaigns-draft-inactive-tab]] — Inactive tab; Status toggle column drives Inactive → Active.
- [[campaigns-draft-entry-paths]] — the state-machine transitions that this pre-flight governs.
- [[marketing-campaigns-banned-info]] — explainer screen for failed channel checks / cascade banned-reasons.
- [[marketing-channels]] — channel suspension matrix (spam / bounce / open / cc_denied).
- [[marketing-campaigns-policy]] — anti-spam gate.
- [[campaign]] — Campaign entity.

## Open questions

No outstanding questions.
