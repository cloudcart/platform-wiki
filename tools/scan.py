#!/usr/bin/env python3
"""
scan.py — leak detector for the public wiki.

Runs over every markdown file and reports which sensitivity rules it trips.
Used twice:

  1. As a TRIAGE pass over the private wiki, to decide what to exclude,
     what to sanitise, and what is safe to copy verbatim.
  2. As a GATE over the produced public wiki. Any hit there is a failure —
     the publish must not proceed.

Usage:
    scan.py <wiki-root> [--gate] [--only RULE] [--files] [--context]
"""

import argparse
import json
import pathlib
import re
import sys
from collections import Counter, defaultdict

# Each rule: (id, severity, compiled regex, human description)
# Severity: BLOCK  = must never appear publicly
#           STRIP  = mechanical removal / rewrite
#           REVIEW = needs a judgement call
RULES = [
    # ---------------------------------------------------------------- BLOCK
    # Scoped to identity/session material. An ad pixel's dedup `event_id`
    # (md5 of cart + product ids) matched the earlier pattern but grants no
    # access — it only lets the ad network collapse duplicate events.
    ("auth-token-derivation", "BLOCK",
     r"md5\s*\(\s*(?:customer|user)_?id|login-by-code|\bsign-?in\b.{0,20}hash|"
     r"MD5\(concat", "token/hash derivation for an auth or identity flow"),

    # Narrowed deliberately. An earlier, broader version matched "read-only
    # authors" (inside "only auth") and every "no audit log" note. Those are
    # merchant-relevant compliance facts that need admin access to exploit —
    # unlike the cases below, which weaken authentication itself.
    ("auth-control-missing", "BLOCK",
     r"(?:hash|token|URL|link) is the only auth|no self-expiry|"
     r"referer check|DISABLED in production|CORS-permissive|"
     r"no origin restriction|"
     r"anyone with the (?:link|URL) can (?:sign in|re-render|access|use)",
     "a weakened or bypassable authentication control"),

    ("public-ip", "BLOCK",
     r"\b(?!10\.|127\.|192\.168\.|172\.(?:1[6-9]|2\d|3[01])\.|0\.0\.0\.0|255\.)"
     r"(?:\d{1,3}\.){3}\d{1,3}\b", "a routable IP address"),

    # Per-plan API caps are printed in the merchant's own admin banner, so
    # they are not secret. What must not ship is the edge protection map:
    # the anti-abuse layers, their thresholds, and the internal tier ladder.
    ("edge-threshold", "BLOCK",
     r"credential[- ]stuffing|per-IP flood|bot limit|throttle key|"
     r"rate[- ]limit bypass|admin-panel per-IP|"
     r"partner / employee tier|demo tier at", "edge protection internals"),

    ("secret-material", "BLOCK",
     r"BEGIN (?:RSA|OPENSSH|PRIVATE)|Bearer\s+[A-Za-z0-9_\-]{20,}|"
     r"\b[A-Fa-f0-9]{32,}\b", "key material or a long opaque token"),

    # Only password policy counts. Field-length validation (names, titles)
    # is ordinary merchant-facing documentation.
    ("credential-policy", "REVIEW",
     r"[Pp]assword[^.\n]{0,40}\d+\s*-\s*\d+\s*chars?",
     "an exact password-length policy"),

    # ---------------------------------------------------------------- STRIP
    ("source-path", "STRIP",
     r"\b(?:app|modules|resources|routes|themes|database|config|public)/"
     r"[A-Za-z0-9_/.\-]+\.(?:php|tpl|vue|js|blade)\b", "an internal source path"),

    ("php-symbol", "STRIP",
     r"\b[A-Z][A-Za-z0-9]*::(?:class\b|[a-zA-Z][A-Za-z0-9]*\s*\()|"
     r"\b[A-Z][A-Za-z0-9]*(?:Controller|Job|Listener|Subscriber|Middleware|"
     r"Repository|Formatter|Resolver|Seeder)\b|"
     r"`(?!parent::child`)(?!global::`)[^`\n]*[A-Za-z]::[A-Za-z_][^`\n]*`|"
     r"`[A-Z][A-Za-z]*(?:Request|Exception|NotFound|DeniedByPlan)`",
     "a class / job / controller name"),

    ("infra-name", "STRIP",
     r"\b(?:base6|lb6|HAProxy|haproxy|imgproxy|Typesense|typesense|"
     r"Elasticsearch|elasticsearch|MongoDB|mongodb|RabbitMQ|Memcached|"
     r"ClickHouse|Laravel|Eloquent|Blade|Docker|docker)\b",
     "an internal technology or host name"),

    ("internal-ticket", "STRIP",
     r"\bDIN-\d+|\bFreshdesk\b|\bfreshdesk\b", "an internal tracker reference"),

    ("partner-contact", "STRIP",
     r"[A-Za-z0-9._%+\-]+@(?:dskbank|klearlending|postbank|unicreditbulbank|"
     r"tbibank|mypos|newpay)\.[a-z.]+", "a partner's operational mailbox"),

    # --------------------------------------------------------------- REVIEW
    ("staff-only", "REVIEW",
     r"staff[- ]only|CloudCart staff|CloudCart employees|support command|"
     r"merchants cannot trigger|not exposed to merchants|internal tool|"
     r"platform-internal", "staff-only tooling or internal mechanics"),

    ("client-theme", "REVIEW",
     r"\bzora[- ]?new\b|\bknowledge-tmarket\b|\bsummer-sfa\b|\bmotivation-[a-z]+\b",
     "a named client's theme"),

    ("disabled-code", "REVIEW",
     r"commented[- ]out|commented out|no-?op\b|wired up but|reachable by direct URL",
     "dead or hidden code paths"),

    ("unverified", "REVIEW",
     r"\(verify\b", "an unverified claim"),

    ("known-issue", "REVIEW",
     r"^#{2,4}\s*Known issues|\bby-design vs bug\b", "a known-issues section"),
]

