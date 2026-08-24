---
type: feature
nav_path: "Orders → Details → Header"
route_name: admin.orders.details
route_path: /admin/orders/details/:order_id
aliases: ["Create order button disabled", "Създай поръчка неактивен", "draft order cannot be created", "draft says add products payment shipping", "order draft blocked", "Order header", "Order details header", "Order breadcrumb", "Order toolbar", "Header actions toolbar", "Draft alert", "Issue return button", "Why does my paid order show Fulfilled"]
tags: [orders, order-details, header, toolbar, status-pill, draft, returns]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 4
---

> Part of [[orders-details]]. See the hub for the other aspects (products, addresses, payment, shipping, history, actions, known issues).

# Order details — Header

## Purpose

The top strip of the order details page: breadcrumb + status pill on the left, prev / next navigation, and a right-hand toolbar of header-level actions. When the order is in draft state, a yellow guidance banner sits directly under the breadcrumb explaining what's missing before the order can be "created".

## Where to find it

Always visible at the top of `/admin/orders/details/<order_id>` — the merchant doesn't need to scroll. Status changes happen here (via the pill) and most "one-shot" order-level actions (print, copy link, cancel, archive) live in the right-hand toolbar.

## What the merchant can do here

### Breadcrumb area

- **Breadcrumb**: `Orders` → `#<order_number>` → `<order date>` → `<order status>` chip.
- **Prev / Next** navigation buttons (with neighbouring order IDs) — walk through orders without going back to [[orders]].

### Status pill — inline change

The breadcrumb's status chip is loaded async (`admin.orders.status.load`). Clicking it opens a popover with the available statuses; selecting one calls `admin.orders.change-status` with the new status. Allowed transitions depend on the merchant's [[settings-statuses]] taxonomy. The full status-change flow + side effects is on [[orders-status-change]].

### Header actions toolbar (right side)

The toolbar's contents are state-conditional and app-conditional. **A draft order has no toolbar at all** — the whole strip is suppressed until the draft is committed via **Create order**, so there is no Print, no Copy checkout link and no 3-dot menu on a draft.

