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

Modern security teams often work with large volumes of guidance, reference architectures, control catalogs, and audit requirements.  
The challenge is not the lack of information — it is turning that information into **clear, consistent, and verifiable control implementation guidance**.

This project is a **local AI-assisted security control implementation engine** that:

- ingests security documentation into a local searchable knowledge base
- builds embeddings and stores them in a vector database
- retrieves relevant guidance for a given security topic or control
- supports structured control implementation outputs
- defines evidence validation expectations for audit readiness
- validates the workflow through an Azure DevOps CI pipeline

The system runs **fully locally** and does **not rely on external APIs**.

---

## Why This Project Exists

Security guidance is usually:

- long
- fragmented
- difficult to operationalize
- inconsistent across teams

This project explores a more practical approach:

**Security documents → semantic retrieval → implementation guidance → evidence-oriented validation**

Instead of manually searching through documentation every time, the engine allows security knowledge to be retrieved and reused in a more structured and repeatable way.

---

## Core Capabilities

### Local Security Knowledge Retrieval
Transforms security guidance documents into a vector-searchable knowledge base for semantic retrieval.

### Architecture-Aware Control Context
Supports the idea of connecting retrieved guidance to control implementation logic and architecture context.

### Evidence Validation Model
Introduces evidence categories and verification expectations so that controls are not only described, but also tied to operational proof.

### CI Validation Pipeline
Uses Azure DevOps to automatically validate environment setup, corpus ingestion, retrieval flow, and unit tests.

### Demo-Ready Outputs
Includes demonstration outputs for security controls such as:

- **AC-4** — Information Flow Enforcement
- **AU-2** — Audit Events
- **SC-7** — Boundary Protection

---

## System Flow

```text
Security Documents
        ↓
Text Chunking
        ↓
Embedding Generation (Ollama)
        ↓
Chroma Vector Store
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

Repository Structure
local-control-engine/
│
├── corpus/                              # Security documentation corpus
├── evidence_templates/                  # Evidence validation templates
├── tests/                               # Unit tests
├── vectorstore/                         # Local vector database artifacts
│
├── ingest_corpus.py                     # Corpus ingestion pipeline
├── query_corpus.py                      # Semantic retrieval CLI
├── control_implementation_engine.py     # Core control implementation logic
├── control_context_builder.py           # Control context generation
├── control_query_builder.py             # Query construction logic
├── control_retriever.py                 # Retrieval layer
├── control_runtime_validator.py         # Runtime validation helpers
│
├── aws_security_baseline.py             # Baseline expectations
├── aws_evidence_collector.py            # Evidence collection logic
├── aws_cloudtrail_evidence_collector.py # CloudTrail evidence logic
│
├── architecture_deviation_detector.py   # Architecture deviation checks
├── enhancement_backlog_builder.py       # Backlog generation from deviations
│
├── azure-pipelines.yml                  # Azure DevOps CI pipeline
├── requirements.txt                     # Python dependencies
└── README.md

Local Setup

1. Clone the repository
git clone https://github.com/kasrarahnama/local-security-control-engine.git
cd local-security-control-engine
2. Install dependencies
pip install -r requirements.txt
3. Make sure Ollama is available locally

This project uses a local embedding model workflow.
You should have Ollama installed and the required model available on your machine.

⸻

Ingest the Security Corpus

Before querying the system, the corpus must be processed and embedded.

Dry-run validation
python ingest_corpus.py --dry_run
Full ingestion
python ingest_corpus.py --rebuild
This step:
	•	loads documents from the corpus
	•	splits them into chunks
	•	generates embeddings locally
	•	stores them in the vector database

Vector store location
vectorstore/aws_security
Query the Corpus

Once the corpus is ingested, semantic retrieval can be used to search for relevant security guidance.

Example query
python query_corpus.py "least privilege"
JSON output
python query_corpus.py "least privilege" --json
Example Project Goal

The long-term direction of this project is to support a workflow where security architecture inputs and retrieved guidance can be combined to produce more structured security control implementation outputs.

In other words, the engine is designed as a stepping stone toward:
	•	architecture-aware control generation
	•	repeatable control implementation logic
	•	evidence-oriented validation
	•	local AI-assisted security engineering workflows

⸻

CI / Validation Pipeline

The repository includes an Azure DevOps pipeline that validates core project functionality.

Pipeline checks include
	•	dependency installation
	•	local environment setup
	•	corpus ingestion validation
	•	unit test execution
	•	retrieval smoke testing

Pipeline definition:
azure-pipelines.yml
Evidence Validation Perspective

A major design idea in this project is that a security control is not complete if it is only described.
It should also be tied to observable evidence.

This project includes an evidence validation model that maps implementation expectations to categories such as:
	•	IAM policies
	•	SCPs
	•	AWS Config
	•	CloudTrail
	•	Flow Logs
	•	Application Logs

This makes the project more aligned with practical audit and operational verification thinking.

⸻

Future Improvements

Planned extensions include:
	•	richer control generation workflows
	•	stronger architecture-to-control mapping
	•	broader framework support (e.g. NIST, ITSG-33)
	•	enhanced retrieval evaluation
	•	more advanced evidence automation
	•	improved output schemas for control implementation

⸻

Tech Stack
<p>
  <img src="https://img.shields.io/badge/Python-3.x-blue" />
  <img src="https://img.shields.io/badge/Ollama-Local%20LLM%20Runtime-black" />
  <img src="https://img.shields.io/badge/Chroma-Vector%20Database-brightgreen" />
  <img src="https://img.shields.io/badge/Azure%20DevOps-CI%2FCD-blueviolet" />
  <img src="https://img.shields.io/badge/Security-Control%20Engineering-darkred" />
</p>
