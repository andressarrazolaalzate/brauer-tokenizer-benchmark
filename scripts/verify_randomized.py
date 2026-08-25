"""Fixed-seed stress test of Proposition 9: 5,075 controlled random cases."""
from __future__ import annotations
import random
from brauer_tokenizer import verify_type_refinement_identity

rng=random.Random(20260825)
cases=0
for n in range(2,31):
    for r in range(1,8):
        for _ in range(25):
            vocab_size=rng.randint(1,n)
            tokens=[f"t{rng.randrange(vocab_size)}" for _ in range(n)]
            verify_type_refinement_identity(tokens,r)
            cases += 1
assert cases == 5075
print(f"Verified Proposition 9 on {cases} fixed-seed random cases.")
