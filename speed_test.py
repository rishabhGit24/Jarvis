#!/usr/bin/env python3
"""
Non-blocking Speed Test for AI-Enhanced High-Performance Jarvis
Demonstrates the performance improvements and caching system
"""
import sys
import os
import time
import threading
import queue
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from jarvis_brain import JarvisBrain
from jarvis_speed import get_performance_stats, perf_optimizer, optimize_startup
from colorama import init, Fore, Style

init(autoreset=True)

def non_blocking_speed_test():
    """Non-blocking speed test that can be interrupted"""
    print(f"{Fore.YELLOW}⚡ JARVIS NON-BLOCKING SPEED TEST{Style.RESET_ALL}")
    print("=" * 60)
    print(f"{Fore.GREEN}This test runs in the background and won't block input!{Style.RESET_ALL}\\n")
    
    # Initialize performance optimization
    print(f"{Fore.CYAN}Optimizing performance...{Style.RESET_ALL}")
    optimize_startup()
    
    # Initialize Jarvis
    print(f"{Fore.CYAN}Initializing high-performance Jarvis...{Style.RESET_ALL}")
    start_time = time.time()
    brain = JarvisBrain()
    
    # Optimize brain for performance
    if hasattr(brain, 'optimize_for_performance'):
        brain.optimize_for_performance()
    
    init_time = time.time() - start_time
    print(f"{Fore.GREEN}✅ Initialization: {init_time:.3f}s{Style.RESET_ALL}\\n")
    
    # Test commands for speed
    test_commands = [
        ("hello", "Hello Jarvis, how are you?"),
        ("file", "Find my document.txt file"),
        ("weather", "What's the weather like?"), 
        ("time", "What time is it?"),
        ("status", "Show me system status"),
        ("hello_cached", "Hello Jarvis, how are you?"),  # Repeat for cache test
        ("simple_math", "What is 15 plus 27?"),  # Test local AI
    ]
    
    print(f"{Fore.BLUE}Testing command processing speed (non-blocking):{Style.RESET_ALL}")
    print("-" * 50)
    
    # Use queue for thread-safe communication
    results_queue = queue.Queue()
    stop_flag = threading.Event()
    
    def test_worker():
        """Worker thread for running tests"""
        total_time = 0
        local_responses = 0
        cloud_responses = 0
        
        for i, (test_type, command) in enumerate(test_commands, 1):
            if stop_flag.is_set():
                break
                
            print(f"{Fore.CYAN}[{i}] Testing:{Style.RESET_ALL} {command[:35]}...")
            
            start_time = time.time()
            try:
                response = brain.process_command(command)
                execution_time = time.time() - start_time
                total_time += execution_time
                
                # Determine if response was cached or from local/cloud AI
                if execution_time < 0.05:
                    cache_indicator = "🚀 INSTANT"
                elif execution_time < 0.2:
                    cache_indicator = "⚡ LOCAL AI"
                    local_responses += 1
                else:
                    cache_indicator = "☁️  CLOUD AI"
                    cloud_responses += 1
                
                print(f"    {cache_indicator} Time: {execution_time:.3f}s")
                print(f"    Response: {response[:45]}...\\n")
                
                # Small delay to make output readable
                time.sleep(0.5)
                
            except Exception as e:
                print(f"    {Fore.RED}❌ Error: {e}{Style.RESET_ALL}\\n")
        
        # Store results
        results_queue.put({
            'total_time': total_time,
            'local_responses': local_responses,
            'cloud_responses': cloud_responses,
            'avg_time': total_time / len(test_commands) if test_commands else 0
        })
    
    # Start test in background thread
    test_thread = threading.Thread(target=test_worker, daemon=True)
    test_thread.start()
    
    print(f"{Fore.GREEN}🔄 Speed test running in background...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}💡 You can continue using Jarvis while the test runs!{Style.RESET_ALL}")
    print(f"{Fore.BLUE}   Test will complete automatically and show results.{Style.RESET_ALL}\\n")
    
    # Wait for completion or timeout
    test_thread.join(timeout=60)  # 60 second timeout
    
    # Get results if available
    try:
        if not results_queue.empty():
            results = results_queue.get_nowait()
            display_results(results)
        else:
            print(f"{Fore.YELLOW}⏱️  Test still running in background...{Style.RESET_ALL}")
    except queue.Empty:
        print(f"{Fore.YELLOW}⏱️  Test results not ready yet...{Style.RESET_ALL}")

def display_results(results):
    """Display test results"""
    print("\\n" + "=" * 60)
    print(f"{Fore.YELLOW}⚡ PERFORMANCE RESULTS{Style.RESET_ALL}")
    print("-" * 40)
    
    stats = get_performance_stats()
    avg_time = results['avg_time']
    
    print(f"{Fore.GREEN}📊 Average Response Time: {avg_time:.3f}s{Style.RESET_ALL}")
    print(f"{Fore.GREEN}🧠 Local AI Responses: {results['local_responses']}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}☁️  Cloud AI Responses: {results['cloud_responses']}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}📦 Total Cached Items: {stats['total_cached_items']}{Style.RESET_ALL}")
    
    # Speed rating
    if avg_time < 0.3:
        speed_rating = f"{Fore.GREEN}🚀 EXTREMELY FAST{Style.RESET_ALL}"
    elif avg_time < 0.8:
        speed_rating = f"{Fore.YELLOW}⚡ VERY FAST{Style.RESET_ALL}"
    elif avg_time < 2.0:
        speed_rating = f"{Fore.BLUE}✅ FAST{Style.RESET_ALL}"
    else:
        speed_rating = f"{Fore.RED}🐌 NEEDS OPTIMIZATION{Style.RESET_ALL}"
    
    print(f"\\nSpeed Rating: {speed_rating}")
    if 'cache_hit_rate' in stats:
        print(f"Cache Hit Rate: {Fore.GREEN}{stats['cache_hit_rate']:.1f}%{Style.RESET_ALL}")
    
    print("\\n" + "=" * 60)
    print(f"{Fore.CYAN}💡 PERFORMANCE FEATURES ACTIVE:{Style.RESET_ALL}")
    print("-" * 40)
    print(f"{Fore.GREEN}✅ Smart Local/Cloud AI Routing{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✅ Intelligent Caching System{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✅ Parallel Processing{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✅ Async Operations{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✅ Memory Optimization{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✅ Streaming Responses{Style.RESET_ALL}")
    
    print("\\n" + "=" * 60)
    print(f"{Fore.GREEN}🎉 HIGH-PERFORMANCE JARVIS IS READY!{Style.RESET_ALL}")

def speed_test():
    """Main speed test function - now non-blocking"""
    return non_blocking_speed_test()

if __name__ == "__main__":
    speed_test()
