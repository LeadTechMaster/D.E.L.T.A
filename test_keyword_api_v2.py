#!/usr/bin/env python3
"""Test Keyword Search - Write to file"""

import requests
import json
import sys

API_KEY = "850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c"

output_file = "/Users/udishkolnik/543/D.E.L.T.A/keyword_test_results.txt"

with open(output_file, 'w') as f:
    f.write("="*70 + "\n")
    f.write("TESTING SERPAPI - KEYWORD FUNCTIONS (REAL API CALLS)\n")
    f.write("="*70 + "\n\n")

    # Test 1: Keyword Autocomplete
    f.write("Test 1: Keyword Autocomplete for 'pizza'\n")
    f.write("-"*70 + "\n")
    
    try:
        url = "https://serpapi.com/search"
        params = {
            "engine": "google_autocomplete",
            "q": "pizza",
            "api_key": API_KEY
        }
        
        response = requests.get(url, params=params, timeout=30)
        f.write(f"Status Code: {response.status_code}\n")
        
        if response.status_code == 200:
            data = response.json()
            f.write("✅ SUCCESS! Got real data from SerpApi\n\n")
            f.write("Keyword Suggestions:\n")
            suggestions = data.get("suggestions", [])
            for i, s in enumerate(suggestions[:10], 1):
                f.write(f"  {i}. {s.get('value', '')}\n")
            f.write(f"\nTotal suggestions: {len(suggestions)}\n")
        else:
            f.write(f"❌ ERROR: {response.status_code}\n")
            f.write(f"{response.text}\n")
            
    except Exception as e:
        f.write(f"❌ EXCEPTION: {e}\n")
    
    f.write("\n" + "="*70 + "\n\n")
    
    # Test 2: Local Pack Results
    f.write("Test 2: Local Pack Results for 'pizza restaurant new york'\n")
    f.write("-"*70 + "\n")
    
    try:
        params2 = {
            "engine": "google",
            "q": "pizza restaurant",
            "location": "New York, NY",
            "api_key": API_KEY
        }
        
        response2 = requests.get(url, params=params2, timeout=30)
        f.write(f"Status Code: {response2.status_code}\n")
        
        if response2.status_code == 200:
            data2 = response2.json()
            f.write("✅ SUCCESS! Got real data from SerpApi\n\n")
            
            # Local Results
            local_results = data2.get("local_results", [])
            if local_results:
                f.write(f"Found {len(local_results)} local businesses:\n\n")
                for i, biz in enumerate(local_results[:3], 1):
                    f.write(f"  {i}. {biz.get('title', 'N/A')}\n")
                    f.write(f"     Address: {biz.get('address', 'N/A')}\n")
                    f.write(f"     Rating: {biz.get('rating', 'N/A')} ({biz.get('reviews', 0)} reviews)\n")
                    f.write(f"     Phone: {biz.get('phone', 'N/A')}\n\n")
            else:
                f.write("No local results found\n")
            
            # People Also Ask
            paa = data2.get("related_questions", [])
            if paa:
                f.write(f"\nPeople Also Ask ({len(paa)} questions):\n")
                for i, q in enumerate(paa[:5], 1):
                    f.write(f"  {i}. {q.get('question', 'N/A')}\n")
        else:
            f.write(f"❌ ERROR: {response2.status_code}\n")
            f.write(f"{response2.text}\n")
            
    except Exception as e:
        f.write(f"❌ EXCEPTION: {e}\n")
    
    f.write("\n" + "="*70 + "\n")
    f.write("TESTS COMPLETE\n")
    f.write("="*70 + "\n")

print(f"Test results written to: {output_file}")

