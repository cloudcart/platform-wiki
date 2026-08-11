---
type: feature
nav_path: "Marketing → Campaigns → Policy → Overview"
route_name: campaigns-policy
route_path: /admin/marketing-new/campaigns/policy
aliases: ["Anti spam policy overview", "Campaign policy gate", "When the anti-spam policy appears", "Per-store policy acceptance"]
tags: [marketing, campaigns, policy, compliance, anti-spam, gdpr]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Policy — overview & merchant use

> Part of [[marketing-campaigns-policy]]. See the hub for the other aspects (page UI, enforcement, acceptance log, versioning, redirect).

## Purpose

The **Anti-Spam Policy** is a **one-time mandatory acceptance gate** that every store must pass before any outbound marketing functionality is enabled. CloudCart shows the full anti-spam terms (CAN-SPAM, GDPR opt-in obligations, prohibited content, sender-reputation rules, abuse-handling); the merchant clicks **Accept**; the platform records the acceptance and stores a per-store flag so the gate never re-appears unless CloudCart issues a newer policy version. Until that acceptance exists, **the merchant cannot open Campaigns, Channels, Saved email templates, or any other campaign-area surface.**

By accepting, the merchant agrees not to spam, not to send to non-opted-in lists, and not to abuse channel credits, and CloudCart obtains a per-merchant audit trail tied to a GDPR-style consent log.

## Where to find it

The policy page is reached **automatically** the first time the merchant tries to enter any campaign-area screen — direct route `/admin/marketing-new/campaigns/policy`. The merchant doesn't navigate here on purpose; they hit it as a redirect when clicking Marketing → Campaigns / Channels / Saved templates before having accepted. See [[campaigns-policy-enforcement]] for the redirect mechanics.

## What the merchant can do here

- **Read the policy text** in the embedded viewer.
- **Click Accept** to clear the gate and proceed to the screen they were originally heading to.

There is no Decline button — declining is implicit (close the tab / navigate away, and stay blocked). There is also **no merchant-facing "revoke" affordance** once accepted: the only way to force a fresh acceptance is for CloudCart support to clear the store's `anti_spam_policy` setting at the DB level. See [[campaigns-policy-versioning]] for the force-re-acceptance path.

## Settings & fields

There are no merchant-editable fields on this screen — it is a viewer plus a single Accept button. The acceptance is recorded into the store's campaigns app `anti_spam_policy` setting (see [[campaigns-policy-acceptance-log]]).

## Business rules

### Acceptance is per-store, not per-staff-member

The `anti_spam_policy` setting lives in the **store's** campaigns app settings, not per-user. So if the store owner accepts once, every staff member of the same store is automatically through the gate. (The acceptance-log row is still per-user — the audit trail records *who* accepted, even though the gate is per-store. See [[campaigns-policy-acceptance-log]].)

### The gate sits behind app-installed + plan gates

A merchant whose plan doesn't include campaigns never sees the policy: the plan-restriction gate blocks earlier. Three middleware layers run on every campaign endpoint, in order — app-installed → plan-restriction → anti-spam policy — and only the third is the policy gate. See [[campaigns-policy-enforcement]] for the full ordering and the admin-namespace-only scope.

### Recommended merchant use

- **Brand-new store**: when the merchant first clicks "Marketing → Campaigns" or "Channels", they're redirected here. Read carefully (especially the prohibited-content section), then Accept; they land on whatever they originally wanted to open.
- **After CloudCart issues a new policy** (rare): no automatic re-prompt is currently wired. If CloudCart wants to force re-acceptance, support clears the per-store setting; the merchant then sees the policy again on next campaign-area visit.
- **For audit / legal purposes**: the policy-acceptance-content record preserves the exact policy text the merchant accepted, alongside IP, user-agent, and timestamp — the merchant's audit trail, extractable on a GDPR data-request. See [[campaigns-policy-acceptance-log]].

## Related

- [[marketing-campaigns-policy]] — hub.
- [[marketing]] — parent Marketing hub.
- [[marketing-campaigns]] — Campaigns list — the most common target of the policy redirect.
- [[marketing-dashboard]] — Marketing Suite dashboard — accessible without the policy gate.
- [[apps-gdpr-overview]] — the broader GDPR consent framework backing the policy.
- [[plan-gates]] — plan restrictions enforced alongside the policy gate.

## Open questions

No outstanding questions.
