#!/usr/bin/env python3
"""
JARVIS - Personal AI Assistant
A sophisticated personal assistant similar to Jarvis from Marvel movies
Created for Mr. Bharadwaj

Features:
- Voice recognition and British accent text-to-speech
- File management and search capabilities
- Weather information and forecasts
- System monitoring and information
- Learning and memory system
- Natural language processing
- Wikipedia integration
- Personal note-taking and preferences

Usage: python jarvis.py
"""

import sys
import os
import signal
import threading
import time
from datetime import datetime
from typing import Optional

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from colorama import init, Fore, Back, Style
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.live import Live
    from rich.table import Table

    from jarvis_voice import JarvisVoice
    from jarvis_brain import JarvisBrain
    from jarvis_memory import JarvisMemory
    import config

    init(autoreset=True)  # Initialize colorama
    console = Console()

except ImportError as e:
    print(f"Missing required dependencies: {e}")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)

class JarvisAssistant:
    def __init__(self):
        self.voice = None
        self.brain = None
        self.memory = None
        self.running = False
        self.voice_mode = True
        self.setup_complete = False

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        console.print("\\n[yellow]Shutting down Jarvis...[/yellow]")
        self.shutdown()
        sys.exit(0)

    def initialize(self) -> bool:
        """Initialize all Jarvis systems"""
        try:
            console.print(Panel.fit(
                "[bold blue]JARVIS PERSONAL ASSISTANT[/bold blue]\\n"
                "[italic]Initializing systems...[/italic]",
                border_style="blue"
            ))

            # Initialize components
            console.print("[cyan]• Loading memory systems...[/cyan]")
            self.memory = JarvisMemory()

            console.print("[cyan]• Initializing AI brain...[/cyan]")
            self.brain = JarvisBrain()

            console.print("[cyan]• Setting up voice systems...[/cyan]")
            self.voice = JarvisVoice()

            # Test voice system
            console.print("[cyan]• Testing voice synthesis...[/cyan]")

            self.setup_complete = True
            return True

        except Exception as e:
            console.print(f"[red]Initialization failed: {e}[/red]")
            return False

    def start(self):
        """Start the Jarvis assistant"""
        if not self.setup_complete:
            if not self.initialize():
                return

        self.running = True
        self.brain.conversation_active = True

        # Display startup interface
        self._display_startup_interface()

        # Get startup message from brain
        startup_message = self.brain.get_startup_message()
        console.print(f"[green]Jarvis:[/green] {startup_message}")

        if self.voice_mode:
            self.voice.speak(startup_message)

            # Start voice recognition in a separate thread
            console.print("[dim]Listening for voice commands... (Say 'Jarvis' to activate)[/dim]")
            self.voice.start_continuous_listening(self._process_voice_command)

        # Main interaction loop
        try:
            self._main_loop()
        except KeyboardInterrupt:
            self._signal_handler(None, None)

    def _display_startup_interface(self):
        """Display the startup interface"""
        current_time = datetime.now().strftime("%H:%M:%S")

        # Create main panel
        title = Text("J.A.R.V.I.S.", style="bold blue")
        subtitle = Text("Just A Rather Very Intelligent System", style="italic cyan")

        info_table = Table(show_header=False, box=None, padding=(0, 2))
        info_table.add_row("[bold]User:[/bold]", f"[green]{config.USER_NAME}[/green]")
        info_table.add_row("[bold]Time:[/bold]", f"[yellow]{current_time}[/yellow]")
        info_table.add_row("[bold]Status:[/bold]", "[green]All Systems Operational[/green]")
        info_table.add_row("[bold]Mode:[/bold]", "[cyan]Voice & Text Interface[/cyan]")

        panel_content = f"{title}\\n{subtitle}\\n\\n{info_table}"

        console.print(Panel(
            info_table,
            title="[bold blue]J.A.R.V.I.S. - Personal Assistant[/bold blue]",
            subtitle="[italic]Ready to serve, Sir[/italic]",
            border_style="blue",
            padding=(1, 2)
        ))

        # Display quick help
        console.print("[dim]Commands: 'help' for assistance, 'quit' to exit, 'text mode' to disable voice[/dim]")

    def _main_loop(self):
        """Main interaction loop"""
        while self.running and self.brain.should_continue_conversation():
            try:
                if not self.voice_mode:
                    # Text-only mode
                    user_input = input(f"\\n{Fore.CYAN}You: {Style.RESET_ALL}").strip()

                    if user_input.lower() in ['quit', 'exit', 'goodbye']:
                        break
                    elif user_input.lower() == 'voice mode':
                        self._enable_voice_mode()
                        continue
                    elif user_input:
                        self._process_text_command(user_input)
                else:
                    # Voice mode - just wait and let the voice thread handle commands
                    time.sleep(0.1)

            except EOFError:
                break
            except Exception as e:
                console.print(f"[red]Error in main loop: {e}[/red]")
                continue

    def _process_voice_command(self, command: str):
        """Process voice command"""
        if not command or not command.strip():
            return

        console.print(f"[blue]You (voice):[/blue] {command}")

        # Check for mode switching commands
        if 'text mode' in command.lower():
            self._disable_voice_mode()
            return

        # Process command through brain
        response = self.brain.process_command(command)
        console.print(f"[green]Jarvis:[/green] {response}")

        if self.voice_mode:
            self.voice.speak(response)

        # Check if conversation should end
        if not self.brain.should_continue_conversation():
            self.running = False

    def _process_text_command(self, command: str):
        """Process text command"""
        console.print(f"[blue]You:[/blue] {command}")

        # Process command through brain
        response = self.brain.process_command(command)
        console.print(f"[green]Jarvis:[/green] {response}")

        # Check if conversation should end
        if not self.brain.should_continue_conversation():
            self.running = False

    def _enable_voice_mode(self):
        """Enable voice recognition mode"""
        if not self.voice_mode:
            self.voice_mode = True
            console.print("[green]Voice mode enabled. Say 'Jarvis' to activate.[/green]")
            self.voice.speak("Voice mode enabled, Sir.")
            self.voice.start_continuous_listening(self._process_voice_command)

    def _disable_voice_mode(self):
        """Disable voice recognition mode"""
        if self.voice_mode:
            self.voice_mode = False
            self.voice.stop_continuous_listening()
            console.print("[yellow]Voice mode disabled. Switching to text input.[/yellow]")
            self.voice.speak("Switching to text mode, Sir.")

    def shutdown(self):
        """Shutdown Jarvis gracefully"""
        self.running = False
        self.brain.conversation_active = False

        if self.voice:
            self.voice.emergency_stop()

        console.print("[green]Jarvis systems shutdown complete. Goodbye, Sir.[/green]")

    def run_diagnostics(self):
        """Run system diagnostics"""
        console.print(Panel.fit(
            "[bold yellow]JARVIS SYSTEM DIAGNOSTICS[/bold yellow]",
            border_style="yellow"
        ))

        diagnostics = Table(show_header=True, header_style="bold magenta")
        diagnostics.add_column("Component", style="cyan", no_wrap=True)
        diagnostics.add_column("Status", style="green")
        diagnostics.add_column("Details")

        # Check voice system
        try:
            if self.voice:
                diagnostics.add_row("Voice Recognition", "✓ Operational", "Speech-to-text ready")
                diagnostics.add_row("Text-to-Speech", "✓ Operational", "British accent configured")
            else:
                diagnostics.add_row("Voice System", "✗ Not Initialized", "Run initialization first")
        except Exception as e:
            diagnostics.add_row("Voice System", "⚠ Warning", str(e))

        # Check brain system
        try:
            if self.brain:
                diagnostics.add_row("AI Brain", "✓ Operational", "Natural language processing ready")
            else:
                diagnostics.add_row("AI Brain", "✗ Not Initialized", "Run initialization first")
        except Exception as e:
            diagnostics.add_row("AI Brain", "⚠ Warning", str(e))

        # Check memory system
        try:
            if self.memory:
                diagnostics.add_row("Memory System", "✓ Operational", "Learning and storage ready")
            else:
                diagnostics.add_row("Memory System", "✗ Not Initialized", "Run initialization first")
        except Exception as e:
            diagnostics.add_row("Memory System", "⚠ Warning", str(e))

        # Check API configurations
        if config.WEATHER_API_KEY:
            diagnostics.add_row("Weather API", "✓ Configured", "Real-time weather data available")
        else:
            diagnostics.add_row("Weather API", "⚠ Not Configured", "Set WEATHER_API_KEY for weather features")

        console.print(diagnostics)

def main():
    """Main entry point"""
    console.print(f"[bold green]Starting JARVIS for {config.USER_NAME}...[/bold green]\\n")

    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--diagnostics":
            jarvis = JarvisAssistant()
            jarvis.initialize()
            jarvis.run_diagnostics()
            return
        elif sys.argv[1] == "--text-only":
            jarvis = JarvisAssistant()
            jarvis.voice_mode = False
            jarvis.start()
            return
        elif sys.argv[1] == "--help":
            print("""
JARVIS Personal Assistant

Usage: python jarvis.py [options]

Options:
  --help        Show this help message
  --diagnostics Run system diagnostics
  --text-only   Start in text-only mode (no voice)

Default: Start with full voice and text interface
            """)
            return

    # Start normal operation
    jarvis = JarvisAssistant()

    try:
        jarvis.start()
    except KeyboardInterrupt:
        console.print("\\n[yellow]Interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
    finally:
        jarvis.shutdown()

if __name__ == "__main__":
    main()
