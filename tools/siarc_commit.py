#!/usr/bin/env python3
"""siarc-commit -- gated commit/push tool.

Makes the prepare -> review -> execute boundary STRUCTURAL, not conventional.

Usage:
    python tools/siarc_commit.py <manifest> [--dry-run]

The agent (or operator) writes a MANIFEST declaring the exact files to commit,
the commit message, and the expected post-stage git status. This tool runs a
set of safety GATES; if all pass it prints the real diff and PAUSES for one
explicit typed confirmation. Only on the exact confirm token does it stage
exactly the declared files, re-verify, commit, and push.

There is deliberately NO way to commit/push without (a) all gates passing and
(b) an interactive confirmation that follows a printed diff. No --yes, no env
bypass, no --force. --dry-run does everything EXCEPT the confirm + push.

Manifest format (JSON or a small YAML subset):
    files:
      - path/relative/to/repo/root.json
      - another.md
    message: |
      commit message, may be multi-line
    expected_status:        # porcelain-ish code expected per file after staging
      path/relative/to/repo/root.json: M
      another.md: M
    branch: main            # optional

Pure standard library (subprocess + json). No third-party deps.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

CONFIRM_TOKEN = "CONFIRM"


# --------------------------------------------------------------------------
# git helpers
# --------------------------------------------------------------------------
def run_git(args, repo_root, env=None, text_input=None):
    """Run a git command; return (returncode, stdout, stderr)."""
    full_env = dict(os.environ)
    if env:
        full_env.update(env)
    proc = subprocess.run(
        ["git"] + args,
        cwd=repo_root,
        env=full_env,
        input=text_input,
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout, proc.stderr


def repo_toplevel(start):
    rc, out, _ = run_git(["rev-parse", "--show-toplevel"], start)
    if rc != 0:
        return None
    return out.strip()


def git_index_path(repo_root):
    rc, out, _ = run_git(["rev-parse", "--git-path", "index"], repo_root)
    if rc != 0:
        return None
    p = out.strip()
    if not os.path.isabs(p):
        p = os.path.join(repo_root, p)
    return p


def current_branch(repo_root):
    rc, out, _ = run_git(["rev-parse", "--abbrev-ref", "HEAD"], repo_root)
    return out.strip() if rc == 0 else None


def parse_name_status(text):
    """Parse `git diff --name-status` output into {path: CODE} (first letter)."""
    result = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        code = parts[0].strip()[:1].upper()
        if code in ("R", "C") and len(parts) >= 3:
            # rename/copy: report the destination path
            path = parts[2].strip()
        else:
            path = parts[-1].strip()
        result[path] = code
    return result


# --------------------------------------------------------------------------
# manifest loading
# --------------------------------------------------------------------------
def parse_simple_yaml(text):
    """Parse the documented YAML subset (files / message / expected_status /
    branch). Deliberately restricted; prefer JSON for anything fancier."""
    data = {"files": [], "message": "", "expected_status": {}}
    lines = text.splitlines()
    i = 0
    n = len(lines)
    while i < n:
        raw = lines[i]
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        # top-level keys begin at column 0
        if not raw[:1].isspace() and ":" in raw:
            key, _, inline = raw.partition(":")
            key = key.strip()
            inline = inline.strip()
            if key == "files":
                i += 1
                items = []
                while i < n and (lines[i].strip().startswith("- ")
                                 or lines[i].strip() == "-"):
                    items.append(lines[i].strip()[1:].strip())
                    i += 1
                data["files"] = [x for x in items if x]
                continue
            if key == "expected_status":
                i += 1
                mapping = {}
                while i < n and lines[i][:1].isspace() and ":" in lines[i] \
                        and not lines[i].strip().startswith("-"):
                    k, _, v = lines[i].strip().partition(":")
                    mapping[k.strip()] = v.strip()
                    i += 1
                data["expected_status"] = mapping
                continue
            if key == "message":
                if inline == "|" or inline == "":
                    i += 1
                    block = []
                    indent = None
                    while i < n and (lines[i].strip() == "" or lines[i][:1].isspace()):
                        if lines[i].strip() == "":
                            block.append("")
                            i += 1
                            continue
                        cur_indent = len(lines[i]) - len(lines[i].lstrip())
                        if indent is None:
                            indent = cur_indent
                        block.append(lines[i][indent:])
                        i += 1
                    while block and block[-1] == "":
                        block.pop()
                    data["message"] = "\n".join(block)
                    continue
                else:
                    data["message"] = inline
                    i += 1
                    continue
            if key == "branch":
                data["branch"] = inline
                i += 1
                continue
        i += 1
    return data


def load_manifest(path):
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    if path.lower().endswith(".json"):
        data = json.loads(text)
    else:
        # try JSON first (a .yaml that is actually JSON still works), else YAML
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            data = parse_simple_yaml(text)
    data.setdefault("files", [])
    data.setdefault("message", "")
    data.setdefault("expected_status", {})
    return data


# --------------------------------------------------------------------------
# dry staging into a throwaway index (side-effect free)
# --------------------------------------------------------------------------
def stage_into_temp_index(repo_root, files):
    """Copy the real index to a temp file, `git add` the declared files against
    it, and return (tmp_index_path, env, staged_name_status). Caller must remove
    the temp index. The real repo/index is never modified."""
    real_index = git_index_path(repo_root)
    fd, tmp_index = tempfile.mkstemp(prefix="siarc_idx_")
    os.close(fd)
    if real_index and os.path.exists(real_index):
        shutil.copyfile(real_index, tmp_index)
    else:
        os.remove(tmp_index)  # let git create a fresh one
    env = {"GIT_INDEX_FILE": tmp_index}
    add_args = ["add", "--"] + files
    run_git(add_args, repo_root, env=env)
    rc, out, _ = run_git(
        ["diff", "--cached", "--name-status"], repo_root, env=env
    )
    staged = parse_name_status(out)
    return tmp_index, env, staged


# --------------------------------------------------------------------------
# gates
# --------------------------------------------------------------------------
class GateResult:
    def __init__(self):
        self.failures = []
        self.warnings = []

    def fail(self, gate, msg):
        self.failures.append((gate, msg))

    def warn(self, gate, msg):
        self.warnings.append((gate, msg))

    @property
    def ok(self):
        return not self.failures


def run_gates(repo_root, manifest):
    res = GateResult()
    files = manifest.get("files", [])
    expected = manifest.get("expected_status", {})
    message = manifest.get("message", "")

    if not files:
        res.fail("G0", "manifest declares no files")
        return res, None, None

    # refuse if the real index is already dirty (would muddy the temp-index delta)
    rc, _, _ = run_git(["diff", "--cached", "--quiet"], repo_root)
    if rc != 0:
        res.fail(
            "G0",
            "the git index is not clean (something is already staged). "
            "Unstage first: `git reset HEAD` -- then re-run.",
        )
        return res, None, None

    # G1 declared-files-exist
    for f in files:
        if not os.path.exists(os.path.join(repo_root, f)):
            res.fail("G1", f"declared file does not exist on disk: {f}")

    # G4 json-parses (before staging; a broken canonical file must never reach
    # the index)
    for f in files:
        if f.lower().endswith(".json"):
            full = os.path.join(repo_root, f)
            if os.path.exists(full):
                try:
                    with open(full, "r", encoding="utf-8") as fh:
                        json.load(fh)
                except (json.JSONDecodeError, OSError) as exc:
                    res.fail("G4", f"declared JSON does not parse: {f} -- {exc}")

    # G6 message-nonempty / non-trivial
    msg_stripped = (message or "").strip()
    if len(msg_stripped) < 3 or not any(c.isalnum() for c in msg_stripped):
        res.fail("G6", "commit message is empty or trivial")

    # G7 branch-check (optional)
    if manifest.get("branch"):
        cur = current_branch(repo_root)
        if cur != manifest["branch"]:
            res.fail(
                "G7",
                f"branch mismatch: on '{cur}', manifest expects "
                f"'{manifest['branch']}'",
            )

    # If files are missing we cannot meaningfully dry-stage; bail so the
    # operator fixes G1 first.
    if any(g == "G1" for g, _ in res.failures):
        return res, None, None

    # dry-stage into a throwaway index for G2 / G3 and for the displayed diff
    tmp_index, env, staged = stage_into_temp_index(repo_root, files)

    declared_set = set(files)
    staged_set = set(staged.keys())

    # G3 diff-non-empty: every declared file must actually change
    for f in files:
        if f not in staged_set:
            res.fail(
                "G3",
                f"declared file has NO diff (silent no-op): {f} "
                "-- nothing would be committed for it",
            )

    # G2 status-matches: staged set EQUALS expected set, no more / no fewer,
    # codes match. (Over-staging is impossible since we add by name, but an
    # under-declared expected_status or a mismatched code fails here.)
    extra_staged = staged_set - set(expected.keys())
    for f in sorted(extra_staged):
        res.fail(
            "G2",
            f"file would be staged but is not in expected_status: {f} "
            "(manifest under-declares)",
        )
    missing_expected = set(expected.keys()) - staged_set
    for f in sorted(missing_expected):
        res.fail(
            "G2",
            f"expected_status lists {f} but it would not be staged "
            "(no change / not declared in files)",
        )
    for f in sorted(staged_set & set(expected.keys())):
        want = (expected.get(f) or "").strip()[:1].upper()
        got = staged.get(f, "")
        if want and want != got:
            res.fail(
                "G2",
                f"status code mismatch for {f}: expected '{want}', "
                f"actual '{got}'",
            )

    # G5 no-stray-untracked-in-scope (warn only)
    scope_dirs = {os.path.dirname(f).replace("\\", "/") for f in files}
    rc, out, _ = run_git(["status", "--porcelain"], repo_root)
    for line in out.splitlines():
        if line[:2] == "??":
            path = line[3:].strip().strip('"')
            d = os.path.dirname(path).replace("\\", "/")
            if d in scope_dirs and path not in declared_set:
                res.warn(
                    "G5",
                    f"untracked file in a declared directory (not in this "
                    f"commit): {path}",
                )

    return res, tmp_index, env


# --------------------------------------------------------------------------
# output helpers
# --------------------------------------------------------------------------
def print_manifest(manifest):
    print("=" * 70)
    print("MANIFEST")
    print("=" * 70)
    print("branch:  ", manifest.get("branch", "(not pinned)"))
    print("files:")
    for f in manifest.get("files", []):
        code = manifest.get("expected_status", {}).get(f, "?")
        print(f"  [{code}] {f}")
    print("message:")
    for line in (manifest.get("message", "") or "").splitlines() or [""]:
        print("  | " + line)
    print()


def print_diff(repo_root, env):
    print("=" * 70)
    print("DIFF TO BE COMMITTED (git diff --cached, via throwaway index)")
    print("=" * 70)
    _, stat, _ = run_git(["diff", "--cached", "--stat"], repo_root, env=env)
    print(stat.rstrip())
    print("-" * 70)
    _, full, _ = run_git(["diff", "--cached"], repo_root, env=env)
    print(full.rstrip())
    print()


def print_gate_report(res):
    print("=" * 70)
    print("GATES")
    print("=" * 70)
    for gate, msg in res.warnings:
        print(f"  [WARN {gate}] {msg}")
    if res.failures:
        for gate, msg in res.failures:
            print(f"  [FAIL {gate}] {msg}")
    else:
        print("  all gates passed")
    print()


# --------------------------------------------------------------------------
# execution (only after confirmation)
# --------------------------------------------------------------------------
def execute_commit(repo_root, manifest):
    files = manifest["files"]
    expected = manifest.get("expected_status", {})

    rc, _, err = run_git(["add", "--"] + files, repo_root)
    if rc != 0:
        print(f"ERROR: git add failed: {err.strip()}", file=sys.stderr)
        return 1

    # re-verify the real staged set matches expectation before the permanent step
    _, out, _ = run_git(["diff", "--cached", "--name-status"], repo_root)
    staged = parse_name_status(out)
    if set(staged.keys()) != set(files):
        print(
            "ABORT: staged set after `git add` does not equal the declared "
            f"files.\n  staged:   {sorted(staged.keys())}\n  declared: "
            f"{sorted(files)}",
            file=sys.stderr,
        )
        run_git(["reset", "-q", "HEAD", "--"] + files, repo_root)
        return 1
    for f, code in staged.items():
        want = (expected.get(f) or "").strip()[:1].upper()
        if want and want != code:
            print(
                f"ABORT: status code mismatch at execute for {f}: "
                f"expected '{want}', actual '{code}'",
                file=sys.stderr,
            )
            run_git(["reset", "-q", "HEAD", "--"] + files, repo_root)
            return 1

    # commit via message file (safe for multi-line)
    fd, msg_file = tempfile.mkstemp(prefix="siarc_msg_")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(manifest["message"].rstrip() + "\n")
        rc, out, err = run_git(["commit", "-F", msg_file], repo_root)
    finally:
        os.remove(msg_file)
    if rc != 0:
        print(f"ERROR: git commit failed: {err.strip() or out.strip()}",
              file=sys.stderr)
        run_git(["reset", "-q", "HEAD", "--"] + files, repo_root)
        return 1

    _, head, _ = run_git(["rev-parse", "HEAD"], repo_root)
    print(f"committed: {head.strip()}")

    rc, out, err = run_git(["push"], repo_root)
    if rc != 0:
        print(
            "WARNING: commit succeeded but push FAILED:\n"
            + (err.strip() or out.strip()),
            file=sys.stderr,
        )
        return 2
    print("push result:")
    print((out + err).strip())
    return 0


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Gated commit/push tool. Prepares, gates, shows the diff, "
        "and pauses for one explicit confirmation before staging exactly the "
        "declared files, committing, and pushing.",
    )
    parser.add_argument(
        "manifest", help="path to the commit manifest (JSON or YAML subset)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="run gates and print the diff, but stop BEFORE the confirm "
        "prompt; never stage, commit, or push.",
    )
    args = parser.parse_args(argv)

    if not os.path.exists(args.manifest):
        print(f"ERROR: manifest not found: {args.manifest}", file=sys.stderr)
        return 1

    repo_root = repo_toplevel(
        os.path.dirname(os.path.abspath(args.manifest)) or "."
    )
    if not repo_root:
        print("ERROR: not inside a git repository", file=sys.stderr)
        return 1

    try:
        manifest = load_manifest(args.manifest)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"ERROR: could not load manifest: {exc}", file=sys.stderr)
        return 1

    print_manifest(manifest)

    res, tmp_index, env = run_gates(repo_root, manifest)
    try:
        if env is not None:
            print_diff(repo_root, env)
        print_gate_report(res)

        if not res.ok:
            print("REFUSED: one or more gates failed; nothing was staged or "
                  "committed.")
            return 1

        if args.dry_run:
            print("DRY RUN: all gates passed. The confirm prompt and "
                  "stage/commit/push were skipped. Nothing changed.")
            return 0

        # interactive confirmation -- the load-bearing human gate
        print("=" * 70)
        print("REVIEW THE DIFF ABOVE.")
        print(f"Type exactly  {CONFIRM_TOKEN}  to stage-exactly, commit, and "
              "push. Anything else aborts.")
        print("=" * 70)
        try:
            answer = input("confirm> ")
        except EOFError:
            answer = ""
        if answer.strip() != CONFIRM_TOKEN:
            print("ABORTED: confirmation token not given. Nothing was staged "
                  "or committed; working tree untouched.")
            return 1
    finally:
        if tmp_index and os.path.exists(tmp_index):
            os.remove(tmp_index)

    return execute_commit(repo_root, manifest)


if __name__ == "__main__":
    sys.exit(main())
