"""
Layer 1: Local Model for Simple Tasks
Handles basic queries without requiring cloud AI or complex processing
"""
import re
import subprocess
import platform
import psutil
from datetime import datetime
from typing import Dict, List, Any, Optional
import config
from jarvis_personal_bio import personal_bio_analyzer

class Layer1LocalModel:
    """Local model for handling simple tasks with instant responses"""
    
    def __init__(self):
        self.simple_patterns = {
            'greeting': {
                'patterns': [
                    r'\b(hello|hi|hey|good morning|good afternoon|good evening|greetings)\b',
                    r'\b(how are you|how do you do)\b'
                ],
                'handler': self._handle_greeting
            },
            'time': {
                'patterns': [
                    r'\b(what time|current time|time is it|what\'s the time)\b',
                    r'\b(clock|time now)\b'
                ],
                'handler': self._handle_time
            },
            'date': {
                'patterns': [
                    r'\b(what date|today|current date|what\'s the date)\b',
                    r'\b(what day|day today|what day is it|what\'s the day)\b',
                    r'\b(day of the week|which day)\b',
                    r'\b(what month|current month|what\'s the month|which month|month is)\b',
                    r'\b(what year|current year|what\'s the year|which year|year is)\b'
                ],
                'handler': self._handle_date
            },
            'who_am_i': {
                'patterns': [
                    r'\b(who am i|who are you|tell me about myself|about me)\b',
                    r'\b(my name|my identity|personal info)\b',
                    r'\b(what is my name|what\'s my name|my name is)\b'
                ],
                'handler': self._handle_who_am_i
            },
            'open_browser': {
                'patterns': [
                    r'\b(open browser|open safari|launch browser|start browser)\b',
                    r'\b(open chrome|open firefox)\b'
                ],
                'handler': self._handle_open_browser
            },
            'system_status': {
                'patterns': [
                    r'\b(system status|how are you|are you working|status)\b',
                    r'\b(functioning|operational|ready)\b'
                ],
                'handler': self._handle_system_status
            },
            'simple_math': {
                'patterns': [
                    r'\b(what is|calculate)\s*(\d+)\s*([+\-*/])\s*(\d+)\b',
                    r'\b(\d+)\s*([+\-*/])\s*(\d+)\s*equals?\b'
                ],
                'handler': self._handle_simple_math
            },
            'weather_basic': {
                'patterns': [
                    r'\b(weather|temperature|climate)\b'
                ],
                'handler': self._handle_weather_basic
            },
            'file_basic': {
                'patterns': [
                    r'\b(find|search|locate).*\b(file|document)\b'
                ],
                'handler': self._handle_file_basic
            }
        }
        
        # Performance tracking
        self.stats = {
            'total_requests': 0,
            'successful_responses': 0,
            'response_times': [],
            'pattern_matches': {}
        }
    
    def can_handle(self, user_input: str) -> bool:
        """Check if this layer can handle the user input"""
        user_input_lower = user_input.lower()
        
        for pattern_name, pattern_data in self.simple_patterns.items():
            for pattern in pattern_data['patterns']:
                if re.search(pattern, user_input_lower, re.IGNORECASE):
                    return True
        
        return False
    
    def process(self, user_input: str) -> str:
        """Process user input and return response"""
        start_time = datetime.now()
        self.stats['total_requests'] += 1
        
        user_input_lower = user_input.lower()
        
        # Find matching pattern
        for pattern_name, pattern_data in self.simple_patterns.items():
            for pattern in pattern_data['patterns']:
                if re.search(pattern, user_input_lower, re.IGNORECASE):
                    try:
                        response = pattern_data['handler'](user_input)
                        self.stats['successful_responses'] += 1
                        self.stats['pattern_matches'][pattern_name] = self.stats['pattern_matches'].get(pattern_name, 0) + 1
                        
                        # Track response time
                        response_time = (datetime.now() - start_time).total_seconds()
                        self.stats['response_times'].append(response_time)
                        
                        return response
                    except Exception as e:
                        return f"I encountered an issue processing that request, Mr. Bharadwaj Sir: {str(e)}"
        
        # No pattern matched
        return None
    
    def _handle_greeting(self, user_input: str) -> str:
        """Handle greeting commands"""
        greetings = [
            f"Good day, {config.USER_NAME}. How may I assist you?",
            f"Hello, Mr. Bharadwaj Sir. At your service.",
            f"Greetings, {config.USER_NAME}. Ready to help.",
            f"Good to see you, Mr. Bharadwaj Sir. What can I do for you?"
        ]
        
        # Add time-based greeting
        now = datetime.now()
        if now.hour < 12:
            time_greeting = "Good morning"
        elif now.hour < 17:
            time_greeting = "Good afternoon"
        else:
            time_greeting = "Good evening"
        
        return f"{time_greeting}, Mr. Bharadwaj Sir. How may I assist you today?"
    
    def _handle_time(self, user_input: str) -> str:
        """Handle time requests"""
        now = datetime.now()
        time_str = now.strftime('%I:%M %p')
        return f"The current time is {time_str}, Mr. Bharadwaj Sir."
    
    def _handle_date(self, user_input: str) -> str:
        """Handle date requests"""
        now = datetime.now()
        user_input_lower = user_input.lower()
        
        # Handle specific queries
        if 'month' in user_input_lower:
            month_str = now.strftime('%B')
            return f"It is {month_str}, Mr. Bharadwaj Sir."
        elif 'year' in user_input_lower:
            year_str = now.strftime('%Y')
            return f"It is {year_str}, Mr. Bharadwaj Sir."
        elif 'day' in user_input_lower and 'week' not in user_input_lower:
            day_str = now.strftime('%A')
            return f"It is {day_str}, Mr. Bharadwaj Sir."
        else:
            # Full date
            date_str = now.strftime('%A, %B %d, %Y')
            return f"Today is {date_str}, Mr. Bharadwaj Sir."
    
    def _handle_who_am_i(self, user_input: str) -> str:
        """Handle personal identity requests"""
        # Get personal summary from bio analyzer
        personal_summary = personal_bio_analyzer.get_personal_summary()
        
        if personal_summary and personal_summary != "Personal information not available.":
            return f"Based on your personal information, Mr. Bharadwaj Sir: {personal_summary}"
        else:
            return f"You are {config.USER_NAME}, and I'm your personal AI assistant, Mr. Bharadwaj Sir. I'm here to help you with various tasks and provide assistance whenever you need it."
    
    def _handle_open_browser(self, user_input: str) -> str:
        """Handle browser opening requests"""
        user_input_lower = user_input.lower()
        
        # Determine which browser to open
        if 'chrome' in user_input_lower:
            browser = 'chrome'
        elif 'firefox' in user_input_lower:
            browser = 'firefox'
        else:
            browser = 'safari'  # Default on macOS
        
        try:
            if platform.system() == 'Darwin':  # macOS
                if browser == 'safari':
                    subprocess.run(['open', '-a', 'Safari'], check=True)
                elif browser == 'chrome':
                    subprocess.run(['open', '-a', 'Google Chrome'], check=True)
                elif browser == 'firefox':
                    subprocess.run(['open', '-a', 'Firefox'], check=True)
            elif platform.system() == 'Windows':
                if browser == 'chrome':
                    subprocess.run(['start', 'chrome'], shell=True, check=True)
                elif browser == 'firefox':
                    subprocess.run(['start', 'firefox'], shell=True, check=True)
                else:
                    subprocess.run(['start', 'msedge'], shell=True, check=True)
            else:  # Linux
                if browser == 'chrome':
                    subprocess.run(['google-chrome'], check=True)
                elif browser == 'firefox':
                    subprocess.run(['firefox'], check=True)
                else:
                    subprocess.run(['xdg-open', 'http://'], check=True)
            
            return f"I've opened {browser.title()} for you, Mr. Bharadwaj Sir."
        
        except subprocess.CalledProcessError:
            return f"I encountered an issue opening {browser}, Mr. Bharadwaj Sir. Please try opening it manually."
        except Exception as e:
            return f"I couldn't open the browser, Mr. Bharadwaj Sir: {str(e)}"
    
    def _handle_system_status(self, user_input: str) -> str:
        """Handle system status requests"""
        try:
            # Get basic system info
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            
            status = f"All systems operational, Mr. Bharadwaj Sir. "
            status += f"CPU: {cpu_percent}%, Memory: {memory.percent}%, "
            status += f"Uptime: {uptime.days} days, {uptime.seconds//3600} hours."
            
            return status
        
        except Exception as e:
            return f"Systems are running, Mr. Bharadwaj Sir, though I encountered an issue retrieving detailed status: {str(e)}"
    
    def _handle_simple_math(self, user_input: str) -> str:
        """Handle simple mathematical calculations"""
        try:
            # Extract numbers and operator
            math_patterns = [
                r'(\d+)\s*([+\-*/])\s*(\d+)',
                r'what is\s*(\d+)\s*([+\-*/])\s*(\d+)',
                r'calculate\s*(\d+)\s*([+\-*/])\s*(\d+)'
            ]
            
            for pattern in math_patterns:
                match = re.search(pattern, user_input)
                if match:
                    num1 = float(match.group(1))
                    operator = match.group(2)
                    num2 = float(match.group(3))
                    
                    if operator == '+':
                        result = num1 + num2
                    elif operator == '-':
                        result = num1 - num2
                    elif operator == '*':
                        result = num1 * num2
                    elif operator == '/':
                        if num2 == 0:
                            return "I cannot divide by zero, Mr. Bharadwaj Sir."
                        result = num1 / num2
                    else:
                        return "I don't recognize that mathematical operation, Mr. Bharadwaj Sir."
                    
                    return f"The result is {result}, Mr. Bharadwaj Sir."
            
            return "I couldn't understand the mathematical expression, Mr. Bharadwaj Sir."
        
        except Exception as e:
            return f"I encountered an error with that calculation, Mr. Bharadwaj Sir: {str(e)}"
    
    def _handle_weather_basic(self, user_input: str) -> str:
        """Handle basic weather requests"""
        return "I'd be happy to check the weather for you, Mr. Bharadwaj Sir, but I need to access weather services for current conditions. Let me transfer this to a more capable system."
    
    def _handle_file_basic(self, user_input: str) -> str:
        """Handle basic file search requests"""
        return "I can help you search for files, Mr. Bharadwaj Sir. Let me transfer this to a more capable system for comprehensive file searching."
    
    def get_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        avg_response_time = 0
        if self.stats['response_times']:
            avg_response_time = sum(self.stats['response_times']) / len(self.stats['response_times'])
        
        return {
            'total_requests': self.stats['total_requests'],
            'successful_responses': self.stats['successful_responses'],
            'success_rate': (self.stats['successful_responses'] / max(self.stats['total_requests'], 1)) * 100,
            'average_response_time': avg_response_time,
            'pattern_matches': self.stats['pattern_matches']
        }
    
    def is_available(self) -> bool:
        """Check if the local model is available"""
        return True  # Always available as it's local

# Initialize the local model
layer1_local_model = Layer1LocalModel()
