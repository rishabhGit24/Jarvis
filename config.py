"""
Configuration settings for Jarvis Personal Assistant
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyDn5in1JWf0SUvjMxagpldT6exjaYZCSmk')

# User Settings
USER_NAME = os.getenv('USER_NAME', 'Mr. Bharadwaj')
USER_LOCATION = os.getenv('USER_LOCATION', 'New York')

# Voice Settings
VOICE_RATE = 185  # Speaking rate (slower for more natural speech)
VOICE_VOLUME = 0.9  # Volume level (0.0 to 1.0)
BRITISH_VOICE_ID = 1  # British accent voice selection

# File Search Settings
SEARCH_DIRECTORIES = [
    os.path.expanduser('~/Desktop'),
    os.path.expanduser('~/Documents'),
    os.path.expanduser('~/Downloads'),
    '/Users/rishabhbharadwajr/Desktop/Misc/proj'
]

# Memory Settings
MEMORY_FILE = 'jarvis_memory.json'
CONVERSATION_HISTORY_LIMIT = 100

# Weather Settings
WEATHER_UNITS = 'metric'  # metric, imperial, or kelvin
