"""
High-Performance Speed Optimization Module for Jarvis
Implements caching, async processing, streaming responses, and performance enhancements
"""
import asyncio
import time
import threading
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache, wraps
from typing import Dict, Any, Optional, Callable, List, Generator, AsyncGenerator
import json
import hashlib
import os
import gc
import sys
from datetime import datetime, timedelta
import weakref

class SpeedCache:
    """Ultra-fast in-memory cache with TTL support"""
    
    def __init__(self, default_ttl: int = 300):  # 5 minutes default
        self.cache = {}
        self.timestamps = {}
        self.default_ttl = default_ttl
        self._lock = threading.RLock()
    
    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key not in self.cache:
                return None
            
            # Check if expired
            if time.time() - self.timestamps[key] > self.default_ttl:
                del self.cache[key]
                del self.timestamps[key]
                return None
            
            return self.cache[key]
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        with self._lock:
            self.cache[key] = value
            self.timestamps[key] = time.time()
    
    def clear_expired(self):
        """Background cleanup of expired entries"""
        with self._lock:
            current_time = time.time()
            expired_keys = [
                key for key, timestamp in self.timestamps.items()
                if current_time - timestamp > self.default_ttl
            ]
            for key in expired_keys:
                del self.cache[key]
                del self.timestamps[key]

