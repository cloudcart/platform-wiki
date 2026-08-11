#!/usr/bin/env python3
"""
build.py — produce the public wiki from the private one.

Every page is either EXCLUDED, REWRITTEN or COPIED. Nothing reaches the
output without passing through one of those three paths, and the result is
verified by tools/scan.py --gate.

Usage:
    build.py <private-wiki-root> <public-wiki-root>
"""

import pathlib
import re
import shutil
import sys
from collections import Counter

# --------------------------------------------------------------------------
# 1. EXCLUSIONS — pages whose subject matter is itself the problem.
#    Each carries the reason it cannot be published.
# --------------------------------------------------------------------------
EXCLUDE = {
    "log.md":
        "internal ingest/operation history — names the codebase, tickets and staff workflow",
    "features/customers-sign-in/customers-sign-in-redirect.md":
        "publishes the impersonation token derivation and its endpoint",
    "features/customers-sign-in/customers-sign-in-security.md":
        "publishes the disabled referer guard, the absent audit trail and the token's non-expiry",
    "features/analytics-pipeline/analytics-backfill-commands.md":
        "staff-only repair commands",
    "features/apps-advanced-search/apps-advanced-search-support.md":
        "staff-only diagnostic commands",
}

EXCLUDE_DIRS = {"templates", ".obsidian"}
EXCLUDE_GLOBS = ["Untitled*.md"]

# --------------------------------------------------------------------------
# 2. RENAMES — a page whose *filename* leaks infrastructure.
# --------------------------------------------------------------------------
RENAMES = {
    "concepts/lb6-haproxy-limits.md": "concepts/platform-rate-limits.md",
    "concepts/background-queue-inventory/background-queue-elasticsearch-sync.md":
        "concepts/background-queue-inventory/background-queue-search-sync.md",
    "concepts/storefront-architecture/storefront-arch-elasticsearch-read-side.md":
        "concepts/storefront-architecture/storefront-arch-search-read-side.md",
    "entities/queue-job/queue-job-mongodb-storage.md":
        "entities/queue-job/queue-job-storage.md",
}
STEM_RENAMES = {
    "lb6-haproxy-limits": "platform-rate-limits",
    "background-queue-elasticsearch-sync": "background-queue-search-sync",
    "storefront-arch-elasticsearch-read-side": "storefront-arch-search-read-side",
    "queue-job-mongodb-storage": "queue-job-storage",
}

# Wikilinks pointing at an excluded page are degraded to plain text.
DEAD_STEMS = {
    "customers-sign-in-redirect", "customers-sign-in-security",
    "analytics-backfill-commands", "apps-advanced-search-support",
}

# --------------------------------------------------------------------------
# 3. FRONTMATTER — fields that exist only to point at source files.
# --------------------------------------------------------------------------
FM_DROP = {"template_path", "shared_template", "component"}

