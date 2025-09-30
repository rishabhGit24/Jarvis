"""
Voice Recognition and Text-to-Speech System for Jarvis
Handles speech input/output with British accent
"""
import speech_recognition as sr
import pyttsx3
import threading
import queue
import time
import re
import random
from typing import Optional
import config

class JarvisVoice:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = self._setup_tts()
        self.is_listening = False
        self.audio_queue = queue.Queue()
        
        # Check if advanced voice is enabled
        self.use_advanced_voice = getattr(config, 'USE_ADVANCED_VOICE', False)
        self.advanced_voice = None
        
        if self.use_advanced_voice:
            try:
                from jarvis_advanced_voice import get_advanced_voice
                self.advanced_voice = get_advanced_voice()
                
                # Set the configured engine and voice
                engine = getattr(config, 'ADVANCED_VOICE_ENGINE', 'gtts')
                voice_desc = getattr(config, 'ADVANCED_VOICE_DESCRIPTION', 'English (UK) - Female')
                self.advanced_voice.set_voice(engine, voice_desc)
                
                print(f"✅ Voice set to: {engine} - {voice_desc}")
            except Exception as e:
                print(f"⚠️  Advanced voice failed, using system voice: {e}")
                self.use_advanced_voice = False

        # Calibrate microphone for ambient noise
        self._calibrate_microphone()

    def _setup_tts(self) -> pyttsx3.Engine:
        """Setup text-to-speech engine with configurable accent"""
        engine = pyttsx3.init()

        # Get available voices
        voices = engine.getProperty('voices')

        # Voice preferences by accent (prioritizing natural female voices)
        accent_voices = {
            'british': ['serena', 'kate', 'emily', 'chloe', 'zoe', 'stephanie', 'daniel', 'oliver'],
            'american': ['victoria', 'allison', 'ava', 'samantha', 'susan', 'zoe', 'kathy', 'alex', 'fred', 'tom'],
            'australian': ['karen', 'catherine', 'lee', 'nicole', 'hayley'],
            'indian': ['veena', 'lekha', 'priya', 'kavya', 'rishi'],
            'irish': ['fiona', 'moira', 'siobhan', 'niamh'],
            'scottish': ['fiona', 'moira', 'isla', 'aileas'],
            'french': ['aurelie', 'amelie', 'celine', 'marie', 'thomas'],
            'german': ['anna', 'petra', 'marlene', 'yannick'],
            'spanish': ['monica', 'carmen', 'esperanza', 'jorge'],
            'italian': ['alice', 'federica', 'paola', 'luca'],
            'canadian': ['tessa', 'nora', 'felix'],
            'south_african': ['tandi']
        }

        # Get preferred voices for selected accent
        selected_accent = getattr(config, 'VOICE_ACCENT', 'british').lower()
        preferred_voices = accent_voices.get(selected_accent, accent_voices['american'])

        selected_voice = None
        
        # First try to find preferred voices for the selected accent
        for preferred in preferred_voices:
            for voice in voices:
                if (voice.name and preferred in voice.name.lower()):
                    # Verify it's actually male or neutral (some voices have incorrect gender tags)
                    gender_str = str(getattr(voice, 'gender', 'unknown')).lower()
                    if 'male' in gender_str or 'neuter' in gender_str:
                        selected_voice = voice
                        print(f"Selected {selected_accent} accent voice: {voice.name}")
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
        """Convert text to speech with ultra-realistic voice"""
        if not text or not text.strip():
            return
            
        # Add ultra-realistic conversational patterns
        formatted_text = self._add_realistic_conversational_patterns(text)
        print(f"Jarvis: {formatted_text}")
        
        # Use advanced voice if available
        if self.use_advanced_voice and self.advanced_voice:
            try:
                if not getattr(config, 'SKIP_VERBOSE_LOGGING', False):
                    print(f"🎭 Using advanced voice: {config.ADVANCED_VOICE_ENGINE}")
                self.advanced_voice.speak(formatted_text)
                return
            except Exception as e:
                print(f"⚠️  Advanced voice failed: {e}, falling back to system voice")
                # Continue to system voice below

        try:
            # Always create a fresh engine instance for reliability
            import pyttsx3
            
            # Create new engine instance to avoid threading issues
            speech_engine = pyttsx3.init()
            
            # Get available voices and set the same British male voice as main engine
            voices = speech_engine.getProperty('voices')
            
            # Use the same voice selection logic as _setup_tts for the configured accent
            accent_voices = {
                'british': ['serena', 'kate', 'emily', 'chloe', 'zoe', 'stephanie', 'daniel', 'oliver'],
                'american': ['victoria', 'allison', 'ava', 'samantha', 'susan', 'zoe', 'kathy', 'alex', 'fred', 'tom'],
                'australian': ['karen', 'catherine', 'lee', 'nicole', 'hayley'],
                'indian': ['veena', 'lekha', 'priya', 'kavya', 'rishi'],
                'irish': ['fiona', 'moira', 'siobhan', 'niamh'],
                'scottish': ['fiona', 'moira', 'isla', 'aileas'],
                'french': ['aurelie', 'amelie', 'celine', 'marie', 'thomas'],
                'german': ['anna', 'petra', 'marlene', 'yannick'],
                'spanish': ['monica', 'carmen', 'esperanza', 'jorge'],
                'italian': ['alice', 'federica', 'paola', 'luca'],
                'canadian': ['tessa', 'nora', 'felix'],
                'south_african': ['tandi']
            }
            
            selected_accent = getattr(config, 'VOICE_ACCENT', 'british').lower()
            preferred_voices = accent_voices.get(selected_accent, accent_voices['american'])
            selected_voice = None
            
            # Find preferred voice for the configured accent
            for preferred in preferred_voices:
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
                
                fallback_engine.setProperty('rate', 280)
                fallback_engine.setProperty('volume', 0.9)
                fallback_engine.say(formatted_text)
                fallback_engine.runAndWait()
                fallback_engine.stop()
                del fallback_engine
                
            except Exception as fallback_error:
                print(f"Fallback TTS also failed: {fallback_error}")
                print(f"Text that failed to speak: {formatted_text}")

    def _add_realistic_conversational_patterns(self, text: str) -> str:
        """Transform text to sound like natural human conversation with ultra-realistic speech patterns"""
        import random
        import re
        
        formatted_text = text
        
        # Natural contractions and human speech patterns
        contractions = {
            "I will": "I'll", "I am": "I'm", "I have": "I've", "I would": "I'd",
            "You are": "you're", "You have": "you've", "You will": "you'll",
            "It is": "it's", "It will": "it'll", "That is": "that's",
            "There is": "there's", "Here is": "here's", "What is": "what's",
            "cannot": "can't", "will not": "won't", "should not": "shouldn't",
            "could not": "couldn't", "would not": "wouldn't", "do not": "don't"
        }
        
        # Apply contractions
        for formal, casual in contractions.items():
            formatted_text = re.sub(r'\b' + re.escape(formal) + r'\b', casual, formatted_text, flags=re.IGNORECASE)
        
        # Add natural conversation starters (occasionally)
        if random.random() < 0.25:  # 25% chance
            if not any(formatted_text.lower().startswith(starter) for starter in ['well', 'so', 'oh', 'ah', 'right', 'okay']):
                starters = ["Well, ", "So, ", "Oh, ", "Ah, ", "Right, ", "Okay, "]
                formatted_text = random.choice(starters) + formatted_text.lower()
        
        # Add natural thinking patterns and fillers (sparingly)
        if random.random() < 0.15:  # 15% chance
            if "let me" in formatted_text.lower() or "I'll" in formatted_text:
                fillers = ["let's see... ", "hmm... ", "let me think... ", "well... "]
                formatted_text = random.choice(fillers) + formatted_text
        
        # Get accent-specific patterns
        accent = getattr(config, 'VOICE_ACCENT', 'british').lower()
        formatted_text = self._add_accent_specific_realism(formatted_text, accent)
        
        # Add natural emotional expressions
        formatted_text = self._add_emotional_realism(formatted_text)
        
        # Occasionally add polite address (not too often)
        if random.random() < 0.3:  # 30% chance
            formatted_text = self._add_natural_address(formatted_text)
        
        # Clean up formatting
        formatted_text = re.sub(r'\s+', ' ', formatted_text).strip()
        formatted_text = formatted_text[0].upper() + formatted_text[1:] if formatted_text else ""
        
        return formatted_text
    
    def _add_accent_specific_realism(self, text: str, accent: str) -> str:
        """Add accent-specific natural expressions"""
        import random
        
        if accent == 'british':
            replacements = {
                "okay": random.choice(["right", "alright", "very well"]),
                "sure": random.choice(["absolutely", "certainly", "of course"]),
                "great": random.choice(["brilliant", "lovely", "fantastic"]),
                "cool": random.choice(["brilliant", "ace", "smashing"]),
                "awesome": random.choice(["brilliant", "fantastic", "marvelous"]),
                "thanks": "cheers" if random.random() < 0.3 else "thank you"
            }
        elif accent == 'american':
            replacements = {
                "brilliant": random.choice(["awesome", "great", "fantastic"]),
                "lovely": random.choice(["nice", "great", "sweet"]),
                "quite": "pretty" if random.random() < 0.4 else "quite"
            }
        elif accent == 'australian':
            replacements = {
                "great": random.choice(["good on ya", "brilliant", "fantastic"]),
                "sure": random.choice(["no worries", "absolutely", "too right"])
            }
        else:
            replacements = {}
        
        for formal, casual in replacements.items():
            text = re.sub(r'\b' + re.escape(formal) + r'\b', casual, text, flags=re.IGNORECASE)
        
        return text
    
    def _add_emotional_realism(self, text: str) -> str:
        """Add subtle emotional expressions to make speech more human"""
        import random
        
        # Add enthusiasm markers
        if any(word in text.lower() for word in ['found', 'located', 'discovered', 'completed']):
            if random.random() < 0.4:  # 40% chance
                enthusiasm = random.choice(["Great! ", "Perfect! ", "Excellent! ", "Wonderful! "])
                text = enthusiasm + text
        
        # Add empathy for problems
        if any(word in text.lower() for word in ['sorry', 'apologize', 'error', 'problem', 'issue']):
            if random.random() < 0.3:  # 30% chance
                empathy = random.choice(["Oh dear, ", "I'm afraid ", "Unfortunately, "])
                text = empathy + text
        
        # Add curiosity for questions
        if text.endswith('?') and random.random() < 0.2:  # 20% chance
            curiosity = random.choice(["Hmm, ", "Let me see... ", "Interesting... "])
            text = curiosity + text
        
        return text
    
    def _add_natural_address(self, text: str) -> str:
        """Add natural, varied ways of addressing the user"""
        import random
        
        # Don't add if already has address
        if any(title in text.lower() for title in ['mr.', 'sir', 'bharadwaj']):
            return text
        
        # Don't add to certain types of responses
        if any(text.lower().startswith(start) for start in ['good', 'hello', 'hi', 'greetings', 'welcome']):
            return text
        
        # Various natural ways to address
        addresses = [
            "Mr. Bharadwaj",
            "sir", 
            "Mr. Bharadwaj sir",
        ]
        
        chosen_address = random.choice(addresses)
        
        # Add naturally to the sentence
        if random.random() < 0.6:  # 60% chance at beginning
            return f"{chosen_address}, {text.lower()}"
        else:  # 40% chance at end
            return f"{text}, {chosen_address}"

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
