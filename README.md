# CloudCart platform wiki

A structured knowledge base of the [CloudCart](https://cloudcart.com) e-commerce platform, written to be **navigated by an LLM**: every admin-panel screen, the data model behind it, the cross-cutting concepts, the JSON API v2 resources, and the customer-facing storefront pages.

~2500 pages. Each covers one thing, states where to find it in the admin panel, what every control does, and the rules that change the outcome.

## Using it

```
wiki/index.md               start here — a compact map, one line per entry
skills/cloudcart-wiki/      the protocol for answering from the wiki
```

Point an assistant at `skills/cloudcart-wiki/SKILL.md` and it will know how to navigate: read the map, pick a hub, follow the `[[wikilinks]]` to the specific page, and cover every dimension the question touches.

The wiki is **not** meant to be read front to back, and not to be grepped at random. The map is the entry point; feature pages are reached through their admin-area hub, so any page is about two hops away.

## Layout

| Folder | What is in it |
|---|---|
| `wiki/features/` | one page per admin-panel screen |
| `wiki/entities/` | the merchant-visible data model — Product, Order, Customer, Plan, App… |
| `wiki/concepts/` | cross-cutting behaviour — checkout flow, inventory tracking, plan gates… |
| `wiki/api-resources/` | JSON API v2 resources |
| `wiki/storefront/` | the public pages a shopper sees |
| `wiki/resources/` | reference material (regulation extracts, schemas, samples) |

Page conventions — frontmatter fields, section structure, what `(verify)` means — are documented in the skill.

## What this copy is

This is a **public, redacted** copy of an internal wiki. Pages describing security mechanics, platform infrastructure and staff-only tooling were removed or rewritten; internal source references, ticket ids and technology names were stripped.

Merchant-facing behaviour is unchanged. Where a page reads as though something was left out, it was — and it was left out on purpose.

The redaction is reproducible rather than hand-applied: `tools/build.py` derives this tree from the internal one, and `tools/scan.py` re-checks the result against a set of leak rules and refuses to pass if any of them still match.

```bash
python3 tools/scan.py wiki --gate     # verify this tree is clean
```

## Accuracy

Pages are written against the platform's actual behaviour, but the platform changes. A claim marked `(verify)` was not confirmed against a running system — treat it as provisional. Anything else may still have drifted since its `updated` date.

This is documentation, not a contract: it describes how the platform behaves, not what CloudCart guarantees it will keep doing.
