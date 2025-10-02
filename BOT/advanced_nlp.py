"""
Advanced Natural Language Processing System
Enhanced NLP with sentiment analysis, entity recognition, and context understanding
"""

import re
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import math

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentimentType(Enum):
    """Sentiment types"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    UNCERTAIN = "uncertain"
    EXCITED = "excited"
    CONCERNED = "concerned"

class UrgencyLevel(Enum):
    """Urgency levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

@dataclass
class SentimentAnalysis:
    """Sentiment analysis result"""
    sentiment: SentimentType
    confidence: float
    intensity: float
    emotional_indicators: List[str]
    urgency_level: UrgencyLevel

@dataclass
class EntityRecognition:
    """Entity recognition result"""
    entities: Dict[str, List[str]]
    confidence_scores: Dict[str, float]
    entity_relationships: Dict[str, List[str]]

@dataclass
class ContextAnalysis:
    """Advanced context analysis result"""
    primary_intent: str
    secondary_intents: List[str]
    sentiment: SentimentAnalysis
    entities: EntityRecognition
    complexity_score: float
    clarity_score: float
    action_required: bool
    follow_up_needed: bool

class AdvancedNLP:
    """Advanced Natural Language Processing system"""
    
    def __init__(self):
        """Initialize advanced NLP system"""
        self.sentiment_lexicon = self._build_sentiment_lexicon()
        self.entity_patterns = self._build_entity_patterns()
        self.intent_patterns = self._build_intent_patterns()
        self.urgency_indicators = self._build_urgency_indicators()
        self.emotional_indicators = self._build_emotional_indicators()
        logger.info("🧠 Advanced NLP system initialized")
    
    def _build_sentiment_lexicon(self) -> Dict[str, Dict[str, Any]]:
        """Build comprehensive sentiment lexicon"""
        return {
            "positive": {
                "words": {
                    "excellent": 0.9, "amazing": 0.9, "perfect": 0.95, "great": 0.8,
                    "fantastic": 0.9, "wonderful": 0.8, "awesome": 0.85, "brilliant": 0.9,
                    "outstanding": 0.9, "superb": 0.9, "terrific": 0.8, "marvelous": 0.85,
                    "love": 0.9, "adore": 0.9, "enjoy": 0.7, "like": 0.6, "prefer": 0.6,
                    "success": 0.8, "successful": 0.8, "prosper": 0.8, "thrive": 0.9,
                    "promising": 0.7, "exciting": 0.8, "interesting": 0.6, "appealing": 0.7,
                    "profitable": 0.8, "lucrative": 0.9, "profitable": 0.8, "beneficial": 0.7,
                    "ideal": 0.8, "perfect": 0.95, "optimal": 0.8, "suitable": 0.6,
                    "confident": 0.7, "certain": 0.8, "sure": 0.6, "positive": 0.7,
                    "hopeful": 0.6, "optimistic": 0.7, "enthusiastic": 0.8
                },
                "phrases": {
                    "can't wait": 0.9, "looking forward": 0.8, "excited about": 0.9,
                    "really want": 0.8, "definitely interested": 0.9, "sounds great": 0.8,
                    "perfect for me": 0.9, "exactly what I need": 0.9, "love the idea": 0.9,
                    "great opportunity": 0.8, "excellent choice": 0.8, "smart move": 0.8,
                    "highly recommend": 0.8, "strongly suggest": 0.8, "best option": 0.8
                }
            },
            "negative": {
                "words": {
                    "terrible": 0.9, "awful": 0.9, "horrible": 0.9, "bad": 0.7,
                    "worst": 0.9, "disappointing": 0.8, "frustrating": 0.8, "annoying": 0.7,
                    "hate": 0.9, "dislike": 0.7, "detest": 0.9, "loathe": 0.9,
                    "failure": 0.8, "failed": 0.8, "unsuccessful": 0.8, "losing": 0.7,
                    "risky": 0.7, "dangerous": 0.8, "unsafe": 0.8, "hazardous": 0.8,
                    "expensive": 0.6, "costly": 0.7, "overpriced": 0.8, "waste": 0.7,
                    "useless": 0.8, "pointless": 0.8, "worthless": 0.9, "meaningless": 0.8,
                    "confused": 0.6, "lost": 0.7, "uncertain": 0.6, "doubtful": 0.7,
                    "worried": 0.7, "concerned": 0.6, "anxious": 0.7, "stressed": 0.7,
                    "disappointed": 0.8, "frustrated": 0.8, "angry": 0.8, "upset": 0.7
                },
                "phrases": {
                    "not sure": 0.7, "don't know": 0.7, "can't decide": 0.7,
                    "too expensive": 0.8, "too risky": 0.8, "not interested": 0.8,
                    "sounds bad": 0.8, "worried about": 0.7, "concerned about": 0.7,
                    "don't like": 0.7, "not good": 0.7, "not working": 0.7,
                    "waste of time": 0.8, "not worth it": 0.8, "avoid": 0.8
                }
            },
            "uncertainty": {
                "words": {
                    "maybe": 0.8, "perhaps": 0.7, "possibly": 0.7, "might": 0.6,
                    "could": 0.6, "may": 0.6, "potentially": 0.7, "considering": 0.6,
                    "thinking": 0.6, "wondering": 0.7, "curious": 0.6, "interested": 0.5,
                    "unsure": 0.8, "uncertain": 0.8, "doubtful": 0.7, "hesitant": 0.7,
                    "confused": 0.7, "puzzled": 0.7, "bewildered": 0.8, "perplexed": 0.8,
                    "undecided": 0.8, "indecisive": 0.8, "ambivalent": 0.8
                },
                "phrases": {
                    "not sure if": 0.8, "don't know if": 0.8, "wondering if": 0.7,
                    "thinking about": 0.6, "considering": 0.6, "exploring": 0.6,
                    "looking into": 0.6, "researching": 0.5, "investigating": 0.5,
                    "on the fence": 0.8, "torn between": 0.7, "can't decide": 0.8
                }
            }
        }
    
    def _build_entity_patterns(self) -> Dict[str, List[str]]:
        """Build entity recognition patterns"""
        return {
            "business_types": [
                r"\b(coffee shop|café|cafe)\b",
                r"\b(restaurant|dining|eatery)\b",
                r"\b(retail store|shop|store)\b",
                r"\b(gym|fitness|workout)\b",
                r"\b(bookstore|book shop)\b",
                r"\b(laundry|laundromat)\b",
                r"\b(pet care|pet grooming|veterinary)\b",
                r"\b(pharmacy|drugstore)\b",
                r"\b(gas station|fuel station)\b",
                r"\b(beauty salon|hair salon)\b",
                r"\b(nail salon|nail shop)\b",
                r"\b(auto repair|car repair|mechanic)\b",
                r"\b(pizza place|pizzeria)\b",
                r"\b(fast food|quick service)\b",
                r"\b(fine dining|upscale restaurant)\b"
            ],
            "locations": [
                r"\b(miami|seattle|denver|chicago|atlanta|dallas|austin|las vegas|phoenix|portland)\b",
                r"\b(new york|los angeles|san francisco|boston|washington|houston|philadelphia|detroit|phoenix|san antonio)\b",
                r"\b(california|texas|florida|new york|pennsylvania|illinois|ohio|georgia|north carolina|michigan)\b",
                r"\b(kansas|nevada|colorado|washington|oregon|arizona|utah|idaho|montana|wyoming)\b",
                r"\b(downtown|uptown|midtown|suburbs|mall|plaza|strip|boulevard|avenue|street)\b"
            ],
            "financial_terms": [
                r"\b(\$[\d,]+|\d+ thousand|\d+ million|\d+k|\d+m)\b",
                r"\b(budget|cost|price|investment|capital|funding|loan|financing)\b",
                r"\b(profit|revenue|income|earnings|returns|roi)\b",
                r"\b(expensive|cheap|affordable|budget-friendly|cost-effective)\b",
                r"\b(break-even|profitable|lucrative|viable|feasible)\b"
            ],
            "time_references": [
                r"\b(asap|immediately|urgently|soon|quickly|fast|rush)\b",
                r"\b(this week|next week|this month|next month|this year|next year)\b",
                r"\b(january|february|march|april|may|june|july|august|september|october|november|december)\b",
                r"\b(spring|summer|fall|winter|autumn)\b",
                r"\b(peak season|off season|holiday season|back to school)\b"
            ],
            "business_actions": [
                r"\b(open|start|launch|begin|establish|create|build|develop|operate|run|manage)\b",
                r"\b(expand|grow|scale|increase|boost|improve|enhance|optimize)\b",
                r"\b(buy|purchase|acquire|invest|fund|finance|support|back)\b",
                r"\b(analyze|research|study|investigate|explore|examine|evaluate|assess)\b",
                r"\b(compare|contrast|choose|select|decide|pick|opt|prefer)\b"
            ]
        }
    
    def _build_intent_patterns(self) -> Dict[str, List[str]]:
        """Build intent recognition patterns"""
        return {
            "business_inquiry": [
                r"want to open", r"looking to start", r"planning to launch",
                r"interested in opening", r"considering starting", r"thinking about opening",
                r"need help with", r"want advice on", r"seeking guidance"
            ],
            "location_question": [
                r"where should", r"where can", r"which location", r"best place to",
                r"where to open", r"where to start", r"location for", r"place for"
            ],
            "business_type_question": [
                r"what type of business", r"what kind of business", r"which business",
                r"business type", r"what should i open", r"what business", r"business ideas"
            ],
            "franchise_inquiry": [
                r"franchise", r"franchise opportunities", r"franchise options",
                r"franchise costs", r"franchise investment", r"buy a franchise"
            ],
            "financial_question": [
                r"how much", r"cost", r"investment", r"budget", r"funding",
                r"expensive", r"affordable", r"financial", r"money"
            ],
            "competition_question": [
                r"competition", r"competitors", r"how many", r"market saturation",
                r"existing businesses", r"competitive", r"market analysis"
            ],
            "urgency_question": [
                r"asap", r"urgent", r"immediately", r"quickly", r"soon",
                r"rush", r"fast", r"time sensitive", r"deadline"
            ]
        }
    
    def _build_urgency_indicators(self) -> Dict[str, float]:
        """Build urgency level indicators"""
        return {
            "urgent": {
                "words": ["asap", "urgent", "immediately", "emergency", "critical", "rush", "deadline"],
                "phrases": ["right now", "as soon as possible", "time sensitive", "need it now"],
                "score": 0.9
            },
            "high": {
                "words": ["soon", "quickly", "fast", "priority", "important", "hurry"],
                "phrases": ["this week", "need help", "can't wait", "time is running"],
                "score": 0.7
            },
            "medium": {
                "words": ["eventually", "sometime", "when possible", "convenient"],
                "phrases": ["when you can", "no rush", "take your time"],
                "score": 0.5
            },
            "low": {
                "words": ["eventually", "someday", "maybe", "perhaps"],
                "phrases": ["not urgent", "whenever", "no hurry"],
                "score": 0.2
            }
        }
    
    def _build_emotional_indicators(self) -> Dict[str, List[str]]:
        """Build emotional indicators"""
        return {
            "excited": ["!", "excited", "can't wait", "looking forward", "amazing", "fantastic"],
            "concerned": ["worried", "concerned", "anxious", "stressed", "nervous"],
            "confident": ["confident", "sure", "certain", "definitely", "absolutely"],
            "confused": ["confused", "lost", "don't understand", "puzzled", "bewildered"],
            "frustrated": ["frustrated", "annoyed", "irritated", "upset", "angry"],
            "hopeful": ["hopeful", "optimistic", "positive", "encouraged", "motivated"]
        }
    
    def analyze_sentiment(self, text: str) -> SentimentAnalysis:
        """Analyze sentiment of text"""
        text_lower = text.lower()
        sentiment_scores = {"positive": 0, "negative": 0, "uncertainty": 0}
        emotional_indicators = []
        
        # Analyze word sentiment
        for sentiment_type, data in self.sentiment_lexicon.items():
            for word, score in data["words"].items():
                if word in text_lower:
                    sentiment_scores[sentiment_type] += score
                    if sentiment_type in ["positive", "negative"]:
                        emotional_indicators.append(word)
            
            for phrase, score in data.get("phrases", {}).items():
                if phrase in text_lower:
                    sentiment_scores[sentiment_type] += score
        
        # Determine primary sentiment
        max_sentiment = max(sentiment_scores.items(), key=lambda x: x[1])
        sentiment_type = max_sentiment[0]
        confidence = min(1.0, max_sentiment[1] / 3.0)  # Normalize confidence
        
        # Map to sentiment enum
        if sentiment_type == "positive":
            sentiment_enum = SentimentType.POSITIVE
        elif sentiment_type == "negative":
            sentiment_enum = SentimentType.NEGATIVE
        else:
            sentiment_enum = SentimentType.UNCERTAIN
        
        # Calculate intensity
        intensity = min(1.0, max_sentiment[1] / 2.0)
        
        # Determine urgency level
        urgency_level = self._determine_urgency_level(text_lower)
        
        logger.info(f"🧠 Sentiment analysis: {sentiment_enum.value} (confidence: {confidence:.2f})")
        
        return SentimentAnalysis(
            sentiment=sentiment_enum,
            confidence=confidence,
            intensity=intensity,
            emotional_indicators=emotional_indicators[:5],  # Top 5 indicators
            urgency_level=urgency_level
        )
    
    def recognize_entities(self, text: str) -> EntityRecognition:
        """Recognize entities in text"""
        entities = {}
        confidence_scores = {}
        entity_relationships = {}
        
        for entity_type, patterns in self.entity_patterns.items():
            found_entities = []
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                found_entities.extend(matches)
            
            if found_entities:
                entities[entity_type] = list(set(found_entities))
                confidence_scores[entity_type] = min(1.0, len(found_entities) / 5.0)
        
        # Find entity relationships
        for entity_type, entity_list in entities.items():
            relationships = []
            for entity in entity_list:
                # Look for entities that appear near each other
                for other_type, other_entities in entities.items():
                    if other_type != entity_type:
                        for other_entity in other_entities:
                            if abs(text.lower().find(entity.lower()) - text.lower().find(other_entity.lower())) < 50:
                                relationships.append(f"{entity_type}:{other_entity}")
            
            entity_relationships[entity_type] = relationships[:3]  # Top 3 relationships
        
        logger.info(f"🧠 Entity recognition: {len(entities)} entity types found")
        
        return EntityRecognition(
            entities=entities,
            confidence_scores=confidence_scores,
            entity_relationships=entity_relationships
        )
    
    def analyze_context(self, text: str) -> ContextAnalysis:
        """Perform comprehensive context analysis"""
        # Analyze sentiment
        sentiment = self.analyze_sentiment(text)
        
        # Recognize entities
        entities = self.recognize_entities(text)
        
        # Determine primary intent
        primary_intent = self._determine_primary_intent(text)
        
        # Find secondary intents
        secondary_intents = self._find_secondary_intents(text)
        
        # Calculate complexity and clarity scores
        complexity_score = self._calculate_complexity_score(text, entities)
        clarity_score = self._calculate_clarity_score(text, sentiment)
        
        # Determine if action is required
        action_required = self._is_action_required(primary_intent, sentiment, entities)
        
        # Determine if follow-up is needed
        follow_up_needed = self._is_follow_up_needed(entities, sentiment)
        
        logger.info(f"🧠 Context analysis: {primary_intent} (complexity: {complexity_score:.2f}, clarity: {clarity_score:.2f})")
        
        return ContextAnalysis(
            primary_intent=primary_intent,
            secondary_intents=secondary_intents,
            sentiment=sentiment,
            entities=entities,
            complexity_score=complexity_score,
            clarity_score=clarity_score,
            action_required=action_required,
            follow_up_needed=follow_up_needed
        )
    
    def _determine_urgency_level(self, text: str) -> UrgencyLevel:
        """Determine urgency level from text"""
        urgency_scores = {}
        
        for level, data in self.urgency_indicators.items():
            score = 0
            for word in data["words"]:
                if word in text:
                    score += 1
            for phrase in data["phrases"]:
                if phrase in text:
                    score += 2
            
            urgency_scores[level] = score
        
        max_urgency = max(urgency_scores.items(), key=lambda x: x[1])
        
        if max_urgency[1] > 0:
            return UrgencyLevel(max_urgency[0])
        
        return UrgencyLevel.MEDIUM  # Default urgency
    
    def _determine_primary_intent(self, text: str) -> str:
        """Determine primary intent from text"""
        intent_scores = {}
        
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    score += 1
            intent_scores[intent] = score
        
        if intent_scores:
            return max(intent_scores.items(), key=lambda x: x[1])[0]
        
        return "general_question"
    
    def _find_secondary_intents(self, text: str) -> List[str]:
        """Find secondary intents in text"""
        secondary_intents = []
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    if intent not in secondary_intents:
                        secondary_intents.append(intent)
        
        return secondary_intents[:2]  # Top 2 secondary intents
    
    def _calculate_complexity_score(self, text: str, entities: EntityRecognition) -> float:
        """Calculate text complexity score"""
        complexity = 0.0
        
        # Sentence length complexity
        sentences = re.split(r'[.!?]+', text)
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        complexity += min(0.3, avg_sentence_length / 20.0)
        
        # Entity complexity
        entity_count = sum(len(entities) for entities in entities.entities.values())
        complexity += min(0.3, entity_count / 10.0)
        
        # Word complexity
        complex_words = ["analyze", "evaluate", "comprehensive", "investigation", "assessment"]
        complex_word_count = sum(1 for word in complex_words if word in text.lower())
        complexity += min(0.2, complex_word_count / 5.0)
        
        # Question complexity
        question_count = text.count('?')
        complexity += min(0.2, question_count / 3.0)
        
        return min(1.0, complexity)
    
    def _calculate_clarity_score(self, text: str, sentiment: SentimentAnalysis) -> float:
        """Calculate text clarity score"""
        clarity = 1.0
        
        # Uncertainty reduces clarity
        if sentiment.sentiment == SentimentType.UNCERTAIN:
            clarity -= 0.3
        
        # Negative sentiment can reduce clarity
        if sentiment.sentiment == SentimentType.NEGATIVE:
            clarity -= 0.2
        
        # Vague words reduce clarity
        vague_words = ["thing", "stuff", "something", "anything", "everything", "nothing"]
        vague_count = sum(1 for word in vague_words if word in text.lower())
        clarity -= min(0.3, vague_count / 5.0)
        
        # Short responses are clearer
        word_count = len(text.split())
        if word_count < 5:
            clarity -= 0.2
        elif word_count > 50:
            clarity -= 0.1
        
        return max(0.0, clarity)
    
    def _is_action_required(self, intent: str, sentiment: SentimentAnalysis, entities: EntityRecognition) -> bool:
        """Determine if immediate action is required"""
        action_intents = ["business_inquiry", "franchise_inquiry", "financial_question", "urgency_question"]
        
        if intent in action_intents:
            return True
        
        if sentiment.urgency_level in [UrgencyLevel.HIGH, UrgencyLevel.URGENT]:
            return True
        
        if entities.entities.get("time_references"):
            return True
        
        return False
    
    def _is_follow_up_needed(self, entities: EntityRecognition, sentiment: SentimentAnalysis) -> bool:
        """Determine if follow-up is needed"""
        if sentiment.sentiment == SentimentType.UNCERTAIN:
            return True
        
        if not entities.entities.get("business_types") and not entities.entities.get("locations"):
            return True
        
        if sentiment.confidence < 0.5:
            return True
        
        return False

# Global instance
advanced_nlp = AdvancedNLP()
