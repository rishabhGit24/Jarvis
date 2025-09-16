#!/usr/bin/env python3
"""
Ultra-Realistic Voice Selector for JARVIS
Choose from high-quality neural TTS voices that sound like real people
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from jarvis_advanced_voice import AdvancedVoiceSystem
import time

def main():
    print("🎭 JARVIS ULTRA-REALISTIC VOICE SELECTOR")
    print("=" * 70)
    print("🚀 This system provides MUCH better, human-like voices!")
    print("🎯 No more robotic speech - these voices sound like real people!")
    print()
    
    # Initialize advanced voice system
    print("🔧 Initializing advanced voice engines...")
    voice_system = AdvancedVoiceSystem()
    
    # Get available voices
    available_voices = voice_system.get_available_voices()
    
    print("\n🎵 AVAILABLE ULTRA-REALISTIC VOICES:")
    print("=" * 70)
    
    option_num = 1
    voice_options = {}
    
    for category, voices in available_voices.items():
        if voices:  # Only show categories with available voices
            print(f"\n📢 {category}:")
            print("-" * 50)
            
            for voice in voices:
                print(f"{option_num:2d}. {voice}")
                voice_options[option_num] = (category, voice)
                option_num += 1
    
    if not voice_options:
        print("❌ No advanced voice engines available!")
        print("\n🔧 Installing required packages...")
        install_packages()
        return
    
    print(f"\n0. Exit")
    print("\n" + "=" * 70)
    
    try:
        while True:
            choice = input(f"\nSelect voice to test (1-{len(voice_options)}, 0 to exit): ").strip()
            
            if choice == '0':
                print("👋 Goodbye!")
                break
            
            try:
                choice_num = int(choice)
                if choice_num in voice_options:
                    category, voice_desc = voice_options[choice_num]
                    
                    print(f"\n🔊 Testing: {voice_desc}")
                    print("🎭 This will sound MUCH more realistic than system voices!")
                    
                    # Determine engine and test
                    if "Neural (Coqui)" in category:
                        voice_system.set_voice('coqui', voice_desc)
                        test_text = "Hello! I'm your ultra-realistic AI assistant. This neural voice sounds much more human and natural than traditional text-to-speech. How do you like this quality?"
                    elif "Google Cloud" in category:
                        voice_system.set_voice('gtts', voice_desc)
                        test_text = f"Hi there! I'm using {voice_desc.lower()} from Google's advanced text-to-speech. This voice has natural intonation and rhythm that makes conversations feel genuine and engaging. Can you hear the difference in accent and tone?"
                    elif "Azure Premium" in category:
                        voice_system.set_voice('azure', voice_desc)
                        test_text = "Greetings! I'm powered by Microsoft Azure's premium neural voices. These voices are trained on real human speech patterns for incredibly lifelike results."
                    else:
                        voice_system.set_voice('system', voice_desc)
                        test_text = "Hello! Even this system voice has been optimized for better quality and naturalness."
                    
                    print(f"Speaking: {test_text}")
                    voice_system.speak(test_text)
                    
                    # Ask if user wants to set this voice
                    print("\n" + "=" * 50)
                    set_voice = input(f"🎯 Use this voice for JARVIS? (y/N): ").strip().lower()
                    
                    if set_voice in ['y', 'yes']:
                        # Update configuration
                        engine = None
                        if "Neural (Coqui)" in category:
                            engine = 'coqui'
                        elif "Google Cloud" in category:
                            engine = 'gtts'
                        elif "Azure Premium" in category:
                            engine = 'azure'
                        else:
                            engine = 'system'
                        
                        if update_jarvis_voice_config(engine, voice_desc):
                            print(f"\n✅ SUCCESS! JARVIS voice updated!")
                            print(f"   🎭 Engine: {engine}")
                            print(f"   🎵 Voice: {voice_desc}")
                            print(f"\n🚀 Your JARVIS now has an ultra-realistic voice!")
                            print(f"   Run: python3 jarvis.py")
                            break
                        else:
                            print("❌ Failed to update configuration")
                    
                else:
                    print("❌ Invalid choice!")
                    
            except ValueError:
                print("❌ Please enter a number!")
                
    except KeyboardInterrupt:
        print("\n\n👋 Cancelled by user.")
    
    finally:
        voice_system.shutdown()

def install_packages():
    """Install required packages for advanced voices"""
    print("📦 Installing advanced TTS packages...")
    
    packages = [
        "gtts>=2.3.0",
        "pygame>=2.1.0", 
        "TTS>=0.22.0"
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        os.system(f"pip install {package}")
    
    print("✅ Installation complete! Please run the script again.")

def update_jarvis_voice_config(engine: str, voice_desc: str) -> bool:
    """Update JARVIS configuration to use the selected voice"""
    try:
        # Read current config
        with open('config.py', 'r') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        # Add or update advanced voice settings
        advanced_voice_config = f"""
# Advanced Voice Engine Settings
ADVANCED_VOICE_ENGINE = '{engine}'  # coqui, gtts, azure, system
ADVANCED_VOICE_DESCRIPTION = '{voice_desc}'
USE_ADVANCED_VOICE = True  # Enable ultra-realistic voices
"""
        
        # Find where to insert the config
        insert_index = -1
        for i, line in enumerate(lines):
            if line.strip().startswith('# File Search Settings'):
                insert_index = i
                break
        
        if insert_index != -1:
            lines.insert(insert_index, advanced_voice_config)
        else:
            lines.append(advanced_voice_config)
        
        # Write back to file
        with open('config.py', 'w') as f:
            f.write('\n'.join(lines))
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating config: {e}")
        return False

if __name__ == "__main__":
    main()
