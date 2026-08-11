---
type: entity
aliases: ["Staff Member", "Moderator", "Administrator", "Admin", "Owner", "Staff", "Персонал", "Модератор", "Администратор", "Собственик"]
tags: [settings, access, staff, permissions, admin, entity]
created: 2026-05-21
updated: 2026-06-10
source_count: 0
---
# Staff Member

## Identity

A **Staff Member** is a human admin account that can log into the store's admin panel — the merchant's team in CloudCart. Every store has **exactly one Owner** (the account that registered the store, with full unconditional access to everything) plus **any number of Moderators** (additional accounts each granted a hand-picked subset of admin-panel permissions). The Owner is set at store creation and cannot be deleted, demoted, or transferred without CloudCart support intervention; Moderators are added, edited, and removed by the Owner (or by another Moderator holding the right permissions) on [[settings-staff]]. Each Staff Member has a username, an email used for login and lifecycle notifications, an optional avatar and contact details, an optional authenticator-app 2FA secret, and — for Moderators — a flat list of permission section IDs that gates which sidebar entries, screens, and API endpoints they can reach.

A Staff Member is distinct from a [[customer]] (a storefront buyer with a customer profile, never an admin account), a [[subscriber]] (a marketing-list audience member, never an admin account), an [[api-key]] (a long-lived programmatic credential with its own scope catalog, no username / no 2FA / no UI surface), and a [[pat-token]] (a short-to-mid-lived developer token, also non-human). See [[merchant-roles]] for the full role-vs-credential map.

This page is a slim hub. The detailed mechanics live in the sub-pages listed below — drill into the one that matches the question.

## Sub-pages (in this cluster)

- [[staff-member-roles-types]] — Owner vs Moderator types; the unique-immutable Owner; support-led ownership transfer; Owner-only surfaces.
- [[staff-member-permissions]] — the permission tree, the subset-delegation rule, plan-gated nodes, the flat payload, and the API permission middleware.
- [[staff-member-lifecycle]] — create / edit / delete flow; the three sequential checks for adding a Moderator; delete visibility rules; plan cap + downgrade carry-over.
- [[staff-member-2fa]] — always-on email channel; opt-in authenticator app; the actor-vs-target 2FA gating matrix on edit; lost-device reset path.
- [[staff-member-sessions-notifications]] — Force sign out vs session-key rotation; the four lifecycle email notifications; no merchant-facing audit-log screen.
- [[staff-member-profile-fields]] — editable profile fields (username, email, password, names, avatar, contacts) and the read-only connected-social-accounts list.

## Aliases

- "Staff Member" — the canonical merchant-facing wiki term.
- "Moderator" — the platform's internal label for non-Owner staff (`type = moderator`); appears in CloudCart's UI on the Staff list and the Add modal.
- "Administrator" / "Admin" — used informally for any admin account (Owner OR Moderator); also the wording on the `administrators` plan-feature cap and on most lifecycle email subjects.
- "Owner" — the single root account per store (`type = owner`); shown as a distinct row on [[settings-staff]] that cannot be deleted.
- "Staff" — the umbrella term used in the Sidebar label "Settings → Staff" and in many sentences in this wiki.
- Bulgarian: "Персонал" (the Sidebar label), "Модератор" (Moderator), "Администратор" (Administrator), "Собственик" (Owner).

## Key Attributes

| Attribute | What the merchant controls | Where documented |
|-----------|----------------------------|------------------|
| **Type** | n/a (set at creation, immutable) | Either `owner` (exactly one per store) or `moderator`. See [[staff-member-roles-types]]. |
| **Username / Email / Names** | Editable from [[settings-staff]] Edit modal | Required. Email is the login identifier + lifecycle-email recipient. See [[staff-member-profile-fields]]. |
| **Password** | Set on create; changed via Edit modal | A non-Owner cannot change the Owner's password. See [[staff-member-profile-fields]]. |
| **Avatar / Contacts** | Editable from Edit modal | All optional. See [[staff-member-profile-fields]]. |
| **Permissions** (Moderators only) | Edited via checkbox tree | Flat array of permission section IDs. The Owner implicitly holds every permission. See [[staff-member-permissions]]. |
| **2FA email channel** | Always on for every staff member | Cannot be turned off. See [[staff-member-2fa]]. |
| **2FA authenticator secret** (`cc2fa_secret`) | Opt-in per account via Edit modal | Optional TOTP via Google Authenticator / Authy / etc. See [[staff-member-2fa]] + [[account-cc2fa]]. |
| **Connected social accounts** | Connect / disconnect from public sign-in (NOT [[settings-staff]]) | Read-only on the Owner's Edit modal. See [[staff-member-profile-fields]]. |
| **Active session** | n/a (computed) | Force-signed-out by the Owner or by session-key rotation. See [[staff-member-sessions-notifications]]. |
| **`createStaffAllow` flag** | n/a (derived from permissions) | Controls whether this staff member sees "Add moderator". See [[staff-member-permissions]]. |

## Where it appears

- [[settings-staff]] — the master Staff list + Add / Edit modal. Where Moderators are created, deleted, password-changed, and have their permissions edited. Where the Owner-only Force sign out lives.
- [[account]] — the logged-in staff member's own personal account hub.
- [[account-cc2fa]] — the per-account 2FA configuration screen (TOTP secret setup).
- [[account-cc2fa-email]] — email-channel 2FA settings.
- [[account-cc2fa-codes]] — recovery codes for 2FA fallback.
- [[settings-admin-notifications]] — toggles for the four staff-lifecycle notifications (`new_admin_account`, `admin_account_changes`, `admin_account_password_change`, `admin_account_password_reset`).
- [[settings-general]] — `sessionKeyGuard` rotation (alternative to Force sign out) and the `site_email` that receives admin-creation notifications.
- [[plans]] / [[plan-features]] — Owner-only Profile dropdown items; the `administrators` plan-feature cap is enforced when adding Moderators.
- [[orders-details]] — the `moderator_id` lock on an order points at the Staff Member currently editing it.
- [[blog-article]] — surfaces the author's username on the storefront (visible publicly when the staff member writes a blog post).

## Related

- [[settings-staff]] — the management screen for Staff Members (List + Add / Edit modal + Force sign out).
- [[merchant-roles]] — concept page on Owner vs Moderator vs API Keys vs PATs, the permission model, and the plan-gated cap.
- [[account]] — the logged-in staff member's own profile / personal account hub.
- [[account-cc2fa]] — per-account 2FA configuration (TOTP secret setup).
- [[account-cc2fa-email]] — email-channel 2FA settings.
- [[account-cc2fa-codes]] — recovery codes for 2FA fallback.
- [[api-key]] — programmatic credential alternative; NOT a Staff Member.
- [[pat-token]] — short-to-mid-lived developer token; NOT a Staff Member.
- [[plan]] — the `administrators` plan-feature caps how many Staff Members the store can have.
- [[plan-gates]] — concept page on how plan limits enforce themselves across the admin panel.
- [[settings-admin-notifications]] — the four staff-lifecycle notifications and their per-type toggles.
- [[settings-general]] — `sessionKeyGuard` rotation alternative to Force sign out, plus the `site_email` that receives admin-creation notifications.
- [[customer]] — storefront buyer, NOT an admin account.
- [[subscriber]] — marketing audience, NOT an admin account.
- [[subscriber-vs-customer]] — concept page on the storefront-user duality (and how both differ from Staff).

## Open Questions

No outstanding questions — all items resolved or distributed to sub-pages.
