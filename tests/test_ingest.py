import tempfile
import unittest
from pathlib import Path

from ingest import chunk_text, load_documents


class IngestTests(unittest.TestCase):
    def test_chunk_text_keeps_chunks_bounded_and_readable(self):
        text = " ".join(f"word{i}" for i in range(160))

        chunks = chunk_text(text, chunk_size=180, overlap=40)

        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(0 < len(chunk) <= 180 for chunk in chunks))
        self.assertGreater(len(set(chunks[0].split()) & set(chunks[1].split())), 0)
        original_words = set(text.split())
        for chunk in chunks:
            for word in chunk.split():
                self.assertIn(word, original_words)

    def test_load_documents_reads_text_files_with_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.txt"
            path.write_text("Title: Sample\nSource: local\n\nBody text.", encoding="utf-8")

            docs = load_documents(tmp)

        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0]["source"], "sample.txt")
        self.assertIn("Body text.", docs[0]["text"])


if __name__ == "__main__":
    unittest.main()
