Local Control Engine

This project implements a local knowledge retrieval engine for security guidance documents.

The system ingests security documentation such as the AWS Well-Architected Security Pillar, generates embeddings using a local embedding model, stores them in a vector database, and enables semantic search over the corpus.

The long-term goal of this project is to build a Control Implementation Engine that can retrieve relevant security guidance and generate structured security control implementations.

⸻

Architecture

The system currently implements the following pipeline:

Corpus Documents
↓
Text Chunking
↓
Embedding Generation (Ollama)
↓
Chroma Vector Database
↓
Semantic Retrieval
↓
Command Line Query Tool
↓
CI Retrieval Validation

⸻

Project Structure

local-control-engine

corpus/
 aws-well-architected/

vectorstore/
 aws_security/

ingest_corpus.py
query_corpus.py
azure-pipelines.yml
requirements.txt
README.md

⸻

Installation

Create a virtual environment:

python3 -m venv .venv
source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Make sure Ollama is installed and running locally.

Pull the embedding model:

ollama pull nomic-embed-text

⸻

Ingesting the Corpus

Before querying the system, documents must be ingested and embedded.

Dry run validation:

python ingest_corpus.py –dry_run

Full ingestion:

python ingest_corpus.py –rebuild –chunk_tokens 600 –overlap_tokens 80 –max_embed_tokens 256 –batch_size 8

This process will:

load documents from the corpus
split them into chunks
generate embeddings
store them in the vector database

The vector database will be created at:

vectorstore/aws_security

⸻

Querying the Corpus

Run semantic search over the corpus.

Example query:

python query_corpus.py “least privilege” –k 3

JSON output:

python query_corpus.py “least privilege” –k 3 –json

Require a minimum number of results:

python query_corpus.py “least privilege” –k 3 –min_results 1

If fewer than the required results are returned, the script exits with exit code 1.

⸻

CI Smoke Test

Azure Pipelines validates retrieval functionality using the following command:

python query_corpus.py “least privilege” –k 3 –min_results 1

This ensures:

the vectorstore loads correctly
embeddings exist
semantic retrieval works

⸻

Important Notes

The directory

vectorstore/

contains local runtime data and must not be committed to the repository.

It is ignored using .gitignore.

⸻

Future Development

The next phase of the project will implement a Control Implementation Engine.

Planned architecture:

Architecture Input (JSON)
↓
Retrieve Relevant Security Guidance
↓
Local LLM Reasoning
↓
Structured Control Implementation Output

This will enable automated generation of security control guidance based on architecture inputs.

⸻

Contributing

Contributions are welcome.

Possible areas of improvement include:

improved chunking strategies
additional corpus sources
improved retrieval ranking
structured control generation

Please submit pull requests with clear descriptions of the changes.