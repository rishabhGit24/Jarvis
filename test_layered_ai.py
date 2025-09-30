#!/usr/bin/env python3
"""
Test script for the layered AI system
Tests all three layers and the routing system
"""
import sys
import os
import time
from datetime import datetime

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from jarvis_personal_bio import personal_bio_analyzer
    from jarvis_layer1_local import layer1_local_model
    from jarvis_layer2_stalling import layer2_stalling_model
    from jarvis_layer3_gemini import layer3_gemini_model
    from jarvis_layered_ai_router import layered_ai_router
    from jarvis_brain import JarvisBrain
    import config
    
    print("✅ All modules imported successfully")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def test_personal_bio_analysis():
    """Test personal bio analysis"""
    print("\n🔍 Testing Personal Bio Analysis...")
    
    try:
        # Test bio analysis
        summary = personal_bio_analyzer.get_personal_summary()
        print(f"Personal Summary: {summary}")
        
        sentiment = personal_bio_analyzer.get_sentiment_summary()
        print(f"Sentiment Analysis: {sentiment}")
        
        # Test personality profile
        profile = personal_bio_analyzer.get_personality_profile()
        print(f"Personality Traits: {len(profile.get('personality_traits', {}))} traits identified")
        
        print("✅ Personal bio analysis working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Personal bio analysis error: {e}")
        return False

def test_layer1_local():
    """Test Layer 1 (Local Model)"""
    print("\n🔍 Testing Layer 1 (Local Model)...")
    
    try:
        # Test simple queries
        test_queries = [
            "Hello",
            "What time is it?",
            "What's the date?",
            "Who am I?",
            "Open browser",
            "System status"
        ]
        
        for query in test_queries:
            if layer1_local_model.can_handle(query):
                response = layer1_local_model.process(query)
                print(f"Query: '{query}' -> Response: '{response[:50]}...'")
            else:
                print(f"Query: '{query}' -> Not handled by Layer 1")
        
        # Test stats
        stats = layer1_local_model.get_stats()
        print(f"Layer 1 Stats: {stats}")
        
        print("✅ Layer 1 (Local Model) working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Layer 1 error: {e}")
        return False

def test_layer2_stalling():
    """Test Layer 2 (Stalling Model)"""
    print("\n🔍 Testing Layer 2 (Stalling Model)...")
    
    try:
        # Test stalling functionality
        def test_callback(user_input):
            return f"Processed: {user_input}"
        
        response = layer2_stalling_model.start_stalling("Test query", test_callback, 3.0)
        print(f"Stalling Response: {response}")
        
        # Wait a bit to see stalling in action
        time.sleep(2)
        
        # Test engagement
        follow_up = layer2_stalling_model.get_engaging_follow_up()
        if follow_up:
            print(f"Follow-up: {follow_up}")
        
        # Test stats
        stats = layer2_stalling_model.get_stats()
        print(f"Layer 2 Stats: {stats}")
        
        print("✅ Layer 2 (Stalling Model) working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Layer 2 error: {e}")
        return False

def test_layer3_gemini():
    """Test Layer 3 (Gemini Model)"""
    print("\n🔍 Testing Layer 3 (Gemini Model)...")
    
    try:
        if not layer3_gemini_model:
            print("⚠️ Layer 3 (Gemini Model) not available - API key may be missing")
            return False
        
        # Test connection
        if not layer3_gemini_model.test_connection():
            print("⚠️ Layer 3 (Gemini Model) connection test failed")
            return False
        
        # Test simple query
        response = layer3_gemini_model.process("Hello, how are you?")
        print(f"Gemini Response: {response[:100]}...")
        
        # Test personalized suggestion
        suggestion = layer3_gemini_model.get_personalized_suggestion()
        print(f"Personalized Suggestion: {suggestion}")
        
        # Test stats
        stats = layer3_gemini_model.get_stats()
        print(f"Layer 3 Stats: {stats}")
        
        print("✅ Layer 3 (Gemini Model) working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Layer 3 error: {e}")
        return False

def test_layered_router():
    """Test Layered AI Router"""
    print("\n🔍 Testing Layered AI Router...")
    
    try:
        # Test routing decisions
        test_queries = [
            "Hello",  # Should go to Layer 1
            "What time is it?",  # Should go to Layer 1
            "Explain quantum computing",  # Should go to Layer 3
            "Tell me about artificial intelligence"  # Should go to Layer 3
        ]
        
        for query in test_queries:
            response = layered_ai_router.route_request(query)
            print(f"Query: '{query}' -> Response: '{response[:50]}...'")
        
        # Test layer status
        status = layered_ai_router.get_layer_status()
        print(f"Layer Status: {status}")
        
        # Test routing stats
        stats = layered_ai_router.get_routing_stats()
        print(f"Routing Stats: {stats}")
        
        print("✅ Layered AI Router working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Layered AI Router error: {e}")
        return False

def test_integrated_brain():
    """Test integrated Jarvis Brain"""
    print("\n🔍 Testing Integrated Jarvis Brain...")
    
    try:
        # Initialize brain
        brain = JarvisBrain()
        
        # Test queries
        test_queries = [
            "Hello",
            "What time is it?",
            "Who am I?",
            "Tell me about yourself",
            "What can you do?"
        ]
        
        for query in test_queries:
            response = brain.process_command(query)
            print(f"Query: '{query}' -> Response: '{response[:50]}...'")
        
        # Test performance stats
        stats = brain.get_performance_stats()
        print(f"Brain Stats: {stats}")
        
        print("✅ Integrated Jarvis Brain working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Integrated Jarvis Brain error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Layered AI System Tests")
    print("=" * 50)
    
    # Test results
    results = {}
    
    # Run tests
    results['personal_bio'] = test_personal_bio_analysis()
    results['layer1'] = test_layer1_local()
    results['layer2'] = test_layer2_stalling()
    results['layer3'] = test_layer3_gemini()
    results['router'] = test_layered_router()
    results['brain'] = test_integrated_brain()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.upper()}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The layered AI system is working correctly.")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
