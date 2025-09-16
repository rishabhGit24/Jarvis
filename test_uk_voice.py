#!/usr/bin/env python3
"""
Test UK Female Voice for JARVIS
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from jarvis_advanced_voice import AdvancedVoiceSystem

def main():
    print("🇬🇧 TESTING UK FEMALE VOICE")
    print("=" * 40)
    
    # Initialize voice system
    voice_system = AdvancedVoiceSystem()
    
    # Set UK female voice
    voice_system.set_voice('gtts', 'English (UK) - Female')
    
    # Test phrases with British expressions
    test_phrases = [
        "Good evening, Mr. Bharadwaj Sir. How may I assist you today?",
        "Certainly, Mr. Bharadwaj. I shall be delighted to help with that.",
        "Right away, Sir. I'm processing your request with utmost care.",
        "Brilliant! That's absolutely spot on, Mr. Bharadwaj.",
        "I do hope you're having a lovely day, Sir. What can I do for you?"
    ]
    
    print("🎭 Testing UK Female Voice with British expressions...\n")
    
    for i, phrase in enumerate(test_phrases, 1):
        print(f"{i}. 🔊 Speaking: \"{phrase}\"")
        try:
            voice_system.speak(phrase)
            print("   ✅ Success!\n")
        except Exception as e:
            print(f"   ❌ Error: {e}\n")
    
    print("🎯 UK Female Voice Test Complete!")
    print("This is your new JARVIS voice - elegant British female accent!")
    
    voice_system.shutdown()

if __name__ == "__main__":
    main()
