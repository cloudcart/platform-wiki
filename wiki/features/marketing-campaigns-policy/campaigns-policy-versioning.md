---
type: feature
nav_path: "Marketing → Campaigns → Policy → Versioning"
route_name: campaigns-policy
route_path: /admin/marketing-new/campaigns/policy
aliases: ["Policy versioning", "Anti spam policy hash", "Policy content hash", "Force re-acceptance", "Policy locale fallback", "md5 policy hash"]
tags: [marketing, campaigns, policy, compliance, anti-spam, gdpr, versioning]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Policy — versioning & locale

> Part of [[marketing-campaigns-policy]]. See the hub for the other aspects (overview, page UI, enforcement, acceptance log, redirect).

## Purpose

This page documents **how the Anti-Spam Policy is versioned** — the content hash, why an old acceptance still grants access after a text update, the locale-fallback rule that picks which translation is shown, and how CloudCart can force a fresh acceptance.

## Where to find it

Versioning is invisible to the merchant — it determines which policy text the iframe shows (see [[campaigns-policy-page-ui]]) and whether the gate re-appears.

## What the merchant can do here

Nothing interactive. The merchant only ever reads and accepts whatever the current version resolves to.

## Settings & fields

The policy CONTENT is centrally managed by CloudCart in the `gdpr_policies` table keyed by `mapping = 'campaigns'`, with bilingual `name_bg` / `name_en` and `description_bg` / `description_en` columns. The version key is `policy.hash = md5(name + description)`, computed from the **localised** values actually shown.

## Business rules

### Policy versioning via hash

CloudCart can issue a NEW version of the policy by editing the policy's `name` / `description`. The hash (`md5(name + description)`) changes, but the merchant's existing per-store `anti_spam_policy` setting still points to the OLD acceptance log (content-hashed against the OLD version — see [[campaigns-policy-acceptance-log]]).

**However, the current production gate logic checks only whether `anti_spam_policy` is empty, not whether its content hash matches the current policy hash.** So in practice an old acceptance still grants access even after a policy-text update. To force re-acceptance, CloudCart would need to invalidate the per-store setting (e.g. via a migration that resets `anti_spam_policy` for all stores when a major policy revision ships).

### No automatic re-prompt — forcing re-acceptance

There is **no merchant-facing "revoke" UI** and no automatic re-prompt when the text changes. The only way to force a fresh acceptance is for CloudCart support (or a migration) to clear the store's `anti_spam_policy` setting at the DB level; the merchant then sees the policy again on the next campaign-area visit.

### Locale fallback is ASCII-only (verified against backend)

The localization branch uses `in_array($lang, ['bg', 'en'])` — Bulgarian admin or English admin. Any other admin locale (cs, de, ro, fr, mk, sr, it, hu, el, nl, es) falls back to `name_en` / `description_en` (the English version). The content hash (`md5(name. description)`) is still computed from the localised values, so a merchant who accepts in Bulgarian and re-visits in English would see a **different hash** — but because the gate checks only "any acceptance exists," not hash-match, this divergence does **not** force re-acceptance.

### Policy is loaded by mapping key, with a fallback stub (verified against backend)

The policy is looked up via the platform code in the central `cc_gate.gdpr_policies` table (the `gate` connection). If no row exists, the controller constructs an in-memory stub with `name_en = name_bg = "Anti spam policy"` and an empty description — preventing a 500 error if the policy seed has not been run. In practice the seeded row always exists on production.

## Related

- [[marketing-campaigns-policy]] — hub.
- [[campaigns-policy-acceptance-log]] — the content-hash record keyed by this hash.
- [[campaigns-policy-enforcement]] — the gate that checks only "accepted at all," not hash-match.
- [[campaigns-policy-page-ui]] — the iframe that shows the locale-resolved text.
- [[apps-gdpr-overview]] — the broader GDPR consent framework.

## Open questions

No outstanding questions.
