"""
Layer 2: Stalling Model to Keep User Occupied
Provides engaging responses while Layer 3 (Gemini) processes complex requests
"""
import random
import time
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
import config
from jarvis_personal_bio import personal_bio_analyzer

class Layer2StallingModel:
    """Stalling model to keep user engaged while complex processing happens"""
    
    def __init__(self):
        self.stalling_responses = {
            'processing': [
                "Let me process that for you, Mr. Bharadwaj Sir...",
                "I'm analyzing your request, Mr. Bharadwaj Sir...",
                "Working on that, Mr. Bharadwaj Sir...",
                "Processing through my systems, Mr. Bharadwaj Sir...",
                "Let me think about that, Mr. Bharadwaj Sir...",
                "Consulting my knowledge base, Mr. Bharadwaj Sir...",
                "Analyzing the information, Mr. Bharadwaj Sir...",
                "Working through that request, Mr. Bharadwaj Sir..."
            ],
            'thinking': [
                "That's an interesting question, Mr. Bharadwaj Sir...",
                "Let me consider that carefully, Mr. Bharadwaj Sir...",
                "I need to think about that, Mr. Bharadwaj Sir...",
                "That requires some analysis, Mr. Bharadwaj Sir...",
                "Let me ponder that for a moment, Mr. Bharadwaj Sir...",
                "That's a thoughtful inquiry, Mr. Bharadwaj Sir...",
                "I'm processing that information, Mr. Bharadwaj Sir...",
                "Let me work through that, Mr. Bharadwaj Sir..."
            ],
            'searching': [
                "Searching through my databases, Mr. Bharadwaj Sir...",
                "Looking through my knowledge base, Mr. Bharadwaj Sir...",
                "Scanning through available information, Mr. Bharadwaj Sir...",
                "Consulting my resources, Mr. Bharadwaj Sir...",
                "Searching for the best answer, Mr. Bharadwaj Sir...",
                "Looking up relevant information, Mr. Bharadwaj Sir...",
                "Scanning through my systems, Mr. Bharadwaj Sir...",
                "Checking my knowledge sources, Mr. Bharadwaj Sir..."
            ],
            'analyzing': [
                "Analyzing the data, Mr. Bharadwaj Sir...",
                "Processing the information, Mr. Bharadwaj Sir...",
                "Examining the details, Mr. Bharadwaj Sir...",
                "Reviewing the information, Mr. Bharadwaj Sir...",
                "Studying the data, Mr. Bharadwaj Sir...",
                "Evaluating the options, Mr. Bharadwaj Sir...",
                "Assessing the situation, Mr. Bharadwaj Sir...",
                "Considering the possibilities, Mr. Bharadwaj Sir..."
            ],
            'personal': [
                "Let me recall what I know about you, Mr. Bharadwaj Sir...",
                "Considering your preferences, Mr. Bharadwaj Sir...",
                "Thinking about your specific needs, Mr. Bharadwaj Sir...",
                "Reflecting on your interests, Mr. Bharadwaj Sir...",
                "Considering your background, Mr. Bharadwaj Sir...",
                "Thinking about your goals, Mr. Bharadwaj Sir...",
                "Reflecting on your personality, Mr. Bharadwaj Sir...",
                "Considering your aspirations, Mr. Bharadwaj Sir..."
            ]
        }
        
        self.contextual_responses = {
            'morning': [
                "Good morning, Mr. Bharadwaj Sir. Let me help you with that...",
                "Starting the day with your request, Mr. Bharadwaj Sir...",
                "Morning processing, Mr. Bharadwaj Sir...",
                "Early morning analysis, Mr. Bharadwaj Sir..."
            ],
            'afternoon': [
                "Afternoon processing, Mr. Bharadwaj Sir...",
                "Midday analysis, Mr. Bharadwaj Sir...",
                "Afternoon consultation, Mr. Bharadwaj Sir...",
                "Lunchtime processing, Mr. Bharadwaj Sir..."
            ],
            'evening': [
                "Evening analysis, Mr. Bharadwaj Sir...",
                "End of day processing, Mr. Bharadwaj Sir...",
                "Evening consultation, Mr. Bharadwaj Sir...",
                "Late day analysis, Mr. Bharadwaj Sir..."
            ]
        }
        
        self.progress_indicators = [
            "Initializing...",
            "Loading data...",
            "Processing...",
            "Analyzing...",
            "Finalizing...",
            "Almost ready...",
            "Preparing response..."
        ]
        
        self.stalling_active = False
        self.stalling_thread = None
        self.user_engaged = False
        
        # Performance tracking
        self.stats = {
            'total_stalling_sessions': 0,
            'average_stalling_time': 0,
            'user_engagement_events': 0,
            'successful_handoffs': 0
        }
    
    def start_stalling(self, user_input: str, callback: Callable[[str], str], 
                      max_wait_time: float = 10.0) -> str:
        """Start stalling process and return initial response"""
        self.stalling_active = True
        self.stats['total_stalling_sessions'] += 1
        
        # Get initial stalling response based on input type
        initial_response = self._get_initial_stalling_response(user_input)
        
        # Start stalling thread
        self.stalling_thread = threading.Thread(
            target=self._stalling_process,
            args=(user_input, callback, max_wait_time)
        )
        self.stalling_thread.daemon = True
        self.stalling_thread.start()
        
        return initial_response
    
    def _stalling_process(self, user_input: str, callback: Callable[[str], str], 
                         max_wait_time: float):
        """Background stalling process"""
        start_time = time.time()
        progress_index = 0
        
        while self.stalling_active and (time.time() - start_time) < max_wait_time:
            # Simulate progress
            if progress_index < len(self.progress_indicators):
                progress = self.progress_indicators[progress_index]
                progress_index += 1
            else:
                progress = random.choice(self.progress_indicators)
            
            # Wait before next update
            time.sleep(1.0)
            
            # Check if callback is ready
            try:
                result = callback(user_input)
                if result and result != "PROCESSING":
                    self.stalling_active = False
                    self.stats['successful_handoffs'] += 1
                    break
            except Exception:
                pass
        
        # Calculate stalling time
        stalling_time = time.time() - start_time
        self.stats['average_stalling_time'] = (
            (self.stats['average_stalling_time'] * (self.stats['total_stalling_sessions'] - 1) + stalling_time) /
            self.stats['total_stalling_sessions']
        )
        
        self.stalling_active = False
    
    def _get_initial_stalling_response(self, user_input: str) -> str:
        """Get initial stalling response based on input type"""
        user_input_lower = user_input.lower()
        
        # Determine response category
        if any(word in user_input_lower for word in ['what', 'who', 'how', 'why', 'when', 'where']):
            category = 'thinking'
        elif any(word in user_input_lower for word in ['find', 'search', 'look', 'locate']):
            category = 'searching'
        elif any(word in user_input_lower for word in ['analyze', 'explain', 'describe', 'tell me about']):
            category = 'analyzing'
        elif any(word in user_input_lower for word in ['remember', 'personal', 'about me', 'my']):
            category = 'personal'
        else:
            category = 'processing'
        
        # Get time-based response
        now = datetime.now()
        if now.hour < 12:
            time_category = 'morning'
        elif now.hour < 17:
            time_category = 'afternoon'
        else:
            time_category = 'evening'
        
        # Combine responses
        base_response = random.choice(self.stalling_responses[category])
        time_response = random.choice(self.contextual_responses[time_category])
        
        # Add personal touch
        personal_touch = self._get_personal_touch()
        
        return f"{base_response} {time_response} {personal_touch}"
    
    def _get_personal_touch(self) -> str:
        """Add personal touch based on user's bio"""
        try:
            personality_traits = personal_bio_analyzer.personality_traits
            if personality_traits:
                top_traits = sorted(personality_traits.items(), 
                                  key=lambda x: x[1]['strength'], reverse=True)[:2]
                
                if top_traits:
                    trait_names = [trait.replace('_', ' ').title() for trait, _ in top_traits]
                    return f"I'm considering your {trait_names[0]} nature, Mr. Bharadwaj Sir."
        except Exception:
            pass
        
        return "I'm considering your specific needs, Mr. Bharadwaj Sir."
    
    def get_engaging_follow_up(self) -> str:
        """Get engaging follow-up response"""
        if not self.stalling_active:
            return None
        
        follow_ups = [
            "Still working on that, Mr. Bharadwaj Sir...",
            "Processing continues, Mr. Bharadwaj Sir...",
            "Almost there, Mr. Bharadwaj Sir...",
            "Finalizing the analysis, Mr. Bharadwaj Sir...",
            "Preparing the response, Mr. Bharadwaj Sir...",
            "Just a moment more, Mr. Bharadwaj Sir...",
            "Nearly complete, Mr. Bharadwaj Sir...",
            "Final touches, Mr. Bharadwaj Sir..."
        ]
        
        return random.choice(follow_ups)
    
    def stop_stalling(self):
        """Stop the stalling process"""
        self.stalling_active = False
        if self.stalling_thread and self.stalling_thread.is_alive():
            self.stalling_thread.join(timeout=1.0)
    
    def is_stalling(self) -> bool:
        """Check if currently stalling"""
        return self.stalling_active
    
    def get_processing_status(self) -> str:
        """Get current processing status"""
        if not self.stalling_active:
            return "Not processing"
        
        statuses = [
            "Processing request...",
            "Analyzing information...",
            "Consulting knowledge base...",
            "Preparing response...",
            "Finalizing analysis...",
            "Almost ready...",
            "Working on it...",
            "Processing through systems..."
        ]
        
        return random.choice(statuses)
    
    def engage_user_with_questions(self, user_input: str) -> List[str]:
        """Generate engaging questions to keep user occupied"""
        questions = []
        
        # Contextual questions based on input
        user_input_lower = user_input.lower()
        
        if 'weather' in user_input_lower:
            questions = [
                "While I check the weather, are you planning any outdoor activities today, Mr. Bharadwaj Sir?",
                "I'm getting the weather data. Do you prefer sunny or rainy days, Mr. Bharadwaj Sir?",
                "Checking weather conditions. What's your favorite season, Mr. Bharadwaj Sir?"
            ]
        elif 'file' in user_input_lower or 'search' in user_input_lower:
            questions = [
                "While I search for that, do you organize your files in any particular way, Mr. Bharadwaj Sir?",
                "I'm looking through your files. Do you have a preferred naming convention, Mr. Bharadwaj Sir?",
                "Searching now. Are you looking for something specific or just browsing, Mr. Bharadwaj Sir?"
            ]
        elif 'system' in user_input_lower or 'computer' in user_input_lower:
            questions = [
                "While I check system status, how has your computer been performing lately, Mr. Bharadwaj Sir?",
                "I'm analyzing system data. Do you notice any particular issues, Mr. Bharadwaj Sir?",
                "Checking system health. Are you satisfied with your current setup, Mr. Bharadwaj Sir?"
            ]
        else:
            questions = [
                "While I process that, is there anything else I can help you with, Mr. Bharadwaj Sir?",
                "I'm working on your request. How has your day been so far, Mr. Bharadwaj Sir?",
                "Processing now. Are you working on any interesting projects, Mr. Bharadwaj Sir?"
            ]
        
        return questions
    
    def get_personal_insights(self) -> str:
        """Get personal insights to share while stalling"""
        try:
            personality_traits = personal_bio_analyzer.personality_traits
            if personality_traits:
                top_trait = max(personality_traits.items(), key=lambda x: x[1]['strength'])
                trait_name = top_trait[0].replace('_', ' ').title()
                
                insights = [
                    f"I notice your {trait_name} nature, Mr. Bharadwaj Sir. That's quite admirable.",
                    f"Your {trait_name} approach to things is impressive, Mr. Bharadwaj Sir.",
                    f"I can see your {trait_name} qualities, Mr. Bharadwaj Sir. Very commendable."
                ]
                
                return random.choice(insights)
        except Exception:
            pass
        
        return "I'm considering your specific needs and preferences, Mr. Bharadwaj Sir."
    
    def get_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        return {
            'total_stalling_sessions': self.stats['total_stalling_sessions'],
            'average_stalling_time': self.stats['average_stalling_time'],
            'user_engagement_events': self.stats['user_engagement_events'],
            'successful_handoffs': self.stats['successful_handoffs'],
            'currently_stalling': self.stalling_active
        }
    
    def is_available(self) -> bool:
        """Check if stalling model is available"""
        return True  # Always available

# Initialize the stalling model
layer2_stalling_model = Layer2StallingModel()