# --------------------------------------------------------------------------
# 4. TEXT SUBSTITUTIONS — applied to every page that survives.
# --------------------------------------------------------------------------
SUBS = [
    # -- routable IP + the person it is attributed to ----------------------
    (r"`?195\.42\.143\.112`?", "a platform-internal address"),
    (r'Documented as "api importer \([A-Z][a-z]+\)" in the code; used by '
     r"CloudCart's internal data importer for analytics\.\s*", ""),

    # -- internal tracker ids ---------------------------------------------
    (r"\s*\(DIN-\d+\)", ""),
    (r"\bDIN-\d+\s+", ""),
    (r"\bthe DIN-\d+\b", "the"),
    (r"\bDIN-\d+\b", ""),
    (r"\bFreshdesk\b", "a support ticket"),

    # -- infrastructure and internal technology ---------------------------
    (r"\bHAProxy LB6\b|\bLB6 \(HAProxy\)\b|\bHAProxy\b|\bhaproxy\b|\bLB6\b|\blb6\b",
     "the platform edge"),
    (r"\bElasticsearch\b|\belasticsearch\b", "the search index"),
    (r"\bTypesense\b|\btypesense\b", "the search engine"),
    (r"\bimgproxy\b", "the image delivery service"),
    (r"\bMongoDB\b|\bmongodb\b", "the analytics store"),
    (r"\bRabbitMQ\b|\bMemcached\b|\bClickHouse\b", "the platform queue"),
    (r"\bbase6\b", "the platform codebase"),
    (r"\b(?:Laravel|Eloquent|Blade)\b", "the application framework"),

    # -- partner operational mailboxes ------------------------------------
    (r"[A-Za-z0-9._%+\-]+@(?:dskbank|klearlending|postbank|unicreditbulbank|"
     r"tbibank|mypos|newpay)\.[a-z.]+", "the provider's support address"),

    # -- internal source paths --------------------------------------------
    (r"`(?:app|modules|resources|routes|database|config|public)/"
     r"[A-Za-z0-9_/.\-]+\.(?:php|vue|js|blade)(?::\d+)?`", "the platform code"),
    (r"\s*Verified \d{4}-\d{2}-\d{2} against the platform code\.", ""),
    (r"(?<!`)\b(?:app|modules|resources|routes|database|config)/"
     r"[A-Za-z0-9_/.\-]+\.(?:php|vue|js|blade)\b", "the platform code"),

    # -- class / job / controller symbols ---------------------------------
    # These must precede the generic *Controller rule below, otherwise the
    # class name inside them is rewritten first and leaves debris such as
    # "Site\\Customer\\the platform code@register".
    (r"`?\b[A-Z][A-Za-z0-9]*(?:\\[A-Z][A-Za-z0-9]*)*@[a-zA-Z][A-Za-z0-9]*`?",
     "the request handler"),
    (r"\{include file=View::path\('[^']*'\)\}", "the shared layout include"),
    (r"`?\bView::(?:exists|path|panel|modal)\('?[^')]*'?\)`?",
     "a view lookup"),
    (r"`[A-Z][A-Za-z0-9]*::[a-zA-Z][A-Za-z0-9]*\(\)`", "the platform code"),
    (r"`[A-Z][A-Za-z0-9]*::class`", "the platform code"),
    (r"`[A-Z][A-Za-z0-9]*(?:Controller|Job|Listener|Subscriber|Middleware|"
     r"Repository|Formatter|Resolver|Seeder)`", "the platform code"),
    (r"\b[A-Z][A-Za-z0-9]*(?:Controller|Job|Listener|Subscriber|Middleware|"
     r"Repository|Formatter|Seeder)\b", "the platform code"),

    # -- remaining application symbols -------------------------------------
    # Say what the class MEANT, not just that code was removed: "throws the
    # platform code" is unreadable where "raises a not-found error" is not.
    (r"`[A-Z][A-Za-z]*NotFound`", "a not-found error"),
    (r"`[A-Z][A-Za-z]*DeniedByPlan`", "a plan-restriction error"),
    (r"`[A-Z][A-Za-z]*Exception`", "an error"),
    (r"`[A-Z][A-Za-z]*Request`", "the request validator"),

    # A class method with arguments — `Plan::canCreateByMap('x')`,
    # `Discount::whereType('y')->findOrFail()`. The earlier pattern only
    # caught the empty-parens form.
    (r"`[A-Z][A-Za-z0-9]*::[a-zA-Z][A-Za-z0-9]*\([^`]*`", "the platform code"),
    (r"`getMessage`", "the error text"),
    (r"`\\?[A-Z][A-Za-z0-9]*::[a-zA-Z][A-Za-z0-9]*\([^`]*\)[^`]*`",
     "the platform code"),
    (r"`\\?[A-Z][A-Za-z0-9]*(?:\\[A-Z][A-Za-z0-9]*)+`", "the platform code"),
    (r"`max\([^`]*\)`|`filemtime\([^`]*\)`|`hasOne\([^`]*\)`",
     "the platform code"),
    (r"`themes/<theme>/[A-Za-z0-9_/.\-]+`", "the theme's own override"),

    # Catch-all for any remaining backticked span carrying a PHP scope
    # resolution — class constants, static calls, namespaced helpers. The
    # shape-by-shape rules above missed roughly 180 of these. Two spellings
    # are domain vocabulary rather than code and are kept: `parent::child`
    # (category nesting) and Smarty's `global::` template namespace.
    (r"`(?!parent::child`)(?!global::`)[^`\n]*[A-Za-z]::[A-Za-z_][^`\n]*`",
     "the platform code"),

    # Template and source paths alike. Theme files are not reachable by the
    # merchant's own developers, so naming them helps nobody outside.
    (r"`(?:themes|modules|app|resources|routes|config|public|database)/"
     r"[A-Za-z0-9_/.\-]+`", "the theme templates"),
    (r"\(From the theme templates\.\)\s*", ""),
    (r"\((?:the theme templates)\)", ""),
    (r"\bShippingProvider\b", "shipping provider"),
    (r"\bPaymentProvider\b", "payment provider"),
    (r"\bSiteResolver\b", "the store resolver"),

    # -- named client themes ----------------------------------------------
    # These identify real merchants by name. The list has no public value:
    # what matters is that support for the page is theme-dependent.
    (r"\(observed in `zora-new`[^)]*\)", "(theme-dependent)"),
    (r"observed in `zora-new`", "observed on themes that ship it"),
    (r"`zora-new`'s", "such a theme's"),
    (r"`zora-new`", "a theme that ships it"),
    (r"`knowledge-tmarket`|`summer-sfa`|`motivation-[a-z]+`|`mdl`",
     "another custom theme"),

    # -- abbreviations and event names the patterns above do not reach -----
    (r"\bES sync\b", "search-index sync"),
    (r"\bES queue\b", "search-index queue"),
    (r"\bES\b(?= (?:sync|index|queue|re-index))", "search-index"),
    (r"`ProductsSearchEnginesSync`", "the search re-index"),
    (r"`postThrottle:[\d,]+`", "a submission throttle"),

    # -- enumerations of the edge's protective layers ----------------------
    (r"terminates TLS, applies per-IP flood limits and bot detection",
     "terminates TLS and applies the platform's abuse protections"),
    (r"the general per-IP flood protection \(40 req/s — verify\)",
     "the platform's general abuse protection"),
    (r"\*\*5 submissions per 1 minute per IP\*\* via the a submission throttle "
     r"middleware", "a submission throttle"),
    (r"\bJIRA `IM-\d+`|\bIM-\d+\b", "an internal ticket"),
    (r" \(the throttle key combines IP \+ route name\)", ""),
    (r"edge enforcement, per-domain throttle key `sha1\(domain\)`, ",
     "edge enforcement, "),
    (r"\s*\(per an internal ticket in the code comment\)", ""),
    (r" — per-IP flood limits, crawler detection, cached fragments",
     " — TLS termination and cached fragments"),
    (r"\(TLS, flood limits, crawler detection\)",
     "(TLS termination and caching)"),
    (r"\bthe edge load balancer\b", "the platform edge"),

    # -- tidy up what the substitutions leave behind -----------------------
    # A replacement beginning with "the" can land after an indefinite
    # article ("a Typesense re-index" -> "a the search engine re-index").
    (r"\b([Aa]n?) (the )", r"\2"),
    # NB: these must never touch line structure. Blank lines carry markdown
    # meaning (paragraphs, lists, tables) and leading spaces carry nesting,
    # so collapse only runs of spaces that follow visible text on a line.
    (r"\(\s*\)", ""),
    (r"\(\s*—\s*", "("),
    (r"(?<=\S) {2,}(?=\S)", " "),
    (r"(?<=\w) +([,.;:])", r"\1"),
    (r"[ \t]+\n", "\n"),
]
SUBS = [(re.compile(p), r) for p, r in SUBS]

