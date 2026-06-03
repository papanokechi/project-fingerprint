#!/usr/bin/env python3
"""
Targeted patch: correct STATE_OF_PLAY.md open-item 3 (and tidy item 4) to reflect
the M10 decision-brief finding -- the DEPOSITED PAPER claims symbolic/numerical
proof (dps=150), NOT Lean, so there is no publication-caveat problem; the
'Thm 6.6 in Lean' overstatement is corpus-internal status tracking only.

Also: replaces the specific item-3/4 block's em-dashes with plain ASCII '--' to
avoid the existing mojibake (the file has UTF-8/Windows-1252 mismatch). Writes the
whole file back as explicit UTF-8.

Run from repo root:  python <thispath>   (targets ./STATE_OF_PLAY.md)
Matches on a stable anchor; refuses if the anchor isn't found.
"""
import sys, io

PATH = "STATE_OF_PLAY.md"

with io.open(PATH, "r", encoding="utf-8", errors="replace") as f:
    s = f.read()

# Anchor: start of item 3 ("3. M10 Lean core") through the end of item 4
# (the line before "## The next move"). We replace that whole span.
start_marker = "3. M10 Lean core"
end_marker = "## The next move"

i = s.find(start_marker)
j = s.find(end_marker)
if i == -1 or j == -1 or j < i:
    sys.exit("ERROR: could not locate the item-3..item-4 span; aborting (no change).")

new_block = (
"3. M10 IndicialPoly stub -- CORPUS-INTERNAL, not a publication problem\n"
"   (CORRECTED 2026-06-03 by the M10 decision brief). Earlier framing treated this\n"
"   as a possible caveat on a DEPOSITED formalization claim. That is wrong: the\n"
"   deposited paper (vquad_resurgence_R2.tex, thm:exclusion2) claims a SYMBOLIC +\n"
"   NUMERICAL proof at dps=150 (verify_frobenius_apparent.py), which it has, and\n"
"   makes NO Lean / machine-checked / formally-verified claim. The stub\n"
"   (IndicialPoly := fun rho => rho^2, vacuous; committed proof has 2 sorrys and\n"
"   textually-but-redundantly invokes the Frobenius axiom) lives ONLY in the\n"
"   corpus-internal M10 status tracking ('Thm66 in Lean'), which is where the\n"
"   overstatement is. So: NO publication caveat needed -- this is internal-status\n"
"   cleanup, a much smaller thing than a published overstatement. Confirmed\n"
"   verbatim against the live file (branch vquad/handoff-2026-04-16, blob\n"
"   5b44e690). Full record: agent-tasks/B-M10-decision-brief.md (supersedes the\n"
"   harsher B-M10-stage0-findings.md framing).\n"
"4. M10 Lean core discoverability (unchanged). Thm66_ApparentSingularity.lean is\n"
"   on branch vquad/handoff-2026-04-16, NOT on main -- anyone cloning\n"
"   wallis-pcf-lean4 normally won't find the Lean core. Published but not\n"
"   discoverable; four neutral options (merge / pointer / leave / strengthen-first)\n"
"   in the decision brief. Operator's call.\n\n"
)

patched = s[:i] + new_block + s[j:]

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(patched)

# verify
with io.open(PATH, "r", encoding="utf-8") as f:
    check = f.read()
ok_corrected = "CORPUS-INTERNAL, not a publication problem" in check
ok_no_mojibake_in_block = "\u00e2\u20ac" not in new_block  # the mangled em-dash sequence
print("PATCH applied.")
print("  item 3 corrected:", ok_corrected)
print("  new block is mojibake-free (ASCII dashes):", ok_no_mojibake_in_block)
print("  NOTE: other em-dashes elsewhere in the file (lines ~17, ~142) are NOT touched by this patch.")
