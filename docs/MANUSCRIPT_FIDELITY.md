# Manuscript-to-code fidelity map

This file records how the public implementation corresponds to the final 15-page manuscript **Brauer Entropy for Cost-Aware Pattern Recognition in LLM Tokenization**.

| Manuscript item | Code | Verification |
|---|---|---|
| Indexed windows and occurrence valencies | `core.occurrence_windows`, `core.occurrence_valencies` | explicit-vs-formula tests for 48 `(N,r)` cases |
| Multiplicity rule | `core.local_multiplicities` | unit tests and explicit construction |
| `C_B`, `nu`, `H_B`, `H_norm`, `dim Lambda`, `dim Z`, components, graph/quiver sizes | `core.occurrence_descriptors` | `tests/test_core.py` |
| Proposition 8 coefficient `c_r` | `core.entropy_asymptotic_coefficient` | values for `r=1,2,3`; exact entropy cross-check through `r=6` |
| Proposition 9 type collapse | `core.type_collapsed_descriptors` | equality/strictness tests + 5,075 fixed-seed randomized cases |
| Figure 1 quiver count (`N=3,r=1`) | `core.occurrence_reference_objects` | exactly 7 quiver arrows |
| 500-sentence corpus, seed `20260823` | `corpus.generate_reference_corpus` | exact digest and published corpus statistics |
| Five tokenizer families | `tokenizers.TOKENIZERS` | canonical repository names for the manuscript aliases; full immutable revisions; `trust_remote_code=False` |
| 10,000 occurrence evaluations | `benchmark.run_benchmark` | row-count assertion |
| Table 2 | `benchmark.run_benchmark` | `benchmark.verify_manuscript_tables` |
| Table 3 | `benchmark.run_benchmark` | `benchmark.verify_manuscript_tables` |
| Table 4 | `scripts/reproduce_table4.py` | exact unit-test values and CSV export |

## Deliberate scope boundaries

- The occurrence baseline is a deterministic function of `(N,r)` and is not presented as lexical evidence.
- Corpus-wide type-collapse output is optional and labelled exploratory because the final manuscript reports only the controlled fixed-length example for Proposition 9.
- No generation model is loaded and no downstream recognition accuracy is computed.
- Economic, runtime, memory, and hardware costs are outside `C_B` and are not inferred from it.

## Environment caveat

Offline tests verify all mathematical results and all article values that do not require external tokenization assets. Reproducing Tables 2 and 3 from raw sentences requires installing the pinned benchmark dependencies and downloading the five pinned tokenizer snapshots. The `--verify-manuscript` flag performs that final end-to-end check and fails on any displayed-value mismatch.

## Publication gate

The release contains `.github/workflows/full-manuscript-benchmark.yml`. This manually triggered workflow performs the network-dependent five-tokenizer run and invokes `--verify-manuscript`; it is the definitive end-to-end check after publication on GitHub.
