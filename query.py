import os

from dotenv import load_dotenv
from groq import Groq

from retriever import retrieve


SYSTEM_PROMPT = (
    "Answer only from the retrieved source text. "
    "If the retrieved text does not answer the question, say you do not have enough information. "
    "Do not use outside knowledge."
)


def format_context(chunks):
    blocks = []
    for index, chunk in enumerate(chunks, start=1):
        blocks.append(
            f"[{index}] source={chunk['source']} chunk={chunk['chunk_index']} "
            f"distance={chunk['distance']:.3f}\n{chunk['text']}"
        )
    return "\n\n".join(blocks)


def source_list(chunks):
    seen = []
    for chunk in chunks:
        label = f"{chunk['source']}#{chunk['chunk_index']}"
        if label not in seen:
            seen.append(label)
    return seen


def offline_answer(question, chunks):
    if not chunks or chunks[0]["distance"] > 0.8:
        answer = "I do not have enough information in the retrieved documents."
    else:
        answer = (
            "No GROQ_API_KEY is set, so this run returns retrieved evidence only.\n"
            f"Best evidence for: {question}\n\n{chunks[0]['text']}"
        )
    return {"answer": answer, "sources": source_list(chunks), "chunks": chunks}


def ask(question, top_k=5):
    load_dotenv()
    chunks = retrieve(question, top_k=top_k)
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return offline_answer(question, chunks)

    client = Groq(api_key=api_key)
    user_prompt = f"Question: {question}\n\nRetrieved sources:\n{format_context(chunks)}"
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
    )
    return {
        "answer": response.choices[0].message.content,
        "sources": source_list(chunks),
        "chunks": chunks,
    }
