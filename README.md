# Brauer Tokenizer Benchmark

Reproducibility code for **Brauer Entropy for Cost-Aware Pattern Recognition in LLM Tokenization** by Andrés Sarrazola-Alzate and Agustín Moreno Cañadas.

This repository implements exactly the two mathematical levels used in the final manuscript:

1. **Occurrence-indexed baseline.** Token positions are distinct Brauer vertices. For fixed sequence length `N` and radius `r`, all reported occurrence descriptors are determined by `(N, r)`.
2. **Type-collapsed refinement.** Equal token strings are identified while indexed windows remain multisets. For `r >= 1`, this preserves `C_B`, cannot increase Brauer entropy, cannot decrease algebra dimension, and changes the last two quantities strictly exactly when a token type repeats.

The repository deliberately does **not** describe the occurrence baseline as a text-sensitive feature extractor and does **not** claim downstream recognition accuracy.

## What is reproduced

- the fixed 500-sentence English corpus generated deterministically with seed `20260823`;
- five Hugging Face tokenizer families: BERT, RoBERTa, GPT-2, Qwen2.5, and Mistral-7B;
  The repository uses the current canonical Hugging Face repository names for the three historical aliases in the paper: `bert-base-uncased` -> `google-bert/bert-base-uncased`, `roberta-base` -> `FacebookAI/roberta-base`, and `gpt2` -> `openai-community/gpt2`. The tokenizer assets are unchanged aliases of the same repositories.
- radii `r = 0, 1, 2, 3` for `500 x 5 x 4 = 10,000` occurrence-baseline evaluations;
- manuscript Table 2: `r=1` tokenizer profile with special-token control;
- manuscript Table 3: radius dependence as an analytic control;
- manuscript Table 4: controlled type-collapse example with `N=23`, 20 types, and one type repeated at positions `2, 6, 12, 18`;
- explicit small-`N` constructions of windows, the co-occurrence graph, the incidence graph, and Brauer-quiver arrows for independent checks of the closed formulas.

The 10,000 occurrence evaluations are **not 10,000 independent structural patterns**. They are repeated evaluations of a descriptor determined by tokenized length and radius. This distinction is part of the final paper.

## Repository layout

```text
src/brauer_tokenizer/
    core.py          mathematical definitions, explicit reference objects, Propositions 8-9 checks
    corpus.py        deterministic 500-sentence corpus generator
    tokenizers.py    pinned Hugging Face tokenizer snapshots
    benchmark.py     full benchmark and manuscript-table verification
scripts/
    materialize_corpus.py
    reproduce_table4.py
    verify_randomized.py
    verify_repository.py
tests/
    test_core.py
    test_corpus_and_manuscript.py
    test_tokenizer_config.py
expected/
    manuscript_tables.json
notebooks/
    reproduce_manuscript.ipynb
docs/
    MANUSCRIPT_FIDELITY.md
```

## Installation

The mathematical core uses only the Python standard library:

```bash
python -m pip install -e .
```

For the full Hugging Face benchmark:

```bash
python -m pip install -e '.[benchmark]'
```

`requirements.txt` contains the same benchmark dependency pins for environments that prefer a requirements file.

## Fast offline verification

These commands require no model download:

```bash
python -m unittest discover -s tests -v
python scripts/verify_repository.py
python scripts/reproduce_table4.py
python scripts/verify_randomized.py
```

The randomized script checks Proposition 9 on 5,075 fixed-seed cases.

## Full manuscript benchmark

The first run downloads **tokenizer assets only** from the pinned Hugging Face revisions. The code never enables `trust_remote_code`.

```bash
brauer-tokenizer-benchmark --output-dir results --verify-manuscript
```

The `--verify-manuscript` flag stops with an error unless Tables 2 and 3 agree with the final manuscript at the displayed precision.

An exploratory corpus-wide type-collapse export is available with:

```bash
brauer-tokenizer-benchmark --output-dir results --verify-manuscript --type-collapse-corpus
```

That additional CSV is clearly marked exploratory because the paper reports a controlled fixed-length type-collapse experiment, not a corpus-wide aggregate for the refinement.

## Special tokens

The primary benchmark retains the special tokens added by each tokenizer. For the Table 2 control, the same tokenized sequence is also counted after removing positions marked by the tokenizer as special. This yields the manuscript shifts at `r=1`: `Delta C_B = 6, 6, 3, 0, 0` for BERT, RoBERTa, Mistral-7B, GPT-2, and Qwen2.5, respectively.

## Corpus reproducibility

The corpus is regenerated from seed `20260823` and sorted deterministically. The exact UTF-8 serialization used by the benchmark has SHA-256:

```text
6888d24246c8b121b6492b9b3132d49564c50149a86a4547c2a2d79fc5d7b9fb
```

To materialize the 500 sentences as a plain-text file, run:

```bash
python scripts/materialize_corpus.py
```

The benchmark does not rely on a mutable external corpus download: it regenerates the fixed sentence set directly from the published seed and templates, then checks its digest in the test suite.

## Cost-aware interpretation

At fixed `r`, ranking occurrence-baseline examples by `C_B` is equivalent to ranking them by token count. Across radii, `C_B` counts the exact number of window-token incidences induced by the local-context rule. It is not a monetary, hardware, runtime, or memory cost, which must be measured separately.

## Citation

See `CITATION.cff`. The software is released under the MIT License.

## Release verification

See [`VERIFICATION_REPORT.md`](VERIFICATION_REPORT.md) for the release audit. The repository also contains a manually triggered **Full manuscript benchmark** GitHub Actions workflow that downloads only the pinned tokenizer assets and runs the final Tables 2--3 fidelity gate.
