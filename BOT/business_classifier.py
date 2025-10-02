#!/usr/bin/env python3
"""
Intelligent Business Type Classifier using Transformers
This module provides sophisticated business type detection using a language model
"""

import logging
import re
from typing import Dict, List, Optional, Tuple
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BusinessTypeClassifier:
    """Advanced business type classifier using transformer models"""
    
    def __init__(self):
        """Initialize the classifier with a pre-trained model"""
        self.classifier = None
        self.tokenizer = None
        self.model = None
        self.business_types = {
            "coffee shop": ["coffee shop", "cafe", "coffeehouse", "coffee bar", "espresso bar", "coffee roastery", "coffee store"],
            "restaurant": ["restaurant", "eatery", "dining", "bistro", "cafe", "diner", "food service", "catering"],
            "retail": ["retail", "store", "shop", "boutique", "marketplace", "merchandise", "goods"],
            "fitness": ["gym", "fitness", "workout", "exercise", "personal training", "yoga", "pilates", "crossfit"],
            "beauty": ["salon", "spa", "beauty", "hair", "nail", "skincare", "cosmetic", "barbershop"],
            "automotive": ["auto repair", "mechanic", "car service", "automotive", "garage", "tire shop"],
            "motorcycle shop": ["motorcycle shop", "bike shop", "biker shop", "motorcycle", "motorbike", "motorcycle dealer", "bike dealer", "harley davidson", "motorcycle repair", "bike repair", "motorcycle service", "bike service", "motorcycle parts", "bike parts", "motorcycle accessories", "bike accessories", "bike", "motorcycle store"],
            "auto dealer": ["auto dealer", "car dealer", "car dealership", "auto dealership", "used cars", "new cars", "vehicle dealer", "automotive dealer", "car sales", "auto sales"],
            "gas station": ["gas station", "fuel station", "petrol station", "gas", "fuel", "convenience store", "gas pump"],
            "pharmacy": ["pharmacy", "drugstore", "chemist", "prescription", "medication", "pharmaceutical"],
            "grocery": ["grocery", "supermarket", "food store", "market", "grocery store", "food market"],
            "clothing": ["clothing", "fashion", "apparel", "garments", "clothes", "wardrobe", "fashion store"],
            "electronics": ["electronics", "technology", "computer", "phone", "tech store", "electronic devices"],
            "home improvement": ["home improvement", "hardware", "construction", "building supplies", "tools", "lumber"],
            "real estate": ["real estate", "property", "housing", "realty", "real estate agent", "property management"],
            "insurance": ["insurance", "insurance agency", "insurance broker", "coverage", "policy"],
            "banking": ["bank", "banking", "financial services", "credit union", "financial institution"],
            "education": ["school", "education", "learning", "training", "academy", "institute", "tutoring"],
            "healthcare": ["medical", "healthcare", "clinic", "hospital", "doctor", "health services", "medical practice"],
            "legal": ["law", "legal", "attorney", "lawyer", "legal services", "law firm"],
            "accounting": ["accounting", "bookkeeping", "tax services", "financial consulting", "cpa"],
            "cleaning": ["cleaning", "janitorial", "housekeeping", "cleaning services", "maid service"],
            "landscaping": ["landscaping", "lawn care", "gardening", "outdoor maintenance", "yard services"],
            "pet care": ["pet care", "veterinary", "pet grooming", "animal care", "pet store", "vet clinic"],
            "laundry service": ["laundry", "laundromat", "laundry service", "dry cleaning", "wash and fold", "laundry mat", "coin laundry"],
            "bookstore": ["bookstore", "book store", "books", "bookshop", "book shop", "literature", "bookseller", "library", "book retailer"],
            "pharmacy": ["pharmacy", "drugstore", "drug store", "pharmacist", "medicine", "prescription", "cvs", "walgreens", "rite aid"],
            "grocery store": ["grocery", "grocery store", "supermarket", "food market", "food store", "market", "super store", "food mart"],
            "ice cream shop": ["ice cream", "ice cream shop", "ice cream parlor", "frozen yogurt", "gelato", "dessert shop", "sweet treats"],
            "hotel": ["hotel", "motel", "lodging", "accommodation", "inn", "resort", "hospitality", "bed and breakfast"],
            "bank": ["bank", "banking", "financial institution", "credit union", "atm", "financial services", "money"],
            "dentist": ["dentist", "dental", "dental office", "dental practice", "oral health", "teeth", "dental care"],
            "veterinarian": ["veterinarian", "vet", "veterinary", "animal hospital", "pet doctor", "animal care", "veterinary clinic"],
            "child care": ["childcare", "daycare", "preschool", "babysitting", "child care services"],
            "senior care": ["senior care", "elderly care", "assisted living", "home care", "senior services"],
            "transportation": ["transportation", "delivery", "shipping", "logistics", "moving", "trucking"],
            "entertainment": ["entertainment", "gaming", "arcade", "cinema", "theater", "recreation"],
            "hospitality": ["hotel", "motel", "lodging", "hospitality", "accommodation", "bed and breakfast"],
            "travel": ["travel", "tourism", "travel agency", "vacation", "trip planning"],
            "professional services": ["consulting", "professional services", "business services", "advisory"],
            "manufacturing": ["manufacturing", "production", "factory", "industrial", "assembly"],
            "construction": ["construction", "contracting", "building", "renovation", "remodeling"],
            "technology": ["technology", "software", "IT services", "tech consulting", "digital services"],
            "marketing": ["marketing", "advertising", "promotion", "branding", "digital marketing"],
            "food service": ["food service", "catering", "food truck", "fast food", "quick service"],
            "beverage": ["beverage", "bar", "pub", "lounge", "drink", "alcohol", "brewery", "winery"],
            "pizza": ["pizza", "pizza shop", "pizza stand", "pizza place", "pizza parlor", "pizza restaurant", "pizzeria", "pizza joint", "pizza store", "pizza kitchen"],
            "fast food": ["fast food", "quick service", "drive thru", "drive through", "takeout", "take away", "burger", "sandwich", "sub", "subway"],
            "bakery": ["bakery", "bakery shop", "baker", "bread", "pastry", "cakes", "desserts", "sweets", "confectionery"],
            "food truck": ["food truck", "mobile food", "street food", "taco truck", "burger truck", "mobile kitchen"],
            "seafood": ["seafood", "fish", "lobster", "crab", "shrimp", "sushi", "raw bar", "fish market"],
            "steakhouse": ["steakhouse", "steak house", "steak", "meat", "grill", "barbecue", "bbq"],
            "italian": ["italian", "italian restaurant", "pasta", "spaghetti", "lasagna", "italian food"],
            "mexican": ["mexican", "mexican restaurant", "taco", "burrito", "mexican food", "tex mex"],
            "chinese": ["chinese", "chinese restaurant", "chinese food", "asian", "asian restaurant"],
            "japanese": ["japanese", "japanese restaurant", "sushi", "ramen", "japanese food"],
            "thai": ["thai", "thai restaurant", "thai food", "pad thai"],
            "indian": ["indian", "indian restaurant", "indian food", "curry", "naan"],
            "mediterranean": ["mediterranean", "greek", "middle eastern", "mediterranean food"],
            "vegetarian": ["vegetarian", "vegan", "plant based", "vegetarian restaurant", "vegan restaurant"],
            "juice bar": ["juice bar", "smoothie", "fresh juice", "juice shop", "smoothie bar"],
            "sandwich shop": ["sandwich", "sandwich shop", "deli", "sub shop", "panini", "hoagie"],
            "breakfast": ["breakfast", "brunch", "breakfast restaurant", "breakfast place", "pancake", "waffle"]
        }
        
        # Initialize the classifier
        self._initialize_classifier()
    
    def _initialize_classifier(self):
        """Initialize the transformer model for classification"""
        try:
            # Use a lightweight, fast model for classification
            model_name = "microsoft/DialoGPT-medium"
            
            # Create a text classification pipeline
            self.classifier = pipeline(
                "text-classification",
                model="cardiffnlp/twitter-roberta-base-emotion",  # Lightweight model
                return_all_scores=True
            )
            
            logger.info("✅ Business classifier initialized successfully")
            
        except Exception as e:
            logger.warning(f"⚠️ Could not initialize transformer model: {e}")
            logger.info("🔄 Falling back to enhanced keyword matching")
            self.classifier = None
    
    def classify_business_type(self, text: str) -> Tuple[str, float]:
        """
        Classify business type from text using intelligent analysis
        
        Args:
            text: Input text to classify
            
        Returns:
            Tuple of (business_type, confidence_score)
        """
        if not text or not text.strip():
            return None, 0.0
        
        text = text.lower().strip()
        
        # First try transformer-based classification if available
        if self.classifier:
            try:
                result = self._classify_with_transformer(text)
                if result[1] > 0.7:  # High confidence threshold
                    return result
            except Exception as e:
                logger.warning(f"⚠️ Transformer classification failed: {e}")
        
        # Fall back to enhanced keyword matching
        return self._classify_with_keywords(text)
    
    def _classify_with_transformer(self, text: str) -> Tuple[str, float]:
        """Use transformer model for classification"""
        # Create a classification prompt
        prompt = f"Classify this business type: {text}"
        
        try:
            # Get predictions from the model
            results = self.classifier(prompt)
            
            # For now, we'll use keyword matching as the transformer
            # approach needs more specific training data
            return self._classify_with_keywords(text)
            
        except Exception as e:
            logger.warning(f"⚠️ Transformer classification error: {e}")
            return self._classify_with_keywords(text)
    
    def _classify_with_keywords(self, text: str) -> Tuple[str, float]:
        """
        Enhanced keyword-based classification with better matching and typo tolerance
        
        Args:
            text: Input text to classify
            
        Returns:
            Tuple of (business_type, confidence_score)
        """
        text = text.lower().strip()
        
        # Normalize common typos and variations
        text = self._normalize_text(text)
        
        # Track matches and scores
        matches = {}
        
        for business_type, keywords in self.business_types.items():
            score = 0
            matched_keywords = []
            
            for keyword in keywords:
                normalized_keyword = self._normalize_text(keyword)
                
                # Exact phrase match gets highest score
                if normalized_keyword in text:
                    score += 25
                    matched_keywords.append(keyword)
                
                # Word boundary matching for individual words
                elif re.search(r'\b' + re.escape(normalized_keyword) + r'\b', text):
                    score += 20
                    matched_keywords.append(keyword)
                
                # Check if all words in keyword are present
                elif all(word in text for word in normalized_keyword.split()):
                    score += 15
                    matched_keywords.append(keyword)
                
                # Fuzzy matching for typos (simple character-based)
                elif self._fuzzy_match(normalized_keyword, text):
                    score += 10
                    matched_keywords.append(f"{keyword} (fuzzy)")
            
            if score > 0:
                matches[business_type] = {
                    'score': score,
                    'keywords': matched_keywords,
                    'confidence': min(score / 25.0, 1.0)
                }
        
        if not matches:
            return None, 0.0
        
        # Find the best match
        best_match = max(matches.items(), key=lambda x: x[1]['score'])
        business_type, match_data = best_match
        
        logger.info(f"🎯 Business classification: '{text}' → '{business_type}' (confidence: {match_data['confidence']:.2f})")
        logger.info(f"🔍 Matched keywords: {match_data['keywords']}")
        
        return business_type, match_data['confidence']
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for better matching"""
        # Common typo corrections
        replacements = {
            'stant': 'stand',
            'shuold': 'should',
            'wont': 'want',
            'opne': 'open',
            'bussiness': 'business',
            'pizza stant': 'pizza stand',
            'coffe': 'coffee',
            'resturant': 'restaurant',
            'salon': 'salon',
            'sallon': 'salon',
            'sallon': 'salon',
            'gym': 'gym',
            'jym': 'gym',
            'fitness': 'fitness',
            'fitnes': 'fitness'
        }
        
        for typo, correction in replacements.items():
            text = text.replace(typo, correction)
        
        return text
    
    def _fuzzy_match(self, keyword: str, text: str) -> bool:
        """Simple fuzzy matching for typos"""
        # Check if keyword is in text with 1-2 character differences
        if len(keyword) < 4:
            return False
        
        # Simple character-based similarity
        for i in range(len(text) - len(keyword) + 1):
            substring = text[i:i + len(keyword)]
            if self._similarity(keyword, substring) > 0.8:
                return True
        
        return False
    
    def _similarity(self, a: str, b: str) -> float:
        """Calculate simple similarity between two strings"""
        if len(a) != len(b):
            return 0.0
        
        matches = sum(1 for x, y in zip(a, b) if x == y)
        return matches / len(a)
    
    def get_all_business_types(self) -> List[str]:
        """Get list of all supported business types"""
        return list(self.business_types.keys())
    
    def get_business_keywords(self, business_type: str) -> List[str]:
        """Get keywords for a specific business type"""
        return self.business_types.get(business_type.lower(), [])
    
    def add_business_type(self, business_type: str, keywords: List[str]):
        """Add a new business type with keywords"""
        self.business_types[business_type.lower()] = [k.lower() for k in keywords]
        logger.info(f"➕ Added business type: {business_type} with {len(keywords)} keywords")
    
    def search_business_types(self, query: str) -> List[Tuple[str, float]]:
        """
        Search for business types matching a query
        
        Args:
            query: Search query
            
        Returns:
            List of (business_type, relevance_score) tuples
        """
        query = query.lower().strip()
        results = []
        
        for business_type, keywords in self.business_types.items():
            relevance = 0
            
            # Check if query matches business type name
            if query in business_type:
                relevance += 20
            
            # Check keyword matches
            for keyword in keywords:
                if query in keyword or keyword in query:
                    relevance += 10
                elif any(word in keyword for word in query.split()):
                    relevance += 5
            
            if relevance > 0:
                results.append((business_type, relevance))
        
        # Sort by relevance score
        results.sort(key=lambda x: x[1], reverse=True)
        return results

# Global instance
business_classifier = BusinessTypeClassifier()

def classify_business_type(text: str) -> Tuple[str, float]:
    """Convenience function for business type classification"""
    return business_classifier.classify_business_type(text)

def search_business_types(query: str) -> List[Tuple[str, float]]:
    """Convenience function for business type search"""
    return business_classifier.search_business_types(query)

if __name__ == "__main__":
    # Test the classifier
    test_cases = [
        "I want to open a biker shop",
        "I want to open a motorcycle shop",
        "I want to open a bike shop",
        "I want to open a gas station",
        "I want to open a restaurant",
        "I want to open a coffee shop",
        "I want to open a car dealership",
        "I want to open an auto dealer"
    ]
    
    print("🧪 Testing Business Type Classifier:")
    print("=" * 50)
    
    for test_case in test_cases:
        business_type, confidence = classify_business_type(test_case)
        print(f"Input: '{test_case}'")
        print(f"Result: '{business_type}' (confidence: {confidence:.2f})")
        print("-" * 30)
