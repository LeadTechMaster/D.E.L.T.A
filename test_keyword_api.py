#!/usr/bin/env python3
"""Test Keyword Search - Direct API Call"""

import requests
import json
import sys

API_KEY = "850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c"

print("="*70)
print("TESTING SERPAPI - KEYWORD AUTOCOMPLETE (REAL API CALL)")
print("="*70)
print()

# Test 1: Keyword Autocomplete/Suggestions
print("Test 1: Keyword Autocomplete for 'pizza'")
print("-"*70)

try:
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_autocomplete",
        "q": "pizza",
        "api_key": API_KEY
    }
    
    response = requests.get(url, params=params, timeout=30)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ SUCCESS! Got real data from SerpApi")
        print()
        print("Keyword Suggestions:")
        suggestions = data.get("suggestions", [])
        for i, s in enumerate(suggestions[:5], 1):
            print(f"  {i}. {s.get('value', '')}")
        print()
        print(f"Total suggestions: {len(suggestions)}")
    else:
        print(f"❌ ERROR: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ EXCEPTION: {e}")
    import traceback
    traceback.print_exc()

print()
print("="*70)

# Test 2: Google Search with Local Pack
print("Test 2: Local Pack Results for 'pizza restaurant new york'")
print("-"*70)

try:
    params2 = {
        "engine": "google",
        "q": "pizza restaurant",
        "location": "New York, NY",
        "api_key": API_KEY
    }
    
    response2 = requests.get(url, params=params2, timeout=30)
    print(f"Status Code: {response2.status_code}")
    
    if response2.status_code == 200:
        data2 = response2.json()
        print("✅ SUCCESS! Got real data from SerpApi")
        print()
        
        # Check for local results
        local_results = data2.get("local_results", [])
        if local_results:
            print(f"Found {len(local_results)} local businesses:")
            for i, biz in enumerate(local_results[:3], 1):
                print(f"\n  {i}. {biz.get('title', 'N/A')}")
                print(f"     Address: {biz.get('address', 'N/A')}")
                print(f"     Rating: {biz.get('rating', 'N/A')} ({biz.get('reviews', 0)} reviews)")
                print(f"     Phone: {biz.get('phone', 'N/A')}")
        else:
            print("No local results found")
            
        # Check for People Also Ask
        paa = data2.get("related_questions", [])
        if paa:
            print(f"\nPeople Also Ask ({len(paa)} questions):")
            for i, q in enumerate(paa[:3], 1):
                print(f"  {i}. {q.get('question', 'N/A')}")
                
    else:
        print(f"❌ ERROR: {response2.status_code}")
        print(response2.text)
        
except Exception as e:
    print(f"❌ EXCEPTION: {e}")
    import traceback
    traceback.print_exc()

print()
print("="*70)
print("TESTS COMPLETE")
print("="*70)

