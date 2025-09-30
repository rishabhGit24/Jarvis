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
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyDaQVdFddNnrK9AKtwJ97hWGGt5630Z6k4')

# User Settings
USER_NAME = os.getenv('USER_NAME', 'Mr. Bharadwaj')
USER_LOCATION = os.getenv('USER_LOCATION', 'Bangalore')

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
VOICE_RATE = 185  # Slower, more natural speech rate
VOICE_VOLUME = 0.9  # Standard volume for clarity

# Response Speed Settings
FAST_RESPONSE_MODE = False  # Disable ultra-fast responses for more natural pacing
MAX_RESPONSE_LENGTH = 300  # Allow longer responses for better quality
QUICK_ACKNOWLEDGMENT = False  # Disable immediate acknowledgment for more natural flow

# AI Processing Speed
GEMINI_TEMPERATURE = 0.4  # Higher temperature for more natural, varied responses
GEMINI_MAX_TOKENS = 300  # Allow more tokens for better quality responses
GEMINI_TIMEOUT = 10  # Longer timeout for better responses

# System Speed Settings
SKIP_VERBOSE_LOGGING = True  # Reduce logging overhead
FAST_STARTUP_MODE = True  # Skip non-essential initialization
PARALLEL_PROCESSING = True  # Enable parallel task processing

# LAYERED AI MODEL SETTINGS
# Layer 1: Local Model Settings
LAYER1_ENABLED = True  # Enable local model for simple tasks
LAYER1_RESPONSE_TIME_LIMIT = 0.5  # Max response time for Layer 1 (seconds)

# Layer 2: Stalling Model Settings
LAYER2_ENABLED = False  # Disable stalling model for more responsive assistant
LAYER2_MAX_STALL_TIME = 10.0  # Maximum stalling time (seconds)
LAYER2_ENGAGEMENT_INTERVAL = 2.0  # Interval between engagement messages (seconds)

# Layer 3: Gemini Model Settings
LAYER3_ENABLED = True  # Enable Gemini model
LAYER3_TIMEOUT = 15.0  # Timeout for Gemini requests (seconds)
LAYER3_CACHE_SIZE = 100  # Maximum cache size for responses
LAYER3_PERSONAL_CONTEXT = True  # Enable personal context from bio

# Personal Bio Analysis Settings
PERSONAL_BIO_FILE = 'personal_info.txt'  # Path to personal bio file
BIO_ANALYSIS_CACHE = 'personal_bio_analysis.json'  # Cache file for bio analysis
SENTIMENT_ANALYSIS_ENABLED = True  # Enable sentiment analysis
PERSONALITY_TRAITS_ENABLED = True  # Enable personality trait extraction

# Smart Routing Settings
SMART_ROUTING_ENABLED = True  # Enable smart routing between layers
ROUTING_DECISION_THRESHOLD = 0.7  # Confidence threshold for routing decisions
FALLBACK_TO_LAYER3 = True  # Fallback to Layer 3 if other layers fail
