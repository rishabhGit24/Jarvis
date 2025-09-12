"""
Jarvis Intelligence and Personality System
Handles natural language processing, command interpretation, and personality responses
"""
import re
import random
import subprocess
import platform
import psutil
import wikipedia
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import config
from jarvis_memory import JarvisMemory
from jarvis_files import JarvisFileManager
from jarvis_weather import JarvisWeather
from jarvis_nlp import JarvisNLP

class JarvisBrain:
    def __init__(self):
        self.memory = JarvisMemory()
        self.file_manager = JarvisFileManager()
        self.weather = JarvisWeather()
        self.nlp = JarvisNLP()
        self.conversation_active = False
        self.use_ai_nlp = True  # Flag to enable/disable AI NLP

        # Command patterns for natural language processing
        self.command_patterns = {
            'greeting': [
                r'hello|hi|hey|good morning|good afternoon|good evening|greetings',
                self._handle_greeting
            ],
            'file_find': [
                r'find|search|locate|look for.*file|open.*file|where is.*file',
                self._handle_file_search
            ],
            'file_open': [
                r'open|launch|start|run',
                self._handle_file_open
            ],
            'weather': [
                r'weather|temperature|forecast|climate|how.*outside',
                self._handle_weather
            ],
            'system_info': [
                r'system|computer|performance|cpu|memory|disk|battery',
                self._handle_system_info
            ],
            'time_date': [
                r'time|date|what.*day|when.*today|current.*time',
                self._handle_time_date
            ],
            'wikipedia': [
                r'what is|who is|tell me about|information about|wikipedia',
                self._handle_wikipedia_search
            ],
            'personal': [
                r'remember|note|personal|about me|my preference',
                self._handle_personal_info
            ],
            'help': [
                r'help|what can you do|commands|capabilities|assist',
                self._handle_help
            ],
            'goodbye': [
                r'goodbye|bye|see you|farewell|exit|quit|stop',
                self._handle_goodbye
            ],
            'compliment': [
                r'thank you|thanks|good job|well done|excellent|brilliant',
                self._handle_compliment
            ],
            'status': [
                r'status|how are you|are you okay|functioning|operational',
                self._handle_status
            ]
        }

        # Personality responses
        self.personality_responses = {
            'acknowledgments': [
                "Certainly, Sir.",
                "Of course, Mr. Bharadwaj.",
                "Right away, Sir.",
                "At once, Sir.",
                "Very good, Sir.",
                "Indeed, Sir.",
                "Understood, Sir."
            ],
            'apologies': [
                "I do apologize, Sir.",
                "My sincere apologies, Mr. Bharadwaj.",
                "I'm terribly sorry, Sir.",
                "Forgive me, Sir.",
                "I regret the inconvenience, Sir."
            ],
            'confirmations': [
                "Task completed successfully, Sir.",
                "Done, Mr. Bharadwaj.",
                "All finished, Sir.",
                "Task accomplished, Sir.",
                "Completed as requested, Sir."
            ],
            'thinking': [
                "Let me check that for you, Sir.",
                "One moment please, Mr. Bharadwaj.",
                "Allow me to investigate, Sir.",
                "Searching now, Sir.",
                "Processing your request, Sir."
            ]
        }

    def process_command(self, user_input: str) -> str:
        """Process user input and return appropriate response using AI NLP or fallback patterns"""
        if not user_input or not user_input.strip():
            return "I didn't quite catch that, Sir. Could you please repeat?"

        original_input = user_input.strip()

        # Try AI NLP first if enabled and available
        if self.use_ai_nlp and hasattr(self.nlp, 'is_available') and self.nlp.is_available():
            try:
                # Get conversation context from memory
                context = {
                    'user_name': config.USER_NAME,
                    'location': config.USER_LOCATION,
                    'time': datetime.now().isoformat(),
                    'recent_interactions': self.memory.memory_data.get('conversation_history', [])[-3:]
                }

                # Use AI to understand the command
                nlp_result = self.nlp.understand_command(original_input, context)

                # Route to appropriate handler based on AI intent
                response = self._handle_ai_intent(nlp_result, original_input)

                # Log interaction
                self.memory.add_conversation(original_input, response)
                self.memory.learn_from_interaction(original_input, nlp_result.get('intent', 'conversation'))

                return response

            except Exception as e:
                print(f"AI NLP error, falling back to pattern matching: {e}")
        # Fallback to original pattern-based processing
        user_input_lower = original_input.lower()

        # Check for command patterns
        for command_type, (pattern, handler) in self.command_patterns.items():
            if re.search(pattern, user_input_lower, re.IGNORECASE):
                try:
                    response = handler(original_input)
                    # Enhance response with AI if available
                    if self.use_ai_nlp:
                        try:
                            response = self.nlp.enhance_personality_response(response, {
                                'command_type': command_type,
                                'user_input': original_input
                            })
                        except Exception:
                            pass  # Use original response if enhancement fails

                    self.memory.add_conversation(original_input, response)
                    self.memory.learn_from_interaction(original_input, command_type)
                    return response
                except Exception as e:
                    error_response = f"I encountered an issue while processing your request, Sir. {str(e)}"
                    self.memory.add_conversation(original_input, error_response)
                    return error_response

        # If no pattern matches, try AI conversation or fallback
        return self._handle_unknown_command(original_input)

    def _handle_greeting(self, user_input: str) -> str:
        """Handle greeting commands"""
        greeting = self.memory.get_personalized_greeting()

        # Add context based on time and recent activity
        now = datetime.now()
        if now.hour < 12:
            if "morning" not in greeting.lower():
                greeting += " I trust you're ready for a productive day ahead?"
        elif now.hour >= 18:
            if "evening" not in greeting.lower():
                greeting += " How may I assist you this evening?"

        return greeting

    def _handle_ai_intent(self, nlp_result: Dict[str, Any], user_input: str) -> str:
        """Handle commands processed by AI NLP"""
        intent = nlp_result.get('intent', 'conversation')
        entities = nlp_result.get('entities', {})
        ai_response = nlp_result.get('response', '')

        # Route to appropriate handler based on AI-determined intent
        if intent == 'file_operation':
            if entities.get('filename'):
                if 'open' in user_input.lower():
                    return self._handle_file_open(user_input, entities)
                else:
                    return self._handle_file_search(user_input, entities)
            else:
                return ai_response or "What file would you like me to help you with, Sir?"

        elif intent == 'weather':
            location = entities.get('location')
            return self._handle_weather(user_input, location)

        elif intent == 'system':
            return self._handle_system_info(user_input)

        elif intent == 'time':
            return self._handle_time_date(user_input)

        elif intent == 'knowledge':
            topic = entities.get('topic')
            if topic:
                return self._handle_wikipedia_search(f"what is {topic}")
            else:
                return ai_response or self._handle_wikipedia_search(user_input)

        elif intent == 'personal':
            return self._handle_personal_info(user_input)

        elif intent == 'greeting':
            return self._handle_greeting(user_input)

        elif intent == 'goodbye':
            return self._handle_goodbye(user_input)

        elif intent == 'help':
            return self._handle_help(user_input)

        elif intent == 'compliment':
            return self._handle_compliment(user_input)

        elif intent == 'status':
            return self._handle_status(user_input)

        else:
            # For conversation or unknown intents, use AI response
            if ai_response and len(ai_response.strip()) > 0:
                return ai_response
            else:
                # Generate a conversational response using AI
                try:
                    context = {
                        'user_name': config.USER_NAME,
                        'intent': intent,
                        'entities': entities
                    }
                    return self.nlp.generate_response(user_input, context)
                except Exception:
                    return self._handle_unknown_command(user_input)

    def _handle_file_search(self, user_input: str, entities: Dict[str, Any] = None) -> str:
        """Handle file search commands"""
        # Try to get filename from AI entities first
        filename = None
        if entities and entities.get('filename'):
            filename = entities['filename']
        else:
            # Fallback to pattern extraction
            filename_patterns = [
                r'find\s+(.+?)(?:\s+file)?$',
                r'search\s+(?:for\s+)?(.+?)(?:\s+file)?$',
                r'locate\s+(.+?)(?:\s+file)?$',
                r'look\s+for\s+(.+?)(?:\s+file)?$',
                r'where\s+is\s+(.+?)(?:\s+file)?$'
            ]

            for pattern in filename_patterns:
                match = re.search(pattern, user_input, re.IGNORECASE)
                if match:
                    filename = match.group(1).strip()
                    break

        if not filename:
            return "I need to know what file you're looking for, Sir. Please specify the filename."

        # Search for files
        thinking_response = random.choice(self.personality_responses['thinking'])
        files = self.file_manager.find_files(filename)

        if not files:
            return f"I'm afraid I couldn't locate any files matching '{filename}', Sir. Perhaps it's in a different location?"

        if len(files) == 1:
            file_info = self.file_manager.get_file_info(files[0])
            self.memory.track_file_access(files[0])
            return f"I found the file, Sir: {file_info['name']} located at {files[0]}. Would you like me to open it?"

        # Multiple files found
        response = f"I found {len(files)} files matching '{filename}', Sir:\\n"
        for i, file_path in enumerate(files[:5], 1):
            file_info = self.file_manager.get_file_info(file_path)
            response += f"{i}. {file_info['name']} - {file_path}\\n"

        if len(files) > 5:
            response += f"... and {len(files) - 5} more files."

        return response

    def _handle_file_open(self, user_input: str, entities: Dict[str, Any] = None) -> str:
        """Handle file open commands"""
        # Try to get filename from AI entities first
        filename = None
        if entities and entities.get('filename'):
            filename = entities['filename']
        else:
            # Fallback to pattern extraction
            open_patterns = [
                r'open\s+(.+?)(?:\s+file)?$',
                r'launch\s+(.+?)(?:\s+file)?$',
                r'start\s+(.+?)(?:\s+file)?$',
                r'run\s+(.+?)(?:\s+file)?$'
            ]

            for pattern in open_patterns:
                match = re.search(pattern, user_input, re.IGNORECASE)
                if match:
                    filename = match.group(1).strip()
                    break

        if not filename:
            # Check recent files
            recent_files = self.file_manager.get_recent_files()
            if recent_files:
                if self.file_manager.open_file(recent_files[0]):
                    return f"Opening your most recent file, Sir: {recent_files[0]}"
            return "Which file would you like me to open, Sir?"

        # Search and open file
        files = self.file_manager.find_files(filename)
        if not files:
            return f"I couldn't find a file named '{filename}', Sir."

        if self.file_manager.open_file(files[0]):
            self.memory.track_file_access(files[0])
            return f"Opening {files[0]}, Sir."
        else:
            return f"I encountered an issue opening the file, Sir."

    def _handle_weather(self, user_input: str, location: str = None) -> str:
        """Handle weather-related commands"""
        # Use provided location or try to extract from input
        if not location:
            location_match = re.search(r'(?:in|for|at)\s+([a-zA-Z\s,]+)', user_input)
            location = location_match.group(1).strip() if location_match else None

        if 'forecast' in user_input:
            forecast = self.weather.get_weather_forecast(location)
            if 'error' in forecast:
                return forecast['error']

            response = f"Here's the weather forecast for {forecast['location']}, Sir:\\n"
            for day in forecast['forecasts'][:3]:  # Show 3 days
                response += f"{day['date']}: {day['description']}, High {day['high_temp']}, Low {day['low_temp']}\\n"
            return response
        else:
            return self.weather.get_weather_summary(location)

    def _handle_system_info(self, user_input: str) -> str:
        """Handle system information requests"""
        try:
            if 'cpu' in user_input or 'processor' in user_input:
                cpu_percent = psutil.cpu_percent(interval=1)
                return f"CPU usage is currently at {cpu_percent}%, Sir."

            elif 'memory' in user_input or 'ram' in user_input:
                memory = psutil.virtual_memory()
                return f"Memory usage: {memory.percent}% of {memory.total // (1024**3)} GB, Sir."

            elif 'disk' in user_input or 'storage' in user_input:
                disk = psutil.disk_usage('/')
                used_gb = disk.used // (1024**3)
                total_gb = disk.total // (1024**3)
                return f"Disk usage: {used_gb} GB of {total_gb} GB used ({disk.percent:.1f}%), Sir."

            elif 'battery' in user_input:
                try:
                    battery = psutil.sensors_battery()
                    if battery:
                        status = "charging" if battery.power_plugged else "discharging"
                        return f"Battery is at {battery.percent:.1f}% and {status}, Sir."
                    else:
                        return "No battery information available, Sir. This appears to be a desktop system."
                except:
                    return "Battery information is not available on this system, Sir."

            else:
                # General system info
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                boot_time = datetime.fromtimestamp(psutil.boot_time())
                uptime = datetime.now() - boot_time

                response = f"System status, Sir:\\n"
                response += f"• CPU: {cpu_percent}%\\n"
                response += f"• Memory: {memory.percent}%\\n"
                response += f"• Uptime: {uptime.days} days, {uptime.seconds//3600} hours\\n"
                response += f"• Platform: {platform.system()} {platform.release()}"

                return response

        except Exception as e:
            return f"I encountered an issue retrieving system information, Sir: {str(e)}"

    def _handle_time_date(self, user_input: str) -> str:
        """Handle time and date requests"""
        now = datetime.now()

        if 'time' in user_input:
            return f"The current time is {now.strftime('%I:%M %p')}, Sir."
        elif 'date' in user_input:
            return f"Today is {now.strftime('%A, %B %d, %Y')}, Sir."
        else:
            return f"It is currently {now.strftime('%I:%M %p on %A, %B %d, %Y')}, Sir."

    def _handle_wikipedia_search(self, user_input: str) -> str:
        """Handle Wikipedia search requests"""
        # Extract search term
        patterns = [
            r'what is\s+(.+)',
            r'who is\s+(.+)',
            r'tell me about\s+(.+)',
            r'information about\s+(.+)',
            r'wikipedia\s+(.+)'
        ]

        search_term = None
        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                search_term = match.group(1).strip()
                break

        if not search_term:
            return "What would you like me to look up for you, Sir?"

        try:
            # Search Wikipedia
            summary = wikipedia.summary(search_term, sentences=3)
            return f"According to Wikipedia, Sir: {summary}"
        except wikipedia.exceptions.DisambiguationError as e:
            options = e.options[:3]
            return f"There are multiple entries for '{search_term}', Sir. Did you mean: {', '.join(options)}?"
        except wikipedia.exceptions.PageError:
            return f"I couldn't find any information about '{search_term}' on Wikipedia, Sir."
        except Exception as e:
            return f"I encountered an issue searching Wikipedia, Sir: {str(e)}"

    def _handle_personal_info(self, user_input: str) -> str:
        """Handle personal information and preferences"""
        if 'remember' in user_input or 'note' in user_input:
            # Extract what to remember
            remember_match = re.search(r'remember\s+(?:that\s+)?(.+)', user_input, re.IGNORECASE)
            note_match = re.search(r'note\s+(?:that\s+)?(.+)', user_input, re.IGNORECASE)

            if remember_match:
                info = remember_match.group(1).strip()
                self.memory.add_personal_note("user_preference", info)
                return f"I've made a note of that, Sir: {info}"
            elif note_match:
                info = note_match.group(1).strip()
                self.memory.add_personal_note("personal_note", info)
                return f"Noted, Sir: {info}"

        # Return personal context
        context = self.memory.get_user_context()
        if context.strip():
            return f"Here's what I know about you, Sir:\\n{context}"
        else:
            return "I'm still learning about your preferences, Sir. Feel free to tell me anything you'd like me to remember."

    def _handle_help(self, user_input: str) -> str:
        """Handle help requests"""
        help_text = """I'm at your service, Sir. Here's what I can assist you with:

• **File Management**: "Find report.txt", "Open document", "Search for images"
• **Weather Information**: "What's the weather?", "Weather forecast", "How's it outside?"
• **System Information**: "System status", "CPU usage", "Battery level"
• **Time & Date**: "What time is it?", "What's today's date?"
• **Information Lookup**: "What is quantum computing?", "Who is Einstein?"
• **Personal Notes**: "Remember that I prefer tea", "Note my meeting at 3 PM"
• **General Conversation**: I'm here to chat and assist with various tasks

Simply speak naturally, and I'll do my best to understand and assist you, Mr. Bharadwaj."""

        return help_text

    def _handle_goodbye(self, user_input: str) -> str:
        """Handle goodbye commands"""
        goodbyes = [
            "Farewell, Sir. It's been a pleasure assisting you.",
            "Goodbye, Mr. Bharadwaj. Until next time.",
            "Good day, Sir. I'll be here when you need me.",
            "Until we speak again, Sir. Take care.",
            "Goodbye, Sir. It's been my honour to serve."
        ]

        self.conversation_active = False
        return random.choice(goodbyes)

    def _handle_compliment(self, user_input: str) -> str:
        """Handle compliments and thanks"""
        responses = [
            "You're most welcome, Sir. It's my pleasure to assist.",
            "Thank you, Mr. Bharadwaj. I'm delighted to be of service.",
            "My pleasure, Sir. I'm here whenever you need assistance.",
            "It's my honour to serve, Sir.",
            "Thank you, Sir. I do strive to be helpful.",
            "Most kind of you to say, Mr. Bharadwaj."
        ]

        return random.choice(responses)

    def _handle_status(self, user_input: str) -> str:
        """Handle status inquiries"""
        responses = [
            "All systems operational, Sir. I'm functioning optimally.",
            "Running smoothly, Mr. Bharadwaj. How may I assist you?",
            "All systems green, Sir. Ready for your commands.",
            "Functioning perfectly, Sir. At your service.",
            "Systems nominal, Mr. Bharadwaj. How can I help?"
        ]

        return random.choice(responses)

    def _handle_unknown_command(self, user_input: str) -> str:
        """Handle unrecognized commands"""
        # Try AI conversation if available
        if self.use_ai_nlp:
            try:
                context = {
                    'user_name': config.USER_NAME,
                    'location': config.USER_LOCATION,
                    'conversation_type': 'general'
                }
                return self.nlp.generate_response(user_input, context)
            except Exception as e:
                print(f"AI conversation error: {e}")
        
        # Fallback responses
        responses = [
            "I'm not entirely certain what you're asking, Sir. Could you please rephrase?",
            "I didn't quite understand that command, Mr. Bharadwaj. Could you clarify?",
            "I'm afraid I don't recognize that request, Sir. Perhaps you could be more specific?",
            "Could you elaborate on that, Sir? I want to ensure I assist you properly.",
            "I'm not sure I follow, Mr. Bharadwaj. Could you try rephrasing that?"
        ]
        
        return random.choice(responses)

    def get_startup_message(self) -> str:
        """Get initial startup message"""
        greeting = self.memory.get_personalized_greeting()

        startup_messages = [
            f"{greeting} All systems are online and ready for your commands.",
            f"{greeting} I'm fully operational and at your service.",
            f"{greeting} All systems initialized successfully. How may I assist you today?",
            f"{greeting} Ready to serve, Sir. What shall we accomplish today?"
        ]

        return random.choice(startup_messages)

    def should_continue_conversation(self) -> bool:
        """Check if conversation should continue"""
        return self.conversation_active
