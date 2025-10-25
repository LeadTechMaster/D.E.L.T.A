#!/usr/bin/env python3
"""
TEST KEYWORD SEARCH & GMB FUNCTIONS - REAL API CALLS
Tests one by one and displays results
"""

import sys
sys.path.insert(0, '/Users/udishkolnik/543/D.E.L.T.A/API_Abilities')

from SerpApi.keyword_suggestions import get_keyword_suggestions
from SerpApi.people_also_ask import get_people_also_ask
from SerpApi.local_pack_results import get_local_pack_results
from Google_Places.gmb_listing_info import get_gmb_listing_info
from Google_Places.place_details import get_place_details

import json

def print_header(title):
    print("\n" + "="*70)
    print(title)
    print("="*70 + "\n")

def print_result(result):
    print(json.dumps(result, indent=2))

# TEST 1: Keyword Suggestions
print_header("TEST 1: KEYWORD SUGGESTIONS - get_keyword_suggestions('pizza')")
result1 = get_keyword_suggestions("pizza")
if result1.get("status") == "success":
    print(f"✅ SUCCESS! Got {result1.get('total_suggestions', 0)} suggestions")
    print(f"\nFirst 5 suggestions:")
    for i, sug in enumerate(result1.get("suggestions", [])[:5], 1):
        print(f"  {i}. {sug}")
else:
    print(f"❌ ERROR: {result1.get('error', 'Unknown error')}")

# TEST 2: People Also Ask
print_header("TEST 2: PEOPLE ALSO ASK - get_people_also_ask('pizza restaurant')")
result2 = get_people_also_ask("pizza restaurant")
if result2.get("status") == "success":
    print(f"✅ SUCCESS! Got {result2.get('total_questions', 0)} questions")
    print(f"\nFirst 3 questions:")
    for i, q in enumerate(result2.get("questions", [])[:3], 1):
        print(f"\n  {i}. {q.get('question', 'N/A')}")
        print(f"     Answer: {q.get('answer', 'N/A')[:100]}...")
else:
    print(f"❌ ERROR: {result2.get('error', 'Unknown error')}")

# TEST 3: Local Pack Results
print_header("TEST 3: LOCAL PACK - get_local_pack_results('pizza', 'New York, NY')")
result3 = get_local_pack_results("pizza", "New York, NY")
if result3.get("status") == "success":
    print(f"✅ SUCCESS! Got {result3.get('total_results', 0)} local businesses")
    print(f"\nTop 3 businesses:")
    for i, biz in enumerate(result3.get("local_pack", [])[:3], 1):
        print(f"\n  {i}. {biz.get('title', 'N/A')}")
        print(f"     Address: {biz.get('address', 'N/A')}")
        print(f"     Rating: {biz.get('rating', 'N/A')} ({biz.get('reviews', 0)} reviews)")
        print(f"     Phone: {biz.get('phone', 'N/A')}")
else:
    print(f"❌ ERROR: {result3.get('error', 'Unknown error')}")

# TEST 4: GMB Place Details (using a well-known place_id)
print_header("TEST 4: GMB PLACE DETAILS - get_place_details('ChIJN1t_tDeuEmsRUsoyG83frY4')")
result4 = get_place_details("ChIJN1t_tDeuEmsRUsoyG83frY4")  # Sydney Opera House
if result4.get("status") == "success":
    print(f"✅ SUCCESS! Got details for: {result4.get('name', 'N/A')}")
    print(f"\n  Name: {result4.get('name', 'N/A')}")
    print(f"  Address: {result4.get('address', 'N/A')}")
    print(f"  Phone: {result4.get('phone', 'N/A')}")
    print(f"  Website: {result4.get('website', 'N/A')}")
    print(f"  Rating: {result4.get('rating', 'N/A')}/5 ({result4.get('total_ratings', 0)} reviews)")
    print(f"  Types: {', '.join(result4.get('types', [])[:3])}")
else:
    print(f"❌ ERROR: {result4.get('error', 'Unknown error')}")

print_header("ALL TESTS COMPLETE!")
print("\n✅ If you see 'SUCCESS' messages above, the APIs are working with REAL DATA!")
print("❌ If you see 'ERROR' messages, check the error details above.\n")

