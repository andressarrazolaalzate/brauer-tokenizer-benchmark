"""Offline repository integrity checks."""
from __future__ import annotations
from pathlib import Path
from brauer_tokenizer import entropy_asymptotic_coefficient, occurrence_descriptors, verify_occurrence_closed_forms
from brauer_tokenizer.corpus import generate_reference_corpus, corpus_sha256

root=Path(__file__).resolve().parents[1]
assert corpus_sha256(generate_reference_corpus()) == "6888d24246c8b121b6492b9b3132d49564c50149a86a4547c2a2d79fc5d7b9fb"
assert verify_occurrence_closed_forms(12,3)==48
for r, target in [(1,-0.12605),(2,-0.22998),(3,-0.32979)]:
    assert abs(entropy_asymptotic_coefficient(r)-target)<5e-6
# Figure 1 quiver count: N=3, r=1 gives seven arrows.
assert occurrence_descriptors(3,1).quiver_arrows == 7
# No internal review-stage filenames or caches should ship.
prohibited={"__pycache__","REVIEWER_REVISION_NOTES.md","type_collapse_patch.py","brauer_audit_core.py"}
for path in root.rglob("*"):
    if path.name == "__pycache__":
        continue
    assert path.name not in prohibited, f"provisional artifact found: {path}"
print("Offline repository integrity checks passed.")
