from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from ingest import build_chunks


DB_DIR = "chroma_db"
COLLECTION = "sbu_off_campus_housing"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
STOPWORDS = {
    "about",
    "after",
    "before",
    "could",
    "from",
    "have",
    "into",
    "near",
    "place",
    "should",
    "that",
    "the",
    "there",
    "what",
    "when",
    "where",
    "which",
    "with",
    "would",
}


_model = None


def embedding_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def collection(reset=False):
    client = chromadb.PersistentClient(path=DB_DIR)
    if reset:
        try:
            client.delete_collection(COLLECTION)
        except Exception:
            pass
    return client.get_or_create_collection(
        COLLECTION,
        metadata={"hnsw:space": "cosine"},
    )


def embed(texts):
    vectors = embedding_model().encode(texts, normalize_embeddings=True)
    return vectors.tolist()


def keyword_overlap(question, text):
    query_terms = {
        word.strip(".,?!:;()[]").lower()
        for word in question.split()
        if len(word.strip(".,?!:;()[]")) >= 4
    }
    query_terms -= STOPWORDS
    text_lower = text.lower()
    return sum(1 for term in query_terms if term in text_lower)


def rebuild_index():
    col = collection(reset=True)
    chunks = build_chunks()
    col.add(
        ids=[chunk["id"] for chunk in chunks],
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[
            {"source": chunk["source"], "chunk_index": chunk["chunk_index"]}
            for chunk in chunks
        ],
        embeddings=embed([chunk["text"] for chunk in chunks]),
    )
    return len(chunks)


def ensure_index():
    col = collection()
    if col.count() == 0:
        rebuild_index()
        col = collection()
    return col


def retrieve(question, top_k=5):
    col = ensure_index()
    candidate_count = min(max(top_k * 4, 20), col.count())
    results = col.query(
        query_embeddings=embed([question]),
        n_results=candidate_count,
        include=["documents", "metadatas", "distances"],
    )
    rows = []
    for text, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        rows.append(
            {
                "text": text,
                "source": metadata["source"],
                "chunk_index": metadata["chunk_index"],
                "distance": float(distance),
            }
        )
    rows.sort(key=lambda row: row["distance"] - 0.04 * keyword_overlap(question, row["text"]))
    return rows[:top_k]


if __name__ == "__main__":
    count = rebuild_index()
    print(f"indexed_chunks={count}")
    print(f"db={Path(DB_DIR).resolve()}")
