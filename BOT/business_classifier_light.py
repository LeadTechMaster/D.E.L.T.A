"""
🧠 Lightweight Business Type Classifier
Optimized for Render free tier deployment (no heavy AI models)
"""

import logging
from typing import Dict, List, Tuple, Optional
import re
from fuzzywuzzy import fuzz, process

logger = logging.getLogger(__name__)

class LightweightBusinessClassifier:
    """Lightweight business classifier using keyword matching and fuzzy logic"""
    
    def __init__(self):
        """Initialize the lightweight classifier"""
        self.business_types = {
            "coffee shop": [
                "coffee shop", "coffee", "cafe", "coffeehouse", "coffee bar", 
                "espresso bar", "coffee roastery", "coffee store", "coffee stand"
            ],
            "restaurant": [
                "restaurant", "bistro", "diner", "eatery", "food truck", 
                "pizza place", "pizza stand", "pizzeria", "burger", "fast food", 
                "sandwich", "bakery", "deli"
            ],
            "retail": [
                "store", "shop", "retail", "boutique", "market", "supermarket",
                "grocery", "convenience store", "bookstore", "book store", "bookshop"
            ],
            "automotive": [
                "auto repair", "car repair", "automotive", "mechanic", "garage",
                "auto shop", "car service", "oil change", "tire", "brake"
            ],
            "beauty": [
                "salon", "beauty", "hair", "nail", "spa", "barbershop", "barber",
                "nail salon", "hair salon", "beauty salon"
            ],
            "fitness": [
                "gym", "fitness", "workout", "exercise", "personal trainer",
                "yoga", "pilates", "crossfit", "boxing", "martial arts"
            ],
            "healthcare": [
                "clinic", "medical", "doctor", "dentist", "pharmacy", "health",
                "wellness", "therapy", "physical therapy", "mental health"
            ],
            "education": [
                "school", "education", "tutoring", "training", "academy",
                "learning", "classes", "courses", "university", "college"
            ],
            "services": [
                "service", "cleaning", "laundry", "laundromat", "laundry service",
                "dry cleaning", "repair", "maintenance", "consulting"
            ],
            "entertainment": [
                "entertainment", "movie", "theater", "cinema", "arcade",
                "gaming", "sports", "recreation", "club", "bar", "pub"
            ],
            "motorcycle shop": [
                "bike", "bicycle", "motorcycle", "motorbike", "scooter",
                "bike shop", "biker shop", "cycle", "motorcycle shop"
            ],
            "pizza": [
                "pizza", "pizza shop", "pizza stand", "pizza place", "pizza parlor", 
                "pizza restaurant", "pizzeria", "pizza joint", "pizza store", "pizza kitchen"
            ],
            "laundry service": [
                "laundry", "laundromat", "laundry service", "dry cleaning", 
                "wash and fold", "laundry mat", "coin laundry"
            ],
            "bookstore": [
                "bookstore", "book store", "books", "bookshop", "book shop", 
                "literature", "bookseller", "library", "book retailer"
            ],
            "gas station": [
                "gas station", "fuel station", "petrol station", "gas", "fuel", 
                "convenience store", "gas pump"
            ],
            "pharmacy": [
                "pharmacy", "drugstore", "drug store", "pharmacist", "medicine", 
                "prescription", "cvs", "walgreens", "rite aid"
            ],
            "hotel": [
                "hotel", "motel", "lodging", "accommodation", "inn", "resort", 
                "hospitality", "bed and breakfast"
            ],
            "bank": [
                "bank", "banking", "financial institution", "credit union", "atm", 
                "financial services", "money"
            ],
            "dentist": [
                "dentist", "dental", "dental office", "dental practice", 
                "oral health", "teeth", "dental care"
            ],
            "veterinarian": [
                "veterinarian", "vet", "veterinary", "animal hospital", 
                "pet doctor", "animal care", "veterinary clinic"
            ]
        }
        
        self.business_categories = {
            "food_service": ["restaurant", "coffee shop", "bakery", "pizza"],
            "retail": ["retail", "store", "bookstore", "boutique"],
            "automotive": ["automotive", "auto repair", "car repair"],
            "beauty_wellness": ["beauty", "salon", "spa", "fitness"],
            "healthcare": ["healthcare", "medical", "clinic"],
            "education": ["education", "school", "training"],
            "services": ["services", "laundry", "cleaning"],
            "entertainment": ["entertainment", "gaming", "sports"],
            "transportation": ["motorcycle shop", "automotive"]
        }
        
        logger.info("✅ Lightweight business classifier initialized successfully")
    
    def classify_business_type(self, text: str) -> Tuple[str, float]:
        """
        Classify business type using lightweight keyword matching
        
        Args:
            text: Input text to classify
            
        Returns:
            Tuple of (business_type, confidence_score)
        """
        if not text:
            return "unknown", 0.0
        
        text = text.lower().strip()
        logger.info(f"🎯 Lightweight business classification: '{text}'")
        
        # Direct keyword matching with scoring
        best_match = None
        best_score = 0.0
        
        for business_type, keywords in self.business_types.items():
            score = self._calculate_keyword_score(text, keywords)
            if score > best_score:
                best_score = score
                best_match = business_type
        
        # Fuzzy matching fallback for close matches
        if best_score < 0.7:
            fuzzy_result = self._fuzzy_match_business_type(text)
            if fuzzy_result and fuzzy_result[1] > best_score:
                best_match, best_score = fuzzy_result
        
        confidence = min(best_score, 1.0)
        result = best_match if best_match else "unknown"
        
        logger.info(f"🧠 Lightweight classifier result: '{result}' (confidence: {confidence:.2f})")
        return result, confidence
    
    def _calculate_keyword_score(self, text: str, keywords: List[str]) -> float:
        """Calculate score based on keyword matches with improved prioritization"""
        text_lower = text.lower()
        
        # Check for exact phrase matches first (highest priority)
        for keyword in keywords:
            if keyword.lower() in text_lower:
                # Exact phrase match gets highest score
                if keyword.lower() == text_lower.strip():
                    return 1.0
                # Phrase contains keyword
                return 0.9
        
        # Check for word boundary matches
        words = text_lower.split()
        matches = 0
        total_words = len(words)
        
        if total_words == 0:
            return 0.0
        
        for word in words:
            # Exact word match
            if word in [k.lower() for k in keywords]:
                matches += 1.0
            # Partial word match
            elif any(k.lower() in word or word in k.lower() for k in keywords):
                matches += 0.6
            # Fuzzy match
            else:
                for keyword in keywords:
                    if fuzz.ratio(word, keyword.lower()) > 85:
                        matches += 0.4
                        break
        
        return matches / total_words
    
    def _fuzzy_match_business_type(self, text: str) -> Optional[Tuple[str, float]]:
        """Use fuzzy matching to find business type"""
        all_keywords = []
        keyword_to_type = {}
        
        for business_type, keywords in self.business_types.items():
            for keyword in keywords:
                all_keywords.append(keyword)
                keyword_to_type[keyword] = business_type
        
        # Find best fuzzy match
        result = process.extractOne(text, all_keywords, scorer=fuzz.token_sort_ratio)
        if result and result[1] > 70:  # 70% similarity threshold
            keyword = result[0]
            business_type = keyword_to_type[keyword]
            confidence = result[1] / 100.0
            return business_type, confidence
        
        return None
    
    def search_business_types(self, query: str) -> List[str]:
        """Search for business types matching query"""
        query = query.lower().strip()
        matches = []
        
        for business_type, keywords in self.business_types.items():
            # Check if query matches business type name
            if fuzz.ratio(query, business_type) > 60:
                matches.append(business_type)
            # Check if query matches any keywords
            elif any(fuzz.ratio(query, keyword) > 60 for keyword in keywords):
                matches.append(business_type)
        
        # Remove duplicates and return
        return list(set(matches))
    
    def get_business_categories(self) -> Dict[str, List[str]]:
        """Get all business categories"""
        return self.business_categories.copy()
    
    def get_business_types(self) -> Dict[str, List[str]]:
        """Get all business types"""
        return self.business_types.copy()

# Global instance
lightweight_classifier = LightweightBusinessClassifier()

# Convenience functions
def classify_business_type(text: str) -> Tuple[str, float]:
    """Classify business type using lightweight classifier"""
    return lightweight_classifier.classify_business_type(text)

def search_business_types(query: str) -> List[str]:
    """Search business types using lightweight classifier"""
    return lightweight_classifier.search_business_types(query)
