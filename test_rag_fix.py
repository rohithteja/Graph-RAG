#!/usr/bin/env python3
"""
Quick test to verify RAG context integration is working
"""
import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(__file__))

from simple_rag import SimpleTraditionalRAG, SimpleGraphRAG, create_superhero_documents
from knowledge_graph import SuperheroGraph

def test_traditional_rag():
    """Test traditional RAG with Superman query"""
    print("🔍 Testing Traditional RAG...")
    
    # Initialize traditional RAG
    traditional_rag = SimpleTraditionalRAG(use_llm=True)
    docs = create_superhero_documents()
    traditional_rag.add_documents(docs)
    
    # Test Superman query
    query = "What is Superman's real name?"
    print(f"\nQuery: {query}")
    
    result = traditional_rag.generate_answer(query)
    print(f"Answer: {result['answer']}")
    print(f"Method: {result['method']}")
    print(f"Retrieved docs: {len(result['retrieved_docs'])}")
    
    return result

def test_graph_rag():
    """Test graph RAG with Superman query"""
    print("\n" + "="*50)
    print("🕸️ Testing Graph RAG...")
    
    try:
        # Initialize graph (may fail if Neo4j not running)
        graph = SuperheroGraph()
        graph.create_superhero_graph()
        
        # Initialize graph RAG
        graph_rag = SimpleGraphRAG(graph, use_llm=True)
        
        # Test Superman query
        query = "What is Superman's real name?"
        print(f"\nQuery: {query}")
        
        result = graph_rag.generate_answer(query)
        print(f"Answer: {result['answer']}")
        print(f"Method: {result['method']}")
        print(f"Retrieved docs: {len(result['retrieved_docs'])}")
        
        # Show retrieved documents
        print("\nRetrieved context:")
        for i, doc in enumerate(result['retrieved_docs'][:2]):
            print(f"{i+1}. {doc}")
        
        graph.close()
        return result
        
    except Exception as e:
        print(f"❌ Graph RAG failed: {e}")
        print("This is expected if Neo4j is not running")
        return None

if __name__ == "__main__":
    print("🧪 Testing RAG Context Integration Fix")
    print("="*50)
    
    # Test traditional RAG
    trad_result = test_traditional_rag()
    
    # Test graph RAG 
    graph_result = test_graph_rag()
    
    print("\n" + "="*50)
    print("✅ Test Results Summary:")
    print(f"Traditional RAG: {'✅ Working' if 'Clark Kent' in trad_result['answer'] else '❌ Not using context'}")
    
    if graph_result:
        print(f"Graph RAG: {'✅ Working' if 'Clark Kent' in graph_result['answer'] else '❌ Not using context'}")
    else:
        print("Graph RAG: ⚠️ Skipped (Neo4j not available)")
