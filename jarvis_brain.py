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
from jarvis_speed import perf_optimizer, speed_cache, timed_execution, fast_response
from jarvis_system_control import JarvisSystemControl
from jarvis_butler_personality import JarvisButlerPersonality

class JarvisBrain:
    def __init__(self):
        self.memory = JarvisMemory()
        self.file_manager = JarvisFileManager()
        self.weather = JarvisWeather()
        self.nlp = JarvisNLP()
        self.system_control = JarvisSystemControl()
        self.butler_personality = JarvisButlerPersonality()
        self.conversation_active = False
        self.use_ai_nlp = True  # Flag to enable/disable AI NLP

        # Enhanced command patterns for comprehensive system control (order matters!)
        self.command_patterns = {
            'greeting': [
                r'hello|hi|hey|good morning|good afternoon|good evening|greetings',
                self._handle_greeting
            ],
            'application_control': [
                r'(?:open|launch|start|run|close|quit)\s+(?:safari|chrome|firefox|browser|calculator|calc|calendar|mail|email|notes|music|photos|finder|files|terminal|settings|preferences)',
                self._handle_application_control
            ],
            'system_control': [
                r'sleep|restart|shutdown|lock|volume|brightness|wifi|bluetooth|mute|unmute',
                self._handle_system_control
            ],
            'website_navigation': [
                r'(?:go to|visit|navigate to|open)\s+(?:\w+\.(?:com|org|net|edu|gov)|www\.\w+|\w+\s+website|\w+\s+site|youtube|github|google)',
                self._handle_website_navigation
            ],
            'file_operations': [
                r'(?:create|make|new)\s+(?:a\s+)?(?:file|folder|directory)',
                self._handle_file_operations
            ],
            'system_info': [
                r'(?:system|computer|cpu|memory|ram|disk|storage|battery).*(?:status|info|usage|performance)|what.*system|check.*(?:cpu|memory|battery)',
                self._handle_system_info
            ],
            'time_date': [
                r'time|date|what.*day|when.*today|current.*time|clock',
                self._handle_time_date
            ],
            'weather': [
                r'weather|temperature|forecast|climate|how.*outside',
                self._handle_weather
            ],
            'wikipedia': [
                r'what is|who is|tell me about|information about|wikipedia|search for',
                self._handle_wikipedia_search
            ],
            'personal': [
                r'remember|note|personal|about me|my preference|learn',
                self._handle_personal_info
            ],
            'help': [
                r'help|what can you do|commands|capabilities|assist|guide',
                self._handle_help
            ],
            'goodbye': [
                r'goodbye|bye|see you|farewell|exit|quit|stop|that.*all',
                self._handle_goodbye
            ],
            'compliment': [
                r'thank you|thanks|good job|well done|excellent|brilliant|perfect|amazing',
                self._handle_compliment
            ],
            'status': [
                r'status|how are you|are you okay|functioning|operational|ready',
                self._handle_status
            ],
            'file_find': [
                r'find.*file|search.*file|locate.*file|where is.*file',
                self._handle_file_search
            ]
        }

        # Personality responses
        self.personality_responses = {
            'acknowledgments': [
                "Certainly, Mr. Bharadwaj Sir.",
                "Of course, Mr. Bharadwaj.",
                "Right away, Mr. Bharadwaj Sir.",
                "At once, Mr. Bharadwaj Sir.",
                "Very good, Mr. Bharadwaj Sir.",
                "Indeed, Mr. Bharadwaj Sir.",
                "Understood, Mr. Bharadwaj Sir."
            ],
            'apologies': [
                "I do apologize, Mr. Bharadwaj Sir.",
                "My sincere apologies, Mr. Bharadwaj.",
                "I'm terribly sorry, Mr. Bharadwaj Sir.",
                "Forgive me, Mr. Bharadwaj Sir.",
                "I regret the inconvenience, Mr. Bharadwaj Sir."
            ],
            'confirmations': [
                "Task completed successfully, Mr. Bharadwaj Sir.",
                "Done, Mr. Bharadwaj.",
                "All finished, Mr. Bharadwaj Sir.",
                "Task accomplished, Mr. Bharadwaj Sir.",
                "Completed as requested, Mr. Bharadwaj Sir."
            ],
            'thinking': [
                "Let me check that for you, Mr. Bharadwaj Sir.",
                "One moment please, Mr. Bharadwaj.",
                "Allow me to investigate, Mr. Bharadwaj Sir.",
                "Searching now, Mr. Bharadwaj Sir.",
                "Processing your request, Mr. Bharadwaj Sir."
            ]
        }

    @timed_execution
    def process_command(self, user_input: str) -> str:
        """Process user input and return appropriate response using enhanced AI NLP with smart routing"""
        if not user_input or not user_input.strip():
            return "I didn't quite catch that, Mr. Bharadwaj Sir. Could you please repeat?"

        original_input = user_input.strip()

        # Check for high-priority system commands first (before AI NLP)
        user_input_lower = original_input.lower()
        
        # Priority system commands that should bypass AI NLP
        priority_patterns = {
            'application_control': r'(?:open|launch|start|run|close|quit)\s+(?:safari|chrome|firefox|browser|calculator|calc|calendar|mail|email|notes|music|photos|finder|files|terminal|settings|preferences)',
            'system_control': r'(?:sleep|restart|shutdown|lock|volume|brightness|wifi|bluetooth|mute|unmute)',
            'website_navigation': r'(?:go to|visit|navigate to|open)\s+(?:\w+\.(?:com|org|net|edu|gov)|www\.\w+|\w+\s+website|\w+\s+site|youtube|github|google)',
            'file_operations': r'(?:create|make|new)\s+(?:a\s+)?(?:file|folder|directory)'
        }
        
        # Check priority patterns first
        for command_type, pattern in priority_patterns.items():
            if re.search(pattern, user_input_lower, re.IGNORECASE):
                handler_map = {
                    'application_control': self._handle_application_control,
                    'system_control': self._handle_system_control,
                    'website_navigation': self._handle_website_navigation,
                    'file_operations': self._handle_file_operations
                }
                
                try:
                    response = handler_map[command_type](original_input)
                    self.memory.add_conversation(original_input, response)
                    self.memory.learn_from_interaction(original_input, command_type)
                    return response
                except Exception as e:
                    error_response = self.butler_personality.apologize_for_error(f"I encountered an issue: {str(e)}")
                    self.memory.add_conversation(original_input, error_response)
                    return error_response

        # Try AI NLP for other commands if enabled and available
        if self.use_ai_nlp and hasattr(self.nlp, 'is_available') and self.nlp.is_available():
            try:
                # Get conversation context from memory
                context = {
                    'user_name': config.USER_NAME,
                    'location': config.USER_LOCATION,
                    'time': datetime.now().isoformat(),
                    'recent_interactions': self.memory.memory_data.get('conversation_history', [])[-3:]
                }

                # Use AI to understand the command (simplified)
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
                    error_response = f"I encountered an issue while processing your request, Mr. Bharadwaj Sir. {str(e)}"
                    self.memory.add_conversation(original_input, error_response)
                    return error_response

        # If no pattern matches, try AI conversation or fallback
        return self._handle_unknown_command(original_input)

    def _handle_greeting(self, user_input: str) -> str:
        """Handle greeting commands with sophisticated butler personality"""
        # Use the butler personality for contextual greetings
        greeting = self.butler_personality.get_contextual_greeting()
        
        # Add any recent context or proactive suggestions
        now = datetime.now()
        if now.hour < 9:  # Early morning
            greeting += " Shall I brief you on today's schedule or check for any urgent matters?"
        elif 12 <= now.hour < 14:  # Lunch time
            greeting += " I hope you're taking a proper break. Anything I can handle while you're away?"
        elif now.hour >= 20:  # Evening
            greeting += " Perhaps I could prepare a summary of today's accomplishments?"
        
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
                return ai_response or "What file would you like me to help you with, Mr. Bharadwaj Sir?"

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
                    # Use async generation for better performance
                    if hasattr(self.nlp, 'async_generate_response'):
                        future = self.nlp.async_generate_response(user_input, context)
                        return future.result() if hasattr(future, 'result') else future
                    else:
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
            return "I need to know what file you're looking for, Mr. Bharadwaj Sir. Please specify the filename."

        # Search for files
        thinking_response = random.choice(self.personality_responses['thinking'])
        files = self.file_manager.find_files(filename)

        if not files:
            return f"I'm afraid I couldn't locate any files matching '{filename}', Mr. Bharadwaj Sir. Perhaps it's in a different location?"

        if len(files) == 1:
            file_info = self.file_manager.get_file_info(files[0])
            self.memory.track_file_access(files[0])
            return f"I found the file, Mr. Bharadwaj Sir: {file_info['name']} located at {files[0]}. Would you like me to open it?"

        # Multiple files found
        response = f"I found {len(files)} files matching '{filename}', Mr. Bharadwaj Sir:\\n"
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
                    return f"Opening your most recent file, Mr. Bharadwaj Sir: {recent_files[0]}"
            return "Which file would you like me to open, Mr. Bharadwaj Sir?"

        # Search and open file
        files = self.file_manager.find_files(filename)
        if not files:
            return f"I couldn't find a file named '{filename}', Mr. Bharadwaj Sir."

        if self.file_manager.open_file(files[0]):
            self.memory.track_file_access(files[0])
            return f"Opening {files[0]}, Mr. Bharadwaj Sir."
        else:
            return f"I encountered an issue opening the file, Mr. Bharadwaj Sir."

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

            response = f"Here's the weather forecast for {forecast['location']}, Mr. Bharadwaj Sir:\\n"
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
                return f"CPU usage is currently at {cpu_percent}%, Mr. Bharadwaj Sir."

            elif 'memory' in user_input or 'ram' in user_input:
                memory = psutil.virtual_memory()
                return f"Memory usage: {memory.percent}% of {memory.total // (1024**3)} GB, Mr. Bharadwaj Sir."

            elif 'disk' in user_input or 'storage' in user_input:
                disk = psutil.disk_usage('/')
                used_gb = disk.used // (1024**3)
                total_gb = disk.total // (1024**3)
                return f"Disk usage: {used_gb} GB of {total_gb} GB used ({disk.percent:.1f}%), Mr. Bharadwaj Sir."

            elif 'battery' in user_input:
                try:
                    battery = psutil.sensors_battery()
                    if battery:
                        status = "charging" if battery.power_plugged else "discharging"
                        return f"Battery is at {battery.percent:.1f}% and {status}, Mr. Bharadwaj Sir."
                    else:
                        return "No battery information available, Mr. Bharadwaj Sir. This appears to be a desktop system."
                except:
                    return "Battery information is not available on this system, Mr. Bharadwaj Sir."

            else:
                # General system info
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                boot_time = datetime.fromtimestamp(psutil.boot_time())
                uptime = datetime.now() - boot_time

                response = f"System status, Mr. Bharadwaj Sir:\\n"
                response += f"• CPU: {cpu_percent}%\\n"
                response += f"• Memory: {memory.percent}%\\n"
                response += f"• Uptime: {uptime.days} days, {uptime.seconds//3600} hours\\n"
                response += f"• Platform: {platform.system()} {platform.release()}"

                return response

        except Exception as e:
            return f"I encountered an issue retrieving system information, Mr. Bharadwaj Sir: {str(e)}"

    def _handle_time_date(self, user_input: str) -> str:
        """Handle time and date requests"""
        now = datetime.now()

        if 'time' in user_input:
            return f"The current time is {now.strftime('%I:%M %p')}, Mr. Bharadwaj Sir."
        elif 'date' in user_input:
            return f"Today is {now.strftime('%A, %B %d, %Y')}, Mr. Bharadwaj Sir."
        else:
            return f"It is currently {now.strftime('%I:%M %p on %A, %B %d, %Y')}, Mr. Bharadwaj Sir."

    def _handle_wikipedia_search(self, user_input: str) -> str:
        """Handle Wikipedia search requests"""
        # Extract search term
        patterns = [
            r'search for\s+(.+)',           # ADD THIS LINE
            r'search\s+(.+)',               # ADD THIS LINE  
            r'look up\s+(.+)',              # ADD THIS LINE
            r'find information about\s+(.+)', # ADD THIS LINE
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
            return "What would you like me to look up for you, Mr. Bharadwaj Sir?"

        try:
            # Search Wikipedia
            summary = wikipedia.summary(search_term, sentences=3)
            return f"According to Wikipedia, Mr. Bharadwaj Sir: {summary}"
        except wikipedia.exceptions.DisambiguationError as e:
            options = e.options[:3]
            return f"There are multiple entries for '{search_term}', Mr. Bharadwaj Sir. Did you mean: {', '.join(options)}?"
        except wikipedia.exceptions.PageError:
            return f"I couldn't find any information about '{search_term}' on Wikipedia, Mr. Bharadwaj Sir."
        except Exception as e:
            return f"I encountered an issue searching Wikipedia, Mr. Bharadwaj Sir: {str(e)}"

    def _handle_personal_info(self, user_input: str) -> str:
        """Handle personal information and preferences"""
        if 'remember' in user_input or 'note' in user_input:
            # Extract what to remember
            remember_match = re.search(r'remember\s+(?:that\s+)?(.+)', user_input, re.IGNORECASE)
            note_match = re.search(r'note\s+(?:that\s+)?(.+)', user_input, re.IGNORECASE)

            if remember_match:
                info = remember_match.group(1).strip()
                self.memory.add_personal_note("user_preference", info)
                return f"I've made a note of that, Mr. Bharadwaj Sir: {info}"
            elif note_match:
                info = note_match.group(1).strip()
                self.memory.add_personal_note("personal_note", info)
                return f"Noted, Mr. Bharadwaj Sir: {info}"

        # Return personal context
        context = self.memory.get_user_context()
        if context.strip():
            return f"Here's what I know about you, Mr. Bharadwaj Sir:\\n{context}"
        else:
            return "I'm still learning about your preferences, Mr. Bharadwaj Sir. Feel free to tell me anything you'd like me to remember."

    def _handle_help(self, user_input: str) -> str:
        """Handle help requests"""
        help_text = """I'm at your service, Mr. Bharadwaj Sir. Here's what I can assist you with:

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
            "Farewell, Mr. Bharadwaj Sir. It's been a pleasure assisting you.",
            "Goodbye, Mr. Bharadwaj. Until next time.",
            "Good day, Mr. Bharadwaj Sir. I'll be here when you need me.",
            "Until we speak again, Mr. Bharadwaj Sir. Take care.",
            "Goodbye, Mr. Bharadwaj Sir. It's been my honour to serve."
        ]

        self.conversation_active = False
        return random.choice(goodbyes)

    def _handle_compliment(self, user_input: str) -> str:
        """Handle compliments and thanks"""
        responses = [
            "You're most welcome, Mr. Bharadwaj Sir. It's my pleasure to assist.",
            "Thank you, Mr. Bharadwaj. I'm delighted to be of service.",
            "My pleasure, Mr. Bharadwaj Sir. I'm here whenever you need assistance.",
            "It's my honour to serve, Mr. Bharadwaj Sir.",
            "Thank you, Mr. Bharadwaj Sir. I do strive to be helpful.",
            "Most kind of you to say, Mr. Bharadwaj."
        ]

        return random.choice(responses)

    def _handle_status(self, user_input: str) -> str:
        """Handle status inquiries"""
        responses = [
            "All systems operational, Mr. Bharadwaj Sir. I'm functioning optimally.",
            "Running smoothly, Mr. Bharadwaj. How may I assist you?",
            "All systems green, Mr. Bharadwaj Sir. Ready for your commands.",
            "Functioning perfectly, Mr. Bharadwaj Sir. At your service.",
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
            "I'm not entirely certain what you're asking, Mr. Bharadwaj Sir. Could you please rephrase?",
            "I didn't quite understand that command, Mr. Bharadwaj. Could you clarify?",
            "I'm afraid I don't recognize that request, Mr. Bharadwaj Sir. Perhaps you could be more specific?",
            "Could you elaborate on that, Mr. Bharadwaj Sir? I want to ensure I assist you properly.",
            "I'm not sure I follow, Mr. Bharadwaj. Could you try rephrasing that?"
        ]
        
        return random.choice(responses)
    
    def _provide_immediate_feedback(self, user_input: str) -> None:
        """Provide immediate feedback to keep user engaged while processing"""
        user_lower = user_input.lower()
        
        # Quick acknowledgments for different types of requests
        if any(word in user_lower for word in ['find', 'search', 'locate']):
            feedback = "Let me search for that right away, Mr. Bharadwaj Sir."
        elif any(word in user_lower for word in ['weather', 'temperature', 'forecast']):
            feedback = "Checking the weather conditions for you, Mr. Bharadwaj Sir."
        elif any(word in user_lower for word in ['open', 'launch', 'start']):
            feedback = "Certainly, Mr. Bharadwaj Sir. Opening that for you now."
        elif any(word in user_lower for word in ['what', 'who', 'tell me', 'explain']):
            feedback = "Allow me to look that up for you, Mr. Bharadwaj Sir."
        elif any(word in user_lower for word in ['system', 'cpu', 'memory', 'status']):
            feedback = "Checking system status, Mr. Bharadwaj Sir."
        else:
            feedback = "Processing your request, Mr. Bharadwaj Sir."
        
        # Print immediate feedback (voice will be handled by the main loop)
        from rich.console import Console
        console = Console()
        console.print(f"[dim cyan]{feedback}[/dim cyan]")
    
    def _get_engaging_processing_message(self, command_type: str) -> str:
        """Get contextual processing messages to keep user engaged"""
        messages = {
            'file_search': [
                "Scanning through your files, Mr. Bharadwaj Sir...",
                "Searching the file system for you...",
                "Let me locate that file for you, Mr. Bharadwaj Sir..."
            ],
            'weather': [
                "Checking current weather conditions, Mr. Bharadwaj Sir...",
                "Fetching the latest weather data for you...",
                "Consulting the meteorological services, Mr. Bharadwaj Sir..."
            ],
            'system_info': [
                "Analyzing system performance, Mr. Bharadwaj Sir...",
                "Gathering system diagnostics for you...",
                "Checking all system parameters, Mr. Bharadwaj Sir..."
            ],
            'wikipedia': [
                "Consulting the knowledge base, Mr. Bharadwaj Sir...",
                "Searching for comprehensive information...",
                "Accessing the encyclopedia for you, Mr. Bharadwaj Sir..."
            ],
            'ai_processing': [
                "Analyzing your request with advanced AI, Mr. Bharadwaj Sir...",
                "Processing through the neural networks...",
                "Consulting the artificial intelligence systems, Mr. Bharadwaj Sir..."
            ],
            'default': [
                "Working on that for you, Mr. Bharadwaj Sir...",
                "Processing your request...",
                "One moment please, Mr. Bharadwaj Sir..."
            ]
        }
        
        import random
        return random.choice(messages.get(command_type, messages['default']))

    def _handle_application_control(self, user_input: str) -> str:
        """Handle application launch/close commands with butler intelligence"""
        user_input_lower = user_input.lower()
        
        # Determine if it's open or close command
        is_close_command = any(word in user_input_lower for word in ['close', 'quit', 'exit', 'stop'])
        
        # Extract application name intelligently
        app_patterns = [
            r'(?:open|launch|start|run|close|quit)\s+(.+?)(?:\s+(?:app|application|browser|program))?$',
            r'(?:open|launch|start|run|close|quit)\s+(?:the\s+)?(.+?)(?:\s+(?:app|application|browser|program))?$'
        ]
        
        app_name = None
        for pattern in app_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                app_name = match.group(1).strip()
                break
        
        if not app_name:
            # Try to extract from common phrases
            if 'safari' in user_input_lower or 'browser' in user_input_lower:
                app_name = 'safari'
            elif 'chrome' in user_input_lower:
                app_name = 'chrome'
            elif 'firefox' in user_input_lower:
                app_name = 'firefox'
            elif 'calculator' in user_input_lower or 'calc' in user_input_lower:
                app_name = 'calculator'
            elif 'calendar' in user_input_lower:
                app_name = 'calendar'
            elif 'mail' in user_input_lower or 'email' in user_input_lower:
                app_name = 'mail'
            elif 'notes' in user_input_lower:
                app_name = 'notes'
            elif 'music' in user_input_lower:
                app_name = 'music'
            elif 'photos' in user_input_lower:
                app_name = 'photos'
            elif 'finder' in user_input_lower or 'files' in user_input_lower:
                app_name = 'finder'
            elif 'terminal' in user_input_lower:
                app_name = 'terminal'
            elif 'settings' in user_input_lower or 'preferences' in user_input_lower:
                app_name = 'system preferences'
        
        if not app_name:
            return self.butler_personality.request_clarification("which application you'd like me to work with")
        
        # Execute the command
        if is_close_command:
            success, message = self.system_control.close_application(app_name)
            if success:
                return self.butler_personality.report_completion(f"I've closed {app_name} for you.")
            else:
                return self.butler_personality.apologize_for_error(f"I couldn't close {app_name}. {message}")
        else:
            # Acknowledge the command first
            acknowledgment = self.butler_personality.acknowledge_command("system")
            
            success, message = self.system_control.open_application(app_name)
            if success:
                return f"{acknowledgment} {app_name.title()} is now open and ready for you."
            else:
                return self.butler_personality.apologize_for_error(f"I couldn't open {app_name}. {message}")

    def _handle_system_control(self, user_input: str) -> str:
        """Handle system control commands like sleep, volume, etc."""
        user_input_lower = user_input.lower()
        
        # Map natural language to system commands
        command_map = {
            'sleep': 'sleep',
            'put to sleep': 'sleep',
            'go to sleep': 'sleep',
            'restart': 'restart',
            'reboot': 'restart',
            'shutdown': 'shutdown',
            'shut down': 'shutdown',
            'power off': 'shutdown',
            'lock': 'lock',
            'lock screen': 'lock',
            'volume up': 'volume up',
            'turn up volume': 'volume up',
            'increase volume': 'volume up',
            'volume down': 'volume down',
            'turn down volume': 'volume down',
            'decrease volume': 'volume down',
            'lower volume': 'volume down',
            'mute': 'mute',
            'silence': 'mute',
            'unmute': 'unmute',
            'turn on sound': 'unmute',
            'brightness up': 'brightness up',
            'brighter': 'brightness up',
            'brightness down': 'brightness down',
            'dimmer': 'brightness down',
            'wifi on': 'wifi on',
            'turn on wifi': 'wifi on',
            'enable wifi': 'wifi on',
            'wifi off': 'wifi off',
            'turn off wifi': 'wifi off',
            'disable wifi': 'wifi off',
            'bluetooth on': 'bluetooth on',
            'turn on bluetooth': 'bluetooth on',
            'enable bluetooth': 'bluetooth on',
            'bluetooth off': 'bluetooth off',
            'turn off bluetooth': 'bluetooth off',
            'disable bluetooth': 'bluetooth off'
        }
        
        # Find matching command
        system_command = None
        for phrase, cmd in command_map.items():
            if phrase in user_input_lower:
                system_command = cmd
                break
        
        if not system_command:
            return self.butler_personality.request_clarification("what system function you'd like me to control")
        
        # Acknowledge potentially disruptive commands
        if system_command in ['sleep', 'restart', 'shutdown', 'lock']:
            acknowledgment = f"Certainly, {config.USER_NAME}. I'll {system_command} the system now."
        else:
            acknowledgment = self.butler_personality.acknowledge_command("system")
        
        success, message = self.system_control.system_command(system_command)
        
        if success:
            return f"{acknowledgment} {message}"
        else:
            return self.butler_personality.apologize_for_error(message)

    def _handle_website_navigation(self, user_input: str) -> str:
        """Handle website navigation commands"""
        # Extract URL from command
        url_patterns = [
            r'(?:go to|visit|navigate to|open)\s+(.+?)(?:\s+(?:website|site))?$',
            r'(?:go to|visit|navigate to|open)\s+(?:the\s+)?(.+?)(?:\s+(?:website|site))?$'
        ]
        
        url = None
        for pattern in url_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                url = match.group(1).strip()
                break
        
        if not url:
            return self.butler_personality.request_clarification("which website you'd like me to open")
        
        # Clean up the URL
        url = url.replace(' ', '')  # Remove spaces
        
        # Add common domains if just a name is given
        if '.' not in url:
            url = f"{url}.com"
        
        acknowledgment = self.butler_personality.acknowledge_command("system")
        success, message = self.system_control.open_website(url)
        
        if success:
            return f"{acknowledgment} Opening {url} in your browser now."
        else:
            return self.butler_personality.apologize_for_error(message)

    def _handle_file_operations(self, user_input: str) -> str:
        """Handle file and folder creation commands"""
        user_input_lower = user_input.lower()
        
        # Determine operation type
        is_folder = any(word in user_input_lower for word in ['folder', 'directory', 'dir'])
        
        # Extract name
        name_patterns = [
            r'(?:create|make|new)\s+(?:a\s+)?(?:file|folder|directory)\s+(?:called\s+|named\s+)?(.+?)$',
            r'(?:create|make|new)\s+(.+?)(?:\s+(?:file|folder|directory))?$'
        ]
        
        name = None
        for pattern in name_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                break
        
        if not name:
            item_type = "folder" if is_folder else "file"
            return self.butler_personality.request_clarification(f"what you'd like to name the {item_type}")
        
        acknowledgment = self.butler_personality.acknowledge_command("system")
        
        if is_folder:
            success, message = self.system_control.create_folder(name)
            item_type = "folder"
        else:
            success, message = self.system_control.create_file(name)
            item_type = "file"
        
        if success:
            return f"{acknowledgment} I've created the {item_type} '{name}' for you."
        else:
            return self.butler_personality.apologize_for_error(message)

    def get_startup_message(self) -> str:
        """Get initial startup message with butler personality"""
        # Use butler personality for sophisticated startup
        greeting = self.butler_personality.get_contextual_greeting()
        
        # Add system status and proactive suggestions
        startup_messages = [
            f"{greeting} All systems are online and optimized for your needs.",
            f"{greeting} I'm fully operational and eager to assist with whatever you require.",
            f"{greeting} All systems initialized successfully. I'm ready to serve.",
            f"{greeting} Standing by and ready to handle any task you have in mind."
        ]

        return random.choice(startup_messages)

    def should_continue_conversation(self) -> bool:
        """Check if conversation should continue"""
        return self.conversation_active
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get comprehensive brain performance statistics"""
        stats = {
            'conversation_active': self.conversation_active,
            'use_ai_nlp': self.use_ai_nlp
        }
        
        # Add NLP performance stats
        if hasattr(self.nlp, 'get_performance_stats'):
            stats['nlp_stats'] = self.nlp.get_performance_stats()
        
        # Add memory stats
        if hasattr(self.memory, 'get_stats'):
            stats['memory_stats'] = self.memory.get_stats()
        
        # Add file manager stats
        if hasattr(self.file_manager, 'get_stats'):
            stats['file_stats'] = self.file_manager.get_stats()
        
        return stats
    
    def optimize_for_performance(self):
        """Optimize brain components for better performance"""
        print("⚡ Optimizing Jarvis Brain for performance...")
        
        # Simple optimization
        if hasattr(self.nlp, 'optimize_for_performance'):
            self.nlp.optimize_for_performance()
        
        print("⚡ Brain optimization complete")