# --------------------------------------------------------------------------
# 5. SECTION DROPS — a single heading inside an otherwise publishable page.
# --------------------------------------------------------------------------
SECTION_DROPS = {
    "features/settings-api-keys/settings-api-keys-rate-limits.md":
        ["Special-IP bypass"],
    "features/settings-pat-tokens.md":
        ["No brute-force throttle"],
    "features/marketing-buy-button/buy-button-embed-runtime.md":
        ["CORS"],
}

# --------------------------------------------------------------------------
# 6. LINE DROPS — a single sentence or bullet, where dropping the whole
#    section would take useful documentation with it.
# --------------------------------------------------------------------------
LINE_DROPS = {
    # The thank-you page is reachable by whoever holds its address, and it
    # carries the customer's order. Saying so publicly invites the attempt.
    "storefront/checkout-complete.md": ["Hash is the only auth"],
    # Names the exact throttle key, so it describes how the quota is scoped
    # and how it could be split — of no use to a merchant.
    "features/settings-api-keys/settings-api-keys-rate-limits.md":
        ["The throttle key is"],
    # Advertises an authentication route that is live but deliberately has
    # no UI — exactly the kind of thing not to point at from a public page.
    "storefront/customer-login.md":
        ["still exists — it is reachable by direct URL"],
}


