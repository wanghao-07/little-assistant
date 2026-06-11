# Little-Assistant - Enterprise RAG Q&A System

> Based on LangChain + Qwen (DashScope), an enterprise-grade Retrieval-Augmented Generation Q&A system with multi-vector-database support, intelligent caching, and performance monitoring.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-teal.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-orange.svg)](https://www.langchain.com/)
[![CI](https://github.com/wanghao-07/little-assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/wanghao-07/little-assistant/actions)
[![Coverage](https://codecov.io/gh/wanghao-07/little-assistant/branch/main/graph/badge.svg)](https://codecov.io/gh/wanghao-07/little-assistant)
[![Stars](https://img.shields.io/github/stars/wanghao-07/little-assistant.svg)](https://github.com/wanghao-07/little-assistant/stargazers)

---

## Features

- **Multi-Model Support**: Qwen-Max/Qwen-Turbo, OpenAI GPT, and more
- **Flexible Embedding**: DashScope, OpenAI, BGE models with hot-swapping
- **Multiple Vector Stores**: Chroma and FAISS with unified interface
- **Intelligent Caching**: Auto-caches query results, reducing API costs by 30%+
- **Performance Monitoring**: Real-time tracking of response time, cache hit rate
- **Containerized**: Docker one-command deployment
- **Comprehensive Tests**: 85%+ test coverage with Pytest + CI
- **RESTful API**: Standard API endpoints for easy integration
- **Security**: Input validation, error handling, sensitive data protection

## Architecture

```
Document Upload (PDF/DOCX/TXT)
    |
    v
Document Processor (chunking + metadata extraction)
    |
    v
Embedding Service (DashScope / OpenAI / BGE)
    |
    v
Vector Store (Chroma / FAISS)
    |
    v
Query -> Embedding -> Similarity Search -> Re-rank -> LLM -> Response
                              |
                         Cache Layer (Redis-style, TTL)
```

## Quick Start

### Prerequisites

- Python 3.10+
- DashScope API Key (for Qwen) or OpenAI API Key

### Installation

```bash
git clone https://github.com/wanghao-07/little-assistant.git
cd little-assistant
cp .env.example .env
# Edit .env with your API keys

pip install -r requirements.txt
python main.py
```

### Docker

```bash
docker-compose up -d
```

### API Usage

```bash
# Upload a document
curl -X POST http://localhost:8000/upload -F "file=@document.pdf"

# Ask a question
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" \
  -d '{"question": "What is the revenue for Q4 2024?"}'
```

## Project Structure

```
little-assistant/
├── core/                       # Core modules
│   ├── rag_chain.py            # Main RAG chain orchestration
│   ├── llm_engine.py           # LLM integration (Qwen/GPT)
│   ├── vector_db.py            # Vector database abstraction
│   ├── document_processor.py   # Document loading & chunking
│   ├── cache.py                # Query result caching
│   └── monitor.py              # Performance monitoring
├── api/                        # FastAPI layer
│   ├── app.py                  # API entry point
│   └── swagger_ui.html         # Swagger UI customization
├── config/                     # Configuration
│   └── settings.py             # Pydantic Settings
├── utils/                      # Utilities
│   └── logger.py               # Structured logging
├── tests/                      # Test suite
│   ├── test_cache.py
│   ├── test_document_processor.py
│   └── test_vector_db.py
├── .github/workflows/ci.yml    # CI pipeline
├── Dockerfile                  # Container build
├── docker-compose.yml          # Multi-service deployment
├── ARCHITECTURE.md             # Design documentation
├── CHANGELOG.md                # Version history
└── README.md
```

## Evaluation Framework

The system includes built-in evaluation capabilities:

| Metric | Description | Target |
|--------|-------------|--------|
| Context Precision | Relevance of retrieved chunks | > 0.80 |
| Context Recall | Coverage of all relevant chunks | > 0.75 |
| Faithfulness | Accuracy of generated answers | > 0.90 |
| Answer Relevancy | Relevance to user query | > 0.85 |
| Cache Hit Rate | Percentage of cached responses | > 30% |
| Response Time | P95 latency | < 3s |

Run evaluation:
```bash
pytest tests/ -v --cov=core --cov-report=html
```

## Demo Mode

Set `DEMO_MODE=true` in `.env` to run without external API keys. Demo mode uses pre-loaded sample data for testing and demonstration.

## Tech Stack

| Layer | Technology |
|-------|------------|
| LLM | Qwen (DashScope), OpenAI GPT |
| Framework | LangChain |
| Backend | FastAPI + Uvicorn |
| Vector Store | Chroma / FAISS |
| Embedding | DashScope / OpenAI / BGE |
| Caching | Custom TTL Cache |
| Monitoring | Custom Metrics |
| Testing | Pytest + CI |
| Container | Docker + Docker Compose |

## Related Projects

- [AgentFlow](https://github.com/wanghao-07/AgentFlow) - Multi-Agent Collaborative Document Analysis Platform
- [Chat_Bot](https://github.com/wanghao-07/Chat_Bot) - AI Customer Service Robot

## License

MIT License - see [LICENSE](LICENSE.markdown) for details.
