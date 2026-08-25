"""Pinned Hugging Face tokenizer definitions and safe loading helpers."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class TokenizerSpec:
    label: str
    hf_name: str
    family: str
    revision: str

# The revisions are immutable Hugging Face repository snapshots. The benchmark
# never enables remote model code; only tokenizer assets are loaded.
TOKENIZERS = (
    TokenizerSpec("BERT", "google-bert/bert-base-uncased", "WordPiece", "86b5e0934494bd15c9632b12f734a8a67f723594"),
    TokenizerSpec("RoBERTa", "FacebookAI/roberta-base", "byte-level BPE", "e2da8e2f811d1448a5b465c236feacd80ffbac7b"),
    TokenizerSpec("Mistral-7B", "mistralai/Mistral-7B-v0.1", "SentencePiece/BPE", "67b958e1e004930a761765ead7c72133cdbfe68d"),
    TokenizerSpec("GPT-2", "openai-community/gpt2", "BPE", "607a30d783dfa663caf39e06633721c8d4cfcd7e"),
    TokenizerSpec("Qwen2.5", "Qwen/Qwen2.5-0.5B-Instruct", "Qwen byte-level BPE", "7ae557604adf67be50417f59c2c2f167def9a775"),
)
TOKENIZER_ORDER = tuple(x.label for x in TOKENIZERS)


def load_tokenizer(spec: TokenizerSpec):
    try:
        from transformers import AutoTokenizer
    except ImportError as exc:
        raise RuntimeError("Install the benchmark dependencies with: pip install -e '.[benchmark]'") from exc
    return AutoTokenizer.from_pretrained(
        spec.hf_name,
        revision=spec.revision,
        use_fast=True,
        trust_remote_code=False,
    )


def tokenize_with_special_control(tokenizer, text: str) -> tuple[list[str], list[str]]:
    """Return token strings with model defaults, and the same sequence without specials."""
    encoded = tokenizer(
        text,
        add_special_tokens=True,
        return_attention_mask=False,
        return_token_type_ids=False,
        return_special_tokens_mask=True,
        truncation=False,
    )
    ids = list(encoded["input_ids"])
    mask = list(encoded.get("special_tokens_mask", [0] * len(ids)))
    tokens = tokenizer.convert_ids_to_tokens(ids)
    without_special = [tok for tok, flag in zip(tokens, mask) if not flag]
    return list(tokens), without_special
