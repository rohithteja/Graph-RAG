#!/usr/bin/env python3
"""
Test script for TinyLlama integration with Graph-RAG
"""

import sys
import os

def test_tinyllama_integration():
    """Test the TinyLlama integration"""
    print("🧪 Testing TinyLlama Integration...")
    
    try:
        # Test import
        print("📦 Testing imports...")
        from tinyllama_integration import TinyLlamaLLM
        print("✅ TinyLlama integration imported successfully")
        
        # Test model initialization
        print("\n🤖 Testing model initialization...")
        llm = TinyLlamaLLM()
        print(f"✅ TinyLlama instance created: {llm.model_name}")
        print(f"📱 Device detected: {llm.device}")
        
        # Test model info before loading
        print("\n📊 Getting model status...")
        info = llm.get_model_info()
        print(f"Status: {info['status']}")
        
        # Test model loading (optional - takes time)
        load_test = input("\n🔄 Load model for full test? This may take a few minutes (y/N): ").lower().strip()
        if load_test == 'y':
            print("🔄 Loading TinyLlama model...")
            llm.load_model()
            
            info = llm.get_model_info()
            print(f"✅ Model loaded successfully!")
            print(f"📊 Model info: {info}")
            
            # Test simple generation
            print("\n🧠 Testing text generation...")
            test_docs = [{
                'title': 'Superman Info',
                'content': 'Superman is a superhero from Krypton with super strength and flight.',
                'similarity': 0.9
            }]
            
            response = llm.generate_response(test_docs, "Who is Superman?", "traditional")
            print(f"🎯 Generated response: {response}")
        
        print("\n✅ All tests passed!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure requirements are installed: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True

def test_rag_integration():
    """Test the RAG integration with TinyLlama"""
    print("\n🧪 Testing RAG Integration...")
    
    try:
        from simple_rag import SimpleTraditionalRAG, create_superhero_documents
        
        # Test traditional RAG with LLM
        print("📄 Testing Traditional RAG with TinyLlama...")
        trad_rag = SimpleTraditionalRAG(use_llm=True)
        docs = create_superhero_documents()
        trad_rag.add_documents(docs)
        
        print("✅ Traditional RAG initialized with TinyLlama")
        
        # Test without loading model (just structure)
        search_results = trad_rag.search("Superman powers", top_k=2)
        print(f"🔍 Search results: {len(search_results)} documents found")
        
        print("✅ RAG integration test passed!")
        
    except Exception as e:
        print(f"❌ RAG integration test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 TinyLlama Integration Test Suite")
    print("=" * 50)
    
    # Run tests
    success = True
    success &= test_tinyllama_integration()
    success &= test_rag_integration()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! TinyLlama integration is ready.")
        print("\n💡 To run the app: streamlit run app.py")
    else:
        print("❌ Some tests failed. Check the errors above.")
        sys.exit(1)