def drop_sections(text, needles):
    """Remove any ###-level section whose heading contains one of `needles`."""
    out, skip_level = [], None
    for line in text.splitlines(keepends=True):
        m = re.match(r"^(#{2,6})\s+(.*)$", line)
        if m:
            level, title = len(m.group(1)), m.group(2)
            if skip_level is not None and level <= skip_level:
                skip_level = None
            if skip_level is None and any(n.lower() in title.lower()
                                          for n in needles):
                skip_level = level
                continue
        if skip_level is None:
            out.append(line)
    return "".join(out)


def strip_frontmatter_fields(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return text
    kept = [ln for ln in m.group(1).splitlines()
            if ln.split(":")[0].strip() not in FM_DROP]
    return "---\n" + "\n".join(kept) + "\n---\n" + m.group(2)


DEAD = "\x01"          # sentinel standing in for a link to an excluded page


def rewrite_links(text):
    def repl(m):
        stem, rest = m.group(1), m.group(2) or ""
        if stem in STEM_RENAMES:
            return f"[[{STEM_RENAMES[stem]}{rest}]]"
        if stem in DEAD_STEMS:
            return DEAD
        return m.group(0)
    return re.sub(r"\[\[([^\]|]+?)(\|[^\]]+)?\]\]", repl, text)


def prune_dead_references(text):
    """Remove what is left over once a link to an excluded page is gone.

    Degrading [[excluded-page]] to its bare words leaves sentences that
    point at documentation the reader cannot reach ("see customers sign in
    security"), and hub bullets advertising a page that no longer exists.
    Both are removed outright: a bullet that *starts* with the reference is
    dropped whole, otherwise the sentence containing it goes.
    """
    kept = []
    for line in text.splitlines():
        if DEAD not in line:
            kept.append(line)
            continue

        # A catalogue entry for a page that is not published.
        if re.match(rf"^\s*[-*]\s*{DEAD}", line):
            continue

        # A trailing item inside an enumeration of sibling links.
        line = re.sub(rf",\s*{DEAD}(?=\s*[.;]|$)", "", line)

        # Otherwise drop the sentence that carries the reference.
        parts = re.split(r"(?<=[.!?])\s+", line)
        parts = [p for p in parts if DEAD not in p]
        line = " ".join(parts).rstrip()

        # Whatever remains must not still carry the sentinel.
        line = line.replace(DEAD, "").rstrip()
        if line.strip() in {"", "-", "*", "- ", "—"}:
            continue
        kept.append(line)
    return "\n".join(kept) + ("\n" if text.endswith("\n") else "")


LINK_RX = re.compile(r"\[\[[^\]]+\]\]")

PHP_BLOCK = re.compile(r"```(\w*)\n(.*?)```", re.S)
PHP_MARKS = re.compile(r"<\?php|\b[A-Z][A-Za-z]*::|->[a-z]\w*\(|\$[a-z]\w*\s*=")


def strip_source_blocks(text):
    """Replace fenced blocks that are platform source with a plain note.

    JSON payloads, shell examples and template snippets are what an
    integrator needs and are kept; application code is not.
    """
    def repl(m):
        lang, body = m.group(1), m.group(2)
        if lang.lower() in {"json", "bash", "sh", "http", "yaml", "html", "css"}:
            return m.group(0)
        if PHP_MARKS.search(body):
            return "_(platform implementation detail omitted)_\n"
        return m.group(0)
    return PHP_BLOCK.sub(repl, text)


def transform(rel, text):
    text = strip_source_blocks(strip_frontmatter_fields(text))
    if rel in SECTION_DROPS:
        text = drop_sections(text, SECTION_DROPS[rel])
    if rel in LINE_DROPS:
        needles = LINE_DROPS[rel]
        text = "\n".join(ln for ln in text.splitlines()
                          if not any(n in ln for n in needles)) + "\n"

    # Wikilink targets are identifiers, not prose. Running the text
    # substitutions over them rewrote [[lb6-haproxy-limits]] into
    # [[the platform edge-the platform edge-limits]], so links are masked
    # out first and restored afterwards; renaming them is rewrite_links' job.
    shelf = []

    def stow(m):
        shelf.append(m.group(0))
        return f"\x00{len(shelf) - 1}\x00"

    text = LINK_RX.sub(stow, text)
    for rx, rep in SUBS:
        text = rx.sub(rep, text)
    text = re.sub(r"\x00(\d+)\x00", lambda m: shelf[int(m.group(1))], text)

    def sub_alias(m):
        target, alias = m.group(1), m.group(2)
        for rx, rep in SUBS:
            alias = rx.sub(rep, alias)
        return f"[[{target}|{alias}]]"

    text = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", sub_alias, text)

    # A substitution that lands after an article yields "The the platform
    # code"; collapse the duplicate while keeping the original casing.
    text = re.sub(r"\b(The|the) the\b", r"\1", text)

    return prune_dead_references(rewrite_links(text))


def main():
    src, dst = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])

    # The first thing main() does is wipe dst. Run with a relative src from
    # the public repo and both resolve to the same directory, which deletes
    # the input before a single page is read.
    src_r, dst_r = src.resolve(), dst.resolve()
    if src_r == dst_r or dst_r in src_r.parents:
        sys.exit(f"refusing to build: destination {dst_r} would erase the "
                 f"source {src_r}")
    if not (src_r / "index.md").exists():
        sys.exit(f"refusing to build: {src_r} does not look like a wiki root "
                 f"(no index.md)")

    # Pages whose sensitive parts are too tangled with useful content for a
    # regex to separate are hand-written once into tools/overrides/ and copied
    # over the generated version, so a rebuild never silently reinstates them.
    overrides = pathlib.Path(__file__).parent / "overrides"

    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)

    for rel in RENAMES:
        if not (src / rel).exists():
            sys.exit(f"rename source does not exist: {rel}")

    stats = Counter()
    for path in sorted(src.rglob("*")):
        if path.is_dir():
            continue
        rel = str(path.relative_to(src))
        parts = pathlib.Path(rel).parts

        if set(parts) & EXCLUDE_DIRS:
            stats["excluded_dir"] += 1
            continue
        if any(pathlib.Path(rel).match(g) for g in EXCLUDE_GLOBS):
            stats["excluded_glob"] += 1
            continue
        if rel in EXCLUDE:
            print(f"  EXCLUDE  {rel}\n           reason: {EXCLUDE[rel]}")
            stats["excluded_page"] += 1
            continue

        target = dst / RENAMES.get(rel, rel)
        target.parent.mkdir(parents=True, exist_ok=True)

        if path.suffix != ".md":
            shutil.copy2(path, target)
            stats["asset"] += 1
            continue

        original = path.read_text(encoding="utf-8", errors="replace")
        new = transform(rel, original)
        target.write_text(new, encoding="utf-8")
        stats["rewritten" if new != original else "copied"] += 1
        if rel in RENAMES:
            print(f"  RENAME   {rel}\n           -> {RENAMES[rel]}")

    if overrides.is_dir():
        for ov in sorted(overrides.rglob("*.md")):
            rel = ov.relative_to(overrides)
            target = dst / rel
            if not target.exists():
                print(f"  !! override has no generated counterpart: {rel}")
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ov, target)
            print(f"  OVERRIDE {rel}")
            stats["overridden"] += 1

    print("\n".join(f"{v:>6}  {k}" for k, v in sorted(stats.items())))
    print(f"{sum(stats.values()):>6}  total considered")


if __name__ == "__main__":
    main()
