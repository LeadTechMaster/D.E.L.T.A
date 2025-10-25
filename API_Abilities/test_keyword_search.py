#!/usr/bin/env python3
"""
Test Keyword Search Volume - REAL API CALL
"""

import sys
sys.path.insert(0, '/Users/udishkolnik/543/D.E.L.T.A/API_Abilities')

from SerpApi.keyword_search_volume import get_keyword_search_volume
import json

print("="*60)
print("TESTING: Keyword Search Volume (REAL API)")
print("="*60)
print()

# Test with a real keyword
keyword = "pizza restaurant"
location = "US"

print(f"Testing keyword: '{keyword}'")
print(f"Location: {location}")
print()
print("Making REAL API call to SerpApi...")
print()

result = get_keyword_search_volume(keyword, location)

print("RESULT:")
print(json.dumps(result, indent=2))
print()

if result.get("status") == "success":
    print("✅ SUCCESS! Got real data from SerpApi")
else:
    print("❌ ERROR:", result.get("error"))

print()
print("="*60)

