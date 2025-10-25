#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  TESTING KEYWORD SEARCH & GMB FUNCTIONS - REAL API CALLS      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

cd /Users/udishkolnik/543/D.E.L.T.A

# Test 1: Keyword Suggestions
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 1: Keyword Suggestions for 'pizza'"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 -c "
import sys
sys.path.insert(0, '/Users/udishkolnik/543/D.E.L.T.A/API_Abilities')
from SerpApi.keyword_suggestions import get_keyword_suggestions
import json
result = get_keyword_suggestions('pizza')
print(f\"Status: {result.get('status')}\")
if result.get('status') == 'success':
    print(f\"✅ SUCCESS! Got {result.get('total_suggestions', 0)} suggestions\")
    print('\\nFirst 10 suggestions:')
    for i, s in enumerate(result.get('suggestions', [])[:10], 1):
        print(f\"  {i}. {s}\")
else:
    print(f\"❌ ERROR: {result.get('error')}\")
"
echo ""

# Test 2: People Also Ask
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 2: People Also Ask for 'pizza restaurant'"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 -c "
import sys
sys.path.insert(0, '/Users/udishkolnik/543/D.E.L.T.A/API_Abilities')
from SerpApi.people_also_ask import get_people_also_ask
result = get_people_also_ask('pizza restaurant')
print(f\"Status: {result.get('status')}\")
if result.get('status') == 'success':
    print(f\"✅ SUCCESS! Got {result.get('total_questions', 0)} questions\")
    print('\\nQuestions:')
    for i, q in enumerate(result.get('questions', [])[:5], 1):
        print(f\"  {i}. {q.get('question')}\")
else:
    print(f\"❌ ERROR: {result.get('error')}\")
"
echo ""

# Test 3: Local Pack Results
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 3: Local Pack Results for 'pizza' in 'New York, NY'"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 -c "
import sys
sys.path.insert(0, '/Users/udishkolnik/543/D.E.L.T.A/API_Abilities')
from SerpApi.local_pack_results import get_local_pack_results
result = get_local_pack_results('pizza', 'New York, NY')
print(f\"Status: {result.get('status')}\")
if result.get('status') == 'success':
    print(f\"✅ SUCCESS! Got {result.get('total_results', 0)} businesses\")
    print('\\nTop 5 businesses:')
    for i, biz in enumerate(result.get('local_pack', [])[:5], 1):
        print(f\"\\n  {i}. {biz.get('title')}\")
        print(f\"     Address: {biz.get('address')}\")
        print(f\"     Rating: {biz.get('rating')} ⭐ ({biz.get('reviews')} reviews)\")
        print(f\"     Phone: {biz.get('phone')}\")
else:
    print(f\"❌ ERROR: {result.get('error')}\")
"
echo ""

# Test 4: GMB Place Details
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 4: GMB Place Details (Sydney Opera House)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 -c "
import sys
sys.path.insert(0, '/Users/udishkolnik/543/D.E.L.T.A/API_Abilities')
from Google_Places.place_details import get_place_details
result = get_place_details('ChIJN1t_tDeuEmsRUsoyG83frY4')
print(f\"Status: {result.get('status')}\")
if result.get('status') == 'success':
    print(f\"✅ SUCCESS! Got details for: {result.get('name')}\")
    print(f\"\\n  Name: {result.get('name')}\")
    print(f\"  Address: {result.get('address')}\")
    print(f\"  Phone: {result.get('phone')}\")
    print(f\"  Website: {result.get('website')}\")
    print(f\"  Rating: {result.get('rating')}/5 ⭐ ({result.get('total_ratings')} reviews)\")
    print(f\"  Photos: {result.get('photos', [])[:1]}\")
else:
    print(f\"❌ ERROR: {result.get('error')}\")
"
echo ""

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                   ALL TESTS COMPLETE!                          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "✅ If you see SUCCESS messages above, APIs are working with REAL DATA!"
echo "❌ If you see ERROR messages, check API keys and network connection."
echo ""

