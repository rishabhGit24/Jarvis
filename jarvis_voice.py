"""
Voice Recognition and Text-to-Speech System for Jarvis
Handles speech input/output with British accent
"""
import speech_recognition as sr
import pyttsx3
import threading
import queue
import time
from typing import Optional
import config

class JarvisVoice:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = self._setup_tts()
        self.is_listening = False
        self.audio_queue = queue.Queue()

        # Calibrate microphone for ambient noise
        self._calibrate_microphone()

    def _setup_tts(self) -> pyttsx3.Engine:
        """Setup text-to-speech engine with realistic British male voice"""
        engine = pyttsx3.init()

        # Get available voices
        voices = engine.getProperty('voices')

        # Priority list for realistic British male voices
        preferred_male_voices = [
            'daniel',     # British English (premium quality)
            'rishi',      # Indian English (good alternative)
            'thomas',     # French accent (backup)
            'xander',     # Dutch English (good quality)
            'fred',       # System voice (fallback)
        ]

        selected_voice = None
        
        # First try to find preferred British male voices
        for preferred in preferred_male_voices:
            for voice in voices:
                if (voice.name and preferred in voice.name.lower()):
                    # Verify it's actually male or neutral (some voices have incorrect gender tags)
                    gender_str = str(getattr(voice, 'gender', 'unknown')).lower()
                    if 'male' in gender_str or 'neuter' in gender_str:
                        selected_voice = voice
                        print(f"Selected preferred British male voice: {voice.name}")
                        break
            if selected_voice:
                break
        
        # If no preferred voice found, find any high-quality male voice
        if not selected_voice:
            male_names = ['daniel', 'thomas', 'fred', 'rishi', 'xander', 'majed', 'albert', 'alex', 'bruce', 'junior', 'ralph']
            for voice in voices:
                if (voice.name and any(male_name in voice.name.lower() for male_name in male_names)):
                    selected_voice = voice
                    print(f"Selected male voice: {voice.name}")
                    break
        
        # Fallback to any voice with male gender
        if not selected_voice:
            for voice in voices:
                gender_str = str(getattr(voice, 'gender', 'unknown')).lower()
                if 'male' in gender_str:
                    selected_voice = voice
                    print(f"Fallback male voice: {voice.name}")
                    break

        # Final fallback to default
        if not selected_voice and voices:
            selected_voice = voices[0]
            print(f"Using default voice: {selected_voice.name}")

        if selected_voice:
            engine.setProperty('voice', selected_voice.id)
            print(f"Voice configured: {selected_voice.name} (ID: {selected_voice.id})")

        # Set voice properties for more natural British speech
        engine.setProperty('rate', config.VOICE_RATE)
        engine.setProperty('volume', config.VOICE_VOLUME)
        
        # Verify settings
        rate = engine.getProperty('rate')
        volume = engine.getProperty('volume')
        print(f"TTS Settings: Rate={rate}, Volume={volume}")

        return engine

    def _calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        print("Calibrating microphone for ambient noise...")
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Microphone calibrated successfully.")
        except Exception as e:
            print(f"Microphone calibration failed: {e}")

    def speak(self, text: str, interrupt_current: bool = True):
        """Convert text to speech with realistic British male voice"""
        if not text or not text.strip():
            return
            
        # Add British mannerisms and formal speech patterns
        formatted_text = self._add_british_mannerisms(text)
        print(f"Jarvis: {formatted_text}")

        try:
            # Always create a fresh engine instance for reliability
            import pyttsx3
            
            # Create new engine instance to avoid threading issues
            speech_engine = pyttsx3.init()
            
            # Get available voices and set the same British male voice as main engine
            voices = speech_engine.getProperty('voices')
            
            # Use the same voice selection logic as _setup_tts for British male voices
            preferred_male_voices = ['daniel', 'rishi', 'thomas', 'xander', 'fred']
            selected_voice = None
            
            # Find preferred British male voice
            for preferred in preferred_male_voices:
                for voice in voices:
                    if (voice.name and preferred in voice.name.lower()):
                        gender_str = str(getattr(voice, 'gender', 'unknown')).lower()
                        if 'male' in gender_str or 'neuter' in gender_str:
                            selected_voice = voice
                            break
                if selected_voice:
                    break
            
            # Fallback to any male voice
            if not selected_voice:
                male_names = ['daniel', 'thomas', 'fred', 'rishi', 'xander', 'majed', 'albert', 'alex', 'bruce', 'junior', 'ralph']
                for voice in voices:
                    if (voice.name and any(male_name in voice.name.lower() for male_name in male_names)):
                        selected_voice = voice
                        break
            
            # Set the voice
            if selected_voice:
                speech_engine.setProperty('voice', selected_voice.id)
            
            # Copy settings from main engine
            speech_engine.setProperty('rate', config.VOICE_RATE)
            speech_engine.setProperty('volume', config.VOICE_VOLUME)
            
            # Speak the text
            speech_engine.say(formatted_text)
            speech_engine.runAndWait()
            
            # Clean up
            speech_engine.stop()
            del speech_engine
            
        except Exception as e:
            print(f"Speech synthesis error: {e}")
            # Fallback: try with basic engine
            try:
                import pyttsx3
                fallback_engine = pyttsx3.init()
                
                # Set basic male voice (Daniel preferred)
                voices = fallback_engine.getProperty('voices')
                for voice in voices:
                    if 'daniel' in voice.name.lower():
                        fallback_engine.setProperty('voice', voice.id)
                        break
                else:
                    # Fallback to any male voice
                    male_names = ['thomas', 'fred', 'rishi', 'xander', 'majed', 'albert']
                    for voice in voices:
                        if any(male_name in voice.name.lower() for male_name in male_names):
                            fallback_engine.setProperty('voice', voice.id)
                            break
                
                fallback_engine.setProperty('rate', 180)
                fallback_engine.setProperty('volume', 0.9)
                fallback_engine.say(formatted_text)
                fallback_engine.runAndWait()
                fallback_engine.stop()
                del fallback_engine
                
            except Exception as fallback_error:
                print(f"Fallback TTS also failed: {fallback_error}")
                print(f"Text that failed to speak: {formatted_text}")

    def _add_british_mannerisms(self, text: str) -> str:
        """Add British speech patterns and natural mannerisms"""
        # Replace common American terms with British equivalents
        replacements = {
            "okay": "very well",
            "sure": "certainly",
            "yeah": "indeed",
            "got it": "understood",
            "no problem": "not at all",
            "you're welcome": "my pleasure",
            "awesome": "excellent",
            "cool": "splendid",
            "great": "brilliant",
            "nice": "lovely",
            "thanks": "thank you",
        }

        formatted_text = text
        
        # Apply replacements (case-insensitive)
        for american, british in replacements.items():
            # Replace whole words only
            import re
            pattern = r'\b' + re.escape(american) + r'\b'
            formatted_text = re.sub(pattern, british, formatted_text, flags=re.IGNORECASE)

        # Add natural pauses for more realistic speech (subtle)
        formatted_text = formatted_text.replace('. ', '. ')  # Keep natural sentence breaks
        formatted_text = formatted_text.replace('!', '!')  # Keep excitement
        formatted_text = formatted_text.replace('?', '?')  # Keep questions natural
        
        # Add polite address occasionally (not always to avoid repetition)
        import random
        should_add_title = random.choice([True, False, False])  # 1/3 chance
        
        if (should_add_title and 
            not any(title in formatted_text.lower() for title in ['mr.', 'sir', 'master']) and
            formatted_text.strip() and 
            not formatted_text.lower().startswith(('good', 'hello', 'greetings', 'i am', 'welcome'))):
            
            # Choose from various polite addresses
            addresses = ["Mr. Bharadwaj Sir", "Sir", "Mr. Bharadwaj"]
            chosen_address = random.choice(addresses)
            formatted_text = f"{chosen_address}, {formatted_text.lower()}"

        # Clean up any double spaces or awkward formatting
        formatted_text = re.sub(r'\s+', ' ', formatted_text).strip()
        
        return formatted_text

    def listen_once(self, timeout: int = 5) -> Optional[str]:
        """Listen for a single command with timeout"""
        try:
            with self.microphone as source:
                print("Listening...")
                # Listen for audio with timeout
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)

            print("Processing speech...")
            # Recognize speech using Google's service
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower().strip()

        except sr.WaitTimeoutError:
            print("Listening timeout - no speech detected")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from speech recognition service: {e}")
            return None
        except Exception as e:
            print(f"Error during speech recognition: {e}")
            return None

    def start_continuous_listening(self, callback_function):
        """Start continuous listening in a separate thread"""
        if self.is_listening:
            return

        self.is_listening = True
        self.listening_thread = threading.Thread(
            target=self._continuous_listen_worker, 
            args=(callback_function,),
            daemon=True
        )
        self.listening_thread.start()
        print("Started continuous listening...")

    def stop_continuous_listening(self):
        """Stop continuous listening"""
        self.is_listening = False
        if hasattr(self, 'listening_thread'):
            self.listening_thread.join(timeout=2)
        print("Stopped continuous listening.")

    def _continuous_listen_worker(self, callback_function):
        """Worker function for continuous listening"""
        while self.is_listening:
            try:
                with self.microphone as source:
                    # Listen for wake word or commands
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)

                try:
                    text = self.recognizer.recognize_google(audio)
                    if text:
                        # Check for wake words
                        wake_words = ['jarvis', 'hey jarvis', 'ok jarvis', 'hello jarvis']
                        text_lower = text.lower().strip()

                        for wake_word in wake_words:
                            if wake_word in text_lower:
                                # Remove wake word and process command
                                command = text_lower.replace(wake_word, '').strip()
                                if command:  # If there's a command after wake word
                                    callback_function(command)
                                else:  # Just wake word, ask for command
                                    self.speak("Yes, Mr. Bharadwaj Sir? How may I assist you?")
                                    # Listen for the actual command
                                    command_text = self.listen_once(timeout=10)
                                    if command_text:
                                        callback_function(command_text)
                                break
                        else:
                            # No wake word found, but check if it's a direct command when already active
                            if hasattr(self, '_active_session') and self._active_session:
                                callback_function(text_lower)

                except sr.UnknownValueError:
                    pass  # Ignore unrecognized speech
                except sr.RequestError:
                    time.sleep(1)  # Brief pause on request errors

            except sr.WaitTimeoutError:
                pass  # Normal timeout, continue listening
            except Exception as e:
                print(f"Continuous listening error: {e}")
                time.sleep(1)

    def set_active_session(self, active: bool):
        """Set whether we're in an active conversation session"""
        self._active_session = active

    def test_voice(self):
        """Test the voice system"""
        test_phrases = [
            f"Good day, {config.USER_NAME}. Voice system is operational.",
            "I am Jarvis, your personal assistant. How may I be of service?",
            "All systems are functioning optimally, Mr. Bharadwaj Sir."
        ]

        for phrase in test_phrases:
            self.speak(phrase)
            time.sleep(1)

    def emergency_stop(self):
        """Emergency stop for all voice operations"""
        self.stop_continuous_listening()
        self.tts_engine.stop()
