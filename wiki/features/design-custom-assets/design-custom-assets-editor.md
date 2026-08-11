---
type: feature
nav_path: "Design → Custom CSS/JS → Editor"
route_name: admin.custom.assets
route_path: /admin/storefront/custom-assets
aliases: ["Custom CSS/JS editor", "Custom code editor", "CodeMirror custom assets", "custom_assets field", "Редактор персонализиран код"]
tags: [design, custom, css, js, advanced]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---
> Part of [[design-custom-assets]]. See the hub for the other aspects (injection point, storage & lifecycle).

# Custom CSS/JS — the editor

## Purpose

This aspect covers the **editor surface** of the [[design-custom-assets]] screen — the single full-width CodeMirror code editor where the merchant pastes raw HTML / CSS / JS, the one `custom_assets` field behind it, and the Save action. It also catalogues the things the editor deliberately does **not** offer (no preview, no rollback, no per-page targeting, no enable/disable toggle), because those gaps drive most support questions about why custom code "doesn't work the way I expected".

## Where to find it

Sidebar → **Design** → **Custom CSS/JS**, route `/admin/storefront/custom-assets`. The editor is the entire body of the screen — there are no tabs or sub-sections. The Save button sits top-right. See the hub [[design-custom-assets]] for the full sub-route table.

## What the merchant can do here

The screen is a single full-width form with one big CodeMirror editor:

- See a **single textarea** styled as a CodeMirror editor:
  - **Mode:** `htmlmixed` — HTML with embedded `<style>` / `<script>` blocks all highlighted appropriately.
  - **Line numbers** on the left.
  - **Line wrapping** on (long lines wrap visually without horizontal scroll).
  - **Code folding** (collapse / expand nested tags via the fold gutter).
  - **Active-line highlight** (the line the cursor is on is shaded).
  - **Bracket matching** (jumping between matching `<tag>` / `</tag>` or `{ }`).
  - **Vertical resize handle** — the editor starts at 250px minimum and the merchant can drag the bottom-right corner to make it taller.
- Paste any combination of:
  - `<style>...</style>` blocks for CSS rules.
  - `<script>...</script>` blocks for inline JavaScript.
  - `<script src="..."></script>` blocks for external scripts.
  - `<link rel="stylesheet" href="...">` tags for external stylesheets.
  - `<meta name="...">` tags (rarely useful but allowed).
  - Plain HTML markup of any kind.
- Click **Save** (top-right *"Edit"* button, label `global.action.edit`) — persists the editor content. Success message: *"Theme settings successfully edited"*.

Where that pasted markup actually lands is covered in [[design-custom-assets-injection]].

### What the merchant cannot do here

- The merchant cannot **target a specific page** with their custom code — whatever is pasted is injected into the `<head>` of EVERY storefront page. To scope code to certain pages, wrap the JS in client-side path checks (e.g., `if (location.pathname.startsWith('/category/')) { ... }`). See [[design-custom-assets-injection]] for why there is no server-side per-page filter.
- The merchant cannot **target the footer / body close** — only the `<head>`. Scripts that need the DOM ready can use standard `DOMContentLoaded` / `load` listeners.
- The merchant cannot **preview before saving** — there is no draft mode, no staging, no "test on a sandbox URL". Save publishes to the LIVE storefront immediately.
- The merchant cannot **see syntax errors** — the editor has no JS / CSS linter. A typo (e.g., a missing closing brace) only surfaces when the storefront renders, where the broken script silently fails or breaks the whole page.
- The merchant cannot **roll back** — there is no version history. Saving replaces the previous content entirely; the merchant must keep their own backup. See [[design-custom-assets-storage]].
- The merchant cannot **enable / disable** the custom code without deleting it. To turn it off temporarily, clear the editor or wrap everything in HTML comments (`<!-- ... -->`).
- The merchant cannot **set a size limit** — the field has no documented maximum (other than database-column limits). Pasting tens of KB is allowed but inflates every storefront page response.
- The merchant cannot **A/B test or schedule** — the code is always-on once saved; there's no time-window, audience-segment, or A/B-split UI.

## Settings & fields

### The single editable field

| Field | Editor | Format | Required | Maximum |
|-------|--------|--------|----------|---------|
| `custom_assets` | CodeMirror `htmlmixed` mode (line numbers, wrapping, folding, active-line, bracket matching) | Free-form HTML / CSS / JS (any combination) | No (an empty save removes all custom code) | No documented limit (constrained by the database column, typically large-text). |

### Save action

| Action | Trigger | Confirmation | Result |
|--------|---------|--------------|--------|
| **Edit** (Save) | Click *Edit* button top-right (label `global.action.edit`) | None | Saves via AJAX. Success message: *"Theme settings successfully edited"*. The storefront serves the new code on the next page load (within seconds — there's no cache flush step). |

Submitting the form (e.g., by pressing Enter while focused on the button) goes through the same AJAX save handler; the form is prevented from reloading the page.

## Business rules

### The editor is initialised on a hidden textarea

The editor library is CodeMirror 5.41–5.59 (loaded from cdnjs at render time), configured for `htmlmixed` mode with HTML / XML / JS / CSS modes also loaded. The dark theme is `base16-dark`. The editor is initialised on a hidden `<textarea>` and its content is synced back to the textarea on every `change` event, so the standard form submit picks up the latest content.

### Save stores the raw value with no validation

The save endpoint receives a POST with one field — `custom_assets` — and stores its raw value verbatim. There is no parsing, no validation, and no transaction wrapper. Failures (e.g., database connection errors) bubble up as standard errors and the merchant sees a generic toast failure. The reasons there is no sanitisation, and the per-theme storage behaviour, are on [[design-custom-assets-injection]] and [[design-custom-assets-storage]] respectively.

## Related

- [[design-custom-assets]] — hub.
- [[design-custom-assets-injection]] — where the pasted markup is injected on the storefront.
- [[design-custom-assets-storage]] — how the saved content is stored, scoped to theme, and removed.
- [[design-theme-editor]] — the variable-based customiser; use it first for any style exposed as a named variable.

## Open questions

None.
