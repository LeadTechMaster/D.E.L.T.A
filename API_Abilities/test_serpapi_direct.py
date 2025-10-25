#!/usr/bin/env python3
"""Direct SerpApi Test"""

import requests
import json

API_KEY = "850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c"

print("Testing SerpApi - Google Trends")
print("="*60)

url = "https://serpapi.com/search"
params = {
    "engine": "google_trends",
    "q": "pizza",
    "api_key": API_KEY,
    "data_type": "TIMESERIES"
}

print(f"Making request to: {url}")
print(f"Params: {params}")
print()

try:
    response = requests.get(url, params=params, timeout=30)
    print(f"Status Code: {response.status_code}")
    print()
    
    if response.status_code == 200:
        data = response.json()
        print("SUCCESS! Got data:")
        print(json.dumps(data, indent=2)[:500])  # First 500 chars
    else:
        print(f"Error: {response.text}")
        
except Exception as e:
    print(f"Exception: {e}")

print("="*60)

