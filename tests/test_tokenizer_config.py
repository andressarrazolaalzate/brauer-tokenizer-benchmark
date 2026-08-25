import unittest
from brauer_tokenizer.tokenizers import TOKENIZERS
class ConfigTests(unittest.TestCase):
    def test_five_pinned_tokenizers(self):
        self.assertEqual(len(TOKENIZERS),5)
        for spec in TOKENIZERS:
            self.assertTrue(spec.revision); self.assertNotEqual(spec.revision,'main')
if __name__ == '__main__': unittest.main()