class AsyncProcessor:
    """Advanced asynchronous task processor with streaming and parallel operations"""
    
    def __init__(self, max_workers: int = 8):  # Increased for better performance
        self.executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="jarvis-async")
        self.loop = None
        self.streaming_queue = queue.Queue()
        self._shutdown = False
        
        # Start async event loop in background thread
        self.loop_thread = threading.Thread(target=self._run_event_loop, daemon=True)
        self.loop_thread.start()
    
    def _run_event_loop(self):
        """Run async event loop in background thread"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
    
    def submit_task(self, func: Callable, *args, **kwargs):
        """Submit a task for async execution"""
        return self.executor.submit(func, *args, **kwargs)
    
    def submit_multiple(self, tasks: List[tuple]) -> List[Any]:
        """Submit multiple tasks and return results as they complete"""
        futures = []
        for func, args, kwargs in tasks:
            future = self.executor.submit(func, *args, **kwargs)
            futures.append(future)
        
        results = []
        for future in as_completed(futures, timeout=10):  # Increased timeout
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                results.append(f"Error: {e}")
        
        return results
    
    def stream_task(self, func: Callable, *args, **kwargs) -> Generator[Any, None, None]:
        """Stream results from a function that yields partial results"""
        def wrapper():
            try:
                for result in func(*args, **kwargs):
                    self.streaming_queue.put(result)
                self.streaming_queue.put(StopIteration)
            except Exception as e:
                self.streaming_queue.put(e)
        
        future = self.executor.submit(wrapper)
        
        while True:
            try:
                result = self.streaming_queue.get(timeout=1)
                if isinstance(result, StopIteration):
                    break
                elif isinstance(result, Exception):
                    raise result
                else:
                    yield result
            except queue.Empty:
                if future.done():
                    break
                continue
    
    async def async_submit(self, func: Callable, *args, **kwargs):
        """Submit task to async event loop"""
        if self.loop and not self.loop.is_closed():
            return await self.loop.run_in_executor(self.executor, func, *args, **kwargs)
        else:
            return self.submit_task(func, *args, **kwargs).result()
    
    def parallel_map(self, func: Callable, items: List[Any], max_concurrent: int = 4) -> List[Any]:
        """Execute function on multiple items in parallel with concurrency limit"""
        results = [None] * len(items)
        
        def process_item(index, item):
            try:
                return index, func(item)
            except Exception as e:
                return index, f"Error: {e}"
        
        # Process in batches to limit concurrent operations
        for i in range(0, len(items), max_concurrent):
            batch = items[i:i + max_concurrent]
            batch_tasks = [(process_item, (i + j, item), {}) for j, item in enumerate(batch)]
            batch_results = self.submit_multiple(batch_tasks)
            
            for idx, result in batch_results:
                results[idx] = result
        
        return results
    
    def shutdown(self):
        self._shutdown = True
        if self.loop and not self.loop.is_closed():
            self.loop.call_soon_threadsafe(self.loop.stop)
        self.executor.shutdown(wait=True)

class PerformanceOptimizer:
    """Main performance optimization controller with intelligent caching and memory management"""
    
    def __init__(self):
        self.cache = SpeedCache()
        self.async_processor = AsyncProcessor()
        self.response_cache = SpeedCache(default_ttl=60)  # 1 minute for responses
        self.file_cache = SpeedCache(default_ttl=600)     # 10 minutes for file searches
        self.ai_cache = SpeedCache(default_ttl=300)       # 5 minutes for AI responses
        self.stream_cache = SpeedCache(default_ttl=30)    # 30 seconds for streaming responses
        
        # Memory management
        self._memory_threshold = 500 * 1024 * 1024  # 500MB threshold
        self._last_gc = time.time()
        
        # Performance tracking
        self.performance_metrics = {
            'cache_hits': 0,
            'cache_misses': 0,
            'async_tasks_completed': 0,
            'memory_cleanups': 0,
            'startup_time': 0
        }
        
        # Start background cleanup
        self._start_cleanup_thread()
    
    def _start_cleanup_thread(self):
        """Start background thread for cache cleanup and memory management"""
        def cleanup_worker():
            while True:
                time.sleep(60)  # Cleanup every minute
                self.cache.clear_expired()
                self.response_cache.clear_expired()
                self.file_cache.clear_expired()
                self.ai_cache.clear_expired()
                self.stream_cache.clear_expired()
                
                # Memory management
                self._manage_memory()
                
                # Update performance metrics
                self.performance_metrics['memory_cleanups'] += 1
        
        cleanup_thread = threading.Thread(target=cleanup_worker, daemon=True)
        cleanup_thread.start()
    
    def _manage_memory(self):
        """Intelligent memory management"""
        current_time = time.time()
        
        # Force garbage collection every 5 minutes
        if current_time - self._last_gc > 300:
            gc.collect()
            self._last_gc = current_time
        
        # Check memory usage and clear caches if needed
        try:
            import psutil
            process = psutil.Process()
            memory_usage = process.memory_info().rss
            
            if memory_usage > self._memory_threshold:
                # Clear oldest cache entries
                self._emergency_cache_cleanup()
                gc.collect()
                
        except ImportError:
            # Fallback if psutil not available
            if current_time % 600 == 0:  # Every 10 minutes
                gc.collect()
    
    def _emergency_cache_cleanup(self):
        """Emergency cache cleanup when memory is low"""
        # Clear half of each cache
        for cache in [self.cache, self.response_cache, self.file_cache, self.ai_cache, self.stream_cache]:
            items_to_remove = len(cache.cache) // 2
            if items_to_remove > 0:
                keys_to_remove = list(cache.cache.keys())[:items_to_remove]
                for key in keys_to_remove:
                    if key in cache.cache:
                        del cache.cache[key]
                        del cache.timestamps[key]
    
    def cache_key(self, prefix: str, *args) -> str:
        """Generate cache key from arguments"""
        key_data = f"{prefix}:{':'.join(str(arg) for arg in args)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def cached_ai_response(self, func):
        """Decorator for caching AI responses"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function arguments
            cache_key = self.cache_key('ai', func.__name__, *args, str(kwargs))
            
            # Try to get from cache
            cached_result = self.ai_cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            self.ai_cache.set(cache_key, result)
            return result
        
        return wrapper
    
    def cached_file_search(self, func):
        """Decorator for caching file search results"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = self.cache_key('file', func.__name__, *args, str(kwargs))
            
            cached_result = self.file_cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            result = func(*args, **kwargs)
            self.file_cache.set(cache_key, result)
            return result
        
        return wrapper
    
    def parallel_execute(self, tasks: List[tuple]) -> List[Any]:
        """Execute multiple tasks in parallel"""
        return self.async_processor.submit_multiple(tasks)
    
    def stream_response(self, func: Callable, *args, **kwargs) -> Generator[str, None, None]:
        """Stream response chunks for real-time processing"""
        cache_key = self.cache_key('stream', func.__name__, *args, str(kwargs))
        
        # Check if we have cached streaming response
        cached_stream = self.stream_cache.get(cache_key)
        if cached_stream:
            for chunk in cached_stream:
                yield chunk
            return
        
        # Generate and cache stream
        stream_chunks = []
        try:
            for chunk in self.async_processor.stream_task(func, *args, **kwargs):
                stream_chunks.append(chunk)
                yield chunk
            
            # Cache the complete stream
            self.stream_cache.set(cache_key, stream_chunks)
            
        except Exception as e:
            yield f"Stream error: {e}"
    
    def intelligent_cache_get(self, cache_type: str, key: str) -> Optional[Any]:
        """Intelligent cache retrieval with performance tracking"""
        cache_map = {
            'default': self.cache,
            'response': self.response_cache,
            'file': self.file_cache,
            'ai': self.ai_cache,
            'stream': self.stream_cache
        }
        
        cache = cache_map.get(cache_type, self.cache)
        result = cache.get(key)
        
        if result is not None:
            self.performance_metrics['cache_hits'] += 1
        else:
            self.performance_metrics['cache_misses'] += 1
        
        return result
    
    def intelligent_cache_set(self, cache_type: str, key: str, value: Any, ttl: Optional[int] = None):
        """Intelligent cache storage with automatic optimization"""
        cache_map = {
            'default': self.cache,
            'response': self.response_cache,
            'file': self.file_cache,
            'ai': self.ai_cache,
            'stream': self.stream_cache
        }
        
        cache = cache_map.get(cache_type, self.cache)
        
        # Estimate memory usage and adjust TTL if needed
        try:
            value_size = sys.getsizeof(value)
            if value_size > 1024 * 1024:  # 1MB
                # Large objects get shorter TTL
                ttl = min(ttl or cache.default_ttl, 60)
        except:
            pass
        
        cache.set(key, value, ttl)
    
    def preload_common_responses(self):
        """Preload commonly used responses for instant access"""
        common_responses = {
            'greeting_morning': "Good morning, Mr. Bharadwaj Sir. How may I assist you today?",
            'greeting_afternoon': "Good afternoon, Mr. Bharadwaj. At your service.",
            'greeting_evening': "Good evening, Mr. Bharadwaj Sir. How may I be of assistance?",
            'acknowledgment': "Certainly, Mr. Bharadwaj Sir. Right away.",
            'processing': "Processing your request, Mr. Bharadwaj Sir.",
            'completed': "Task completed successfully, Mr. Bharadwaj Sir.",
            'error': "I encountered an issue, Mr. Bharadwaj Sir. Please try again."
        }
        
        for key, response in common_responses.items():
            self.response_cache.set(key, response, ttl=3600)  # Cache for 1 hour
    
    def get_instant_response(self, response_type: str) -> Optional[str]:
        """Get preloaded response instantly"""
        return self.response_cache.get(response_type)
    
    def shutdown(self):
        """Cleanup resources"""
        self.async_processor.shutdown()

# Global performance optimizer instance
perf_optimizer = PerformanceOptimizer()

def speed_cache(cache_type: str = 'default', ttl: int = 300):
    """Decorator for general caching"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = perf_optimizer.cache_key(cache_type, func.__name__, *args, str(kwargs))
            
            cached_result = perf_optimizer.cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            result = func(*args, **kwargs)
            perf_optimizer.cache.set(cache_key, result)
            return result
        
        return wrapper
    return decorator

