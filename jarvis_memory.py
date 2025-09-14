"""
Memory and Learning System for Jarvis
Handles user preferences, conversation history, and adaptive learning
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
import config

class JarvisMemory:
    def __init__(self):
        self.memory_file = config.MEMORY_FILE
        self.memory_data = self.load_memory()

    def load_memory(self) -> Dict[str, Any]:
        """Load memory from file or create new memory structure"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass

        # Initialize new memory structure
        return {
            'user_preferences': {
                'name': config.USER_NAME,
                'location': config.USER_LOCATION,
                'favorite_topics': [],
                'daily_schedule': {},
                'frequently_accessed_files': {},
                'preferred_responses': {}
            },
            'conversation_history': [],
            'learned_patterns': {
                'common_requests': {},
                'file_access_patterns': {},
                'time_based_preferences': {}
            },
            'personal_notes': {},
            'important_dates': {},
            'last_interaction': None
        }

    def save_memory(self):
        """Save current memory state to file"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.memory_data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving memory: {e}")

    def add_conversation(self, user_input: str, jarvis_response: str):
        """Add conversation to history with timestamp"""
        conversation = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'jarvis_response': jarvis_response
        }
        self.memory_data['conversation_history'].append(conversation)
        # Limit conversation history size
        if len(self.memory_data['conversation_history']) > config.CONVERSATION_HISTORY_LIMIT:
            self.memory_data['conversation_history'] = self.memory_data['conversation_history'][-config.CONVERSATION_HISTORY_LIMIT:]

        self.memory_data['last_interaction'] = datetime.now().isoformat()
        self.save_memory()

    def learn_from_interaction(self, user_input: str, action_taken: str):
        """Learn patterns from user interactions"""
        # Track common requests
        request_key = user_input.lower().strip()
        if request_key in self.memory_data['learned_patterns']['common_requests']:
            self.memory_data['learned_patterns']['common_requests'][request_key] += 1
        else:
            self.memory_data['learned_patterns']['common_requests'][request_key] = 1
        # Learn time-based patterns
        current_hour = datetime.now().hour
        time_period = self.get_time_period(current_hour)
        if time_period not in self.memory_data['learned_patterns']['time_based_preferences']:
            self.memory_data['learned_patterns']['time_based_preferences'][time_period] = []
        if action_taken not in self.memory_data['learned_patterns']['time_based_preferences'][time_period]:
            self.memory_data['learned_patterns']['time_based_preferences'][time_period].append(action_taken)
        self.save_memory()
    def track_file_access(self, file_path: str):
        """Track frequently accessed files"""
        if file_path in self.memory_data['user_preferences']['frequently_accessed_files']:
            self.memory_data['user_preferences']['frequently_accessed_files'][file_path] += 1
        else:
            self.memory_data['user_preferences']['frequently_accessed_files'][file_path] = 1
        self.save_memory()
    def add_personal_note(self, topic: str, note: str):
        """Add personal note about the user"""
        self.memory_data['personal_notes'][topic] = {
            'note': note,
            'timestamp': datetime.now().isoformat()
        }
        self.save_memory()
    def get_user_context(self) -> str:
        """Generate context about the user for personalized responses"""
        context = f"User: {self.memory_data['user_preferences']['name']}\n"
        context += f"Location: {self.memory_data['user_preferences']['location']}\n"
        if self.memory_data['personal_notes']:
            context += "Personal Notes:\n"
            for topic, data in self.memory_data['personal_notes'].items():
                context += f"- {topic}: {data['note']}\n"
        if self.memory_data['user_preferences']['favorite_topics']:
            context += f"Interests: {', '.join(self.memory_data['user_preferences']['favorite_topics'])}\n"
        return context
    def get_time_period(self, hour: int) -> str:
        """Determine time period from hour"""
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 21:
            return "evening"
        else:
            return "night"
    def get_personalized_greeting(self) -> str:
        """Generate personalized greeting based on time and history"""
        current_hour = datetime.now().hour
        time_period = self.get_time_period(current_hour)
        greetings = {
            "morning": [
                f"Good morning, {config.USER_NAME}. I trust you slept well?",
                f"Morning, {config.USER_NAME}. Ready to tackle the day?",
                f"Good morning, Mr. Bharadwaj Sir. How may I assist you today?"
            ],
            "afternoon": [
                f"Good afternoon, {config.USER_NAME}. How has your day been?",
                f"Afternoon, Mr. Bharadwaj Sir. What can I help you with?",
                f"Good afternoon, {config.USER_NAME}. At your service."
            ],
            "evening": [
                f"Good evening, {config.USER_NAME}. I hope your day was productive.",
                f"Evening, Mr. Bharadwaj Sir. How may I be of assistance?",
                f"Good evening, {config.USER_NAME}. Ready to wind down?"
            ],
            "night": [
                f"Good evening, {config.USER_NAME}. Working late tonight?",
                f"Evening, Mr. Bharadwaj Sir. Burning the midnight oil?",
                f"Good evening, {config.USER_NAME}. How may I assist you?"
            ]
        }
        import random
        return random.choice(greetings[time_period])
