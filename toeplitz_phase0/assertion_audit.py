"""Mechanical audit of every guard in the pipeline.

THE RULE BEING MECHANISED
-------------------------
L-044 and L-048 were the same bug wearing different clothes.  In both, the
assertion was written entirely in terms of quantities produced by the path
under test:

    positive_control:  planted the relation from the basis it was HANDED,
                       so a shrunken basis recovered its own plant.
    saturation guard:  tested `M >= orders[-1]`, where BOTH names are
                       outputs -- the selected truncation and the length of
                       the coefficient file that selected it.

Both fixes replaced an output-derived symbol with a declared one: the
declared basis, and `2*s <= orders[-1]` where `s` is an input.

So the criterion is not "is this check in its validity domain", which needs
insight, but:

    A GUARD MUST CONTAIN AT LEAST ONE SYMBOL THE PATH UNDER TEST CANNOT
    INFLUENCE.

A guard written purely from locally-computed values has no external referent
and can only ever compare the pipeline to itself.  That is checkable by
walking the AST, which is the point: two of the eleven instances were guards
written specifically to prevent the failure they then missed, so an audit
that depends on the auditor noticing is the wrong instrument.

WHAT THIS TOOL DOES AND DOES NOT DO
-----------------------------------
It reports; it does not decide.  It cannot know that `vals` is the object
under test rather than an independent reference -- that is the residual
judgement, and it is flagged for a human rather than resolved.  What it does
mechanically is classify every Name in every guard as DECLARED (parameter,
module constant, literal, loop bound over a literal range) or COMPUTED
(assigned from a call, or transitively from something computed), and flag
comparisons in which no DECLARED symbol appears.

Run: python assertion_audit.py
"""
import ast
import json
import os
import sys

GUARD_NAMES = {"ok", "passed", "saturated", "good", "valid", "reportable",
               "consistent", "agree", "stable", "converged", "clean"}
FAIL_WORDS = ("FAIL", "REFUS", "SATURAT", "INCONSIST", "raise", "HALT",
              "WRONG", "NOT reportable", "abort")


PURE = {"int", "float", "str", "len", "abs", "sorted", "list", "tuple",
        "set", "min", "max", "sum", "bool", "round", "range", "enumerate",
        "zip", "dict"}


