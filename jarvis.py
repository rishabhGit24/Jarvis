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
    from jarvis_speed import optimize_startup, get_performance_stats, perf_optimizer
    from jarvis_background_tasks import initialize_background_system, shutdown_background_system
    from jarvis_enhanced_ui import enhanced_ui
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
        self.background_task_manager = None
        self.smart_task_router = None

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        console.print("\\n[yellow]Shutting down Jarvis...[/yellow]")
        self.shutdown()
        sys.exit(0)

    def initialize(self) -> bool:
        """Initialize all Jarvis systems with speed optimization"""
        try:
            console.print(Panel.fit(
                "[bold blue]JARVIS PERSONAL ASSISTANT[/bold blue]\\n"
                "[italic]Initializing high-performance systems...[/italic]",
                border_style="blue"
            ))
            
            # Simple initialization for reliability
            console.print("[yellow]⚡ Activating systems...[/yellow]")
            
            # Initialize components sequentially for reliability
            console.print("[cyan]• Loading systems sequentially for stability...[/cyan]")
            
            # Initialize memory
            console.print("[dim]  - Initializing memory system...[/dim]")
            self.memory = JarvisMemory()
            
            # Initialize brain
            console.print("[dim]  - Initializing AI brain...[/dim]")
            self.brain = JarvisBrain()
            
            # Initialize voice
            console.print("[dim]  - Initializing voice system...[/dim]")
            self.voice = JarvisVoice()
            
            # Initialize background task system
            console.print("[dim]  - Initializing background task system...[/dim]")
            self.background_task_manager, self.smart_task_router = initialize_background_system(self.voice, self.brain.nlp)
            
            if not all([self.memory, self.brain, self.voice, self.background_task_manager]):
                console.print("[red]⚠ Some components failed to initialize[/red]")
                return False
            
            console.print(f"[green]✅ All systems ready with enhanced user experience[/green]")
            
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
        """Display the enhanced startup interface"""
        enhanced_ui.display_startup_interface()
        enhanced_ui.print_welcome_message()

    def _main_loop(self):
        """Main interaction loop"""
        while self.running and self.brain.should_continue_conversation():
            try:
                if not self.voice_mode:
                    # Text-only mode
                    user_input = enhanced_ui.get_user_input("You: ").strip()

                    if user_input.lower() in ['quit', 'exit', 'goodbye']:
                        break
                    elif user_input.lower() == 'voice mode':
                        self._enable_voice_mode()
                        continue
                    elif user_input.lower() == 'help':
                        enhanced_ui.display_help()
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
        """Process voice command with enhanced UI"""
        if not command or not command.strip():
            return

        # Display user query
        enhanced_ui.display_user_query(command, "voice")

        # Check for mode switching commands
        if 'text mode' in command.lower():
            self._disable_voice_mode()
            return

        # Process command through brain with enhanced UI feedback
        try:
            # Determine task type for smart routing
            task_type = self._determine_task_type(command)
            
            # Display processing status
            if task_type:
                enhanced_ui.display_processing_status(
                    f"Processing {task_type} request", 
                    "router", 
                    "Analyzing and routing to appropriate AI layer"
                )
            
            if self.smart_task_router and task_type:
                # Use background processing for complex tasks
                def brain_wrapper(cmd):
                    return self.brain.process_command(cmd)
                
                response = self.smart_task_router.execute_task(
                    task_type, 
                    brain_wrapper, 
                    command,
                    command
                )
            else:
                # Direct processing for simple commands
                response = self.brain.process_command(command)
            
            # Stop processing loader and display Jarvis response
            enhanced_ui.stop_processing_loader()
            enhanced_ui.display_jarvis_response(response, "completed", "Speaking response...")

            if self.voice_mode:
                self.voice.speak(response)

        except Exception as e:
            enhanced_ui.stop_processing_loader()
            error_response = f"I apologize, Mr. Bharadwaj Sir. I encountered an issue: {str(e)}"
            enhanced_ui.display_error(error_response)
            if self.voice_mode:
                self.voice.speak(error_response)

        # Check if conversation should end
        if not self.brain.should_continue_conversation():
            self.running = False

    def _process_text_command(self, command: str):
        """Process text command with enhanced UI"""
        # Display user query
        enhanced_ui.display_user_query(command, "text")

        # Process command through brain with enhanced UI feedback
        try:
            # Determine task type for smart routing
            task_type = self._determine_task_type(command)
            
            # Display processing status
            if task_type:
                enhanced_ui.display_processing_status(
                    f"Processing {task_type} request", 
                    "router", 
                    "Analyzing and routing to appropriate AI layer"
                )
            
            if self.smart_task_router and task_type:
                # Use background processing for complex tasks
                def brain_wrapper(cmd):
                    return self.brain.process_command(cmd)
                
                response = self.smart_task_router.execute_task(
                    task_type, 
                    brain_wrapper, 
                    command,
                    command
                )
            else:
                # Direct processing for simple commands
                response = self.brain.process_command(command)
            
            # Stop processing loader and display Jarvis response
            enhanced_ui.stop_processing_loader()
            enhanced_ui.display_jarvis_response(response, "completed", "Speaking response...")

            # Always speak the response if voice is available (even in text mode)
            if self.voice:
                self.voice.speak(response)

        except Exception as e:
            enhanced_ui.stop_processing_loader()
            error_response = f"I apologize, Mr. Bharadwaj Sir. I encountered an issue: {str(e)}"
            enhanced_ui.display_error(error_response)
            if self.voice:
                self.voice.speak(error_response)

        # Check if conversation should end
        if not self.brain.should_continue_conversation():
            self.running = False

    def _enable_voice_mode(self):
        """Enable voice recognition mode"""
        if not self.voice_mode:
            self.voice_mode = True
            enhanced_ui.display_mode_change("Voice")
            self.voice.speak("Voice mode enabled, Mr. Bharadwaj Sir.")
            self.voice.start_continuous_listening(self._process_voice_command)

    def _disable_voice_mode(self):
        """Disable voice recognition mode"""
        if self.voice_mode:
            self.voice_mode = False
            self.voice.stop_continuous_listening()
            enhanced_ui.display_mode_change("Text")
            self.voice.speak("Switching to text mode, Mr. Bharadwaj Sir.")
    
    def _determine_task_type(self, command: str) -> Optional[str]:
        """Determine the type of task for smart routing"""
        command_lower = command.lower()
        
        # Map command patterns to task types
        if any(word in command_lower for word in ['find', 'search', 'locate', 'file']):
            return 'file_search'
        elif any(word in command_lower for word in ['weather', 'temperature', 'forecast', 'climate']):
            return 'weather_fetch'
        elif any(word in command_lower for word in ['what is', 'who is', 'tell me about', 'explain', 'wikipedia']):
            return 'wikipedia_search'
        elif any(word in command_lower for word in ['system', 'cpu', 'memory', 'disk', 'battery', 'performance']):
            return 'system_analysis'
        elif len(command.split()) > 10:  # Long queries likely need AI processing
            return 'ai_processing'
        
        return None  # Simple commands don't need background processing

    def shutdown(self):
        """Shutdown Jarvis gracefully"""
        self.running = False
        if self.brain and hasattr(self.brain, 'conversation_active'):
            self.brain.conversation_active = False
        
        if self.voice and hasattr(self.voice, 'emergency_stop'):
            try:
                self.voice.emergency_stop()
            except Exception as e:
                enhanced_ui.display_error(f"Voice shutdown warning: {e}")
        
        # Shutdown background task system
        try:
            shutdown_background_system()
        except Exception as e:
            enhanced_ui.display_error(f"Background task system shutdown warning: {e}")
        
        # Shutdown performance optimizer
        try:
            perf_optimizer.shutdown()
        except Exception as e:
            enhanced_ui.display_error(f"Performance optimizer shutdown warning: {e}")
        
        # Display shutdown message
        enhanced_ui.display_shutdown()

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
        
        if config.GEMINI_API_KEY:
            diagnostics.add_row("Gemini AI", "✓ Configured", "Advanced NLP enabled")
        else:
            diagnostics.add_row("Gemini AI", "⚠ Not Configured", "Set GEMINI_API_KEY for AI features")
        
        # Performance stats
        stats = get_performance_stats()
        diagnostics.add_row("Performance Cache", "✓ Active", f"{stats['total_cached_items']} cached items")
        diagnostics.add_row("Cache Hit Rate", "✓ Optimized", f"{stats.get('cache_hit_rate', 0):.1f}%")
        
        # Smart AI Routing stats
        if self.brain and hasattr(self.brain, 'get_performance_stats'):
            brain_stats = self.brain.get_performance_stats()
            if 'nlp_stats' in brain_stats and 'routing_stats' in brain_stats['nlp_stats']:
                routing_stats = brain_stats['nlp_stats']['routing_stats']
                local_pct = routing_stats.get('local_percentage', 0)
                diagnostics.add_row("Smart AI Routing", "✓ Active", f"{local_pct:.1f}% local processing")
        
        # Memory usage
        if 'memory_usage_mb' in stats:
            memory_mb = stats['memory_usage_mb']
            diagnostics.add_row("Memory Usage", "✓ Monitored", f"{memory_mb:.1f} MB")
        
        # Async processing
        async_completed = stats.get('async_tasks_completed', 0)
        diagnostics.add_row("Async Processing", "✓ Active", f"{async_completed} tasks completed")
        
        console.print(diagnostics)
        
        # Additional performance details
        console.print("\\n[bold cyan]Performance Details:[/bold cyan]")
        perf_table = Table(show_header=True, header_style="bold blue")
        perf_table.add_column("Metric", style="cyan")
        perf_table.add_column("Value", style="green")
        
        perf_table.add_row("Startup Time", f"{stats.get('startup_time', 0):.3f}s")
        perf_table.add_row("Total Cache Items", str(stats.get('total_cached_items', 0)))
        perf_table.add_row("Memory Cleanups", str(stats.get('memory_cleanups', 0)))
        
        if 'cpu_percent' in stats:
            perf_table.add_row("CPU Usage", f"{stats['cpu_percent']:.1f}%")
        
        console.print(perf_table)

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
