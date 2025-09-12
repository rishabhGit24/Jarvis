"""
Setup script for JARVIS Personal Assistant
Handles installation, configuration, and initial setup
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - Compatible")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Install basic requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Basic dependencies installed successfully")
        
        # Try to install PyAudio with system-specific instructions
        try:
            import pyaudio
            print("✅ PyAudio already installed")
        except ImportError:
            print("🔧 Installing PyAudio...")
            install_pyaudio()
            
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def install_pyaudio():
    """Install PyAudio with system-specific handling"""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        print("🍎 macOS detected - Installing PyAudio...")
        try:
            # Try to install with pip first
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyaudio"])
            print("✅ PyAudio installed successfully")
        except subprocess.CalledProcessError:
            print("⚠️  PyAudio installation failed. You may need to install portaudio first:")
            print("   Run: brew install portaudio")
            print("   Then: pip install pyaudio")
            
    elif system == "Windows":
        print("🪟 Windows detected - Installing PyAudio...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyaudio"])
            print("✅ PyAudio installed successfully")
        except subprocess.CalledProcessError:
            print("⚠️  PyAudio installation failed. Try:")
            print("   pip install pipwin")
            print("   pipwin install pyaudio")
            
    elif system == "Linux":
        print("🐧 Linux detected - Installing PyAudio...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyaudio"])
            print("✅ PyAudio installed successfully")
        except subprocess.CalledProcessError:
            print("⚠️  PyAudio installation failed. You may need to install system dependencies:")
            print("   Ubuntu/Debian: sudo apt-get install python3-pyaudio")
            print("   CentOS/RHEL: sudo yum install python3-pyaudio")

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    print("\n🔧 Creating configuration file...")
    
    env_content = """# JARVIS Personal Assistant Configuration
# 
# Weather API Key (Optional but recommended)
# Get your free API key from: https://openweathermap.org/api
WEATHER_API_KEY=

# User Settings
USER_NAME=Mr. Bharadwaj
USER_LOCATION=New York

# Voice Settings (Advanced)
VOICE_RATE=180
VOICE_VOLUME=0.9
"""
    
    try:
        with open(".env", "w") as f:
            f.write(env_content)
        print("✅ Configuration file created: .env")
        print("📝 Edit .env to add your API keys and preferences")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def test_installation():
    """Test if all components can be imported"""
    print("\n🧪 Testing installation...")
    
    components = [
        ("speech_recognition", "Speech Recognition"),
        ("pyttsx3", "Text-to-Speech"),
        ("requests", "HTTP Requests"),
        ("colorama", "Terminal Colors"),
        ("rich", "Rich Terminal Display"),
        ("psutil", "System Information"),
        ("wikipedia", "Wikipedia Integration")
    ]
    
    all_good = True
    
    for module, name in components:
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} - Import failed")
            all_good = False
    
    return all_good

def setup_voice_test():
    """Test voice system"""
    print("\n🎤 Testing voice system...")
    
    try:
        import pyttsx3
        engine = pyttsx3.init()
        
        # Test TTS
        print("🔊 Testing text-to-speech...")
        engine.say("Voice system test successful, Sir.")
        engine.runAndWait()
        
        print("✅ Text-to-speech working")
        
        # Test microphone
        try:
            import speech_recognition as sr
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("🎙️  Testing microphone... (This may take a moment)")
                r.adjust_for_ambient_noise(source, duration=1)
            print("✅ Microphone access working")
            
        except Exception as e:
            print(f"⚠️  Microphone test failed: {e}")
            print("   You may need to grant microphone permissions")
            
        return True
        
    except Exception as e:
        print(f"❌ Voice system test failed: {e}")
        return False

def create_launcher_script():
    """Create convenient launcher scripts"""
    print("\n🚀 Creating launcher scripts...")
    
    # Create bash script for Unix systems
    if platform.system() in ["Darwin", "Linux"]:
        launcher_content = f"""#!/bin/bash
# JARVIS Launcher Script
cd "{os.getcwd()}"
python3 jarvis.py "$@"
"""
        try:
            with open("start_jarvis.sh", "w") as f:
                f.write(launcher_content)
            os.chmod("start_jarvis.sh", 0o755)
            print("✅ Created start_jarvis.sh")
        except Exception as e:
            print(f"⚠️  Failed to create launcher script: {e}")
    
    # Create batch script for Windows
    if platform.system() == "Windows":
        launcher_content = f"""@echo off
REM JARVIS Launcher Script
cd /d "{os.getcwd()}"
python jarvis.py %*
pause
"""
        try:
            with open("start_jarvis.bat", "w") as f:
                f.write(launcher_content)
            print("✅ Created start_jarvis.bat")
        except Exception as e:
            print(f"⚠️  Failed to create launcher script: {e}")

def display_next_steps():
    """Display next steps for the user"""
    print("\n" + "="*60)
    print("🎉 JARVIS SETUP COMPLETE!")
    print("="*60)
    
    print("\n📋 Next Steps:")
    print("1. 🔑 Get a weather API key (optional but recommended):")
    print("   • Visit: https://openweathermap.org/api")
    print("   • Sign up for free account")
    print("   • Copy API key to .env file")
    
    print("\n2. 🚀 Start JARVIS:")
    print("   • Run: python jarvis.py")
    print("   • Or use: ./start_jarvis.sh (Unix) or start_jarvis.bat (Windows)")
    
    print("\n3. 🎤 First Run:")
    print("   • Grant microphone permissions when prompted")
    print("   • Say 'Jarvis' to activate voice commands")
    print("   • Try: 'Jarvis, what can you do?'")
    
    print("\n📖 Documentation:")
    print("   • Read README.md for detailed usage guide")
    print("   • Run 'python jarvis.py --help' for command options")
    print("   • Run 'python jarvis.py --diagnostics' to test systems")
    
    print("\n🎭 Example Commands:")
    print("   • 'Jarvis, find my document.txt'")
    print("   • 'What's the weather like?'")
    print("   • 'What is artificial intelligence?'")
    print("   • 'System status report'")
    
    print(f"\n✨ Welcome to JARVIS, Mr. Bharadwaj!")
    print("   At your service, Sir. 🎩")

def main():
    """Main setup function"""
    print("🤖 JARVIS Personal Assistant Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed during dependency installation")
        sys.exit(1)
    
    # Create configuration file
    if not create_env_file():
        print("\n⚠️  Configuration file creation failed, but continuing...")
    
    # Test installation
    if not test_installation():
        print("\n❌ Some components failed to install correctly")
        print("Please check the error messages above and try again")
        sys.exit(1)
    
    # Test voice system
    setup_voice_test()
    
    # Create launcher scripts
    create_launcher_script()
    
    # Show next steps
    display_next_steps()

if __name__ == "__main__":
    main()