def async_task(func):
    """Decorator to make functions run asynchronously"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return perf_optimizer.async_processor.submit_task(func, *args, **kwargs)
    return wrapper

def timed_execution(func):
    """Decorator to measure execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        print(f"⚡ {func.__name__} executed in {execution_time:.3f}s")
        return result
    return wrapper

class FastResponse:
    """Ultra-fast response generation"""
    
    def __init__(self):
        self.quick_responses = {
            # Instant acknowledgments
            'hello': ["Good day, Mr. Bharadwaj Sir.", "At your service, Mr. Bharadwaj.", "How may I assist you, Mr. Bharadwaj Sir?"],
            'thanks': ["My pleasure, Mr. Bharadwaj Sir.", "You're most welcome, Mr. Bharadwaj.", "It's my honour to serve, Mr. Bharadwaj Sir."],
            'status': ["All systems operational, Mr. Bharadwaj Sir.", "Functioning optimally, Mr. Bharadwaj.", "Ready for your commands, Mr. Bharadwaj Sir."],
            
            # Quick confirmations
            'yes': ["Certainly, Mr. Bharadwaj Sir.", "Of course, Mr. Bharadwaj.", "Right away, Mr. Bharadwaj Sir."],
            'processing': ["One moment please, Mr. Bharadwaj Sir.", "Processing now, Mr. Bharadwaj.", "Working on that, Mr. Bharadwaj Sir."],
            'completed': ["Done, Mr. Bharadwaj Sir.", "Completed successfully, Mr. Bharadwaj.", "Task finished, Mr. Bharadwaj Sir."],
            
            # Error responses
            'error': ["I apologize, Mr. Bharadwaj Sir.", "Something went wrong, Mr. Bharadwaj.", "Let me try again, Mr. Bharadwaj Sir."],
            'unclear': ["Could you clarify that, Mr. Bharadwaj Sir?", "I didn't quite catch that, Mr. Bharadwaj.", "Please repeat, Mr. Bharadwaj Sir."]
        }
    
    def get_instant(self, response_type: str) -> str:
        """Get instant response without AI processing"""
        import random
        responses = self.quick_responses.get(response_type, self.quick_responses['yes'])
        return random.choice(responses)

