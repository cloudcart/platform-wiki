---
type: feature
nav_path: "Marketing → Campaigns → Copy → What transfers"
route_name: admin.api.campaigns.copy
route_path: /admin/api/core/marketing/campaigns/copy/{id}
aliases: ["What gets copied", "Copy campaign fields", "What is preserved on copy", "Copy title suffix", "Message design snapshot on copy"]
tags: [marketing, campaigns, copy, duplicate]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Copy campaign — what transfers

> Part of [[marketing-campaigns-copy]]. See the hub for the other aspects (action flow, state & quota).

## Purpose

This aspect is the authoritative field-by-field answer to "what does Copy actually carry over, and what does it reset?" It also covers the *" - Copy"* title suffix (and its unconditional stacking), the deliberate `start_at` exclusion, how message designs are snapshotted, how saved-template links are preserved (with the shared-edit warning), and how the trigger segment and exit tags are referenced rather than duplicated.

## Where to find it

This is the data outcome of the **Copy** action — Sidebar → **Marketing** → **Campaigns** → any non-archived tab → **Copy** in a row. There is no separate screen; the result is visible as pre-filled fields when [[marketing-campaigns-edit]] opens for the new Draft.

## What the merchant can do here

After Copy, the merchant inspects the pre-filled editor and adjusts anything that should differ for the new send (title, trigger segment, step delays, message content, start time). Everything in the "Copied = Yes" rows below arrives pre-filled; everything in the "Copied = NO" rows starts blank / reset.

## Settings & fields

### What gets copied

| Field | Copied | Notes |
|-------|--------|-------|
| `type` | Yes | Regular stays Regular; Automated stays Automated. |
| `title` | Yes, with suffix | *"{title} - Copy"* |
| `description` | Yes | |
| `trigger_condition` | Yes | Same trigger; for Automated this could be `gets_in_segment` etc. |
| `trigger_segment` | Yes | Points to the **same** segment as the source. The merchant can change it in the editor. |
| `customers_tags` | Yes | Exit tag value (comma-separated tag-name list). |
| `purpose` | Yes | Exit purpose. |
| `repeat` | Yes | Repeat-the-campaign toggle. |
| `use_exists_subscribers` | Yes | "Execute campaign for existing subscribers in segment" toggle. |
| `dynamic_tags` | Yes | Dynamic-generated-tags-from-segment toggle (may be silently reset on save — see Business rules). |
| **Actions** (every step) | Yes | All step rows are replicated with new IDs, kept in the same order. |
| **Action templates** (every message) | Yes | All message templates are replicated and re-linked to the new actions by `(campaign_id, action_order)`. |
| `active` | **NO** — reset to 2 (Draft) | Cloned campaigns start in Draft regardless of source state. See [[campaigns-copy-state-and-quota]]. |
| `archived_at` | **NO** — reset to NULL | Cloning an archived campaign produces a fresh Draft. |
| `progress` | **NO** — reset | The progress state is per-instance. |
| `start_at` | **NO** | Deliberately excluded — the copy has no schedule (see below). |
| `created_at` / `updated_at` | **NO** | New timestamps. |
| `id` | **NO** | New auto-increment ID. |
| Enrolled subscribers (pivot) | **NO** | The copy starts with zero enrolled subscribers. |
| Statistics (logs / counters) | **NO** | The copy starts with zero stats. |

### `start_at` is NOT copied

The clone deliberately excludes the source's `start_at` value — the copy's `start_at` is unset. A scheduled source campaign produces a copy with **no** schedule, and the merchant must pick a new start time in the editor before launching.

## Business rules

### Title suffix: unconditional *" - Copy"* stacking

The clone title is mechanically *"{source.title} - Copy"*. There's no "if already ends with - Copy, append a number" smartness — copying *"Welcome - Copy"* produces *"Welcome - Copy - Copy"*, and copying that produces *"Welcome - Copy - Copy - Copy"*.

### Title-collision is detected on the next Save, not on Copy

The Copy endpoint itself does **not** check whether the *"{source.title} - Copy"* title already exists; it inserts the row regardless. The conflict only surfaces when the merchant clicks **Save campaign** in the editor — the title field's `unique:campaigns,title` validator returns *"Campaign with this title already exists"*. So after Copy the merchant lands on the editor with a possibly-colliding title pre-filled, but the page does not warn until a save attempt. The merchant must rename before saving. Merchants who copy repeatedly without renaming will hit this on save.

### Message designs are copied as verbatim snapshots

For **Email** steps, the Unlayer JSON design + HTML + variables are all copied verbatim — the clone's email looks identical to the source's on send. The same applies for **SMS** body text, **Viber** payload, and **Web Push** title + body. If the source's email referenced an image URL on the merchant's CDN, the clone references the **same** URL — there's no asset duplication.

### Saved-template linkage is preserved — shared-edit warning

If a step references a **saved** Email template (via `template_id` + `template_type`) rather than carrying a fully-inline copy, the clone preserves that link — its action template still points at the saved template. **Future edits to the saved template will affect BOTH the source and the copy** — there's no "snapshot at copy time" behaviour for the linked case. Merchants who want a fully independent copy must duplicate the saved template separately in [[marketing-campaigns-message-template|saved templates]] and re-link the copy's step to the new one.

### Tags are referenced, not duplicated

The exit tag (`customers_tags`) is a comma-separated tag-name list — the clone copies this string verbatim. The tags themselves live in [[marketing-subscribers|Tags]] and are referenced by name; the clone references the same tags as the source. If the merchant later renames a tag, both campaigns reflect the new name automatically.

### Predefined-template provenance is NOT preserved

If the source was originally cloned from a [[marketing-campaigns-from-predefined|predefined template]], the resulting clone in this Copy flow does **not** remember its predefined-template origin. The copy is just a regular campaign — there's no link back to the template.

### `dynamic_tags` may be silently reset on save

The `dynamic_tags` field is copied verbatim — but on the next Save, the platform cross-checks whether the (also-copied) trigger segment actually supports dynamic tags. If not, `dynamic_tags` is force-set to 0 on save. So if the merchant copies the source then swaps the trigger segment to one without dynamic-tag support, the toggle quietly stops working. See [[campaigns-copy-state-and-quota]] for the full segment-related save behaviour and [[marketing-campaigns-edit]] for the validation rules.

## Related

- [[marketing-campaigns-copy]] — hub.
- [[marketing-campaigns-edit]] — editor where the copied fields land pre-filled.
- [[marketing-campaigns-message-template]] — saved templates; the shared-edit warning applies to linked steps.
- [[marketing-campaigns-from-predefined]] — predefined-template clone path (provenance not preserved on Copy).
- [[marketing-segments]] — the trigger segment shared between source and copy.
- [[marketing-subscribers]] — tags referenced (not duplicated) by the copy.
- [[campaign]] — Campaign entity (and its actions / steps that get cloned).

## Open questions

No outstanding questions.
