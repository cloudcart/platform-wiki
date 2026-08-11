---
type: feature
nav_path: "Notifications"
route_name: notifications
route_path: /admin/notifications/:type?
aliases: ["Notifications inbox", "Alerts", "Известия", "Уведомления"]
tags: [base, notifications, alerts, inbox]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 6
---
# Notifications

## Purpose

The **Notifications** screen is the merchant's **in-app inbox** — a paginated, filterable list of every alert the platform has raised for the store. Each row is a notification that an internal app, integration, or automated job emitted: a low-stock warning, a failed payment retry, a successful CSV import, an installation prompt, a backup-completion message, etc.

The page has TWO interlocking jobs:

1. **Browse + mark-as-read** the historical inbox — filter by severity tab (Important / Success / Errors / Warning / Alerts / Info) and by app (the integration / module that fired it).
2. **Configure WHICH real-time toaster pop-ups** the merchant wants to see while working inside the admin — a per-severity-bucket on/off panel opened from the **Settings** button. Note this controls *toaster pop-ups only*, NOT what gets written to the inbox (the inbox keeps everything regardless).

## Where to find it

- **Sidebar → Notifications** (top-level entry).
- Topbar bell icon → **View all notifications** link drops the merchant here too.
- URL `/admin/notifications/:type?` where `:type` is one of `success`, `error`, `warning`, `alert`, `info` or empty (defaults to **Important** — the catch-all "everything unread" tab).

