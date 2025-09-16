#!/usr/bin/env python3
"""
Test Audio Playback for JARVIS
Verify that audio can be played properly on the system
"""

import os
import sys
import tempfile
import subprocess
import time

def test_system_audio():
    """Test if system audio playback works"""
    print("🔊 Testing system audio playback...")
    
    # Test 1: afplay (macOS built-in)
    print("\n1. Testing afplay (macOS audio player)...")
    try:
        # Create a simple test using say command
        result = subprocess.run(['say', 'Testing audio playback'], timeout=10)
        if result.returncode == 0:
            print("✅ afplay/say works!")
        else:
            print("❌ afplay/say failed")
    except Exception as e:
        print(f"❌ afplay/say error: {e}")
    
    # Test 2: Google TTS
    print("\n2. Testing Google TTS...")
    try:
        from gtts import gTTS
        
        # Create TTS
        tts = gTTS(text="Hello! This is a Google TTS test.", lang='en', tld='com')
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tts.save(tmp_file.name)
            print(f"📁 Audio saved to: {tmp_file.name}")
            
            # Try to play with afplay
            try:
                print("🔊 Playing with afplay...")
                subprocess.run(['afplay', tmp_file.name], check=True)
                print("✅ Google TTS + afplay works!")
            except subprocess.CalledProcessError as e:
                print(f"❌ afplay failed: {e}")
                
                # Try with open
                try:
                    print("🔊 Trying with 'open' command...")
                    subprocess.run(['open', tmp_file.name], check=True)
                    time.sleep(3)  # Wait for playback
                    print("✅ Google TTS + open works!")
                except subprocess.CalledProcessError as e2:
                    print(f"❌ open failed: {e2}")
            
            # Cleanup
            try:
                os.unlink(tmp_file.name)
            except:
                pass
                
    except ImportError:
        print("❌ gTTS not installed")
    except Exception as e:
        print(f"❌ Google TTS error: {e}")
    
    # Test 3: Pygame
    print("\n3. Testing pygame audio...")
    try:
        import pygame
        pygame.mixer.init()
        print("✅ Pygame mixer initialized")
        
        # Test with a simple tone (if available)
        try:
            # Create a simple test tone
            import numpy as np
            duration = 1  # seconds
            sample_rate = 22050
            frequency = 440  # A4 note
            
            t = np.linspace(0, duration, int(sample_rate * duration))
            wave = np.sin(2 * np.pi * frequency * t)
            
            # Convert to pygame format
            sound_array = (wave * 32767).astype(np.int16)
            stereo_array = np.zeros((len(sound_array), 2), dtype=np.int16)
            stereo_array[:, 0] = sound_array
            stereo_array[:, 1] = sound_array
            
            sound = pygame.sndarray.make_sound(stereo_array)
            sound.play()
            time.sleep(1.5)
            print("✅ Pygame audio test successful!")
            
        except ImportError:
            print("ℹ️  NumPy not available for pygame tone test")
        except Exception as e:
            print(f"⚠️  Pygame tone test failed: {e}")
            
        pygame.mixer.quit()
        
    except ImportError:
        print("❌ pygame not installed")
    except Exception as e:
        print(f"❌ pygame error: {e}")

def check_audio_system():
    """Check audio system configuration"""
    print("\n🔍 Checking audio system...")
    
    # Check if audio devices are available
    try:
        result = subprocess.run(['system_profiler', 'SPAudioDataType'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Audio system information available")
            # Look for output devices
            if "Output" in result.stdout:
                print("✅ Audio output devices found")
            else:
                print("⚠️  No audio output devices found")
        else:
            print("❌ Could not get audio system info")
    except Exception as e:
        print(f"❌ Audio system check failed: {e}")

if __name__ == "__main__":
    print("🎵 JARVIS AUDIO SYSTEM TEST")
    print("=" * 50)
    
    check_audio_system()
    test_system_audio()
    
    print("\n" + "=" * 50)
    print("🎯 RECOMMENDATIONS:")
    print("   - If 'say' works, system audio is fine")
    print("   - If Google TTS works, advanced voices will work")
    print("   - Make sure your volume is turned up!")
    print("   - Check System Preferences > Sound > Output")