| Action | When visible | What it does |
|--------|--------------|--------------|
| **View invoice** | Only when an Invoicing app is active AND a raw invoice number exists on the order | Opens the invoice PDF in a new tab. Full flow: [[orders-invoice]]. |
| **Issue return** | Only when the order is returnable — see below | Opens the return modal (Full return / Partial return). Full flow: [[orders-details-returns]] → [[orders-returns]]. |
| **Print order** | Always | Opens the print dialog (uses the merchant's `print_body` setting from [[settings-invoicing]] if configured, otherwise the default body). Full flow: [[orders-receipt]]. |
| **Copy checkout link** | Only when order is NOT completed / paid / refunded AND fulfillment is not fulfilled | Copies an encrypted checkout-resume URL — used to send a payment link to the customer if the order is still pending. |
| **imos3d XML download** | Only when imos3d app is installed AND the order has imos3d metadata | Downloads the XML feed for the imos3d / furniture pipeline. |
| **3-dot dropdown** | Always when at least one of the below is allowed | Conditional menu — see next table. |

### 3-dot dropdown menu

| Menu item | When visible | What it does |
|---|---|---|
| **Cancel order** | Only when `order.status == pending` AND `quantity_enough` (stock is sufficient) | Confirmation *"Are you sure?"* dialog → status transitions to `cancelled`. Restocks lines per [[inventory-restock]]. |
| **Archive / Unarchive** | Only for `completed` / `cancelled` orders | Toggles the archived flag. Archived orders are filtered out of default views unless **Archived = Yes**. |
| **Mark as completed** | Only when `order.status == 'paid'` AND `status_fulfillment == 'fulfilled'` | Promotes status to `completed`. Fires the Completed status's customer notification email if the per-status email toggle is ON in [[settings-statuses]]. |

### There is no longer a "Credit note" dropdown

The old order-level **Credit note** menu (Create / Download / Send credit note) has been **removed from the toolbar**. Whole-order credit notes are now issued **per return**, from the **Returns & exchanges** box — see [[orders-details-returns]]. Credit notes created under the old flow remain downloadable from the returns list and from [[orders-invoices]]; the accounting model itself is unchanged ([[orders-credit]]).

### Draft alert (only when `is_draft = 1`)

A warning banner is rendered for orders in draft state. The content is composed dynamically, and **each fragment appears only when that specific piece is missing**:

- No line items → *"… add products …"* fragment.
- No payment record on the order → *"… select payment …"* fragment.
- No shipping record on the order → *"… configure shipping …"* fragment. Skipped entirely when the order has **only digital products** (nothing to ship), so a digital-only draft is never held back for shipping.

### 🔴 ANY ONE missing piece disables Create order — not all three

The **Create order** button is disabled when **products OR payment OR shipping** is missing. It is not a case of "all three must be missing"; a draft that has products and payment but no shipping record is blocked exactly the same way.

This matters when reading a merchant's report. Because the fragments are per-piece, **the banner text tells you precisely what is missing** — a banner naming only delivery means products and payment are recorded and only the shipping record is absent. Conversely, a disabled button is **not** evidence that all three are missing, and it is not evidence of a validation fault: it is the designed response to the one piece that is not there.

Two traps when checking the order's data against the banner:

- **The payment shown is the newest record.** The order's payment is read as the most recent payment row, so older rows left behind by earlier changes of method are irrelevant — one current record is enough to satisfy the check, and several stale ones do not block anything.
- **A courier being visible and selected on screen is not the same as a shipping record existing.** If the courier returned a quote but the rate never got written to the order, there is no shipping record and the draft stays blocked — the screen shows a chosen courier while the banner correctly reports delivery as missing. Investigate why the rate is empty ([[orders-details-shipping]]), not why the button is disabled.

**Other button states:**

- Order ready but not confirmed → **Create order** button enabled + (for online payments) a second **Create order and send to client** button (creates the order AND emails the customer a payment link).
- Order confirmed but waiting for online payment → manual-order help text + the customer's checkout URL with a copy-to-clipboard action and a **Send as email** button.

See [[orders-add]] for the manual-order-add flow that produces this draft state.

## Settings & fields

The header itself has no editable fields — every control is an action button or a navigation chip. The behaviour of those controls is configured elsewhere:

- Status taxonomy: [[settings-statuses]].
- Invoice / credit-note numbering: [[settings-invoicing]].
- Print body template (`print_body`): [[settings-invoicing]].
- Lock-orders timing (governs when the page is accessible to another moderator): `lock_orders` + `lock_orders_time` on **Settings → General** ([[settings-general-operational-toggles]]) — see [[orders-details-known-issues]].

## Business rules

### Status pill omits five statuses

The status dropdown surfaced from the breadcrumb pill OMITS five statuses: `chargebacked`, `disputed`, `timeouted`, `failed`, `voided`. An order CAN end up in those states (via payment-gateway webhooks), but the merchant cannot manually move an order INTO them from this pill — they're reachable only via automated payment-provider transitions.

### Status pill — draft orders only see "Cancelled"

For orders with `is_draft = 1` AND status != `cancelled`, the pill shows the draft-state badge and the dropdown is filtered to ONLY offer **Cancelled** as a target. Drafts can't transition to paid / completed / etc. via the pill — the merchant must use the **Create order** action on the draft alert first.

### The badge reads "Fulfilled" instead of the order status once the order is fulfilled

A frequent *"why does my paid order say Fulfilled?"* question. Whenever the order's **fulfillment status is `fulfilled`** and its order status is **not** `completed` and **not** `cancelled`, the badge shows the word **Fulfilled** — the fulfillment state, not the order status. A `paid` + fulfilled order therefore displays **Fulfilled**, even though its status is still `paid`. A draft shows **Draft** the same way.

This is display-only substitution: nothing has changed on the order, the status is still `paid`, and the badge keeps the **colour** of the real status (green for `paid`). The same substitution is applied in the **Status** column of the [[orders]] list, so the two surfaces agree. It does **not** apply to customer emails or campaign merge fields — those still print the real status. To read the underlying status, open the pill: the dropdown is built from the real status.

### Status pill colour scheme (verified)

The status badge's CSS class depends on combined state:

- **Completed** → green (`badge-green`).
- **Paid** → green (`badge-green`).
- **Pending** + `status_fulfillment = not_fulfilled` → orange.
- **Pending** + `status_fulfillment = fulfilled` → purple.
- **Cancelled** → red (`badge-red`).
- **Any custom status** → blue (`badge-blue`).
- **Archived** → gray (`badge-gray`).

### Cancel-order conditions

The **Cancel order** action is hidden unless the order is `pending` AND stock is sufficient (`quantity_enough`). For other statuses, cleanup paths are Refund ([[orders-payment-refund]]) for paid orders, Archive for completed / cancelled, or a return with its credit note ([[orders-details-returns]]) for refund accounting.

### When "Issue return" is shown

The action appears only when the order is **returnable**: it has not already been fully returned, its status is not one of the negative statuses (cancelled / refunded / voided / failed / chargebacked / disputed / timeouted), and it has either an **invoice number** already or has reached the point where one would be issued (`paid` / `completed` / fulfilled / fully digital). A pending, un-invoiced order is therefore NOT returnable and shows no Issue-return button — cancel it instead.

### Manual-order copy-to-clipboard checkout link

When the order is a manually-created draft awaiting the customer's online payment, the draft alert surfaces the encrypted checkout-resume URL (`/checkout/order/<increment_hash>/<encrypted_order_number>`). The link is partially truncated for display but copyable in full — clicking it copies the URL, then a tooltip flips to *"Link copied"*. The same URL also drives a **Send as email** action.

### Side effects of save

Any header-level action that changes status runs the platform's full save pipeline — see [[orders-details]] business rules and [[order-processing-pipeline]] for the chained effects (stock recompute, invoice numbering, customer income totals, webhook, audit log).

## Related

- [[orders-details]] — hub.
- [[orders-status-change]] — full status-change flow + per-transition side effects.
- [[orders-invoice]] — View invoice action.
- [[orders-details-returns]] — the Issue-return action + the Returns box that replaced the credit-note dropdown.
- [[orders-credit]] — the credit-note document itself (now issued from a return).
- [[orders-receipt]] — Print order action.
- [[orders-add]] — manual-order-add (produces the draft state).
- [[orders-archive]] — archive / unarchive flow.
- [[settings-statuses]] — status taxonomy + per-status customer-email toggle.
- [[settings-invoicing]] — invoice / receipt / `print_body` config.
- [[settings-general-operational-toggles]] — `lock_orders` + `lock_orders_time` (governs moderator-lock).

## Open questions

None.
