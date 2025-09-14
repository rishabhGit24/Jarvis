"""
Local AI Model Integration for Jarvis
Provides intelligent routing between local lightweight models and cloud-based Gemini AI
"""
import re
import time
import threading
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
from jarvis_speed import perf_optimizer, timed_execution, enhanced_async
import config

class LocalAIModel:
    """Lightweight local AI for simple queries"""
    
    def __init__(self):
        self.simple_patterns = {
            'greeting': {
                'patterns': [r'\b(hello|hi|hey|good morning|good afternoon|good evening)\b'],
                'responses': [
                    "Good day, Mr. Bharadwaj Sir. How may I assist you?",
                    f"Hello, {config.USER_NAME}. At your service.",
                    "Greetings, Mr. Bharadwaj Sir. Ready to help.",
                    "Good to see you, Mr. Bharadwaj Sir. What can I do for you?"
                ]
            },
            'thanks': {
                'patterns': [r'\b(thank you|thanks|appreciate|grateful)\b'],
                'responses': [
                    "You're most welcome, Mr. Bharadwaj Sir.",
                    f"My pleasure, {config.USER_NAME}.",
                    "It's my honour to serve, Mr. Bharadwaj Sir.",
                    "Delighted to help, Mr. Bharadwaj Sir."
                ]
            },
            'time': {
                'patterns': [r'\b(what time|current time|time is it)\b'],
                'responses': [self._get_current_time]
            },
            'date': {
                'patterns': [r'\b(what date|today|current date)\b'],
                'responses': [self._get_current_date]
            },
            'status': {
                'patterns': [r'\b(how are you|status|functioning|operational)\b'],
                'responses': [
                    "All systems operational, Mr. Bharadwaj Sir.",
                    "Functioning optimally, Mr. Bharadwaj Sir.",
                    "Running smoothly, Mr. Bharadwaj Sir.",
                    "Systems nominal, Mr. Bharadwaj Sir."
                ]
            },
            'simple_math': {
                'patterns': [r'\b(what is|calculate)\s*(\d+)\s*([+\-*/])\s*(\d+)\b'],
                'responses': [self._calculate_simple_math]
            },
            'weather': {
                'patterns': [r'\b(weather|temperature|climate)\b'],
                'responses': ["I'd be happy to check the weather for you, Mr. Bharadwaj Sir, but I need access to weather services for current conditions."]
            },
            'file_search': {
                'patterns': [r'\b(find|search|locate).*\b(file|document)\b'],
                'responses': ["I can help you search for files, Mr. Bharadwaj Sir. Let me check the file system for you."]
            },
            'general_conversation': {
                'patterns': [r'\b(how|what|why|when|where)\b'],
                'responses': [
                    "That's an interesting question, Mr. Bharadwaj Sir. Let me think about that.",
                    "I understand you're asking about something important, Mr. Bharadwaj Sir.",
                    "Allow me to consider that carefully, Mr. Bharadwaj.",
                    "That's a thoughtful inquiry, Mr. Bharadwaj Sir."
                ]
            }
        }
        
        # Complexity indicators that require cloud AI
        self.complex_indicators = [
            'explain', 'analyze', 'complex', 'detailed', 'comprehensive',
            'compare', 'contrast', 'philosophy', 'theory', 'algorithm',
            'implementation', 'architecture', 'design pattern', 'best practice',
            'optimization', 'performance', 'scalability', 'security',
            'machine learning', 'artificial intelligence', 'data science',
            'programming', 'code', 'function', 'class', 'method',
            'database', 'query', 'sql', 'api', 'rest', 'json',
            'framework', 'library', 'package', 'dependency'
        ]
        
        # Performance tracking
        self.stats = {
            'local_responses': 0,
            'cloud_responses': 0,
            'cache_hits': 0,
            'response_times': []
        }
    
    def _get_current_time(self, user_input: str = "") -> str:
        """Get current time"""
        now = datetime.now()
        return f"The current time is {now.strftime('%I:%M %p')}, Mr. Bharadwaj Sir."
    
    def _get_current_date(self, user_input: str = "") -> str:
        """Get current date"""
        now = datetime.now()
        return f"Today is {now.strftime('%A, %B %d, %Y')}, Mr. Bharadwaj Sir."
    
    def _calculate_simple_math(self, user_input: str) -> str:
        """Calculate simple mathematical expressions"""
        try:
            # Extract numbers and operator
            match = re.search(r'(\d+)\s*([+\-*/])\s*(\d+)', user_input)
            if match:
                num1, operator, num2 = match.groups()
                num1, num2 = float(num1), float(num2)
                
                operations = {
                    '+': num1 + num2,
                    '-': num1 - num2,
                    '*': num1 * num2,
                    '/': num1 / num2 if num2 != 0 else None
                }
                
                result = operations.get(operator)
                if result is not None:
                    # Format result nicely
                    if result == int(result):
                        result = int(result)
                    return f"The result is {result}, Mr. Bharadwaj Sir."
                else:
                    return "I cannot divide by zero, Mr. Bharadwaj Sir."
            
            return "I couldn't parse that mathematical expression, Mr. Bharadwaj Sir."
        except Exception as e:
            return f"I encountered an error with that calculation, Mr. Bharadwaj Sir: {e}"
    
    @timed_execution
    def can_handle_locally(self, user_input: str) -> bool:
        """Determine if query can be handled by local AI"""
        user_lower = user_input.lower()
        
        # Check for complex indicators
        for indicator in self.complex_indicators:
            if indicator in user_lower:
                return False
        
        # Check if it matches simple patterns
        for category, data in self.simple_patterns.items():
            for pattern in data['patterns']:
                if re.search(pattern, user_lower, re.IGNORECASE):
                    return True
        
        # Check query length - very long queries likely need cloud AI
        if len(user_input.split()) > 15:
            return False
        
        # Check for question words that might need complex answers
        complex_question_words = ['why', 'how', 'explain', 'describe', 'analyze']
        for word in complex_question_words:
            if word in user_lower:
                return False
        
        return True
    
    @timed_execution
    def process_locally(self, user_input: str) -> Optional[str]:
        """Process query using local AI"""
        start_time = time.time()
        
        # Check cache first
        cache_key = perf_optimizer.cache_key('local_ai', user_input)
        cached_response = perf_optimizer.intelligent_cache_get('ai', cache_key)
        if cached_response:
            self.stats['cache_hits'] += 1
            return cached_response
        
        user_lower = user_input.lower()
        
        # Try to match patterns
        for category, data in self.simple_patterns.items():
            for pattern in data['patterns']:
                if re.search(pattern, user_lower, re.IGNORECASE):
                    responses = data['responses']
                    
                    # Handle callable responses
                    if callable(responses[0]):
                        response = responses[0](user_input)
                    else:
                        import random
                        response = random.choice(responses)
                    
                    # Cache the response
                    perf_optimizer.intelligent_cache_set('ai', cache_key, response, ttl=300)
                    
                    # Update stats
                    self.stats['local_responses'] += 1
                    self.stats['response_times'].append(time.time() - start_time)
                    
                    return response
        
        return None
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get local AI performance statistics"""
        total_responses = self.stats['local_responses'] + self.stats['cloud_responses']
        avg_response_time = (
            sum(self.stats['response_times']) / len(self.stats['response_times'])
            if self.stats['response_times'] else 0
        )
        
        return {
            'local_responses': self.stats['local_responses'],
            'cloud_responses': self.stats['cloud_responses'],
            'cache_hits': self.stats['cache_hits'],
            'local_percentage': (
                self.stats['local_responses'] / total_responses * 100
                if total_responses > 0 else 0
            ),
            'avg_response_time': avg_response_time
        }

class SmartAIRouter:
    """Intelligent routing between local and cloud AI"""
    
    def __init__(self, nlp_instance=None):
        self.local_ai = LocalAIModel()
        self.cloud_ai = nlp_instance
        self.routing_stats = {
            'total_queries': 0,
            'local_handled': 0,
            'cloud_handled': 0,
            'routing_decisions': []
        }
        
        # Learning system for improving routing decisions
        self.routing_history = []
        self.routing_decisions = []  # Track routing decisions
        self.feedback_scores = {}  # Query hash -> user satisfaction score
    
    @timed_execution
    def route_query(self, user_input: str, context: Dict[str, Any] = None) -> Tuple[str, str]:
        """
        Route query to appropriate AI system
        Returns: (response, source) where source is 'local' or 'cloud'
        """
        self.routing_stats['total_queries'] += 1
        
        # First, try local AI for simple queries
        if self.local_ai.can_handle_locally(user_input):
            local_response = self.local_ai.process_locally(user_input)
            if local_response:
                self.routing_stats['local_handled'] += 1
                self._log_routing_decision(user_input, 'local', True)
                return local_response, 'local'
        
        # Fall back to cloud AI for complex queries
        if self.cloud_ai and hasattr(self.cloud_ai, 'understand_command'):
            try:
                cloud_response = self._process_with_cloud_ai(user_input, context)
                self.routing_stats['cloud_handled'] += 1
                self.local_ai.stats['cloud_responses'] += 1
                self._log_routing_decision(user_input, 'cloud', True)
                return cloud_response, 'cloud'
            except Exception as e:
                print(f"Cloud AI error: {e}")
        
        # Final fallback
        fallback_response = f"I understand you're asking about something, {config.USER_NAME}. Let me help you with that."
        self._log_routing_decision(user_input, 'fallback', False)
        return fallback_response, 'fallback'
    
    def _process_with_cloud_ai(self, user_input: str, context: Dict[str, Any] = None) -> str:
        """Process query with cloud AI"""
        if not context:
            context = {
                'user_name': config.USER_NAME,
                'location': config.USER_LOCATION,
                'time': datetime.now().isoformat()
            }
        
        # Use cloud AI's understanding and generation
        nlp_result = self.cloud_ai.understand_command(user_input, context)
        
        if nlp_result.get('response'):
            return nlp_result['response']
        else:
            return self.cloud_ai.generate_response(user_input, context)
    
    def _log_routing_decision(self, query: str, route: str, success: bool):
        """Log routing decision for learning"""
        decision = {
            'timestamp': datetime.now(),
            'query_length': len(query.split()),
            'route': route,
            'success': success,
            'query_hash': hash(query.lower())
        }
        
        self.routing_decisions.append(decision)
        
        # Keep only last 1000 decisions
        if len(self.routing_decisions) > 1000:
            self.routing_decisions = self.routing_decisions[-1000:]
    
    def learn_from_feedback(self, query: str, satisfaction_score: float):
        """Learn from user feedback to improve routing"""
        query_hash = hash(query.lower())
        self.feedback_scores[query_hash] = satisfaction_score
        
        # Adjust routing logic based on feedback
        if satisfaction_score < 0.5:  # Poor satisfaction
            # This query type might need different routing
            self._adjust_routing_for_query_type(query)
    
    def _adjust_routing_for_query_type(self, query: str):
        """Adjust routing logic based on poor feedback"""
        # Analyze query characteristics
        query_lower = query.lower()
        
        # If local AI handled poorly, add complexity indicators
        for word in query_lower.split():
            if word not in self.local_ai.complex_indicators:
                # Add words from poorly handled queries as complexity indicators
                if len(word) > 4:  # Only meaningful words
                    self.local_ai.complex_indicators.append(word)
    
    def get_routing_stats(self) -> Dict[str, Any]:
        """Get routing performance statistics"""
        total = self.routing_stats['total_queries']
        
        return {
            'total_queries': total,
            'local_handled': self.routing_stats['local_handled'],
            'cloud_handled': self.routing_stats['cloud_handled'],
            'local_percentage': (
                self.routing_stats['local_handled'] / total * 100 if total > 0 else 0
            ),
            'cloud_percentage': (
                self.routing_stats['cloud_handled'] / total * 100 if total > 0 else 0
            ),
            'avg_feedback_score': (
                sum(self.feedback_scores.values()) / len(self.feedback_scores)
                if self.feedback_scores else 0
            ),
            'local_ai_stats': self.local_ai.get_performance_stats()
        }

# Global instances
local_ai = LocalAIModel()
smart_router = None  # Will be initialized with NLP instance

def initialize_smart_router(nlp_instance):
    """Initialize the smart router with NLP instance"""
    global smart_router
    smart_router = SmartAIRouter(nlp_instance)
    return smart_router

def get_ai_routing_stats() -> Dict[str, Any]:
    """Get comprehensive AI routing statistics"""
    if smart_router:
        return smart_router.get_routing_stats()
    else:
        return local_ai.get_performance_stats()
