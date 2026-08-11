---
type: feature
nav_path: "Marketing → Campaigns → Edit → Steps 4 & 5 (Exit)"
route_name: campaigns-edit
route_path: /admin/marketing-new/campaigns/edit/:type(regular|automated)/:id
aliases: ["Campaign exit tag", "Tag customers card", "Campaign exit purpose", "Makes an order", "Customers tags"]
tags: [marketing, campaigns, edit, exit, tagging, step-4, step-5]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[marketing-campaigns-edit]]. See the hub for the other aspects (main settings, trigger, actions, conditions, message modals, launch flow, validation rules).

# Edit campaign — Steps 4 & 5 (Exit tag + purpose)

## Purpose

Steps 4 and 5 sit at the bottom of the editor and define **what happens when a subscriber finishes the campaign successfully**. Step 4 picks the exit tag(s) — applied to subscribers who finish the funnel (or hit the exit condition in Step 5) — so the merchant can re-target / segment them later. Step 5 picks the **exit purpose** — the runtime condition that fires the early-exit (and tags the subscriber).

The two steps are documented together because they share the same exit-flow concept and are typically configured together at the end of the editor session.

## Where to find it

Boxes 4 and 5 (bottom of the **Edit campaign** screen — [[marketing-campaigns-edit]]). Both are rendered as `CampaignStepCard` components.

- **Step 4** is titled *"Tag customers"* with description *"Tag the customer who exit the campaign successfully with"*.
- **Step 5** is titled *"Campaign exit"* with description *"Exit campaign when the customer"*.

## What the merchant can do here

### Step 4 — Tag customers

- **Pick one or more exit tags** from the autocomplete dropdown.
- **Create a new tag inline** via the **+ Add new** affordance in the autocomplete — free text creates the tag on submit.

Customers who finish the campaign without being filtered out get tagged with these tags — handy for re-targeting / segmentation.

### Step 5 — Campaign exit

- **Pick the exit condition** — currently only *"Makes an order"* is exposed in the modern editor. When the chosen condition fires for an enrolled subscriber, they exit the campaign early and are tagged with the exit tag from Step 4.

## Settings & fields

### Step 4 — Tag customers card

| Field | v-model | Notes |
|-------|---------|-------|
| **Tags** | `customersTagsIds` synced with `formData.customers_tags` | `CcSelect` in `tags` mode with autocomplete from `/admin/autocomplete/customer-tags?key=tag`, `resolve-on-load: true`, error from `errorStore.getError('customers_tags')` |

Selecting tags emits the full `{id, name}` objects which are normalised into the form payload at save time.

### Step 5 — Campaign exit card

| Field | v-model | Options |
|-------|---------|---------|
| **Exit condition** | `formData.purpose` | `makes_an_order` (*"Makes an order"*) — currently the only option exposed in the modern editor |

## Business rules

- **Exit tag is applied on successful exit.** When the subscriber completes the funnel naturally OR hits the Step 5 exit condition, the tags from Step 4 are applied. Subscribers filtered out of the campaign (e.g., banned channel, unsubscribed) are **not** tagged.
- **Step 5 condition fires early-exit + tag.** Once the `purpose` fires for an enrolled subscriber (e.g., they `makes_an_order`), the campaign exits them on the next worker cycle, applies the Step 4 tags, and removes them from the active enrolment pool.
- **Tags created inline are persisted to the store's tag library.** The save endpoint adds any new tags to the store's library as part of the save cascade — see [[campaigns-edit-validation-rules]].
- **Currently only `makes_an_order` is selectable.** The legacy editor exposed additional `purpose` values; the modern Vue editor restricts the dropdown to `makes_an_order` only. (verify — confirm whether the backend accepts other values via API even though the dropdown hides them.)
- **`customers_tags` survives a draft save without validation.** The Save-draft path doesn't validate the tags list; the Start-campaign pre-flight check only verifies that other required settings are filled (segment, action steps, messages) — see [[campaigns-edit-validation-rules]].

## Related

- [[marketing-campaigns-edit]] — hub.
- [[marketing-campaigns-subscribers]] — the recipient list shows which subscribers exited and got tagged.

## Open questions

- (verify) Whether the save endpoint accepts `purpose` values other than `makes_an_order` (e.g., `set_customer_group`) via direct API calls — the legacy editor exposed more options, but the modern dropdown restricts to one. Custom-API callers may still be able to set others.
