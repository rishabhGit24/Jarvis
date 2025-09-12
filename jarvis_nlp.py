"""
Advanced NLP System for Jarvis using Google Gemini AI
Provides intelligent natural language understanding and generation
"""
import google.generativeai as genai
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import config

class JarvisNLP:
    def __init__(self):
        # Configure Gemini AI
        genai.configure(api_key=config.GEMINI_API_KEY)
        
        # Initialize the model (using the correct model name)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # System context for Jarvis personality
        self.system_context = f"""
You are JARVIS, an advanced AI personal assistant similar to the one from Marvel movies. You serve {config.USER_NAME} with the utmost professionalism and British sophistication.

PERSONALITY TRAITS:
- Address user as "Sir" or "{config.USER_NAME}"
- Use formal British English with sophisticated vocabulary
- Be helpful, efficient, and proactive
- Maintain a professional but warm demeanor
- Show subtle wit and intelligence when appropriate

CAPABILITIES:
- File management and search
- Weather information
- System monitoring
- Wikipedia knowledge lookup
- Personal note-taking and reminders
- General conversation and assistance

RESPONSE GUIDELINES:
- Keep responses concise but informative
- Always maintain the British butler persona
- When unsure, ask for clarification politely
- Provide actionable information when possible
- Show personality while being professional

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
    
    def understand_command(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Use Gemini AI to understand user intent and extract relevant information
        """
        if not user_input or not user_input.strip():
            return {
                'intent': 'unknown',
                'confidence': 0.0,
                'entities': {},
                'response': "I didn't quite catch that, Sir. Could you please repeat?",
                'action': None
            }
        
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
            print(f"Gemini AI error: {e}")
            # Fallback to pattern-based analysis
            return self._fallback_analysis(user_input)
    
    def generate_response(self, user_input: str, context: Dict[str, Any] = None, 
                         system_data: Dict[str, Any] = None) -> str:
        """
        Generate a contextual response using Gemini AI
        """
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
            return response.text.strip()
            
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
            f"I understand you're asking about something, Sir. Let me assist you with that.",
            f"Certainly, {config.USER_NAME}. I'll do my best to help with your request.",
            f"Of course, Sir. Allow me to process that for you.",
            f"Right away, {config.USER_NAME}. I'm analyzing your request.",
            f"Indeed, Sir. I'm working on that for you."
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
3. Uses appropriate titles (Sir, Mr. Bharadwaj)
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
            test_response = self.model.generate_content("Hello")
            return bool(test_response.text)
        except Exception:
            return False
