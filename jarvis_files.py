"""
File Management System for Jarvis
Handles file search, open, create, and management operations
"""
import os
import subprocess
import platform
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import fnmatch
import mimetypes
import config
from jarvis_speed import perf_optimizer, speed_cache, timed_execution

class JarvisFileManager:
    def __init__(self):
        self.search_directories = config.SEARCH_DIRECTORIES
        self.file_cache = {}
        self.recently_accessed = []

    @timed_execution
    @speed_cache('file_search', ttl=600)  # Cache for 10 minutes
    def find_files(self, filename: str, search_dirs: Optional[List[str]] = None) -> List[str]:
        """Find files matching the given filename pattern with caching"""
        if search_dirs is None:
            search_dirs = self.search_directories

        matching_files = []

        # Clean the filename pattern
        filename = filename.strip().lower()

        # Add wildcards if not present
        if not any(char in filename for char in ['*', '?']):
            filename = f"*{filename}*"

        for directory in search_dirs:
            try:
                if os.path.exists(directory):
                    for root, dirs, files in os.walk(directory):
                        # Skip hidden directories and common ignore patterns
                        dirs[:] = [d for d in dirs if not d.startswith('.') and 
                                 d not in ['node_modules', '__pycache__', '.git']]

                        for file in files:
                            if fnmatch.fnmatch(file.lower(), filename):
                                full_path = os.path.join(root, file)
                                matching_files.append(full_path)
            except (PermissionError, OSError) as e:
                print(f"Cannot access directory {directory}: {e}")
                continue

        # Sort by relevance (exact matches first, then by modification time)
        matching_files.sort(key=lambda x: (
            not os.path.basename(x).lower().startswith(filename.replace('*', '')),
            -os.path.getmtime(x) if os.path.exists(x) else 0
        ))

        return matching_files[:20]  # Limit results

    def open_file(self, file_path: str) -> bool:
        """Open file with the default system application"""
        try:
            if not os.path.exists(file_path):
                return False

            system = platform.system()

            if system == "Darwin":  # macOS
                subprocess.run(["open", file_path], check=True)
            elif system == "Windows":
                os.startfile(file_path)
            else:  # Linux
                subprocess.run(["xdg-open", file_path], check=True)

            # Track recently accessed files
            self.recently_accessed.insert(0, file_path)
            self.recently_accessed = self.recently_accessed[:10]  # Keep last 10

            return True

        except Exception as e:
            print(f"Error opening file {file_path}: {e}")
            return False

    def get_file_info(self, file_path: str) -> Dict[str, str]:
        """Get detailed information about a file"""
        if not os.path.exists(file_path):
            return {"error": "File not found"}

        try:
            stat_info = os.stat(file_path)
            file_size = stat_info.st_size

            # Format file size
            if file_size < 1024:
                size_str = f"{file_size} bytes"
            elif file_size < 1024 * 1024:
                size_str = f"{file_size / 1024:.1f} KB"
            elif file_size < 1024 * 1024 * 1024:
                size_str = f"{file_size / (1024 * 1024):.1f} MB"
            else:
                size_str = f"{file_size / (1024 * 1024 * 1024):.1f} GB"

            # Get file type
            mime_type, _ = mimetypes.guess_type(file_path)
            file_type = mime_type if mime_type else "Unknown"

            return {
                "name": os.path.basename(file_path),
                "path": file_path,
                "size": size_str,
                "type": file_type,
                "modified": self._format_timestamp(stat_info.st_mtime),
                "created": self._format_timestamp(stat_info.st_ctime)
            }

        except Exception as e:
            return {"error": f"Cannot get file info: {e}"}

    def create_file(self, file_path: str, content: str = "") -> bool:
        """Create a new file with optional content"""
        try:
            # Ensure directory exists
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return True

        except Exception as e:
            print(f"Error creating file {file_path}: {e}")
            return False

    def read_file_content(self, file_path: str, max_lines: int = 50) -> str:
        """Read and return file content (limited for large files)"""
        try:
            if not os.path.exists(file_path):
                return "File not found"

            # Check if file is binary
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                if b'\0' in chunk:
                    return "Binary file - cannot display content"

            # Read text file
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

                if len(lines) <= max_lines:
                    return ''.join(lines)
                else:
                    content = ''.join(lines[:max_lines])
                    content += f"\n... (showing first {max_lines} lines of {len(lines)} total lines)"
                    return content

        except Exception as e:
            return f"Error reading file: {e}"

    @timed_execution
    @speed_cache('content_search', ttl=300)  # Cache for 5 minutes
    def search_in_files(self, search_term: str, file_pattern: str = "*", 
                       search_dirs: Optional[List[str]] = None) -> List[Dict[str, str]]:
        """Search for text within files with caching"""
        if search_dirs is None:
            search_dirs = self.search_directories

        results = []
        search_term = search_term.lower()

        for directory in search_dirs:
            try:
                if not os.path.exists(directory):
                    continue

                for root, dirs, files in os.walk(directory):
                    # Skip hidden directories
                    dirs[:] = [d for d in dirs if not d.startswith('.')]

                    for file in files:
                        if fnmatch.fnmatch(file.lower(), file_pattern.lower()):
                            file_path = os.path.join(root, file)

                            try:
                                # Skip binary files
                                with open(file_path, 'rb') as f:
                                    if b'\0' in f.read(1024):
                                        continue

                                # Search in text files
                                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                    for line_num, line in enumerate(f, 1):
                                        if search_term in line.lower():
                                            results.append({
                                                "file": file_path,
                                                "line": line_num,
                                                "content": line.strip()
                                            })

                                            if len(results) >= 20:  # Limit results
                                                return results

                            except (PermissionError, UnicodeDecodeError):
                                continue

            except (PermissionError, OSError):
                continue

        return results

    def get_directory_contents(self, directory_path: str) -> List[Dict[str, str]]:
        """Get contents of a directory"""
        try:
            if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
                return []

            contents = []
            for item in os.listdir(directory_path):
                if item.startswith('.'):  # Skip hidden files
                    continue

                item_path = os.path.join(directory_path, item)
                is_dir = os.path.isdir(item_path)

                contents.append({
                    "name": item,
                    "path": item_path,
                    "type": "directory" if is_dir else "file",
                    "size": "" if is_dir else self._get_human_size(os.path.getsize(item_path))
                })

            # Sort: directories first, then files
            contents.sort(key=lambda x: (x["type"] != "directory", x["name"].lower()))
            return contents

        except Exception as e:
            print(f"Error reading directory {directory_path}: {e}")
            return []

    def _format_timestamp(self, timestamp: float) -> str:
        """Format timestamp to readable string"""
        from datetime import datetime
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

    def _get_human_size(self, size: int) -> str:
        """Convert size to human readable format"""
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        elif size < 1024 * 1024 * 1024:
            return f"{size / (1024 * 1024):.1f} MB"
        else:
            return f"{size / (1024 * 1024 * 1024):.1f} GB"

    def get_recent_files(self) -> List[str]:
        """Get recently accessed files"""
        return [f for f in self.recently_accessed if os.path.exists(f)]

    def smart_file_search(self, query: str) -> List[str]:
        """Intelligent file search based on query"""
        # Extract file extension if mentioned
        extensions = {
            'text': ['.txt', '.md', '.rtf'],
            'document': ['.doc', '.docx', '.pdf'],
            'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
            'video': ['.mp4', '.avi', '.mov', '.mkv'],
            'audio': ['.mp3', '.wav', '.flac', '.m4a'],
            'code': ['.py', '.js', '.html', '.css', '.java', '.cpp'],
            'data': ['.csv', '.json', '.xml', '.xlsx']
        }

        # Check if query mentions file type
        search_extensions = []
        query_lower = query.lower()
        for file_type, exts in extensions.items():
            if file_type in query_lower:
                search_extensions.extend(exts)

        # Search for files
        results = self.find_files(query)

        # Filter by extension if specified
        if search_extensions:
            results = [f for f in results if any(f.lower().endswith(ext) for ext in search_extensions)]

        return results
