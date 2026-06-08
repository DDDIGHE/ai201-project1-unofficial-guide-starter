# Project 1 Planning: The Unofficial Guide

## Domain

Off-campus housing advice for Stony Brook students. This information is hard to use because it is scattered across Reddit posts and student replies instead of one searchable source.

## Documents

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | r/SBU housing search thread | Budget and search advice | https://www.reddit.com/r/SBU/comments/1t4dx0z/off_campus_housing_for_sbu/ |
| 2 | r/SBU graduate roommate post | $900-$1000 roommate search | https://www.reddit.com/r/SBU/comments/1eeyvht |
| 3 | r/SBU housing quality thread | rent, roommates, deposits, old houses | https://www.reddit.com/r/SBU/comments/1rjtnja/off_campus_housing/ |
| 4 | r/SBU international student thread | scams, locations, search sites | https://www.reddit.com/r/SBU/comments/1b7oyij |
| 5 | r/SBU missed campus housing thread | Facebook group warning | https://www.reddit.com/r/SBU/comments/1dezhk7 |
| 6 | r/SBU official listing thread | official SBU listing access and limits | https://www.reddit.com/r/SBU/comments/13819jj |
| 7 | r/SBU low-budget room thread | $850-$900 search advice | https://www.reddit.com/r/SBU/comments/1jkuzt4 |
| 8 | r/SBU no-car close room thread | close housing and Lot 40 example | https://www.reddit.com/r/SBU/comments/1bq4xi3 |
| 9 | r/SBU bus-access housing post | bus access and deposit warning context | https://www.reddit.com/r/SBU/comments/1dc91y1 |
| 10 | r/SBU fall graduate budget thread | $1000 budget and Lot 40 example | https://www.reddit.com/r/SBU/comments/1cuwplk |

## Chunking Strategy

**Chunk size:** 360 characters.

**Overlap:** about 70 characters, implemented at word boundaries.

**Reasoning:** The documents are short Reddit-style posts and replies. Small chunks keep each warning or price point retrievable, while overlap keeps short housing advice from being split too harshly.

## Retrieval Approach

**Embedding model:** `sentence-transformers/all-MiniLM-L6-v2`.

**Top-k:** 5 returned chunks. ChromaDB first retrieves more candidates, then a small keyword overlap rerank fixes exact-warning queries like "deposit before seeing the place."

**Production tradeoff reflection:** For a real deployment I would compare a stronger embedding model, multilingual support, latency, and hosted API cost. I would also add source/date metadata filters.

## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Where should I search for an off-campus room under 900 dollars? | Shared-house bedrooms, SBU housing Facebook groups, Facebook Marketplace, Craigslist, bus stop posters, word of mouth, and Reddit. |
| 2 | Should I pay an application fee or deposit before seeing the place in person? | No; students warn not to pay fees or deposits before seeing the place. |
| 3 | If I have no car, should I stay near Stony Brook Road? | Yes; one reply says students without cars should stay in the Stony Brook area, especially around Stony Brook Road. |
| 4 | Are one-bedroom apartments near SBU usually more than 2000 dollars per month? | Yes; one reply says one-bedroom apartments near SBU are usually more than $2000 per month. |
| 5 | Which housing source has fewer scammers? | Private Facebook groups are described as having fewer scammers, but the system may confuse this with general scam warnings. |

## Anticipated Challenges

1. Many posts use overlapping terms like "deposit," so retrieval can confuse security-deposit advice with scam-deposit advice.

2. Reddit posts are short and informal, so a broad question can retrieve a related but incomplete chunk.

## Architecture

```text
documents/*.txt
  -> ingest.py cleans text and builds word-boundary chunks
  -> retriever.py embeds with all-MiniLM-L6-v2 and stores in ChromaDB
  -> retriever.py retrieves top candidates and reranks with keyword overlap
  -> query.py sends retrieved chunks to Groq if GROQ_API_KEY is set
  -> cli.py prints answer, sources, and retrieved chunks
```

## AI Tool Plan

**Milestone 3 — Ingestion and chunking:** Use Codex with the chunking section and source files as input. Verify with unit tests and `python ingest.py`.

**Milestone 4 — Embedding and retrieval:** Use Codex to wire ChromaDB and sentence-transformers. Verify with CLI queries and source/distance output.

**Milestone 5 — Generation and interface:** Use Codex to build a Groq-backed grounded prompt plus a CLI. Verify with in-domain and out-of-scope queries.
