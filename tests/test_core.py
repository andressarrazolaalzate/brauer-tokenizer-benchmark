import math, random, unittest
from brauer_tokenizer import (
    entropy_asymptotic_coefficient, occurrence_descriptors, occurrence_entropy_closed,
    type_collapsed_descriptors, verify_occurrence_closed_forms, verify_type_refinement_identity,
)

class CoreTests(unittest.TestCase):
    def test_explicit_reference_matches_closed_descriptors(self):
        self.assertEqual(verify_occurrence_closed_forms(12,3),48)
    def test_singleton_normalized_entropy_is_undefined(self):
        self.assertTrue(math.isnan(occurrence_descriptors(1,0).H_norm))
    def test_asymptotic_coefficients(self):
        for r,target in [(1,-0.12605),(2,-0.22998),(3,-0.32979)]:
            self.assertAlmostEqual(entropy_asymptotic_coefficient(r),target,places=5)
    def test_exact_entropy_closed_form(self):
        for r in range(1,7):
            for n in (2*r+1, 50, 200):
                self.assertAlmostEqual(occurrence_descriptors(n,r).HB, occurrence_entropy_closed(n,r), places=12)
    def test_unique_types_recover_baseline(self):
        tokens=["a","b","c","d","e"]
        for r in (1,2,3):
            o=occurrence_descriptors(len(tokens),r); t=type_collapsed_descriptors(tokens,r)
            self.assertEqual(t.CB,o.CB); self.assertAlmostEqual(t.HB,o.HB,places=12)
            self.assertEqual(t.dim_Lambda,o.dim_Lambda); self.assertEqual(t.dim_Z,o.dim_Z)
    def test_repetition_is_strict(self):
        tokens=["a","b","a","c","a"]
        for r in (1,2,3): verify_type_refinement_identity(tokens,r)
    def test_table4_exact(self):
        tokens=[f"u{i}" for i in range(1,24)]
        for p in (2,6,12,18): tokens[p-1]="repeat"
        expected={1:(67,3.130287202848717,2.881995675483960,176,284),2:(109,3.126406319823572,2.885510957684386,462,732),3:(149,3.123079491303721,2.882816355087436,884,1388)}
        for r,(cb,ho,ht,do,dt) in expected.items():
            o=occurrence_descriptors(23,r); t=type_collapsed_descriptors(tokens,r)
            self.assertEqual(o.CB,cb); self.assertAlmostEqual(o.HB,ho,places=12); self.assertAlmostEqual(t.HB,ht,places=12)
            self.assertEqual(o.dim_Lambda,do); self.assertEqual(t.dim_Lambda,dt); self.assertEqual(o.dim_Z,24); self.assertEqual(t.dim_Z,24)
    def test_no_duplicate_descriptor_keys(self):
        keys=list(occurrence_descriptors(5,1).to_dict()); self.assertEqual(len(keys),len(set(keys)))

if __name__ == '__main__': unittest.main()
