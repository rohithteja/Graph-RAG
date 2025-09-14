"""
Quick test to verify the setup works
"""

def test_imports():
    """Test if all required packages can be imported"""
    try:
        import streamlit as st
        print("✅ Streamlit imported")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
    
    try:
        from neo4j import GraphDatabase
        print("✅ Neo4j driver imported") 
    except ImportError as e:
        print(f"❌ Neo4j import failed: {e}")
    
    try:
        import pandas as pd
        print("✅ Pandas imported")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")

def test_traditional_rag():
    """Test Traditional RAG functionality"""
    try:
        from simple_rag import SimpleTraditionalRAG, create_superhero_documents
        
        rag = SimpleTraditionalRAG()
        docs = create_superhero_documents()
        rag.add_documents(docs)
        
        results = rag.search("Superman powers")
        print(f"✅ Traditional RAG works - found {len(results)} results")
        return True
    except Exception as e:
        print(f"❌ Traditional RAG failed: {e}")
        return False

def test_neo4j_connection():
    """Test Neo4j connection"""
    try:
        from knowledge_graph import SuperheroGraph
        
        graph = SuperheroGraph()
        # Just test connection, don't create data
        with graph.driver.session() as session:
            session.run("RETURN 1")
        graph.close()
        print("✅ Neo4j connection successful")
        return True
    except Exception as e:
        print(f"❌ Neo4j connection failed: {e}")
        print("   Make sure Neo4j is running: docker run -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:latest")
        return False

if __name__ == "__main__":
    print("🧪 Testing Graph RAG Demo Setup\n")
    
    print("1. Testing imports...")
    test_imports()
    
    print("\n2. Testing Traditional RAG...")
    test_traditional_rag()
    
    print("\n3. Testing Neo4j connection...")
    test_neo4j_connection()
    
    print("\n🎯 Setup complete! Run: streamlit run app.py")
