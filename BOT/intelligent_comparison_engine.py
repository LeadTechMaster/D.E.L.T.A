"""
Intelligent Comparison & Recommendation Engine
Provides smart comparisons, recommendations, and decision support
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComparisonType(Enum):
    """Types of comparisons to perform"""
    BUSINESS_TYPES = "business_types"
    LOCATIONS = "locations"
    FRANCHISES = "franchises"
    COMPETITORS = "competitors"
    INVESTMENT_OPTIONS = "investment_options"

class RecommendationType(Enum):
    """Types of recommendations"""
    BUSINESS_TYPE = "business_type"
    LOCATION = "location"
    FRANCHISE = "franchise"
    INVESTMENT_STRATEGY = "investment_strategy"
    MARKET_ENTRY = "market_entry"

@dataclass
class ComparisonCriteria:
    """Criteria for comparison"""
    profitability: float
    competition_level: float
    investment_required: float
    growth_potential: float
    market_demand: float
    location_suitability: float
    franchise_support: float
    risk_level: float

@dataclass
class ComparisonResult:
    """Result of comparison"""
    item_name: str
    criteria_scores: ComparisonCriteria
    overall_score: float
    strengths: List[str]
    weaknesses: List[str]
    recommendation_reason: str
    best_for: List[str]

@dataclass
class SmartRecommendation:
    """Smart recommendation with reasoning"""
    recommendation_type: RecommendationType
    recommended_item: str
    confidence_score: float
    reasoning: str
    benefits: List[str]
    risks: List[str]
    next_steps: List[str]
    alternative_options: List[str]

class IntelligentComparisonEngine:
    """Advanced comparison and recommendation engine"""
    
    def __init__(self):
        """Initialize the comparison engine"""
        self.comparison_weights = self._build_comparison_weights()
        self.recommendation_frameworks = self._build_recommendation_frameworks()
        self.decision_matrices = self._build_decision_matrices()
        logger.info("🎯 Intelligent comparison engine initialized")
    
    def _build_comparison_weights(self) -> Dict[str, Dict[str, float]]:
        """Build weights for different comparison scenarios"""
        return {
            "conservative_investor": {
                "profitability": 0.25,
                "competition_level": 0.20,
                "investment_required": 0.15,
                "growth_potential": 0.15,
                "market_demand": 0.10,
                "location_suitability": 0.10,
                "franchise_support": 0.05,
                "risk_level": 0.30  # High weight for low risk
            },
            "aggressive_growth": {
                "profitability": 0.30,
                "competition_level": 0.10,
                "investment_required": 0.10,
                "growth_potential": 0.30,
                "market_demand": 0.15,
                "location_suitability": 0.05,
                "franchise_support": 0.05,
                "risk_level": 0.10  # Low weight for risk
            },
            "balanced_approach": {
                "profitability": 0.25,
                "competition_level": 0.15,
                "investment_required": 0.15,
                "growth_potential": 0.20,
                "market_demand": 0.15,
                "location_suitability": 0.10,
                "franchise_support": 0.10,
                "risk_level": 0.20
            },
            "first_time_entrepreneur": {
                "profitability": 0.20,
                "competition_level": 0.15,
                "investment_required": 0.20,
                "growth_potential": 0.15,
                "market_demand": 0.15,
                "location_suitability": 0.10,
                "franchise_support": 0.20,  # High weight for support
                "risk_level": 0.25  # High weight for low risk
            }
        }
    
    def _build_recommendation_frameworks(self) -> Dict[str, Dict[str, Any]]:
        """Build recommendation frameworks for different scenarios"""
        return {
            "high_competition_market": {
                "strategy": "differentiation",
                "recommendations": [
                    "Focus on niche markets",
                    "Consider unique positioning",
                    "Analyze competitor weaknesses",
                    "Look for underserved segments"
                ],
                "avoid": [
                    "Direct competition with established players",
                    "Commoditized business models",
                    "Overcrowded locations"
                ]
            },
            "emerging_market": {
                "strategy": "early_entry",
                "recommendations": [
                    "Establish market leadership",
                    "Build strong brand recognition",
                    "Focus on customer education",
                    "Plan for rapid expansion"
                ],
                "avoid": [
                    "Waiting too long to enter",
                    "Underestimating market education needs",
                    "Insufficient capital for growth"
                ]
            },
            "saturated_market": {
                "strategy": "optimization",
                "recommendations": [
                    "Focus on operational efficiency",
                    "Identify cost advantages",
                    "Build customer loyalty",
                    "Consider adjacent markets"
                ],
                "avoid": [
                    "Price wars",
                    "Undifferentiated offerings",
                    "Overexpansion"
                ]
            },
            "low_demand_market": {
                "strategy": "market_development",
                "recommendations": [
                    "Verify demand exists",
                    "Research market barriers",
                    "Consider market education",
                    "Look for demand drivers"
                ],
                "avoid": [
                    "Assuming low competition = opportunity",
                    "Insufficient market research",
                    "Ignoring demand indicators"
                ]
            }
        }
    
    def _build_decision_matrices(self) -> Dict[str, Dict[str, Any]]:
        """Build decision matrices for complex decisions"""
        return {
            "franchise_vs_independent": {
                "franchise_advantages": [
                    "Proven business model",
                    "Brand recognition",
                    "Training and support",
                    "Marketing assistance",
                    "Supply chain relationships"
                ],
                "franchise_disadvantages": [
                    "Higher initial investment",
                    "Ongoing royalties",
                    "Limited flexibility",
                    "Territory restrictions",
                    "Brand dependency"
                ],
                "independent_advantages": [
                    "Complete control",
                    "Lower ongoing costs",
                    "Flexibility in operations",
                    "No territory restrictions",
                    "Unique branding opportunities"
                ],
                "independent_disadvantages": [
                    "Higher risk",
                    "Need to build brand",
                    "No support system",
                    "Supply chain challenges",
                    "Marketing from scratch"
                ]
            },
            "location_selection": {
                "high_traffic_locations": {
                    "pros": ["High visibility", "Foot traffic", "Impulse purchases"],
                    "cons": ["High rent", "High competition", "Noise/parking issues"],
                    "best_for": ["Retail", "Food service", "Impulse-driven businesses"]
                },
                "residential_locations": {
                    "pros": ["Lower rent", "Local customer base", "Less competition"],
                    "cons": ["Limited foot traffic", "Seasonal variations", "Limited visibility"],
                    "best_for": ["Services", "Subscription businesses", "Local community businesses"]
                },
                "commercial_locations": {
                    "pros": ["Business customers", "Higher spending", "Consistent demand"],
                    "cons": ["Higher rent", "Limited hours", "Competition from corporate"],
                    "best_for": ["B2B services", "Professional services", "Corporate catering"]
                }
            }
        }
    
    def compare_business_types(self, business_types: List[str], 
                             market_data: Dict[str, Any],
                             user_profile: Dict[str, Any]) -> List[ComparisonResult]:
        """Compare multiple business types"""
        results = []
        
        for business_type in business_types:
            # Get market data for this business type
            business_data = market_data.get(business_type, {})
            
            # Calculate criteria scores
            criteria = self._calculate_business_criteria(business_type, business_data)
            
            # Calculate overall score
            overall_score = self._calculate_overall_score(criteria, user_profile)
            
            # Generate strengths and weaknesses
            strengths, weaknesses = self._analyze_business_strengths_weaknesses(business_type, business_data)
            
            # Generate recommendation reason
            recommendation_reason = self._generate_recommendation_reason(business_type, criteria, user_profile)
            
            # Determine best use cases
            best_for = self._determine_best_use_cases(business_type, criteria)
            
            result = ComparisonResult(
                item_name=business_type,
                criteria_scores=criteria,
                overall_score=overall_score,
                strengths=strengths,
                weaknesses=weaknesses,
                recommendation_reason=recommendation_reason,
                best_for=best_for
            )
            results.append(result)
        
        # Sort by overall score
        results.sort(key=lambda x: x.overall_score, reverse=True)
        
        logger.info(f"🎯 Compared {len(business_types)} business types")
        return results
    
    def compare_locations(self, locations: List[str], 
                         business_type: str,
                         market_data: Dict[str, Any]) -> List[ComparisonResult]:
        """Compare multiple locations for a business type"""
        results = []
        
        for location in locations:
            # Get market data for this location
            location_data = market_data.get(location, {})
            
            # Calculate criteria scores
            criteria = self._calculate_location_criteria(location, business_type, location_data)
            
            # Calculate overall score (using balanced approach for locations)
            overall_score = self._calculate_overall_score(criteria, {"investment_style": "balanced_approach"})
            
            # Generate strengths and weaknesses
            strengths, weaknesses = self._analyze_location_strengths_weaknesses(location, business_type, location_data)
            
            # Generate recommendation reason
            recommendation_reason = self._generate_location_recommendation_reason(location, business_type, criteria)
            
            # Determine best use cases
            best_for = self._determine_location_best_use_cases(location, business_type, criteria)
            
            result = ComparisonResult(
                item_name=location,
                criteria_scores=criteria,
                overall_score=overall_score,
                strengths=strengths,
                weaknesses=weaknesses,
                recommendation_reason=recommendation_reason,
                best_for=best_for
            )
            results.append(result)
        
        # Sort by overall score
        results.sort(key=lambda x: x.overall_score, reverse=True)
        
        logger.info(f"🎯 Compared {len(locations)} locations for {business_type}")
        return results
    
    def generate_smart_recommendation(self, analysis_data: Dict[str, Any],
                                    user_profile: Dict[str, Any],
                                    comparison_results: List[ComparisonResult]) -> SmartRecommendation:
        """Generate smart recommendation based on analysis and comparisons"""
        
        # Determine recommendation type
        recommendation_type = self._determine_recommendation_type(analysis_data)
        
        # Get best option from comparison results
        best_option = comparison_results[0] if comparison_results else None
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(analysis_data, best_option)
        
        # Generate reasoning
        reasoning = self._generate_recommendation_reasoning(analysis_data, best_option, user_profile)
        
        # Generate benefits and risks
        benefits, risks = self._analyze_recommendation_benefits_risks(best_option, analysis_data)
        
        # Generate next steps
        next_steps = self._generate_next_steps(best_option, analysis_data)
        
        # Generate alternative options
        alternative_options = [result.item_name for result in comparison_results[1:3]]  # Top 2 alternatives
        
        recommendation = SmartRecommendation(
            recommendation_type=recommendation_type,
            recommended_item=best_option.item_name if best_option else "No clear recommendation",
            confidence_score=confidence_score,
            reasoning=reasoning,
            benefits=benefits,
            risks=risks,
            next_steps=next_steps,
            alternative_options=alternative_options
        )
        
        logger.info(f"🎯 Generated recommendation: {recommendation.recommended_item} (confidence: {confidence_score:.2f})")
        return recommendation
    
    def _calculate_business_criteria(self, business_type: str, business_data: Dict[str, Any]) -> ComparisonCriteria:
        """Calculate criteria scores for a business type"""
        territory = business_data.get("territory_analysis", {})
        demographics = business_data.get("demographics", {})
        franchise_opps = business_data.get("franchise_opportunities", [])
        
        # Calculate profitability (based on market size and competition)
        competitor_count = territory.get("competitor_count", 0)
        population = demographics.get("total_population", 1000000)
        profitability = max(0.1, 1.0 - (competitor_count / (population / 10000)))
        
        # Calculate competition level
        competition_level = min(1.0, competitor_count / 10.0)
        
        # Calculate investment required (based on franchise data)
        investment_required = 0.5  # Default moderate
        if franchise_opps:
            # Estimate based on franchise opportunities
            investment_required = min(1.0, len(franchise_opps) / 5.0)
        
        # Calculate growth potential
        growth_potential = territory.get("opportunity_score", 0.5)
        
        # Calculate market demand
        market_demand = max(0.1, 1.0 - competition_level)
        
        # Calculate location suitability (business type dependent)
        location_suitability = self._calculate_location_suitability_score(business_type, demographics)
        
        # Calculate franchise support
        franchise_support = min(1.0, len(franchise_opps) / 3.0) if franchise_opps else 0.1
        
        # Calculate risk level (inverse of stability)
        risk_level = max(0.1, competition_level + (1.0 - growth_potential) * 0.5)
        
        return ComparisonCriteria(
            profitability=profitability,
            competition_level=competition_level,
            investment_required=investment_required,
            growth_potential=growth_potential,
            market_demand=market_demand,
            location_suitability=location_suitability,
            franchise_support=franchise_support,
            risk_level=risk_level
        )
    
    def _calculate_location_criteria(self, location: str, business_type: str, location_data: Dict[str, Any]) -> ComparisonCriteria:
        """Calculate criteria scores for a location"""
        territory = location_data.get("territory_analysis", {})
        demographics = location_data.get("demographics", {})
        franchise_opps = location_data.get("franchise_opportunities", [])
        
        # Similar to business criteria but location-focused
        competitor_count = territory.get("competitor_count", 0)
        population = demographics.get("total_population", 1000000)
        median_income = demographics.get("median_household_income", 50000)
        
        # Calculate profitability
        profitability = max(0.1, min(1.0, (median_income / 100000) * (1.0 - competitor_count / 20.0)))
        
        # Calculate competition level
        competition_level = min(1.0, competitor_count / 15.0)
        
        # Calculate investment required (based on location cost)
        investment_required = max(0.1, min(1.0, median_income / 75000))
        
        # Calculate growth potential
        growth_potential = territory.get("opportunity_score", 0.5)
        
        # Calculate market demand
        market_demand = max(0.1, population / 2000000)  # Normalize to 2M population
        
        # Calculate location suitability
        location_suitability = self._calculate_location_suitability_score(business_type, demographics)
        
        # Calculate franchise support
        franchise_support = min(1.0, len(franchise_opps) / 3.0) if franchise_opps else 0.1
        
        # Calculate risk level
        risk_level = max(0.1, competition_level + (1.0 - growth_potential) * 0.5)
        
        return ComparisonCriteria(
            profitability=profitability,
            competition_level=competition_level,
            investment_required=investment_required,
            growth_potential=growth_potential,
            market_demand=market_demand,
            location_suitability=location_suitability,
            franchise_support=franchise_support,
            risk_level=risk_level
        )
    
    def _calculate_location_suitability_score(self, business_type: str, demographics: Dict[str, Any]) -> float:
        """Calculate how suitable a location is for a specific business type"""
        population = demographics.get("total_population", 1000000)
        median_income = demographics.get("median_household_income", 50000)
        
        # Business type specific suitability
        suitability_scores = {
            "restaurant": min(1.0, population / 1000000) * min(1.0, median_income / 60000),
            "retail": min(1.0, population / 800000) * min(1.0, median_income / 55000),
            "fitness": min(1.0, population / 1200000) * min(1.0, median_income / 65000),
            "beauty": min(1.0, population / 1500000) * min(1.0, median_income / 55000),
            "automotive": min(1.0, population / 800000) * min(1.0, median_income / 50000),
            "coffee shop": min(1.0, population / 900000) * min(1.0, median_income / 55000),
            "pizza": min(1.0, population / 700000) * min(1.0, median_income / 45000)
        }
        
        return suitability_scores.get(business_type, 0.5)
    
    def _calculate_overall_score(self, criteria: ComparisonCriteria, user_profile: Dict[str, Any]) -> float:
        """Calculate overall score based on criteria and user profile"""
        investment_style = user_profile.get("investment_style", "balanced_approach")
        weights = self.comparison_weights.get(investment_style, self.comparison_weights["balanced_approach"])
        
        # Calculate weighted score
        overall_score = (
            criteria.profitability * weights["profitability"] +
            (1.0 - criteria.competition_level) * weights["competition_level"] +  # Invert competition (lower is better)
            (1.0 - criteria.investment_required) * weights["investment_required"] +  # Invert investment (lower is better)
            criteria.growth_potential * weights["growth_potential"] +
            criteria.market_demand * weights["market_demand"] +
            criteria.location_suitability * weights["location_suitability"] +
            criteria.franchise_support * weights["franchise_support"] +
            (1.0 - criteria.risk_level) * weights["risk_level"]  # Invert risk (lower is better)
        )
        
        return min(1.0, max(0.0, overall_score))
    
    def _analyze_business_strengths_weaknesses(self, business_type: str, business_data: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """Analyze strengths and weaknesses of a business type"""
        territory = business_data.get("territory_analysis", {})
        competitor_count = territory.get("competitor_count", 0)
        franchise_opps = business_data.get("franchise_opportunities", [])
        
        strengths = []
        weaknesses = []
        
        # Competition analysis
        if competitor_count < 3:
            strengths.append("Low competition - first mover advantage")
        elif competitor_count > 10:
            weaknesses.append("High competition - market saturation")
        else:
            strengths.append("Moderate competition - healthy market")
        
        # Franchise opportunities
        if franchise_opps and len(franchise_opps) > 3:
            strengths.append("Multiple franchise opportunities available")
        elif not franchise_opps:
            weaknesses.append("Limited franchise support options")
        
        # Market size
        demographics = business_data.get("demographics", {})
        population = demographics.get("total_population", 1000000)
        if population > 1500000:
            strengths.append("Large market size")
        elif population < 500000:
            weaknesses.append("Small market size")
        
        return strengths, weaknesses
    
    def _analyze_location_strengths_weaknesses(self, location: str, business_type: str, location_data: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """Analyze strengths and weaknesses of a location"""
        territory = location_data.get("territory_analysis", {})
        demographics = location_data.get("demographics", {})
        
        strengths = []
        weaknesses = []
        
        # Demographics analysis
        median_income = demographics.get("median_household_income", 50000)
        if median_income > 70000:
            strengths.append("High median income - good spending power")
        elif median_income < 40000:
            weaknesses.append("Lower median income - limited spending power")
        
        # Population analysis
        population = demographics.get("total_population", 1000000)
        if population > 1000000:
            strengths.append("Large population base")
        elif population < 300000:
            weaknesses.append("Small population base")
        
        # Competition analysis
        competitor_count = territory.get("competitor_count", 0)
        if competitor_count < 2:
            strengths.append("Low competition in area")
        elif competitor_count > 8:
            weaknesses.append("High competition in area")
        
        return strengths, weaknesses
    
    def _generate_recommendation_reason(self, item_name: str, criteria: ComparisonCriteria, user_profile: Dict[str, Any]) -> str:
        """Generate reasoning for recommendation"""
        investment_style = user_profile.get("investment_style", "balanced_approach")
        
        if investment_style == "conservative_investor":
            if criteria.risk_level < 0.3:
                return f"{item_name} offers low risk with stable returns, perfect for conservative investors"
            else:
                return f"{item_name} may be too risky for conservative investment approach"
        
        elif investment_style == "aggressive_growth":
            if criteria.growth_potential > 0.7:
                return f"{item_name} shows high growth potential, ideal for aggressive growth strategy"
            else:
                return f"{item_name} has limited growth potential for aggressive investors"
        
        else:  # balanced_approach
            # Calculate a simple score for balanced approach
            balanced_score = (criteria.profitability + criteria.growth_potential + criteria.market_demand) / 3
            if balanced_score > 0.6:
                return f"{item_name} offers balanced risk-reward profile with good market opportunity"
            else:
                return f"{item_name} may not offer optimal balance for most investors"
    
    def _generate_location_recommendation_reason(self, location: str, business_type: str, criteria: ComparisonCriteria) -> str:
        """Generate reasoning for location recommendation"""
        if criteria.location_suitability > 0.7:
            return f"{location} is highly suitable for {business_type} with strong demographic match"
        elif criteria.competition_level < 0.3:
            return f"{location} offers low competition for {business_type} with good opportunity"
        elif criteria.market_demand > 0.7:
            return f"{location} shows strong market demand for {business_type}"
        else:
            return f"{location} may present challenges for {business_type} success"
    
    def _determine_best_use_cases(self, business_type: str, criteria: ComparisonCriteria) -> List[str]:
        """Determine best use cases for a business type"""
        use_cases = []
        
        if criteria.risk_level < 0.3:
            use_cases.append("Conservative investors")
        if criteria.growth_potential > 0.7:
            use_cases.append("Growth-focused entrepreneurs")
        if criteria.franchise_support > 0.6:
            use_cases.append("First-time business owners")
        if criteria.competition_level < 0.4:
            use_cases.append("Market entry strategies")
        if criteria.profitability > 0.7:
            use_cases.append("Profit-focused investors")
        
        return use_cases if use_cases else ["General business opportunity"]
    
    def _determine_location_best_use_cases(self, location: str, business_type: str, criteria: ComparisonCriteria) -> List[str]:
        """Determine best use cases for a location"""
        use_cases = []
        
        if criteria.market_demand > 0.7:
            use_cases.append("High-demand businesses")
        if criteria.competition_level < 0.3:
            use_cases.append("Market entry opportunities")
        if criteria.profitability > 0.7:
            use_cases.append("Premium service businesses")
        if criteria.location_suitability > 0.7:
            use_cases.append(f"Optimal for {business_type}")
        
        return use_cases if use_cases else [f"General {business_type} location"]
    
    def _determine_recommendation_type(self, analysis_data: Dict[str, Any]) -> RecommendationType:
        """Determine the type of recommendation to make"""
        if "business_type" in analysis_data and "location" in analysis_data:
            return RecommendationType.MARKET_ENTRY
        elif "franchise_opportunities" in analysis_data:
            return RecommendationType.FRANCHISE
        else:
            return RecommendationType.BUSINESS_TYPE
    
    def _calculate_confidence_score(self, analysis_data: Dict[str, Any], best_option: Optional[ComparisonResult]) -> float:
        """Calculate confidence score for recommendation"""
        if not best_option:
            return 0.0
        
        # Base confidence on overall score
        confidence = best_option.overall_score
        
        # Adjust based on data quality
        territory = analysis_data.get("territory_analysis", {})
        franchise_opps = analysis_data.get("franchise_opportunities", [])
        
        # Increase confidence if we have good data
        if territory.get("competitor_count", 0) > 0:
            confidence += 0.1
        if franchise_opps:
            confidence += 0.1
        if analysis_data.get("demographics", {}).get("total_population", 0) > 0:
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def _generate_recommendation_reasoning(self, analysis_data: Dict[str, Any], best_option: Optional[ComparisonResult], user_profile: Dict[str, Any]) -> str:
        """Generate detailed reasoning for recommendation"""
        if not best_option:
            return "Insufficient data to make a strong recommendation"
        
        reasoning_parts = [
            f"Based on comprehensive analysis, {best_option.item_name} scores {best_option.overall_score:.1f}/1.0 overall",
            f"Key strengths include: {', '.join(best_option.strengths[:2])}",
            f"Market conditions show {best_option.criteria_scores.competition_level:.1f} competition level",
            f"Growth potential is {best_option.criteria_scores.growth_potential:.1f}/1.0"
        ]
        
        return ". ".join(reasoning_parts) + "."
    
    def _analyze_recommendation_benefits_risks(self, best_option: Optional[ComparisonResult], analysis_data: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """Analyze benefits and risks of recommendation"""
        if not best_option:
            return [], []
        
        benefits = best_option.strengths.copy()
        risks = best_option.weaknesses.copy()
        
        # Add analysis-specific benefits/risks
        territory = analysis_data.get("territory_analysis", {})
        if territory.get("market_saturation") == "high":
            risks.append("Market saturation may limit growth")
        elif territory.get("market_saturation") == "low":
            benefits.append("Low market saturation presents opportunity")
        
        return benefits, risks
    
    def _generate_next_steps(self, best_option: Optional[ComparisonResult], analysis_data: Dict[str, Any]) -> List[str]:
        """Generate next steps for the recommendation"""
        if not best_option:
            return ["Gather more market data", "Define investment criteria", "Research alternative options"]
        
        next_steps = [
            f"Conduct detailed market research for {best_option.item_name}",
            "Develop comprehensive business plan",
            "Secure financing and investment capital"
        ]
        
        # Add specific next steps based on analysis
        territory = analysis_data.get("territory_analysis", {})
        if territory.get("competitor_count", 0) > 5:
            next_steps.append("Develop competitive differentiation strategy")
        
        franchise_opps = analysis_data.get("franchise_opportunities", [])
        if franchise_opps:
            next_steps.append("Research franchise opportunities and requirements")
        
        return next_steps

# Global instance
intelligent_comparison_engine = IntelligentComparisonEngine()
