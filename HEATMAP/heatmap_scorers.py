"""
D.E.L.T.A Heatmap Scoring Algorithms
Distinct, data-driven scoring formulas for each heatmap layer
"""

import math
from typing import Dict, Any, List

# Constants
EPS = 1e-9

def norm(x: float, a: float, b: float) -> float:
    """Normalize value x to range [0,1] between a and b"""
    return (x - a) / max(b - a, EPS)

def clamp01(x: float) -> float:
    """Clamp value to [0,1] range"""
    return max(0, min(1, x))

def logn(x: float) -> float:
    """Log10 with minimum value of 1"""
    return math.log10(max(x, 1))

class HeatmapScorers:
    """Scoring algorithms for different heatmap layers"""
    
    @staticmethod
    def competition_score(poi: Dict[str, Any]) -> float:
        """
        Business competition scoring - DRAMATIC DIFFERENCES:
        - High reviews & rating = strong competitor (10x amplification)
        - Exact category match = more relevant
        - Brand recognition = additional factor
        """
        rating = clamp01((poi.get('rating', 0) or 0) / 5)  # 0..1
        reviews = clamp01(logn(poi.get('user_ratings_total', 0) or 0) / 2)  # More aggressive scaling
        category_match = clamp01(poi.get('category_match', 0.4))  # 0..1
        is_brand = 1.0 if poi.get('is_brand', False) else 0.3  # Bigger brand penalty
        
        # DRAMATIC scoring - amplify differences by 10x
        base_score = (0.60 * reviews) + (0.25 * rating) + (0.10 * category_match) + (0.05 * is_brand)
        
        # Amplify high performers dramatically
        if base_score > 0.7:
            score = 0.7 + (base_score - 0.7) * 10  # 10x amplification for top performers
        else:
            score = base_score * 0.5  # Suppress low performers
        
        return clamp01(score)
    
    @staticmethod
    def review_power_score(poi: Dict[str, Any]) -> float:
        """
        Review power scoring - DRAMATIC DIFFERENCES:
        - Heavy reviewers = high marketing influence (10x amplification)
        - Rating quality moderates the influence
        """
        reviews = clamp01(logn(poi.get('user_ratings_total', 0) or 0) / 2.5)  # More aggressive
        rating = clamp01((poi.get('rating', 0) or 0) / 5)
        
        # DRAMATIC scoring - focus heavily on review volume
        base_score = 0.85 * reviews + 0.15 * rating
        
        # Amplify high review counts dramatically
        if reviews > 0.6:  # High review count
            score = 0.6 + (base_score - 0.6) * 8  # 8x amplification for high reviewers
        else:
            score = base_score * 0.3  # Suppress low reviewers
        
        return clamp01(score)
    
    @staticmethod
    def foot_traffic_score(cell: Dict[str, Any]) -> float:
        """
        Foot traffic proxy from nearby POI categories - DRAMATIC DIFFERENCES:
        - Transit hubs = high traffic (10x amplification)
        - Attractions = high traffic
        - Cafes = medium traffic
        - Malls = medium-high traffic
        """
        transit = cell.get('transit_count', 0)
        cafes = cell.get('cafe_count', 0)
        attractions = cell.get('attraction_count', 0)
        malls = cell.get('mall_count', 0)
        
        # Weighted aggregation with dramatic differences
        agg = 2.0 * transit + 0.8 * cafes + 1.5 * attractions + 1.0 * malls  # Amplified weights
        
        # DRAMATIC scoring - amplify high traffic areas
        base_score = clamp01(logn(agg) / 1.8)  # More aggressive scaling
        
        # Amplify high traffic areas dramatically
        if agg > 5:  # High traffic area
            score = 0.7 + (base_score - 0.7) * 4  # 4x amplification for high traffic
        else:
            score = base_score * 0.3  # Suppress low traffic areas
        
        return clamp01(score)
    
    @staticmethod
    def demographics_score(demographics: Dict[str, Any]) -> float:
        """
        Demographic density scoring - DRAMATIC DIFFERENCES:
        - Population density = primary factor (10x amplification)
        - Education level = secondary factor
        - Age distribution = tertiary factor
        """
        pop_density = demographics.get('population_density', 0)
        education_ratio = demographics.get('bachelor_plus_ratio', 0.1)
        median_age = demographics.get('median_age', 35)
        
        # Normalize population density (assume 0-5000 per km² range)
        pop_norm = clamp01(norm(pop_density, 0, 5000))
        
        # Education ratio (0.05 to 0.8 range)
        edu_norm = clamp01(norm(education_ratio, 0.05, 0.8))
        
        # Age factor (peak around 34, decline with distance)
        age_factor = clamp01(1 - abs(median_age - 34) / 30)
        
        # DRAMATIC scoring - amplify population density
        base_score = 0.70 * pop_norm + 0.20 * edu_norm + 0.10 * age_factor
        
        # Amplify high population areas dramatically
        if pop_norm > 0.7:  # High population density
            score = 0.7 + (base_score - 0.7) * 6  # 6x amplification for dense areas
        else:
            score = base_score * 0.4  # Suppress low density areas
        
        return clamp01(score)
    
    @staticmethod
    def income_wealth_score(demographics: Dict[str, Any]) -> float:
        """
        Income & wealth scoring - DRAMATIC DIFFERENCES:
        - Median income = primary factor (10x amplification)
        - Education level = secondary factor
        """
        median_income = demographics.get('median_household_income', 50000)
        education_ratio = demographics.get('bachelor_plus_ratio', 0.1)
        
        # Normalize income (assume $30k to $150k range)
        income_norm = clamp01(norm(median_income, 30000, 150000))
        
        # Education ratio
        edu_norm = clamp01(norm(education_ratio, 0.05, 0.8))
        
        # DRAMATIC scoring - amplify high income areas
        base_score = 0.85 * income_norm + 0.15 * edu_norm
        
        # Amplify wealthy areas dramatically
        if income_norm > 0.8:  # High income
            score = 0.8 + (base_score - 0.8) * 5  # 5x amplification for wealthy areas
        else:
            score = base_score * 0.3  # Suppress low income areas
        
        return clamp01(score)
    
    @staticmethod
    def opportunity_score(demographics: Dict[str, Any], competition_density: float) -> float:
        """
        Market opportunity scoring - DRAMATIC DIFFERENCES:
        - High demand (demographics + income) - high supply (competition) = opportunity (10x amplification)
        """
        # Calculate demand from demographics and income
        demo_score = HeatmapScorers.demographics_score(demographics)
        income_score = HeatmapScorers.income_wealth_score(demographics)
        
        demand = clamp01(0.60 * demo_score + 0.40 * income_score)
        supply = clamp01(competition_density)
        
        # DRAMATIC opportunity scoring
        base_opportunity = demand * (1 - 0.9 * supply)  # More aggressive competition penalty
        
        # Amplify high opportunity areas dramatically
        if base_opportunity > 0.6:  # High opportunity
            score = 0.6 + (base_opportunity - 0.6) * 7  # 7x amplification for high opportunity
        else:
            score = base_opportunity * 0.2  # Suppress low opportunity areas
        
        return clamp01(score)
    
    @staticmethod
    def calculate_category_match(business_type: str, poi_types: List[str]) -> float:
        """
        Calculate how well a POI matches the target business type
        """
        if not poi_types:
            return 0.3
        
        business_type_lower = business_type.lower()
        poi_types_lower = [t.lower() for t in poi_types]
        
        # Exact match
        if business_type_lower in poi_types_lower:
            return 1.0
        
        # Related categories
        related_categories = {
            'coffee shop': ['cafe', 'coffee', 'bakery', 'food'],
            'restaurant': ['food', 'meal_takeaway', 'meal_delivery', 'cafe'],
            'gym': ['gym', 'fitness', 'sports', 'health'],
            'retail': ['store', 'shopping_mall', 'clothing_store', 'electronics_store'],
            'gas station': ['gas_station', 'convenience_store'],
            'pharmacy': ['pharmacy', 'drugstore', 'health']
        }
        
        if business_type_lower in related_categories:
            for related in related_categories[business_type_lower]:
                if related in poi_types_lower:
                    return 0.6
        
        # Broad match
        broad_categories = {
            'coffee shop': ['establishment', 'point_of_interest'],
            'restaurant': ['establishment', 'point_of_interest'],
            'gym': ['establishment', 'point_of_interest'],
            'retail': ['establishment', 'point_of_interest']
        }
        
        if business_type_lower in broad_categories:
            for broad in broad_categories[business_type_lower]:
                if broad in poi_types_lower:
                    return 0.3
        
        return 0.1  # Minimal match
