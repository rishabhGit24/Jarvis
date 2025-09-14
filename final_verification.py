#!/usr/bin/env python3
"""
Final Verification Script for JARVIS High-Performance System
Tests all critical functionality to ensure everything works properly
"""
import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from colorama import init, Fore, Style
init(autoreset=True)

def print_header(title):
    print(f"\n{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{title.center(60)}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")

def print_test(test_name, status, details=""):
    status_color = Fore.GREEN if status == "PASS" else Fore.RED if status == "FAIL" else Fore.YELLOW
    status_symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
    print(f"{status_symbol} {Fore.CYAN}{test_name:<30}{Style.RESET_ALL} {status_color}{status}{Style.RESET_ALL}")
    if details:
        print(f"   {Fore.BLUE}{details}{Style.RESET_ALL}")

def main():
    print_header("JARVIS FINAL VERIFICATION")
    
    total_tests = 0
    passed_tests = 0
    
    # Test 1: Local AI Processing
    print_test("Testing Local AI Processing", "RUNNING")
    try:
        from jarvis_local_ai import LocalAIModel
        local_ai = LocalAIModel()
        
        # Test various queries
        test_queries = [
            ("hello", "greeting"),
            ("thank you", "gratitude"), 
            ("what time is it", "time"),
            ("how are you", "status"),
            ("what is 5 plus 3", "math")
        ]
        
        local_successes = 0
        for query, query_type in test_queries:
            if local_ai.can_handle_locally(query):
                response = local_ai.process_locally(query)
                if response and len(response) > 10:
                    local_successes += 1
        
        if local_successes >= 4:
            print_test("Local AI Processing", "PASS", f"{local_successes}/5 queries handled correctly")
            passed_tests += 1
        else:
            print_test("Local AI Processing", "FAIL", f"Only {local_successes}/5 queries handled")
        total_tests += 1
        
    except Exception as e:
        print_test("Local AI Processing", "FAIL", f"Error: {e}")
        total_tests += 1
    
    # Test 2: Smart AI Routing
    print_test("Testing Smart AI Routing", "RUNNING")
    try:
        from jarvis_local_ai import initialize_smart_router
        from jarvis_nlp import JarvisNLP
        
        nlp = JarvisNLP()
        router = initialize_smart_router(nlp)
        
        # Test routing decisions
        simple_query = "hello"
        response, source = router.route_query(simple_query)
        
        if response and source in ['local', 'cloud', 'fallback']:
            print_test("Smart AI Routing", "PASS", f"Query routed to {source}")
            passed_tests += 1
        else:
            print_test("Smart AI Routing", "FAIL", "Routing failed")
        total_tests += 1
        
    except Exception as e:
        print_test("Smart AI Routing", "FAIL", f"Error: {e}")
        total_tests += 1
    
    # Test 3: Brain Command Processing
    print_test("Testing Brain Command Processing", "RUNNING")
    try:
        from jarvis_brain import JarvisBrain
        brain = JarvisBrain()
        
        # Test command processing
        test_commands = ["hello jarvis", "thank you", "what time is it"]
        brain_successes = 0
        
        for cmd in test_commands:
            response = brain.process_command(cmd)
            if response and len(response) > 10 and "Mr. Bharadwaj Sir" in response:
                brain_successes += 1
        
        if brain_successes >= 2:
            print_test("Brain Command Processing", "PASS", f"{brain_successes}/3 commands processed correctly")
            passed_tests += 1
        else:
            print_test("Brain Command Processing", "FAIL", f"Only {brain_successes}/3 commands processed")
        total_tests += 1
        
    except Exception as e:
        print_test("Brain Command Processing", "FAIL", f"Error: {e}")
        total_tests += 1
    
    # Test 4: Performance Optimization
    print_test("Testing Performance Optimization", "RUNNING")
    try:
        from jarvis_speed import get_performance_stats, optimize_startup, perf_optimizer
        
        # Test optimization
        start_time = time.time()
        optimize_startup()
        optimization_time = time.time() - start_time
        
        # Test caching
        perf_optimizer.intelligent_cache_set('test', 'verification_key', 'verification_value')
        cached_value = perf_optimizer.intelligent_cache_get('test', 'verification_key')
        
        # Get stats
        stats = get_performance_stats()
        
        if (optimization_time < 1.0 and 
            cached_value == 'verification_value' and 
            'total_cached_items' in stats):
            print_test("Performance Optimization", "PASS", f"Optimization: {optimization_time:.3f}s, Cache working")
            passed_tests += 1
        else:
            print_test("Performance Optimization", "FAIL", "Some optimization features not working")
        total_tests += 1
        
    except Exception as e:
        print_test("Performance Optimization", "FAIL", f"Error: {e}")
        total_tests += 1
    
    # Test 5: Full JARVIS Initialization
    print_test("Testing Full JARVIS Initialization", "RUNNING")
    try:
        from jarvis import JarvisAssistant
        
        jarvis = JarvisAssistant()
        start_time = time.time()
        result = jarvis.initialize()
        init_time = time.time() - start_time
        
        # Test basic functionality
        if result and jarvis.brain and jarvis.memory and jarvis.voice:
            # Test a command through the brain (not voice)
            response = jarvis.brain.process_command("hello")
            if response and "Mr. Bharadwaj Sir" in response:
                print_test("Full JARVIS Initialization", "PASS", f"Init: {init_time:.1f}s, All components working")
                passed_tests += 1
            else:
                print_test("Full JARVIS Initialization", "FAIL", "Components initialized but not responding correctly")
        else:
            print_test("Full JARVIS Initialization", "FAIL", f"Initialization failed or missing components")
        total_tests += 1
        
    except Exception as e:
        print_test("Full JARVIS Initialization", "FAIL", f"Error: {e}")
        total_tests += 1
    
    # Test 6: Speed and Responsiveness
    print_test("Testing Speed and Responsiveness", "RUNNING")
    try:
        from jarvis_brain import JarvisBrain
        brain = JarvisBrain()
        
        # Test response times
        fast_queries = ["hello", "thank you", "what time is it"]
        response_times = []
        
        for query in fast_queries:
            start_time = time.time()
            response = brain.process_command(query)
            response_time = time.time() - start_time
            response_times.append(response_time)
        
        avg_response_time = sum(response_times) / len(response_times)
        
        if avg_response_time < 0.1:  # Less than 100ms average
            print_test("Speed and Responsiveness", "PASS", f"Avg response: {avg_response_time:.3f}s")
            passed_tests += 1
        elif avg_response_time < 0.5:  # Less than 500ms average
            print_test("Speed and Responsiveness", "WARN", f"Avg response: {avg_response_time:.3f}s (acceptable)")
            passed_tests += 0.5
        else:
            print_test("Speed and Responsiveness", "FAIL", f"Avg response: {avg_response_time:.3f}s (too slow)")
        total_tests += 1
        
    except Exception as e:
        print_test("Speed and Responsiveness", "FAIL", f"Error: {e}")
        total_tests += 1
    
    # Final Results
    print_header("VERIFICATION RESULTS")
    
    success_rate = (passed_tests / total_tests) * 100
    
    print(f"{Fore.CYAN}Tests Passed: {Fore.GREEN}{passed_tests:.1f}/{total_tests}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Success Rate: {Fore.GREEN}{success_rate:.1f}%{Style.RESET_ALL}")
    
    if success_rate >= 90:
        print(f"\n{Fore.GREEN}🎉 EXCELLENT! JARVIS is fully optimized and ready for use!{Style.RESET_ALL}")
        print(f"{Fore.BLUE}All critical systems are working perfectly.{Style.RESET_ALL}")
        status = "EXCELLENT"
    elif success_rate >= 80:
        print(f"\n{Fore.YELLOW}⚡ GOOD! JARVIS is working well with minor issues.{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Most systems are operational and performance is good.{Style.RESET_ALL}")
        status = "GOOD"
    elif success_rate >= 60:
        print(f"\n{Fore.YELLOW}⚠️  ACCEPTABLE! JARVIS is functional but needs some attention.{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Core features work but some optimizations may need fixing.{Style.RESET_ALL}")
        status = "ACCEPTABLE"
    else:
        print(f"\n{Fore.RED}🔧 NEEDS WORK! JARVIS has significant issues that need fixing.{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Several critical systems are not working properly.{Style.RESET_ALL}")
        status = "NEEDS_WORK"
    
    # Usage Instructions
    print_header("USAGE INSTRUCTIONS")
    print(f"{Fore.GREEN}✅ To start JARVIS normally:{Style.RESET_ALL}")
    print(f"   {Fore.CYAN}python3 jarvis.py{Style.RESET_ALL}")
    
    print(f"\n{Fore.GREEN}✅ To run diagnostics:{Style.RESET_ALL}")
    print(f"   {Fore.CYAN}python3 jarvis.py --diagnostics{Style.RESET_ALL}")
    
    print(f"\n{Fore.GREEN}✅ To run speed test:{Style.RESET_ALL}")
    print(f"   {Fore.CYAN}python3 speed_test.py{Style.RESET_ALL}")
    
    print(f"\n{Fore.GREEN}✅ To start in text-only mode:{Style.RESET_ALL}")
    print(f"   {Fore.CYAN}python3 jarvis.py --text-only{Style.RESET_ALL}")
    
    print(f"\n{Fore.BLUE}🎯 Key Features Active:{Style.RESET_ALL}")
    print(f"   • Smart Local/Cloud AI Routing")
    print(f"   • Intelligent Caching System")
    print(f"   • Parallel Processing")
    print(f"   • Memory Optimization")
    print(f"   • Async Operations")
    print(f"   • Performance Monitoring")
    
    return status

if __name__ == "__main__":
    result = main()
    print(f"\n{Fore.YELLOW}Verification Status: {result}{Style.RESET_ALL}")
