#!/usr/bin/env python3
"""
🍕 D.E.L.T.A CLI - Comprehensive Business Intelligence Terminal
Connects to ALL APIs and provides deep data analysis for business opportunities

Usage: python delta_cli.py
"""

import asyncio
import aiohttp
import json
import os
import sys
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import argparse
import time

# API Configuration
API_BASE_URL = "http://localhost:8001"
BOT_BASE_URL = "http://localhost:8002"

@dataclass
class BusinessAnalysis:
    """Complete business analysis data structure"""
    business_type: str
    location: str
    coordinates: Tuple[float, float]
    competitors: List[Dict]
    demographics: Dict
    heatmap_layers: Dict[str, Any]
    market_opportunity: Dict
    franchise_data: Dict
    social_media_insights: Dict
    advertising_data: Dict
    search_trends: Dict
    investment_analysis: Dict

class DeltaCLI:
    """D.E.L.T.A CLI - Comprehensive Business Intelligence Terminal"""
    
    def __init__(self):
        self.session = None
        self.current_analysis: Optional[BusinessAnalysis] = None
        self.available_apis = []
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        await self.check_api_status()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def check_api_status(self):
        """Check status of all available APIs"""
        print("🔍 Checking API Status...")
        
        try:
            async with self.session.get(f"{API_BASE_URL}/api/v1/status") as response:
                if response.status == 200:
                    data = await response.json()
                    self.available_apis = data.get('services', {})
                    print(f"✅ Backend API: Active")
                    for service, status in self.available_apis.items():
                        emoji = "✅" if status == "active" else "❌"
                        print(f"  {emoji} {service.title()}: {status}")
                else:
                    print("❌ Backend API: Inactive")
        except Exception as e:
            print(f"❌ Backend API: Connection failed - {e}")
        
        # Check bot status
        try:
            async with self.session.get(f"{BOT_BASE_URL}/health") as response:
                if response.status == 200:
                    print("✅ Bot API: Active")
                else:
                    print("❌ Bot API: Inactive")
        except Exception as e:
            print(f"❌ Bot API: Connection failed - {e}")
        
        print()
    
    async def geocode_location(self, location: str) -> Tuple[float, float]:
        """Get coordinates for a location using Mapbox"""
        try:
            url = f"{API_BASE_URL}/api/v1/mapbox/geocode"
            params = {"query": location}
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('features'):
                        feature = data['features'][0]
                        coords = feature['center']
                        return coords[1], coords[0]  # lat, lng
        except Exception as e:
            print(f"❌ Geocoding error: {e}")
        
        return None, None
    
    async def search_businesses(self, business_type: str, lat: float, lng: float, radius: float = 5000) -> List[Dict]:
        """Search for businesses using Google Places API"""
        try:
            url = f"{API_BASE_URL}/api/v1/google-places/search"
            params = {
                "query": business_type,
                "location": f"{lat},{lng}",
                "radius": radius
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('businesses', [])
        except Exception as e:
            print(f"❌ Business search error: {e}")
        
        return []
    
    async def get_demographics(self, lat: float, lng: float) -> Dict:
        """Get demographic data using Census API"""
        try:
            # Use state code for now (NY = 36)
            url = f"{API_BASE_URL}/api/v1/census/demographics"
            params = {"state_code": "36"}  # New York
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('demographics', {})
        except Exception as e:
            print(f"❌ Demographics error: {e}")
        
        return {}
    
    async def get_heatmap_layers(self, business_type: str, lat: float, lng: float, radius_km: float = 5.0) -> Dict[str, Any]:
        """Get all available heatmap layers"""
        layers = {}
        layer_types = [
            "business_competition",
            "market_opportunity", 
            "demographic_density",
            "income_wealth",
            "foot_traffic",
            "review_power"
        ]
        
        print("🔥 Generating heatmap analysis layers...")
        
        for layer_type in layer_types:
            try:
                url = f"{API_BASE_URL}/api/v1/heatmap/{layer_type}"
                params = {
                    "lat": lat,
                    "lng": lng,
                    "radius_km": radius_km,
                    "business_type": business_type
                }
                
                async with self.session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        layers[layer_type] = data
                        print(f"  ✅ {layer_type}: {data.get('total_points', 0)} data points")
                    else:
                        print(f"  ❌ {layer_type}: Failed")
            except Exception as e:
                print(f"  ❌ {layer_type}: Error - {e}")
        
        return layers
    
    async def get_search_trends(self, business_type: str, location: str) -> Dict:
        """Get search trends using SerpAPI"""
        try:
            url = f"{API_BASE_URL}/api/v1/serpapi/search"
            params = {
                "query": f"{business_type} {location}",
                "location": location
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
        except Exception as e:
            print(f"❌ Search trends error: {e}")
        
        return {}
    
    async def get_franchise_data(self, business_type: str) -> Dict:
        """Get franchise information using SerpAPI"""
        try:
            url = f"{API_BASE_URL}/api/v1/serpapi/search"
            params = {
                "query": f"{business_type} franchise opportunities investment cost",
                "location": "United States"
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
        except Exception as e:
            print(f"❌ Franchise data error: {e}")
        
        return {}
    
    async def get_meta_ads_data(self, business_type: str, location: str) -> Dict:
        """Get Meta Ads data for competitor analysis"""
        try:
            url = f"{API_BASE_URL}/api/v1/meta-ads/search"
            params = {
                "query": business_type,
                "location": location
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
        except Exception as e:
            print(f"❌ Meta Ads data error: {e}")
        
        return {}
    
    async def comprehensive_analysis(self, business_type: str, location: str) -> BusinessAnalysis:
        """Perform comprehensive business analysis using ALL available APIs"""
        print(f"\n🎯 COMPREHENSIVE ANALYSIS: {business_type.upper()} in {location.upper()}")
        print("=" * 80)
        
        # Step 1: Geocode location
        print(f"📍 Step 1: Geocoding {location}...")
        lat, lng = await self.geocode_location(location)
        if not lat or not lng:
            raise Exception(f"Could not geocode location: {location}")
        print(f"✅ Coordinates: {lat:.4f}, {lng:.4f}")
        
        # Step 2: Search for competitors
        print(f"\n🏢 Step 2: Analyzing competitors...")
        competitors = await self.search_businesses(business_type, lat, lng)
        print(f"✅ Found {len(competitors)} competitors")
        
        # Step 3: Get demographics
        print(f"\n👥 Step 3: Analyzing demographics...")
        demographics = await self.get_demographics(lat, lng)
        print(f"✅ Demographics data retrieved")
        
        # Step 4: Generate heatmap layers
        print(f"\n🔥 Step 4: Generating heatmap analysis...")
        heatmap_layers = await self.get_heatmap_layers(business_type, lat, lng)
        
        # Step 5: Get search trends
        print(f"\n📊 Step 5: Analyzing search trends...")
        search_trends = await self.get_search_trends(business_type, location)
        print(f"✅ Search trends analyzed")
        
        # Step 6: Get franchise data
        print(f"\n🏆 Step 6: Researching franchise opportunities...")
        franchise_data = await self.get_franchise_data(business_type)
        print(f"✅ Franchise data retrieved")
        
        # Step 7: Get Meta Ads data
        print(f"\n📱 Step 7: Analyzing competitor advertising...")
        meta_ads_data = await self.get_meta_ads_data(business_type, location)
        print(f"✅ Advertising analysis complete")
        
        # Calculate market opportunity score
        market_opportunity = self.calculate_market_opportunity(
            competitors, demographics, heatmap_layers
        )
        
        # Calculate investment analysis
        investment_analysis = self.calculate_investment_analysis(
            competitors, franchise_data, demographics
        )
        
        analysis = BusinessAnalysis(
            business_type=business_type,
            location=location,
            coordinates=(lat, lng),
            competitors=competitors,
            demographics=demographics,
            heatmap_layers=heatmap_layers,
            market_opportunity=market_opportunity,
            franchise_data=franchise_data,
            social_media_insights=meta_ads_data,
            advertising_data=meta_ads_data,
            search_trends=search_trends,
            investment_analysis=investment_analysis
        )
        
        self.current_analysis = analysis
        return analysis
    
    def calculate_market_opportunity(self, competitors: List[Dict], demographics: Dict, heatmap_layers: Dict) -> Dict:
        """Calculate market opportunity score"""
        competitor_count = len(competitors)
        
        # Calculate average competitor rating
        avg_rating = 0
        total_reviews = 0
        for competitor in competitors:
            rating = competitor.get('rating', 0)
            reviews = competitor.get('user_ratings_total', 0)
            if rating > 0:
                avg_rating += rating * reviews
                total_reviews += reviews
        
        avg_rating = avg_rating / total_reviews if total_reviews > 0 else 0
        
        # Market saturation score (lower is better)
        saturation_score = min(competitor_count / 10, 1.0)  # Max 1.0 for 10+ competitors
        
        # Opportunity score (higher is better)
        opportunity_score = max(0, 1.0 - saturation_score)
        
        return {
            "competitor_count": competitor_count,
            "average_competitor_rating": round(avg_rating, 2),
            "total_reviews": total_reviews,
            "market_saturation": round(saturation_score, 2),
            "opportunity_score": round(opportunity_score, 2),
            "recommendation": "HIGH OPPORTUNITY" if opportunity_score > 0.7 else "MODERATE OPPORTUNITY" if opportunity_score > 0.4 else "LOW OPPORTUNITY"
        }
    
    def calculate_investment_analysis(self, competitors: List[Dict], franchise_data: Dict, demographics: Dict) -> Dict:
        """Calculate investment analysis"""
        # Estimate startup costs based on business type and location
        base_cost = 50000  # Base startup cost
        location_multiplier = 2.5  # Manhattan is expensive
        total_estimated_cost = base_cost * location_multiplier
        
        # Calculate potential revenue based on demographics and competition
        population_factor = 1.5  # High population density
        competition_factor = max(0.3, 1.0 - (len(competitors) / 20))
        estimated_monthly_revenue = 15000 * population_factor * competition_factor
        
        # ROI calculation
        monthly_profit_margin = 0.2  # 20% profit margin
        monthly_profit = estimated_monthly_revenue * monthly_profit_margin
        months_to_roi = total_estimated_cost / monthly_profit if monthly_profit > 0 else 999
        
        return {
            "estimated_startup_cost": f"${total_estimated_cost:,.0f}",
            "estimated_monthly_revenue": f"${estimated_monthly_revenue:,.0f}",
            "estimated_monthly_profit": f"${monthly_profit:,.0f}",
            "months_to_roi": round(months_to_roi, 1),
            "risk_level": "HIGH" if len(competitors) > 15 else "MODERATE" if len(competitors) > 8 else "LOW",
            "investment_recommendation": "PROCEED" if months_to_roi < 24 and len(competitors) < 10 else "CAUTIOUS" if months_to_roi < 36 else "RECONSIDER"
        }
    
    def display_analysis_summary(self, analysis: BusinessAnalysis):
        """Display comprehensive analysis summary"""
        print(f"\n📋 COMPREHENSIVE ANALYSIS SUMMARY")
        print("=" * 80)
        
        # Basic Info
        print(f"🏢 Business Type: {analysis.business_type.title()}")
        print(f"📍 Location: {analysis.location}")
        print(f"🗺️  Coordinates: {analysis.coordinates[0]:.4f}, {analysis.coordinates[1]:.4f}")
        
        # Market Opportunity
        print(f"\n🎯 MARKET OPPORTUNITY ANALYSIS:")
        print(f"  • Competitors Found: {analysis.market_opportunity['competitor_count']}")
        print(f"  • Average Competitor Rating: {analysis.market_opportunity['average_competitor_rating']}/5.0")
        print(f"  • Total Reviews in Area: {analysis.market_opportunity['total_reviews']:,}")
        print(f"  • Market Saturation: {analysis.market_opportunity['market_saturation']:.1%}")
        print(f"  • Opportunity Score: {analysis.market_opportunity['opportunity_score']:.1%}")
        print(f"  • Recommendation: {analysis.market_opportunity['recommendation']}")
        
        # Investment Analysis
        print(f"\n💰 INVESTMENT ANALYSIS:")
        print(f"  • Estimated Startup Cost: {analysis.investment_analysis['estimated_startup_cost']}")
        print(f"  • Estimated Monthly Revenue: {analysis.investment_analysis['estimated_monthly_revenue']}")
        print(f"  • Estimated Monthly Profit: {analysis.investment_analysis['estimated_monthly_profit']}")
        print(f"  • Months to ROI: {analysis.investment_analysis['months_to_roi']}")
        print(f"  • Risk Level: {analysis.investment_analysis['risk_level']}")
        print(f"  • Investment Recommendation: {analysis.investment_analysis['investment_recommendation']}")
        
        # Heatmap Analysis
        print(f"\n🔥 HEATMAP ANALYSIS:")
        for layer_type, layer_data in analysis.heatmap_layers.items():
            points = layer_data.get('total_points', 0)
            print(f"  • {layer_type.replace('_', ' ').title()}: {points} data points")
        
        # Top Competitors
        print(f"\n🏆 TOP COMPETITORS:")
        for i, competitor in enumerate(analysis.competitors[:5], 1):
            name = competitor.get('name', 'Unknown')
            rating = competitor.get('rating', 'N/A')
            reviews = competitor.get('user_ratings_total', 0)
            print(f"  {i}. {name} - {rating}/5.0 ({reviews:,} reviews)")
    
    def display_detailed_competitors(self):
        """Display detailed competitor analysis"""
        if not self.current_analysis:
            print("❌ No analysis available. Run analysis first.")
            return
        
        print(f"\n🏢 DETAILED COMPETITOR ANALYSIS")
        print("=" * 80)
        
        for i, competitor in enumerate(self.current_analysis.competitors, 1):
            print(f"\n{i}. {competitor.get('name', 'Unknown Business')}")
            print(f"   📍 Address: {competitor.get('address', 'N/A')}")
            print(f"   ⭐ Rating: {competitor.get('rating', 'N/A')}/5.0")
            print(f"   📝 Reviews: {competitor.get('user_ratings_total', 0):,}")
            print(f"   💰 Price Level: {'$' * competitor.get('price_level', 0)}")
            print(f"   🏷️  Types: {', '.join(competitor.get('types', [])[:3])}")
            if competitor.get('place_id'):
                print(f"   🔗 Place ID: {competitor['place_id']}")
    
    def display_heatmap_details(self):
        """Display detailed heatmap analysis"""
        if not self.current_analysis:
            print("❌ No analysis available. Run analysis first.")
            return
        
        print(f"\n🔥 DETAILED HEATMAP ANALYSIS")
        print("=" * 80)
        
        for layer_type, layer_data in self.current_analysis.heatmap_layers.items():
            print(f"\n📊 {layer_type.replace('_', ' ').title()}:")
            print(f"   • Total Points: {layer_data.get('total_points', 0)}")
            print(f"   • Center: {layer_data.get('center', {})}")
            print(f"   • Radius: {layer_data.get('radius_km', 0)} km")
            print(f"   • Business Type: {layer_data.get('business_type', 'N/A')}")
    
    def save_analysis_report(self, filename: str = None):
        """Save analysis to JSON file"""
        if not self.current_analysis:
            print("❌ No analysis available to save.")
            return
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"delta_analysis_{timestamp}.json"
        
        # Convert analysis to dictionary
        analysis_dict = {
            "business_type": self.current_analysis.business_type,
            "location": self.current_analysis.location,
            "coordinates": self.current_analysis.coordinates,
            "timestamp": datetime.now().isoformat(),
            "market_opportunity": self.current_analysis.market_opportunity,
            "investment_analysis": self.current_analysis.investment_analysis,
            "competitors": self.current_analysis.competitors,
            "demographics": self.current_analysis.demographics,
            "heatmap_layers": self.current_analysis.heatmap_layers,
            "franchise_data": self.current_analysis.franchise_data,
            "search_trends": self.current_analysis.search_trends
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(analysis_dict, f, indent=2, default=str)
            print(f"✅ Analysis saved to: {filename}")
        except Exception as e:
            print(f"❌ Error saving analysis: {e}")
    
    async def interactive_mode(self):
        """Interactive CLI mode"""
        print("🍕 D.E.L.T.A CLI - Interactive Mode")
        print("Type 'help' for commands or 'quit' to exit")
        print("=" * 50)
        
        while True:
            try:
                command = input("\n🍕 D.E.L.T.A> ").strip().lower()
                
                if command == 'quit' or command == 'exit':
                    print("👋 Goodbye!")
                    break
                
                elif command == 'help':
                    self.show_help()
                
                elif command == 'status':
                    await self.check_api_status()
                
                elif command.startswith('analyze '):
                    parts = command.split(' ', 2)
                    if len(parts) >= 3:
                        business_type = parts[1]
                        location = parts[2]
                        await self.comprehensive_analysis(business_type, location)
                        self.display_analysis_summary(self.current_analysis)
                    else:
                        print("❌ Usage: analyze <business_type> <location>")
                        print("   Example: analyze pizza manhattan")
                
                elif command == 'competitors':
                    self.display_detailed_competitors()
                
                elif command == 'heatmaps':
                    self.display_heatmap_details()
                
                elif command == 'save':
                    self.save_analysis_report()
                
                elif command == 'summary':
                    if self.current_analysis:
                        self.display_analysis_summary(self.current_analysis)
                    else:
                        print("❌ No analysis available. Run 'analyze' first.")
                
                else:
                    print("❌ Unknown command. Type 'help' for available commands.")
            
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def show_help(self):
        """Show help information"""
        print("\n📖 D.E.L.T.A CLI Commands:")
        print("=" * 40)
        print("analyze <business> <location>  - Run comprehensive analysis")
        print("competitors                   - Show detailed competitor data")
        print("heatmaps                      - Show heatmap analysis details")
        print("summary                       - Show analysis summary")
        print("save                          - Save analysis to JSON file")
        print("status                        - Check API status")
        print("help                          - Show this help")
        print("quit/exit                     - Exit the CLI")
        print("\n💡 Example: analyze pizza manhattan")

async def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="D.E.L.T.A CLI - Business Intelligence Terminal")
    parser.add_argument('--business', '-b', help='Business type to analyze')
    parser.add_argument('--location', '-l', help='Location to analyze')
    parser.add_argument('--interactive', '-i', action='store_true', help='Start interactive mode')
    parser.add_argument('--output', '-o', help='Output file for analysis results')
    
    args = parser.parse_args()
    
    async with DeltaCLI() as cli:
        if args.business and args.location:
            # Direct analysis mode
            print(f"🎯 Analyzing {args.business} in {args.location}...")
            analysis = await cli.comprehensive_analysis(args.business, args.location)
            cli.display_analysis_summary(analysis)
            
            if args.output:
                cli.save_analysis_report(args.output)
        
        elif args.interactive:
            # Interactive mode
            await cli.interactive_mode()
        
        else:
            # Default: show help and start interactive mode
            print("🍕 D.E.L.T.A CLI - Business Intelligence Terminal")
            print("=" * 60)
            cli.show_help()
            print("\n🚀 Starting interactive mode...")
            await cli.interactive_mode()

if __name__ == "__main__":
    asyncio.run(main())



