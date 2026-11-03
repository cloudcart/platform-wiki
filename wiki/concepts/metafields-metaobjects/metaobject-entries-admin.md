---
type: concept
nav_path: "Settings → Metaobjects → a metaobject definition → Entries"
route_name: metafields.entries
route_path: /admin/settings/metafields/metaobjects/:definitionId/entries, /admin/settings/metafields/metaobjects/:definitionId/entries/new, /admin/settings/metafields/metaobjects/:definitionId/entries/:entryId
aliases: ["Metaobject entries list", "Entries list", "Add entry", "Delete entries", "Delete entry", "Used in", "Used in card", "And more", "Not used yet", "Its references are removed from", "Unnamed entries", "Списък със записи на метаобект", "Добавяне на запис", "Изтриване на записи", "Къде се използва запис"]
tags: [metaobjects, custom-data, entries, admin, concepts]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 5
---

# Metaobject entries in the admin

> Part of [[metafields-metaobjects]]. What a definition and an entry are is in [[metaobjects-definitions]].

## Definition

Each metaobject definition has an **entries list**, where its entries are found, added and deleted, and each entry has its own **page**, where its fields are edited and its **Used in** card shows what points to it.

To reach the list: Settings → Metaobjects → click a metaobject definition under *Metaobject definitions*. It needs the **Metaobjects** permission. Someone who holds only the definitions permission opens the definition's page instead ([[metafields-permissions]]). The list's header has *Add entry*, and *Edit definition* for whoever may change definitions.

## Scope

### Columns

| Column | What it shows | Sorts |
|---|---|---|
| **Display name** | The entry's name, with its handle under it. Opens the entry. An unnamed entry shows as *"<definition name> #<id>"*. | yes |
| Every other field | One column per field, in the fields' order. | no |
| **Status** | *Active* or *Draft*, with the definition's active-draft status. *Deleting…* while a bulk delete runs. | no |
| **Updated** | The last update, in the store's time zone and formats. | yes |

The default order is **last updated first**, so a new entry is on top. In display-name order, unnamed entries come after the named, in both directions. The Admin GraphQL `metaobjects(sortKey: "display_name")` orders them the same way.

### What a cell holds

A cell is one line of text, cut by the column's width, with the whole line in its tooltip. The row carries a value's first 256 characters, and a longer value ends with "…".

| Value | Shown as |
|---|---|
| A list | Its items joined with ", " |
| A reference or a file | By name, or *"It no longer exists"* |
| True or false | *True* or *False* |
| Date, date and time | In the store's formats and time zone |
| Money | With the store's sign. An amount in another currency has its code beside it ([[metafields-types]]). |
| Measurement | With its unit in the admin's language |
| Rating | Its value and the top of its scale, `4.5 / 5` |
| Link | Its text and address, `Care guide (https://…)` |
| Multi-line and rich text | As plain text on one line |
| Colour | Its code with a swatch |

### Search and filter

- **Search** finds a display name by its start, in any case, or an entry by its exact handle.
- **Unnamed entries** are found by a start of "<definition name> #", and by their id's digits after it.
- **Status filter**: *Active* or *Draft*, with the active-draft status.

Search, filter, sort and page stay in the page's address.

### Adding and saving

- **New entry**: *Add entry*, then the save toasts *"«{name}» is added."* and **returns to the list**. A new entry sends every field.
- **Saved entry**: the page's save bar sends only the fields that differ from the stored entry, and only those are checked. A value flagged invalid, or a reference to a deleted record, does not hold back a save of the other fields. Given again, it is refused.
- **Required fields** are required in drafts too: *"A value is required, in a draft too."*
- The page has a **Handle** card (*"Unique among the definition's entries: letters, digits and -. The old handle is not kept."*) and, with the active-draft status, a **Status** card.

How each type is entered is in [[metafields-value-inputs]].

### Used in

The **Used in** card is on a saved entry's page. It lists the **first 50 references**, each owner once, in the order products, customers, categories, entries.

It shows the owner types the admin may read:

| Owner | Needs | Opens |
|---|---|---|
| Other entries | The entries permission the page already needs | That entry's page |
| Products | Products, or Products → Products | The product's editor (`/admin/products/edit/:id`) |
| Customers | Customers | The customer's page |
| Categories | Products, or Products → Categories | The categories list, searched by the category's name |

A record that is gone shows *"It no longer exists"*. Its other texts are:

- *"And more."*: there are references past the 50, or on owners the admin may not read.
- *"Used only where you may not open it."*
- *"Not used yet."*

### Deleting

| Action | Confirmation | Then |
|---|---|---|
| **Delete entry**, on its page | *"Delete «{name}»?"*, then *"Its references are removed from:"* with a line per owner type and its count, or *"It is not used anywhere."*, then *"This can't be undone."* | Toast *"«{name}» is deleted."*, back to the list |
| **Delete entries**, the list's bulk action | *"Delete {count} entries?"*, *"{count} entries are deleted."*, *"Their references are removed from:"* with counts, or *"They are not used anywhere."*, then *"The entries are deleted in the background. This can't be undone."* | Toast *"{count} entries are being deleted in the background."*; rows show *Deleting…* until the job has run |

The confirmation reads its counts when it opens, and *Delete* waits for them. If they cannot be read it says so and *Delete* stays disabled. What a deletion does to references is in [[metaobjects-definitions]].

## Contrasts

- **Used in vs the delete confirmation**: the card counts nothing and lists what the admin may read. The confirmation counts every owner type.
- **The list's search vs the API's `query:`**: the list's search is plain text. The Admin GraphQL and Storefront API lists take a query language, by field ([[metafields-search-syntax]]).

## Where it applies

- **Settings → Metaobjects → a definition → Entries** (route `metafields.entries`) and each entry's page (route `metafields.entry`, new `metafields.entry.create`).
- The same entries through the API: [[metafields-admin-api]].
- [[metafields-limits]]: up to 1,000,000 entries per definition, 250 per batch deletion.

## Related

- [[metafields-metaobjects]]: hub.
- [[metaobjects-definitions]]: the definition, its fields, handles and status.
- [[metafields-permissions]]: who reads and changes entries.
- [[metafields-value-inputs]]: the inputs on an entry's page.

## Open Questions

- None known.
