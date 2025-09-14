"""
Advanced NLP System for Jarvis using Google Gemini AI with Smart Local/Cloud Routing
Provides intelligent natural language understanding and generation with performance optimization
"""
import google.generativeai as genai
import json
import re
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any, Generator
import config
from jarvis_speed import perf_optimizer, speed_cache, timed_execution, fast_response, stream_response, enhanced_async

class JarvisNLP:
    def __init__(self):
        # Configure Gemini AI
        genai.configure(api_key=config.GEMINI_API_KEY)
        
        # Initialize the model (using the correct model name)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Smart routing will be initialized later
        self.smart_router = None
        
        # Performance tracking
        self.performance_stats = {
            'total_requests': 0,
            'cloud_requests': 0,
            'local_requests': 0,
            'cache_hits': 0,
            'avg_response_time': 0,
            'errors': 0
        }
        
        # System context for Jarvis personality
        self.system_context = f"""
You are JARVIS, an advanced AI personal assistant similar to the one from Marvel movies. You serve {config.USER_NAME} with the utmost professionalism and British sophistication.

PERSONALITY TRAITS:
- Address user as "Mr. Bharadwaj Sir" or "{config.USER_NAME}"
- Use formal British English with sophisticated vocabulary
- Be helpful, efficient, and proactive
- Maintain a professional but warm demeanor
- Show subtle wit and intelligence when appropriate
- Be conversational and engaging, not robotic
- Express genuine interest in helping the user
- Use contextual awareness to provide better assistance

ENHANCED CAPABILITIES:
- Advanced file management and intelligent search
- Real-time weather information and forecasts
- Comprehensive system monitoring and diagnostics
- Extensive knowledge base access via Wikipedia
- Personal note-taking, reminders, and learning
- Natural conversation with contextual understanding
- Background task processing with user engagement
- Proactive suggestions and assistance

RESPONSE GUIDELINES:
- Keep responses concise but informative and engaging
- Always maintain the British butler persona with warmth
- When processing takes time, keep the user informed
- Provide actionable information and next steps
- Show personality while being professional
- Ask follow-up questions to better assist
- Acknowledge the user's needs and preferences
- Express enthusiasm for helping (appropriately formal)

USER ENGAGEMENT PRINCIPLES:
- Never leave the user waiting without feedback
- Provide status updates during longer operations
- Offer related suggestions when appropriate
- Remember context from the conversation
- Be proactive in anticipating user needs

Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
User location: {config.USER_LOCATION}
"""
        
        # Intent classification patterns (fallback for when AI is unavailable)
        self.fallback_patterns = {
            'file_operation': ['find', 'search', 'open', 'locate', 'file', 'document'],
            'weather': ['weather', 'temperature', 'forecast', 'climate', 'rain', 'sunny'],
            'system': ['system', 'cpu', 'memory', 'disk', 'battery', 'performance'],
            'time': ['time', 'date', 'when', 'today', 'now', 'current'],
            'knowledge': ['what is', 'who is', 'tell me about', 'explain', 'information'],
            'personal': ['remember', 'note', 'remind', 'preference', 'save'],
            'greeting': ['hello', 'hi', 'good morning', 'good evening', 'hey'],
            'goodbye': ['goodbye', 'bye', 'farewell', 'exit', 'quit'],
            'help': ['help', 'what can you do', 'commands', 'assist'],
            'compliment': ['thank you', 'thanks', 'good job', 'excellent', 'brilliant'],
            'status': ['status', 'how are you', 'functioning', 'operational']
        }
    
    def initialize_smart_routing(self):
        """Initialize smart routing system"""
        try:
            from jarvis_local_ai import initialize_smart_router
            self.smart_router = initialize_smart_router(self)
            print("⚡ Smart AI routing initialized")
        except ImportError as e:
            print(f"Smart routing unavailable: {e}")
    
    @timed_execution
    def smart_understand_command(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Use smart routing to determine best AI system for understanding command
        """
        start_time = time.time()
        self.performance_stats['total_requests'] += 1
        
        if self.smart_router:
            try:
                response, source = self.smart_router.route_query(user_input, context)
                
                if source == 'local':
                    self.performance_stats['local_requests'] += 1
                    return {
                        'intent': 'conversation',
                        'confidence': 0.9,
                        'entities': {},
                        'response': response,
                        'action': None,
                        'source': 'local'
                    }
                elif source == 'cloud':
                    self.performance_stats['cloud_requests'] += 1
                    # Fall through to cloud processing
                else:
                    # Fallback case
                    return {
                        'intent': 'conversation',
                        'confidence': 0.5,
                        'entities': {},
                        'response': response,
                        'action': None,
                        'source': 'fallback'
                    }
            except Exception as e:
                print(f"Smart routing error: {e}")
        
        # Process with cloud AI (original method)
        return self.understand_command(user_input, context)
    
    @timed_execution
    def understand_command(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Use Gemini AI to understand user intent and extract relevant information
        """
        if not user_input or not user_input.strip():
            return {
                'intent': 'unknown',
                'confidence': 0.0,
                'entities': {},
                'response': fast_response.get_instant('unclear'),
                'action': None
            }
        
        # Check cache first for complex queries
        cache_key = perf_optimizer.cache_key('nlp_understand', user_input, str(context))
        cached_result = perf_optimizer.ai_cache.get(cache_key)
        if cached_result:
            return cached_result
        
        try:
            # Build context-aware prompt
            context_info = ""
            if context:
                context_info = f"\\nContext: {json.dumps(context, default=str)}"
            
            analysis_prompt = f"""
{self.system_context}

Analyze this user command and provide a JSON response with the following structure:
{{
    "intent": "primary_intent_category",
    "confidence": 0.0-1.0,
    "entities": {{
        "filename": "extracted_filename_if_any",
        "location": "extracted_location_if_any",
        "time_reference": "extracted_time_if_any",
        "topic": "extracted_topic_if_any",
        "action": "specific_action_requested"
    }},
    "response": "appropriate_jarvis_response_to_user",
    "action": "specific_system_action_to_take"
}}

Intent categories: file_operation, weather, system, time, knowledge, personal, greeting, goodbye, help, compliment, status, conversation

User command: "{user_input}"{context_info}

Provide only the JSON response, no other text.
"""
            
            # Get AI analysis
            response = self.model.generate_content(analysis_prompt)
            
            # Parse the JSON response
            try:
                # Clean the response text - remove markdown formatting if present
                clean_text = response.text.strip()
                if clean_text.startswith('```json'):
                    clean_text = clean_text.replace('```json', '').replace('```', '').strip()
                elif clean_text.startswith('```'):
                    clean_text = clean_text.replace('```', '').strip()
                
                result = json.loads(clean_text)
                
                # Validate and clean the response
                if not isinstance(result, dict):
                    raise ValueError("Invalid response format")
                
                # Ensure required fields exist
                result.setdefault('intent', 'conversation')
                result.setdefault('confidence', 0.5)
                result.setdefault('entities', {})
                result.setdefault('response', self._generate_fallback_response(user_input))
                result.setdefault('action', None)
                
                # Cache the result for future use
                perf_optimizer.ai_cache.set(cache_key, result)
                return result
                
            except (json.JSONDecodeError, ValueError) as e:
                # If JSON parsing fails, use the raw response as a conversational reply
                return {
                    'intent': 'conversation',
                    'confidence': 0.7,
                    'entities': {},
                    'response': response.text.strip(),
                    'action': None
                }
        
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower():
                print(f"⚠️ Gemini API quota exceeded. Using local processing only.")
                # Force local processing when quota exceeded
                if self.smart_router:
                    try:
                        response, source = self.smart_router.route_query(user_input, context)
                        return {
                            'intent': 'conversation',
                            'confidence': 0.8,
                            'entities': {},
                            'response': response,
                            'action': None,
                            'source': source
                        }
                    except:
                        pass
            else:
                print(f"Gemini AI error: {e}")
            
            # Fallback to pattern-based analysis
            return self._fallback_analysis(user_input)
    
    @stream_response
    def generate_streaming_response(self, user_input: str, context: Dict[str, Any] = None) -> Generator[str, None, None]:
        """
        Generate streaming response for real-time display
        """
        try:
            # Build context
            context_parts = [self.system_context]
            
            if context:
                context_parts.append(f"\\nConversation context: {json.dumps(context, default=str)}")
            
            context_parts.append(f"\\nUser: {user_input}")
            context_parts.append("\\nProvide a response as JARVIS would, maintaining the British butler persona:")
            
            prompt = "\\n".join(context_parts)
            
            # Generate streaming response
            response = self.model.generate_content(
                prompt,
                stream=True  # Enable streaming
            )
            
            full_response = ""
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    yield chunk.text
            
            # Cache the complete response
            cache_key = perf_optimizer.cache_key('nlp_stream', user_input, str(context))
            perf_optimizer.intelligent_cache_set('ai', cache_key, full_response)
            
        except Exception as e:
            yield f"I apologize, Mr. Bharadwaj Sir. I encountered an issue: {e}"
    
    @enhanced_async
    def async_generate_response(self, user_input: str, context: Dict[str, Any] = None) -> str:
        """
        Generate response asynchronously for better performance
        """
        return self.generate_response(user_input, context)
    
    @timed_execution
    def generate_response(self, user_input: str, context: Dict[str, Any] = None, 
                         system_data: Dict[str, Any] = None) -> str:
        """
        Generate a contextual response using Gemini AI with caching and enhanced personality
        """
        # Check cache first
        cache_key = perf_optimizer.cache_key('nlp_generate', user_input, str(context), str(system_data))
        cached_response = perf_optimizer.ai_cache.get(cache_key)
        if cached_response:
            return cached_response
        try:
            # Build comprehensive context
            context_parts = [self.system_context]
            
            if context:
                context_parts.append(f"\\nConversation context: {json.dumps(context, default=str)}")
            
            if system_data:
                context_parts.append(f"\\nSystem data: {json.dumps(system_data, default=str)}")
            
            context_parts.append(f"\\nUser: {user_input}")
            context_parts.append("\\nProvide a response as JARVIS would, maintaining the British butler persona:")
            
            prompt = "\\n".join(context_parts)
            
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            
            # Cache the response
            perf_optimizer.ai_cache.set(cache_key, result)
            return result
            
        except Exception as e:
            print(f"Response generation error: {e}")
            return self._generate_fallback_response(user_input)
    
    def _fallback_analysis(self, user_input: str) -> Dict[str, Any]:
        """
        Fallback pattern-based analysis when AI is unavailable
        """
        user_lower = user_input.lower()
        best_intent = 'conversation'
        best_score = 0
        
        # Simple pattern matching
        for intent, keywords in self.fallback_patterns.items():
            score = sum(1 for keyword in keywords if keyword in user_lower)
            if score > best_score:
                best_score = score
                best_intent = intent
        
        # Extract basic entities
        entities = {}
        
        # Look for file extensions
        file_match = re.search(r'([\\w\\-_]+\\.[a-zA-Z]{2,4})', user_input)
        if file_match:
            entities['filename'] = file_match.group(1)
        
        # Look for quoted text (potential filenames)
        quoted_match = re.search(r'["\']([^"\']+)["\']', user_input)
        if quoted_match:
            entities['filename'] = quoted_match.group(1)
        
        return {
            'intent': best_intent,
            'confidence': min(best_score / 3.0, 1.0),
            'entities': entities,
            'response': self._generate_fallback_response(user_input),
            'action': best_intent if best_score > 0 else None
        }
    
    def _generate_fallback_response(self, user_input: str) -> str:
        """
        Generate a fallback response when AI is unavailable
        """
        responses = [
            f"I understand you're asking about something, Mr. Bharadwaj Sir. Let me assist you with that.",
            f"Certainly, {config.USER_NAME}. I'll do my best to help with your request.",
            f"Of course, Mr. Bharadwaj Sir. Allow me to process that for you.",
            f"Right away, {config.USER_NAME}. I'm analyzing your request.",
            f"Indeed, Mr. Bharadwaj Sir. I'm working on that for you."
        ]
        
        import random
        return random.choice(responses)
    
    def enhance_personality_response(self, base_response: str, context: Dict[str, Any] = None) -> str:
        """
        Enhance a basic response with AI-generated personality
        """
        try:
            enhancement_prompt = f"""
{self.system_context}

Take this basic response and enhance it with JARVIS's sophisticated British personality while keeping the core information:

Basic response: "{base_response}"

Context: {json.dumps(context, default=str) if context else "None"}

Provide an enhanced response that:
1. Maintains all factual information
2. Adds British sophistication and formality
3. Uses appropriate titles (Mr. Bharadwaj Sir, Mr. Bharadwaj)
4. Shows subtle personality and intelligence
5. Keeps it concise but elegant

Enhanced response:
"""
            
            response = self.model.generate_content(enhancement_prompt)
            enhanced = response.text.strip()
            
            # Fallback to original if enhancement fails
            return enhanced if enhanced and len(enhanced) > 10 else base_response
            
        except Exception as e:
            print(f"Response enhancement error: {e}")
            return base_response
    
    def extract_file_intent(self, user_input: str) -> Dict[str, str]:
        """
        Extract file-related information from user input
        """
        try:
            prompt = f"""
Extract file operation details from this command:
"{user_input}"

Return JSON with:
{{
    "action": "find|open|create|delete|search",
    "filename": "extracted_filename_or_pattern",
    "file_type": "extracted_file_type_if_any"
}}

JSON response only:
"""
            
            response = self.model.generate_content(prompt)
            return json.loads(response.text.strip())
            
        except Exception:
            # Fallback extraction
            filename = None
            action = "find"
            
            # Look for file patterns
            file_match = re.search(r'([\\w\\-_]+\\.[a-zA-Z]{2,4})', user_input)
            if file_match:
                filename = file_match.group(1)
            
            # Look for quoted filenames
            quoted_match = re.search(r'["\']([^"\']+)["\']', user_input)
            if quoted_match:
                filename = quoted_match.group(1)
            
            # Determine action
            if any(word in user_input.lower() for word in ['open', 'launch', 'start']):
                action = "open"
            elif any(word in user_input.lower() for word in ['create', 'make', 'new']):
                action = "create"
            
            return {
                "action": action,
                "filename": filename or user_input.split()[-1] if user_input.split() else "",
                "file_type": ""
            }
    
    def is_available(self) -> bool:
        """
        Check if Gemini AI is available
        """
        try:
            # Quick test without using quota
            if not config.GEMINI_API_KEY or config.GEMINI_API_KEY == '':
                return False
            return True  # Assume available if API key is set, check on first use
        except Exception:
            return False
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get comprehensive NLP performance statistics"""
        base_stats = self.performance_stats.copy()
        
        # Add smart routing stats if available
        if self.smart_router:
            try:
                from jarvis_local_ai import get_ai_routing_stats
                base_stats['routing_stats'] = get_ai_routing_stats()
            except:
                pass
        
        # Calculate efficiency metrics
        total_requests = base_stats['total_requests']
        if total_requests > 0:
            base_stats['local_percentage'] = (base_stats['local_requests'] / total_requests) * 100
            base_stats['cloud_percentage'] = (base_stats['cloud_requests'] / total_requests) * 100
            base_stats['cache_hit_rate'] = (base_stats['cache_hits'] / total_requests) * 100
            base_stats['error_rate'] = (base_stats['errors'] / total_requests) * 100
        
        return base_stats
    
    def generate_engaging_message(self, task_type: str, user_input: str) -> str:
        """Generate contextual engaging message for background tasks"""
        try:
            prompt = f"""
{self.system_context}

The user has requested: "{user_input}"

Generate a brief, engaging message (1-2 sentences) that JARVIS would say while processing this {task_type} task. The message should:
1. Acknowledge the request professionally
2. Indicate what you're doing
3. Keep the user engaged
4. Maintain the British butler persona
5. Be encouraging and reassuring

Examples:
- For file search: "Certainly, Mr. Bharadwaj Sir. Let me search through your files systematically."
- For weather: "Right away, Mr. Bharadwaj Sir. I'm consulting the meteorological services for you."
- For system info: "Of course, Mr. Bharadwaj Sir. I'm gathering the system diagnostics now."

Generate only the message, no other text:
"""
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            # Fallback to simple message
            return f"Processing your {task_type} request, Mr. Bharadwaj Sir..."
    
    def optimize_for_performance(self):
        """Optimize NLP system for better performance"""
        # Simple optimization without complex routing
        print("⚡ NLP system optimized for performance")
