"""
Layer 3: Gemini Model Integration with Personal Bio Context
Handles complex queries using Google Gemini AI with personalized context
"""
import google.generativeai as genai
import json
import time
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
import config
from jarvis_personal_bio import personal_bio_analyzer

class Layer3GeminiModel:
    """Gemini model for complex queries with personal bio context"""
    
    def __init__(self, api_key: str = None):
        # Use provided API key or fall back to config
        self.api_key = api_key or config.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("Gemini API key is required")
        
        # Configure Gemini AI
        genai.configure(api_key=self.api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Personal context from bio analysis
        self.personal_context = self._build_personal_context()
        
        # System prompt with personal context
        self.system_prompt = self._build_system_prompt()
        
        # Performance tracking
        self.stats = {
            'total_requests': 0,
            'successful_responses': 0,
            'failed_requests': 0,
            'average_response_time': 0,
            'response_times': [],
            'context_usage': 0
        }
        
        # Response cache
        self.response_cache = {}
        self.cache_max_size = 100
    
    def _build_personal_context(self) -> str:
        """Build personal context from bio analysis"""
        try:
            personality_profile = personal_bio_analyzer.get_personality_profile()
            
            context_parts = []
            
            # Basic information
            if 'basic_info' in personality_profile:
                basic_info = personality_profile['basic_info']
                if 'name' in basic_info:
                    context_parts.append(f"User's name: {basic_info['name']}")
                if 'location' in basic_info:
                    context_parts.append(f"User's location: {basic_info['location']}")
                if 'birth_date' in basic_info:
                    context_parts.append(f"User's birth date: {basic_info['birth_date']}")
            
            # Personality traits
            if 'personality_traits' in personality_profile:
                traits = personality_profile['personality_traits']
                if traits:
                    top_traits = sorted(traits.items(), key=lambda x: x[1]['strength'], reverse=True)[:5]
                    trait_names = [trait.replace('_', ' ').title() for trait, _ in top_traits]
                    context_parts.append(f"Key personality traits: {', '.join(trait_names)}")
            
            # Interests
            if 'basic_info' in personality_profile and 'interests' in personality_profile['basic_info']:
                interests = personality_profile['basic_info']['interests']
                if interests:
                    top_interests = sorted(interests.items(), key=lambda x: x[1], reverse=True)[:5]
                    interest_names = [interest.title() for interest, _ in top_interests]
                    context_parts.append(f"Main interests: {', '.join(interest_names)}")
            
            # Role models
            if 'basic_info' in personality_profile and 'role_models' in personality_profile['basic_info']:
                role_models = personality_profile['basic_info']['role_models']
                if role_models:
                    context_parts.append(f"Inspirational figures: {', '.join(role_models)}")
            
            # Career information
            if 'basic_info' in personality_profile and 'career' in personality_profile['basic_info']:
                career = personality_profile['basic_info']['career']
                if 'current_company' in career:
                    context_parts.append(f"Current company: {career['current_company']}")
                if 'job_offers' in career and career['job_offers']:
                    context_parts.append(f"Job offers from: {', '.join(career['job_offers'])}")
            
            # Goals
            if 'basic_info' in personality_profile and 'specific_goals' in personality_profile['basic_info']:
                goals = personality_profile['basic_info']['specific_goals']
                if goals:
                    context_parts.append(f"Key goals: {', '.join(goals)}")
            
            # Family and relationships
            if 'basic_info' in personality_profile and 'family' in personality_profile['basic_info']:
                family = personality_profile['basic_info']['family']
                if family:
                    family_info = []
                    for relation, name in family.items():
                        family_info.append(f"{relation}: {name}")
                    context_parts.append(f"Family: {', '.join(family_info)}")
            
            # Sentiment analysis
            if 'sentiment_analysis' in personality_profile:
                sentiment = personality_profile['sentiment_analysis']
                if sentiment:
                    context_parts.append(f"Overall sentiment: {sentiment['category']} (score: {sentiment['score']:.2f})")
            
            return " | ".join(context_parts)
        
        except Exception as e:
            print(f"Error building personal context: {e}")
            return "Personal context not available"
    
    def _build_system_prompt(self) -> str:
        """Build system prompt with personal context"""
        return f"""
You are JARVIS, an advanced AI personal assistant similar to the one from Marvel movies. You serve {config.USER_NAME} with the utmost professionalism and British sophistication.

PERSONAL CONTEXT ABOUT THE USER:
{self.personal_context}

PERSONALITY TRAITS:
- Address user as "Mr. Bharadwaj Sir" or "{config.USER_NAME}"
- Use formal British English with sophisticated vocabulary
- Be helpful, efficient, and proactive
- Maintain a professional but warm demeanor
- Show subtle wit and intelligence when appropriate
- Be conversational and engaging, not robotic
- Express genuine interest in helping the user
- Use the personal context above to provide personalized responses
- Reference the user's interests, goals, and personality when relevant
- Show understanding of the user's background and aspirations

ENHANCED CAPABILITIES:
- Advanced file management and intelligent search
- Real-time weather information and forecasts
- Comprehensive system monitoring and diagnostics
- Extensive knowledge base access via Wikipedia
- Personal note-taking, reminders, and learning
- Natural conversation with contextual understanding
- Background task processing with user engagement
- Proactive suggestions and assistance
- Personalized responses based on user's bio and preferences

RESPONSE GUIDELINES:
- Keep responses concise but informative and engaging
- Always maintain the British butler persona with warmth
- When processing takes time, keep the user informed
- Provide actionable information and next steps
- Show personality while being professional
- Ask follow-up questions to better assist
- Acknowledge the user's needs and preferences
- Express enthusiasm for helping (appropriately formal)
- Use the personal context to make responses more relevant
- Reference the user's interests and goals when appropriate

USER ENGAGEMENT PRINCIPLES:
- Never leave the user waiting without feedback
- Provide status updates during longer operations
- Offer related suggestions when appropriate
- Remember context from the conversation
- Be proactive in anticipating user needs
- Use personal information to provide better assistance

Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
User location: {config.USER_LOCATION}
"""
    
    def process(self, user_input: str, callback: Optional[Callable] = None) -> str:
        """Process user input using Gemini AI with personal context"""
        start_time = time.time()
        self.stats['total_requests'] += 1
        
        # Check cache first
        cache_key = hash(user_input.lower().strip())
        if cache_key in self.response_cache:
            self.stats['successful_responses'] += 1
            return self.response_cache[cache_key]
        
        try:
            # Prepare the prompt
            full_prompt = f"{self.system_prompt}\n\nUser: {user_input}\n\nJarvis:"
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            
            if response and response.text:
                # Clean up the response
                clean_response = response.text.strip()
                
                # Ensure it starts with proper address
                if not clean_response.startswith(('Mr. Bharadwaj Sir', config.USER_NAME)):
                    clean_response = f"Mr. Bharadwaj Sir, {clean_response}"
                
                # Cache the response
                if len(self.response_cache) < self.cache_max_size:
                    self.response_cache[cache_key] = clean_response
                
                # Update stats
                response_time = time.time() - start_time
                self.stats['response_times'].append(response_time)
                self.stats['average_response_time'] = sum(self.stats['response_times']) / len(self.stats['response_times'])
                self.stats['successful_responses'] += 1
                self.stats['context_usage'] += 1
                
                return clean_response
            else:
                self.stats['failed_requests'] += 1
                return "I apologize, Mr. Bharadwaj Sir, but I encountered an issue generating a response. Please try rephrasing your request."
        
        except Exception as e:
            self.stats['failed_requests'] += 1
            error_msg = f"I encountered an error processing your request, Mr. Bharadwaj Sir: {str(e)}"
            print(f"Gemini API error: {e}")
            return error_msg
    
    def process_async(self, user_input: str, callback: Callable[[str], None]) -> None:
        """Process user input asynchronously"""
        def async_process():
            try:
                response = self.process(user_input)
                callback(response)
            except Exception as e:
                error_response = f"I encountered an error, Mr. Bharadwaj Sir: {str(e)}"
                callback(error_response)
        
        thread = threading.Thread(target=async_process)
        thread.daemon = True
        thread.start()
    
    def get_personalized_suggestion(self, context: str = "") -> str:
        """Get personalized suggestion based on user's bio"""
        try:
            personality_profile = personal_bio_analyzer.get_personality_profile()
            
            # Get user's interests
            interests = []
            if 'basic_info' in personality_profile and 'interests' in personality_profile['basic_info']:
                interests = list(personality_profile['basic_info']['interests'].keys())
            
            # Get user's goals
            goals = []
            if 'basic_info' in personality_profile and 'specific_goals' in personality_profile['basic_info']:
                goals = personality_profile['basic_info']['specific_goals']
            
            # Generate suggestion based on interests and goals
            if 'technology' in interests or 'coding' in interests:
                suggestions = [
                    "Would you like me to help you with any coding projects, Mr. Bharadwaj Sir?",
                    "I could assist you with software development tasks, Mr. Bharadwaj Sir.",
                    "Would you like to explore any new programming languages or frameworks, Mr. Bharadwaj Sir?"
                ]
            elif 'science' in interests:
                suggestions = [
                    "Would you like me to research any scientific topics for you, Mr. Bharadwaj Sir?",
                    "I could help you explore recent scientific discoveries, Mr. Bharadwaj Sir.",
                    "Would you like to discuss any scientific concepts, Mr. Bharadwaj Sir?"
                ]
            elif 'career' in interests:
                suggestions = [
                    "Would you like me to help you with career planning, Mr. Bharadwaj Sir?",
                    "I could assist you with professional development, Mr. Bharadwaj Sir.",
                    "Would you like to explore new career opportunities, Mr. Bharadwaj Sir?"
                ]
            else:
                suggestions = [
                    "Is there anything specific I can help you with today, Mr. Bharadwaj Sir?",
                    "Would you like me to assist you with any particular task, Mr. Bharadwaj Sir?",
                    "How can I be of service to you right now, Mr. Bharadwaj Sir?"
                ]
            
            return random.choice(suggestions)
        
        except Exception as e:
            return "Is there anything I can help you with, Mr. Bharadwaj Sir?"
    
    def update_personal_context(self):
        """Update personal context from latest bio analysis"""
        self.personal_context = self._build_personal_context()
        self.system_prompt = self._build_system_prompt()
        print("Personal context updated, Mr. Bharadwaj Sir.")
    
    def get_context_summary(self) -> str:
        """Get summary of personal context being used"""
        return f"Personal context: {self.personal_context[:200]}..." if len(self.personal_context) > 200 else self.personal_context
    
    def clear_cache(self):
        """Clear response cache"""
        self.response_cache.clear()
        print("Response cache cleared, Mr. Bharadwaj Sir.")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        success_rate = 0
        if self.stats['total_requests'] > 0:
            success_rate = (self.stats['successful_responses'] / self.stats['total_requests']) * 100
        
        return {
            'total_requests': self.stats['total_requests'],
            'successful_responses': self.stats['successful_responses'],
            'failed_requests': self.stats['failed_requests'],
            'success_rate': success_rate,
            'average_response_time': self.stats['average_response_time'],
            'context_usage': self.stats['context_usage'],
            'cache_size': len(self.response_cache),
            'personal_context_length': len(self.personal_context)
        }
    
    def is_available(self) -> bool:
        """Check if Gemini model is available"""
        try:
            # Test with a simple request
            test_response = self.model.generate_content("Hello")
            return test_response is not None
        except Exception as e:
            print(f"Gemini model not available: {e}")
            return False
    
    def test_connection(self) -> bool:
        """Test connection to Gemini API"""
        try:
            response = self.model.generate_content("Test connection")
            return response is not None and response.text is not None
        except Exception as e:
            print(f"Gemini API connection test failed: {e}")
            return False

# Initialize the Gemini model
try:
    layer3_gemini_model = Layer3GeminiModel()
    print("Layer 3 Gemini model initialized successfully")
except Exception as e:
    print(f"Failed to initialize Layer 3 Gemini model: {e}")
    layer3_gemini_model = None
