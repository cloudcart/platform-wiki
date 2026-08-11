---
type: entity
aliases: ["Staff member profile", "Staff member fields", "Username email password", "Staff avatar", "Staff contacts", "Connected social accounts", "Профил на персонал"]
tags: [settings, access, staff, admin, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---
# Staff Member — Profile Fields

## Identity

This page catalogues the editable profile fields on a [[staff-member|Staff Member]] record — the data a merchant fills in on the Add / Edit modal on [[settings-staff]] — plus the read-only connected-social-accounts list that appears on the Owner's own row.

> Part of [[staff-member]]. See the hub for the other aspects (roles & types, permissions, lifecycle, 2FA, sessions & notifications).

## Aliases

- "Profile Summary" — the avatar + name block in the Edit modal.
- "Contacts" — the optional address / phone block in the Edit modal.
- "Connected social accounts" — the read-only OAuth-identity list on the Owner's row.

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Username** | Editable from the Edit modal | Required. Visible on the storefront where the staff member's name appears publicly (e.g. blog post author — see [[blog-article]]). |
| **Email** | Editable from the Edit modal | Required. Used as the login identifier and as the recipient for per-account lifecycle emails (2FA codes, password reset). Must be a valid email format. |
| **Password** | Set on create; changed via the Edit modal's "Change password" | Hashed at rest. A non-Owner cannot change the Owner's password. A user can change their own password. |
| **First name** / **Last name** | Editable from the Edit modal | Required at creation. Used in greetings and admin notification emails. |
| **Avatar** | Uploaded via the Edit modal's Profile Summary | Optional image (250×250, max 25 MB, standard image MIME types). Shown next to the username in the Staff list and in the admin top bar when this account is signed in. |
| **Contacts** (`info.country`, `info.city`, `info.street`, `info.postal_code`, `phone`) | Editable from the Edit modal's Contacts section | All optional. Computed into the Staff list's "Address" column as `<country>, <city>, <street>, <postal_code>` with empty values skipped. |
| **Connected social accounts** | Connect / disconnect from the public sign-in flow (NOT [[settings-staff]]) | Read-only list on the Owner's Edit modal showing OAuth identities (Google, Facebook, etc.). Moderators don't see this section. |
| **Last updated** | n/a (auto-set) | Timestamp shown in the Staff list; default sort is by ID descending (newest first). |

## Where it appears

- [[settings-staff]] — the Add / Edit modal where every profile field is set.
- [[blog-article]] — surfaces the username publicly on the storefront when a staff member authors a post.
- [[account]] — the logged-in staff member's own profile hub.

## Business rules

### Password change is constrained by role

A staff member can change their own password from the Edit modal's "Change password". A **non-Owner cannot change the Owner's password** — the server returns HTTP 422. Password updates queue the `admin_account_password_change` notification (see [[staff-member-sessions-notifications]]).

### The Address column is computed from optional contact fields

The Staff list's "Address" column is assembled from `info.country`, `info.city`, `info.street`, and `info.postal_code`, joined with commas and skipping any empty value. None of these are required; a staff member with no contact data simply shows a blank Address.

### Connected social accounts are managed only in the public sign-in flow

Connecting / disconnecting social-login accounts (Google, Facebook, Apple) lives only in the public sign-in flow, NOT in [[settings-staff]]. The Edit modal shows the list (read-only) for the Owner's own row. To disconnect a social account, the Owner must visit the public account-settings page outside the admin panel or contact support. Moderators do not see this section at all.

### Username is public on the storefront

Because the username surfaces publicly anywhere the staff member's name appears (notably as the [[blog-article|blog post]] author), merchants should treat it as a customer-visible display name, not an internal handle.

## Related

- [[staff-member]] — hub.
- [[settings-staff]] — the Add / Edit modal for all profile fields.
- [[account]] — the staff member's own profile hub.
- [[blog-article]] — where the username appears publicly.
- [[staff-member-2fa]] — the 2FA fields on the same Edit modal.

## Open Questions

None.
