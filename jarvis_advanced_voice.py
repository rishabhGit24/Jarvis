"""
Advanced Voice System for JARVIS with High-Quality Female Voices
Integrates multiple TTS engines for ultra-realistic speech
"""
import os
import sys
import tempfile
import pygame
import threading
import time
from typing import Optional, Dict, Any
import config

class AdvancedVoiceSystem:
    """Advanced voice system with multiple high-quality TTS engines"""
    
    def __init__(self):
        self.engines = {}
        self.current_engine = None
        self.voice_config = {}
        
        # Initialize pygame for audio playback
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Initialize available engines
        self._initialize_engines()
    
    def _initialize_engines(self):
        """Initialize all available TTS engines"""
        print("🎭 Initializing advanced voice engines...")
        
        # 1. Try Google TTS (gTTS) - High quality, many voices
        try:
            from gtts import gTTS
            self.engines['gtts'] = self._gtts_speak
            print("✅ Google TTS (gTTS) initialized")
        except ImportError:
            print("⚠️  gTTS not available. Install with: pip install gtts")
        
        # 2. Coqui TTS - Ultra-realistic neural voices (optional)
        # Note: Coqui TTS requires Python <3.12, skipping for now
        print("ℹ️  Coqui TTS skipped (requires Python <3.12)")
        
        # 3. Try Azure Cognitive Services (if configured)
        try:
            import azure.cognitiveservices.speech as speechsdk
            if hasattr(config, 'AZURE_SPEECH_KEY') and config.AZURE_SPEECH_KEY:
                self.engines['azure'] = self._azure_speak
                print("✅ Azure Speech Services initialized")
        except ImportError:
            print("⚠️  Azure Speech SDK not available")
        
        # 4. Fallback to system TTS
        try:
            import pyttsx3
            self.engines['system'] = self._system_speak
            print("✅ System TTS (fallback) initialized")
        except ImportError:
            print("❌ No TTS engines available!")
        
        # Set default engine (prioritize Google TTS for quality)
        if 'gtts' in self.engines:
            self.current_engine = 'gtts'
        elif 'azure' in self.engines:
            self.current_engine = 'azure'
        elif 'coqui' in self.engines:
            self.current_engine = 'coqui'
        else:
            self.current_engine = 'system'
        
        print(f"🎯 Using engine: {self.current_engine}")
    
    def _initialize_coqui(self):
        """Initialize Coqui TTS with best female models"""
        try:
            from TTS.api import TTS
            
            # Best female voice models
            female_models = [
                "tts_models/en/ljspeech/tacotron2-DDC",  # High quality female
                "tts_models/en/ljspeech/glow-tts",       # Natural female
                "tts_models/en/jenny/jenny",              # Jenny voice
            ]
            
            # Try to load the best available model
            for model in female_models:
                try:
                    self.coqui_tts = TTS(model_name=model, progress_bar=False)
                    self.voice_config['coqui_model'] = model
                    print(f"✅ Loaded Coqui model: {model}")
                    break
                except Exception as e:
                    print(f"⚠️  Failed to load {model}: {e}")
                    continue
        except Exception as e:
            print(f"❌ Coqui initialization failed: {e}")
    
    def get_available_voices(self) -> Dict[str, list]:
        """Get all available high-quality voices"""
        voices = {
            'Google Cloud Female Voices': [],
            'Azure Premium Female Voices': [],
            'System Voices': []
        }
        
        if 'gtts' in self.engines:
            voices['Google Cloud Female Voices'] = [
                "English (US) - Female",
                "English (UK) - Female", 
                "English (AU) - Female",
                "English (IN) - Female",
                "English (CA) - Female"
            ]
        
        if 'azure' in self.engines:
            voices['Azure Premium Female Voices'] = [
                "Aria - American English Neural",
                "Jenny - American English Neural",
                "Michelle - American English Neural",
                "Libby - British English Neural",
                "Sonia - British English Neural"
            ]
        
        return voices
    
    def set_voice(self, engine: str, voice_id: str = None):
        """Set the active voice engine and voice"""
        if engine in self.engines:
            self.current_engine = engine
            if voice_id:
                self.voice_config[f'{engine}_voice'] = voice_id
                # For gTTS, store the specific voice selection
                if engine == 'gtts':
                    self.current_gtts_voice = voice_id
            print(f"🎭 Voice set to: {engine} - {voice_id or 'default'}")
        else:
            print(f"❌ Engine {engine} not available")
    
    def speak(self, text: str, interrupt_current: bool = True):
        """Speak text using the current engine"""
        if not text or not text.strip():
            return
        
        if self.current_engine and self.current_engine in self.engines:
            try:
                self.engines[self.current_engine](text)
            except Exception as e:
                print(f"❌ Speech failed with {self.current_engine}: {e}")
                # Fallback to system voice
                if 'system' in self.engines:
                    self.engines['system'](text)
        else:
            print("❌ No speech engine available")
    
    def _gtts_speak(self, text: str):
        """Speak using Google TTS with improved reliability and speed"""
        try:
            from gtts import gTTS
            import subprocess
            
            # Get voice settings from the current selection
            voice_setting = getattr(self, 'current_gtts_voice', 'american')
            
            # Map voice selections to gTTS parameters
            voice_map = {
                'English (US) - Female': ('en', 'com'),
                'English (UK) - Female': ('en', 'co.uk'),
                'English (AU) - Female': ('en', 'com.au'),
                'English (IN) - Female': ('en', 'co.in'),
                'English (CA) - Female': ('en', 'ca'),
                'american': ('en', 'com'),
                'british': ('en', 'co.uk'),
                'australian': ('en', 'com.au'),
                'indian': ('en', 'co.in'),
                'canadian': ('en', 'ca')
            }
            
            lang, tld = voice_map.get(voice_setting, ('en', 'com'))
            
            print(f"🎭 Using voice: {voice_setting} (lang={lang}, tld={tld})")
            
            # Create TTS object with timeout and retry logic
            max_retries = 2
            for attempt in range(max_retries):
                try:
                    print(f"🔄 Generating speech (attempt {attempt + 1}/{max_retries})...")
                    tts = gTTS(text=text, lang=lang, tld=tld, slow=False)
                    
                    # Save to temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                        tts.save(tmp_file.name)
                        
                        print(f"✅ Audio generated: {tmp_file.name}")
                        
                        # Use afplay directly (fastest and most reliable on macOS)
                        try:
                            print("🔊 Playing audio...")
                            result = subprocess.run(['afplay', tmp_file.name], 
                                                  check=True, timeout=30)
                            print("✅ Playback completed!")
                            break  # Success, exit retry loop
                            
                        except subprocess.TimeoutExpired:
                            print("⚠️ Playback timeout, continuing...")
                            break
                        except subprocess.CalledProcessError as e:
                            print(f"❌ afplay failed: {e}")
                            # Try alternative method
                            try:
                                subprocess.run(['open', tmp_file.name], check=True)
                                time.sleep(2)  # Give it time to start
                                print("✅ Opened with system player")
                                break
                            except subprocess.CalledProcessError:
                                print("❌ All playback methods failed")
                        
                        finally:
                            # Clean up
                            time.sleep(0.2)
                            try:
                                os.unlink(tmp_file.name)
                            except:
                                pass
                    
                    break  # Success, exit retry loop
                    
                except Exception as e:
                    print(f"⚠️ Attempt {attempt + 1} failed: {e}")
                    if attempt == max_retries - 1:
                        raise  # Last attempt failed
                    time.sleep(1)  # Wait before retry
                
        except Exception as e:
            print(f"❌ gTTS error: {e}")
            raise
    
    def _coqui_speak(self, text: str):
        """Speak using Coqui TTS"""
        try:
            if not hasattr(self, 'coqui_tts'):
                raise Exception("Coqui TTS not initialized")
            
            # Generate speech to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                self.coqui_tts.tts_to_file(text=text, file_path=tmp_file.name)
                
                # Play audio
                pygame.mixer.music.load(tmp_file.name)
                pygame.mixer.music.play()
                
                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                # Clean up
                os.unlink(tmp_file.name)
                
        except Exception as e:
            print(f"Coqui TTS error: {e}")
            raise
    
    def _azure_speak(self, text: str):
        """Speak using Azure Cognitive Services"""
        try:
            import azure.cognitiveservices.speech as speechsdk
            
            # Configure Azure Speech
            speech_config = speechsdk.SpeechConfig(
                subscription=config.AZURE_SPEECH_KEY,
                region=config.AZURE_SPEECH_REGION
            )
            
            # Set high-quality female voice
            speech_config.speech_synthesis_voice_name = "en-US-AriaNeural"
            
            # Create synthesizer
            synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
            
            # Speak
            result = synthesizer.speak_text_async(text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                print("Azure TTS completed successfully")
            else:
                print(f"Azure TTS failed: {result.reason}")
                
        except Exception as e:
            print(f"Azure TTS error: {e}")
            raise
    
    def _system_speak(self, text: str):
        """Fallback to system TTS"""
        try:
            import pyttsx3
            
            engine = pyttsx3.init()
            
            # Try to set a good female voice
            voices = engine.getProperty('voices')
            female_voices = ['samantha', 'victoria', 'allison', 'karen', 'serena']
            
            for voice in voices:
                if voice.name and any(fv in voice.name.lower() for fv in female_voices):
                    engine.setProperty('voice', voice.id)
                    break
            
            engine.setProperty('rate', 280)
            engine.setProperty('volume', 0.9)
            
            engine.say(text)
            engine.runAndWait()
            engine.stop()
            
        except Exception as e:
            print(f"System TTS error: {e}")
            raise
    
    def test_voice(self, engine: str = None):
        """Test the current or specified voice"""
        test_text = "Hello! I'm your advanced AI assistant with ultra-realistic voice synthesis. How does this sound to you?"
        
        if engine:
            original_engine = self.current_engine
            self.set_voice(engine)
            self.speak(test_text)
            self.current_engine = original_engine
        else:
            self.speak(test_text)
    
    def shutdown(self):
        """Cleanup resources"""
        try:
            pygame.mixer.quit()
        except:
            pass

# Global instance
advanced_voice = None

def initialize_advanced_voice():
    """Initialize the advanced voice system"""
    global advanced_voice
    advanced_voice = AdvancedVoiceSystem()
    return advanced_voice

def get_advanced_voice():
    """Get the advanced voice instance"""
    global advanced_voice
    if advanced_voice is None:
        advanced_voice = initialize_advanced_voice()
    return advanced_voice
