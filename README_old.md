# 🦸‍♂️ Graph RAG vs Traditional RAG Demo

Interactive demonstration comparing Traditional RAG and Graph RAG approaches using superhero data, **powered by fast API-based LLMs**.

## 🎯 Purpose

This is a **demonstration project** to showcase the differences between:
- **📄 Traditional RAG**: Keyword matching search → AI generation
- **🕸️ Graph RAG**: Knowledge graph traversal → AI synthesis

## ✨ Fast API-Based LLM Integration

This project uses **API-based LLMs** for lightning-fast responses:
- 🤖 **API-powered answers** (OpenAI, Groq, HuggingFace, Ollama)
- ⚡ **Lightning fast**: Responses in 1-3 seconds vs 10-30 seconds locally
- 🧠 **High-quality responses** from state-of-the-art models
- 🎯 **Context-aware** based on retrieved information
- 🔄 **Mock mode**: Perfect for testing without API keys
- 🐳 **Ultra-lightweight Docker**: No model downloads neededaditional RAG Demo

Simple demonstration comparing Traditional RAG and Graph RAG approaches using superhero data, now **powered by TinyLlama** for natural language generation.

## 🎯 Purpose

This is a **demonstration project** to showcase the differences between:
- **Traditional RAG**: Keyword matching search + TinyLlama generation
- **Graph RAG**: Knowledge graph traversal + TinyLlama synthesis

## ✨ New: TinyLlama Integration

This project now includes **TinyLlama-1.1B-Chat** for generating natural language responses:
- 🤖 **AI-powered answers** instead of raw document retrieval
- 🧠 **Natural language understanding** of queries
- 🎯 **Context-aware responses** based on retrieved information
- � **Fallback mechanisms** for reliability

## �🛠️ Tech Stack

- **Streamlit**: Web interface
- **Neo4j**: Knowledge graph database  
- **API LLMs**: OpenAI, Groq, HuggingFace, or Ollama
- **Requests**: Simple HTTP API calls (no model downloads!)
- **Docker**: Lightweight containerized deployment
- **Python**: Core implementation

## 🚀 Quick Start

### Option 1: Docker (Recommended)

1. **Start with Docker**
```bash
./start.sh
```
Or manually:
```bash
docker-compose up --build
```

2. **Access the Application**
- Streamlit App: http://localhost:8501
- Neo4j Browser: http://localhost:7474 (neo4j/password)

### Option 2: Local Development

1. **Install Requirements**
```bash
pip install -r requirements.txt
```

2. **Start Neo4j** (Docker)
```bash
docker run -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:latest
```

3. **Test TinyLlama Integration** (Optional)
```bash
python test_tinyllama.py
```

4. **Run the Demo**
```bash
streamlit run app.py
```

Visit: http://localhost:8501

## 🤖 TinyLlama Features

### AI-Powered Responses
- **🧠 Natural Language Generation**: TinyLlama converts retrieved information into fluent responses
- **🎯 Context-Aware**: Understands the difference between Traditional and Graph RAG contexts
- **⚡ Lightweight**: 1.1B parameter model runs on CPU or GPU
- **� Fallback Safe**: Automatically falls back to simple responses if model fails

### Configuration Options
- **Enable/Disable TinyLlama**: Toggle AI responses in the sidebar
- **Device Selection**: Automatic GPU/CPU detection
- **Model Status**: Real-time model loading and performance info

## �📊 What You'll See

### Traditional RAG + TinyLlama
- Document-based search with keyword matching
- TinyLlama generates natural responses from retrieved documents
- Good for direct factual questions

### Graph RAG + TinyLlama  
- Relationship-based search through knowledge graph
- TinyLlama synthesizes information from connected entities
- Good for connected questions

## 🦸‍♂️ Demo Data

Simple superhero knowledge graph:
- Superman, Batman, Wonder Woman, Flash
- Relationships: teammates, allies, enemies
- Teams: Justice League
- Powers and origins