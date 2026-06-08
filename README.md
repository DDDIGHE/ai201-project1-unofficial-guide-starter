# The Unofficial Guide — Project 1

## Domain

This system answers Stony Brook off-campus housing questions from student Reddit advice. It focuses on search channels, budgets, scam warnings, and car-free location advice.

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | r/SBU housing search thread | Reddit | https://www.reddit.com/r/SBU/comments/1t4dx0z/off_campus_housing_for_sbu/ |
| 2 | r/SBU graduate roommate post | Reddit | https://www.reddit.com/r/SBU/comments/1eeyvht |
| 3 | r/SBU housing quality thread | Reddit | https://www.reddit.com/r/SBU/comments/1rjtnja/off_campus_housing/ |
| 4 | r/SBU international student thread | Reddit | https://www.reddit.com/r/SBU/comments/1b7oyij |
| 5 | r/SBU missed campus housing thread | Reddit | https://www.reddit.com/r/SBU/comments/1dezhk7 |
| 6 | r/SBU official listing thread | Reddit | https://www.reddit.com/r/SBU/comments/13819jj |
| 7 | r/SBU low-budget room thread | Reddit | https://www.reddit.com/r/SBU/comments/1jkuzt4 |
| 8 | r/SBU no-car close room thread | Reddit | https://www.reddit.com/r/SBU/comments/1bq4xi3 |
| 9 | r/SBU bus-access housing post | Reddit | https://www.reddit.com/r/SBU/comments/1dc91y1 |
| 10 | r/SBU fall graduate budget thread | Reddit | https://www.reddit.com/r/SBU/comments/1cuwplk |

## Chunking Strategy

**Chunk size:** 360 characters.

**Overlap:** about 70 characters, kept on word boundaries.

**Why these choices fit your documents:** The documents are short posts and replies. Smaller chunks make specific price, scam, and location advice easier to retrieve.

**Final chunk count:** 23.

Sample chunks:

1. `sbu_housing_07_low_budget_search.txt#0`: budget around $850-$900 usually means a bedroom in a shared house.
2. `sbu_housing_07_low_budget_search.txt#1`: search Facebook groups, Marketplace, Craigslist, bus stop posters, or word of mouth; do not pay before seeing the place.
3. `sbu_housing_04_scams_and_locations.txt#1`: watch for people asking for money before a house is seen.
4. `sbu_housing_04_scams_and_locations.txt#2`: students without cars should stay in the Stony Brook area, especially Stony Brook Road.
5. `sbu_housing_01_where_to_search.txt#1`: one-bedroom apartments near SBU are usually more than $2000 per month.

## Embedding Model

**Model used:** `sentence-transformers/all-MiniLM-L6-v2`.

**Production tradeoff reflection:** I would compare stronger hosted embeddings against this local model for accuracy, latency, multilingual support, cost, and longer-context handling.

## Grounded Generation

**System prompt grounding instruction:** `Answer only from the retrieved source text. If the retrieved text does not answer the question, say you do not have enough information. Do not use outside knowledge.`

**How source attribution is surfaced in the response:** `cli.py` prints source filenames and chunk indexes after every answer. If `GROQ_API_KEY` is missing, the system returns retrieved evidence only instead of guessing.

## Query Interface

Run:

```bash
conda run -n machine_learning python retriever.py
conda run -n machine_learning python cli.py "Where should I search for an off-campus room under 900 dollars?"
```

Input is one question. Output includes an answer, source chunks, and retrieval distances.

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Where should I search for an off-campus room under 900 dollars? | Shared-house bedrooms and informal channels like SBU Facebook groups, Marketplace, Craigslist, posters, word of mouth, and Reddit. | Retrieved the $850-$900 shared-house source and related search sources. | Relevant | Accurate |
| 2 | Should I pay an application fee or deposit before seeing the place in person? | No; do not pay fees or deposits before seeing the place. | Retrieved the warning that students should never pay an application fee or deposit before seeing the place. | Relevant | Accurate |
| 3 | If I have no car, should I stay near Stony Brook Road? | Yes; stay in the Stony Brook area, especially around Stony Brook Road. | Retrieved the no-car/Stony Brook Road advice. | Relevant | Accurate |
| 4 | Are one-bedroom apartments near SBU usually more than 2000 dollars per month? | Yes. | Retrieved the chunk saying one-bedroom apartments near SBU are usually more than $2000 per month. | Relevant | Accurate |
| 5 | Which housing source has fewer scammers? | Private Facebook groups are described as having fewer scammers. | Retrieved general scam-warning chunks instead of the exact private-group comparison. | Partially relevant | Partially accurate |

Out-of-scope check: `Which professor gives the easiest exams?` returns `I do not have enough information in the retrieved documents.`

## Failure Case Analysis

**Question that failed:** Which housing source has fewer scammers?

**What the system returned:** It retrieved general scam warnings and advice to check places in person.

**Root cause (tied to a specific pipeline stage):** The retrieval stage matched the broad word "scammers" but did not rank the small chunk with the exact private Facebook group comparison high enough.

**What you would change to fix it:** Add metadata tags for `source_type` and `risk_type`, or use a stronger reranker that handles comparison questions better.

## Spec Reflection

**One way the spec helped you during implementation:** The spec kept the project narrow: one domain, ten local source files, one embedding model, and one CLI. That made it easier to test each stage without adding a web scraper or a large UI.

**One way your implementation diverged from the spec, and why:** I added a small keyword-overlap rerank after semantic retrieval. The pure embedding search confused similar housing-deposit chunks, so the rerank improved exact warning questions without adding a full hybrid-search system.

## AI Usage

**Instance 1**

- *What I gave the AI:* The project requirements, the off-campus housing domain, and the ten source notes.
- *What it produced:* A minimal ingestion, chunking, retrieval, and CLI structure.
- *What I changed or overrode:* I kept only the required path and removed stretch features.

**Instance 2**

- *What I gave the AI:* A failing retrieval example about paying a deposit before seeing a place.
- *What it produced:* A small keyword-overlap rerank idea.
- *What I changed or overrode:* I limited it to sorting existing ChromaDB candidates instead of building a separate BM25 index.