COMPILED = [(rid, sev, re.compile(pat, re.M), desc) for rid, sev, pat, desc in RULES]


def scan_text(text):
    """Return {rule_id: [(lineno, line)]} for every rule the text trips."""
    hits = defaultdict(list)
    lines = text.splitlines()
    for rid, _sev, rx, _desc in COMPILED:
        for m in rx.finditer(text):
            lineno = text.count("\n", 0, m.start()) + 1
            line = lines[lineno - 1].strip() if lineno <= len(lines) else ""
            hits[rid].append((lineno, line))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--gate", action="store_true",
                    help="exit non-zero if anything is found")
    ap.add_argument("--only", help="restrict to one rule id")
    ap.add_argument("--files", action="store_true",
                    help="list matching file paths only")
    ap.add_argument("--context", action="store_true",
                    help="print the matched lines")
    ap.add_argument("--severity", help="restrict to one severity")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    root = pathlib.Path(args.root)
    sev_of = {rid: sev for rid, sev, _, _ in RULES}
    desc_of = {rid: desc for rid, _, _, desc in RULES}

    per_file = {}
    counts = Counter()
    files_per_rule = Counter()

    for path in sorted(root.rglob("*.md")):
        hits = scan_text(path.read_text(encoding="utf-8", errors="replace"))
        if args.only:
            hits = {k: v for k, v in hits.items() if k == args.only}
        if args.severity:
            hits = {k: v for k, v in hits.items()
                    if sev_of[k] == args.severity}
        if not hits:
            continue
        rel = str(path.relative_to(root))
        per_file[rel] = hits
        for rid, occ in hits.items():
            counts[rid] += len(occ)
            files_per_rule[rid] += 1

    if args.json:
        print(json.dumps({f: {k: v for k, v in h.items()}
                          for f, h in per_file.items()}, indent=1))
    elif args.files:
        for f in per_file:
            print(f)
    elif args.context:
        for f, hits in per_file.items():
            print(f"\n=== {f}")
            for rid, occ in sorted(hits.items()):
                for lineno, line in occ[:4]:
                    print(f"  [{sev_of[rid]}/{rid}] :{lineno} {line[:150]}")
    else:
        total = len(list(root.rglob("*.md")))
        print(f"scanned {total} files, {len(per_file)} tripped a rule\n")
        print(f"{'SEV':<7} {'RULE':<24} {'FILES':>6} {'HITS':>7}  WHAT")
        for rid, _sev, _rx, _d in COMPILED:
            if files_per_rule[rid]:
                print(f"{sev_of[rid]:<7} {rid:<24} {files_per_rule[rid]:>6} "
                      f"{counts[rid]:>7}  {desc_of[rid]}")

    if args.gate and per_file:
        print(f"\nGATE FAILED — {len(per_file)} files still contain "
              f"material that must not be published.", file=sys.stderr)
        return 1
    if args.gate:
        print("GATE PASSED — no rule tripped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
