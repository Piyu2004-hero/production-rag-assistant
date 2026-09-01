# 🚀 Production RAG Assistant

A production-style **Retrieval-Augmented Generation (RAG)** system that enables users to upload documents and ask questions using grounded, context-aware AI responses.

This project goes beyond a basic chatbot by implementing a modular AI engineering architecture with document ingestion, semantic chunking, embeddings, FAISS vector search, query rewriting, reranking, LLM generation, response validation, source citations, streaming responses, and API-based integration.

---

## 📌 Project Overview

The **Production RAG Assistant** processes user-provided documents and uses their content as the knowledge base for answering questions.

Supported document formats:

* 📄 PDF
* 📝 TXT
* 📘 Markdown (`.md`)

The system converts uploaded documents into searchable vector representations and retrieves the most relevant information whenever the user asks a question.

### Core Pipeline

```text
                    DOCUMENT INGESTION
                           │
                           ▼
                  Upload PDF/TXT/MD
                           │
                           ▼
                       Parsing
                           │
                           ▼
                    Preprocessing
                           │
                           ▼
                       Chunking
                           │
                           ▼
                 Embedding Generation
                           │
                           ▼
                     FAISS Index
                           │
                           │
                           ▼
                     USER QUERY
                           │
                           ▼
                    Query Rewriting
                           │
                           ▼
                  Relevant Retrieval
                           │
                           ▼
                       Reranking
                           │
                           ▼
                    Grounded Prompt
                           │
                           ▼
                         LLM
                           │
                           ▼
                 Response Validation
                           │
                           ▼
                  Streaming Response
                           │
                           ▼
                    Sources/Citations
```

---

# ✨ Features

### 📂 Multi-format Document Upload

Supports:

* PDF
* TXT
* Markdown

### 🧹 Document Processing

Uploaded documents are:

1. Parsed
2. Cleaned
3. Preprocessed
4. Split into manageable chunks

### 🧩 Intelligent Chunking

Documents are divided into overlapping chunks to preserve contextual information during retrieval.

Default configuration:

```text
Chunk Size:       900
Chunk Overlap:    150
```

### 🔢 Semantic Embeddings

The system uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

to convert document chunks into numerical vector representations.

### 🔎 FAISS Vector Search

FAISS is used for efficient similarity search over document embeddings.

The system retrieves the most relevant chunks based on the user's question.

### 🔄 Query Rewriting

User questions can be rewritten into improved search queries before retrieval.

This helps improve semantic retrieval quality.

### 🎯 Reranking

Retrieved chunks are reranked so that the most relevant context is provided to the language model.

### 🤖 LLM Integration

The project supports LLM-based response generation using an external LLM API.

The current configuration uses:

```text
Provider: Groq
Model: llama-3.3-70b-versatile
```

### 📚 Grounded Answers

The language model receives retrieved document context instead of relying only on general knowledge.

This helps reduce unsupported responses and hallucinations.

### 🔗 Source Citations

Responses can include information about the documents and chunks used to generate the answer.

### ⚡ Streaming Responses

The API provides a streaming endpoint for progressively returning generated answers.

### 🧪 Typed Validation

Pydantic models are used for structured request and response validation.

### 🌐 REST API

FastAPI provides endpoints for:

```text
GET  /health
POST /documents/upload
POST /query
POST /query/stream
```

### 🖥️ Streamlit Interface

A Streamlit frontend provides an interactive interface for:

* Uploading documents
* Asking questions
* Viewing generated answers
* Viewing sources

### 🔀 LangGraph Workflow

LangGraph is included for structured workflow orchestration and enables the RAG pipeline to be represented as a state-based workflow.

### 🐳 Docker Support

Docker configuration is included for deployment and environment consistency.

---

# 🏗️ Project Architecture

```text
production-rag-assistant/
│
├── app/
│   ├── api.py
│   ├── config.py
│   ├── models.py
│   │
│   └── services/
│       ├── parsers.py
│       ├── chunking.py
│       ├── embeddings.py
│       ├── vector_store.py
│       ├── reranker.py
│       ├── llm.py
│       ├── prompts.py
│       ├── rag.py
│       └── ingestion.py
│
├── tests/
│   ├── test_chunking.py
│   └── test_health.py
│
├── data/
│   ├── uploads/
│   └── indexes/
│
├── streamlit_app.py
├── langgraph_workflow.py
│
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── .gitignore
└── README.md
```

---

# 🧰 Technologies Used

| Technology            | Purpose                       |
| --------------------- | ----------------------------- |
| Python                | Core programming language     |
| FastAPI               | Backend REST API              |
| Streamlit             | User interface                |
| LangGraph             | Workflow orchestration        |
| LangChain             | LLM/RAG ecosystem integration |
| FAISS                 | Vector similarity search      |
| Sentence Transformers | Text embeddings               |
| Pydantic              | Data validation               |
| Groq                  | LLM API                       |
| Uvicorn               | ASGI server                   |
| Docker                | Containerization              |
| Pytest                | Testing                       |

---

# ⚙️ Configuration

The application uses environment variables stored in `.env`.

Example:

```env
GROQ_API_KEY=your_groq_api_key

LLM_PROVIDER=groq
LLM_MODEL=llama-3.3-70b-versatile

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

CHUNK_SIZE=900
CHUNK_OVERLAP=150

RETRIEVAL_K=8
RERANK_K=5

MAX_CONTEXT_CHARS=12000

API_HOST=127.0.0.1
API_PORT=8000
```

