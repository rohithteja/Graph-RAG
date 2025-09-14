"""
Simple RAG implementations for demo
"""
import json
from typing import List, Dict, Any
from api_llm import APILLM

class SimpleTraditionalRAG:
    """Simple traditional RAG using keyword matching (no embeddings for simplicity)"""
    
    def __init__(self, use_llm=True):
        self.documents = []
        self.use_llm = use_llm
        self.llm = APILLM() if use_llm else None
    
    def add_documents(self, docs: List[Dict[str, Any]]):
        """Add documents to the knowledge base"""
        self.documents = docs
        print(f"✅ Added {len(docs)} documents to Traditional RAG")
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Search for relevant documents using simple keyword matching"""
        if not self.documents:
            return []
        
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        # Calculate simple similarity scores
        scored_docs = []
        for doc in self.documents:
            content_words = set(doc['content'].lower().split())
            title_words = set(doc['title'].lower().split())
            
            # Simple word overlap scoring
            content_overlap = len(query_words.intersection(content_words))
            title_overlap = len(query_words.intersection(title_words)) * 2  # Title matches worth more
            
            # Character name matching (bonus for superhero names)
            character_match = 0
            if 'character' in doc and doc['character'].lower() in query_lower:
                character_match = 5
            
            total_score = content_overlap + title_overlap + character_match
            
            if total_score > 0:
                result = doc.copy()
                result['similarity'] = total_score / 10.0  # Normalize to 0-1 range
                scored_docs.append(result)
        
        # Sort by score and return top-k
        scored_docs.sort(key=lambda x: x['similarity'], reverse=True)
        return scored_docs[:top_k]
    
    def generate_answer(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        """Generate an answer using retrieved documents and TinyLlama"""
        # Get relevant documents
        retrieved_docs = self.search(query, top_k)
        
        if not self.use_llm or not self.llm:
            # Return simple concatenated results
            if not retrieved_docs:
                return {
                    "answer": "No relevant information found.",
                    "retrieved_docs": [],
                    "method": "traditional_simple"
                }
            
            # Simple concatenation of retrieved content
            answer = "Based on the available information:\n\n"
            for i, doc in enumerate(retrieved_docs[:3]):
                answer += f"{i+1}. {doc.get('title', 'Document')}: {doc.get('content', '')}\n"
            
            return {
                "answer": answer,
                "retrieved_docs": retrieved_docs,
                "method": "traditional_simple"
            }
        
        # Use TinyLlama to generate response
        try:
            llm_response = self.llm.generate_response(retrieved_docs, query, "traditional")
            return {
                "answer": llm_response,
                "retrieved_docs": retrieved_docs,
                "method": "traditional_llm"
            }
        except Exception as e:
            # Fallback to simple method
            return {
                "answer": f"LLM Error: {str(e)}. Fallback: " + retrieved_docs[0].get('content', 'No information available.') if retrieved_docs else "No information found.",
                "retrieved_docs": retrieved_docs,
                "method": "traditional_fallback"
            }

class SimpleGraphRAG:
    """Simple Graph RAG using the Neo4j knowledge graph"""
    
    def __init__(self, graph_instance=None, use_llm=True):
        self.graph = graph_instance
        self.use_llm = use_llm
        self.llm = APILLM() if use_llm else None
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search using graph relationships"""
        if not self.graph:
            return []
        
        query_lower = query.lower()
        results = []
        
        # Extract hero name if mentioned
        hero_name = None
        if 'superman' in query_lower:
            hero_name = 'Superman'
        elif 'batman' in query_lower:
            hero_name = 'Batman'  
        elif 'wonder woman' in query_lower:
            hero_name = 'Wonder Woman'
        elif 'flash' in query_lower:
            hero_name = 'Flash'
        
        if hero_name:
            # Always get detailed hero information first
            hero_details = self.graph.query_graph("hero_details", hero_name)
            results.extend(hero_details)
            
            # For relationship-specific queries, add connection info
            if any(word in query_lower for word in ['teammate', 'team', 'ally', 'friend', 'relationship', 'connect', 'related']):
                # Get teammates
                teammates = self.graph.query_graph("teammates", hero_name)
                results.extend(teammates)
                
                # Get all relationships
                relationships = self.graph.query_graph("hero_relationships", hero_name) 
                results.extend(relationships)
            
            # For basic "who is" questions, also show some connections to demonstrate graph capabilities
            elif any(word in query_lower for word in ['who', 'what', 'about']):
                # Add a few key relationships to show the graph advantage
                teammates = self.graph.query_graph("teammates", hero_name)
                if teammates:
                    results.extend(teammates[:2])  # Just show 2 teammates
                    
            # For power/ability questions, focus on the hero details (already added above)
            # No additional queries needed
        
        elif 'justice league' in query_lower or 'team member' in query_lower:
            # Get team members
            members = self.graph.query_graph("team_members")
            results.extend(members)
        
        else:
            # Default: return all heroes for general queries
            heroes = self.graph.query_graph("all_heroes")
            results.extend(heroes)
        
        return results
    
    def generate_answer(self, query: str) -> Dict[str, Any]:
        """Generate an answer using graph search and TinyLlama"""
        # Get relevant graph data
        retrieved_docs = self.search(query)
        
        if not self.use_llm or not self.llm:
            # Return simple concatenated results
            if not retrieved_docs:
                return {
                    "answer": "No relevant information found in the knowledge graph.",
                    "retrieved_docs": [],
                    "method": "graph_simple"
                }
            
            # Simple concatenation of graph results
            answer = "Based on the knowledge graph:\n\n"
            for i, doc in enumerate(retrieved_docs[:5]):
                doc_type = doc.get('type', 'Unknown')
                content = doc.get('content', str(doc))
                answer += f"{i+1}. [{doc_type}] {content}\n"
            
            return {
                "answer": answer,
                "retrieved_docs": retrieved_docs,
                "method": "graph_simple"
            }
        
        # Use TinyLlama to generate response
        try:
            llm_response = self.llm.generate_response(retrieved_docs, query, "graph")
            return {
                "answer": llm_response,
                "retrieved_docs": retrieved_docs,
                "method": "graph_llm"
            }
        except Exception as e:
            # Fallback to simple method
            fallback_answer = "LLM Error: " + str(e)
            if retrieved_docs:
                fallback_answer += f"\n\nFallback: {retrieved_docs[0].get('content', 'No information available.')}"
            return {
                "answer": fallback_answer,
                "retrieved_docs": retrieved_docs,
                "method": "graph_fallback"
            }

