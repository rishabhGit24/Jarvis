"""
Background Task Manager for Jarvis
Handles long-running tasks while keeping the user engaged with real-time feedback
"""
import threading
import time
import queue
from typing import Callable, Any, Dict, Optional
from datetime import datetime
from rich.console import Console
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text
import config

console = Console()

class BackgroundTaskManager:
    """Manages background tasks with user engagement"""
    
    def __init__(self, voice_system=None, nlp_system=None):
        self.voice_system = voice_system
        self.nlp_system = nlp_system
        self.active_tasks = {}
        self.task_counter = 0
        self.feedback_messages = queue.Queue()
        self.is_running = True
        
        # Start feedback thread
        self.feedback_thread = threading.Thread(target=self._feedback_loop, daemon=True)
        self.feedback_thread.start()
    
    def execute_with_engagement(self, task_func: Callable, task_name: str, 
                              engagement_messages: list, user_input: str = "", *args, **kwargs) -> Any:
        """
        Execute a task in the background while keeping user engaged
        
        Args:
            task_func: Function to execute
            task_name: Name of the task for tracking
            engagement_messages: List of messages to show during processing
            user_input: Original user input for context
            *args, **kwargs: Arguments for the task function
        
        Returns:
            Result of the task function
        """
        task_id = self._get_next_task_id()
        
        # Create task info
        task_info = {
            'id': task_id,
            'name': task_name,
            'start_time': datetime.now(),
            'messages': engagement_messages,
            'user_input': user_input,
            'result': None,
            'error': None,
            'completed': False
        }
        
        self.active_tasks[task_id] = task_info
        
        # Start engagement
        self._start_engagement(task_id)
        
        # Execute task in background
        def task_wrapper():
            try:
                result = task_func(*args, **kwargs)
                task_info['result'] = result
                task_info['completed'] = True
            except Exception as e:
                task_info['error'] = str(e)
                task_info['completed'] = True
        
        task_thread = threading.Thread(target=task_wrapper, daemon=True)
        task_thread.start()
        
        # Wait for completion while showing engagement
        while not task_info['completed']:
            time.sleep(0.1)
        
        # Stop engagement
        self._stop_engagement(task_id)
        
        # Clean up
        del self.active_tasks[task_id]
        
        # Return result or raise error
        if task_info['error']:
            raise Exception(task_info['error'])
        
        return task_info['result']
    
    def _get_next_task_id(self) -> int:
        """Get next task ID"""
        self.task_counter += 1
        return self.task_counter
    
    def _start_engagement(self, task_id: int):
        """Start user engagement for a task"""
        task_info = self.active_tasks[task_id]
        
        # Generate and show initial message
        if task_info['messages']:
            # Try to generate AI-powered engaging message
            if self.nlp_system and hasattr(self.nlp_system, 'generate_engaging_message'):
                try:
                    user_input = task_info.get('user_input', '')
                    initial_message = self.nlp_system.generate_engaging_message(task_info['name'], user_input)
                except Exception:
                    initial_message = task_info['messages'][0]
            else:
                initial_message = task_info['messages'][0]
            
            console.print(f"[cyan]{initial_message}[/cyan]")
            
            # Speak the message if voice is available
            if self.voice_system:
                try:
                    self.voice_system.speak(initial_message)
                except Exception as e:
                    console.print(f"[dim yellow]Voice feedback unavailable: {e}[/dim yellow]")
        
        # Start periodic engagement messages
        self.feedback_messages.put(('start_engagement', task_id))
    
    def _stop_engagement(self, task_id: int):
        """Stop user engagement for a task"""
        self.feedback_messages.put(('stop_engagement', task_id))
    
    def _feedback_loop(self):
        """Background loop for providing user feedback"""
        engagement_timers = {}
        
        while self.is_running:
            try:
                # Check for feedback messages
                try:
                    message_type, task_id = self.feedback_messages.get(timeout=0.5)
                    
                    if message_type == 'start_engagement':
                        engagement_timers[task_id] = time.time()
                    elif message_type == 'stop_engagement':
                        if task_id in engagement_timers:
                            del engagement_timers[task_id]
                
                except queue.Empty:
                    pass
                
                # Provide periodic feedback for active tasks
                current_time = time.time()
                for task_id, start_time in list(engagement_timers.items()):
                    if task_id in self.active_tasks:
                        task_info = self.active_tasks[task_id]
                        elapsed = current_time - start_time
                        
                        # Show progress messages every 3 seconds
                        if elapsed > 3 and len(task_info['messages']) > 1:
                            message_index = min(int(elapsed / 3), len(task_info['messages']) - 1)
                            if message_index > 0:  # Skip the initial message
                                message = task_info['messages'][message_index]
                                console.print(f"[dim cyan]{message}[/dim cyan]")
                                
                                # Update start time to avoid repeated messages
                                engagement_timers[task_id] = current_time
                
                time.sleep(0.5)
                
            except Exception as e:
                console.print(f"[dim red]Feedback loop error: {e}[/dim red]")
    
    def shutdown(self):
        """Shutdown the background task manager"""
        self.is_running = False
        if self.feedback_thread.is_alive():
            self.feedback_thread.join(timeout=1.0)

