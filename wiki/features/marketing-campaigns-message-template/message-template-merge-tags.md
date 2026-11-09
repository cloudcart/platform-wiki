---
type: feature
nav_path: "Marketing → Campaigns → Edit → Set message → Merge tags"
route_name: admin.api.campaigns.email-templates.variables
route_path: /admin/api/core/marketing/campaigns/email-templates/variables
aliases: ["Merge tags", "Campaign variables", "Personalisation variables", "{$shop_name}", "{$subscriber_first_name}", "{$products_leave_feedback_url}", "{$dynamic_discount_code}", "Variables legend", "Променливи в кампания", "Динамичен код за отстъпка"]
tags: [marketing, campaigns, message, template, variables, personalisation]
plan_gates: ["campaigns"]
created: 2026-06-10
updated: 2026-11-09
source_count: 3
---

> Part of [[marketing-campaigns-message-template]]. See the hub for the other aspects (Email designer, channel variants, saved + predefined, demo send, validation, save flow).

# Campaign message editor — Merge tags & personalisation

## Purpose

Merge tags (a.k.a. variables) let the merchant write **one** message template that personalises per recipient at send time. The editor renders them as `{$variable_name}` literal strings everywhere (preview, demo, body) — substitution happens inside the per-channel send job against the real recipient's data, never inside the editor.

This aspect documents the variables catalogue, the discount variables, the segment-dependent variables (`{$triggered_products:N}`), the Variables legend UI, and how variables are extracted from the body for validation.

## Where to find it

- **Email designer:** Variables legend pane below the Unlayer designer in the scratch modal.
- **SMS / Viber / Web Push:** Variables legend pane below the form column in `CampaignMessageSettingsModal`.
- **Unlayer merge-tag dropdown:** Unlayer's built-in merge-tag dropdown is pre-populated with the same variable list.

The variables list is fetched from `GET /admin/api/core/marketing/campaigns/email-templates/variables` (`apiMarketingCampaignEmailTemplates.variables`). The legend is campaign-aware — segments that support dynamic tags include extra variables.

## What the merchant can do here

### Variables legend pane

Common layout across all channels:

- Heading *"Variables legend"*.
- Long description: *"Those are the variables you can use in the notification. When the email is sent, those variables will be replaced with their actual values. Example: {$shop_name} will be replaced with the name of your store."*
- A 2-column grid of `{$variable}` (clickable to copy to clipboard, toast *"Copied to clipboard"* on success or *"Failed to copy"* on failure) + a human-readable label.

### Common variables

These resolve on every campaign:

| Variable | Resolves to |
|----------|-------------|
| `{$shop_name}` | Store's name. |
| `{$shop_url}` | Store's storefront URL. |
| `{$logo}` | URL of the store's logo. |
| `{$subscriber_first_name}` / `{$subscriber_last_name}` | Recipient's first / last name. |
| `{$subscriber_email}` | Recipient's email address (Email only). |
| `{$unsubscribe_url}` | Link to the recipient's subscription page ([[storefront-notifications]]); the platform does not add it. Not in Web Push. |

Web Push offers only `{$shop_name}`, `{$subscriber_first_name}` and `{$subscriber_last_name}`. Any `{$...}` still unresolved at send time is **removed**, so a button or link pointing to it ends up empty.

### Dynamic discount variables

| Variable | Resolves to |
|----------|-------------|
| `{$dynamic_discount_code}` | A **new** code generated for each recipient, valid only for the products the segment triggered for that recipient. Offered only when the segment provides `{$triggered_products:N}` and the plan includes `discount-code-pro` ([[marketing-discounts-code-pro]]). |
| `{$discount_code:CODE}` | One entry per active discount with a code (EAN8 / EAN13 excluded). Resolves to a **link to the cart with that discount applied**, not to the code text. |

For `{$dynamic_discount_code}` the message must also contain the triggered-products block, and the server requires a discount type, value and max uses (or unlimited). Today's campaign editor sends none of them, so such a message fails with *"Field is required"* (from the code; verify in the live editor). On save the platform creates a Code PRO discount named *"Campaign action order N - <campaign title>"* that holds the generated codes.

`{$generate_discount_code:10%}` is only a leftover label string: no legend offers it and nothing replaces it, so it is removed at send time like any unresolved variable.

The save flow's regex `~{\$([^{}]*)(:([^:\}]*))?}~` extracts every `{$var}` and `{$var:arg}` occurrence and runs the per-variable validators (see [[message-template-validation]]).

### Segment-dependent variables

