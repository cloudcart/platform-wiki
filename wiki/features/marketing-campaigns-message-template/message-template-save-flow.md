---
type: feature
nav_path: "Marketing → Campaigns → Edit → Set message → Save flow"
route_name: admin.api.campaigns.message-template.create
route_path: /admin/api/core/marketing/campaigns/message/create/{campaign_id}/{action_order}/{type}/{predefined?}
aliases: ["Campaign message save", "Save template to step", "Delete saved template from step", "Запис на шаблон към стъпка", "Изтриване на шаблон от стъпка"]
tags: [marketing, campaigns, message, template, save, persistence]
plan_gates: ["campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-message-template]]. See the hub for the other aspects (Email designer, channel variants, merge tags, saved + predefined, demo send, validation).

# Campaign message editor — Save & delete flow

## Purpose

This aspect documents what happens when the merchant clicks **Save** on the message editor, on any channel: which endpoint is called, how a re-save overwrites the step's existing message, and how a saved message is removed from a step.

## Where to find it

Save uses:

| Endpoint | Method | Route path | Purpose |
|----------|--------|------------|---------|
| save message | POST | `/admin/api/core/marketing/campaigns/message/create/{campaign_id}/{action_order}/{type}/{predefined?}` | Save the message template for the step |
| load existing | GET | `/admin/api/core/marketing/campaigns/messages/{campaign_id}/{action_order}/{type}` | Load any previously-saved message for the step (plural `messages` here) |
| delete template | POST | `/admin/api/core/marketing/campaigns/message/delete/{id}` | Remove a saved message template from a step (POST, not DELETE) |

URL segments:

- `{campaign_id}` — the parent campaign.
- `{action_order}` — the step's 0-based order within the campaign.
- `{type}` — channel action type (`email`, `sms_nth_message`, `sms_msghub_message`, `viber_message`, `web_push`).
- `{predefined}` — optional; the predefined campaign ID for internal CloudCart template authoring; for merchant saves it's `0`.

(Note: `message` is singular in the save / delete paths, plural `messages` in the GET load path.)

## What the merchant can do here

The merchant doesn't call this endpoint directly — clicking **Save** in the editor (Email designer, or the SMS / Viber / Web Push modal) triggers it. What follows is what each save sends and returns.

### Email save

1. The Email designer exports the rendered HTML + design.
2. It posts to `/admin/api/core/marketing/campaigns/message/create/{campaign_id}/{action_order}/email/0` with: `name`, `internal_title`, `subject`, `send_to` (the test recipient — remembered for next opens), `template_json` (the design), `message_html` (the rendered email), plus `template_id` + `template_type` when the message was loaded from a saved template (preserves the link; see [[message-template-saved-and-predefined]]).
3. On success: the step's saved message appears inline, the modal closes, and a *"Template saved successfully."* toast shows.

### SMS / Viber / Web Push save

1. The message label is copied into the step's `internal_title`.
2. The message content is stored under the step's `condition`:
   - Viber: `condition.message` (text) + `condition.imageURL`, `condition.buttonText`, `condition.buttonURL`
   - SMS: `condition.message` (text)
   - Web Push: `condition.message` with `title` / `body` / `icon` / `image`
3. If the campaign already has an ID + step order: it posts to `/admin/api/core/marketing/campaigns/message/create/{campaign_id}/{action_order}/{type}/0` to persist the step's saved message.
4. On success: the step is marked as having a chosen message, a *"Saved successfully"* toast shows, and the modal closes.
5. On failure: the step rolls back to "no message chosen".
6. When the campaign has no ID yet (unsaved campaign): nothing is posted — the message stays in the page only and the step keeps showing **Set message**.

### What the save does on the server

1. Validates the request against the channel's rules, then validates the merge-tag variables (see [[message-template-validation]] and [[message-template-merge-tags]]).
2. If a valid `template_id` + `template_type` pair is supplied and the referenced saved template still exists, it links the step's message to that saved template.
3. Saves the step's message keyed by `(campaign_id, action_order)`, then returns the "saved message" panel so the campaign editor refreshes that step inline.

## Settings & fields

### One saved message per step

Each step keeps a single saved message, keyed by the campaign and the step's 0-based order (`action_order`). Re-saving a step **replaces** its existing message in place — it does not add a second one.

The channel `type` is overwritten too: if a merchant changes a step from Email to SMS and re-saves, the previous Email content is overwritten by the SMS content.

### Predefined-campaign save path

When the URL includes a `{predefined}` ID, the message is saved into the predefined campaign's own catalog instead of the merchant's campaign — the path CloudCart staff use to curate predefined templates. A merchant never sees this URL with a `predefined` value; for merchant edits `predefined` is `0`.

Because the two paths use different storage, predefined templates don't appear among the merchant's own campaign messages. When a merchant *uses* a predefined campaign as the starting point for a new campaign, the predefined content is copied into the new campaign's steps at that point. (verify the exact copy mechanism)

### Inline refresh — no full page reload

After a successful save, the campaign editor receives the step's "saved message" panel in the response and swaps it into the step's **Set message** area inline — no full page reload.

### First-save vs subsequent-save toast

The toast is *"Successfully added"* on first save and *"Successfully edited"* on later edits.

## Business rules

### Save overwrites the step's message in place

Re-saving a step overwrites its saved message rather than adding another. The campaign editor keeps each step's order unique, so steps can't collide on the same `action_order`.

### Delete is permanent

The delete path (`/admin/api/core/marketing/campaigns/message/delete/{id}`) removes the step's saved message permanently — there is no soft-delete or undo. After delete the step reverts to the "no message set" state, and the merchant must click **Set message** again to author a new one. For predefined-campaign editing, the deleted entry is removed from the predefined catalog instead.

### Saved-template link is re-checked on every save

The save re-verifies the `template_type` + `template_id` pair on **every** save, not just the first. So if CloudCart removed a saved-template type between the merchant's first save and a later edit, the later save silently drops the link. Otherwise editing a "linked" step preserves the link as long as the saved template still exists. See [[message-template-saved-and-predefined]] for the propagation rules.

### Customer-mail save path is separate

The Email designer is also used for the "customer mail" path. That save goes to a different endpoint — see [[marketing-omnichannel-mails-list]]. The save documented here is the **campaign** path only.

### Library save vs campaign save are distinct buttons

The Email designer exposes both **Save template** (library — see [[message-template-saved-and-predefined]]) and **Save** (campaign — this aspect). Clicking the wrong one is a common confusion: library save stores the design in the saved-templates library without binding it to any campaign step; campaign save binds it to the step and optionally links it to a saved template.

### Demo dispatch is NOT a save

Demo sends (`/admin/api/core/marketing/campaigns/message/demo/{type}`) are entirely separate from save — they don't save the step's message and don't consume plan credits. See [[message-template-demo-send]].

### Modal closes on success

When a campaign save succeeds, the editor modal closes and the merchant lands back on the campaign editor with the step showing its newly-saved message.

## Related

- [[marketing-campaigns-message-template]] — hub.
- [[marketing-campaigns-edit]] — parent campaign editor; the step renders the "saved message" state from this save's response.
- [[message-template-email-designer]] — the modal that produces the Email save payload.
- [[message-template-channel-variants]] — the modal that produces the SMS / Viber / Web Push save payload.
- [[message-template-saved-and-predefined]] — saved-template link verification + propagation.
- [[message-template-validation]] — the two-pass validation that runs first.
- [[marketing-omnichannel-mails-list]] — customer-mail save path (separate endpoint).
- [[marketing-campaigns]] — the campaign step (action) entity.

## Open questions

- Does the campaign editor render the "saved message" panel returned by the save, or rebuild it from the JSON payload?
- Confirm the predefined-campaign → merchant-campaign copy mechanism (when the predefined content lands in the merchant's campaign step, if ever).
