# Local AI Security Control Implementation Engine

> A local AI-powered engine for transforming security guidance into structured, architecture-aware control implementation outputs.

<p align="center">
  <b>Security Corpus Ingestion</b> •
  <b>Vector Retrieval</b> •
  <b>Control Guidance</b> •
  <b>Evidence Validation</b> •
  <b>Azure DevOps CI</b>
</p>

---

## Overview

Modern security teams work with large volumes of documentation, architecture references, and compliance frameworks.  
The challenge is not the lack of information — it is translating that information into **consistent and operational security control implementations**.

This project implements a **local AI-assisted security control implementation engine** that:

- ingests security documentation into a searchable knowledge base
- generates embeddings locally
- stores them in a vector database
- retrieves relevant security guidance through semantic search
- produces structured control implementation outputs
- associates controls with verifiable evidence
- validates workflows through CI pipelines

The entire system runs **locally** and does **not rely on external APIs**.

---

## Problem

Security documentation is often:

- extremely large
- fragmented across sources
- difficult to operationalize
- inconsistent across teams

This project explores a structured approach:

Security Documentation  
↓  
Semantic Retrieval  
↓  
Control Implementation Guidance  
↓  
Evidence Validation

Instead of manually navigating documents, the system enables **semantic retrieval and structured control implementation generation**.

---

## Core Capabilities

### Local Security Knowledge Retrieval

Transforms security documentation into a vector-searchable knowledge base.

### Control Context Construction

Builds contextual information required to map retrieved guidance to security control implementation.

### Evidence Validation Layer

Associates security controls with observable operational evidence for verification and audits.

### Continuous Integration Validation

Azure DevOps pipelines validate ingestion, retrieval functionality, and unit tests.

### Demonstration Control Outputs

Example controls included in the repository:

- **AC-4 — Information Flow Enforcement**
- **AU-2 — Audit Events**
- **SC-7 — Boundary Protection**

---

## System Architecture

Security Documents  
↓  
Text Chunking  
↓  
Embedding Generation (Ollama)  
↓  
Vector Database (Chroma)  
↓  
Semantic Retrieval  
↓  
Control Context Builder  
↓  
Control Implementation Engine  
↓  
Evidence Validation Layer  
↓  
Structured Security Control Output

---

## Repository Structure

local-control-engine/

corpus/  
Security documentation corpus

evidence_templates/  
Evidence validation templates

tests/  
Unit tests

vectorstore/  
Local vector database

ingest_corpus.py  
Corpus ingestion pipeline

query_corpus.py  
Semantic retrieval interface

control_implementation_engine.py  
Control implementation engine

control_context_builder.py  
Control context generation

control_query_builder.py  
Query generation logic

control_retriever.py  
Retrieval engine

control_runtime_validator.py  
Runtime validation

aws_security_baseline.py  
AWS baseline expectations

aws_evidence_collector.py  
Evidence collection helpers

aws_cloudtrail_evidence_collector.py  
CloudTrail validation helpers

architecture_deviation_detector.py  
Architecture deviation detection

enhancement_backlog_builder.py  
Improvement backlog generation

azure-pipelines.yml  
Azure DevOps CI pipeline

requirements.txt  
Python dependencies

README.md  
Project documentation

---

## Installation

Clone repository

```
git clone https://github.com/kasrarahnama/local-security-control-engine.git
cd local-security-control-engine
```

Install dependencies

```
pip install -r requirements.txt
```

Ensure **Ollama** is installed locally and the embedding model is available.

---

## Corpus Ingestion

Dry-run validation

```
python ingest_corpus.py --dry_run
```

Full ingestion

```
python ingest_corpus.py --rebuild
```

This process:

- loads documents
- splits them into chunks
- generates embeddings
- stores them in the vector database

Vector database location

```
vectorstore/aws_security
```

---

## Query the Security Corpus

Example semantic query

```
python query_corpus.py "least privilege"
```

JSON output

```
python query_corpus.py "least privilege" --json
```

---

## Demo Control Outputs

Example output file

```
demo_controls_output.json
```

Demonstration outputs include:

AC-4  
AU-2  
SC-7

---

## CI Validation

The project includes an Azure DevOps pipeline.

Pipeline tasks:

- dependency installation
- corpus ingestion validation
- retrieval smoke tests
- unit tests

Pipeline file

```
azure-pipelines.yml
```

---

## Evidence Validation Model

Security controls should not only describe configuration requirements but also define **how those configurations are verified**.

Evidence categories include:

- IAM Policies
- AWS Config
- CloudTrail Logs
- Flow Logs
- Monitoring Signals
- Application Logs

This aligns security implementation with **auditability and operational verification**.

---

## Future Work

Possible improvements include:

- architecture-to-control mapping automation
- expanded compliance framework support
- improved retrieval evaluation
- stronger output schemas
- enhanced evidence automation

---

## Technology Stack

Python  
Ollama (local embedding runtime)  
Chroma Vector Database  
Azure DevOps CI  
Security Control Engineering Concepts

---

## Author

Kasra Rahnama Fard  
Machine Learning • Security Systems • AI Engineering
