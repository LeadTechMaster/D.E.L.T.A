#!/usr/bin/env python3
"""Test Keyword Functions with REAL API Calls - Show Actual Data"""

import sys
sys.path.insert(0, '/Users/udishkolnik/543/D.E.L.T.A/API_Abilities')

import json
from datetime import datetime

# Import the functions
from SerpApi.keyword_suggestions import get_keyword_suggestions
from SerpApi.people_also_ask import get_people_also_ask
from SerpApi.local_pack_results import get_local_pack_results
from SerpApi.keyword_search_volume import get_keyword_search_volume

output = []

def log(msg):
    print(msg)
    output.append(msg)

log("="*80)
log("KEYWORD SEARCH FUNCTIONS - REAL API TEST RESULTS")
log(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
log("="*80)
log("")

# TEST 1: Keyword Suggestions
log("━"*80)
log("TEST 1: Keyword Suggestions - get_keyword_suggestions('pizza restaurant')")
log("━"*80)
try:
    result1 = get_keyword_suggestions("pizza restaurant")
    
    if result1.get("status") == "success":
        log("✅ STATUS: WORKING - Got REAL data from SerpApi")
        log(f"   Total Suggestions: {result1.get('total_suggestions', 0)}")
        log("")
        log("   REAL Keyword Suggestions:")
        for i, suggestion in enumerate(result1.get("suggestions", [])[:10], 1):
            log(f"   {i}. {suggestion}")
        log("")
        log(f"   API Response: {result1.get('data_source', 'SerpApi')}")
    else:
        log(f"❌ STATUS: NOT WORKING")
        log(f"   Error: {result1.get('error', 'Unknown error')}")
        
except Exception as e:
    log(f"❌ STATUS: EXCEPTION")
    log(f"   Error: {str(e)}")

log("")

# TEST 2: People Also Ask
log("━"*80)
log("TEST 2: People Also Ask - get_people_also_ask('best pizza')")
log("━"*80)
try:
    result2 = get_people_also_ask("best pizza")
    
    if result2.get("status") == "success":
        log("✅ STATUS: WORKING - Got REAL data from SerpApi")
        log(f"   Total Questions: {result2.get('total_questions', 0)}")
        log("")
        log("   REAL People Also Ask Questions:")
        for i, q in enumerate(result2.get("questions", [])[:5], 1):
            log(f"   {i}. Q: {q.get('question', 'N/A')}")
            answer = q.get('answer', 'N/A')
            if len(answer) > 100:
                answer = answer[:100] + "..."
            log(f"      A: {answer}")
            log("")
    else:
        log(f"❌ STATUS: NOT WORKING")
        log(f"   Error: {result2.get('error', 'Unknown error')}")
        
except Exception as e:
    log(f"❌ STATUS: EXCEPTION")
    log(f"   Error: {str(e)}")

log("")

# TEST 3: Local Pack Results
log("━"*80)
log("TEST 3: Local Pack - get_local_pack_results('pizza', 'New York, NY')")
log("━"*80)
try:
    result3 = get_local_pack_results("pizza", "New York, NY")
    
    if result3.get("status") == "success":
        log("✅ STATUS: WORKING - Got REAL data from SerpApi")
        log(f"   Total Businesses Found: {result3.get('total_results', 0)}")
        log("")
        log("   REAL Local Pack Results (Top 5 Pizza Places in NYC):")
        for i, biz in enumerate(result3.get("local_pack", [])[:5], 1):
            log(f"   {i}. {biz.get('title', 'N/A')}")
            log(f"      📍 Address: {biz.get('address', 'N/A')}")
            log(f"      ⭐ Rating: {biz.get('rating', 'N/A')} ({biz.get('reviews', 0)} reviews)")
            log(f"      📞 Phone: {biz.get('phone', 'N/A')}")
            log(f"      🕒 Hours: {biz.get('hours', 'N/A')}")
            log("")
    else:
        log(f"❌ STATUS: NOT WORKING")
        log(f"   Error: {result3.get('error', 'Unknown error')}")
        
except Exception as e:
    log(f"❌ STATUS: EXCEPTION")
    log(f"   Error: {str(e)}")

log("")

# TEST 4: Keyword Search Volume
log("━"*80)
log("TEST 4: Search Volume - get_keyword_search_volume('pizza')")
log("━"*80)
try:
    result4 = get_keyword_search_volume("pizza", "US")
    
    if result4.get("status") == "success":
        log("✅ STATUS: WORKING - Got REAL data from SerpApi")
        log(f"   Keyword: {result4.get('keyword', 'N/A')}")
        log(f"   Location: {result4.get('location', 'N/A')}")
        log("")
        log("   REAL Search Volume Data:")
        data = result4.get('data', {})
        if 'interest_over_time' in data:
            log(f"   Interest Over Time: {data.get('interest_over_time', {}).get('timeline_data', [])[:3]}")
    else:
        log(f"❌ STATUS: NOT WORKING")
        log(f"   Error: {result4.get('error', 'Unknown error')}")
        
except Exception as e:
    log(f"❌ STATUS: EXCEPTION")
    log(f"   Error: {str(e)}")

log("")
log("="*80)
log("TEST SUMMARY")
log("="*80)
log("")
log("✅ = Function works with REAL API data")
log("❌ = Function has errors or not working")
log("")
log("All data above is REAL - pulled from live APIs!")
log("="*80)

# Write to file
with open('/Users/udishkolnik/543/D.E.L.T.A/KEYWORD_TEST_RESULTS.txt', 'w') as f:
    f.write('\n'.join(output))

print("\n📝 Full results saved to: KEYWORD_TEST_RESULTS.txt")

