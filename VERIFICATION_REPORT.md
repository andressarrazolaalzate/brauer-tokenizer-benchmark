# Release verification report

This report records the release checks for version **1.1.0** of the code accompanying **Brauer Entropy for Cost-Aware Pattern Recognition in LLM Tokenization**.

## Release decision

**Status: ready for GitHub publication.**

The mathematical layer, deterministic corpus, controlled type-collapse experiment, repository structure, metadata, and offline regression suite have been verified in the release tree. The only check not executed in the present isolated runtime is a fresh download and execution of the five external Hugging Face tokenizer snapshots. That network-dependent check is encoded as both a command-line gate (`--verify-manuscript`) and a manually triggered GitHub Actions workflow.

## What was verified locally

- 500 unique synthetic sentences are regenerated from seed `20260823`.
- Corpus SHA-256: `6888d24246c8b121b6492b9b3132d49564c50149a86a4547c2a2d79fc5d7b9fb`.
- Corpus statistics agree with the manuscript: mean word count 18.722 (SD 2.095, range 13--23); mean character count 124.354 (SD 16.924, range 77--153).
- The occurrence implementation is independently checked against materialized windows, co-occurrence edges, incidence edges, connected components, and Brauer-quiver arrows for all 48 pairs `1 <= N <= 12`, `0 <= r <= 3`.
- Figure 1 is reproduced combinatorially: `N=3`, `r=1` gives seven quiver arrows.
- Proposition 8 coefficients reproduce `c_1=-0.12605`, `c_2=-0.22998`, and `c_3=-0.32979` at the stated precision; the exact entropy formula is cross-checked through `r=6` in the unit tests.
- Proposition 9 is checked by unit tests and by 5,075 fixed-seed randomized cases.
- The controlled Table 4 (`N=23`, repeated type at positions 2, 6, 12, 18) is reproduced exactly before rounding, including `dim Z = 24` for both models.
- Table 2 affine identities and special-token shifts are checked from the final manuscript targets.
- Table 3 cost-growth percentages are reconstructed from the final mean lengths.
- `H_norm` is `NaN` for a one-vertex probability space rather than being assigned zero.
- Descriptor dictionaries contain one key per quantity.
- No `trust_remote_code=True` call is present.
- Five tokenizer repositories are pinned to full immutable commit SHAs rather than `main`; all five revision pages were independently checked on Hugging Face on 2026-08-25.
- No review-stage files, Python bytecode, generated results, or cache directories are included in the release ZIP.
- Package installation succeeds without fetching optional benchmark dependencies.
- The notebook is valid JSON and delegates the scientific implementation to the installed package rather than carrying a divergent copy of the old benchmark.

## Manuscript fidelity

### Occurrence baseline

`brauer_tokenizer.core.occurrence_descriptors` implements the final manuscript's occurrence-indexed baseline. The code and README explicitly state that the occurrence vector is controlled by `(N,r)` and is not lexical evidence.

### Type-collapsed refinement

`brauer_tokenizer.core.type_collapsed_descriptors` implements the final manuscript's repetition-sensitive refinement. For `r >= 1`, the verification suite checks preservation of `C_B` and `dim Z`, non-increase of Brauer entropy, non-decrease of algebra dimension, preservation of quiver-arrow mass, and strictness exactly when a token type repeats.

### Tables 2 and 3

`brauer-tokenizer-benchmark --verify-manuscript` recomputes the full 500 x 5 x 4 occurrence experiment with the pinned tokenizer snapshots and raises an error unless the displayed values of Tables 2 and 3 match the final manuscript.

### Table 4

`scripts/reproduce_table4.py` reproduces every reported row of the fixed-length type-collapse comparison from the declared positions. It is not presented as a corpus average.

### Cost-aware scope

The README mirrors the final paper: at fixed radius, `C_B` orders examples exactly as token count does; across radii it records local window-token incidence amplification. Monetary, runtime, memory, and hardware cost are not inferred from `C_B`.

## External end-to-end gate

On GitHub, run **Actions -> Full manuscript benchmark -> Run workflow**. It installs the pinned benchmark dependencies, downloads tokenizer assets from their pinned revisions, reproduces Tables 2 and 3 with `--verify-manuscript`, reproduces Table 4, and uploads the generated numerical outputs.

A successful workflow run is the final network-dependent confirmation that the external tokenizer assets still resolve exactly as pinned.
