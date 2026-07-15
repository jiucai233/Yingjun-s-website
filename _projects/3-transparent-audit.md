---
layout: page
title: "Transparent-Audit: Smart Receipt Audit System"
description: Automated receipt audit pipeline using PaddleOCR, RAG with ChromaDB, and LLM-based compliance reasoning
importance: 4
category: work
github: https://github.com/jiucai233/28th-project-receiptaudit-dev
img: assets/img/transparent-audit-cover.png
---

## Background

Organizations need to verify that employee expense receipts comply with internal financial policies. **Transparent-Audit** automates this process end-to-end: from receipt image upload to compliance verdict, using OCR, vector-based policy retrieval, and LLM reasoning.

## Architecture

The system follows a modular pipeline:

```
Receipt Image → OCR Engine → RAG Policy Retrieval → AI Auditor → PDF Report
```

### 1. OCR & Preprocessing
PaddleOCR extracts text from receipt images with automated skew correction and rotation handling. Structured fields (merchant, timestamp, items, prices, totals) are parsed from raw OCR output.

### 2. RAG Policy Retrieval
Organization policy PDFs are ingested, chunked, and embedded into a **ChromaDB** vector database. Given a parsed receipt, the system retrieves the most relevant policy clauses via semantic search — achieving **94.7% recall**.

### 3. AI Auditing Agent
A **LangChain**-driven reasoning agent analyzes the receipt against retrieved policy clauses, detecting violations such as late-night purchases, restricted merchants, and unauthorized expenses.

### 4. Report Generation
Audit verdicts, risk scores, and violation details are compiled into PDF reports.

## Benchmark Results

| Metric | Score |
|--------|-------|
| OCR baseline field accuracy | 76.4% |
| Skew correction improvement | +35.7% (22.7% → 58.4%) |
| RAG recall (top 3) | 84.6% |
| End-to-end accuracy (ground truth input) | 92.0% |
| End-to-end accuracy (OCR-parsed input) | 86.0% |

A key finding: sequential LLM correction cycles *degrade* accuracy due to hallucination — single-pass processing is optimal.

## Tech Stack

**Backend:** FastAPI, PaddleOCR, ChromaDB, LangChain, Upstage LLM API
**Frontend:** React, TypeScript, Vite, TailwindCSS
**DevOps:** Docker, Docker Compose
