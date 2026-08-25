import json, math, statistics, unittest
from pathlib import Path
from brauer_tokenizer.corpus import generate_reference_corpus, corpus_sha256, validate_reference_corpus
from brauer_tokenizer.manuscript import TABLE2, TABLE3_GROWTH

class CorpusAndManuscriptTests(unittest.TestCase):
    def test_corpus_digest_and_stats(self):
        s=generate_reference_corpus(); self.assertEqual(len(s),500); self.assertEqual(len(set(s)),500)
        self.assertEqual(corpus_sha256(s),"6888d24246c8b121b6492b9b3132d49564c50149a86a4547c2a2d79fc5d7b9fb")
        words=[len(x.split()) for x in s]; chars=[len(x) for x in s]
        self.assertAlmostEqual(statistics.mean(words),18.722,places=3); self.assertAlmostEqual(statistics.pstdev(words),2.0949262516852474,places=12)
        self.assertEqual((min(words),max(words)),(13,23)); self.assertAlmostEqual(statistics.mean(chars),124.354,places=3)
        self.assertEqual((min(chars),max(chars)),(77,153))
    def test_distributed_corpus_is_regeneration(self):
        root=Path(__file__).resolve().parents[1]; validate_reference_corpus(root/'data/ciarp_english_sentences_500.txt')
    def test_table2_affine_arithmetic(self):
        for row in TABLE2.values():
            self.assertAlmostEqual(3*row['N_incl']-2,row['CB'],places=3)
            self.assertAlmostEqual(8*row['N_incl']-8,row['dim_Lambda'],places=3)
            self.assertAlmostEqual(3*(row['N_incl']-row['N_excl']),row['delta_CB'],places=3)

    def test_public_expected_table_file_matches_constants(self):
        root=Path(__file__).resolve().parents[1]
        data=json.loads((root/'expected/manuscript_tables.json').read_text(encoding='utf-8'))
        order=['N_incl','N_excl','CB','HB','dim_Lambda','delta_CB']
        for label,row in TABLE2.items():
            self.assertEqual(data['table2'][label], [row[k] for k in order])
        for r,vals in TABLE3_GROWTH.items():
            self.assertEqual(data['table3_cost_growth_percent'][str(r)], vals)

    def test_table3_cost_growth_from_mean_length(self):
        for label,row in TABLE2.items():
            cb1=3*row['N_incl']-2
            cb2=5*row['N_incl']-6; cb3=7*row['N_incl']-12
            self.assertAlmostEqual(100*(cb2-cb1)/cb1,TABLE3_GROWTH[2][label],places=2)
            self.assertAlmostEqual(100*(cb3-cb1)/cb1,TABLE3_GROWTH[3][label],places=2)

if __name__ == '__main__': unittest.main()
