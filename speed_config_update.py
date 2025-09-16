#!/usr/bin/env python3
"""
JARVIS Speed Optimization Update
Applies comprehensive speed improvements to all systems
"""

def update_config_for_speed():
    """Update config.py with speed optimizations"""
    
    speed_additions = """
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
"""

    try:
        with open('config.py', 'r') as f:
            content = f.read()
        
        # Add speed settings if not already present
        if "SPEED OPTIMIZATION SETTINGS" not in content:
            content += speed_additions
            
            with open('config.py', 'w') as f:
                f.write(content)
            
            print("✅ Speed optimization settings added to config.py")
        else:
            print("ℹ️  Speed settings already exist in config.py")
            
    except Exception as e:
        print(f"❌ Error updating config: {e}")

def update_voice_speeds():
    """Update all voice speed settings"""
    
    files_to_update = [
        ('jarvis_voice.py', 'fallback_engine.setProperty(\'rate\', 190)', 'fallback_engine.setProperty(\'rate\', 280)'),
        ('jarvis_advanced_voice.py', 'engine.setProperty(\'rate\', 180)', 'engine.setProperty(\'rate\', 280)'),
        ('test_realistic_voice.py', 'test_engine.setProperty(\'rate\', 180)', 'test_engine.setProperty(\'rate\', 280)'),
        ('voice_selector.py', 'engine.setProperty(\'rate\', 180)', 'engine.setProperty(\'rate\', 280)'),
    ]
    
    for filename, old_line, new_line in files_to_update:
        try:
            with open(filename, 'r') as f:
                content = f.read()
            
            if old_line in content:
                content = content.replace(old_line, new_line)
                
                with open(filename, 'w') as f:
                    f.write(content)
                
                print(f"✅ Updated voice speed in {filename}")
            else:
                print(f"ℹ️  {filename} already optimized or not found")
                
        except FileNotFoundError:
            print(f"⚠️  {filename} not found")
        except Exception as e:
            print(f"❌ Error updating {filename}: {e}")

if __name__ == "__main__":
    print("🚀 JARVIS SPEED OPTIMIZATION")
    print("=" * 40)
    
    print("\n1. Updating configuration for speed...")
    update_config_for_speed()
    
    print("\n2. Updating voice speeds...")
    update_voice_speeds()
    
    print("\n✅ SPEED OPTIMIZATION COMPLETE!")
    print("🎯 JARVIS will now respond much faster!")
    print("🚀 Restart JARVIS to apply all changes")
