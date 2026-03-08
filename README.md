# Local AI Security Control Implementation Engine

A local AI-assisted security control implementation engine that retrieves security best-practice guidance and generates structured control implementation outputs for cloud architectures.

This project demonstrates how security documentation (such as the AWS Well-Architected Security Pillar) can be transformed into a searchable knowledge base and used to generate structured implementation guidance for security controls.

The system runs fully locally and does not rely on external APIs.

---

# Problem

Security teams often need to translate architecture descriptions into concrete security control implementations.

However:

• Security documentation is large and fragmented  
• Manual control interpretation is slow  
• Implementation guidance is inconsistent across teams  

This project explores how a **local retrieval-augmented architecture analysis engine** can assist in generating consistent and structured control implementation guidance.

---

# Key Features

• Local semantic retrieval engine for security documentation  
• Vector database powered by Chroma  
• Local embedding generation using Ollama  
• Architecture-aware control context building  
• Structured control implementation output  
• Evidence validation model for security controls  
• CI validation pipeline using Azure DevOps  
• Demo-ready control outputs (AC-4, AU-2, SC-7)

---

# System Architecture

The pipeline implemented in this project:

Corpus Documents  
↓  
Text Chunking  
↓  
Embedding Generation (Local Model via Ollama)  
↓  
Vector Storage (Chroma DB)  
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

# Repository Structure

local-control-engine/

corpus/                     Security documentation corpus  
evidence_templates/         Evidence validation templates  
tests/                      Unit tests  

ingest_corpus.py            Corpus ingestion pipeline  
query_corpus.py             Semantic retrieval CLI  

control_implementation_engine.py  
control_context_builder.py  
control_query_builder.py  
control_retriever.py  
control_runtime_validator.py  

aws_security_baseline.py  
aws_evidence_collector.py  
aws_cloudtrail_evidence_collector.py  

architecture_deviation_detector.py  
enhancement_backlog_builder.py  

azure-pipelines.yml         CI validation pipeline  
requirements.txt  
README.md  

---

# Setup

Clone the repository

git clone https://github.com/kasrarahnama/local-security-control-engine.git

cd local-security-control-engine

Install dependencies

pip install -r requirements.txt

---

# Ingest Security Corpus

Before querying the system, the security documentation must be ingested and embedded.

Dry run validation

python ingest_corpus.py --dry_run

Full ingestion

python ingest_corpus.py --rebuild

This process will:

• load documents from the corpus  
• split them into chunks  
• generate embeddings  
• store them in the vector database  

Vector store location

vectorstore/aws_security

---

# Query the Security Corpus

Run semantic search over the corpus.

Example query

python query_corpus.py "least privilege"

JSON output

python query_corpus.py "least privilege" --json

---

# Demo Controls

The repository includes demonstration outputs for several security controls:

AC-4 — Information Flow Enforcement  
AU-2 — Audit Events  
SC-7 — Boundary Protection  

Example output file:

demo_controls_output.json

---

# CI Validation

The project includes a CI pipeline using Azure DevOps.

Pipeline checks include:

• dependency installation  
• corpus ingestion validation  
• retrieval smoke tests  
• unit tests  

Defined in:

azure-pipelines.yml

---

# Future Improvements

• Support for additional compliance frameworks (NIST, ITSG-33)  
• Automated architecture analysis from OSCAL inputs  
• Integration with security telemetry sources  
• Enhanced control validation workflows  

---

# Author

Kasra Rahnama Fard

Machine Learning & Security Systems Engineering
