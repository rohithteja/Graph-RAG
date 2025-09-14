# Graph-RAG: Traditional vs Graph-based RAG Comparison

Professional demonstration of Graph-based Retrieval-Augmented Generation (RAG) using Neo4j knowledge graphs and API-based LLMs.

## 🚀 Features

- **Neo4j Knowledge Graph**: Superhero entities with relationships
- **Traditional RAG**: Vector-based similarity search  
- **Graph RAG**: Leverages graph relationships for enhanced context
- **API LLM Integration**: OpenAI, Groq, and Ollama support
- **Docker Deployment**: One-command setup
- **Interactive Comparison**: Side-by-side RAG results

## ⚡ Quick Start

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd Graph-RAG
```

### 2. Set Up API Key
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API key
# Recommended: Get free Groq API key from https://groq.com/
```

### 3. Launch with Docker
```bash
docker compose up --build
```

### 4. Access Application
- **Web Interface**: http://localhost:8501
- **Neo4j Browser**: http://localhost:7474 (neo4j/password)

## 🔑 API Configuration

### Option 1: Groq (Recommended - FREE)
```bash
# Get free API key from https://groq.com/
GROQ_API_KEY=gsk_your_api_key_here
```
✅ **Pros**: Free tier, very fast responses, Llama models

### Option 2: OpenAI (Paid)
```bash
# Requires OpenAI account
OPENAI_API_KEY=sk-your_api_key_here
```
✅ **Pros**: High quality responses, GPT models

### Option 3: Ollama (Local)
```bash
# Install Ollama first: https://ollama.ai/
OLLAMA_BASE_URL=http://localhost:11434
```
✅ **Pros**: Completely free, runs locally, no API calls

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit UI  │────│   RAG Engine     │────│   LLM API       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                        ┌──────────────────┐
                        │   Neo4j Graph    │
                        │   Knowledge DB   │
                        └──────────────────┘
```

## 📊 How It Works

1. **Knowledge Graph**: Neo4j stores superhero entities, powers, and relationships
2. **Query Processing**: User asks questions about superheroes
3. **Traditional RAG**: Vector similarity search across documents
4. **Graph RAG**: Leverages graph structure and relationships
5. **LLM Response**: API-based models generate answers using retrieved context
6. **Comparison**: Side-by-side results highlight approach differences

## 🎯 Example Queries

Test these questions to see the difference:

```
"What is Superman's real name?"
"Who are Batman's allies?"
"What powers does Wonder Woman have?"
"Which heroes are from Gotham City?"
"How are Superman and Batman related?"
```

## 🛠️ Manual Installation

For non-Docker setup:

```bash
# Install dependencies
pip install -r requirements.txt

# Start Neo4j
docker run -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password neo4j:5.13

# Run application
streamlit run app.py
```

## 📁 Project Structure

```
Graph-RAG/
├── app.py              # Main Streamlit application
├── simple_rag.py       # RAG implementation classes
├── knowledge_graph.py  # Neo4j graph setup
├── api_llm.py         # LLM API integration
├── requirements.txt    # Python dependencies
├── docker-compose.yml  # Docker services
├── Dockerfile         # Application container
└── .env.example       # Environment template
```

## 💰 Cost Comparison

| API Provider | Cost | Speed | Setup |
|-------------|------|-------|-------|
| **Groq** | Free tier | Very Fast | Easy |
| **OpenAI** | ~$0.002/request | Fast | Easy |
| **Ollama** | Free | Medium | Local install |

## 🔧 Troubleshooting

### No LLM API configured
```bash
# Check .env file has API key set
cat .env
# Should show: GROQ_API_KEY=gsk_...
```

### Neo4j connection failed
```bash
# Check if Neo4j container is running
docker ps | grep neo4j
```

### Slow responses
- Use Groq API for fastest responses
- OpenAI is also fast but requires payment
- Ollama is slower but completely free

### Docker build issues
```bash
# Ensure Docker has enough memory (4GB+)
docker system prune  # Clean up if needed
```

## 🚀 Production Deployment

For production use:
1. Use environment-specific `.env` files  
2. Set up proper Neo4j authentication
3. Configure API rate limiting
4. Add monitoring and logging
5. Use production-grade Docker orchestration

## 📝 License

This project is for educational and demonstration purposes.
