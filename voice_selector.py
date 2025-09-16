#!/usr/bin/env python3
"""
JARVIS Voice Selector
Choose specific voices within accents and test them
"""

import pyttsx3
import os
import sys

def get_all_system_voices():
    """Get all available system voices"""
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.stop()
        return voices
    except Exception as e:
        print(f"Error getting voices: {e}")
        return []

def categorize_voices():
    """Categorize voices by accent/language"""
    voices = get_all_system_voices()
    
    categories = {
        'British': [],
        'American': [],
        'Australian': [],
        'Indian': [],
        'Irish': [],
        'Scottish': [],
        'French': [],
        'German': [],
        'Spanish': [],
        'Italian': [],
        'Other': []
    }
    
    # Categorization keywords
    keywords = {
        'British': ['daniel', 'oliver', 'serena', 'kate', 'gb', 'british', 'uk'],
        'American': ['alex', 'fred', 'victoria', 'allison', 'tom', 'bruce', 'ralph', 'us', 'american'],
        'Australian': ['karen', 'lee', 'catherine', 'au', 'australian'],
        'Indian': ['rishi', 'veena', 'lekha', 'in', 'indian'],
        'Irish': ['moira', 'fiona', 'ie', 'irish'],
        'Scottish': ['fiona', 'moira', 'scottish'],
        'French': ['thomas', 'aurelie', 'fr', 'french'],
        'German': ['anna', 'yannick', 'de', 'german'],
        'Spanish': ['monica', 'jorge', 'es', 'spanish'],
        'Italian': ['luca', 'alice', 'it', 'italian']
    }
    
    for voice in voices:
        if not voice.name:
            continue
            
        voice_name_lower = voice.name.lower()
        voice_id_lower = voice.id.lower() if voice.id else ""
        
        categorized = False
        for category, kw_list in keywords.items():
            if any(kw in voice_name_lower or kw in voice_id_lower for kw in kw_list):
                categories[category].append(voice)
                categorized = True
                break
        
        if not categorized:
            categories['Other'].append(voice)
    
    return categories

def test_voice(voice):
    """Test a specific voice"""
    try:
        engine = pyttsx3.init()
        engine.setProperty('voice', voice.id)
        engine.setProperty('rate', 280)
        engine.setProperty('volume', 1.0)
        
        test_text = "Hello, Mr. Bharadwaj Sir. This is how I sound with this voice."
        print(f"Testing voice: {voice.name}")
        print(f"Speaking: {test_text}")
        
        engine.say(test_text)
        engine.runAndWait()
        engine.stop()
        return True
    except Exception as e:
        print(f"Error testing voice: {e}")
        return False

def update_voice_preference(accent, voice_name):
    """Update the voice preference in config.py"""
    try:
        with open('config.py', 'r') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        # Update accent
        for i, line in enumerate(lines):
            if line.strip().startswith('VOICE_ACCENT'):
                lines[i] = f"VOICE_ACCENT = '{accent.lower()}'  # Change this to your preferred accent"
                break
        
        # Update preferred voice
        for i, line in enumerate(lines):
            if line.strip().startswith('PREFERRED_VOICE'):
                lines[i] = f"PREFERRED_VOICE = '{voice_name.lower()}'  # Set specific voice name or leave empty"
                break
        
        with open('config.py', 'w') as f:
            f.write('\n'.join(lines))
        
        return True
    except Exception as e:
        print(f"Error updating config: {e}")
        return False

def main():
    print("🎭 JARVIS VOICE SELECTOR")
    print("=" * 60)
    
    print("Scanning available system voices...")
    categories = categorize_voices()
    
    # Show available voices by category
    voice_options = {}
    option_num = 1
    
    for category, voices in categories.items():
        if voices:  # Only show categories with voices
            print(f"\n📢 {category} Voices:")
            print("-" * 30)
            for voice in voices:
                gender = getattr(voice, 'gender', 'Unknown')
                print(f"{option_num:2d}. {voice.name} ({gender})")
                voice_options[option_num] = (category, voice)
                option_num += 1
    
    if not voice_options:
        print("No voices found!")
        return
    
    print(f"\n0. Exit")
    print("\n" + "=" * 60)
    
    try:
        while True:
            choice = input(f"\nSelect voice to test (1-{len(voice_options)}, 0 to exit): ").strip()
            
            if choice == '0':
                print("Goodbye!")
                break
            
            try:
                choice_num = int(choice)
                if choice_num in voice_options:
                    category, voice = voice_options[choice_num]
                    
                    print(f"\n🔊 Testing {voice.name} ({category})...")
                    if test_voice(voice):
                        
                        # Ask if user wants to set this voice
                        set_voice = input(f"\nSet {voice.name} as JARVIS voice? (y/N): ").strip().lower()
                        if set_voice in ['y', 'yes']:
                            voice_name = voice.name.split()[0].lower()  # Get first name
                            
                            if update_voice_preference(category, voice_name):
                                print(f"\n✅ SUCCESS!")
                                print(f"   Accent: {category}")
                                print(f"   Voice: {voice.name}")
                                print(f"\n🎯 Restart JARVIS to use the new voice:")
                                print(f"   source jarvis_env/bin/activate && python3 jarvis.py")
                                break
                            else:
                                print("❌ Failed to update configuration")
                    else:
                        print("❌ Voice test failed")
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Please enter a number!")
                
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")

if __name__ == "__main__":
    main()
