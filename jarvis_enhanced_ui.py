"""
Enhanced UI System for Jarvis
Provides a clean, attractive interface with clear conversation flow
"""
import time
from datetime import datetime
from typing import Optional, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.columns import Columns
from rich.align import Align
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.status import Status
from rich.layout import Layout
from rich import box
import config
import threading
import time

class JarvisEnhancedUI:
    """Enhanced UI system for Jarvis with clean conversation flow"""
    
    def __init__(self):
        self.console = Console()
        self.conversation_history = []
        self.current_status = "Ready"
        self.current_layer = None
        self.processing_active = False
        self.processing_thread = None
        self.live_display = None
        
    def clear_screen(self):
        """Clear the screen"""
        self.console.clear()
    
    def display_startup_interface(self):
        """Display enhanced startup interface"""
        self.clear_screen()
        
        # Create main title
        title = Text("J.A.R.V.I.S.", style="bold blue")
        subtitle = Text("Just A Rather Very Intelligent System", style="italic cyan")
        
        # System status table
        status_table = Table(show_header=False, box=box.ROUNDED, padding=(0, 1))
        status_table.add_column("Component", style="cyan", width=20)
        status_table.add_column("Status", style="green", width=30)
        
        status_table.add_row("🤖 AI Brain", "✅ Operational")
        status_table.add_row("🎤 Voice System", "✅ Ready")
        status_table.add_row("🧠 Memory", "✅ Active")
        status_table.add_row("⚡ Performance", "✅ Optimized")
        status_table.add_row("👤 User", f"✅ {config.USER_NAME}")
        
        # Create main panel
        main_panel = Panel(
            Align.center(f"{title}\n{subtitle}\n\n{status_table}"),
            title="[bold blue]JARVIS PERSONAL ASSISTANT[/bold blue]",
            subtitle="[italic]Ready to serve, Mr. Bharadwaj Sir[/italic]",
            border_style="blue",
            padding=(1, 2),
            box=box.DOUBLE
        )
        
        self.console.print(main_panel)
        self.console.print()
        
        # Quick help
        help_text = "[dim]💡 Commands: 'help' for assistance, 'quit' to exit, 'text mode' to disable voice[/dim]"
        self.console.print(Align.center(help_text))
        self.console.print()
    
    def display_user_query(self, query: str, input_type: str = "voice"):
        """Display user query in an attractive format"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Determine icon based on input type
        icon = "🎤" if input_type == "voice" else "⌨️"
        
        # Create user query panel
        query_panel = Panel(
            f"[bold white]{query}[/bold white]",
            title=f"[bold blue]{icon} USER QUERY[/bold blue]",
            subtitle=f"[dim]{timestamp}[/dim]",
            border_style="blue",
            box=box.ROUNDED,
            padding=(1, 2)
        )
        
        self.console.print(query_panel)
        self.console.print()
        
        # Store in history
        self.conversation_history.append({
            "type": "user",
            "content": query,
            "timestamp": timestamp,
            "input_type": input_type
        })
    
    def display_processing_status(self, status: str, layer: str = None, details: str = None):
        """Display processing status with layer information"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Layer mapping
        layer_info = {
            "layer1": "🧠 Layer 1: Local Model",
            "layer2": "⏳ Layer 2: Stalling Model", 
            "layer3": "🤖 Layer 3: Gemini AI",
            "router": "🔄 Smart Router"
        }
        
        layer_text = layer_info.get(layer, "⚙️ Processing") if layer else "⚙️ Processing"
        
        # Create processing panel
        processing_content = f"[bold yellow]{status}[/bold yellow]"
        if details:
            processing_content += f"\n[dim]{details}[/dim]"
        
        processing_panel = Panel(
            processing_content,
            title=f"[bold yellow]{layer_text}[/bold yellow]",
            subtitle=f"[dim]{timestamp}[/dim]",
            border_style="yellow",
            box=box.ROUNDED,
            padding=(1, 2)
        )
        
        self.console.print(processing_panel)
        self.console.print()
    
    def start_processing_loader(self, layer: str = None, query: str = None):
        """Start animated processing loader"""
        if self.processing_active:
            self.stop_processing_loader()
        
        self.processing_active = True
        self.current_layer = layer
        
        # Start processing animation in a separate thread
        self.processing_thread = threading.Thread(
            target=self._show_processing_animation,
            args=(layer, query),
            daemon=True
        )
        self.processing_thread.start()
    
    def _show_processing_animation(self, layer: str, query: str):
        """Show animated processing indicator"""
        # Layer-specific messages
        layer_messages = {
            "layer1": [
                "🧠 Local processing...",
                "⚡ Quick analysis...",
                "🔍 Pattern matching...",
                "✅ Generating response..."
            ],
            "layer2": [
                "⏳ Engaging stalling process...",
                "🤔 Considering your request...",
                "📊 Analyzing complexity...",
                "🔄 Preparing response..."
            ],
            "layer3": [
                "🤖 Gemini AI processing...",
                "🧠 Deep analysis...",
                "📚 Knowledge synthesis...",
                "✨ Crafting response..."
            ],
            "fallback": [
                "🔄 Fallback processing...",
                "🔧 System recovery...",
                "⚙️ Alternative routing...",
                "🎯 Finalizing response..."
            ]
        }
        
        messages = layer_messages.get(layer, [
            "⚙️ Processing...",
            "🔄 Analyzing...",
            "📊 Working...",
            "✨ Finalizing..."
        ])
        
        # Create progress bar
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=self.console,
            transient=True
        )
        
        task = progress.add_task("Processing your request...", total=100)
        
        try:
            with Live(progress, refresh_per_second=4, console=self.console) as live:
                message_index = 0
                progress_value = 0
                
                while self.processing_active and progress_value < 100:
                    # Update message
                    if message_index < len(messages):
                        progress.update(task, description=messages[message_index])
                        message_index += 1
                    else:
                        message_index = 0
                    
                    # Simulate progress
                    progress_value += 2
                    progress.update(task, completed=progress_value)
                    
                    time.sleep(0.5)
                    
                    # If we've been processing for a while, show more detailed status
                    if progress_value > 50:
                        progress.update(task, description=f"🔄 Still processing... ({progress_value}%)")
                    
                    if progress_value > 80:
                        progress.update(task, description="✨ Almost ready...")
                
                # Complete the progress
                if self.processing_active:
                    progress.update(task, completed=100, description="✅ Processing complete!")
                    time.sleep(0.5)
        
        except Exception as e:
            # Handle any display errors gracefully
            pass
    
    def stop_processing_loader(self):
        """Stop the processing loader"""
        self.processing_active = False
        if self.processing_thread and self.processing_thread.is_alive():
            self.processing_thread.join(timeout=1.0)
        self.current_layer = None
    
    def show_processing_status_update(self, message: str, layer: str = None):
        """Show a processing status update without stopping the loader"""
        if self.processing_active:
            timestamp = datetime.now().strftime("%H:%M:%S")
            layer_text = f"[{layer}] " if layer else ""
            self.console.print(f"[dim]{timestamp}[/dim] {layer_text}[yellow]{message}[/yellow]")
    
    def show_layer_transition(self, from_layer: str, to_layer: str, reason: str = None):
        """Show when transitioning between layers"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        transition_text = f"[dim]{timestamp}[/dim] [cyan]🔄 Transitioning from {from_layer} to {to_layer}"
        if reason:
            transition_text += f" ({reason})"
        transition_text += "[/cyan]"
        self.console.print(transition_text)
    
    def display_jarvis_response(self, response: str, status: str = "completed", action: str = None):
        """Display Jarvis response in an attractive format"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Status icons
        status_icons = {
            "completed": "✅",
            "processing": "⏳", 
            "error": "❌",
            "speaking": "🔊"
        }
        
        status_icon = status_icons.get(status, "✅")
        
        # Create response content
        response_content = f"[bold white]{response}[/bold white]"
        
        if action:
            response_content += f"\n\n[dim]🔊 {action}[/dim]"
        
        # Create response panel
        response_panel = Panel(
            response_content,
            title=f"[bold green]🤖 JARVIS RESPONSE[/bold green]",
            subtitle=f"[dim]{timestamp} {status_icon} {status.title()}[/dim]",
            border_style="green",
            box=box.ROUNDED,
            padding=(1, 2)
        )
        
        self.console.print(response_panel)
        self.console.print()
        
        # Store in history
        self.conversation_history.append({
            "type": "jarvis",
            "content": response,
            "timestamp": timestamp,
            "status": status,
            "action": action
        })
    
    def display_error(self, error: str):
        """Display error message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        error_panel = Panel(
            f"[bold red]{error}[/bold red]",
            title="[bold red]❌ ERROR[/bold red]",
            subtitle=f"[dim]{timestamp}[/dim]",
            border_style="red",
            box=box.ROUNDED,
            padding=(1, 2)
        )
        
        self.console.print(error_panel)
        self.console.print()
    
    def display_action_progress(self, action: str, progress: float = None):
        """Display action progress"""
        if progress is not None:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console,
                transient=True
            ) as progress:
                task = progress.add_task(action, total=100)
                progress.update(task, completed=int(progress * 100))
        else:
            with Status(action, console=self.console, spinner="dots") as status:
                time.sleep(0.5)  # Brief display
    
    def display_system_info(self, info: Dict[str, Any]):
        """Display system information"""
        info_table = Table(title="System Information", box=box.ROUNDED)
        info_table.add_column("Component", style="cyan")
        info_table.add_column("Status", style="green")
        info_table.add_column("Details", style="white")
        
        for component, data in info.items():
            status = data.get("status", "Unknown")
            details = data.get("details", "")
            info_table.add_row(component, status, details)
        
        self.console.print(info_table)
        self.console.print()
    
    def display_conversation_summary(self):
        """Display conversation summary"""
        if not self.conversation_history:
            return
        
        summary_table = Table(title="Conversation Summary", box=box.ROUNDED)
        summary_table.add_column("Time", style="dim")
        summary_table.add_column("Type", style="cyan")
        summary_table.add_column("Content", style="white")
        
        for entry in self.conversation_history[-10:]:  # Last 10 entries
            entry_type = "👤 User" if entry["type"] == "user" else "🤖 Jarvis"
            content = entry["content"][:50] + "..." if len(entry["content"]) > 50 else entry["content"]
            summary_table.add_row(entry["timestamp"], entry_type, content)
        
        self.console.print(summary_table)
        self.console.print()
    
    def display_help(self):
        """Display help information"""
        help_table = Table(title="Available Commands", box=box.ROUNDED)
        help_table.add_column("Command", style="cyan")
        help_table.add_column("Description", style="white")
        
        commands = [
            ("Time/Date", "What time is it? What day is it?"),
            ("System Info", "System status, CPU usage, memory"),
            ("File Operations", "Find files, open documents"),
            ("Weather", "Weather forecast, temperature"),
            ("Web Search", "Search Wikipedia, look up information"),
            ("Personal", "Who am I? Tell me about myself"),
            ("Applications", "Open Safari, Chrome, Calculator"),
            ("Help", "Show this help menu"),
            ("Quit", "Exit Jarvis")
        ]
        
        for command, description in commands:
            help_table.add_row(command, description)
        
        self.console.print(help_table)
        self.console.print()
    
    def display_mode_change(self, mode: str):
        """Display mode change notification"""
        mode_panel = Panel(
            f"[bold white]Switched to {mode} mode[/bold white]",
            title="[bold yellow]🔄 MODE CHANGE[/bold yellow]",
            border_style="yellow",
            box=box.ROUNDED,
            padding=(1, 2)
        )
        
        self.console.print(mode_panel)
        self.console.print()
    
    def display_shutdown(self):
        """Display shutdown message"""
        shutdown_panel = Panel(
            "[bold white]Thank you for using Jarvis, Mr. Bharadwaj Sir.\nGoodbye![/bold white]",
            title="[bold red]👋 SHUTDOWN[/bold red]",
            border_style="red",
            box=box.DOUBLE,
            padding=(1, 2)
        )
        
        self.console.print(shutdown_panel)
    
    def get_user_input(self, prompt: str = "You: ") -> str:
        """Get user input with enhanced prompt"""
        return self.console.input(f"[bold cyan]{prompt}[/bold cyan]")
    
    def print_separator(self):
        """Print a visual separator"""
        self.console.print("[dim]" + "─" * 80 + "[/dim]")
    
    def print_welcome_message(self):
        """Print welcome message"""
        welcome_text = """
[bold blue]Welcome to Jarvis, Mr. Bharadwaj Sir![/bold blue]

I'm your personal AI assistant, equipped with:
• 🧠 Advanced AI processing with personal context
• 🎤 Voice recognition and speech synthesis  
• ⚡ Multi-layer intelligent routing
• 📊 Real-time system monitoring
• 🎯 Personalized responses based on your profile

I'm ready to assist you with any task. Simply speak naturally or type your commands.
"""
        self.console.print(welcome_text)
        self.console.print()

# Initialize the enhanced UI
enhanced_ui = JarvisEnhancedUI()
