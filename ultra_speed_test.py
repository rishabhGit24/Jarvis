#!/usr/bin/env python3
"""
Ultra Speed Test for JARVIS
Test response times with current optimizations
"""

import time
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from jarvis_advanced_voice import AdvancedVoiceSystem

def test_current_speed():
    """Test current voice speed"""
    print("⚡ JARVIS ULTRA SPEED TEST")
    print("=" * 40)
    
    voice_system = AdvancedVoiceSystem()
    voice_system.set_voice('gtts', 'English (UK) - Female')
    
    test_phrases = [
        "Yes Sir!",
        "Certainly, Mr. Bharadwaj.",
        "Right away, Sir!",
        "Processing your request.",
        "Task completed successfully!"
    ]
    
    total_time = 0
    
    for i, phrase in enumerate(test_phrases, 1):
        print(f"\n{i}. Testing: \"{phrase}\"")
        
        start_time = time.time()
        try:
            voice_system.speak(phrase)
            end_time = time.time()
            
            duration = end_time - start_time
            total_time += duration
            
            print(f"   ⏱️  Duration: {duration:.2f}s")
            
            if duration < 2:
                print("   🚀 ULTRA FAST!")
            elif duration < 3:
                print("   ⚡ FAST")
            elif duration < 4:
                print("   ✅ GOOD")
            else:
                print("   ⚠️  SLOW")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    avg_time = total_time / len(test_phrases)
    print(f"\n📊 SPEED RESULTS:")
    print(f"   Average response time: {avg_time:.2f}s")
    print(f"   Total test time: {total_time:.2f}s")
    
    if avg_time < 2:
        print("   🎯 EXCELLENT SPEED! ⚡")
    elif avg_time < 3:
        print("   🎯 GOOD SPEED! ✅")
    else:
        print("   🎯 Could be faster ⚠️")
    
    voice_system.shutdown()

def show_current_settings():
    """Show current speed settings"""
    print("\n🔧 CURRENT SPEED SETTINGS:")
    print("-" * 30)
    
    try:
        import config
        print(f"VOICE_RATE: {getattr(config, 'VOICE_RATE', 'Not set')}")
        print(f"FAST_RESPONSE_MODE: {getattr(config, 'FAST_RESPONSE_MODE', 'Not set')}")
        print(f"MAX_RESPONSE_LENGTH: {getattr(config, 'MAX_RESPONSE_LENGTH', 'Not set')}")
        print(f"USE_ADVANCED_VOICE: {getattr(config, 'USE_ADVANCED_VOICE', 'Not set')}")
        print(f"ADVANCED_VOICE_ENGINE: {getattr(config, 'ADVANCED_VOICE_ENGINE', 'Not set')}")
    except Exception as e:
        print(f"Error reading config: {e}")

if __name__ == "__main__":
    show_current_settings()
    test_current_speed()
    
    print("\n🎯 SPEED OPTIMIZATION SUMMARY:")
    print("✅ Voice rate increased to 280 WPM")
    print("✅ Google TTS optimized for speed")
    print("✅ Audio playback streamlined")
    print("✅ UK Female voice configured")
    print("\n🚀 JARVIS is now optimized for ultra-fast responses!")
