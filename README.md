# J.A.R.V.I.S. - Personal AI Assistant

**Just A Rather Very Intelligent System**

A sophisticated personal assistant inspired by Jarvis from the Marvel movies, designed specifically for Mr. Bharadwaj. This AI assistant features voice recognition, British accent text-to-speech, intelligent file management, weather integration, and adaptive learning capabilities.

## 🌟 Features

### 🎤 Voice Interface
- **Speech Recognition**: Natural voice command processing
- **British Accent TTS**: Sophisticated text-to-speech with British mannerisms
- **Wake Word Detection**: Responds to "Jarvis", "Hey Jarvis", "OK Jarvis"
- **Continuous Listening**: Always ready to assist

### 🧠 Advanced AI Intelligence (Powered by Google Gemini)
- **Advanced NLP**: Google Gemini AI for sophisticated natural language understanding
- **Intent Recognition**: Accurately identifies what you want to do from natural speech
- **Entity Extraction**: Intelligently extracts filenames, locations, topics from commands
- **Conversational AI**: Engages in natural, contextual conversations beyond simple commands
- **Learning System**: Adapts to your preferences and patterns over time
- **Memory Management**: Remembers personal information and preferences
- **Contextual Responses**: Provides personalized, time-aware responses

### 📁 File Management
- **Intelligent File Search**: Find files by name or pattern across multiple directories
- **Quick File Access**: Open files with voice commands
- **Recent Files Tracking**: Remember frequently accessed files
- **Content Search**: Search within file contents

### 🌤️ Weather Integration
- **Real-time Weather**: Current conditions for any location
- **Weather Forecasts**: Multi-day weather predictions
- **Contextual Advice**: Weather-based recommendations
- **Location Awareness**: Default location with override capability

### 💻 System Monitoring
- **System Status**: CPU, memory, disk usage monitoring
- **Battery Information**: Power status and battery levels (laptops)
- **Uptime Tracking**: System performance metrics
- **Cross-platform Support**: Works on macOS, Windows, and Linux

### 📚 Knowledge Access
- **Wikipedia Integration**: Instant access to world knowledge
- **Information Lookup**: Answer questions on any topic
- **Smart Disambiguation**: Handle multiple search results intelligently

### 🎭 Jarvis Personality
- **British Butler Mannerisms**: Formal, polite, and sophisticated responses
- **Time-aware Greetings**: Appropriate greetings based on time of day
- **Personalized Interaction**: Addresses you as "Mr. Bharadwaj" and "Mr. Bharadwaj Sir"
- **Professional Demeanor**: Maintains the Jarvis character consistently

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Microphone for voice input
- Speakers or headphones for audio output
- Internet connection for weather and Wikipedia features

### Installation

