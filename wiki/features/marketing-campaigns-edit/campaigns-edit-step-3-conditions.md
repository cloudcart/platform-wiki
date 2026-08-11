---
type: feature
nav_path: "Marketing → Campaigns → Edit → Step 3 (Conditions)"
route_name: campaigns-edit
route_path: /admin/marketing-new/campaigns/edit/:type(regular|automated)/:id
aliases: ["Campaign condition block", "IF / ELSE branch", "Link clicked", "Email opened", "Overdue action", "Branch step"]
tags: [marketing, campaigns, edit, condition, automated, step-3]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[marketing-campaigns-edit]]. See the hub for the other aspects (main settings, trigger, actions, exit, message modals, launch flow, validation rules).

# Edit campaign — Step 3 condition blocks

## Purpose

In **Automated** campaigns the merchant can insert a **condition block** between action steps. The condition watches one of the previous step's deliverable outcomes (link clicked, email opened) and branches the funnel into an **IF** path (condition met) and an **ELSE** path (deadline expired without the outcome). Each branch can choose its own delay, action, and tag side-effects.

This page covers the condition block itself — the IF/ELSE field tables, the validators, the save/delete affordances. The condition block is a sibling of the action step covered on [[campaigns-edit-step-3-actions]]; both live inside Step 3 of the editor.

Regular campaigns do **not** support condition blocks — the **Condition** option in the **Next action** dropdown is hidden for Regular.

## Where to find it

Inside Step 3 ("Campaign actions") on the **Edit campaign** screen ([[marketing-campaigns-edit]]). The merchant adds a condition via the **Next action** dropdown's `condition` option — available only when the last block in the funnel is an action step (not another condition).

## What the merchant can do here

- **Add a condition** after an action step via the **Next action** dropdown.
- **Pick the condition type** (IF branch trigger): *Link was clicked* or *Email was opened*.
- **Set the IF-branch deadline** — how long to wait for the condition to fire.
- **Set the IF-branch overdue action** — what to do when the condition fires (continue, exit, set tags, exit + set tags).
- **Set the ELSE-branch deadline and action** — what to do when the deadline elapses without the condition firing.
- **Save the condition** (button **Save condition**) — runs validators and collapses to saved state.
- **Delete the condition** via the trash icon — removes the condition data from the parent action (but keeps the parent step itself).

## Settings & fields

Condition block (`MarketingCampaignConditionStep`) is rendered as a card with a blue `#4CB7D9` badge labelled *"Condition"*. Layout is a 2-column grid (IF branch on the left, OR/ELSE on the right).

### IF branch (left column)

| Field | v-model | Options |
|-------|---------|---------|
| **If the following condition is completed** | `internalCondition.continue_condition` | `link_clicked` (*"Link was clicked"*), `email_opened` (*"Email was opened"*) |
| **Condition deadline** (Execute action select) | `deadline_type / _interval / _interval_type` | Immediately or interval (`hours / days / weeks / months`) |
| **Execute** delay (IF) | `deadline_type_if / _interval_if / _interval_type_if` | Immediately or interval |
| **Action (IF)** | `overdue_action_if` | `continue_with_next_step` (*"Continue with next step"*), `remove_from_campaign` (*"Remove from campaign"*), `set_tags` (*"Set tags"*), `remove_from_campaign_and_set_tags` (*"Remove from campaign and set tags"*) |
| **Tags (IF)** | `tags_for_overdue_if` | Visible only when action is `set_tags` or `remove_from_campaign_and_set_tags`. Autocomplete-driven from `/admin/autocomplete/customer-tags?key=tag` |

### ELSE branch (right column)

Same fields as IF, suffixed `_else`. The header text reads *"OR"* + *"Link not clicked"* (or *"Email was not opened"* depending on the chosen condition type).

| Field | v-model | Options |
|-------|---------|---------|
| **Execute** delay (ELSE) | `deadline_type_else / _interval_else / _interval_type_else` | Immediately or interval |
| **Action (ELSE)** | `overdue_action_else` | Same 4 options as IF |
| **Tags (ELSE)** | `tags_for_overdue_else` | Visible only when action requires tags |

### Header copy

- IF branch header: *"If the following condition is completed"* + the chosen condition label.
- ELSE branch header: *"And if the condition is not completed"* + the negated condition label (*"Link not clicked"* or *"Email was not opened"*).

### Save condition validators

Clicking **Save condition** runs:

- *"Please select a condition."* if `continue_condition` is empty.
- *"Please select an action for the 'If' branch."*
- *"Please select tags for the 'If' branch."* (if the IF action requires tags)
- *"Please select an action for the 'Else' branch."*
- *"Please select tags for the 'Else' branch."* (if the ELSE action requires tags)

On pass, the condition card collapses to saved state.

### Delete condition

Trash icon in the corner — confirms *"Remove condition?"* — removes the condition data from the parent action (but keeps the parent step itself). The condition block is conceptually a child of the preceding action step's `condition` field, not a peer of it.

## Business rules

- **Conditions are Automated-only.** The **Next action** dropdown's `condition` option is hidden for Regular campaigns. (Regular campaigns are capped at 1 action step total — see [[campaigns-edit-validation-rules]].)
- **A condition can only follow an action step, not another condition.** The **Next action** dropdown only shows the `condition` option when the last block is an action step.
- **The condition watches the preceding step's outcome.** `link_clicked` and `email_opened` only make sense after a deliverable step (Email / SMS / Viber / Web Push); the editor doesn't enforce a type-check but the runtime won't fire the condition for non-deliverable preceding actions.
- **All-saved rule applies to conditions too.** The pre-flight check on Start campaign requires that every condition is saved (no unsaved drafts) — see [[campaigns-edit-validation-rules]]. The error toast reads *"You must save all steps and conditions first!"*.
- **Deleting a condition keeps the parent step.** The trash on the condition removes only the condition data — the action step it was attached to remains. To remove the action step itself, use its own trash icon (see [[campaigns-edit-step-3-actions]]).
- **Editing affordance hides the "Next action" skeleton.** While any step or condition is in editing state, the **Next action** dropdown disappears — the merchant must save the current block first.

## Related

- [[marketing-campaigns-edit]] — hub.

## Open questions

No outstanding questions.
