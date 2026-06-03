#!/usr/bin/env python3
"""Tests for siarc_commit.py.

Builds throwaway git repos (each with a bare 'origin' remote so push works for
real) and asserts the tool behaves -- ESPECIALLY the refusal cases. A gate is
only trusted once it is watched refusing.

Run:  python tools/test_siarc_commit.py
Exit code 0 iff every test passes.
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "siarc_commit.py")

PASS, FAIL = "PASS", "FAIL"
_results = []


def record(name, ok, asserts, detail=""):
    _results.append((name, ok))
    status = PASS if ok else FAIL
    print(f"[{status}] {name}: {asserts}")
    if not ok and detail:
        for line in detail.splitlines():
            print("        " + line)


def git(args, cwd, **kw):
    return subprocess.run(["git"] + args, cwd=cwd, capture_output=True,
                          text=True, **kw)


def run_tool(manifest_path, cwd, dry_run=False, stdin=None):
    cmd = [sys.executable, TOOL, manifest_path]
    if dry_run:
        cmd.append("--dry-run")
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          input=stdin)


def new_repo():
    """Create a temp working repo with a bare origin remote; return root dir."""
    root = tempfile.mkdtemp(prefix="siarc_test_")
    work = os.path.join(root, "work")
    bare = os.path.join(root, "origin.git")
    os.makedirs(work)
    git(["init", "-b", "main", "--bare", bare], cwd=root)
    git(["init", "-b", "main", work], cwd=root)
    git(["config", "user.email", "t@example.com"], cwd=work)
    git(["config", "user.name", "tester"], cwd=work)
    git(["config", "commit.gpgsign", "false"], cwd=work)
    git(["remote", "add", "origin", bare], cwd=work)
    # seed an initial commit so HEAD/diffs exist
    write(work, "alpha.txt", "alpha v1\n")
    write(work, "data.json", '{"a": 1}\n')
    git(["add", "alpha.txt", "data.json"], cwd=work)
    git(["commit", "-m", "init"], cwd=work)
    git(["push", "-u", "origin", "main"], cwd=work)
    os.makedirs(os.path.join(work, ".siarc"), exist_ok=True)
    return root, work, bare


def write(work, rel, content):
    p = os.path.join(work, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(content)


def manifest(work, files, message, expected, branch=None, name="m.json"):
    import json
    path = os.path.join(work, ".siarc", name)
    data = {"files": files, "message": message, "expected_status": expected}
    if branch:
        data["branch"] = branch
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh)
    return path


def head(work):
    return git(["rev-parse", "HEAD"], cwd=work).stdout.strip()


def index_clean(work):
    return git(["diff", "--cached", "--quiet"], cwd=work).returncode == 0


def cleanup(root):
    shutil.rmtree(root, ignore_errors=True)


# --------------------------------------------------------------------------
def t1_clean_dry_run():
    root, work, _ = new_repo()
    try:
        write(work, "alpha.txt", "alpha v2 changed\n")
        mpath = manifest(work, ["alpha.txt"], "update alpha text",
                         {"alpha.txt": "M"})
        r = run_tool(mpath, work, dry_run=True)
        ok = (r.returncode == 0
              and "all gates passed" in r.stdout
              and "DRY RUN" in r.stdout
              and "alpha v2 changed" in r.stdout)  # diff shown
        record("T1 clean/dry-run", ok,
               "declared file changed, status matches -> reaches prompt "
               "(dry-run, no push), diff printed, exit 0",
               r.stdout + r.stderr)
    finally:
        cleanup(root)


def t2_silent_noop():
    root, work, _ = new_repo()
    try:
        # declare a file with NO change
        mpath = manifest(work, ["alpha.txt"], "noop commit attempt",
                         {"alpha.txt": "M"})
        r = run_tool(mpath, work, dry_run=True)
        ok = (r.returncode != 0
              and "G3" in r.stdout
              and "REFUSED" in r.stdout)
        record("T2 silent-noop", ok,
               "declared file has no diff -> G3 FAIL, refuses (the bug that "
               "hit STATE_OF_PLAY twice)", r.stdout + r.stderr)
    finally:
        cleanup(root)


def t3_contamination():
    # (a) stray untracked in a declared dir -> G5 warns, gates still pass
    root, work, _ = new_repo()
    try:
        write(work, "sub/main.txt", "tracked\n")
        git(["add", "sub/main.txt"], cwd=work)
        git(["commit", "-m", "add sub"], cwd=work)
        write(work, "sub/main.txt", "tracked changed\n")
        write(work, "sub/stray.txt", "another thread wrote here\n")  # untracked
        mpath = manifest(work, ["sub/main.txt"], "update sub/main",
                         {"sub/main.txt": "M"})
        r = run_tool(mpath, work, dry_run=True)
        warn_ok = (r.returncode == 0 and "WARN G5" in r.stdout
                   and "stray.txt" in r.stdout)
        record("T3a contamination/G5-warn", warn_ok,
               "untracked file in a declared dir -> G5 WARNS (not fail), "
               "gates pass", r.stdout + r.stderr)
    finally:
        cleanup(root)

    # (b) manifest under-declares (expected_status omits a changed declared file)
    root, work, _ = new_repo()
    try:
        write(work, "alpha.txt", "alpha changed\n")
        write(work, "data.json", '{"a": 2}\n')
        mpath = manifest(work, ["alpha.txt", "data.json"], "two-file commit",
                         {"alpha.txt": "M"})  # data.json omitted
        r = run_tool(mpath, work, dry_run=True)
        ok = (r.returncode != 0 and "G2" in r.stdout
              and "under-declares" in r.stdout)
        record("T3b under-declare/G2-fail", ok,
               "expected_status omits a file that would stage -> G2 FAIL",
               r.stdout + r.stderr)
    finally:
        cleanup(root)


def t4_broken_json():
    root, work, _ = new_repo()
    try:
        write(work, "data.json", '{"a": 1, broken}\n')  # invalid JSON
        mpath = manifest(work, ["data.json"], "update data",
                         {"data.json": "M"})
        r = run_tool(mpath, work, dry_run=True)
        ok = (r.returncode != 0 and "G4" in r.stdout and "REFUSED" in r.stdout)
        record("T4 broken-json", ok,
               "declared json has a syntax error -> G4 FAIL, refuses",
               r.stdout + r.stderr)
    finally:
        cleanup(root)


def t5_non_confirmation():
    root, work, _ = new_repo()
    try:
        before = head(work)
        write(work, "alpha.txt", "alpha v2\n")
        mpath = manifest(work, ["alpha.txt"], "should not commit",
                         {"alpha.txt": "M"})
        r = run_tool(mpath, work, dry_run=False, stdin="no\n")
        after = head(work)
        ok = (r.returncode != 0
              and "ABORTED" in r.stdout
              and before == after          # no new commit
              and index_clean(work))       # nothing staged
        record("T5 non-confirmation", ok,
               "operator does NOT type the token -> abort, stage nothing, "
               "tree untouched, no commit", r.stdout + r.stderr
               + f"\nbefore={before} after={after} index_clean="
               f"{index_clean(work)}")
    finally:
        cleanup(root)


def t6_over_staging_exact():
    root, work, bare = new_repo()
    try:
        before = head(work)
        # two files changed; declare ONLY alpha.txt
        write(work, "alpha.txt", "alpha committed\n")
        write(work, "data.json", '{"a": 999}\n')  # changed but NOT declared
        mpath = manifest(work, ["alpha.txt"], "commit only alpha",
                         {"alpha.txt": "M"}, branch="main")
        r = run_tool(mpath, work, dry_run=False, stdin="CONFIRM\n")
        after = head(work)
        committed = git(["show", "--name-only", "--pretty=format:",
                         "HEAD"], cwd=work).stdout.split()
        # data.json must remain uncommitted (still modified in worktree)
        status = git(["status", "--porcelain"], cwd=work).stdout
        # confirm push reached the bare remote
        remote_head = git(["--git-dir", bare, "rev-parse", "main"],
                          cwd=work).stdout.strip()
        ok = (r.returncode == 0
              and before != after
              and committed == ["alpha.txt"]   # EXACTLY the declared file
              and "data.json" in status        # the undeclared change survived
              and remote_head == after)        # pushed
        record("T6 over-staging/exact + push", ok,
               "stages EXACTLY the declared file (never the undeclared "
               "data.json), commits, and pushes to origin",
               r.stdout + r.stderr
               + f"\ncommitted={committed} remote_head={remote_head} "
               f"after={after}\nstatus={status!r}")
    finally:
        cleanup(root)


def t7_branch_mismatch():
    root, work, _ = new_repo()
    try:
        write(work, "alpha.txt", "alpha v2\n")
        mpath = manifest(work, ["alpha.txt"], "wrong branch",
                         {"alpha.txt": "M"}, branch="release")
        r = run_tool(mpath, work, dry_run=True)
        ok = (r.returncode != 0 and "G7" in r.stdout)
        record("T7 branch-check", ok,
               "manifest pins branch 'release' but on 'main' -> G7 FAIL",
               r.stdout + r.stderr)
    finally:
        cleanup(root)


def t8_yaml_manifest():
    root, work, _ = new_repo()
    try:
        write(work, "alpha.txt", "alpha yaml\n")
        ypath = os.path.join(work, ".siarc", "m.yaml")
        with open(ypath, "w", encoding="utf-8") as fh:
            fh.write(
                "files:\n  - alpha.txt\n"
                "message: |\n  yaml manifest commit\n  second line\n"
                "expected_status:\n  alpha.txt: M\n"
                "branch: main\n"
            )
        r = run_tool(ypath, work, dry_run=True)
        ok = (r.returncode == 0 and "all gates passed" in r.stdout
              and "yaml manifest commit" in r.stdout
              and "second line" in r.stdout)
        record("T8 yaml-manifest", ok,
               "YAML-subset manifest parses (files/message-block/expected/"
               "branch) and reaches prompt", r.stdout + r.stderr)
    finally:
        cleanup(root)


def main():
    if shutil.which("git") is None:
        print("git not found", file=sys.stderr)
        return 2
    t1_clean_dry_run()
    t2_silent_noop()
    t3_contamination()
    t4_broken_json()
    t5_non_confirmation()
    t6_over_staging_exact()
    t7_branch_mismatch()
    t8_yaml_manifest()

    print("-" * 70)
    total = len(_results)
    passed = sum(1 for _, ok in _results if ok)
    refusals = ["T2 silent-noop", "T4 broken-json", "T5 non-confirmation",
                "T6 over-staging/exact + push"]
    refusals_ok = all(ok for name, ok in _results
                      if name in refusals)
    print(f"{passed}/{total} checks passed; "
          f"refusal/safety cases (T2/T4/T5/T6) "
          f"{'ALL FIRED' if refusals_ok else 'NOT all firing'}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
