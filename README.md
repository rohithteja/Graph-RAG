# Graph RAG vs Traditional RAG Demo

Simple demonstration comparing Traditional RAG and Graph RAG approaches using superhero data.

## 🎯 Purpose

This is a **demonstration project** to showcase the differences between:
- **Traditional RAG**: Vector similarity search
- **Graph RAG**: Knowledge graph traversal

## 🛠️ Tech Stack

- **Streamlit**: Web interface
- **Neo4j**: Knowledge graph database
- **Ollama**: Local LLM
- **Sentence Transformers**: Embeddings
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

3. **Run the Demo**
```bash
streamlit run app.py
```

Visit: http://localhost:8501

## 📊 What You'll See

### Traditional RAG
- Document-based search
- Vector similarity matching
- Good for factual questions

### Graph RAG  
- Relationship-based search
- Network traversal
- Good for connected questions

## 🦸‍♂️ Demo Data

Simple superhero knowledge graph:
- Superman, Batman, Wonder Woman, Flash
- Relationships: teammates, allies, enemies
- Teams: Justice League
- Powers and origins