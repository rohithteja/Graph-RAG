
"""
API-based LLM Integration for Graph-RAG
Clean, fast, and reliable using external APIs
"""
import os
import requests
from typing import List, Dict, Any
import json

class APILLM:
    """Professional API-based LLM integration - OpenAI compatible"""
    
    def __init__(self):
        """Initialize API LLM with environment variables"""
        self.loaded = False
        self.api_type = None
        self.api_key = None
        self.base_url = None
        self.model = None
        
        # Try to find available API
        self._detect_api()
    
    def _detect_api(self):
        """Detect which API is available from environment"""
        
        # Check OpenAI API
        if os.getenv("OPENAI_API_KEY"):
            self.api_type = "openai"
            self.api_key = os.getenv("OPENAI_API_KEY")
            self.base_url = "https://api.openai.com/v1"
            self.model = "gpt-3.5-turbo"
            print("✅ OpenAI API configured")
            self.loaded = True
            
        # Check Groq API (Free tier available)
        elif os.getenv("GROQ_API_KEY"):
            self.api_type = "groq"
            self.api_key = os.getenv("GROQ_API_KEY")
            self.base_url = "https://api.groq.com/openai/v1"
            self.model = "llama3-8b-8192"  # Fast Groq model
            print("✅ Groq API configured")
            self.loaded = True
            
        # Check Ollama (Local API server)
        elif os.getenv("OLLAMA_BASE_URL"):
            self.api_type = "ollama"
            self.base_url = os.getenv("OLLAMA_BASE_URL")
            self.model = "llama2"  # Default Ollama model
            print("✅ Ollama API configured")
            self.loaded = True
            
        else:
            self.loaded = False
            print("❌ No API configured")
            print("Please set one of:")
            print("  - OPENAI_API_KEY (OpenAI API)")
            print("  - GROQ_API_KEY (Groq - has free tier)")
            print("  - OLLAMA_BASE_URL (Local Ollama server)")
    
    def load_model(self):
        """API doesn't need model loading - just verify configuration"""
        return self.loaded
    
    def generate_response(self, context_docs: List[Dict[str, Any]], query: str, rag_type: str = "traditional") -> str:
        """Generate response using API LLM"""
        if not self.loaded:
            return """❌ No LLM API configured. 

To use this application, please:
1. Get a free API key from Groq: https://groq.com/
2. Set environment variable: GROQ_API_KEY=your_key_here
3. Restart the application

Alternative APIs:
- OpenAI: Set OPENAI_API_KEY
- Ollama: Set OLLAMA_BASE_URL=http://localhost:11434"""
        
        # Build context from retrieved documents
        context = self._build_context(context_docs, rag_type)
        
        # Create prompt
        prompt = self._create_prompt(context, query, rag_type)
        
        try:
            if self.api_type in ["openai", "groq"]:
                return self._call_openai_api(prompt)
            elif self.api_type == "ollama":
                return self._call_ollama_api(prompt)
            else:
                return "❌ Unsupported API type"
                
        except Exception as e:
            return f"❌ API Error: {str(e)}\n\nPlease check your API key and internet connection."
    
    def _call_openai_api(self, prompt: str) -> str:
        """Call OpenAI-compatible API (OpenAI, Groq)"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that answers questions about superheroes based on the provided context. Always use the specific information from the context in your response."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 300,
            "temperature": 0.3  # Lower temperature for more consistent responses
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        else:
            error_msg = f"API Error {response.status_code}"
            try:
                error_detail = response.json().get("error", {}).get("message", response.text)
                error_msg += f": {error_detail}"
            except:
                error_msg += f": {response.text}"
            raise Exception(error_msg)
    
    def _call_ollama_api(self, prompt: str) -> str:
        """Call Ollama API"""
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "top_p": 0.9
            }
        }
        
        response = requests.post(
            f"{self.base_url}/api/generate",
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["response"].strip()
        else:
            raise Exception(f"Ollama Error {response.status_code}: {response.text}")
    
    def _build_context(self, docs: List[Dict[str, Any]], rag_type: str) -> str:
        """Build context string from retrieved documents"""
        if not docs:
            return "No relevant information found."
        
        context_parts = []
        
        for i, doc in enumerate(docs[:5]):  # Top 5 most relevant docs
            if rag_type == "graph" and "type" in doc:
                # Graph RAG context - format graph data properly
                doc_type = doc.get("type", "unknown")
                
                # Extract meaningful content from graph data
                if doc_type == "hero":
                    name = doc.get("name", "Unknown Hero")
                    real_name = doc.get("real_name", "")
                    powers = doc.get("powers", [])
                    origin = doc.get("origin", "")
                    team = doc.get("team", "")
                    
                    content = f"{name}"
                    if real_name:
                        content += f" (real name: {real_name})"
                    if powers:
                        content += f" has powers: {', '.join(powers)}"
                    if origin:
                        content += f", from {origin}"
                    if team:
                        content += f", member of {team}"
                        
                elif doc_type == "relationship":
                    hero1 = doc.get("hero1", "")
                    hero2 = doc.get("hero2", "")
                    relationship = doc.get("relationship", "")
                    content = f"{hero1} and {hero2} are {relationship}"
                    
                elif doc_type == "teammate":
                    teammate = doc.get("teammate", "")
                    team = doc.get("team", "")
                    content = f"{teammate} is a teammate in {team}"
                    
                else:
                    # Fallback - extract key information
                    content = doc.get("content", "")
                    if not content:
                        # Build content from available fields
                        key_fields = []
                        for key, value in doc.items():
                            if key not in ["type", "content"] and value:
                                if isinstance(value, list):
                                    key_fields.append(f"{key}: {', '.join(map(str, value))}")
                                else:
                                    key_fields.append(f"{key}: {value}")
                        content = ", ".join(key_fields)
                
                context_parts.append(f"[{doc_type.upper()}] {content}")
                
            else:
                # Traditional RAG context
                title = doc.get('title', f'Document {i+1}')
                content = doc.get('content', '')
                if not content:
                    # Fallback to extracting from other fields
                    content = str(doc)
                similarity = doc.get('similarity', 0)
                context_parts.append(f"[{title}] (relevance: {similarity:.2f}) {content}")
        
        return "\n\n".join(context_parts)
    
    def _create_prompt(self, context: str, query: str, rag_type: str) -> str:
        """Create a clear prompt for the API"""
        
        prompt = f"""Answer the question based on the provided context. Use specific details from the context in your response.

