"""Materialize the deterministic 500-sentence corpus as a UTF-8 text file."""
from __future__ import annotations
from pathlib import Path
from brauer_tokenizer.corpus import generate_reference_corpus, corpus_sha256, corpus_text

out = Path("data") / "ciarp_english_sentences_500.txt"
out.parent.mkdir(parents=True, exist_ok=True)
sentences = generate_reference_corpus()
out.write_text(corpus_text(sentences), encoding="utf-8")
print(f"Wrote {len(sentences)} sentences to {out}")
print(f"SHA-256: {corpus_sha256(sentences)}")
