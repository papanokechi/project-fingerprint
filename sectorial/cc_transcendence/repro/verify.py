#!/usr/bin/env python3
"""EBR-III reproducibility verifier.

One-command audit of the /repro package. Run from the repro/ directory:

    python verify.py            # verify against HASH_MANIFEST.json
    python verify.py --write    # (re)generate HASH_MANIFEST.json

What it checks:
  * file SHA-256 of every script, report, Lean source, the paper .tex/.pdf,
    and the claims-ledger snapshot, against HASH_MANIFEST.json;
  * for every results JSON, recomputes the canonical SHA-256 of the
    hash-free object and confirms it equals the hash embedded in the file
    (self-consistency of each frozen artifact).

Exit code 0 iff every check passes.
"""
import json
import hashlib
import glob
import os
import sys

HASHKEYS = [
    "canonical_sha256_of_hashfree_object",
    "canonical_sha256",
    "sha256",
]

# The corpus is heterogeneous: the earliest artifact (cc1) canonicalizes with
# compact separators, a trailing newline, and a run-sensitive key exclusion;
# the later artifacts strip only the hash key and use default separators with
# no trailing newline. verify.py tries each known recipe and accepts the first
# that reproduces the embedded hash, reporting which recipe matched.
_RUN_SENSITIVE = {
    "HERE", "abspath", "absolute_path", "timestamp", "cwd", "_path",
    "timestamp_utc", "generated", "date", "host", "hostname",
}

# (exclude_run_sensitive, separators, trailing_newline, label)
_RECIPES = [
    (False, (", ", ": "), False, "default-seps/no-nl/strip-hashkey"),
    (True, (",", ":"), True, "compact-seps/nl/strip-run-sensitive"),
    (True, (",", ":"), False, "compact-seps/no-nl/strip-run-sensitive"),
    (False, (",", ":"), True, "compact-seps/nl/strip-hashkey"),
    (True, (", ", ": "), False, "default-seps/no-nl/strip-run-sensitive"),
]


def file_sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def match_self_hash(obj, hashkey):
    """Return (matched_label, recomputed) for the first recipe that reproduces
    the embedded hash, else (None, recomputed_under_first_recipe)."""
    embedded = obj[hashkey].lower()
    first = None
    for excl_rs, seps, nl, label in _RECIPES:
        drop = {hashkey} | (_RUN_SENSITIVE if excl_rs else set())
        stripped = {k: v for k, v in obj.items() if k not in drop}
        txt = json.dumps(stripped, sort_keys=True, ensure_ascii=False,
                         separators=seps, default=str)
        if nl:
            txt += "\n"
        got = hashlib.sha256(txt.encode("utf-8")).hexdigest()
        if first is None:
            first = got
        if got.lower() == embedded:
            return label, got
    return None, first


def build_manifest():
    m = {"scripts": {}, "results": {}, "reports": {}, "lean": {},
         "paper": {}, "ledger": {}}
    for p in sorted(glob.glob("scripts/*.py")):
        m["scripts"][os.path.basename(p)] = file_sha(p)
    for p in sorted(glob.glob("reports/*.md")):
        m["reports"][os.path.basename(p)] = file_sha(p)
    for p in sorted(glob.glob("lean/cc4_cores/*")):
        if os.path.isfile(p):
            m["lean"][os.path.basename(p)] = file_sha(p)
    for p in ["paper/ebr3_v1.tex", "paper/ebr3_v1.pdf"]:
        if os.path.exists(p):
            m["paper"][os.path.basename(p)] = file_sha(p)
    if os.path.exists("claims_cc.jsonl"):
        m["ledger"]["claims_cc.jsonl"] = file_sha("claims_cc.jsonl")
    for p in sorted(glob.glob("results/*.json")):
        name = os.path.basename(p)
        obj = json.load(open(p, encoding="utf-8"))
        entry = {"file_sha256": file_sha(p)}
        hk = next((k for k in HASHKEYS if isinstance(obj, dict) and k in obj),
                  None)
        if hk:
            label, recomputed = match_self_hash(obj, hk)
            entry["self_hash_key"] = hk
            entry["embedded"] = obj[hk]
            entry["recomputed_hashfree"] = recomputed
            entry["matched_recipe"] = label
        m["results"][name] = entry
    return m


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    write = "--write" in sys.argv
    here = os.path.dirname(os.path.abspath(__file__))
    os.chdir(here)
    m = build_manifest()

    if write:
        json.dump(m, open("HASH_MANIFEST.json", "w", encoding="utf-8"),
                  indent=2, sort_keys=True, ensure_ascii=False)
        print("wrote HASH_MANIFEST.json")
        return 0

    if not os.path.exists("HASH_MANIFEST.json"):
        print("HASH_MANIFEST.json missing; run: python verify.py --write")
        return 2
    expected = json.load(open("HASH_MANIFEST.json", encoding="utf-8"))

    failures = 0
    # 1) embedded self-hash consistency of each results JSON
    print("== results-JSON embedded self-hash consistency ==")
    for name, entry in sorted(m["results"].items()):
        if "embedded" in entry:
            ok = entry.get("matched_recipe") is not None
            tag = "PASS" if ok else "FAIL"
            recipe = entry.get("matched_recipe") or "NO-RECIPE-MATCHED"
            print(f"  {tag}  {name}  [{entry['self_hash_key']}]  ({recipe})")
            if not ok:
                failures += 1
        else:
            print(f"  ----  {name}  (no embedded hash)")

    # 2) file hashes vs manifest
    print("== file SHA-256 vs HASH_MANIFEST.json ==")
    for section in ("scripts", "reports", "lean", "paper", "ledger"):
        for name, sha in sorted(m[section].items()):
            exp = expected.get(section, {}).get(name)
            ok = (exp is not None and exp.lower() == sha.lower())
            if not ok:
                print(f"  FAIL  {section}/{name}")
                failures += 1
    for name, entry in sorted(m["results"].items()):
        exp = expected.get("results", {}).get(name, {}).get("file_sha256")
        ok = (exp is not None and exp.lower() == entry["file_sha256"].lower())
        if not ok:
            print(f"  FAIL  results/{name}")
            failures += 1
    if failures == 0:
        print("  all file hashes match the manifest")

    print(f"\n{'ALL CHECKS PASS' if failures == 0 else str(failures)+' FAILURE(S)'}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
