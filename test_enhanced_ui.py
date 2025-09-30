#!/usr/bin/env python3
"""
Test script for the enhanced UI system
Demonstrates the new clean, attractive interface
"""
import sys
import os
import time
from datetime import datetime

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from jarvis_enhanced_ui import enhanced_ui
    from jarvis_personal_bio import personal_bio_analyzer
    from jarvis_layer1_local import layer1_local_model
    from jarvis_layer2_stalling import layer2_stalling_model
    from jarvis_layer3_gemini import layer3_gemini_model
    from jarvis_layered_ai_router import layered_ai_router
    import config
    
    print("✅ All modules imported successfully")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def test_enhanced_ui():
    """Test the enhanced UI system"""
    print("🚀 Testing Enhanced UI System")
    print("=" * 50)
    
    try:
        # Test startup interface
        print("\n🔍 Testing Startup Interface...")
        enhanced_ui.display_startup_interface()
        time.sleep(2)
        
        # Test user query display
        print("\n🔍 Testing User Query Display...")
        enhanced_ui.display_user_query("What time is it?", "voice")
        time.sleep(1)
        
        # Test processing status
        print("\n🔍 Testing Processing Status...")
        enhanced_ui.display_processing_status(
            "Analyzing time request", 
            "layer1", 
            "Routing to local model for instant response"
        )
        time.sleep(1)
        
        # Test Jarvis response
        print("\n🔍 Testing Jarvis Response...")
        enhanced_ui.display_jarvis_response(
            "The current time is 11:30 PM, Mr. Bharadwaj Sir.",
            "completed",
            "Speaking response..."
        )
        time.sleep(1)
        
        # Test complex query
        print("\n🔍 Testing Complex Query...")
        enhanced_ui.display_user_query("Explain quantum computing", "text")
        time.sleep(1)
        
        enhanced_ui.display_processing_status(
            "Processing complex query", 
            "layer3", 
            "Using Gemini AI with personal context"
        )
        time.sleep(2)
        
        enhanced_ui.display_jarvis_response(
            "Mr. Bharadwaj Sir, quantum computing represents a revolutionary approach to computation that leverages quantum mechanical phenomena...",
            "completed",
            "Speaking detailed response..."
        )
        time.sleep(1)
        
        # Test error display
        print("\n🔍 Testing Error Display...")
        enhanced_ui.display_error("I encountered an issue processing that request, Mr. Bharadwaj Sir.")
        time.sleep(1)
        
        # Test mode change
        print("\n🔍 Testing Mode Change...")
        enhanced_ui.display_mode_change("Voice")
        time.sleep(1)
        
        # Test help display
        print("\n🔍 Testing Help Display...")
        enhanced_ui.display_help()
        time.sleep(1)
        
        # Test system info
        print("\n🔍 Testing System Info...")
        system_info = {
            "AI Brain": {"status": "Operational", "details": "All layers active"},
            "Voice System": {"status": "Ready", "details": "British accent enabled"},
            "Memory": {"status": "Active", "details": "Learning from interactions"},
            "Performance": {"status": "Optimized", "details": "Fast response times"}
        }
        enhanced_ui.display_system_info(system_info)
        time.sleep(1)
        
        # Test conversation summary
        print("\n🔍 Testing Conversation Summary...")
        enhanced_ui.display_conversation_summary()
        time.sleep(1)
        
        # Test shutdown
        print("\n🔍 Testing Shutdown...")
        enhanced_ui.display_shutdown()
        
        print("\n✅ Enhanced UI system working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Enhanced UI error: {e}")
        return False

def demo_conversation_flow():
    """Demonstrate a complete conversation flow"""
    print("\n🎭 Demonstrating Complete Conversation Flow")
    print("=" * 50)
    
    # Simulate a conversation
    conversations = [
        ("What time is it?", "voice"),
        ("Open Safari browser", "voice"), 
        ("Tell me about artificial intelligence", "text"),
        ("Who am I?", "voice"),
        ("Help", "text")
    ]
    
    responses = [
        "The current time is 11:35 PM, Mr. Bharadwaj Sir.",
        "I've opened Safari for you, Mr. Bharadwaj Sir.",
        "Mr. Bharadwaj Sir, artificial intelligence is a fascinating field that combines computer science, mathematics, and cognitive science...",
        "Based on your personal information, Mr. Bharadwaj Sir: You are Rishabh Bhardwaj R, a motivated tech-savvy individual...",
        "I'm at your service, Mr. Bharadwaj Sir. Here's what I can assist you with..."
    ]
    
    for i, (query, input_type) in enumerate(conversations):
        print(f"\n--- Conversation {i+1} ---")
        
        # Display user query
        enhanced_ui.display_user_query(query, input_type)
        time.sleep(0.5)
        
        # Display processing
        enhanced_ui.display_processing_status(
            f"Processing {input_type} request", 
            "router", 
            "Analyzing and routing to appropriate AI layer"
        )
        time.sleep(0.5)
        
        # Display response
        enhanced_ui.display_jarvis_response(
            responses[i],
            "completed",
            "Speaking response..."
        )
        time.sleep(1)
    
    print("\n✅ Conversation flow demonstration complete")

def main():
    """Main test function"""
    print("🚀 Enhanced UI System Test")
    print("=" * 50)
    
    # Test enhanced UI
    ui_success = test_enhanced_ui()
    
    if ui_success:
        # Demo conversation flow
        demo_conversation_flow()
        
        print("\n🎉 Enhanced UI system is working perfectly!")
        print("🎯 The interface now provides:")
        print("  • Clean conversation boxes")
        print("  • Clear user query display")
        print("  • Processing status indicators")
        print("  • Attractive Jarvis responses")
        print("  • Action feedback")
        print("  • Error handling")
        print("  • Mode change notifications")
        print("  • Help and system information")
        
        print("\n💡 To use the enhanced UI:")
        print("  python jarvis.py")
        print("  # The interface will automatically use the enhanced UI")
    else:
        print("\n❌ Enhanced UI system has issues")
        sys.exit(1)

if __name__ == "__main__":
    main()
