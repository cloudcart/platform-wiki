---
type: feature
nav_path: "Marketing → Channels → Email notifications → Template editor"
route_name: marketing-mails-list
route_path: /admin/marketing-new/omnichannel/mails/list
aliases: ["Customer mail template editor", "CampaignEmailTemplateScratchModal", "Unlayer designer for customer mails", "Send example email", "Test email", "Тестов имейл", "Редактор на имейл шаблон"]
tags: [marketing, omnichannel, email, notifications, editor, unlayer]
plan_gates: ["change_email_notifications", "test_mail"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-omnichannel-mails-list]]. See the hub for related aspects (mail labels, toggles & gating, variables, abandoned-cart, customisation limits).

# Email notifications — template editor modal

## Purpose

The template editor modal is the **shared editor** between this page and the campaigns flow. It's where the merchant edits a customer mail's **Name**, **Subject**, **HTML body**, and (implicitly) the `template_json` shape, using the Unlayer visual designer. The same modal handles three modes: customer-mail edit (this page), campaign-step edit ([[marketing-campaigns-edit]]), and saved scratch-template edit ([[marketing-campaigns]] saved-templates list).

## Where to find it

Open from the **Email notifications** list at `/admin/marketing-new/omnichannel/mails/list` by clicking any row's **Name** cell.

The modal title is **"Email template"** (BG **"Имейл шаблон"**), or **"Edit template"** when editing a saved scratch template.

## What the merchant can do here

### Three modes (one modal, three callers)

| Mode | Prop signature | Save button | Persists to |
|---|---|---|---|
| **Customer mail edit** (this page) | `customerMailId` set, `campaignId = null` | **Save** | `PUT /admin/api/core/marketing/customer-mails/{id}` |
| **Campaign step edit** | `campaignId` set, `customerMailId = null` | **Save** | Campaign step |
| **Saved scratch template** | Neither set (`isEditSaved` mode) | **Save template** | Saved-template store |

### Modal layout (size `xll`)

- **Title** — *"Email template"* (or *"Edit template"* for saved templates).
- **Send to** field — recipient address for test sends. Help text: *"Email address to send the test message to"*. Defaults to `site_email` from [[settings-general]].
- **Name** field — template display name shown in the list (not visible to the customer). Help text: *"This is the name of the notification"*.
- **Subject** field — email subject line. Variables restricted to `allowed_subject_vars` for the label — see [[omnichannel-mails-variables]]. Help text: *"This is the subject that the recipient will see"*.
- **Unlayer designer** — visual builder embedded as a `cc-unlayer-designer` div, min height 700px. Persists both `template_json` (re-editable shape) and `message_html` (rendered HTML). A `CcLoader` shows while it boots.
- **Variables legend** — 2-column grid of `{variable, description}` pairs. Each variable is a clickable `fa-copy` button — clicking copies the code (e.g., `{$order_id}`) to clipboard. List source: `GET /admin/api/core/marketing/customer-mails/{id}/variables`.
- **Footer actions** (left to right): **Cancel** · **Save template** (saved-template mode only) · **Save** (customer-mail / campaign mode) · **Send example email** (always present).

### Send example email

Independent of save. Dispatches a one-off send to the typed **Send to** address using the **current (unsaved)** designer state — useful for previewing edits before committing them. Behaviour:

- Substitutes placeholder example values for variables (e.g., `{$order_id}` → a real recent order; `{$customer_first_name}` → the admin's first name) (verify).
- Subject prefixed `[TEST]` to make filtering test mails in the merchant's inbox easy.
- Gated by the **`test_mail`** plan feature — when not granted the button is hidden (the controller exposes `allow_test_mail = false`).

## Settings & fields

### What gets persisted on Save (customer-mail mode)

`PUT /admin/api/core/marketing/customer-mails/{id}` with:

| Field | Source | Notes |
|---|---|---|
| `name` | Name input | Per-locale via the platform code |
| `subject` | Subject input | Per-locale; variables filtered against `allowed_subject_vars` |
| `message_html` | Unlayer rendered HTML | Sent to the recipient |
| `template_json` | Unlayer designer state | Re-editable shape |

Side-effects on save:

- Bumps the parent the platform code timestamp.
- Closes the modal and refreshes the list (so the **Last edited** column updates).
- Per-field errors surface inline via `errorStore.getError(field)`.

### Per-locale editing

Each `Mail` has one or more `MailLanguage` rows — one per language the store supports. The editor opens the row matching `site('language')` (the admin's CP language). Editing only changes the currently-selected language version; switching admin language and re-opening edits a different `MailLanguage` row. See [[omnichannel-mails-customisation-limits]].

## Business rules

### The modal is shared — caller props decide behaviour

The Vue component name is the same in both surfaces. The difference is whether `customerMailId` (this page) or `campaignId` ([[marketing-campaigns]] / [[marketing-campaigns-edit]]) is set. The **Save** action and **Variables legend** endpoint both branch on which prop is present. Saved-template mode is a third branch when neither is set.

### Save is per-locale, not bulk

A single Save persists ONE language version. To translate a template into all store languages, the merchant must switch admin language, re-open, edit, save — per language. There is no "translate all" or "copy from default locale" in the modal (verify).

### Send example does NOT require saving first

Send example uses the in-memory designer state, NOT the persisted row. This is the merchant's primary preview tool — see [[omnichannel-mails-customisation-limits]] for the full list of customisation surfaces.

### Editor save is gated by the `change_email_notifications` plan feature

Lower plans see the row in the list but cannot open the editor (the route `marketing/omnichannel/mails/edit/%` is plan-gated). The hub's plan-gates section covers the full upsell logic.

### Variable-insert dropdown comes from the backend, not hardcoded in Vue

The variable list is fetched at modal-open via `GET /admin/api/core/marketing/customer-mails/{id}/variables` — the Vue component is label-agnostic. Adding a new variable to a label is a backend-only change (`Config::$customer_mail_type_vars[label]['allowed_vars']`).

## Related

- [[marketing-omnichannel-mails-list]] — hub.
- [[omnichannel-mails-variables]] — variable allow-list semantics inserted via the legend.
- [[omnichannel-mails-labels]] — the trigger event that owns each editable row.
- [[marketing-campaigns-edit]] — campaign-step mode for the same modal.
- [[marketing-campaigns]] — saved-template mode for the same modal.
- [[message-template-email-designer]] — Unlayer designer details from the campaigns side.
- [[message-template-save-flow]] — save flow on the campaigns side (sister surface).
- [[email-template]] — the entity persisted by the editor.
- [[plan-features]] — the `change_email_notifications` and `test_mail` upsell screens.

## Open questions

- 📡 **Placeholder example values for Send example.** The exact substitution rules per variable (latest real order? made-up?) need verification per label.
- 📡 **Per-locale Save batch.** Whether there is any UI affordance to copy a template across locales (verify).