⚠️ **Never commit your `.env` file or API keys to GitHub.**

Use:

```text
.env.example
```

as the configuration template.

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/production-rag-assistant.git
```

Move into the project:

```bash
cd production-rag-assistant
```

---

# 2. Create a Virtual Environment

### Windows

```powershell
python -m venv .venv
```

Activate:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

# 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 4. Configure Environment Variables

Copy:

```text
.env.example
```

to:

```text
.env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Open:

```powershell
notepad .env
```

Add your API key:

```env
GROQ_API_KEY=your_actual_api_key
```

---

# ▶️ Running the Application

The application consists of two parts:

```text
FastAPI Backend
       +
Streamlit Frontend
```

## Start FastAPI

Open a terminal:

```bash
python -m uvicorn app.api:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

# 📖 API Documentation

FastAPI automatically provides interactive Swagger documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

Available endpoints:

```text
GET  /health
POST /documents/upload
POST /query
POST /query/stream
```

OpenAPI specification:

```text
http://127.0.0.1:8000/openapi.json
```

---

# 🖥️ Start Streamlit

Open a second terminal.

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run:

```bash
streamlit run streamlit_app.py
```

The interface will normally be available at:

```text
http://localhost:8501
```

---

# 📤 Document Upload

The system accepts:

```text
PDF
TXT
Markdown
```

Example:

```text
User
 │
 │ Upload document
 ▼
Streamlit
 │
 ▼
FastAPI
 │
 ▼
Document Parser
 │
 ▼
Preprocessing
 │
 ▼
Chunking
 │
 ▼
Embedding Model
 │
 ▼
FAISS
```

The resulting vectors are stored in the configured index directory.

---

# 💬 Question Answering

When the user asks a question:

```text
User Question
      │
      ▼
Query Rewriting
      │
      ▼
Vector Retrieval
      │
      ▼
Top-K Chunks
      │
      ▼
Reranking
      │
      ▼
Relevant Context
      │
      ▼
Grounded Prompt
      │
      ▼
Groq LLM
      │
      ▼
Validated Response
      │
      ▼
Sources
```

---

# 🔍 Example Query

Suppose the uploaded document contains information about RAG.

User asks:

```text
What is Retrieval-Augmented Generation?
```

The system:

1. Rewrites the query.
2. Searches the FAISS index.
3. Retrieves relevant chunks.
4. Reranks the retrieved chunks.
5. Builds a grounded prompt.
6. Sends the context to the LLM.
7. Generates the response.
8. Returns the answer with sources.

---

# 🧪 Testing

Run:

```bash
pytest -v
```

The project contains tests for:

```text
tests/
├── test_chunking.py
└── test_health.py
```

---

# 🐳 Docker

Docker support is included through:

```text
Dockerfile
docker-compose.yml
```

If Docker Desktop is installed and running:

```bash
docker compose up --build
```

The API can then be accessed through:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

To stop:

```bash
docker compose down
```

---

# 🔐 Security

This project follows basic secret-management practices.

### Never commit:

```text
.env
API keys
access tokens
credentials
```

The `.gitignore` file excludes sensitive configuration.

Use:

```text
.env.example
```

for sharing configuration structure.

---

# 📈 Production-Oriented Design

The project is designed around modular AI engineering principles.

Instead of putting the entire RAG pipeline into one Python file, responsibilities are separated:

```text
parsers.py
     ↓
chunking.py
     ↓
embeddings.py
     ↓
vector_store.py
     ↓
reranker.py
     ↓
llm.py
     ↓
prompts.py
     ↓
rag.py
     ↓
ingestion.py
```

This makes individual components easier to:

* Test
* Maintain
* Replace
* Extend
* Deploy

---

# 🔮 Future Improvements

Possible future enhancements include:

* PostgreSQL/pgvector support
* Redis caching
* Hybrid BM25 + vector retrieval
* Advanced cross-encoder reranking
* Multi-user authentication
* Document access permissions
* Conversation memory
* Observability and tracing
* Evaluation datasets
* RAG quality metrics
* LLM response evaluation
* CI/CD pipeline
* Cloud deployment
* Kubernetes deployment
* Background document processing
* Distributed vector search

---

# 🎯 Learning Outcomes

This project demonstrates practical experience with:

* Retrieval-Augmented Generation
* Generative AI
* Large Language Models
* Vector embeddings
* Semantic search
* FAISS
* Document processing
* FastAPI
* Streamlit
* LangGraph
* LangChain
* Pydantic
* API design
* Streaming responses
* Software modularity
* Testing
* Docker
* Environment management

---

# 👨‍💻 Author

**Piyush Saxena**

Production-style AI/RAG engineering project demonstrating modern Generative AI and backend development practices.

---

# ⭐ Project Highlights

```text
✓ Multi-format document ingestion
✓ Semantic chunking
✓ Sentence Transformer embeddings
✓ FAISS vector search
✓ Query rewriting
✓ Retrieval
✓ Reranking
✓ Grounded prompting
✓ Groq LLM integration
✓ Response validation
✓ Source citations
✓ Streaming API
✓ FastAPI backend
✓ Streamlit frontend
✓ LangGraph workflow
✓ Docker support
✓ Automated tests
✓ Modular architecture
```

---

## 📄 License

This project is intended for educational, portfolio, and demonstration purposes.
