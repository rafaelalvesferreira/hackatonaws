#!/usr/bin/env python3
"""
Basic test script for the Bedrock Document Agent
Tests the system without requiring AWS credentials
"""

import sys
import os
sys.path.insert(0, '.')

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from config.settings import Config
        print("✓ Config module imported")
    except Exception as e:
        print(f"✗ Config import failed: {e}")
        return False
    
    try:
        from src.document_processor import DocumentProcessor
        print("✓ DocumentProcessor imported")
    except Exception as e:
        print(f"✗ DocumentProcessor import failed: {e}")
        return False
    
    try:
        import flask
        from flask_cors import CORS
        print("✓ Flask modules imported")
    except Exception as e:
        print(f"✗ Flask import failed: {e}")
        return False
    
    try:
        import streamlit
        print("✓ Streamlit imported")
    except Exception as e:
        print(f"✗ Streamlit import failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration loading"""
    print("\n⚙️  Testing configuration...")
    
    try:
        from config.settings import Config
        
        print(f"✓ AWS Region: {Config.AWS_REGION}")
        print(f"✓ Documents path: {Config.DOCUMENTS_PATH}")
        print(f"✓ Vector store path: {Config.VECTOR_STORE_PATH}")
        print(f"✓ Flask host: {Config.FLASK_HOST}")
        print(f"✓ Flask port: {Config.FLASK_PORT}")
        print(f"✓ Chunk size: {Config.CHUNK_SIZE}")
        print(f"✓ Max search results: {Config.MAX_SEARCH_RESULTS}")
        
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def test_directories():
    """Test if required directories exist"""
    print("\n📁 Testing directories...")
    
    from config.settings import Config
    
    directories = [
        Config.DOCUMENTS_PATH,
        Config.PROMPTS_PATH,
        os.path.dirname(Config.VECTOR_STORE_PATH)
    ]
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"✓ Directory exists: {directory}")
        else:
            print(f"✗ Directory missing: {directory}")
            return False
    
    return True

def test_documents():
    """Test if documents exist"""
    print("\n📄 Testing documents...")
    
    from config.settings import Config
    
    if not os.path.exists(Config.DOCUMENTS_PATH):
        print(f"✗ Documents directory not found: {Config.DOCUMENTS_PATH}")
        return False
    
    documents = os.listdir(Config.DOCUMENTS_PATH)
    if not documents:
        print("⚠️  No documents found in documents directory")
        return False
    
    print(f"✓ Found {len(documents)} files in documents directory:")
    for doc in documents:
        print(f"  - {doc}")
    
    return True

def main():
    """Run all tests"""
    print("🚀 Starting Bedrock Document Agent Basic Tests\n")
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Directories", test_directories),
        ("Documents", test_documents)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    print("\n" + "="*50)
    print("📊 TEST RESULTS SUMMARY")
    print("="*50)
    
    passed = 0
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:15} {status}")
        if result:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(results)} tests")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Your system is ready.")
        print("\nNext steps:")
        print("1. Configure your AWS credentials in .env file")
        print("2. Run: python3 run_streamlit.py")
        print("3. Open http://localhost:8501 in your browser")
    else:
        print(f"\n⚠️  {len(results) - passed} tests failed. Please fix the issues above.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
