from pathlib import Path
import re


DOCUMENTS_DIR = Path("documents")
CHUNK_SIZE = 360
CHUNK_OVERLAP = 70


def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()


def load_documents(directory=DOCUMENTS_DIR):
    docs = []
    for path in sorted(Path(directory).glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        docs.append({"source": path.name, "text": clean_text(text)})
    return docs


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    text = clean_text(text)
    if not text:
        return []
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        current = []
        length = 0
        index = start
        while index < len(words):
            next_length = length + len(words[index]) + (1 if current else 0)
            if current and next_length > chunk_size:
                break
            current.append(words[index])
            length = next_length
            index += 1

        chunks.append(" ".join(current))
        if index == len(words):
            break

        overlap_length = 0
        overlap_count = 0
        for word in reversed(current):
            next_length = overlap_length + len(word) + (1 if overlap_count else 0)
            if next_length > overlap:
                break
            overlap_length = next_length
            overlap_count += 1
        start = max(start + 1, index - overlap_count)
    return chunks


def build_chunks(directory=DOCUMENTS_DIR, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    for doc in load_documents(directory):
        for index, text in enumerate(chunk_text(doc["text"], chunk_size, overlap)):
            chunks.append(
                {
                    "id": f"{Path(doc['source']).stem}-{index}",
                    "text": text,
                    "source": doc["source"],
                    "chunk_index": index,
                }
            )
    return chunks


if __name__ == "__main__":
    chunks = build_chunks()
    print(f"documents={len(load_documents())}")
    print(f"chunks={len(chunks)}")
    for chunk in chunks[:5]:
        print(f"\n[{chunk['source']} #{chunk['chunk_index']}]\n{chunk['text']}")