class SmartTaskRouter:
    """Routes tasks to appropriate execution method based on complexity"""
    
    def __init__(self, task_manager: BackgroundTaskManager):
        self.task_manager = task_manager
        
        # Define task types that benefit from background processing
        self.background_task_types = {
            'file_search': [
                "Scanning through your files, Mr. Bharadwaj Sir...",
                "Searching directories and subdirectories...",
                "Checking file metadata and contents...",
                "Almost finished with the search, Mr. Bharadwaj Sir..."
            ],
            'weather_fetch': [
                "Contacting weather services, Mr. Bharadwaj Sir...",
                "Retrieving current conditions...",
                "Processing meteorological data...",
                "Finalizing weather report for you, Mr. Bharadwaj Sir..."
            ],
            'ai_processing': [
                "Analyzing your request with advanced AI, Mr. Bharadwaj Sir...",
                "Processing through neural networks...",
                "Generating intelligent response...",
                "Finalizing the analysis for you, Mr. Bharadwaj Sir..."
            ],
            'system_analysis': [
                "Gathering system information, Mr. Bharadwaj Sir...",
                "Analyzing performance metrics...",
                "Compiling diagnostic data...",
                "Preparing system report for you, Mr. Bharadwaj Sir..."
            ],
            'wikipedia_search': [
                "Accessing the knowledge base, Mr. Bharadwaj Sir...",
                "Searching comprehensive databases...",
                "Retrieving relevant information...",
                "Compiling the information for you, Mr. Bharadwaj Sir..."
            ]
        }
    
    def execute_task(self, task_type: str, task_func: Callable, user_input: str = "", *args, **kwargs) -> Any:
        """
        Execute task with appropriate method based on type
        
        Args:
            task_type: Type of task (determines engagement strategy)
            task_func: Function to execute
            user_input: Original user input for context
            *args, **kwargs: Arguments for the task function
        
        Returns:
            Result of the task function
        """
        if task_type in self.background_task_types:
            # Use background processing with engagement
            messages = self.background_task_types[task_type]
            return self.task_manager.execute_with_engagement(
                task_func, task_type, messages, user_input, *args, **kwargs
            )
        else:
            # Execute directly for simple tasks
            return task_func(*args, **kwargs)
    
    def add_custom_task_type(self, task_type: str, messages: list):
        """Add a custom task type with engagement messages"""
        self.background_task_types[task_type] = messages

# Global instances (will be initialized by main system)
background_task_manager = None
smart_task_router = None

def initialize_background_system(voice_system=None, nlp_system=None):
    """Initialize the background task system"""
    global background_task_manager, smart_task_router
    
    background_task_manager = BackgroundTaskManager(voice_system, nlp_system)
    smart_task_router = SmartTaskRouter(background_task_manager)
    
    console.print("[dim green]⚡ Background task system initialized[/dim green]")
    return background_task_manager, smart_task_router

def shutdown_background_system():
    """Shutdown the background task system"""
    global background_task_manager
    
    if background_task_manager:
        background_task_manager.shutdown()
        console.print("[dim yellow]Background task system shutdown[/dim yellow]")
