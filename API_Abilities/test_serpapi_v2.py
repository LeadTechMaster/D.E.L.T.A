#!/usr/bin/env python3
"""Direct SerpApi Test - Writing to file"""

import requests
import json

API_KEY = "850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c"

with open('/Users/udishkolnik/543/D.E.L.T.A/API_Abilities/api_test_result.txt', 'w') as f:
    f.write("Testing SerpApi - Google Search\n")
    f.write("="*60 + "\n\n")
    
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": "pizza restaurant new york",
        "api_key": API_KEY,
        "location": "New York, NY",
        "num": 5
    }
    
    f.write(f"Making request to: {url}\n")
    f.write(f"Keyword: pizza restaurant new york\n\n")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        f.write(f"Status Code: {response.status_code}\n\n")
        
        if response.status_code == 200:
            data = response.json()
            f.write("✅ SUCCESS! Got REAL data from SerpApi\n\n")
            f.write(json.dumps(data, indent=2)[:2000])  # First 2000 chars
            f.write("\n\n... (truncated)")
        else:
            f.write(f"❌ Error: {response.text}\n")
            
    except Exception as e:
        f.write(f"❌ Exception: {e}\n")
    
    f.write("\n" + "="*60 + "\n")

