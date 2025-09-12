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
        """Setup text-to-speech engine with British accent"""
        engine = pyttsx3.init()

        # Get available voices
        voices = engine.getProperty('voices')

        # Try to find British accent voice
        british_voice = None
        for voice in voices:
            if voice.name and ('british' in voice.name.lower() or 
                             'uk' in voice.name.lower() or 
                             'daniel' in voice.name.lower() or
                             'serena' in voice.name.lower()):
                british_voice = voice
                break

        # If no British voice found, use the second available voice (often better than default)
        if british_voice is None and len(voices) > 1:
            british_voice = voices[1]
        elif british_voice is None:
            british_voice = voices[0] if voices else None

        if british_voice:
            engine.setProperty('voice', british_voice.id)
            print(f"Using voice: {british_voice.name}")

        # Set voice properties
        engine.setProperty('rate', config.VOICE_RATE)
        engine.setProperty('volume', config.VOICE_VOLUME)

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
        """Convert text to speech with British accent"""
        if interrupt_current:
            self.tts_engine.stop()

        # Add British mannerisms and formal speech patterns
        formatted_text = self._add_british_mannerisms(text)

        print(f"Jarvis: {formatted_text}")

        try:
            self.tts_engine.say(formatted_text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"Speech synthesis error: {e}")

    def _add_british_mannerisms(self, text: str) -> str:
        """Add British speech patterns and mannerisms"""
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
        }

        formatted_text = text
        for american, british in replacements.items():
            formatted_text = formatted_text.replace(american, british)

        # Add formal address if not present
        if not any(title in formatted_text.lower() for title in ['mr.', 'sir', 'master']):
            if formatted_text.strip() and not formatted_text.lower().startswith(('good', 'hello', 'greetings')):
                formatted_text = f"Sir, {formatted_text.lower()}"

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
                                    self.speak("Yes, Sir? How may I assist you?")
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
            "All systems are functioning optimally, Sir."
        ]

        for phrase in test_phrases:
            self.speak(phrase)
            time.sleep(1)

    def emergency_stop(self):
        """Emergency stop for all voice operations"""
        self.stop_continuous_listening()
        self.tts_engine.stop()
