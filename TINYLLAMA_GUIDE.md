# 🤖 TinyLlama Integration Guide

This guide explains how to use TinyLlama with the Graph-RAG application via Docker.

## 🚀 Quick Start with Docker

### Prerequisites
- Docker and Docker Compose installed
- At least 4GB RAM available for containers
- Internet connection (for downloading TinyLlama model)

### Running the Application

1. **Start all services:**
   ```bash
   ./run_docker.sh
   ```

2. **Access the applications:**
   - **Streamlit App**: http://localhost:8501
   - **Neo4j Browser**: http://localhost:7474 (neo4j/password)

### 🧠 TinyLlama Features

The application now includes TinyLlama (1.1B parameter model) for:

- **Natural Language Generation**: Convert retrieved documents into fluent responses
- **Context Understanding**: Better comprehension of user queries
- **Response Synthesis**: Combine multiple sources into coherent answers

### 🎯 Usage

1. **Initialize Systems**: Click "🚀 Initialize Systems" in the sidebar
2. **Enable TinyLlama**: Check "Enable TinyLlama LLM" option
3. **Ask Questions**: Try queries like:
   - "Who is Superman?"
   - "What are Batman's powers?"
   - "Who are Superman's teammates?"

### 📊 Comparison Modes

The app provides several comparison views:

- **🤖 AI Answers**: TinyLlama-generated responses (Traditional vs Graph RAG)
- **📊 Side-by-Side**: Raw search results comparison
- **📄 Traditional Details**: Document-based retrieval analysis
- **🕸️ Graph Details**: Knowledge graph traversal analysis

### ⚙️ Configuration

You can configure TinyLlama behavior by:

- **Enabling/Disabling**: Use the sidebar checkbox
- **Model Selection**: Modify `tinyllama_integration.py` for different models
- **Generation Parameters**: Adjust temperature, max_tokens in the code

### 🔧 Troubleshooting

**Model Loading Issues:**
- TinyLlama will automatically download on first use (~2GB)
- If download fails, check internet connection
- The app falls back to simple text responses if LLM fails

**Performance:**
- First model load takes 1-2 minutes
- Subsequent responses are faster
- CPU-only version is used in Docker for compatibility

**Memory Issues:**
- Ensure Docker has at least 4GB RAM allocated
- TinyLlama uses ~2GB when loaded
- Monitor system resources during use

### 🐳 Docker Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │     Neo4j       │
│   + TinyLlama   │◄──►│  Knowledge      │
│   (Port 8501)   │    │  Graph          │
│                 │    │  (Port 7687)    │
└─────────────────┘    └─────────────────┘
```

### 📝 Example Queries

**Traditional RAG Questions:**
- "What are Wonder Woman's powers?"
- "Tell me about The Flash"

**Graph RAG Questions:**
- "Who are Superman's teammates?"
- "What relationships exist between heroes?"
- "Which heroes are in the Justice League?"

### 🔄 Stopping Services

Press `Ctrl+C` in the terminal running the Docker services, or:

```bash
docker compose down
```
