---
type: feature
nav_path: "Orders → + Add order → Delivery methods"
route_name: admin.orders.add
route_path: /admin/orders/add
aliases: ["Add order delivery methods", "Manual order delivery radio", "To address / To office / To locker / To store", "Add order pickup picker", "Stores app multi-store on manual order"]
tags: [orders, manual, smarty, draft, delivery, shipping]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-add]]. See the hub for the other aspects (wizard, customer, address handling, validation, draft state, no-API rationale).

# Add order — delivery methods

## Purpose

The **Delivery method** radio block in the **+ Add order** side panel decides what the order's shipping target is — a saved address, a courier pickup office, a courier locker, or a physical store run by the Stores app. This page documents the four radio values, when each one appears, what sub-block opens for each, and the JavaScript that swaps the sub-blocks on change.

## Where to find it

The Delivery method radio block lives in the sidebar of the **+ Add order** side panel, below the Customer card — see [[orders-add-wizard]] for the full panel layout.

## What the merchant can do here

### The four radio values

The radio set is built dynamically from the controller's `$types` array (the result of an installed-courier + Stores-app inspection). Possible values:

| Radio value | Label | When it appears | What sub-block shows |
|---|---|---|---|
| `address` | *"To address"* | Always | **Shipping address** dropdown — saved-addresses-of-customer list (`address_id` select). When customer has none, shows warning + the **+ Add new address** link. |
| `office` | *"To office"* | When at least one installed courier supports office pickup | **Office** picker (`office_id`, AJAX to `/admin/orders/offices/0`, min 2 chars to search) + first name + last name + phone (all required). |
| `locker` | *"To locker"* | When at least one installed courier supports locker pickup | **Locker** picker (`locker_id`, AJAX to `/admin/orders/offices/1`) + first name + last name + phone (all required). |
| `marketplace` | *"To store"* / *"To marketplace"* | When the **Stores** app is installed AND ≥ 1 active store exists | **Store** dropdown (`store_id`, from the active-stores array) + first name + last name + phone (all required). |

### Sub-block swap JavaScript

Switching the radio triggers JavaScript that:

- Removes the `.hidden` class on the matching sub-block.
- Adds `.hidden` to all other sub-blocks.
- Shows/hides the **+ Add new address** link (visible only for the `address` mode).
- Clears any previous validation errors on the radio block.

The sub-blocks themselves are detailed below.

### Address sub-block

Triggered when the merchant picks **To address**. Shows the **Shipping address** dropdown populated from the customer's saved addresses (loaded by the customer-change handler — see [[orders-add-customer]]). The **+ Add new address** link sits next to the dropdown — clicking it opens a slide-out-over-panel for creating a new address. See [[orders-add-address-handling]] for the full address handling.

### Office / locker sub-block

Triggered when the merchant picks **To office** or **To locker**. The picker is a Select2 autocomplete that queries `/admin/orders/offices/0` (offices) or `/admin/orders/offices/1` (lockers) for matching pickup points — minimum two characters to trigger the search.

The office and locker pickers use a custom Select2 result template (`window.officeResultTemplates`) that:

- Prepends the office image (max 20px tall) on the right.
- **Bolds the matched substring** of the office name when there's a search term — typing "сoph" highlights "**Soph**ia Central Office".

Once a pickup point is picked, the **first name**, **last name**, and **phone** fields all become required — the customer record's name is not used because the courier's manifest needs the actual recipient at the pickup desk.

### Marketplace sub-block (Stores app)

Triggered when the merchant picks **To store** / **To marketplace**. The store dropdown lists active shops from the **Stores** app. Once a store is picked, the same first-name / last-name / phone trio becomes required.

When the Stores app is installed and active, the merchant gets this store-selector so they can attribute this manual order to a specific physical / virtual location (e.g., a chain with multiple physical locations sharing one platform admin). The order's `shop_id` is set accordingly. The store's related shipping address gets a `marketplace_id` reference linking the order to that store.

## Settings & fields

| Field | Required when | Error message |
|---|---|---|
| **Delivery to** (radio) | When customer is selected | *"Please pick a delivery type"* |
| **Office ID** (`office_id`) | Delivery-to = office | *"Please select an office"* |
| **Locker ID** (`locker_id`) | Delivery-to = locker | *"Please select an office"* (locker is merged into office_id pre-validation — see [[orders-add-validation-save]]) |
| **Address ID** | Delivery-to = address | *"Please select an address"* |
| **Store ID** (`store_id`) | Delivery-to = marketplace | *"Please select a store"* |
| **First name / Last name / Phone** | Delivery-to = office, locker or marketplace | Field-level required |

The full validation table including the office-code parsing fallback is on [[orders-add-validation-save]].

## Business rules

### `$types` is dynamic — radios appear only when supported

The `address` radio is always present. The other three are inspected from the installed shipping integrations + the Stores app at page load — so a store with no pickup-capable courier installed will see only **To address** and (if the app is installed) **To store**.

### Office code carries the courier prefix

The picked office or locker's ID is shaped `<courier>-<office-code>` (e.g., `econt-1234`). The save endpoint parses the courier prefix to look up the courier and validate the office through that courier's API — see [[orders-add-validation-save]].

### Auto-creates a shipping provider on draft (verified)

For pickup orders (office / locker / marketplace), the platform automatically attaches the matching shipping provider record to the draft on step-1 save. The merchant doesn't pick a courier separately — it's inferred from the office prefix or store selection.

For address delivery, **no shipping provider is attached** at this step; the merchant configures shipping later on [[orders-details]].

### Side `side` flag is set from shipping provider

The order's meta `side` (payer side: sender vs receiver) is auto-set from the shipping provider's default config. For address delivery (no provider attached yet), the default is `PAYER_RECEIVER`.

### Auto-creates a saved address on customer's profile

For `office`, `locker`, and `marketplace`, the captured pickup-point details are saved as a new entry in the customer's saved-addresses list. See [[orders-add-address-handling]].

## Related

- [[orders-add]] — hub.
- [[orders-add-wizard]] — panel layout regions hosting the radio block.
- [[orders-add-address-handling]] — what the **Add new address** link opens for `address` mode + saved-address side effects for pickup modes.
- [[orders-add-validation-save]] — full validation table; office-code parsing; locker→office_id pre-validation.
- [[orders-details]] — where the merchant configures shipping for address-delivery orders in step 2.
- [[customers-details-shipping-addresses]] — saved-addresses list updated as a side effect of pickup-mode saves.

## Open questions

None.