# Global fast response instance
fast_response = FastResponse()

def optimize_startup():
    """Optimize Jarvis startup time with parallel initialization"""
    print("⚡ Initializing high-performance mode...")
    start_time = time.time()
    
    # Record startup time
    perf_optimizer.performance_metrics['startup_time'] = start_time
    
    # Parallel initialization tasks
    def preload_responses():
        perf_optimizer.preload_common_responses()
    
    def warm_caches():
        # Pre-cache common file extensions
        common_extensions = ['.txt', '.pdf', '.doc', '.docx', '.py', '.js', '.html', '.css']
        for ext in common_extensions:
            cache_key = perf_optimizer.cache_key('file_ext', ext)
            perf_optimizer.file_cache.set(cache_key, [], ttl=1800)  # 30 minutes
    
    def optimize_memory():
        # Initial garbage collection
        gc.collect()
        
        # Set optimal garbage collection thresholds
        gc.set_threshold(700, 10, 10)
    
    def preload_system_info():
        # Pre-cache system information
        try:
            import psutil
            cpu_info = psutil.cpu_percent(interval=None)
            memory_info = psutil.virtual_memory()
            
            cache_key = perf_optimizer.cache_key('system', 'basic_info')
            perf_optimizer.cache.set(cache_key, {
                'cpu': cpu_info,
                'memory': memory_info.percent
            }, ttl=60)
        except:
            pass
    
    # Execute initialization tasks in parallel
    tasks = [
        (preload_responses, (), {}),
        (warm_caches, (), {}),
        (optimize_memory, (), {}),
        (preload_system_info, (), {})
    ]
    
    perf_optimizer.parallel_execute(tasks)
    
    startup_time = time.time() - start_time
    perf_optimizer.performance_metrics['startup_time'] = startup_time
    print(f"⚡ Performance optimization ready in {startup_time:.3f}s")

def get_performance_stats() -> Dict[str, Any]:
    """Get comprehensive performance statistics"""
    base_stats = {
        'cache_size': len(perf_optimizer.cache.cache),
        'ai_cache_size': len(perf_optimizer.ai_cache.cache),
        'file_cache_size': len(perf_optimizer.file_cache.cache),
        'response_cache_size': len(perf_optimizer.response_cache.cache),
        'stream_cache_size': len(perf_optimizer.stream_cache.cache),
        'total_cached_items': (
            len(perf_optimizer.cache.cache) +
            len(perf_optimizer.ai_cache.cache) +
            len(perf_optimizer.file_cache.cache) +
            len(perf_optimizer.response_cache.cache) +
            len(perf_optimizer.stream_cache.cache)
        )
    }
    
    # Add performance metrics
    base_stats.update(perf_optimizer.performance_metrics)
    
    # Calculate cache hit rate
    total_requests = base_stats['cache_hits'] + base_stats['cache_misses']
    base_stats['cache_hit_rate'] = (
        base_stats['cache_hits'] / total_requests if total_requests > 0 else 0.0
    )
    
    # Add memory usage if available
    try:
        import psutil
        process = psutil.Process()
        base_stats['memory_usage_mb'] = process.memory_info().rss / (1024 * 1024)
        base_stats['cpu_percent'] = process.cpu_percent()
    except:
        pass
    
    return base_stats

# New streaming decorator for real-time responses
def stream_response(func):
    """Decorator to enable streaming responses"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return perf_optimizer.stream_response(func, *args, **kwargs)
    return wrapper

# Enhanced async decorator with better error handling
def enhanced_async(func):
    """Enhanced async decorator with caching and error handling"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            future = perf_optimizer.async_processor.submit_task(func, *args, **kwargs)
            result = future.result(timeout=30)  # 30 second timeout
            perf_optimizer.performance_metrics['async_tasks_completed'] += 1
            return result
        except Exception as e:
            return f"Async task error: {e}"
    return wrapper
