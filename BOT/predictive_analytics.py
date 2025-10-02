"""
Advanced Predictive Analytics System
Provides market forecasting, trend analysis, and predictive insights
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import math
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MarketTrend:
    """Represents a market trend analysis"""
    business_type: str
    location: str
    trend_direction: str  # "growing", "stable", "declining"
    confidence: float
    factors: List[str]
    timeframe: str
    predicted_growth: float
    risk_level: str

@dataclass
class OpportunityScore:
    """Represents an opportunity scoring analysis"""
    overall_score: float
    market_saturation: float
    competition_level: float
    demographic_match: float
    economic_factors: float
    seasonality: float
    growth_potential: float
    recommendations: List[str]

class PredictiveAnalytics:
    """Advanced predictive analytics for business intelligence"""
    
    def __init__(self):
        """Initialize predictive analytics system"""
        self.market_indicators = self._build_market_indicators()
        self.seasonal_patterns = self._build_seasonal_patterns()
        self.economic_factors = self._build_economic_factors()
        logger.info("📊 Advanced predictive analytics system initialized")
    
    def _build_market_indicators(self) -> Dict[str, Dict[str, Any]]:
        """Build market indicators for different business types"""
        return {
            "coffee shop": {
                "growth_rate": 0.08,
                "seasonality": {"spring": 1.1, "summer": 1.2, "fall": 1.0, "winter": 0.9},
                "demographic_factors": ["population_density", "median_income", "education_level"],
                "competition_threshold": 0.7,
                "market_maturity": "mature"
            },
            "restaurant": {
                "growth_rate": 0.05,
                "seasonality": {"spring": 1.0, "summer": 1.1, "fall": 1.0, "winter": 0.95},
                "demographic_factors": ["population_density", "median_income", "age_distribution"],
                "competition_threshold": 0.8,
                "market_maturity": "mature"
            },
            "retail": {
                "growth_rate": 0.03,
                "seasonality": {"spring": 1.0, "summer": 0.9, "fall": 1.3, "winter": 1.2},
                "demographic_factors": ["population_density", "median_income", "disposable_income"],
                "competition_threshold": 0.9,
                "market_maturity": "mature"
            },
            "bookstore": {
                "growth_rate": -0.02,
                "seasonality": {"spring": 1.0, "summer": 0.8, "fall": 1.2, "winter": 1.1},
                "demographic_factors": ["education_level", "median_income", "population_density"],
                "competition_threshold": 0.6,
                "market_maturity": "declining"
            },
            "gym": {
                "growth_rate": 0.12,
                "seasonality": {"spring": 1.3, "summer": 1.4, "fall": 0.8, "winter": 0.9},
                "demographic_factors": ["median_income", "age_distribution", "health_consciousness"],
                "competition_threshold": 0.7,
                "market_maturity": "growing"
            },
            "laundry service": {
                "growth_rate": 0.04,
                "seasonality": {"spring": 1.0, "summer": 1.1, "fall": 1.0, "winter": 1.0},
                "demographic_factors": ["population_density", "apartment_ratio", "median_income"],
                "competition_threshold": 0.5,
                "market_maturity": "stable"
            },
            "pet care": {
                "growth_rate": 0.15,
                "seasonality": {"spring": 1.2, "summer": 1.1, "fall": 1.0, "winter": 1.0},
                "demographic_factors": ["median_income", "pet_ownership", "disposable_income"],
                "competition_threshold": 0.6,
                "market_maturity": "growing"
            }
        }
    
    def _build_seasonal_patterns(self) -> Dict[str, Dict[str, float]]:
        """Build seasonal patterns for different business types"""
        return {
            "coffee shop": {
                "january": 0.95, "february": 0.98, "march": 1.05, "april": 1.08,
                "may": 1.1, "june": 1.15, "july": 1.2, "august": 1.18,
                "september": 1.1, "october": 1.05, "november": 1.0, "december": 0.95
            },
            "restaurant": {
                "january": 0.9, "february": 0.95, "march": 1.0, "april": 1.05,
                "may": 1.1, "june": 1.1, "july": 1.05, "august": 1.0,
                "september": 1.0, "october": 1.05, "november": 1.1, "december": 1.2
            },
            "retail": {
                "january": 1.3, "february": 0.9, "march": 1.0, "april": 1.0,
                "may": 1.0, "june": 0.9, "july": 0.9, "august": 0.95,
                "september": 1.0, "october": 1.1, "november": 1.2, "december": 1.4
            }
        }
    
    def _build_economic_factors(self) -> Dict[str, float]:
        """Build economic factors affecting business success"""
        return {
            "inflation_rate": 0.03,
            "unemployment_rate": 0.05,
            "interest_rate": 0.05,
            "consumer_confidence": 0.75,
            "disposable_income_growth": 0.02,
            "population_growth": 0.01
        }
    
    def analyze_market_trends(self, business_type: str, location: str, 
                            demographics: Dict[str, Any], 
                            competition_data: Dict[str, Any]) -> MarketTrend:
        """Analyze market trends for a business type and location"""
        
        # Get market indicators
        indicators = self.market_indicators.get(business_type, {
            "growth_rate": 0.05,
            "seasonality": {"spring": 1.0, "summer": 1.0, "fall": 1.0, "winter": 1.0},
            "demographic_factors": ["population_density", "median_income"],
            "competition_threshold": 0.7,
            "market_maturity": "stable"
        })
        
        # Calculate trend direction
        base_growth = indicators["growth_rate"]
        
        # Adjust for demographic factors
        demographic_multiplier = self._calculate_demographic_multiplier(
            demographics, indicators["demographic_factors"]
        )
        
        # Adjust for competition
        competition_level = competition_data.get("competitor_count", 0) / 10.0
        competition_multiplier = max(0.5, 1.0 - (competition_level - indicators["competition_threshold"]))
        
        # Calculate final growth rate
        predicted_growth = base_growth * demographic_multiplier * competition_multiplier
        
        # Determine trend direction
        if predicted_growth > 0.05:
            trend_direction = "growing"
            risk_level = "low"
        elif predicted_growth > -0.02:
            trend_direction = "stable"
            risk_level = "medium"
        else:
            trend_direction = "declining"
            risk_level = "high"
        
        # Calculate confidence
        confidence = min(0.95, 0.7 + abs(predicted_growth) * 2)
        
        # Identify factors
        factors = []
        if demographic_multiplier > 1.1:
            factors.append("Favorable demographics")
        if competition_multiplier > 1.1:
            factors.append("Low competition")
        if indicators["market_maturity"] == "growing":
            factors.append("Growing market segment")
        
        logger.info(f"📊 Market trend analysis: {business_type} in {location} - {trend_direction} ({predicted_growth:.2%})")
        
        return MarketTrend(
            business_type=business_type,
            location=location,
            trend_direction=trend_direction,
            confidence=confidence,
            factors=factors,
            timeframe="12 months",
            predicted_growth=predicted_growth,
            risk_level=risk_level
        )
    
    def calculate_opportunity_score(self, business_type: str, location: str,
                                 demographics: Dict[str, Any],
                                 competition_data: Dict[str, Any]) -> OpportunityScore:
        """Calculate comprehensive opportunity score"""
        
        # Market saturation score (lower is better)
        competitor_count = competition_data.get("competitor_count", 0)
        market_saturation = min(1.0, competitor_count / 20.0)
        market_saturation_score = 1.0 - market_saturation
        
        # Competition level score
        avg_rating = competition_data.get("average_rating", 3.0)
        competition_score = max(0.0, min(1.0, (5.0 - avg_rating) / 2.0))
        
        # Demographic match score
        demographic_score = self._calculate_demographic_score(demographics, business_type)
        
        # Economic factors score
        economic_score = self._calculate_economic_score()
        
        # Seasonality score
        current_month = datetime.now().month
        seasonal_score = self._calculate_seasonal_score(business_type, current_month)
        
        # Growth potential score
        growth_score = self._calculate_growth_potential(business_type, location)
        
        # Calculate overall score
        weights = {
            "market_saturation": 0.25,
            "competition": 0.20,
            "demographics": 0.20,
            "economics": 0.15,
            "seasonality": 0.10,
            "growth": 0.10
        }
        
        overall_score = (
            market_saturation_score * weights["market_saturation"] +
            competition_score * weights["competition"] +
            demographic_score * weights["demographics"] +
            economic_score * weights["economics"] +
            seasonal_score * weights["seasonality"] +
            growth_score * weights["growth"]
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            market_saturation_score, competition_score, demographic_score,
            economic_score, seasonal_score, growth_score
        )
        
        logger.info(f"📊 Opportunity score calculated: {overall_score:.2f} for {business_type} in {location}")
        
        return OpportunityScore(
            overall_score=overall_score,
            market_saturation=market_saturation_score,
            competition_level=competition_score,
            demographic_match=demographic_score,
            economic_factors=economic_score,
            seasonality=seasonal_score,
            growth_potential=growth_score,
            recommendations=recommendations
        )
    
    def _calculate_demographic_multiplier(self, demographics: Dict[str, Any], 
                                        factors: List[str]) -> float:
        """Calculate demographic multiplier for market analysis"""
        multiplier = 1.0
        
        population = demographics.get("total_population", 1000000)
        income = demographics.get("median_household_income", 50000)
        
        # Population density factor
        if "population_density" in factors:
            if population > 2000000:  # Major metro
                multiplier *= 1.2
            elif population > 500000:  # Large city
                multiplier *= 1.1
            elif population < 100000:  # Small city
                multiplier *= 0.9
        
        # Income factor
        if "median_income" in factors:
            if income > 75000:
                multiplier *= 1.15
            elif income > 60000:
                multiplier *= 1.05
            elif income < 40000:
                multiplier *= 0.9
        
        return multiplier
    
    def _calculate_demographic_score(self, demographics: Dict[str, Any], 
                                   business_type: str) -> float:
        """Calculate demographic compatibility score"""
        score = 0.5  # Base score
        
        income = demographics.get("median_household_income", 50000)
        population = demographics.get("total_population", 1000000)
        
        # Business type specific scoring
        if business_type in ["coffee shop", "restaurant"]:
            if income > 60000:
                score += 0.3
            if population > 500000:
                score += 0.2
        
        elif business_type in ["gym", "pet care"]:
            if income > 70000:
                score += 0.4
            if population > 300000:
                score += 0.3
        
        elif business_type in ["retail", "bookstore"]:
            if income > 50000:
                score += 0.2
            if population > 200000:
                score += 0.3
        
        return min(1.0, score)
    
    def _calculate_economic_score(self) -> float:
        """Calculate economic factors score"""
        # Simulate economic indicators
        inflation = self.economic_factors["inflation_rate"]
        unemployment = self.economic_factors["unemployment_rate"]
        consumer_confidence = self.economic_factors["consumer_confidence"]
        
        # Calculate score based on economic health
        score = consumer_confidence
        if unemployment > 0.07:
            score -= 0.2
        if inflation > 0.05:
            score -= 0.1
        
        return max(0.0, min(1.0, score))
    
    def _calculate_seasonal_score(self, business_type: str, month: int) -> float:
        """Calculate seasonal score for current month"""
        seasonal_patterns = self.seasonal_patterns.get(business_type, {
            "january": 1.0, "february": 1.0, "march": 1.0, "april": 1.0,
            "may": 1.0, "june": 1.0, "july": 1.0, "august": 1.0,
            "september": 1.0, "october": 1.0, "november": 1.0, "december": 1.0
        })
        
        month_names = ["january", "february", "march", "april", "may", "june",
                      "july", "august", "september", "october", "november", "december"]
        
        current_month_name = month_names[month - 1]
        seasonal_multiplier = seasonal_patterns[current_month_name]
        
        # Convert to 0-1 score
        return min(1.0, seasonal_multiplier * 0.8)
    
    def _calculate_growth_potential(self, business_type: str, location: str) -> float:
        """Calculate growth potential score"""
        indicators = self.market_indicators.get(business_type, {})
        base_growth = indicators.get("growth_rate", 0.05)
        market_maturity = indicators.get("market_maturity", "stable")
        
        # Adjust for market maturity
        if market_maturity == "growing":
            growth_score = 0.8 + min(0.2, base_growth * 2)
        elif market_maturity == "stable":
            growth_score = 0.6 + min(0.2, base_growth * 2)
        else:  # declining
            growth_score = 0.3 + min(0.2, max(0, base_growth * 2))
        
        return min(1.0, growth_score)
    
    def _generate_recommendations(self, market_saturation: float, competition: float,
                                demographics: float, economics: float,
                                seasonality: float, growth: float) -> List[str]:
        """Generate recommendations based on scores"""
        recommendations = []
        
        if market_saturation > 0.8:
            recommendations.append("Market is underserved - excellent opportunity")
        elif market_saturation < 0.3:
            recommendations.append("High competition - consider differentiation strategy")
        
        if competition > 0.7:
            recommendations.append("Weak competition - capitalize on market gaps")
        elif competition < 0.3:
            recommendations.append("Strong competition - focus on unique value proposition")
        
        if demographics > 0.8:
            recommendations.append("Excellent demographic match for this business")
        elif demographics < 0.4:
            recommendations.append("Demographics may not be ideal - consider alternative locations")
        
        if economics > 0.8:
            recommendations.append("Favorable economic conditions for business growth")
        elif economics < 0.4:
            recommendations.append("Economic conditions are challenging - plan for resilience")
        
        if seasonality > 0.8:
            recommendations.append("Peak season timing - ideal for launch")
        elif seasonality < 0.4:
            recommendations.append("Off-season timing - consider delayed launch")
        
        if growth > 0.8:
            recommendations.append("High growth potential in this market segment")
        elif growth < 0.4:
            recommendations.append("Limited growth potential - consider market expansion")
        
        return recommendations[:5]  # Limit to top 5 recommendations

# Global instance
predictive_analytics = PredictiveAnalytics()
