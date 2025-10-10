#!/usr/bin/env python3
"""
Simple test to verify backend dependencies and startup
"""

def test_imports():
    try:
        import fastapi
        import uvicorn
        import httpx
        print("✅ All required packages imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_heatmap_import():
    try:
        import sys
        sys.path.append('/Users/udishkolnik/Downloads/D.E.L.T.A 2')
        from HEATMAP import heatmap_api
        print("✅ HEATMAP module imported successfully")
        return True
    except ImportError as e:
        print(f"❌ HEATMAP import error: {e}")
        return False

def test_basic_server():
    try:
        from fastapi import FastAPI
        import uvicorn
        
        app = FastAPI()
        
        @app.get("/")
        def read_root():
            return {"message": "D.E.L.T.A Backend Test - Working!"}
        
        print("✅ FastAPI server created successfully")
        return True
    except Exception as e:
        print(f"❌ Server creation error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing D.E.L.T.A Backend Dependencies...")
    print()
    
    imports_ok = test_imports()
    print()
    
    heatmap_ok = test_heatmap_import()
    print()
    
    server_ok = test_basic_server()
    print()
    
    if imports_ok and heatmap_ok and server_ok:
        print("🎉 All tests passed! Backend should work.")
    else:
        print("❌ Some tests failed. Check the errors above.")
