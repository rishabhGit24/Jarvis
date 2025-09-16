#!/usr/bin/env python3
"""
Test JARVIS Ultra-Realistic Voice System
Demo the natural conversation patterns and female voices
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from jarvis_voice import JarvisVoice
import time

def test_realistic_conversation():
    """Test the ultra-realistic conversation patterns"""
    print("🎭 TESTING ULTRA-REALISTIC JARVIS CONVERSATION")
    print("=" * 60)
    
    # Initialize voice system
    print("Initializing voice system...")
    voice = JarvisVoice()
    
    # Test various realistic conversation scenarios
    test_phrases = [
        # Natural responses
        "I have found the file you were looking for.",
        "I am currently processing your request.",
        "That is a great question about machine learning.",
        "I will search for that information right away.",
        "I cannot locate that file at the moment.",
        "You are absolutely right about that.",
        
        # Emotional responses
        "I found three documents that match your search.",
        "I apologize for the error in processing.",
        "What would you like me to help you with today?",
        "The weather forecast looks quite interesting.",
        
        # Complex responses
        "Based on my analysis of the system performance, everything looks optimal.",
        "I understand you want to know about artificial intelligence applications.",
        "Let me search through your files to find the presentation you mentioned.",
        
        # Questions and curiosity
        "Would you like me to open the file for you?",
        "Are you looking for a specific type of document?",
        "What else can I help you with?",
    ]
    
    print("\n🔊 Testing realistic conversation patterns:")
    print("(Each phrase will be spoken with natural human-like patterns)\n")
    
    for i, phrase in enumerate(test_phrases, 1):
        print(f"{i:2d}. Original: {phrase}")
        
        # Let JARVIS process and speak the phrase
        voice.speak(phrase)
        
        # Small pause between phrases
        time.sleep(2)
        
        # Ask if user wants to continue every 5 phrases
        if i % 5 == 0 and i < len(test_phrases):
            response = input(f"\nContinue testing? ({len(test_phrases) - i} phrases remaining) [y/N]: ").strip().lower()
            if response not in ['y', 'yes']:
                break
            print()
    
    print("\n✅ Realistic conversation test completed!")
    print("\n🎯 Key features demonstrated:")
    print("   • Natural contractions (I'll, you're, can't)")
    print("   • Conversational starters (Well, So, Right)")
    print("   • Emotional expressions (Great!, Oh dear, Hmm)")
    print("   • Accent-specific vocabulary")
    print("   • Natural addressing patterns")
    print("   • Human-like speech hesitations")

def test_female_voices():
    """Test available female voices"""
    print("\n🎵 TESTING FEMALE VOICE OPTIONS")
    print("=" * 60)
    
    import pyttsx3
    
    # Get all available voices
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    # Find female voices
    female_voices = []
    female_keywords = ['victoria', 'allison', 'ava', 'samantha', 'susan', 'serena', 'kate', 'emily', 'karen', 'catherine', 'veena', 'fiona', 'monica', 'alice']
    
    for voice in voices:
        if voice.name:
            for keyword in female_keywords:
                if keyword in voice.name.lower():
                    female_voices.append(voice)
                    break
    
    if not female_voices:
        print("No female voices found on this system.")
        return
    
    print(f"Found {len(female_voices)} female voices:")
    for i, voice in enumerate(female_voices, 1):
        print(f"{i:2d}. {voice.name}")
    
    # Test a sample phrase with each voice
    test_phrase = "Hello! I'm your AI assistant. How can I help you today?"
    
    print(f"\nTesting phrase: '{test_phrase}'\n")
    
    for voice in female_voices:
        try:
            print(f"🔊 Testing: {voice.name}")
            
            # Create fresh engine for each voice
            test_engine = pyttsx3.init()
            test_engine.setProperty('voice', voice.id)
            test_engine.setProperty('rate', 280)
            test_engine.setProperty('volume', 1.0)
            
            test_engine.say(test_phrase)
            test_engine.runAndWait()
            test_engine.stop()
            
            time.sleep(1)
            
        except Exception as e:
            print(f"   ❌ Error testing {voice.name}: {e}")
    
    engine.stop()

def main():
    try:
        print("🎭 JARVIS ULTRA-REALISTIC VOICE TESTER")
        print("=" * 60)
        print("This will test:")
        print("1. Ultra-realistic conversation patterns")
        print("2. Natural human-like speech")
        print("3. Female voice options")
        print("4. Emotional expressions")
        print("5. Accent-specific vocabulary")
        print()
        
        choice = input("What would you like to test?\n1. Realistic conversation\n2. Female voices\n3. Both\nChoice (1-3): ").strip()
        
        if choice == '1':
            test_realistic_conversation()
        elif choice == '2':
            test_female_voices()
        elif choice == '3':
            test_realistic_conversation()
            test_female_voices()
        else:
            print("Invalid choice. Testing realistic conversation...")
            test_realistic_conversation()
            
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    main()
