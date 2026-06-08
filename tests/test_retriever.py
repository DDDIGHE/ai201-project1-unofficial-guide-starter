import unittest

from retriever import keyword_overlap


class RetrieverTests(unittest.TestCase):
    def test_keyword_overlap_prefers_exact_warning_terms(self):
        question = "pay application fee or deposit before seeing the place"
        good = "Students should never pay an application fee or deposit before seeing the place in person."
        weak = "Students should document the move-in condition to protect the security deposit."

        self.assertGreater(keyword_overlap(question, good), keyword_overlap(question, weak))


if __name__ == "__main__":
    unittest.main()
