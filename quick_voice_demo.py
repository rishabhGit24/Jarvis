#!/usr/bin/env python3
"""
Quick Voice Demo for JARVIS
Test all female voices with short samples
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from jarvis_advanced_voice import AdvancedVoiceSystem
import time

def main():
    print("🎭 JARVIS QUICK VOICE DEMO")
    print("=" * 50)
    print("🚀 Testing all female voices with short samples!")
    print()
    
    # Initialize voice system
    voice_system = AdvancedVoiceSystem()
    
    # Define voices to test
    voices_to_test = [
        ("English (US) - Female", "Hello! I'm an American female voice."),
        ("English (UK) - Female", "Hello! I'm a British female voice."),
        ("English (AU) - Female", "G'day! I'm an Australian female voice."),
        ("English (IN) - Female", "Hello! I'm an Indian English female voice."),
        ("English (CA) - Female", "Hello! I'm a Canadian female voice, eh?")
    ]
    
    print("🔊 Starting voice demonstrations...")
    print("(Each voice will speak a short phrase)")
    print()
    
    for i, (voice_name, test_text) in enumerate(voices_to_test, 1):
        print(f"\n{i}. 🎵 Testing: {voice_name}")
        print(f"   📝 Text: \"{test_text}\"")
        
        try:
            # Set the specific voice
            voice_system.set_voice('gtts', voice_name)
            
            # Speak the text
            voice_system.speak(test_text)
            
            print("   ✅ Voice test completed!")
            
            # Small pause between voices
            time.sleep(1)
            
        except Exception as e:
            print(f"   ❌ Voice test failed: {e}")
            continue
    
    print("\n" + "=" * 50)
    print("🎯 VOICE DEMO COMPLETE!")
    print()
    
    # Ask user which voice they preferred
    print("Which voice did you like best?")
    for i, (voice_name, _) in enumerate(voices_to_test, 1):
        print(f"{i}. {voice_name}")
    
    try:
        choice = input("\nEnter choice (1-5) or 0 to skip: ").strip()
        
        if choice in ['1', '2', '3', '4', '5']:
            choice_num = int(choice) - 1
            selected_voice = voices_to_test[choice_num][0]
            
            print(f"\n🎭 You selected: {selected_voice}")
            print("🔧 Configuring JARVIS to use this voice...")
            
            # Update config
            if update_jarvis_config(selected_voice):
                print("✅ JARVIS voice updated successfully!")
                print(f"🚀 Run 'python3 jarvis.py' to use your new voice!")
            else:
                print("❌ Failed to update configuration")
        else:
            print("👋 No voice selected. Goodbye!")
            
    except KeyboardInterrupt:
        print("\n👋 Demo cancelled.")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        voice_system.shutdown()

def update_jarvis_config(selected_voice: str) -> bool:
    """Update JARVIS configuration with selected voice"""
    try:
        # Read current config
        with open('config.py', 'r') as f:
            content = f.read()
        
        # Add advanced voice configuration
        advanced_config = f"""
# Ultra-Realistic Voice Configuration
USE_ADVANCED_VOICE = True
ADVANCED_VOICE_ENGINE = 'gtts'
ADVANCED_VOICE_DESCRIPTION = '{selected_voice}'
SELECTED_FEMALE_VOICE = '{selected_voice}'
"""
        
        # Check if advanced voice config already exists
        if "USE_ADVANCED_VOICE" in content:
            # Update existing configuration
            lines = content.split('\n')
            new_lines = []
            skip_next = False
            
            for line in lines:
                if skip_next:
                    skip_next = False
                    continue
                    
                if line.strip().startswith('USE_ADVANCED_VOICE'):
                    new_lines.append(f"USE_ADVANCED_VOICE = True")
                elif line.strip().startswith('ADVANCED_VOICE_ENGINE'):
                    new_lines.append(f"ADVANCED_VOICE_ENGINE = 'gtts'")
                elif line.strip().startswith('ADVANCED_VOICE_DESCRIPTION'):
                    new_lines.append(f"ADVANCED_VOICE_DESCRIPTION = '{selected_voice}'")
                elif line.strip().startswith('SELECTED_FEMALE_VOICE'):
                    new_lines.append(f"SELECTED_FEMALE_VOICE = '{selected_voice}'")
                else:
                    new_lines.append(line)
            
            content = '\n'.join(new_lines)
        else:
            # Add new configuration
            content += advanced_config
        
        # Write back to file
        with open('config.py', 'w') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"Config update error: {e}")
        return False

if __name__ == "__main__":
    main()
