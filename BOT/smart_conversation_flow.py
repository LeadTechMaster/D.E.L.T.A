"""
Smart Conversation Flow Manager - Advanced Logic for Natural Conversations
Handles multi-step reasoning, contextual follow-ups, and intelligent conversation management
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConversationState(Enum):
    """Conversation states for flow management"""
    GREETING = "greeting"
    COLLECTING_BUSINESS_TYPE = "collecting_business_type"
    COLLECTING_LOCATION = "collecting_location"
    ANALYZING_MARKET = "analyzing_market"
    PROVIDING_INSIGHTS = "providing_insights"
    FOLLOW_UP_QUESTIONS = "follow_up_questions"
    COMPARISON_MODE = "comparison_mode"
    DEEP_DIVE_ANALYSIS = "deep_dive_analysis"
    RECOMMENDATION_PHASE = "recommendation_phase"

class AnalysisType(Enum):
    """Types of analysis to perform"""
    BASIC_MARKET = "basic_market"
    COMPETITION_DEEP_DIVE = "competition_deep_dive"
    FRANCHISE_ANALYSIS = "franchise_analysis"
    DEMOGRAPHIC_ANALYSIS = "demographic_analysis"
    FINANCIAL_ANALYSIS = "financial_analysis"
    LOCATION_COMPARISON = "location_comparison"
    BUSINESS_TYPE_COMPARISON = "business_type_comparison"

@dataclass
class ConversationContext:
    """Current conversation context"""
    session_id: str
    current_state: ConversationState
    business_type: Optional[str]
    location: Optional[str]
    previous_analyses: List[Dict[str, Any]]
    user_preferences: Dict[str, Any]
    conversation_depth: int
    analysis_history: List[AnalysisType]
    pending_follow_ups: List[str]
    user_satisfaction_level: float

@dataclass
class SmartFollowUp:
    """Smart follow-up suggestion"""
    question: str
    reasoning: str
    priority: int
    analysis_type: Optional[AnalysisType]
    expected_benefit: str

class SmartConversationFlow:
    """Manages intelligent conversation flow and multi-step reasoning"""
    
    def __init__(self):
        """Initialize smart conversation flow"""
        self.conversation_contexts: Dict[str, ConversationContext] = {}
        self.flow_patterns = self._build_flow_patterns()
        self.follow_up_strategies = self._build_follow_up_strategies()
        self.reasoning_engines = self._build_reasoning_engines()
        logger.info("🧠 Smart conversation flow manager initialized")
    
    def _build_flow_patterns(self) -> Dict[ConversationState, Dict[str, Any]]:
        """Build conversation flow patterns"""
        return {
            ConversationState.GREETING: {
                "next_states": [ConversationState.COLLECTING_BUSINESS_TYPE, ConversationState.COLLECTING_LOCATION],
                "triggers": ["business_mentioned", "location_mentioned", "general_question"],
                "suggestions": ["Ask about business type", "Ask about location", "Provide general guidance"]
            },
            ConversationState.COLLECTING_BUSINESS_TYPE: {
                "next_states": [ConversationState.COLLECTING_LOCATION, ConversationState.ANALYZING_MARKET],
                "triggers": ["business_type_provided", "location_also_provided"],
                "suggestions": ["Ask for location", "Begin market analysis if location known"]
            },
            ConversationState.COLLECTING_LOCATION: {
                "next_states": [ConversationState.ANALYZING_MARKET, ConversationState.PROVIDING_INSIGHTS],
                "triggers": ["location_provided", "both_provided"],
                "suggestions": ["Begin comprehensive analysis", "Provide market insights"]
            },
            ConversationState.ANALYZING_MARKET: {
                "next_states": [ConversationState.PROVIDING_INSIGHTS, ConversationState.FOLLOW_UP_QUESTIONS],
                "triggers": ["analysis_complete", "user_questions"],
                "suggestions": ["Present findings", "Ask follow-up questions"]
            },
            ConversationState.PROVIDING_INSIGHTS: {
                "next_states": [ConversationState.FOLLOW_UP_QUESTIONS, ConversationState.COMPARISON_MODE],
                "triggers": ["insights_delivered", "comparison_requested"],
                "suggestions": ["Offer comparisons", "Suggest next steps"]
            },
            ConversationState.FOLLOW_UP_QUESTIONS: {
                "next_states": [ConversationState.DEEP_DIVE_ANALYSIS, ConversationState.RECOMMENDATION_PHASE],
                "triggers": ["follow_up_selected", "recommendation_requested"],
                "suggestions": ["Deep dive analysis", "Provide recommendations"]
            },
            ConversationState.COMPARISON_MODE: {
                "next_states": [ConversationState.DEEP_DIVE_ANALYSIS, ConversationState.RECOMMENDATION_PHASE],
                "triggers": ["comparison_complete", "recommendation_ready"],
                "suggestions": ["Analyze differences", "Make recommendations"]
            }
        }
    
    def _build_follow_up_strategies(self) -> Dict[str, List[SmartFollowUp]]:
        """Build intelligent follow-up strategies"""
        return {
            "basic_analysis_complete": [
                SmartFollowUp(
                    question="Would you like to see detailed competitor analysis?",
                    reasoning="Competition analysis is crucial for business success",
                    priority=1,
                    analysis_type=AnalysisType.COMPETITION_DEEP_DIVE,
                    expected_benefit="Better understanding of market positioning"
                ),
                SmartFollowUp(
                    question="Should I find franchise opportunities in this area?",
                    reasoning="Franchises can reduce risk and provide support",
                    priority=2,
                    analysis_type=AnalysisType.FRANCHISE_ANALYSIS,
                    expected_benefit="Lower risk business opportunities"
                ),
                SmartFollowUp(
                    question="Do you want demographic data for this location?",
                    reasoning="Demographics help identify target customers",
                    priority=3,
                    analysis_type=AnalysisType.DEMOGRAPHIC_ANALYSIS,
                    expected_benefit="Better customer targeting"
                )
            ],
            "high_competition": [
                SmartFollowUp(
                    question="Would you like to analyze alternative locations?",
                    reasoning="High competition suggests exploring other areas",
                    priority=1,
                    analysis_type=AnalysisType.LOCATION_COMPARISON,
                    expected_benefit="Find less competitive markets"
                ),
                SmartFollowUp(
                    question="Should I analyze different business types for this location?",
                    reasoning="Location might be better suited for other businesses",
                    priority=2,
                    analysis_type=AnalysisType.BUSINESS_TYPE_COMPARISON,
                    expected_benefit="Optimize business-location match"
                ),
                SmartFollowUp(
                    question="Would you like to see niche market opportunities?",
                    reasoning="Niche markets can avoid direct competition",
                    priority=3,
                    analysis_type=AnalysisType.BASIC_MARKET,
                    expected_benefit="Find underserved market segments"
                )
            ],
            "low_competition": [
                SmartFollowUp(
                    question="Should I verify market demand exists?",
                    reasoning="Low competition might indicate low demand",
                    priority=1,
                    analysis_type=AnalysisType.DEMOGRAPHIC_ANALYSIS,
                    expected_benefit="Validate market opportunity"
                ),
                SmartFollowUp(
                    question="Would you like to analyze why competitors haven't entered?",
                    reasoning="Understanding barriers helps assess feasibility",
                    priority=2,
                    analysis_type=AnalysisType.FINANCIAL_ANALYSIS,
                    expected_benefit="Identify potential challenges"
                ),
                SmartFollowUp(
                    question="Should I research market growth potential?",
                    reasoning="Early entry requires understanding growth trajectory",
                    priority=3,
                    analysis_type=AnalysisType.BASIC_MARKET,
                    expected_benefit="Assess long-term viability"
                )
            ],
            "franchise_opportunities_found": [
                SmartFollowUp(
                    question="Would you like detailed financial analysis of these franchises?",
                    reasoning="Financial details are crucial for franchise decisions",
                    priority=1,
                    analysis_type=AnalysisType.FINANCIAL_ANALYSIS,
                    expected_benefit="Make informed investment decisions"
                ),
                SmartFollowUp(
                    question="Should I compare franchise vs. independent business?",
                    reasoning="Comparison helps choose the right business model",
                    priority=2,
                    analysis_type=AnalysisType.BUSINESS_TYPE_COMPARISON,
                    expected_benefit="Choose optimal business approach"
                ),
                SmartFollowUp(
                    question="Would you like territory availability analysis?",
                    reasoning="Territory availability affects franchise success",
                    priority=3,
                    analysis_type=AnalysisType.COMPETITION_DEEP_DIVE,
                    expected_benefit="Ensure exclusive territory"
                )
            ]
        }
    
    def _build_reasoning_engines(self) -> Dict[str, Any]:
        """Build reasoning engines for different scenarios"""
        return {
            "market_analysis_reasoning": {
                "high_competition": {
                    "reasoning": "High competition indicates market saturation",
                    "suggestions": ["Explore niche markets", "Consider differentiation", "Analyze alternative locations"],
                    "next_analysis": AnalysisType.LOCATION_COMPARISON
                },
                "low_competition": {
                    "reasoning": "Low competition might indicate opportunity or low demand",
                    "suggestions": ["Verify market demand", "Research entry barriers", "Analyze growth potential"],
                    "next_analysis": AnalysisType.DEMOGRAPHIC_ANALYSIS
                },
                "moderate_competition": {
                    "reasoning": "Moderate competition suggests healthy market",
                    "suggestions": ["Focus on differentiation", "Analyze competitor strengths", "Identify market gaps"],
                    "next_analysis": AnalysisType.COMPETITION_DEEP_DIVE
                }
            },
            "investment_reasoning": {
                "high_investment": {
                    "reasoning": "High investment requires careful financial planning",
                    "suggestions": ["Explore financing options", "Consider partnerships", "Analyze ROI projections"],
                    "next_analysis": AnalysisType.FINANCIAL_ANALYSIS
                },
                "moderate_investment": {
                    "reasoning": "Moderate investment balances risk and opportunity",
                    "suggestions": ["Compare ROI with competitors", "Analyze break-even timeline", "Consider growth potential"],
                    "next_analysis": AnalysisType.FINANCIAL_ANALYSIS
                },
                "low_investment": {
                    "reasoning": "Low investment reduces financial risk",
                    "suggestions": ["Focus on growth strategies", "Analyze scalability", "Consider multiple locations"],
                    "next_analysis": AnalysisType.BASIC_MARKET
                }
            }
        }
    
    def get_conversation_context(self, session_id: str) -> ConversationContext:
        """Get or create conversation context"""
        if session_id not in self.conversation_contexts:
            self.conversation_contexts[session_id] = ConversationContext(
                session_id=session_id,
                current_state=ConversationState.GREETING,
                business_type=None,
                location=None,
                previous_analyses=[],
                user_preferences={},
                conversation_depth=0,
                analysis_history=[],
                pending_follow_ups=[],
                user_satisfaction_level=0.5
            )
        return self.conversation_contexts[session_id]
    
    def update_context(self, session_id: str, business_type: Optional[str] = None,
                      location: Optional[str] = None, analysis_data: Optional[Dict[str, Any]] = None,
                      user_satisfaction: Optional[float] = None) -> ConversationContext:
        """Update conversation context"""
        context = self.get_conversation_context(session_id)
        
        if business_type:
            context.business_type = business_type
        if location:
            context.location = location
        if analysis_data:
            context.previous_analyses.append(analysis_data)
        if user_satisfaction is not None:
            context.user_satisfaction_level = user_satisfaction
        
        context.conversation_depth += 1
        
        # Update state based on available information
        self._update_conversation_state(context)
        
        logger.info(f"🧠 Updated context for {session_id}: state={context.current_state.value}")
        return context
    
    def _update_conversation_state(self, context: ConversationContext):
        """Update conversation state based on available information"""
        if not context.business_type and not context.location:
            context.current_state = ConversationState.GREETING
        elif context.business_type and not context.location:
            context.current_state = ConversationState.COLLECTING_LOCATION
        elif not context.business_type and context.location:
            context.current_state = ConversationState.COLLECTING_BUSINESS_TYPE
        elif context.business_type and context.location and not context.previous_analyses:
            context.current_state = ConversationState.ANALYZING_MARKET
        elif context.previous_analyses and context.current_state == ConversationState.ANALYZING_MARKET:
            context.current_state = ConversationState.PROVIDING_INSIGHTS
        elif context.pending_follow_ups:
            context.current_state = ConversationState.FOLLOW_UP_QUESTIONS
    
    def generate_smart_follow_ups(self, session_id: str, analysis_data: Dict[str, Any]) -> List[SmartFollowUp]:
        """Generate intelligent follow-up questions based on analysis"""
        context = self.get_conversation_context(session_id)
        follow_ups = []
        
        # Determine strategy based on analysis results
        strategy_key = self._determine_follow_up_strategy(analysis_data)
        
        if strategy_key in self.follow_up_strategies:
            follow_ups = self.follow_up_strategies[strategy_key].copy()
        
        # Apply reasoning engine
        reasoning_result = self._apply_reasoning_engine(analysis_data)
        if reasoning_result:
            follow_ups.extend(reasoning_result)
        
        # Prioritize and filter based on context
        filtered_follow_ups = self._filter_and_prioritize_follow_ups(follow_ups, context)
        
        context.pending_follow_ups = [fup.question for fup in filtered_follow_ups]
        
        logger.info(f"🧠 Generated {len(filtered_follow_ups)} smart follow-ups for {session_id}")
        return filtered_follow_ups[:3]  # Return top 3
    
    def _determine_follow_up_strategy(self, analysis_data: Dict[str, Any]) -> str:
        """Determine which follow-up strategy to use"""
        territory = analysis_data.get("territory_analysis", {})
        franchise_opps = analysis_data.get("franchise_opportunities", [])
        
        # Check competition level
        competitor_count = territory.get("competitor_count", 0)
        if competitor_count > 10:
            return "high_competition"
        elif competitor_count < 3:
            return "low_competition"
        
        # Check for franchise opportunities
        if franchise_opps and len(franchise_opps) > 0:
            return "franchise_opportunities_found"
        
        # Default strategy
        return "basic_analysis_complete"
    
    def _apply_reasoning_engine(self, analysis_data: Dict[str, Any]) -> List[SmartFollowUp]:
        """Apply reasoning engine to generate additional follow-ups"""
        follow_ups = []
        
        # Market analysis reasoning
        territory = analysis_data.get("territory_analysis", {})
        competitor_count = territory.get("competitor_count", 0)
        
        if competitor_count > 10:
            reasoning = self.reasoning_engines["market_analysis_reasoning"]["high_competition"]
        elif competitor_count < 3:
            reasoning = self.reasoning_engines["market_analysis_reasoning"]["low_competition"]
        else:
            reasoning = self.reasoning_engines["market_analysis_reasoning"]["moderate_competition"]
        
        # Create follow-up based on reasoning
        for suggestion in reasoning["suggestions"][:2]:  # Top 2 suggestions
            follow_ups.append(SmartFollowUp(
                question=f"Would you like me to {suggestion.lower()}?",
                reasoning=reasoning["reasoning"],
                priority=2,
                analysis_type=reasoning["next_analysis"],
                expected_benefit="Better market understanding"
            ))
        
        return follow_ups
    
    def _filter_and_prioritize_follow_ups(self, follow_ups: List[SmartFollowUp], 
                                         context: ConversationContext) -> List[SmartFollowUp]:
        """Filter and prioritize follow-ups based on context"""
        # Remove duplicates
        unique_follow_ups = []
        seen_questions = set()
        
        for follow_up in follow_ups:
            if follow_up.question not in seen_questions:
                unique_follow_ups.append(follow_up)
                seen_questions.add(follow_up.question)
        
        # Sort by priority
        unique_follow_ups.sort(key=lambda x: x.priority)
        
        # Apply user preference filtering
        filtered = []
        for follow_up in unique_follow_ups:
            if self._should_include_follow_up(follow_up, context):
                filtered.append(follow_up)
        
        return filtered
    
    def _should_include_follow_up(self, follow_up: SmartFollowUp, context: ConversationContext) -> bool:
        """Determine if follow-up should be included based on context"""
        # Skip if already analyzed
        if follow_up.analysis_type in context.analysis_history:
            return False
        
        # Skip if user satisfaction is low and question is complex
        if context.user_satisfaction_level < 0.3 and follow_up.priority > 2:
            return False
        
        # Include based on conversation depth
        if context.conversation_depth > 5 and follow_up.priority > 2:
            return False
        
        return True
    
    def get_next_conversation_step(self, session_id: str) -> Dict[str, Any]:
        """Get the next step in the conversation flow"""
        context = self.get_conversation_context(session_id)
        flow_pattern = self.flow_patterns.get(context.current_state, {})
        
        next_step = {
            "current_state": context.current_state.value,
            "suggested_next_states": flow_pattern.get("next_states", []),
            "triggers": flow_pattern.get("triggers", []),
            "suggestions": flow_pattern.get("suggestions", []),
            "conversation_depth": context.conversation_depth,
            "user_satisfaction": context.user_satisfaction_level
        }
        
        return next_step
    
    def should_escalate_analysis(self, session_id: str) -> bool:
        """Determine if analysis should be escalated"""
        context = self.get_conversation_context(session_id)
        
        # Escalate if high user satisfaction and deep conversation
        if context.user_satisfaction_level > 0.7 and context.conversation_depth > 3:
            return True
        
        # Escalate if multiple failed attempts
        if context.conversation_depth > 6 and context.user_satisfaction_level < 0.4:
            return True
        
        return False

# Global instance
smart_conversation_flow = SmartConversationFlow()
