"""
Layered AI Router for Jarvis
Intelligently routes requests between Layer 1 (Local), Layer 2 (Stalling), and Layer 3 (Gemini)
"""
import time
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
import config
from jarvis_layer1_local import layer1_local_model
from jarvis_layer2_stalling import layer2_stalling_model
from jarvis_layer3_gemini import layer3_gemini_model
from jarvis_enhanced_ui import enhanced_ui

class LayeredAIRouter:
    """Intelligent router for the three-layer AI system"""
    
    def __init__(self):
        self.layer1 = layer1_local_model
        self.layer2 = layer2_stalling_model
        self.layer3 = layer3_gemini_model
        
        # Routing configuration
        self.routing_config = {
            'layer1_priority': ['greeting', 'time', 'date', 'who_am_i', 'open_browser', 'system_status', 'simple_math'],
            'layer2_priority': ['complex_analysis', 'detailed_explanation', 'research', 'creative_writing'],
            'layer3_priority': ['conversation', 'personal_advice', 'complex_queries', 'knowledge_questions']
        }
        
        # Performance tracking
        self.stats = {
            'total_requests': 0,
            'layer1_requests': 0,
            'layer2_requests': 0,
            'layer3_requests': 0,
            'routing_decisions': {},
            'average_response_time': 0,
            'response_times': [],
            'fallback_usage': 0
        }
        
        # Request complexity indicators
        self.complexity_indicators = {
            'simple': ['time', 'date', 'hello', 'hi', 'status', 'who am i', 'open browser', 'what day', 'what time', 'today', 'what is my name', 'my name', 'who am i', 'what month', 'what year', 'month is', 'year is'],
            'medium': ['weather', 'file search', 'system info', 'calculate'],
            'complex': ['explain', 'analyze', 'compare', 'describe', 'tell me about', 'how does', 'why is', 'what is']
        }
    
    def route_request(self, user_input: str, callback: Optional[Callable] = None) -> str:
        """Route user request to appropriate layer"""
        start_time = time.time()
        self.stats['total_requests'] += 1
        
        # Determine request complexity
        complexity = self._determine_complexity(user_input)
        
        print(f"[LAYERED AI] Query: '{user_input}' - Complexity: {complexity}")
        
        # Route based on complexity and layer availability
        if complexity == 'simple' and self.layer1.is_available():
            print(f"[LAYERED AI] → Routing to Layer 1 (Local Model)")
            enhanced_ui.start_processing_loader("layer1", user_input)
            return self._route_to_layer1(user_input, start_time)
        elif complexity == 'medium':
            # Skip Layer 2 stalling - route directly to Layer 3 for medium complexity
            if self.layer3.is_available() and config.LAYER3_ENABLED:
                print(f"[LAYERED AI] → Routing to Layer 3 (Gemini Model) - Layer 2 disabled")
                enhanced_ui.start_processing_loader("layer3", user_input)
                return self._route_to_layer3(user_input, start_time, callback)
            elif self.layer1.is_available():
                print(f"[LAYERED AI] → Fallback to Layer 1")
                enhanced_ui.start_processing_loader("layer1", user_input)
                return self._route_to_layer1(user_input, start_time)
        elif complexity == 'complex' and self.layer3.is_available():
            print(f"[LAYERED AI] → Routing to Layer 3 (Gemini Model)")
            enhanced_ui.start_processing_loader("layer3", user_input)
            return self._route_to_layer3(user_input, start_time, callback)
        
        # Fallback routing
        print(f"[LAYERED AI] → Using fallback routing")
        enhanced_ui.start_processing_loader("fallback", user_input)
        return self._fallback_routing(user_input, start_time, callback)
    
    def _determine_complexity(self, user_input: str) -> str:
        """Determine the complexity of the user request"""
        user_input_lower = user_input.lower()
        
        # Check for simple indicators
        for indicator in self.complexity_indicators['simple']:
            if indicator in user_input_lower:
                return 'simple'
        
        # Check for complex indicators
        for indicator in self.complexity_indicators['complex']:
            if indicator in user_input_lower:
                return 'complex'
        
        # Check for medium indicators
        for indicator in self.complexity_indicators['medium']:
            if indicator in user_input_lower:
                return 'medium'
        
        # Default to medium complexity
        return 'medium'
    
    def _route_to_layer1(self, user_input: str, start_time: float) -> str:
        """Route request to Layer 1 (Local Model)"""
        try:
            print(f"[LAYER 1] Processing: '{user_input}'")
            enhanced_ui.show_processing_status_update("Local model analyzing...", "LAYER 1")
            response = self.layer1.process(user_input)
            if response:
                self.stats['layer1_requests'] += 1
                self._update_routing_stats('layer1', time.time() - start_time)
                print(f"[LAYER 1] ✓ Response generated successfully")
                enhanced_ui.stop_processing_loader()
                return response
            else:
                print(f"[LAYER 1] ✗ Could not handle request, using fallback")
                enhanced_ui.show_layer_transition("Layer 1", "Fallback", "No response generated")
                # Layer 1 couldn't handle it, try fallback
                return self._fallback_routing(user_input, start_time)
        except Exception as e:
            print(f"[LAYER 1] ✗ Error: {e}")
            enhanced_ui.show_layer_transition("Layer 1", "Fallback", f"Error: {e}")
            return self._fallback_routing(user_input, start_time)
    
    def _route_to_layer2(self, user_input: str, start_time: float, callback: Optional[Callable] = None) -> str:
        """Route request to Layer 2 (Stalling Model)"""
        try:
            print(f"[LAYER 2] Starting stalling process for: '{user_input}'")
            enhanced_ui.show_processing_status_update("Engaging stalling process...", "LAYER 2")
            
            # For simple queries like "what is my name", route directly to Layer 3
            if any(phrase in user_input.lower() for phrase in ['what is my name', 'my name', 'who am i']):
                print(f"[LAYER 2] → Simple query detected, routing directly to Layer 3")
                enhanced_ui.show_layer_transition("Layer 2", "Layer 3", "Simple query detected")
                return self._route_to_layer3(user_input, start_time, callback)
            
            # Start stalling process
            stalling_response = self.layer2.start_stalling(
                user_input, 
                lambda x: self._get_layer3_response(x),
                config.LAYER2_MAX_STALL_TIME
            )
            
            self.stats['layer2_requests'] += 1
            self._update_routing_stats('layer2', time.time() - start_time)
            print(f"[LAYER 2] ✓ Stalling response generated")
            
            # Layer 2 returns stalling response immediately, so stop the loader
            enhanced_ui.show_processing_status_update("Stalling response generated", "LAYER 2")
            enhanced_ui.stop_processing_loader()
            
            return stalling_response
        except Exception as e:
            print(f"[LAYER 2] ✗ Error: {e}")
            enhanced_ui.show_layer_transition("Layer 2", "Fallback", f"Error: {e}")
            return self._fallback_routing(user_input, start_time, callback)
    
    def _route_to_layer3(self, user_input: str, start_time: float, callback: Optional[Callable] = None) -> str:
        """Route request to Layer 3 (Gemini Model)"""
        try:
            print(f"[LAYER 3] Processing: '{user_input}'")
            enhanced_ui.show_processing_status_update("Gemini AI processing...", "LAYER 3")
            
            if callback:
                # Asynchronous processing
                print(f"[LAYER 3] → Using async processing")
                enhanced_ui.show_processing_status_update("Starting async processing...", "LAYER 3")
                self.layer3.process_async(user_input, callback)
                return "Processing your request, Mr. Bharadwaj Sir..."
            else:
                # Synchronous processing
                print(f"[LAYER 3] → Using sync processing")
                enhanced_ui.show_processing_status_update("Gemini AI analyzing...", "LAYER 3")
                response = self.layer3.process(user_input)
                self.stats['layer3_requests'] += 1
                self._update_routing_stats('layer3', time.time() - start_time)
                print(f"[LAYER 3] ✓ Response generated successfully")
                enhanced_ui.stop_processing_loader()
                return response
        except Exception as e:
            print(f"[LAYER 3] ✗ Error: {e}")
            enhanced_ui.show_layer_transition("Layer 3", "Fallback", f"Error: {e}")
            return self._fallback_routing(user_input, start_time, callback)
    
    def _get_layer3_response(self, user_input: str) -> str:
        """Get response from Layer 3 for Layer 2 stalling"""
        try:
            if self.layer3.is_available():
                return self.layer3.process(user_input)
            else:
                return "I apologize, Mr. Bharadwaj Sir, but I'm experiencing some technical difficulties."
        except Exception as e:
            return f"I encountered an issue, Mr. Bharadwaj Sir: {str(e)}"
    
    def _fallback_routing(self, user_input: str, start_time: float, callback: Optional[Callable] = None) -> str:
        """Fallback routing when primary layer fails"""
        self.stats['fallback_usage'] += 1
        print(f"[FALLBACK] Attempting fallback routing for: '{user_input}'")
        enhanced_ui.show_processing_status_update("Fallback routing activated...", "FALLBACK")
        
        # Try layers in order of preference
        if self.layer1.is_available():
            try:
                print(f"[FALLBACK] → Trying Layer 1")
                enhanced_ui.show_processing_status_update("Trying Layer 1 fallback...", "FALLBACK")
                response = self.layer1.process(user_input)
                if response:
                    self.stats['layer1_requests'] += 1
                    self._update_routing_stats('layer1_fallback', time.time() - start_time)
                    print(f"[FALLBACK] ✓ Layer 1 succeeded")
                    enhanced_ui.stop_processing_loader()
                    return response
            except Exception as e:
                print(f"[FALLBACK] ✗ Layer 1 failed: {e}")
                enhanced_ui.show_processing_status_update(f"Layer 1 failed: {e}", "FALLBACK")
        
        if self.layer3.is_available():
            try:
                print(f"[FALLBACK] → Trying Layer 3")
                enhanced_ui.show_processing_status_update("Trying Layer 3 fallback...", "FALLBACK")
                if callback:
                    self.layer3.process_async(user_input, callback)
                    print(f"[FALLBACK] ✓ Layer 3 async started")
                    return "Processing your request, Mr. Bharadwaj Sir..."
                else:
                    response = self.layer3.process(user_input)
                    self.stats['layer3_requests'] += 1
                    self._update_routing_stats('layer3_fallback', time.time() - start_time)
                    print(f"[FALLBACK] ✓ Layer 3 succeeded")
                    enhanced_ui.stop_processing_loader()
                    return response
            except Exception as e:
                print(f"[FALLBACK] ✗ Layer 3 failed: {e}")
                enhanced_ui.show_processing_status_update(f"Layer 3 failed: {e}", "FALLBACK")
        
        # Ultimate fallback
        print(f"[FALLBACK] ✗ All layers failed, using ultimate fallback")
        enhanced_ui.stop_processing_loader()
        return "I apologize, Mr. Bharadwaj Sir, but I'm experiencing technical difficulties. Please try again later."
    
    def _update_routing_stats(self, layer: str, response_time: float):
        """Update routing statistics"""
        self.stats['routing_decisions'][layer] = self.stats['routing_decisions'].get(layer, 0) + 1
        self.stats['response_times'].append(response_time)
        self.stats['average_response_time'] = sum(self.stats['response_times']) / len(self.stats['response_times'])
    
    def get_smart_suggestion(self, user_input: str) -> str:
        """Get smart suggestion based on user input and personal context"""
        try:
            if self.layer3.is_available():
                return self.layer3.get_personalized_suggestion(user_input)
            else:
                return "Is there anything else I can help you with, Mr. Bharadwaj Sir?"
        except Exception:
            return "How can I assist you further, Mr. Bharadwaj Sir?"
    
    def update_personal_context(self):
        """Update personal context across all layers"""
        try:
            if self.layer3.is_available():
                self.layer3.update_personal_context()
            print("Personal context updated across all layers, Mr. Bharadwaj Sir.")
        except Exception as e:
            print(f"Error updating personal context: {e}")
    
    def get_layer_status(self) -> Dict[str, Any]:
        """Get status of all layers"""
        return {
            'layer1': {
                'available': self.layer1.is_available(),
                'stats': self.layer1.get_stats() if hasattr(self.layer1, 'get_stats') else {}
            },
            'layer2': {
                'available': self.layer2.is_available(),
                'stats': self.layer2.get_stats() if hasattr(self.layer2, 'get_stats') else {}
            },
            'layer3': {
                'available': self.layer3.is_available() if self.layer3 else False,
                'stats': self.layer3.get_stats() if self.layer3 and hasattr(self.layer3, 'get_stats') else {}
            }
        }
    
    def get_routing_stats(self) -> Dict[str, Any]:
        """Get comprehensive routing statistics"""
        return {
            'total_requests': self.stats['total_requests'],
            'layer_distribution': {
                'layer1': self.stats['layer1_requests'],
                'layer2': self.stats['layer2_requests'],
                'layer3': self.stats['layer3_requests']
            },
            'routing_decisions': self.stats['routing_decisions'],
            'average_response_time': self.stats['average_response_time'],
            'fallback_usage': self.stats['fallback_usage'],
            'success_rate': (self.stats['total_requests'] - self.stats['fallback_usage']) / max(self.stats['total_requests'], 1) * 100
        }
    
    def optimize_routing(self):
        """Optimize routing based on performance data"""
        try:
            # Analyze routing patterns
            total_requests = self.stats['total_requests']
            if total_requests > 10:  # Only optimize after sufficient data
                layer1_ratio = self.stats['layer1_requests'] / total_requests
                layer2_ratio = self.stats['layer2_requests'] / total_requests
                layer3_ratio = self.stats['layer3_requests'] / total_requests
                
                # Adjust routing thresholds based on performance
                if layer1_ratio > 0.7:
                    print("Layer 1 is handling most requests efficiently")
                if layer2_ratio > 0.5:
                    print("Layer 2 stalling is being used frequently")
                if layer3_ratio > 0.6:
                    print("Layer 3 is handling complex requests well")
                
                # Log optimization results
                print(f"Routing optimization complete. Layer distribution: L1={layer1_ratio:.1%}, L2={layer2_ratio:.1%}, L3={layer3_ratio:.1%}")
        except Exception as e:
            print(f"Error optimizing routing: {e}")
    
    def reset_stats(self):
        """Reset routing statistics"""
        self.stats = {
            'total_requests': 0,
            'layer1_requests': 0,
            'layer2_requests': 0,
            'layer3_requests': 0,
            'routing_decisions': {},
            'average_response_time': 0,
            'response_times': [],
            'fallback_usage': 0
        }
        print("Routing statistics reset, Mr. Bharadwaj Sir.")
    
    def is_available(self) -> bool:
        """Check if any layer is available"""
        return (self.layer1.is_available() or 
                self.layer2.is_available() or 
                (self.layer3 and self.layer3.is_available()))

# Initialize the layered AI router
layered_ai_router = LayeredAIRouter()