When the campaign targets a segment that emits dynamic tags (e.g., abandoned-cart products from [[marketing-segments]]), extra variables appear in the legend:

| Variable | Resolves to |
|----------|-------------|
| `{$triggered_products:N}` | The first N products the segment matched for this subscriber (e.g. the abandoned-cart products), rendered as product blocks with links. Hidden products are included, since they open by direct link; a product must be active, not a draft, published and within its active-to date. |
| `{$products_leave_feedback_url}` | Link to a page where the subscriber reviews the products they bought. Only with a Product Reviews condition in the segment — see [[apps-product-review-campaign-link]]. |

The legend pane is campaign-aware: it only shows these when the campaign's segment supports them.

### Click-to-copy interaction

Every `{$variable}` chip in the legend is clickable; on click it copies the verbatim string (including the `{$` and `}`) to the clipboard and toasts *"Copied to clipboard"*. The merchant can paste straight into the body field. The same chips render inside Unlayer's merge-tag dropdown for Email.

## Settings & fields

### Variable substitution at SEND time, NOT at save time

Variables are stored verbatim in the saved template — substitution happens inside the per-channel send job against the actual recipient's data. So the merchant authors freely with variables; the editor doesn't validate against a specific customer. Demo sends are the one exception — they use synthetic data, see below.

### Demo-send substitution uses synthetic subscriber data

The demo handler builds a `new Subscriber(['first_name' => 'FirstName', 'last_name' => 'LasName', 'country' => setting('country')])` plus a synthetic `SubscriberChannel`. Variables in the message body resolve against this synthetic record — `{$subscriber_first_name}` → `FirstName`, `{$subscriber_last_name}` → `LasName`, `{$shop_name}` → the merchant's actual shop name.

The typo *"LasName"* (missing second `T`) is verified in source — the demo really does render `LasName` for the last name, while real sends use the real subscriber's last name. Full demo flow on [[message-template-demo-send]].

### Variables in Unlayer's merge-tag dropdown

Unlayer's built-in merge-tag dropdown is pre-populated with the CloudCart variable catalogue. The merchant uses Unlayer's UI to insert them, or types them by hand into text blocks. Both paths produce the same `{$variable}` literal in the saved Unlayer JSON.

## Business rules

### Two-pass validation extracts variables on save

The save flow performs two validation passes (full table on [[message-template-validation]]):

1. `validateChannelMessageRequest` — basic field-level rules (max length, required, etc.).
2. `validateChannelMessageRequestVariables` — scans the body with regex `~{\$([^{}]*)(:([^:\}]*))?}~` and invokes per-variable `validateVariableXxx($request, $text, $argument)` methods.

A save can fail for two distinct reasons: malformed body fields OR un-resolvable variable references.

### Missing dynamic-discount setup is an error

`{$dynamic_discount_code}` without the triggered-products block, or without the discount type / value / max uses, fails the second validation pass. At send time it comes out empty when the plan lacks Code PRO or the recipient has no triggered products; a code that fails to save is logged as an error.

### Variable names are stable

The variable names (`{$shop_name}`, `{$subscriber_first_name}`, `{$unsubscribe_url}`, etc.) are stable platform identifiers — they don't change across plan tiers, languages, or channel types. A variable resolves the same way on every channel that offers it.

### Tracking URL shortening + UTM stamping applies to Email

For Email demos AND real sends, the body's URLs are rewritten via `shortenUrls(text, {cc_campaign: {...}, cc_subscriber: {...}, utm_source: 'cloudcart', utm_medium: getUtmMedium, utm_campaign: campaign.title})`. The `cc_campaign` and `cc_subscriber` query params drive the platform's click-tracking; UTM stamping identifies CloudCart as source, the channel as medium, and the campaign title as the UTM campaign — automatic, no manual setup needed.

### Customer data is never touched by the editor

The editor doesn't pre-resolve variables for preview — the preview pane shows `{$variable_name}` as literal strings. This avoids the cost of fetching subscriber records into the editor AND prevents accidental data leaks through demo flows.

## Related

- [[marketing-campaigns-message-template]] — hub.
- [[marketing-campaigns-edit]] — parent campaign editor.
- [[marketing-discounts]] — the active discounts listed as `{$discount_code:CODE}`; [[marketing-discounts-code-pro]] — the code type `{$dynamic_discount_code}` generates.
- [[marketing-segments]] — segments that emit dynamic tags consumed by `{$triggered_products:N}`.
- [[message-template-validation]] — the two-pass validation that runs the per-variable validators.
- [[message-template-demo-send]] — synthetic-subscriber substitution path.

## Open questions

None.
