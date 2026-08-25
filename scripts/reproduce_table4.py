"""Reproduce the fixed-length type-collapse experiment reported as Table 4."""
from __future__ import annotations
import csv
from pathlib import Path
from brauer_tokenizer import occurrence_descriptors, type_collapsed_descriptors, verify_type_refinement_identity

TOKENS = [f"u{i}" for i in range(1, 24)]
for position in (2, 6, 12, 18):
    TOKENS[position - 1] = "repeat"
assert len(TOKENS) == 23 and len(set(TOKENS)) == 20

rows=[]
for r in (1,2,3):
    o=occurrence_descriptors(23,r); t=type_collapsed_descriptors(TOKENS,r)
    verify_type_refinement_identity(TOKENS,r)
    rows.append({"radius":r,"CB":o.CB,"HB":o.HB,"HB_type":t.HB,"delta_H":t.HB-o.HB,
                 "dim_Lambda":o.dim_Lambda,"dim_Lambda_type":t.dim_Lambda,"ratio":t.dim_Lambda/o.dim_Lambda,
                 "dim_Z":o.dim_Z,"dim_Z_type":t.dim_Z})
out=Path("results"); out.mkdir(exist_ok=True)
path=out/"table4_type_collapse.csv"
with path.open("w",newline="",encoding="utf-8") as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for x in rows:
    print(f"r={x['radius']}: CB={x['CB']}, HB={x['HB']:.4f}, H~= {x['HB_type']:.4f}, ΔH={x['delta_H']:.4f}, dim={x['dim_Lambda']}, dim~={x['dim_Lambda_type']}, ratio={x['ratio']:.2f}, Z={x['dim_Z']}")
print(path)