def create_superhero_documents():
    """Create superhero documents for traditional RAG"""
    documents = [
        {
            "id": "superman_bio",
            "title": "Superman Biography",
            "content": "Superman, also known as Clark Kent, is a fictional superhero from the planet Krypton. He possesses incredible powers including super strength, flight, invulnerability, heat vision, and x-ray vision. He was sent to Earth as an infant and raised by Jonathan and Martha Kent in Smallville, Kansas. Superman is a founding member of the Justice League and works as a reporter for the Daily Planet in Metropolis.",
            "character": "Superman"
        },
        {
            "id": "batman_bio", 
            "title": "Batman Biography",
            "content": "Batman, whose real identity is Bruce Wayne, is a billionaire vigilante who fights crime in Gotham City. After witnessing his parents' murder as a child, Bruce dedicated his life to fighting crime. He has no superhuman powers but relies on his intelligence, martial arts skills, detective abilities, and advanced technology. Batman is known for his dark persona and is a founding member of the Justice League.",
            "character": "Batman"
        },
        {
            "id": "wonder_woman_bio",
            "title": "Wonder Woman Biography", 
            "content": "Wonder Woman, also known as Diana Prince, is an Amazonian princess from the island of Themyscira. She possesses superhuman strength, speed, and durability. Her signature weapons include the Lasso of Truth, indestructible bracelets, and a sword and shield. Wonder Woman serves as an ambassador for peace and is a founding member of the Justice League.",
            "character": "Wonder Woman"
        },
        {
            "id": "flash_bio",
            "title": "Flash Biography",
            "content": "The Flash, whose real name is Barry Allen, is the fastest man alive. He gained his super-speed powers after being struck by lightning and doused with chemicals. Barry can run faster than the speed of light, travel through time, and phase through solid objects. He works as a forensic scientist for the Central City Police Department and is a member of the Justice League.",
            "character": "Flash"
        },
        {
            "id": "justice_league_info",
            "title": "Justice League Information",
            "content": "The Justice League is a team of superheroes including Superman, Batman, Wonder Woman, Flash, Green Lantern, Aquaman, and others. Founded to protect Earth from threats too large for any single hero, the team operates from the Watchtower satellite. The Justice League represents hope, justice, and heroism, with each member bringing unique abilities to protect humanity.",
            "character": "Team"
        }
    ]
    
    return documents

if __name__ == "__main__":
    # Test Traditional RAG
    print("🔍 Testing Traditional RAG...")
    traditional_rag = SimpleTraditionalRAG()
    docs = create_superhero_documents()
    traditional_rag.add_documents(docs)
    
    query = "What are Superman's powers?"
    results = traditional_rag.search(query)
    print(f"\nQuery: {query}")
    for i, result in enumerate(results):
        print(f"{i+1}. {result['title']} (similarity: {result['similarity']:.3f})")
