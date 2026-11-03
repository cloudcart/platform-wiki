---
type: feature
nav_path: "Apps → GDPR → Policy → Form mapping"
route_name: apps.gdpr.policies
route_path: /admin/apps/gdpr/policy
aliases: ["Policy form mapping", "Required policy", "Optional policy", "Marketing policy", "customer.marketing", "Policy checkbox order", "Policy on checkout", "Policy on registration"]
tags: [apps, gdpr, compliance, policy, consent, marketing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
# GDPR — Policy: form mapping

> Part of [[apps-gdpr-policy]]. See the hub for the other aspects (editor, storefront rendering, seeding).

## Purpose

This aspect documents how policies **attach to storefront forms** — the many-to-many mapping between policies and the 5 GDPR form types, the required-vs-optional distinction, the order checkboxes render in, the single marketing-policy designation that drives the `customer.marketing` field, and the silent skip of inactive policies. The modal that creates the policies themselves is on [[apps-gdpr-policy-editor]].

## Where to find it

The attachment is configured under the form sections of the GDPR app (the per-form policy selector), saved via the form-section saves documented on [[apps-gdpr-settings]]. The 5 form types come from [[apps-gdpr-overview]]: `register`, `contacts`, `submit_payment`, `segment_subscription_popup`, `policies_popup`.

## What the merchant can do here

- Attach one or more policies to each of the 5 form types.
- Mark each attachment **required** (must be accepted to submit the form) or **optional** (a checkbox the customer may leave unchecked).
- Designate exactly one policy as the **marketing policy** (via the modal toggle on [[apps-gdpr-policy-editor]]).

## Settings & fields

### Policy-to-form mapping is many-to-many

Each policy can be attached to any number of the 5 form types. Per attachment the merchant marks the policy as required or optional:

| Attachment | Storefront behaviour |
|---|---|
| **Required** | The customer must tick the checkbox to submit that form (e.g., must accept Terms at checkout). |
| **Optional** | The checkbox can be left unchecked (e.g., marketing consent at registration). |

### Render order

The mapping renders **"optional first, then by id"** — optional policies appear before required ones in the form. (verify) whether this ordering can be customised by the merchant; it is currently fixed.

## Business rules

### Marketing-policy designation — at most ONE per store

The `marketing_policy` setting holds the ID of a single policy. When a customer accepts/rejects the marketing policy in the consent flow, their `customer.marketing` field flips to yes/no accordingly and a customer-marketing-changed event fires. Other integrations (subscriber lists, mail tools) react to that event.

Saving a new policy with the marketing toggle ON **overwrites** the previous designation. **Only ONE policy can be the marketing policy per store at any time** — designating a different one silently demotes the previous one (no warning).

### Inactive policies are silently skipped at render time

The autocomplete dropdown lists inactive policies too (see [[apps-gdpr-policy-editor]]), so a merchant can attach an inactive policy to a form. The mapping saves, but the storefront's form-policy filter (`getFormPolicies`) excludes inactive policies when rendering — so the customer never sees the checkbox. A required policy that has been deactivated simply disappears from the form, with no error and no acceptance prompt. When a merchant reports "the consent checkbox isn't showing on checkout," the first thing to verify is whether the attached policy is Active.

### Acceptance is recorded per policy + content snapshot

When the customer ticks "I accept," the platform records the acceptance in [[apps-gdpr-acceptance]] keyed to the policy plus a snapshot of the exact text accepted (see [[apps-gdpr-policy-storefront]] for the snapshot/versioning mechanics). Required acceptances are mandatory for form submission; optional ones are recorded as yes or no.

## Related

- [[apps-gdpr-policy]] — hub.
- [[apps-gdpr-policy-editor]] — the marketing toggle + why inactive policies still appear in autocomplete.
- [[apps-gdpr-policy-storefront]] — how accepted text is snapshotted per acceptance.
- [[apps-gdpr-overview]] — the 5 GDPR form types.
- [[apps-gdpr-settings]] — where form-attachment is saved.
- [[apps-gdpr-acceptance]] — the acceptance log these mappings write to.
- [[checkout-flow]] — `submit_payment` form where required policies gate submission.

## Open questions

- Whether the "optional first, then by id" render order is merchant-customisable. Currently fixed (verify).
