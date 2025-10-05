#!/usr/bin/env python3
"""
Test enhanced API integrations
"""

import asyncio
import sys
import os
sys.path.append('.')

async def test_meta_ads():
    try:
        from enhanced_meta_ads_integration import get_meta_ads_intelligence
        
        print("🔍 Testing Meta Ads Integration...")
        result = await get_meta_ads_intelligence('butcher shop', 'dallas')
        
        print(f"✅ Success: {result.get('success', False)}")
        if result.get('success'):
            analysis = result.get('analysis', {})
            print(f"📊 Total Ads Found: {result.get('total_ads', 0)}")
            print(f"🎯 Market Activity: {analysis.get('market_activity', 'Unknown')}")
            print(f"💰 Estimated Competitor Spend: ${analysis.get('estimated_competitor_spend', 0)}")
            print(f"💡 Insights: {analysis.get('insights', [])}")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Meta Ads test failed: {e}")

async def test_brightlocal():
    try:
        from enhanced_brightlocal_integration import get_brightlocal_intelligence
        
        print("\n🔍 Testing Brightlocal Integration...")
        result = await get_brightlocal_intelligence('butcher shop', 'dallas')
        
        print(f"✅ Success: {result.get('success', False)}")
        if result.get('success'):
            analysis = result.get('analysis', {})
            print(f"📊 Total Results: {result.get('total_results', 0)}")
            print(f"⭐ Average Rating: {analysis.get('average_rating', 0)}")
            print(f"📝 Total Reviews: {analysis.get('total_reviews', 0)}")
            print(f"🔗 Citation Sources: {analysis.get('citation_sources', 0)}")
            print(f"💡 Insights: {analysis.get('insights', [])}")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Brightlocal test failed: {e}")

async def main():
    print("🚀 Testing Enhanced API Integrations")
    print("=" * 50)
    
    await test_meta_ads()
    await test_brightlocal()
    
    print("\n🎉 Enhanced API testing complete!")

if __name__ == "__main__":
    asyncio.run(main())
