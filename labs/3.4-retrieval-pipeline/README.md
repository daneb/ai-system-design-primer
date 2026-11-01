# Lab 3.4: Keyword vs dense vs hybrid retrieval

Supports section [3.4 Retrieval pipeline](../../docs/3-components/3.4-retrieval-pipeline.md).

**Question:** when does fusing a keyword retriever with a dense retriever (Reciprocal Rank Fusion)
actually help?

## Run it

```sh
python3 hybrid_rrf.py            # summary table
python3 hybrid_rrf.py --verbose  # top-5 ranking per query and retriever
```

Needs Python 3.9+ and numpy. No network.

## Set-up

- `corpus.json`: 24 short, fictional bank-policy documents and 14 queries of three types: **exact**
  (identifiers such as `TX-4471`), **paraphrase** (different vocabulary from the document) and
  **mixed**. Relevant documents were labelled before any retriever was run.
- **Keyword:** BM25 (k1 = 1.5, b = 0.75), with identifiers such as `tx-4471` kept as single tokens.
- **Dense:** latent semantic analysis (TF-IDF + truncated SVD, 12 dimensions). This is a classical
  stand-in because neither the author's machine nor the build environment could download a neural
  embedding model. It is much weaker than a modern embedding model.
- **Hybrid:** RRF with c = 60, as in Cormack, Clarke & Buettcher (SIGIR 2009) and Azure AI Search.

## Result (run 2026-11-01)

recall@3 / MRR:

| System | exact | paraphrase | mixed | all |
|---|---|---|---|---|
| keyword (BM25) | 1.00 / 1.00 | 0.67 / 0.67 | 1.00 / 0.88 | 0.86 / 0.82 |
| dense (LSA) | 1.00 / 1.00 | 0.67 / 0.71 | 1.00 / 1.00 | 0.86 / 0.88 |
| hybrid (RRF) | 1.00 / 1.00 | 0.67 / 0.71 | 1.00 / 0.88 | 0.86 / 0.84 |

## What it shows

1. **Keyword search is reliable for identifiers.** BM25 put the right document first for every exact
   query, including telling `TX-4471` apart from `TX-4417`. Anthropic's contextual retrieval post makes
   the same argument with an error-code example.
2. **Fusion only helps when the retrievers make different mistakes.** Both retrievers missed the same
   two queries: "expensive present" (the document says "gifts") and "clicked a suspicious link" (the
   document says "phishing"). LSA is built from the same word statistics as BM25, so it shares its
   blind spots. RRF can only re-order what at least one retriever found; it cannot recover a document
   that neither retrieved.
3. **Fusion can demote a correct answer.** For "paste confidential data into a public chatbot", LSA
   ranked the right document first and BM25 ranked it second; after fusion it was second. This is one
   reason production pipelines put a reranker after fusion: fusion is for recall, reranking for
   precision.

The lab does **not** measure the size of the benefit of hybrid search. Use the published results for
that (Anthropic's contextual retrieval experiments; Microsoft's Azure AI Search relevance benchmarks)
and your own evaluation set.

## Exercises

1. Replace `LSA.embed()` with a neural embedding model (any provider, or a local
   sentence-transformers model) and re-run. Do the two paraphrase failures move? Does RRF now beat both
   retrievers?
2. Add query rewriting before retrieval: ask a model to restate each query in the vocabulary of a
   policy document, retrieve with the rewrite, and fuse it with the original.
3. Add a reranker after RRF and measure MRR again.
4. Write five more queries of your own before running them, and see whether the conclusions hold.
