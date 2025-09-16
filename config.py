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
VOICE_RATE = 220  # Speaking rate (slower for more natural speech)
VOICE_VOLUME = 0.9  # Volume level (0.0 to 1.0)
BRITISH_VOICE_ID = 1  # British accent voice selection

# Voice Accent Settings
# Options: 'british', 'american', 'australian', 'indian', 'irish', 'scottish'
VOICE_ACCENT = 'american'  # Change this to your preferred accent

# Specific Voice Selection (optional - leave empty for auto-selection)
# British Female: serena, kate, emily, chloe, zoe, stephanie
# British Male: daniel, oliver
# American Female: victoria, allison, ava, samantha, susan, zoe, kathy
# American Male: alex, fred, tom, bruce, ralph
# Australian Female: karen, catherine, nicole, hayley
# Australian Male: lee
# Indian Female: veena, lekha, priya, kavya
# Indian Male: rishi
# Irish Female: fiona, moira, siobhan, niamh
# French Female: aurelie, amelie, celine, marie
# German Female: anna, petra, marlene
# Spanish Female: monica, carmen, esperanza
# Italian Female: alice, federica, paola
PREFERRED_VOICE = 'victoria'  # Set specific voice name or leave empty

# Conversation Realism Settings
NATURAL_SPEECH_PATTERNS = True  # Enable ultra-realistic conversation patterns
EMOTIONAL_RESPONSES = True      # Enable emotional expressions in speech
ACCENT_SPECIFIC_EXPRESSIONS = True  # Use accent-specific natural expressions

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

# Ultra-Realistic Voice Configuration
USE_ADVANCED_VOICE = True
ADVANCED_VOICE_ENGINE = 'gtts'
ADVANCED_VOICE_DESCRIPTION = 'English (UK) - Female'
SELECTED_FEMALE_VOICE = 'English (UK) - Female'

# SPEED OPTIMIZATION SETTINGS
VOICE_RATE = 280  # Ultra-fast speech rate
VOICE_VOLUME = 0.95  # Slightly higher volume for clarity at speed

# Response Speed Settings
FAST_RESPONSE_MODE = True  # Enable ultra-fast responses
MAX_RESPONSE_LENGTH = 150  # Limit response length for speed
QUICK_ACKNOWLEDGMENT = True  # Immediate acknowledgment before processing

# AI Processing Speed
GEMINI_TEMPERATURE = 0.3  # Lower temperature for faster, more focused responses
GEMINI_MAX_TOKENS = 200  # Limit tokens for faster generation
GEMINI_TIMEOUT = 5  # 5-second timeout for AI responses

# System Speed Settings
SKIP_VERBOSE_LOGGING = True  # Reduce logging overhead
FAST_STARTUP_MODE = True  # Skip non-essential initialization
PARALLEL_PROCESSING = True  # Enable parallel task processing
