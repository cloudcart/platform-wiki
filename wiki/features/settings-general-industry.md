---
type: feature
nav_path: "Settings → General → Industry"
route_name: admin.main_industry.index
route_path: /admin/settings/general/industry
aliases: ["Main industry", "Primary industry", "Industry selector", "Основна индустрия", "Основен бранш", "CloudCart Analytics industry"]
tags: [base, settings, general, industry, analytics, onboarding]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 4
---
# Industry (Main industry / Primary branch)

## Purpose

A **one-shot modal screen** asking the merchant to pick the single industry that best represents their store. The selection is saved as the store's `main_industry` (a singular Google Product Category ID) and is used downstream by **CloudCart Analytics** as the primary categorization for the store's sales data and benchmark comparisons.

This is **separate** from the multi-select industry picker on [[settings-general]] ("What niche is your online store?"). That one (`site_industry`) is a JSON array used for Google Shopping integration and internal site segmentation. This screen sets the singular `main_industry` used by Analytics.

## Where to find it

The screen is not a regular sidebar destination. It opens automatically when an upstream onboarding / Analytics flow navigates the merchant here while `main_industry` is unset. Direct URL: `/admin/settings/general/industry`.

Once `main_industry` is set, visiting the URL **immediately redirects to the dashboard** — the modal won't display a second time.

## What the merchant can do here

- Read a brief informational message about CloudCart Analytics: *"Dear customers, We would like to inform you that we will soon launch our new feature — CloudCart Analytics. ... it is necessary for you to choose your niche, which will be set by default for the calculation of future analytical data for your store."*
- Select a single industry from a dropdown of Google Product Category options (the same flat list of base categories used elsewhere on the platform).
- Click **Save** to persist the choice. On success the page redirects back to wherever the merchant was interrupted (see [Post-save redirect](#post-save-redirect)), or to the dashboard.

What the merchant CANNOT do here:

- Pick multiple industries — this is a single-value selector (use [[settings-general]]'s multi-select for that).
- Re-open this screen once `main_industry` is set — visiting the URL just redirects to the dashboard. To change the value later, the merchant must use [[settings-general]]'s multi-select or contact support.
- Skip / dismiss without choosing — the modal has no Close button, the backdrop can't be clicked away, and Escape doesn't dismiss it.
- See category descriptions — only the category name is shown.

## Settings & fields

| Field / Control | What it does | Validation / notes |
|-----------------|--------------|--------------------|
| **Industry dropdown** (`industry`) | Single-select of Google Product Category IDs. | Required. Server rejects any value that isn't a real ID in the platform's Google Product Category taxonomy. |
| **Save button** | Persists the choice on `main_industry`. | Disabled while submitting. Shows a spinner. |

## Modals and sub-flows

This screen IS itself a modal (size `lg`). It is the entire page — there are no nested modals or sub-flows.

### Modal characteristics

| Element | Content |
|---------|---------|
| **Title** | *"Important"* (yellow warning shield icon + bold heading). |
| **Body — alert** | A yellow alert panel with the full informational message (5-paragraph welcome describing CloudCart Analytics). |
| **Field label** | *"Please select a primary branch, which is most suitable for your business"* |
| **Dropdown** | Native browser select (NOT searchable). A green border marks a valid pick, a red border an empty one. |
| **Save button** | The footer's only button — no Cancel. Disabled while submitting; shows a spinner. |

The modal is **forced-open**: Escape does nothing, clicking the backdrop does nothing, and there is no X icon in the header. The merchant cannot dismiss it without picking a value and clicking Save (navigating away to another URL is also intercepted).

### Post-save redirect

On a successful save the merchant is redirected back to the page they were interrupted on — the screen reads a `?return=<path>` parameter from the URL and navigates to `/admin/<path>`, or to `/admin/` if `return` is absent. This is a full page navigation, not an in-app route change, because the merchant usually arrived here as a redirect from a flow that should be revisited.

### Post-save failure

On error the server's message is shown as a red panel between the alert and the dropdown. The modal stays open, the Save button re-enables, and the merchant can try again or pick a different industry.

## Business rules

### Different from `site_industry` — applies to Analytics, not to the storefront

The value chosen here writes to a single `main_industry` field on the store. This is **distinct** from `site_industry` (a JSON array, set by the multi-select on [[settings-general]]). The two serve different consumers:

- **`main_industry` (this screen)** → CloudCart Analytics — the primary categorization that rolls the store up under one taxonomy bucket for industry-benchmark reports.
- **`site_industry` (settings-general)** → Google Shopping product-category alignment, internal site-segmentation that groups merchants for cross-merchant analytics and targeted communications, and the onboarding "industry answered" flag.

A merchant who updates one does NOT automatically update the other; if the store's positioning changes, update both independently.

### Self-redirect when already set — modal won't reopen

If `main_industry` is already set, the route redirects to the dashboard. The merchant cannot re-open this modal from this URL. **Changing the value after the fact** requires contacting support or being routed back by some other onboarding/Analytics flow that forces a re-selection (rare).

### Single value — no multi-select here

Despite living next to a multi-select on [[settings-general]], this screen forces a **single** primary industry. Analytics needs one canonical bucket per store for its rollups; a multi-select would create ambiguity ("is this store fashion or beauty?"). The merchant must pick the closest fit.

### Saved value is visible immediately

Saving updates the store record directly, so the new value is visible on the next read across the platform with no cache delay.

### No plan-gating

This screen is not gated by any plan-feature. Any active merchant can access it.

## How it works (verified against backend)

### One screen, two purposes — onboarding and Analytics unlock

The screen serves two adjacent goals:

1. **Onboarding step**: a new store created without `main_industry` is sent through this modal to capture the merchant's primary niche before deeper Analytics views.
2. **CloudCart Analytics gate**: the in-app banner mentions "for the calculation of future analytical data" — the value seeds the Analytics pipeline's per-site dimension.

A middleware was originally designed to force-redirect every admin request here until `main_industry` is set, but it is **currently disabled** — the merchant can use the rest of the admin without setting it. The screen is reached only when a specific upstream flow explicitly navigates here.

### Allowed-industries list comes from a shared source

The dropdown options are the same flat list of top-level Google Product Categories used by Google Shopping integrations and elsewhere, so any category here also exists in the [[settings-general]] multi-select.

### Permission

The screen requires standard admin login under the umbrella `settings` permission — there is no separate granular permission. A merchant Administrator always has access; a Moderator with no settings grants does not.

## Related

- [[settings]] — parent hub.
- [[settings-general]] — the multi-select industry field (`site_industry`) lives there, separate from `main_industry`.
- [[analytics]] — primary consumer of the `main_industry` value.
- [[apps-google-shopping]] — uses `site_industry` (the multi-select), not `main_industry`.
- [[plan-gates]] — concept page on plan-based feature gating (this screen is NOT gated).

## Open questions

_None._
