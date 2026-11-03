---
type: feature
nav_path: "Orders → Order details → Credit note → Actions"
route_name: admin.order.credit.action
route_path: /admin/orders/credit/action/:order_id
aliases: ["Credit note actions", "Create credit note", "Download credit note", "Send credit note", "View credit note dropdown"]
tags: [orders, credit-note, refund, pdf, invoicing, smarty]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 7
---
# Credit note — actions (Create / Download / Send)

> Part of [[orders-credit]]. See the hub for the other aspects (eligibility, numbering, document, send quirks).

## Purpose

The three merchant actions on the **View credit note** dropdown — **Create**, **Download**, and **Send to customer** — plus the inline-AJAX UI that drives them. This aspect covers the button, the dropdown, which links are visible in each state, and the no-modal flow. Eligibility (when the button appears at all) is on [[orders-credit-eligibility]]; the PDF itself is on [[orders-credit-document]].

## Where to find it

From [[orders-details]] → action toolbar → **View credit note** button (icon `fa-file-alt`). Clicking the button toggles open a small hover-style dropdown (`.credit-note-dropdown`) anchored below it: white background, 1 px grey border, 5 px radius, min-width 185 px. The dropdown contains up to three vertically-stacked links.

## What the merchant can do here

- **Create credit note** — issues the credit note (consumes the next credit-note number — see [[orders-credit-numbering]]).
- **Download credit note** — opens the PDF in a new tab.
- **Send credit note** — emails the PDF to the customer.

## Settings & fields

Three routes back the actions:

- `POST /admin/orders/credit/create` (`admin.order.credit.create`) — **Create**. Posts `order_id` in the body (from the page's JS context).
- `GET /admin/orders/credit/action/{order_id}/{output?}` — **Download** PDF. The `output` param is accepted but not branched on; `target="_blank"` opens a new tab.
- `POST /admin/orders/credit/action/{order_id}` — **Send** to customer (queues the notification email; same route as Download, different verb).

**Dropdown link visibility** — which links show (vs hidden via the `.hidden` CSS class) depends on whether a credit-note number is already assigned:

| State | Create | Download | Send |
|-------|--------|----------|------|
| No credit number yet | Visible | Hidden | Hidden |
| Credit number assigned | Hidden | Visible | Visible |

After Create succeeds, inline JS removes `.hidden` from all three links, then re-applies it to Create — so the merchant sees Download + Send immediately without a page reload.

**Result toasts** (translated):

- Create success: *"Credit note created"* (`order.action.notify.credit_note_created`).
- Create error: *"Could not create credit note"* (`order.action.notify.credit_note_create_error`).
- Send: *"Credit note sent"* (`order.action.notify.credit_note_sent`).

## Business rules

### No modal — all three actions are inline AJAX

Unlike the invoice's manual-number flow (see [[orders-invoice]]) — which opens a modal when `invoice_number_type = 2` to collect a typed number — the credit-note flow has NO data-collection step. There is no eligibility wizard, no amount-entry input, no reason-text field, no date picker. The merchant clicks Create and the platform fills everything from the order's current state (number, date, line items, totals, reason text — see [[orders-credit-numbering]] + [[orders-credit-document]]).

### Issue-and-send chain — Send creates on the fly

The Send flow internally issues-and-fetches the credit note. So if no credit note has been created yet, **Send credit note will create one on the fly** before sending. The merchant can skip the Create step entirely and click Send directly if they're confident the order is eligible.

### Download requires an existing credit note

The Download route returns 404 if no credit note exists OR the active provider returns null. The merchant must Create the credit note first before downloading.

### Smarty / jQuery / AJAX flow

- Create and Send use AJAX POST with toastr notifications.
- Download is a direct link with `target="_blank"`.
- Dropdown button visibility toggles via `.hidden` class manipulation after Create succeeds.
- Several toast behaviours are misleading (always-green on Send, fire-and-forget) — see [[orders-credit-send-quirks]].

### Permission

Standard orders permission scope. Some external invoicing apps may add per-app permissions.

## Related

- [[orders-credit]] — hub.
- [[orders-details]] — parent page (the dropdown lives here).
- [[orders-invoice]] — sister flow; its modal-based manual-number entry contrasts with the no-modal credit flow.

## Open questions

- Whether a merchant-facing "cancel credit note" link is ever added to this dropdown (currently none).