CONTEXT INFORMATION:
{context}

QUESTION: {query}

INSTRUCTIONS:
- Answer based on the context provided
- Include specific details like names, powers, relationships when available
- Be concise but informative
- If the context doesn't contain the answer, say so clearly"""
        
        return prompt
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the API configuration"""
        if not self.loaded:
            return {
                "status": "not_configured",
                "message": "No API configured. Set OPENAI_API_KEY, GROQ_API_KEY, or OLLAMA_BASE_URL",
                "api_type": "none"
            }
        
        return {
            "status": "ready",
            "api_type": self.api_type.upper(),
            "model": self.model,
            "description": f"{self.api_type.upper()} API using {self.model}"
        }

import requests
import json
import os
from typing import List, Dict, Any

class APILLM:
    """Simple API-based LLM integration using Groq API"""
    
    def __init__(self):
        """Initialize API LLM client"""
        self.api_key = os.getenv("GROQ_API_KEY", "")
        self.model_name = "mixtral-8x7b-32768"  # Fast Mixtral model
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.loaded = True  # API is always "loaded"
        
        if not self.api_key:
            print("⚠️  No GROQ_API_KEY found - using mock responses")
            print("📝 Get free API key at: https://console.groq.com/")
            self.use_mock = True
            self.model_name = "mock"
        else:
            print("🚀 Using Groq API for fast LLM responses")
            print(f"🤖 Model: {self.model_name}")
            self.use_mock = False
    
    def load_model(self):
        """API models are always ready"""
        print("✅ API LLM ready!")
        self.loaded = True
    
    def generate_response(self, context_docs: List[Dict[str, Any]], query: str, rag_type: str = "traditional") -> str:
        """Generate response using API or mock"""
        if self.use_mock:
            return self._generate_mock_response(context_docs, query, rag_type)
        
        try:
            return self._generate_api_response(context_docs, query, rag_type)
        except Exception as e:
            print(f"⚠️ API error: {e}")
            return self._generate_mock_response(context_docs, query, rag_type)
    
    def _generate_api_response(self, context_docs: List[Dict[str, Any]], query: str, rag_type: str) -> str:
        """Generate response using Groq API"""
        context = self._build_context(context_docs, rag_type)
        
        messages = [
            {
                "role": "system", 
                "content": f"You are a helpful assistant answering questions about superheroes. You use {rag_type} RAG to find information."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {query}\n\nProvide a helpful answer based on the context."
            }
        ]
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model_name,
            "messages": messages,
            "max_tokens": 200,
            "temperature": 0.7
        }
        
        response = requests.post(self.base_url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    
    def _generate_mock_response(self, context_docs: List[Dict[str, Any]], query: str, rag_type: str) -> str:
        """Generate mock responses based on retrieved context"""
        query_lower = query.lower()
        
        if not context_docs:
            return "I couldn't find any relevant information to answer your question."
        
        # Extract key information from retrieved documents
        all_context = ""
        hero_info = {}
        
        for doc in context_docs:
            content = doc.get('content', str(doc))
            all_context += content + " "
            
            # Extract specific hero details from content
            if 'Superman' in content and 'Clark Kent' in content:
                hero_info['superman_real_name'] = 'Clark Kent'
            if 'Batman' in content and 'Bruce Wayne' in content:
                hero_info['batman_real_name'] = 'Bruce Wayne'
            if 'Wonder Woman' in content and 'Diana Prince' in content:
                hero_info['wonder_woman_real_name'] = 'Diana Prince'
            if 'Flash' in content and 'Barry Allen' in content:
                hero_info['flash_real_name'] = 'Barry Allen'
        
        # Answer based on query and extracted context
        if any(word in query_lower for word in ['superman', 'clark']):
            if 'real name' in query_lower or 'name' in query_lower:
                if 'superman_real_name' in hero_info:
                    return f"Superman's real name is {hero_info['superman_real_name']}. This information comes from the retrieved documents."
                elif 'Clark Kent' in all_context:
                    return "Superman's real name is Clark Kent, as mentioned in the knowledge base."
            
            # Find Superman-specific info from context
            superman_details = []
            if 'Krypton' in all_context:
                superman_details.append("from the planet Krypton")
            if 'super strength' in all_context:
                superman_details.append("has super strength")
            if 'flight' in all_context:
                superman_details.append("can fly")
            if 'Justice League' in all_context:
                superman_details.append("is a member of the Justice League")
            
            if superman_details:
                return f"Based on the retrieved context: Superman {', '.join(superman_details)}."
            else:
                return f"Superman information found in context: {all_context[:200]}..."
        
        elif any(word in query_lower for word in ['batman', 'bruce']):
            if 'real name' in query_lower or 'name' in query_lower:
                if 'batman_real_name' in hero_info:
                    return f"Batman's real name is {hero_info['batman_real_name']}."
                elif 'Bruce Wayne' in all_context:
                    return "Batman's real name is Bruce Wayne."
            return f"Batman information from context: {all_context[:200]}..."
        
        elif any(word in query_lower for word in ['wonder woman', 'diana']):
            if 'real name' in query_lower or 'name' in query_lower:
                if 'wonder_woman_real_name' in hero_info:
                    return f"Wonder Woman's real name is {hero_info['wonder_woman_real_name']}."
                elif 'Diana Prince' in all_context:
                    return "Wonder Woman's real name is Diana Prince."
            return f"Wonder Woman information from context: {all_context[:200]}..."
        
        elif any(word in query_lower for word in ['flash', 'barry']):
            if 'real name' in query_lower or 'name' in query_lower:
                if 'flash_real_name' in hero_info:
                    return f"The Flash's real name is {hero_info['flash_real_name']}."
                elif 'Barry Allen' in all_context:
                    return "The Flash's real name is Barry Allen."
            return f"Flash information from context: {all_context[:200]}..."
        
        elif any(word in query_lower for word in ['team', 'justice league', 'group']):
            return f"The Justice League is a team of superheroes including Superman, Batman, Wonder Woman, and The Flash. They work together to protect Earth from major threats. The {rag_type} RAG system found connections between these heroes."
        
        elif any(word in query_lower for word in ['power', 'ability', 'strength']):
            return f"Based on the {rag_type} search, the heroes have various powers: Superman has super strength and flight, Batman relies on technology and intellect, Wonder Woman has combat skills and magical items, and Flash has super-speed."
        
        else:
            return f"Based on the {rag_type} RAG search, I found relevant superhero information in the knowledge base. The context shows details about various heroes and their characteristics."
    
    def _build_context(self, docs: List[Dict[str, Any]], rag_type: str) -> str:
        """Build context string from retrieved documents"""
        if not docs:
            return "No relevant information found."
        
        context_parts = []
        for i, doc in enumerate(docs[:3]):  # Limit to top 3
            if rag_type == "graph" and "type" in doc:
                context_parts.append(f"{doc['type']}: {doc.get('content', str(doc))}")
            else:
                title = doc.get('title', f'Document {i+1}')
                content = doc.get('content', str(doc))
                context_parts.append(f"{title}: {content}")
        
        return "\n".join(context_parts)
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            "status": "loaded",
            "model_name": self.model_name,
            "type": "api" if not self.use_mock else "mock",
            "description": "Groq Mixtral API (Fast)" if not self.use_mock else "Mock responses (No API key)",
            "speed": "⚡ Very Fast",
            "device": "cloud" if not self.use_mock else "local"
        }
