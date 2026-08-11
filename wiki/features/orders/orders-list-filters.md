---
type: feature
nav_path: "Orders → List → Filters"
route_name: admin.orders
route_path: /admin/orders/list
aliases: ["Orders list filters", "Order filter bar", "Order list filter operators", "Order filter URL", "Recovered source filter", "Made through filter", "Orders search box", "Saved filters", "Филтри на списъка с поръчки", "Запазени филтри"]
tags: [orders, list, filters, operators, search, saved-filters, url-encoding, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 5
---

> Part of [[orders]]. See the hub for the other aspects (columns, bulk actions, status taxonomy, default visibility, export, locking).

# Orders list — filters

## Purpose

The filter bar on `/admin/orders` combines a **free-text search box**, 22+ structured filter types, and **saved filter presets**. The merchant picks a filter from the dropdown, refines with operators (Is / Is not / Exactly / etc.), and stacks multiple filters together. The state is shareable as a URL **and** remembered in the session.

## Where to find it

Filter bar above the list table on `/admin/orders`. The merchant adds filters via the `+` (add filter) control; each filter shows its current value as a chip, removable individually. The search box and the **Saved filters** menu sit in the same bar.

## What the merchant can do here

### Free-text search box

A single keyword field, and the fastest way to find one specific order. What it matches depends on what is typed:

| Input | Matched against |
|---|---|
| A **number** | order number, invoice number, receipt number, product SKU, product barcode |
| A number (always) | shipping **and** billing **phone** — matched from the END, with leading zeros ignored, so `888123456` finds `+359888123456` |
| **Text** | customer email, customer first name, customer last name, the customer's checkout note, and product name / category / vendor |
| Anything containing **`@`** | customer email |
| Anything else | courier **waybill number**, payment hash, payment provider reference, and the order's checkout hash |

Practical consequences: searching a **phone number** or a **waybill number** is usually the quickest route to a customer's order; text matches are **prefix** matches, so searching `ivanov` finds *Ivanov* but searching `vanov` finds nothing.

Using the search box counts as applying a filter — so it also drops the silent default exclusion and reveals archived / cancelled / voided orders (see [[orders-list-default-visibility]]).

### Saved filter presets

The filter bar has a **Saved filters** menu. Once a filter combination is applied, **Save filter** stores it under a name (up to 30 characters), per admin — so each staff member keeps their own set. Saved presets can be deleted from the same menu, and can be **pinned as tabs** above the list for one-click switching. When the merchant has none, the menu reads *"No saved filters"*.

This is the right answer to *"I run the same filter every morning"* — no need to bookmark URLs.

### The 22+ filter types, by category

**Money & status:**
- **Order total** — Exactly / Not equal to / Less than / More than. Currency input.
- **Status** — Is / Is not + one of the platform's order statuses (see [[settings-statuses]] + [[orders-list-status-taxonomy]]).
- **Payment status** — Is / Is not + one of the payment statuses.
- **Status fulfillment** — Pick a fulfillment status directly.

**Providers:**
- **Payment provider** — Is / Is not + autocomplete from configured payment providers.
- **Shipping provider** — Is / Is not + autocomplete from configured shipping integrations.

**Customer:**
- **Customer** — Autocomplete from the customer list.
- **Customer group** — Autocomplete from customer groups.

**Discounts:**
- **Discount** — Any / No / specific discount type (Flat / Percent / Fixed / Shipping / etc.).
- **Discount code** — Visible only when discount codes exist; pick a specific code from the dropdown.

**Date:**
- **Date added** — Exactly / Before / After / From-To range. Date pickers.
- **Expected delivery** (conditional) — From / To range with date+time. Visible only when **Shipping Hours** app is installed.

**Geography:**
- **Region** — Autocomplete from city names.

**Marketing attribution:**
- **Recovered source** — Filter by recovered abandoned-cart source (e.g., email).
- **Made through** — Filter by where / how the order was created (storefront / admin / etc.).
- **Referer** — Autocomplete from past referer strings.
- **UTM source** / **UTM medium** / **UTM campaign** — Autocomplete from historical UTM values.

**Flags:**
- **Fast order** — Yes / No.
- **Archived** — Yes / No.
- **Draft** — show only orders flagged as drafts.
- **Created by admin** — show only manually-entered orders (filter `isAdmin = yes`).

**Apps-conditional:**
- **Supplier** — Visible only when the **Suppliers** app is installed.
- **Products** — Is / Is not + autocomplete from products (limit the list to orders containing specific products).

### Filter operator encoding (verified)

The filter operators in the URL query string are numeric codes, NOT free text:

| Operator | Numeric code | Used by filters |
|---|---|---|
| Is | 1 | status, payment status, payment provider, shipping provider, customer, products |
| Is not | 2 | same as above |
| Less than | 3 | order total |
| More than | 4 | order total |
| Exactly | 1 | order total, date added |
| Not equal to | 2 | order total |
| Before | 2 | date added |
| After | 3 | date added |
| From-To range | 4 | date added (with separate `value[from]` + `value[to]`) |

Yes / No flag filters use string values: `yes` / `no` / `1` / `0` depending on the filter (Fast order uses 1/0, Archived uses yes/no, Draft uses yes-only, Created-by-admin uses yes-only).

### Filter URL conventions

All filters serialize into the URL as `filters[<key>][operator]=<code>&filters[<key>][value]=<value>`. Multi-value filters (autocomplete) post their selected ID(s) into `filters[<key>][value]`. Date-range filters use the bracket form `filters[dateAdded][value][from]` + `filters[dateAdded][value][to]`. The merchant CAN share the URL with another admin to reproduce the same view. Appending `?filter_reset` clears the remembered filters (see below).

## Settings & fields

The filter UI reads its option lists from elsewhere:

- Status taxonomy: [[settings-statuses]] (including merchant-defined custom statuses).
- Payment providers: [[settings-payment-providers]].
- Shipping providers: [[shipping]].
- Customer groups: customers area.
- Discount codes: [[marketing-discounts]].

Saved presets are stored per admin account; page size and page number are remembered separately from the filters themselves.

## Business rules

### Filters are REMEMBERED — this is the top "wrong numbers" cause

Filter state is **persisted for the session**, not per page load. Once the merchant applies a filter, it is stored and **re-applied automatically** the next time they open Orders — even after navigating to a completely different part of the admin panel and back, and even though the URL then shows no `filters[...]`.

This produces the classic confusion: *"orders are missing"* / *"my totals are wrong"* / *"my export only had half the orders"* when in reality a filter set hours earlier is still active. Two ways out:

- clear the filter chips in the bar, or
- open the list with `?filter_reset` appended.

The sort column, sort direction, page and page size are handled separately and are not part of the remembered filter set. Because the export reads the same state, a forgotten filter silently narrows the export too — see [[orders-list-export]].

### Status = Pending silently ALSO filters to not-fulfilled

A hard-coded quirk with real consequences. Whenever **Pending** is among the selected values of the **Status** filter, the platform silently adds a second condition: fulfillment must be **not fulfilled**.

So an order that is `pending` **and** already fulfilled is **invisible** under Status = Pending. Nothing in the UI hints at it — the filter chip just reads *"Order status is Pending"*. The extra condition is applied even with the **Is not** operator, where it makes no sense at all.

Merchants hunting a pending-but-dispatched order should filter by fulfillment status, use the free-text search box, or clear the Status filter.

### Payment status and Order total cancel each other out

The **Payment status** filter and the **Order total** filter are registered under the same internal slot, so applying both means **Order total wins and Payment status is silently dropped** from the query.

The UI gives no warning: both chips stay on screen, both look active, and the result set is simply wrong — it is filtered by total only. The merchant should apply them **one at a time** (filter by payment status, then read the totals; or filter by total, then read the payment statuses) rather than stacking them.

### Recovered source vocabulary — email only in the UI

The **Recovered source** filter dropdown in the filters template exposes exactly ONE option (excluding "All"):

- **email** — *"Recovered from email"* (`order.filter.recovered_from_email`).

Although the platform's underlying `restore_source` meta field CAN hold other values (e.g., `messenger` for the Messenger Bot recovery flow), the filter UI does not surface them — so merchants can only filter for email-recovered orders from this screen. To find Messenger-recovered orders, the merchant has to use the URL query string directly (`filters[recoveredSource]=messenger`).

The "Order was recovered through `<source>`" banner in [[orders-history]] correctly renders ALL recorded sources, not just email.

### "Made through" vocabulary — dropdown is EMPTY

The **Made through** filter renders as an empty select with only the *"-- All --"* option. There are NO predefined options in the filter template — so out-of-the-box the filter effectively does nothing in the UI. The platform's `cart.source` meta CAN be set to values like `messenger-bot` by integration apps, but the merchant cannot pick those from the dropdown — they'd need to type the value into the URL query string manually (`filters[madeThrough]=messenger-bot`).

This filter is effectively a placeholder for future expansion. Most stores can ignore it.

### Conditional filters — Shipping Hours app

The **Expected delivery** filter appears only when the **Shipping Hours** app is installed. (The same app conditionally adds the **Shipping date** column — see [[orders-list-columns]].)

### Conditional filter — Suppliers app

The **Supplier** filter appears only when the **Suppliers** app is installed.

### Conditional filter — Discount code

The **Discount code** filter appears only when at least one discount code exists in the store (see [[marketing-discounts]]). On stores with no codes, the filter type is hidden from the dropdown.

### Filter stack is OR within type, AND across types

Selecting multiple values inside one filter is an OR (e.g., Status = Paid OR Completed). Stacking filters of different types is AND (Status = Paid AND Date added = Today). The filter chip UI doesn't make the OR explicit — the merchant sees multiple values in one chip.

### Applying ANY filter reveals cancelled, voided AND archived orders

The default list silently hides cancelled, voided and archived orders. That exclusion is **all-or-nothing**: the moment **any** filter is applied — a date range, a customer, even just typing in the search box — the exclusion is dropped **completely**, and archived / cancelled / voided orders appear alongside everything else.

So a merchant who filters by *Date added = Today* sees MORE orders than the unfiltered list, including archived ones they did not ask for. See [[orders-list-default-visibility]].

## Related

- [[orders]] — hub.
- [[orders-list-columns]] — column layout (filter bar sits above this).
- [[orders-list-status-taxonomy]] — Status filter target values.
- [[orders-list-default-visibility]] — why filter presence changes default visibility.
- [[settings-statuses]] — status taxonomy.
- [[settings-payment-providers]] — payment-provider autocomplete source.
- [[shipping]] — shipping-provider autocomplete source.
- [[marketing-discounts]] — discount-code autocomplete source.
- [[orders-history]] — where ALL recovered-source values render (vs the filter-UI single option).
- [[orders-list-export]] — inherits the remembered filter state.
- [[fulfillment-and-warehouse]] — the fulfillment status silently added by the Pending filter.

## Open questions

None.
