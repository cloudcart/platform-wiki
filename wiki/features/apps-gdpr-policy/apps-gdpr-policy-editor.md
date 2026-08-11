---
type: feature
nav_path: "Apps → GDPR → Policy → Editor"
route_name: apps.gdpr.policies
route_path: /admin/apps/gdpr/policy
aliases: ["GDPR policy editor", "Add policy", "Edit policy", "Policy revision", "Policy list", "Policy status toggle", "Delete policy", "Policy autocomplete", "Policy name uniqueness"]
tags: [apps, gdpr, compliance, policy, legal, privacy]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---
# GDPR — Policy: editor

> Part of [[apps-gdpr-policy]]. See the hub for the other aspects (form mapping, storefront rendering, seeding).

## Purpose

This aspect documents the **policy list and the create/edit modal** — the surface where the merchant actually adds, edits, activates, and deletes policy documents. It covers the data-table list, the deliberately minimal three-field modal, the validation rules, the one-click status toggle, and the hard-delete behaviour. How those policies attach to storefront forms is on [[apps-gdpr-policy-forms]]; how they render to customers is on [[apps-gdpr-policy-storefront]].

## Where to find it

Sidebar → Apps → GDPR → **Policy tab** (`/admin/apps/gdpr/policy`). The policy list is a standard data table; the per-row Edit action and the "add policy" action open `AddEditPolicyModal.vue`.

## What the merchant can do here

- See all policies in a filterable / searchable / paginated table (Title, Status, Created / Updated, Actions).
- Create a new policy (title + rich-text body + marketing toggle).
- Edit an existing policy's title, body, or marketing designation.
- Toggle a policy Active / Inactive in one click (no save step).
- Delete a policy (hard delete, no trash / restore).

## Settings & fields

### Add / edit policy modal (`AddEditPolicyModal.vue`) — only THREE merchant fields

The create/edit modal is intentionally minimal. It collects exactly three fields:

| Field | Component | Notes |
|---|---|---|
| **Policy** (`pol.name`, max 191, min 2) | InputComponent | The title customers see. Required. Tooltip explains it is the customer-facing title. |
| **Marketing** (`marketing_policy`, toggle) | ActiveSwitch | Designates this policy as THE marketing-consent policy — see [[apps-gdpr-policy-forms]]. Only ONE policy per store can hold this flag. Tooltip: *"With this option, you mark that the policy is related to your marketing goals. This policy will appear to your customers to agree to receive marketing messages from your store."* |
| **Policy text** (`pol.content`, min 2 chars, HTML) | TextEditor | Full rich-text body. Supports the `{cookies_table}` placeholder rendered at storefront time — see [[apps-gdpr-policy-storefront]]. |

The modal header reads **"Create a Policy"** on add and **"Policy Revision"** on edit. Save fires `POST /api/gdpr/policy/` (create) or `PATCH /api/gdpr/policy/{policy_id}` (update). Field-level validation errors surface inline (`responseErrors['policy.name']`, `responseErrors['policy.content']`).

**The modal does NOT include**: a status toggle (handled inline on the list, below), the form-mapping selector (configured under the form-section saves in [[apps-gdpr-settings]]), URL handle / SEO meta (auto-derived from the title — see [[apps-gdpr-policy-storefront]]), or a version / effective-date field (versioning is captured implicitly via content-hash snapshots in the acceptance log — see [[apps-gdpr-policy-storefront]]).

### Status toggle

Per-policy status flip via `GET /api/gdpr/policy/status/{policy_id}/{status?}`. Instant (no save step). The response is `{status: 'success', html: 'Active'|'Inactive', active: true|false}` — the data table updates the badge directly from the response HTML.

## Business rules

### Validation — minimum 2 characters for name and content

the platform code requires both `policy.name` (min 2, max 191 characters) and `policy.content` (min 2 characters, no upper limit). **Empty bodies or single-character titles are rejected.** The name has a 191-char hard cap (the utf8mb4 index limit). Content has no upper bound — the merchant can paste long-form HTML.

### Policy name uniqueness — enforced against the ENTIRE pages table

The validation rule `unique:pages,name` checks the policy name against the FULL pages table. The merchant CANNOT create a policy whose name matches an existing regular page (e.g., "About Us"). Names must be unique across BOTH policies AND regular pages — because a policy is a `regular`-typed Page underneath (see [[apps-gdpr-policy-storefront]]).

### Status toggle is one-click + zero validation

`GET /api/gdpr/policy/status/{policy_id}/{status?}` flips active/inactive without re-validating content. The merchant CAN deactivate a required policy (e.g., the Terms of Service attached to checkout) — the storefront will then skip that policy in the form, potentially breaking the required-acceptance UX. **No warning fires on deactivating an in-use policy.** Inactive policies don't appear in the storefront forms or the autocomplete dropdown at render time.

### Delete is a hard delete — no soft-delete

`DELETE /api/gdpr/policy/{id}` removes the row from the database. The policy disappears from the list and the storefront. The acceptance-log content snapshots are NOT cascade-deleted (they are referenced by a `RESTRICT` foreign key), so past acceptances continue to display their stored snapshot title/content. **There is no "trash" or restore for deleted policies** — recreating a deleted policy means starting from scratch.

### Policy autocomplete returns ALL non-trashed policies regardless of active

`GET /api/gdpr/policy/auto-complete` (`gdpr.api.auto_complete.policies`) returns matching policies for typeahead — used to attach policies to forms without scrolling a long list. It includes INACTIVE policies. If the merchant attaches an inactive policy to a form, the mapping saves, but the storefront's form-policy filter excludes inactive policies at render time — so the customer never sees the checkbox. This silent skip can confuse a merchant who attached the policy but doesn't see it on the storefront (see [[apps-gdpr-policy-forms]] for the render-time filtering).

## Related

- [[apps-gdpr-policy]] — hub.
- [[apps-gdpr-policy-forms]] — how the marketing toggle and form attachments behave at render time.
- [[apps-gdpr-policy-storefront]] — policy-as-Page model, name auto-handle, implicit versioning.
- [[apps-gdpr-settings]] — where form-attachment of policies is saved.
- [[apps-gdpr-acceptance]] — the immutable acceptance log that preserves deleted-policy snapshots.

## Open questions

None.