1. **Clone or download the project**:
   ```bash
   cd /Users/rishabhbharadwajr/Desktop/Misc/proj
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API keys** (optional but recommended):
   - Create a `.env` file in the project directory
   - Add your API keys:
     ```
     GEMINI_API_KEY=your_google_gemini_api_key
     WEATHER_API_KEY=your_openweathermap_api_key
     USER_LOCATION=your_city_name
     USER_NAME=Mr. Bharadwaj
     ```

4. **Run Jarvis**:
   ```bash
   python jarvis.py
   ```

### Getting API Keys

#### Google Gemini AI (For Advanced NLP)
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Add it to your `.env` file as `GEMINI_API_KEY`

**Free tier includes:**
- 15 requests per minute
- 1 million tokens per minute
- Advanced natural language understanding

#### Weather API (OpenWeatherMap)
1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Generate an API key
4. Add it to your `.env` file as `WEATHER_API_KEY`

**Free tier includes:**
- Current weather data
- 5-day weather forecast
- 1,000 API calls per day

## 📖 Usage Guide

### Voice Commands

Jarvis responds to natural language. Here are some examples:

#### File Management
- "Jarvis, find my report.txt file"
- "Open the presentation document"
- "Search for Python files"
- "Where is my resume?"

#### Weather Information
- "What's the weather like?"
- "Weather forecast for tomorrow"
- "How's the weather in London?"
- "Is it going to rain today?"

#### System Information
- "What's my CPU usage?"
- "How much memory am I using?"
- "Check my battery level"
- "System status report"

#### Information Lookup
- "What is quantum computing?"
- "Who is Albert Einstein?"
- "Tell me about machine learning"
- "Information about Mars"

#### Personal Assistant
- "Remember that I prefer tea over coffee"
- "Note my meeting at 3 PM tomorrow"
- "What do you know about me?"
- "Help me with available commands"

#### Time and Date
- "What time is it?"
- "What's today's date?"
- "Current time and date"

### Text Mode

If you prefer text interaction or have microphone issues:

```bash
python jarvis.py --text-only
```

You can switch between voice and text modes during operation:
- Say "text mode" to disable voice
- Type "voice mode" to enable voice

## 🛠️ Advanced Configuration

### Customizing Search Directories

Edit `config.py` to modify file search locations:

```python
SEARCH_DIRECTORIES = [
    os.path.expanduser('~/Desktop'),
    os.path.expanduser('~/Documents'),
    os.path.expanduser('~/Downloads'),
    '/your/custom/directory'
]
```

### Voice Settings

Adjust voice parameters in `config.py`:

```python
VOICE_RATE = 180        # Speaking rate (words per minute)
VOICE_VOLUME = 0.9      # Volume level (0.0 to 1.0)
```

### Memory Settings

Configure learning and memory:

```python
CONVERSATION_HISTORY_LIMIT = 100  # Number of conversations to remember
```

## 🔧 Troubleshooting

### Common Issues

#### "No module named 'pyaudio'"
**Solution**: Install PyAudio dependencies
- **macOS**: `brew install portaudio` then `pip install pyaudio`
- **Windows**: `pip install pipwin && pipwin install pyaudio`
- **Linux**: `sudo apt-get install python3-pyaudio`

#### Voice recognition not working
1. Check microphone permissions
2. Test microphone with other applications
3. Try running: `python jarvis.py --diagnostics`

#### British voice not available
- The system will automatically select the best available voice
- On macOS: Install additional voices in System Preferences > Accessibility > Spoken Content
- On Windows: Install additional voices in Settings > Time & Language > Speech

#### Weather not working
1. Ensure you have a valid OpenWeatherMap API key
2. Check your internet connection
3. Verify the API key in your `.env` file

### System Diagnostics

Run system diagnostics to check all components:

```bash
python jarvis.py --diagnostics
```

## 🎯 Command Reference

### Wake Words
- "Jarvis"
- "Hey Jarvis"
- "OK Jarvis"
- "Hello Jarvis"

### System Commands
- "help" - Show available commands
- "status" - System status check
- "goodbye" / "exit" / "quit" - End session
- "text mode" / "voice mode" - Switch input modes

### File Operations
- "find [filename]" - Search for files
- "open [filename]" - Open file
- "search [text] in files" - Search file contents
- "recent files" - Show recently accessed files

### Information Commands
- "weather" / "weather in [location]" - Current weather
- "forecast" - Weather forecast
- "what is [topic]" - Wikipedia lookup
- "system info" - System performance
- "time" / "date" - Current time/date

## 🔒 Privacy & Security

- **Local Processing**: Most operations happen locally on your machine
- **API Usage**: Only weather and Wikipedia features require internet
- **Data Storage**: Personal notes stored locally in `jarvis_memory.json`
- **No Cloud Sync**: All data remains on your device

## 🤝 Contributing

This is a personal assistant designed specifically for Mr. Bharadwaj. However, the codebase is modular and can be adapted for other users by modifying the configuration files.

## 📄 License

This project is created as a personal assistant system. Please respect the intended use and any applicable terms for the integrated APIs (OpenWeatherMap, Wikipedia).

## 🆘 Support

For issues or questions:
1. Run diagnostics: `python jarvis.py --diagnostics`
2. Check the troubleshooting section above
3. Verify all dependencies are installed correctly

---

**"At your service, Mr. Bharadwaj."** - J.A.R.V.I.S.
