"""
Jarvis System Control Module
Provides comprehensive system access and application control
Like a true personal butler with complete system privileges
"""

import subprocess
import os
import platform
import time
from typing import Dict, List, Optional, Tuple, Any
import psutil
import webbrowser
from pathlib import Path

class JarvisSystemControl:
    def __init__(self):
        self.system = platform.system()
        self.applications = self._discover_applications()
        
    def _discover_applications(self) -> Dict[str, str]:
        """Discover installed applications and their paths"""
        apps = {}
        
        if self.system == "Darwin":  # macOS
            # Common application paths
            app_paths = [
                "/Applications",
                "/System/Applications",
                "~/Applications"
            ]
            
            for app_path in app_paths:
                expanded_path = os.path.expanduser(app_path)
                if os.path.exists(expanded_path):
                    for item in os.listdir(expanded_path):
                        if item.endswith('.app'):
                            app_name = item.replace('.app', '').lower()
                            apps[app_name] = os.path.join(expanded_path, item)
            
            # Add system commands and browsers
            apps.update({
                'safari': '/Applications/Safari.app',
                'chrome': '/Applications/Google Chrome.app',
                'firefox': '/Applications/Firefox.app',
                'finder': '/System/Library/CoreServices/Finder.app',
                'terminal': '/Applications/Utilities/Terminal.app',
                'calculator': '/Applications/Calculator.app',
                'calendar': '/Applications/Calendar.app',
                'mail': '/Applications/Mail.app',
                'notes': '/Applications/Notes.app',
                'music': '/Applications/Music.app',
                'photos': '/Applications/Photos.app',
                'facetime': '/Applications/FaceTime.app',
                'messages': '/Applications/Messages.app',
                'settings': '/Applications/System Preferences.app',
                'system preferences': '/Applications/System Preferences.app',
                'activity monitor': '/Applications/Utilities/Activity Monitor.app',
                'disk utility': '/Applications/Utilities/Disk Utility.app'
            })
            
        return apps
    
    def open_application(self, app_name: str) -> Tuple[bool, str]:
        """Open an application by name"""
        app_name_lower = app_name.lower().strip()
        
        # Handle special cases and aliases
        app_aliases = {
            'browser': 'safari',
            'web browser': 'safari',
            'internet': 'safari',
            'google': 'chrome',
            'google chrome': 'chrome',
            'file manager': 'finder',
            'files': 'finder',
            'command line': 'terminal',
            'cmd': 'terminal',
            'calc': 'calculator',
            'cal': 'calendar',
            'email': 'mail',
            'text editor': 'textedit',
            'editor': 'textedit',
            'preferences': 'system preferences',
            'settings': 'system preferences'
        }
        
        # Check aliases first
        if app_name_lower in app_aliases:
            app_name_lower = app_aliases[app_name_lower]
        
        # Try exact match first
        if app_name_lower in self.applications:
            return self._launch_app(self.applications[app_name_lower], app_name)
        
        # Try partial match
        for app, path in self.applications.items():
            if app_name_lower in app or app in app_name_lower:
                return self._launch_app(path, app)
        
        # Try system command
        try:
            if self.system == "Darwin":
                subprocess.run(['open', '-a', app_name], check=True, capture_output=True)
                return True, f"Successfully opened {app_name}"
        except subprocess.CalledProcessError:
            pass
        
        return False, f"Could not find or open application: {app_name}"
    
    def _launch_app(self, app_path: str, app_name: str) -> Tuple[bool, str]:
        """Launch application at given path"""
        try:
            if self.system == "Darwin":
                subprocess.run(['open', app_path], check=True, capture_output=True)
                return True, f"Successfully opened {app_name}"
        except subprocess.CalledProcessError as e:
            return False, f"Failed to open {app_name}: {str(e)}"
        except Exception as e:
            return False, f"Error opening {app_name}: {str(e)}"
    
    def open_website(self, url: str) -> Tuple[bool, str]:
        """Open a website in the default browser"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            webbrowser.open(url)
            return True, f"Opening {url} in your browser"
        except Exception as e:
            return False, f"Failed to open website: {str(e)}"
    
    def system_command(self, command: str) -> Tuple[bool, str]:
        """Execute system commands safely"""
        safe_commands = {
            'sleep': self._sleep_system,
            'restart': self._restart_system,
            'shutdown': self._shutdown_system,
            'lock': self._lock_system,
            'volume up': lambda: self._adjust_volume('+10'),
            'volume down': lambda: self._adjust_volume('-10'),
            'mute': lambda: self._adjust_volume('0'),
            'unmute': lambda: self._adjust_volume('50'),
            'brightness up': lambda: self._adjust_brightness('+10'),
            'brightness down': lambda: self._adjust_brightness('-10'),
            'wifi on': lambda: self._toggle_wifi(True),
            'wifi off': lambda: self._toggle_wifi(False),
            'bluetooth on': lambda: self._toggle_bluetooth(True),
            'bluetooth off': lambda: self._toggle_bluetooth(False)
        }
        
        command_lower = command.lower().strip()
        
        if command_lower in safe_commands:
            try:
                result = safe_commands[command_lower]()
                return True, result if isinstance(result, str) else f"Executed: {command}"
            except Exception as e:
                return False, f"Failed to execute {command}: {str(e)}"
        
        return False, f"Command '{command}' is not recognized or not safe to execute"
    
    def _sleep_system(self) -> str:
        """Put system to sleep"""
        if self.system == "Darwin":
            subprocess.run(['pmset', 'sleepnow'], check=True)
        return "Putting the system to sleep"
    
    def _restart_system(self) -> str:
        """Restart the system"""
        if self.system == "Darwin":
            subprocess.run(['sudo', 'shutdown', '-r', 'now'], check=True)
        return "Restarting the system"
    
    def _shutdown_system(self) -> str:
        """Shutdown the system"""
        if self.system == "Darwin":
            subprocess.run(['sudo', 'shutdown', '-h', 'now'], check=True)
        return "Shutting down the system"
    
    def _lock_system(self) -> str:
        """Lock the system"""
        if self.system == "Darwin":
            subprocess.run(['/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession', '-suspend'], check=True)
        return "Locking the system"
    
    def _adjust_volume(self, level: str) -> str:
        """Adjust system volume"""
        if self.system == "Darwin":
            if level.startswith(('+', '-')):
                subprocess.run(['osascript', '-e', f'set volume output volume (output volume of (get volume settings) {level})'], check=True)
            else:
                subprocess.run(['osascript', '-e', f'set volume output volume {level}'], check=True)
        return f"Volume adjusted to {level}"
    
    def _adjust_brightness(self, level: str) -> str:
        """Adjust screen brightness"""
        if self.system == "Darwin":
            # This requires additional setup, simplified for now
            return f"Brightness adjustment requested: {level}"
        return "Brightness control not available"
    
    def _toggle_wifi(self, enable: bool) -> str:
        """Toggle WiFi on/off"""
        if self.system == "Darwin":
            action = "on" if enable else "off"
            subprocess.run(['networksetup', '-setairportpower', 'en0', action], check=True)
            return f"WiFi turned {action}"
        return "WiFi control not available"
    
    def _toggle_bluetooth(self, enable: bool) -> str:
        """Toggle Bluetooth on/off"""
        if self.system == "Darwin":
            # This requires additional setup for security
            action = "enabled" if enable else "disabled"
            return f"Bluetooth {action} (requires manual confirmation for security)"
        return "Bluetooth control not available"
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Get battery info if available
            battery = None
            try:
                battery = psutil.sensors_battery()
            except:
                pass
            
            # Get network info
            network = psutil.net_io_counters()
            
            status = {
                'cpu_usage': cpu_percent,
                'memory_total': memory.total,
                'memory_available': memory.available,
                'memory_percent': memory.percent,
                'disk_total': disk.total,
                'disk_free': disk.free,
                'disk_percent': (disk.used / disk.total) * 100,
                'network_sent': network.bytes_sent,
                'network_received': network.bytes_recv,
                'uptime': time.time() - psutil.boot_time()
            }
            
            if battery:
                status['battery_percent'] = battery.percent
                status['battery_plugged'] = battery.power_plugged
                status['battery_time_left'] = battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else None
            
            return status
            
        except Exception as e:
            return {'error': str(e)}
    
    def create_file(self, filename: str, content: str = "") -> Tuple[bool, str]:
        """Create a new file"""
        try:
            with open(filename, 'w') as f:
                f.write(content)
            return True, f"Created file: {filename}"
        except Exception as e:
            return False, f"Failed to create file: {str(e)}"
    
    def create_folder(self, folder_name: str) -> Tuple[bool, str]:
        """Create a new folder"""
        try:
            os.makedirs(folder_name, exist_ok=True)
            return True, f"Created folder: {folder_name}"
        except Exception as e:
            return False, f"Failed to create folder: {str(e)}"
    
    def get_running_applications(self) -> List[str]:
        """Get list of currently running applications"""
        running_apps = []
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name']:
                        running_apps.append(proc.info['name'])
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        except Exception:
            pass
        
        return list(set(running_apps))  # Remove duplicates
    
    def close_application(self, app_name: str) -> Tuple[bool, str]:
        """Close a running application"""
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'] and app_name.lower() in proc.info['name'].lower():
                        proc.terminate()
                        return True, f"Closed {app_name}"
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            return False, f"Could not find running application: {app_name}"
        except Exception as e:
            return False, f"Failed to close application: {str(e)}"
