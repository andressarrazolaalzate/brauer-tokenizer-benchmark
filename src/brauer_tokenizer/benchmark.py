"""Full 500-sentence tokenizer benchmark and manuscript-table export."""
from __future__ import annotations
import argparse
import csv
import json
import math
from pathlib import Path
from statistics import mean

from .core import occurrence_descriptors, type_collapsed_descriptors
from .corpus import generate_reference_corpus, validate_reference_corpus, corpus_sha256
from .manuscript import TABLE2, TABLE3_ENTROPY, TABLE3_GROWTH
from .tokenizers import TOKENIZERS, tokenize_with_special_control, load_tokenizer

RADII = (0, 1, 2, 3)


def _write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader(); writer.writerows(rows)


def run_benchmark(output_dir: str | Path, *, include_corpus_type_collapse: bool = False) -> dict:
    """Run the article benchmark. Network is needed only to fetch pinned tokenizer assets."""
    output = Path(output_dir); output.mkdir(parents=True, exist_ok=True)
    corpus_path = Path(__file__).resolve().parents[2] / "data" / "ciarp_english_sentences_500.txt"
    if corpus_path.exists():
        validate_reference_corpus(corpus_path)
        sentences = corpus_path.read_text(encoding="utf-8").splitlines()
    else:
        sentences = generate_reference_corpus()

    rows: list[dict] = []
    token_rows: list[dict] = []
    type_rows: list[dict] = []
    for spec in TOKENIZERS:
        tokenizer = load_tokenizer(spec)
        for text_id, text in enumerate(sentences, 1):
            tokens, tokens_excl = tokenize_with_special_control(tokenizer, text)
            token_rows.append({
                "text_id": text_id, "tokenizer": spec.label, "text": text,
                "n_tokens_incl": len(tokens), "n_tokens_excl": len(tokens_excl),
                "n_special_tokens": len(tokens)-len(tokens_excl),
                "tokens": " ".join(tokens),
            })
            for radius in RADII:
                d = occurrence_descriptors(len(tokens), radius)
                rows.append({"text_id":text_id,"tokenizer":spec.label,"radius":radius,**d.to_dict()})
                if include_corpus_type_collapse and radius >= 1:
                    t = type_collapsed_descriptors(tokens, radius)
                    type_rows.append({"text_id":text_id,"tokenizer":spec.label,"radius":radius,**t.to_dict()})

    if len(rows) != 500 * len(TOKENIZERS) * len(RADII):
        raise AssertionError("unexpected occurrence-row count")
    _write_csv(output / "occurrence_benchmark.csv", rows)
    _write_csv(output / "tokens_by_sentence.csv", token_rows)
    if type_rows:
        _write_csv(output / "type_collapse_corpus_exploratory.csv", type_rows)

    table2 = []
    for spec in TOKENIZERS:
        tr = [x for x in token_rows if x["tokenizer"] == spec.label]
        r1 = [x for x in rows if x["tokenizer"] == spec.label and x["radius"] == 1]
        table2.append({
            "tokenizer": spec.label,
            "mean_N_incl": mean(x["n_tokens_incl"] for x in tr),
            "mean_N_excl": mean(x["n_tokens_excl"] for x in tr),
            "mean_CB_incl": mean(x["CB"] for x in r1),
            "mean_HB": mean(x["HB"] for x in r1),
            "mean_dim_Lambda": mean(x["dim_Lambda"] for x in r1),
            "delta_mean_CB": 3 * (mean(x["n_tokens_incl"] for x in tr)-mean(x["n_tokens_excl"] for x in tr)),
        })
    _write_csv(output / "table2_tokenizer_profile.csv", table2)

    table3 = []
    for radius in RADII:
        out = {"radius": radius}
        for spec in TOKENIZERS:
            rr = [x for x in rows if x["tokenizer"] == spec.label and x["radius"] == radius]
            out[f"HB_{spec.label}"] = mean(x["HB"] for x in rr)
            out[f"CB_{spec.label}"] = mean(x["CB"] for x in rr)
        table3.append(out)
    _write_csv(output / "table3_radius_control.csv", table3)

    metadata = {
        "corpus_seed": 20260823,
        "corpus_sha256": corpus_sha256(sentences),
        "n_sentences": len(sentences), "radii": list(RADII),
        "n_occurrence_evaluations": len(rows),
        "tokenizers": [spec.__dict__ for spec in TOKENIZERS],
        "corpus_type_collapse_exploratory": include_corpus_type_collapse,
    }
    (output / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return {"rows": rows, "token_rows": token_rows, "table2": table2, "table3": table3, "metadata": metadata}


def verify_manuscript_tables(result: dict) -> None:
    """Assert that a completed benchmark reproduces manuscript Tables 2 and 3."""
    t2 = {row["tokenizer"]: row for row in result["table2"]}
    fields = {
        "N_incl":"mean_N_incl", "N_excl":"mean_N_excl", "CB":"mean_CB_incl",
        "HB":"mean_HB", "dim_Lambda":"mean_dim_Lambda", "delta_CB":"delta_mean_CB"
    }
    for tokenizer, expected in TABLE2.items():
        for ek, ak in fields.items():
            if round(t2[tokenizer][ak], 3) != round(expected[ek], 3):
                raise AssertionError(f"Table 2 mismatch: {tokenizer} {ek}: {t2[tokenizer][ak]} != {expected[ek]}")

    by_radius = {row["radius"]: row for row in result["table3"]}
    for r, expected in TABLE3_ENTROPY.items():
        for tokenizer, value in expected.items():
            actual = by_radius[r][f"HB_{tokenizer}"]
            if round(actual, 3) != round(value, 3):
                raise AssertionError(f"Table 3 entropy mismatch: r={r}, {tokenizer}")
    for r, expected in TABLE3_GROWTH.items():
        for tokenizer, value in expected.items():
            cb1 = by_radius[1][f"CB_{tokenizer}"]; cbr = by_radius[r][f"CB_{tokenizer}"]
            actual = 100 * (cbr-cb1)/cb1
            if round(actual, 2) != round(value, 2):
                raise AssertionError(f"Table 3 growth mismatch: r={r}, {tokenizer}: {actual} != {value}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Reproduce the 500-sentence CIARP Brauer tokenizer benchmark.")
    parser.add_argument("--output-dir", default="results")
    parser.add_argument("--type-collapse-corpus", action="store_true", help="Also export exploratory corpus-wide type-collapse descriptors (not reported in the article).")
    parser.add_argument("--verify-manuscript", action="store_true", help="Require rounded Tables 2 and 3 to match the final article.")
    args = parser.parse_args()
    result = run_benchmark(args.output_dir, include_corpus_type_collapse=args.type_collapse_corpus)
    if args.verify_manuscript:
        verify_manuscript_tables(result)
        print("Manuscript Tables 2 and 3 reproduced exactly at their reported precision.")
    print(f"Wrote benchmark outputs to {args.output_dir}")

if __name__ == "__main__":
    main()