The legacy `important` slug is rewritten to the empty-type route on entry (it's the default tab).

## What the merchant can do here

### Browse the inbox by severity tab

Six tabs across the top, each with an unread-count badge:

| Tab label | Type slug | Source |
|---|---|---|
| **Important (n)** | (empty / default) | `tableData.meta.unread.important` |
| **Success (n)** | `success` | `tableData.meta.unread.success` |
| **Errors (n)** | `error` | `tableData.meta.unread.error` |
| **Warning (n)** | `warning` | `tableData.meta.unread.warning` |
| **Alerts (n)** | `alert` | `tableData.meta.unread.alert` |
| **Info (n)** | `info` | `tableData.meta.unread.info` |

Switching tab changes `:type` in the URL and re-instantiates the `NotificationsModel(type)` — fetches the filtered list.

### Filter by application

Above the table, a **Select with ajax** dropdown lists every installed app on the store. Selecting one filters notifications to `filters[initiator_id]=<app_id>`. Default selection is *"All notifications"*. The selection is debounced (350ms) before refreshing the table.

The app options come from `useSharedAppsInfo` — every installed app on the store + an "All notifications" entry at the top.

### Read the table rows

Three columns:

| Column | Renders |
|---|---|
| **Date** | Formatted timestamp via custom `Date` component (uses the store's `format.dateTime`). |
| **Message** | The notification text + an icon for the severity + a link to the related screen (e.g., a CSV import job → `/admin/apps/csv-import/progress/{id}`). |
| **Action** | Optional CTA button — e.g., *"View order"*, *"Configure backup"*, *"Upgrade plan"*. Some Action buttons open the **Plan upgrade side-panel** (PlanFeature) when the destination is plan-gated. |

Default sort: `id desc` (newest first). Sorting is NOT user-toggleable per column.

### Worked example — a webhook-failure alert

The most-asked case is a webhook failure (see [[settings-hooks-auto-disable]] for when it disables). The row carries the **verbatim error the receiver returned**, so the merchant can fix it without leaving the screen. There are three message forms:

- **Auto-disabled** (a permanent-failure code, or the final failed retry) — *"The Webhook (`{event} - {url}`) has been deactivate because we received an error from the receiver with message: `{receiver error}`"*.
- **Transient error, still active / will retry** — *"The Webhook (`{event} - {url}`) has an error from the receiver with message: `{receiver error}`"*.
- **DNS failure** — *"Could not resolve host for web hook with url: `{url}`"*.

`{event} - {url}` is the event name + receiver URL (e.g. *"Order updated - https://merchant.com/webhook"*); `{receiver error}` is the receiver's response text (for JSON bodies the platform extracts the `error` / `message` field). Repeated failures of the same webhook **collapse into one row** (latest error shown), and the **same message is emailed** to the store email — see [[admin-notification-entity-delivery]] and [[admin-notifications-recipient-routing]].

### Mark notifications as read

- **Single row** — click anywhere on the row that has an Action component → `POST /admin/api/core/notifications/read` with `{ids: [id]}`. The row flips to `read: 1` and the bell badge decrements via `useNotifications.getNotificationsCount`.
- **Bulk** — select rows via the table's checkbox column; the **Mark as read** action appears at the bottom; click → `POST /admin/api/core/notifications/read` with the selected IDs. Toast confirms *"Marked as read successfully"*.
- The Mark-as-read action is the ONLY bulk action — no bulk delete, no bulk archive (notifications are immutable).

### Open the Plan-feature side panel (when needed)

Some notifications are about features the merchant's plan doesn't include. Clicking them opens the **PlanFeature side panel** (the same panel used when buying feature packs) — the merchant can purchase the missing feature inline; on success, the page calls `handleAfterPay(result)` which closes the panel.

### Configure real-time toaster pop-ups (Settings modal)

Top-right of the page header is the **Settings** button (gear icon). Clicking it opens a **right-side modal** titled *"Settings"*:

#### Modal: "Configure your real-time notifications"

Body: 7 toggle switches (ActiveSwitch), one per severity bucket.

| Toggle | Default | What it controls |
|---|---|---|
| **Alert notifications** | ON | Toaster pop-ups for `alert` severity (critical platform issues — security, payment-gateway downtime). |
| **Error notifications** | ON | Toaster for `error` (failed jobs, integration errors). |
| **Important notifications** | ON | Toaster for `important` (catch-all for anything tagged high-priority). |
| **Warning notifications** | ON | Toaster for `warning` (low stock, expiring SSL, etc.). |
| **Success notifications** | ON | Toaster for `success` (import completed, backup done). |
| **Info notifications** | ON | Toaster for `info` (general updates). |
| **Orders notifications** | ON | Toaster for new orders specifically. |

Footer of the modal:

- **Cancel** button → discards changes (resets to current `allowedNotifications`) and closes.
- **Save** button → `POST /admin/api/core/settings/notifications` with the seven flags. On success, updates `allowedNotifications` (so the next pop-up obeys the new rules) and toasts *"Successfully updated"*.

The modal cannot be closed by clicking the backdrop (`no-close-on-backdrop: true`) — the merchant must explicitly Cancel or Save.

#### What does this NOT do?

The toaster toggles ONLY affect the real-time pop-up that appears in the bottom-right of every admin page when a fresh notification arrives. The Notifications inbox itself ALWAYS receives every notification regardless of the toggles — the merchant can read suppressed types later from the tabs.

## Settings & fields

The page has no per-row settings — the only inputs are the tab selector, app filter, and the Settings modal (above).

## Business rules

- **Tabs + counts.** Each severity tab sets `:type` in the URL and refetches; the per-tab unread count and the topbar bell badge come from the same per-bucket count and update after each read.
- **Mark-as-read is opportunistic.** Clicking a row's Action (or opening its Plan-feature panel) marks that one notification read; pure reading without a click does not.
- **Toaster settings are per-store, not per-admin.** Toggling a severity off in the Settings modal stops the real-time pop-ups for **every** admin, not just the one who changed it.
- **Real-time routing.** Live notifications arrive in real time; only the severities enabled in the Settings modal surface as toaster pop-ups — the rest go to the inbox silently. The inbox always keeps everything, regardless of the toggles.
- **Append-only.** Notifications aren't deleted from the inbox here; the platform prunes old read ones on a schedule (verify retention window).
- **App filter is single-select** — one installed app at a time, or "All notifications".

## Related

- [[settings-admin-notifications]] — admin-level notification *delivery* preferences (email / SMS routing rules).
- [[apps]] — the apps catalog (filter dropdown source).
- [[dashboard]] — quick stats counters; the bell icon lives in the topbar adjacent to it.
- [[backup]] — typical source of "backup completed" notifications.
- [[apps-csv-import]] — typical source of "import finished" notifications.

## Open questions

(none — verified against `Index.vue`, `ConfigureToasterNotifications.vue`, and `useLiveNotifications.js`.)