class Classifier(ast.NodeVisitor):
    """Split names into DECLARED (external referent) and COMPUTED.

    Refined after running the first version against the codebase, which
    produced false positives that would have made the audit noise:

      * `M = int(sys.argv[1])` was tainted as COMPUTED because `int(...)` is
        a Call.  Command-line input is the most external referent available.
        Pure builtins applied to declared operands now preserve declaredness.
      * imported module names are external and are declared.

    `origins` additionally records, for each computed name, the names its
    defining expression referenced, so a finding can report whether the
    dependency chain reaches any declared symbol at all.  That distinguishes
    "compares two path outputs with no anchor anywhere" (the L-048 shape)
    from "compares derived quantities that trace back to declared inputs"
    (weaker, usually fine).
    """

    def __init__(self, module_consts):
        self.module_consts = module_consts
        self.declared = set(module_consts)
        self.computed = set()
        self.origins = {}

    def run(self, fn):
        for a in list(fn.args.args) + list(fn.args.kwonlyargs):
            self.declared.add(a.arg)
        if fn.args.vararg:
            self.declared.add(fn.args.vararg.arg)
        for _ in range(8):
            before = (len(self.declared), len(self.computed))
            for node in ast.walk(fn):
                if isinstance(node, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
                    tgts = ([node.target] if not isinstance(node, ast.Assign)
                            else node.targets)
                    val = node.value
                    if val is None:
                        continue
                    names = {n.id for n in ast.walk(val)
                             if isinstance(n, ast.Name)}
                    calls = [n for n in ast.walk(val) if isinstance(n, ast.Call)]
                    impure = any(not (isinstance(c.func, ast.Name) and
                                      c.func.id in PURE) for c in calls)
                    comp = (impure and bool(calls)) or bool(names & self.computed)
                    for t in tgts:
                        for nm in _targets(t):
                            self.origins.setdefault(nm, set()).update(names)
                            if comp:
                                self.computed.add(nm)
                                self.declared.discard(nm)
                            elif nm not in self.computed:
                                self.declared.add(nm)
                elif isinstance(node, ast.For):
                    it = node.iter
                    names = {n.id for n in ast.walk(it)
                             if isinstance(n, ast.Name)}
                    calls = [n for n in ast.walk(it) if isinstance(n, ast.Call)]
                    impure = any(not (isinstance(c.func, ast.Name) and
                                      c.func.id in PURE) for c in calls)
                    comp = bool(names & self.computed) or (impure and bool(calls))
                    for nm in _targets(node.target):
                        self.origins.setdefault(nm, set()).update(names)
                        (self.computed if comp else self.declared).add(nm)
            if (len(self.declared), len(self.computed)) == before:
                break
        return self

    def closure(self, name, seen=None):
        """All names this one transitively depends on, including itself."""
        seen = seen or set()
        if name in seen:
            return seen
        seen.add(name)
        for src in self.origins.get(name, ()):
            self.closure(src, seen)
        return seen

    def side_closure(self, node):
        out = set()
        for n in ast.walk(node):
            if isinstance(n, ast.Name):
                out |= self.closure(n.id)
        return out

    def reaches_declared(self, name, seen=None):
        """Does this name's dependency chain touch any declared symbol?"""
        seen = seen or set()
        if name in seen:
            return False
        seen.add(name)
        for src in self.origins.get(name, ()):
            if src in self.declared:
                return True
            if self.reaches_declared(src, seen):
                return True
        return False


def _targets(t):
    if isinstance(t, ast.Name):
        return [t.id]
    if isinstance(t, (ast.Tuple, ast.List)):
        out = []
        for e in t.elts:
            out += _targets(e)
        return out
    return []


def guard_nodes(fn):
    """Yield (kind, node) for things that act as guards."""
    for node in ast.walk(fn):
        if isinstance(node, ast.Assert):
            yield "assert", node.test
        elif isinstance(node, ast.If):
            src = ast.dump(node)
            raises = any(isinstance(n, (ast.Raise,)) for n in ast.walk(node))
            says = any(w.lower() in src.lower() for w in FAIL_WORDS)
            if raises or says:
                yield "if-guard", node.test
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                for nm in _targets(t):
                    if nm.lower() in GUARD_NAMES:
                        yield f"flag:{nm}", node.value


def _operand_literals(expr):
    """Constants used as COMPARISON OPERANDS, not as subscript indices.

    `orders[-1]` contains the constant 1, which is an array index and is in no
    sense an external referent.  Counting it as one made the auditor pass the
    known-broken L-048 guard -- caught by running the auditor against that
    guard before trusting it.
    """
    found = []
    for cmpnode in [n for n in ast.walk(expr) if isinstance(n, ast.Compare)]:
        for side in [cmpnode.left] + list(cmpnode.comparators):
            for n in ast.walk(side):
                if isinstance(n, ast.Subscript):
                    continue
                if isinstance(n, ast.Constant) and isinstance(
                        n.value, (int, float)):
                    # Skip constants that live inside a subscript slice.
                    if not any(isinstance(p, ast.Subscript)
                               for p in _ancestors(side, n)):
                        found.append(n.value)
    return found


def _ancestors(root, target):
    out = []

    def walk(node, chain):
        if node is target:
            out.extend(chain)
            return True
        for ch in ast.iter_child_nodes(node):
            if walk(ch, chain + [node]):
                return True
        return False

    walk(root, [])
    return out


def audit_expr(expr, cls):
    """Findings for the guard expression AS A WHOLE.

    THE CRITERION, after two rounds of self-correction.

    First attempt asked "does the guard mention a declared symbol".  On real
    code that is useless in both directions: almost every value eventually
    traces to a parameter, so the audit reported 0 findings over 65 guards --
    a result indistinguishable from an audit that does nothing, which is the
    very failure mode this project keeps hitting.

    The sharp question is not whether an anchor exists somewhere, but whether
    THE TWO SIDES OF THE COMPARISON ARE INDEPENDENT.  A check whose measured
    side and whose threshold side descend from the same computation compares
    the pipeline to itself, and that is exactly what L-044 and L-048 were:

        L-048:  M <- best <- search(coeffs);  orders <- sorted(coeffs)
                                              common ancestor: coeffs
        L-044:  want <- ks <- vals;  rel <- pslq_search(target) <- vals
                                              common ancestor: vals

    Both repairs severed that link -- `2*s` where s is an input, and a plant
    built from `declared`.  So:

        A GUARD IS SUSPECT IF EVERY COMPARISON IN IT HAS A COMMON COMPUTED
        ANCESTOR ON BOTH SIDES.

    A disjunction is clean if any one clause is independent, since any clause
    alone is sufficient to fire it.
    """
    cmps = [n for n in ast.walk(expr) if isinstance(n, ast.Compare)]
    if not cmps:
        return []
    worst = None
    for c in cmps:
        left = cls.side_closure(c.left)
        right = set()
        for comp in c.comparators:
            right |= cls.side_closure(comp)
        shared = (left & right) & cls.computed
        if not shared:
            return []          # this clause is independent: guard is fine
        worst = shared if worst is None else worst
    names = {n.id for n in ast.walk(expr) if isinstance(n, ast.Name)}
    return [("CIRCULAR-COMPARISON", sorted(names & cls.computed),
             sorted(worst))]


def _waiver(src_lines, lineno):
    """An explicit, auditable disposition for a flagged guard.

    A finding may be legitimately accepted, but accepting it by deleting the
    check or loosening the tool would make the audit self-defeating -- the
    same shape as a control that passes by being switched off.  So a waiver
    is written next to the guard as

        # AUDIT-REVIEWED: <reason>

    and the tool COUNTS AND PRINTS waivers rather than hiding them.  A waiver
    with no reason text is not honoured.
    """
    lo = max(0, lineno - 12)
    for ln in src_lines[lo:lineno]:
        if "AUDIT-REVIEWED" in ln:
            reason = ln.split("AUDIT-REVIEWED", 1)[1].lstrip(": ").strip()
            if reason:
                return reason
    return None



# --------------------------------------------------------------------------
# SECOND PASS -- transcribed numeric literals
# --------------------------------------------------------------------------
#
# L-050's root cause was not a circular guard.  It was a hardcoded dict of
# values TRANSCRIBED AT AUTHORING TIME instead of computed at runtime:
#
#     PREDICTED = {149: 129.4, 200: 173.8, 250: 217.3}
#
# The transcription rounded 2s/ln(10) inconsistently, injecting a spurious
# drift the same size as the effect under study.  The special-case rule was
# "never subtract a rounded prediction"; the general rule is NO TRANSCRIBED
# NUMERICS IN VERIFICATION CODE, and unlike the guard criterion it really is
# grep-able.
#
# The discriminant between a SPECIFICATION and a TRANSCRIPTION is precision.
# A declared threshold is round by construction -- 10, 1e-17, 1e4, 0.5.  A
# transcribed value carries the fingerprint of a computation someone ran
# elsewhere: three or more significant digits.  That is the test applied here.

SIGDIG_LIMIT = 3        # declared: >= this many sig digits reads as transcribed


def _sigdigits(v):
    """Significant digits in a numeric literal, ignoring sign and exponent."""
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return 0
    if v == 0:
        return 0
    s = repr(abs(v))
    if "e" in s or "E" in s:
        s = s.split("e")[0].split("E")[0]
    s = s.replace(".", "").lstrip("0").rstrip("0")
    return len(s)


def numeric_transcriptions(tree, src_lines, fname):
    """Numeric literals precise enough to be transcribed results."""
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant):
            continue
        if isinstance(node.value, bool) or not isinstance(
                node.value, (int, float)):
            continue
        n = _sigdigits(node.value)
        if n < SIGDIG_LIMIT:
            continue
        # Integers are overwhelmingly counts, node numbers, precisions and
        # array sizes -- 120 dps, M=600, s=149.  Those are inputs, and an
        # input is exactly what a check SHOULD be anchored to.  The failure
        # mode is a transcribed non-integer.
        if isinstance(node.value, int):
            continue
        ln = getattr(node, "lineno", 0)
        out.append({"file": fname, "line": ln, "value": repr(node.value),
                    "sigdigits": n,
                    "src": src_lines[ln - 1].strip()[:90] if ln else "",
                    "waiver": _waiver(src_lines, ln)})
    return out


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    files = sorted(f for f in os.listdir(root) if f.endswith(".py"))
    findings = []
    n_guards = 0
    for f in files:
        src = open(os.path.join(root, f), encoding="utf-8").read()
        src_lines = src.splitlines()
        try:
            tree = ast.parse(src)
        except SyntaxError as e:
            print(f"[skip] {f}: {e}")
            continue
        module_consts = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for al in node.names:
                    module_consts.add((al.asname or al.name).split(".")[0])
        for node in tree.body:
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                tg = (node.targets if isinstance(node, ast.Assign)
                      else [node.target])
                for t in tg:
                    module_consts.update(_targets(t))
        for fn in [n for n in ast.walk(tree)
                   if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
            cls = Classifier(module_consts).run(fn)
            for kind, expr in guard_nodes(fn):
                n_guards += 1
                for sev, comp, decl in audit_expr(expr, cls):
                    ln = getattr(expr, "lineno", fn.lineno)
                    findings.append({"file": f, "func": fn.name, "line": ln,
                                     "kind": kind, "severity": sev,
                                     "computed": comp, "declared": decl,
                                     "waiver": _waiver(src_lines, ln)})

    transcriptions = []
    for f in files:
        src = open(os.path.join(root, f), encoding="utf-8").read()
        try:
            tree = ast.parse(src)
        except SyntaxError:
            continue
        transcriptions += numeric_transcriptions(tree, src.splitlines(), f)
    tr_hard = [x for x in transcriptions if not x["waiver"]]

    waived = [x for x in findings if x["waiver"]]
    hard = [x for x in findings
            if x["severity"] == "CIRCULAR-COMPARISON" and not x["waiver"]]
    soft = []
    anch = []

    print("=" * 74)
    print("ASSERTION AUDIT -- guards with no symbol outside the path under test")
    print("=" * 74)
    print(f"  files scanned ............ {len(files)}")
    print(f"  guard expressions ........ {n_guards}")
    print(f"  CIRCULAR-COMPARISON ...... {len(hard)}   <-- the L-044/L-048 class")
    print(f"  waived (reviewed) ........ {len(waived)}")
    print(f"  TRANSCRIBED NUMERICS ..... {len(tr_hard)}   <-- the L-050 class")
    print(f"    (waived transcriptions)  {len(transcriptions) - len(tr_hard)}")
    for x in tr_hard[:20]:
        print(f"      {x['file']}:{x['line']}  {x['value']} "
              f"({x['sigdigits']} sig digits)")
        print(f"          {x['src']}")


    if hard:
        print("\n--- BOTH SIDES SHARE A COMPUTED ANCESTOR ---")
        for x in hard:
            print(f"  {x['file']}:{x['line']}  {x['func']}()  [{x['kind']}]")
            print(f"      computed: {x['computed']}   shared ancestor: {x['declared']}")
    if soft:
        print("\n--- LITERAL THRESHOLD ONLY (referent is a magic number) ---")
        for x in soft:
            print(f"  {x['file']}:{x['line']}  {x['func']}()  [{x['kind']}]"
                  f"  computed={x['computed']}")

    if waived:
        print("\n--- WAIVED (explicitly reviewed, still reported) ---")
        for x in waived:
            print(f"  {x['file']}:{x['line']}  {x['func']}()")
            print(f"      {x['waiver']}")
    json.dump({"files": len(files), "guards": n_guards,
               "circular": hard, "waived": waived,
               "transcribed": tr_hard,
               "transcribed_waived": len(transcriptions) - len(tr_hard)},
              open("out/assertion_audit.json", "w"), indent=2)
    print("\n[out] out/assertion_audit.json")
    return 1 if (hard or tr_hard) else 0


if __name__ == "__main__":
    sys.exit(main())
