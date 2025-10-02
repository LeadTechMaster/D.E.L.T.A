"""
Advanced Conversation Memory System
Maintains context, learns from interactions, and provides intelligent continuity
"""

import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ConversationTurn:
    """Represents a single turn in the conversation"""
    turn_id: str
    timestamp: datetime
    user_message: str
    bot_response: str
    detected_intent: str
    entities: Dict[str, Any]
    analysis_data: Optional[Dict[str, Any]] = None
    user_satisfaction: Optional[float] = None
    follow_up_needed: bool = False

@dataclass
class UserProfile:
    """User profile with preferences and history"""
    user_id: str
    preferences: Dict[str, Any]
    business_interests: List[str]
    location_preferences: List[str]
    investment_range: Optional[Tuple[float, float]]
    experience_level: str
    communication_style: str
    last_interaction: datetime

class ConversationMemory:
    """Advanced conversation memory with learning capabilities"""
    
    def __init__(self, storage_file: str = "storage/conversation_memory.json"):
        """Initialize conversation memory system"""
        self.storage_file = storage_file
        self.conversations: Dict[str, List[ConversationTurn]] = {}
        self.user_profiles: Dict[str, UserProfile] = {}
        self.global_insights: Dict[str, Any] = {}
        self.load_memory()
        logger.info("🧠 Advanced conversation memory system initialized")
    
    def load_memory(self):
        """Load conversation memory from storage"""
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
                self.conversations = self._deserialize_conversations(data.get('conversations', {}))
                self.user_profiles = self._deserialize_profiles(data.get('user_profiles', {}))
                self.global_insights = data.get('global_insights', {})
            logger.info(f"📂 Loaded {len(self.conversations)} conversation histories")
        except FileNotFoundError:
            logger.info("📂 No existing conversation memory found, starting fresh")
        except Exception as e:
            logger.error(f"❌ Error loading conversation memory: {e}")
    
    def save_memory(self):
        """Save conversation memory to storage"""
        try:
            data = {
                'conversations': self._serialize_conversations(self.conversations),
                'user_profiles': self._serialize_profiles(self.user_profiles),
                'global_insights': self.global_insights,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            logger.info("💾 Conversation memory saved successfully")
        except Exception as e:
            logger.error(f"❌ Error saving conversation memory: {e}")
    
    def _serialize_conversations(self, conversations: Dict[str, List[ConversationTurn]]) -> Dict[str, List[Dict]]:
        """Serialize conversations for JSON storage"""
        serialized = {}
        for session_id, turns in conversations.items():
            serialized[session_id] = [asdict(turn) for turn in turns]
        return serialized
    
    def _deserialize_conversations(self, data: Dict[str, List[Dict]]) -> Dict[str, List[ConversationTurn]]:
        """Deserialize conversations from JSON"""
        conversations = {}
        for session_id, turns_data in data.items():
            turns = []
            for turn_data in turns_data:
                turn_data['timestamp'] = datetime.fromisoformat(turn_data['timestamp'])
                turns.append(ConversationTurn(**turn_data))
            conversations[session_id] = turns
        return conversations
    
    def _serialize_profiles(self, profiles: Dict[str, UserProfile]) -> Dict[str, Dict]:
        """Serialize user profiles for JSON storage"""
        serialized = {}
        for user_id, profile in profiles.items():
            serialized[user_id] = asdict(profile)
        return serialized
    
    def _deserialize_profiles(self, data: Dict[str, Dict]) -> Dict[str, UserProfile]:
        """Deserialize user profiles from JSON"""
        profiles = {}
        for user_id, profile_data in data.items():
            profile_data['last_interaction'] = datetime.fromisoformat(profile_data['last_interaction'])
            profiles[user_id] = UserProfile(**profile_data)
        return profiles
    
    def add_turn(self, session_id: str, user_message: str, bot_response: str, 
                 detected_intent: str, entities: Dict[str, Any], 
                 analysis_data: Optional[Dict[str, Any]] = None) -> str:
        """Add a new conversation turn"""
        turn_id = str(uuid.uuid4())
        turn = ConversationTurn(
            turn_id=turn_id,
            timestamp=datetime.now(),
            user_message=user_message,
            bot_response=bot_response,
            detected_intent=detected_intent,
            entities=entities,
            analysis_data=analysis_data
        )
        
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        self.conversations[session_id].append(turn)
        
        # Update user profile
        self._update_user_profile(session_id, entities, analysis_data)
        
        # Extract insights
        self._extract_insights(turn)
        
        logger.info(f"🧠 Added turn {turn_id} to session {session_id}")
        return turn_id
    
    def get_conversation_context(self, session_id: str, turns_back: int = 3) -> List[ConversationTurn]:
        """Get recent conversation context"""
        if session_id not in self.conversations:
            return []
        
        recent_turns = self.conversations[session_id][-turns_back:]
        return recent_turns
    
    def get_user_profile(self, session_id: str) -> Optional[UserProfile]:
        """Get user profile for session"""
        return self.user_profiles.get(session_id)
    
    def _update_user_profile(self, session_id: str, entities: Dict[str, Any], 
                           analysis_data: Optional[Dict[str, Any]]):
        """Update user profile based on current interaction"""
        if session_id not in self.user_profiles:
            self.user_profiles[session_id] = UserProfile(
                user_id=session_id,
                preferences={},
                business_interests=[],
                location_preferences=[],
                investment_range=None,
                experience_level="beginner",
                communication_style="formal",
                last_interaction=datetime.now()
            )
        
        profile = self.user_profiles[session_id]
        profile.last_interaction = datetime.now()
        
        # Update business interests
        if entities.get("business_type"):
            if entities["business_type"] not in profile.business_interests:
                profile.business_interests.append(entities["business_type"])
        
        # Update location preferences
        if entities.get("location"):
            if entities["location"] not in profile.location_preferences:
                profile.location_preferences.append(entities["location"])
        
        # Detect experience level
        uncertainty_level = entities.get("uncertainty_level", 0)
        if uncertainty_level > 0.5:
            profile.experience_level = "beginner"
        elif uncertainty_level < 0.2:
            profile.experience_level = "experienced"
        
        # Detect communication style
        emphasis_level = entities.get("emphasis_level", 0)
        if emphasis_level > 0.3:
            profile.communication_style = "enthusiastic"
        elif entities.get("sentiment") == "positive":
            profile.communication_style = "friendly"
    
    def _extract_insights(self, turn: ConversationTurn):
        """Extract insights from conversation turn"""
        # Track popular business types
        if turn.entities.get("business_type"):
            business_type = turn.entities["business_type"]
            if "popular_business_types" not in self.global_insights:
                self.global_insights["popular_business_types"] = {}
            
            if business_type not in self.global_insights["popular_business_types"]:
                self.global_insights["popular_business_types"][business_type] = 0
            self.global_insights["popular_business_types"][business_type] += 1
        
        # Track popular locations
        if turn.entities.get("location"):
            location = turn.entities["location"]
            if "popular_locations" not in self.global_insights:
                self.global_insights["popular_locations"] = {}
            
            if location not in self.global_insights["popular_locations"]:
                self.global_insights["popular_locations"][location] = 0
            self.global_insights["popular_locations"][location] += 1
        
        # Track common questions and patterns
        if "common_patterns" not in self.global_insights:
            self.global_insights["common_patterns"] = {}
        
        pattern_key = f"{turn.detected_intent}_{bool(turn.entities.get('business_type'))}_{bool(turn.entities.get('location'))}"
        if pattern_key not in self.global_insights["common_patterns"]:
            self.global_insights["common_patterns"][pattern_key] = 0
        self.global_insights["common_patterns"][pattern_key] += 1
    
    def get_smart_suggestions(self, session_id: str, current_entities: Dict[str, Any]) -> List[str]:
        """Get smart suggestions based on conversation history"""
        suggestions = []
        
        # Get user profile
        profile = self.get_user_profile(session_id)
        if profile:
            # Suggest based on previous interests
            if profile.business_interests and not current_entities.get("business_type"):
                suggestions.append(f"Based on your interests, you might like: {', '.join(profile.business_interests[-2:])}")
            
            # Suggest based on previous locations
            if profile.location_preferences and not current_entities.get("location"):
                suggestions.append(f"You've shown interest in: {', '.join(profile.location_preferences[-2:])}")
        
        # Get global insights
        if "popular_business_types" in self.global_insights:
            popular_types = sorted(
                self.global_insights["popular_business_types"].items(),
                key=lambda x: x[1], reverse=True
            )[:3]
            if popular_types:
                suggestions.append(f"Popular business types: {', '.join([t[0] for t in popular_types])}")
        
        return suggestions
    
    def detect_conversation_patterns(self, session_id: str) -> Dict[str, Any]:
        """Detect patterns in the conversation"""
        if session_id not in self.conversations:
            return {}
        
        turns = self.conversations[session_id]
        patterns = {
            "total_turns": len(turns),
            "has_business_type": any(turn.entities.get("business_type") for turn in turns),
            "has_location": any(turn.entities.get("location") for turn in turns),
            "common_intents": {},
            "conversation_flow": []
        }
        
        # Analyze intent patterns
        for turn in turns:
            intent = turn.detected_intent
            if intent not in patterns["common_intents"]:
                patterns["common_intents"][intent] = 0
            patterns["common_intents"][intent] += 1
            patterns["conversation_flow"].append(intent)
        
        return patterns
    
    def generate_contextual_response_enhancement(self, session_id: str, 
                                               base_response: str) -> str:
        """Enhance response based on conversation context"""
        profile = self.get_user_profile(session_id)
        if not profile:
            return base_response
        
        enhancements = []
        
        # Add personalization based on profile
        if profile.communication_style == "enthusiastic":
            enhancements.append("I'm excited to help you with this!")
        elif profile.communication_style == "friendly":
            enhancements.append("I'm here to make this easy for you!")
        
        # Add experience-based guidance
        if profile.experience_level == "beginner":
            enhancements.append("I'll explain everything step by step.")
        elif profile.experience_level == "experienced":
            enhancements.append("I'll provide detailed, advanced insights.")
        
        # Add suggestions based on history
        smart_suggestions = self.get_smart_suggestions(session_id, {})
        if smart_suggestions:
            enhancements.extend(smart_suggestions)
        
        if enhancements:
            return base_response + "\n\n" + "\n".join([f"• {enhancement}" for enhancement in enhancements])
        
        return base_response

# Global instance
conversation_memory = ConversationMemory()
