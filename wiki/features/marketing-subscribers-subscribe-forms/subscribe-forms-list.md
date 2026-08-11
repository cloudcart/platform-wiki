---
type: feature
nav_path: "Marketing → Subscribers → Subscribe Forms → List view"
route_name: subscribe-forms.list
route_path: /admin/marketing-new/subscribers/subscribe-forms
aliases: ["Subscribe forms list", "Subscribe forms admin list", "Списък с форми за абонамент"]
tags: [marketing, subscribers, forms, popup, storefront, admin]
plan_gates: ["subscriber_forms"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-subscribers-subscribe-forms]]. See the hub for the other aspects (builder, templates, layout, triggers, fields, submission flow, GDPR consent, known issues).

# Subscribe forms — list view

## Purpose

The admin index for all subscribe forms on the store. From this single page the merchant sees every form's conversion at-a-glance (views vs successful submissions), toggles forms on/off, opens the visual builder, copies the embed snippet for inline forms, or bulk-deletes obsolete entries. It is the operational dashboard for the entire subscribe-forms feature.

## Where to find it

Sidebar → **Marketing** → **Subscribers** → **Subscribe Forms**. Route: `/admin/marketing-new/subscribers/subscribe-forms` (route name `subscribe-forms.list`). Plan-gated by the `subscriber_forms` feature key.

## What the merchant can do here

- See a list of all subscribe forms with: name, Successfully submitted count, Views count, embed-code button, Active toggle.
- Click **Add form** (button text: *"Add form"*) — opens the visual builder (see [[subscribe-forms-builder]]).
- Edit an existing form by clicking its row name — opens the same builder.
- Toggle a form's **Active** switch inline. Inactive forms aren't served to the storefront.
- Click the **Embed** icon to view the JavaScript snippet to paste into a page (only enabled for `embedded = true` forms — see [[subscribe-forms-builder]]). The snippet loads the form from `subscribers/forms/embed/<id>` and renders it inline.
- Bulk-delete forms (route `admin.segments.subscriber_form.bulkDelete`). Deletion is "soft" — the row is hidden but the record is retained; removing a form frees a plan-quota slot.
- See a draft state — when a form has unfinished edits, it shows a "save" icon instead of the Active switch (label: *"Draft"*).
- See the per-plan remaining-form count next to the Add button (call to `admin.common.remaining/subscriber_form`).

## Settings & fields

### Form list columns

| Column | What it shows |
|--------|---------------|
| Name | Merchant-set form title (clickable — opens builder). |
| Successfully submitted | Total submissions count (atomic increment on each subscribe — see [[subscribe-forms-submission-flow]]). |
| Views | Total times the form was opened/rendered on the storefront. Incremented when the storefront calls `GET /subscribers/forms/<id>` (route `subscribers.subscriptions.form`). |
| Embed | Inline code-block button — opens a modal with the JavaScript snippet to paste. Disabled for popup-type forms. |
| Active | On/Off toggle (or "Draft" icon if the form has never been published). |

Conversion rate = `submitted / views`. The merchant uses this to tune popup timing, copy, and offered incentives — but the platform does not surface a column for it (compute manually).

### Embed code modal

Opens when the merchant clicks the Embed icon for an `embedded = true` form:

- **Title**: *"Embed code"*.
- **Header banner** (green, info-icon): *"Paste this code on the site where you want it to be seen."*
- **Code preview** — read-only code editor (HTML syntax highlighting, with line numbers, line wrapping, code folding, active-line highlight, and bracket matching). Fixed height **800 px**.
- **Copy code** button (ghost style, `fa-clone` icon, floating top-right) — copies the entire snippet to the clipboard.
- **Close** button (no save).

The generated snippet:

1. Defines a uniquely-named callback keyed to the form's 24-character id.
2. Creates a `<script>` tag pointing to the form's embed URL (`/subscribers/forms/embed/<id>`).
3. When the response loads, the callback pulls in the form's rendering module from the CDN plus a Google Fonts stylesheet, then renders the form at the script tag's position on the page.

## Business rules

### Plan-gating

Subscribe forms are gated by the plan's `subscriber_forms` feature key. The Add form button shows the remaining-quota counter (`/admin/common/remaining/subscriber_form` returns `{remaining: N}` — the plan's `subscriber_forms` allowance minus the number of forms already in use). Past the cap, the merchant must upgrade or delete an existing form to add another. The remaining counter excludes soft-deleted forms.

### Soft-deletion

Deletion is "soft" — admin "delete" sets `deleted_at` and the form stops being served (it's excluded from both the storefront and the admin listing). The form record plus its `submitted` / `views` counters are retained indefinitely. A true purge is not exposed in the UI — it would require a manual operation by the team that manages the database.

### Form identifiers

Each form is identified by a 24-character id, which is why the embed URLs and the snippet's callback name embed that exact 24-character string.

### Embed button only for inline forms

The Embed icon is disabled for popup/slide-in/bar forms (`embedded = false`) — those don't need a snippet; the storefront module fetches them in bulk at startup. Only `embedded = true` forms (inline page modules — see [[subscribe-forms-builder]]) need the snippet.

## Related

- [[marketing-subscribers-subscribe-forms]] — hub.
- [[marketing-subscribers]] — parent — where captured subscribers land.
- [[marketing-subscribers-custom-fields]] — custom-field definitions surfaced in the builder.
- [[subscriber-form]] — entity page.

## Open questions

None.
