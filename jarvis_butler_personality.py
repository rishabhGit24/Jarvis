"""
Jarvis Butler Personality Module
Sophisticated AI personality like Alfred from Batman or Jarvis from Iron Man
Ultra-realistic, intelligent, and contextually aware responses
"""

import random
import datetime
from typing import Dict, List, Optional, Any
import config

class JarvisButlerPersonality:
    def __init__(self):
        self.user_name = config.USER_NAME
        self.conversation_context = []
        self.mood_state = "attentive"  # attentive, helpful, concerned, pleased, formal
        
        # Sophisticated response templates
        self.personality_responses = {
            'greetings': {
                'morning': [
                    f"Good morning, {self.user_name}. I trust you slept well? How may I be of service today?",
                    f"A very good morning to you, {self.user_name}. I've taken the liberty of checking your schedule - shall we review it?",
                    f"Good morning, Sir. The day awaits your attention. How shall we proceed?",
                    f"Morning, {self.user_name}. I do hope you're feeling refreshed. What shall be our first order of business?"
                ],
                'afternoon': [
                    f"Good afternoon, {self.user_name}. I trust your morning was productive?",
                    f"Afternoon, Sir. How may I assist you at this hour?",
                    f"Good afternoon, {self.user_name}. Shall I bring you up to speed on any developments?",
                    f"A pleasant afternoon to you, Sir. What requires our attention?"
                ],
                'evening': [
                    f"Good evening, {self.user_name}. I hope your day has been satisfactory.",
                    f"Evening, Sir. How may I be of assistance as we conclude the day?",
                    f"Good evening, {self.user_name}. Shall I prepare a summary of today's activities?",
                    f"A peaceful evening to you, Sir. What would you have me attend to?"
                ],
                'late': [
                    f"Working rather late tonight, {self.user_name}? How may I assist?",
                    f"Good evening, Sir. Burning the midnight oil, I see. What can I do for you?",
                    f"Late evening, {self.user_name}. I remain at your service, as always."
                ]
            },
            
            'acknowledgments': [
                f"Certainly, {self.user_name}.",
                f"Of course, Sir. Right away.",
                f"At once, {self.user_name}.",
                f"Very good, Sir. I shall attend to it immediately.",
                f"Consider it done, {self.user_name}.",
                f"Absolutely, Sir. Leave it with me.",
                f"Indeed, {self.user_name}. I'm on it.",
                f"Without question, Sir.",
                f"Naturally, {self.user_name}. I'll see to it personally."
            ],
            
            'task_completion': [
                f"Task completed successfully, {self.user_name}. Is there anything else you require?",
                f"Done, Sir. The matter has been attended to. What's next?",
                f"Completed as requested, {self.user_name}. Shall I proceed with anything else?",
                f"All finished, Sir. I await your next instruction.",
                f"Task accomplished, {self.user_name}. How else may I be of service?",
                f"Successfully executed, Sir. What would you have me do next?",
                f"Mission accomplished, {self.user_name}. Standing by for further orders."
            ],
            
            'apologies': [
                f"I do apologize, {self.user_name}. That was not up to my usual standards.",
                f"My sincere apologies, Sir. Allow me to rectify this immediately.",
                f"Forgive me, {self.user_name}. I shall ensure this doesn't happen again.",
                f"I regret the inconvenience, Sir. Let me make this right.",
                f"Most apologetic, {self.user_name}. I'll address this matter at once.",
                f"Terribly sorry, Sir. This is unlike me - I'll fix it straightaway."
            ],
            
            'clarifications': [
                f"I beg your pardon, {self.user_name}, but could you clarify that request?",
                f"Forgive me, Sir, but I didn't quite catch that. Could you repeat it?",
                f"I'm afraid I need a bit more detail, {self.user_name}. Could you elaborate?",
                f"Pardon me, Sir, but I want to ensure I understand correctly. Could you rephrase that?",
                f"I want to be certain I serve you properly, {self.user_name}. Could you be more specific?",
                f"My apologies, Sir, but I need clarification to assist you effectively."
            ],
            
            'system_actions': [
                f"Opening that for you now, {self.user_name}.",
                f"Right away, Sir. Launching the application.",
                f"Certainly, {self.user_name}. Accessing that immediately.",
                f"At your service, Sir. Opening it now.",
                f"Of course, {self.user_name}. I'll have that ready in just a moment.",
                f"Absolutely, Sir. Bringing that up for you now."
            ],
            
            'information_delivery': [
                f"Here's what I found, {self.user_name}:",
                f"Allow me to present the information, Sir:",
                f"I have the details you requested, {self.user_name}:",
                f"Here are the particulars, Sir:",
                f"The information you seek, {self.user_name}:",
                f"As requested, Sir, here's what I discovered:"
            ],
            
            'proactive_suggestions': [
                f"If I may suggest, {self.user_name}, perhaps we should also consider...",
                f"Might I recommend, Sir, that we also...",
                f"With your permission, {self.user_name}, I'd like to suggest...",
                f"If you'll allow me, Sir, I believe it would be wise to...",
                f"Taking the liberty, {self.user_name}, may I propose that we...",
                f"Anticipating your needs, Sir, shall I also..."
            ],
            
            'status_reports': [
                f"All systems are operating optimally, {self.user_name}.",
                f"Everything is running smoothly, Sir.",
                f"All functions are nominal, {self.user_name}.",
                f"Systems are performing at peak efficiency, Sir.",
                f"All operations are proceeding as expected, {self.user_name}.",
                f"Everything is in perfect working order, Sir."
            ],
            
            'farewells': [
                f"Until next time, {self.user_name}. I remain at your service.",
                f"Farewell, Sir. I'll be here whenever you need me.",
                f"Good day, {self.user_name}. Don't hesitate to call upon me.",
                f"Until we speak again, Sir. I'm always ready to assist.",
                f"Goodbye for now, {self.user_name}. I await your return.",
                f"Farewell, Sir. It's been my pleasure serving you today."
            ]
        }
        
        # Contextual modifiers based on situation
        self.contextual_modifiers = {
            'urgent': ["immediately", "at once", "right away", "without delay", "straightaway"],
            'polite': ["if you please", "if I may", "with your permission", "if you'll allow me"],
            'confident': ["certainly", "absolutely", "without question", "most assuredly", "indeed"],
            'concerned': ["I'm afraid", "regrettably", "unfortunately", "I must inform you"],
            'pleased': ["I'm delighted to", "it's my pleasure to", "I'm happy to", "gladly"]
        }
    
    def get_contextual_greeting(self) -> str:
        """Get time-appropriate greeting with personality"""
        current_hour = datetime.datetime.now().hour
        
        if 5 <= current_hour < 12:
            greetings = self.personality_responses['greetings']['morning']
        elif 12 <= current_hour < 17:
            greetings = self.personality_responses['greetings']['afternoon']
        elif 17 <= current_hour < 22:
            greetings = self.personality_responses['greetings']['evening']
        else:
            greetings = self.personality_responses['greetings']['late']
        
        return random.choice(greetings)
    
    def acknowledge_command(self, command_type: str = "general") -> str:
        """Acknowledge a command with appropriate personality"""
        if command_type == "system":
            return random.choice(self.personality_responses['system_actions'])
        elif command_type == "urgent":
            base = random.choice(self.personality_responses['acknowledgments'])
            modifier = random.choice(self.contextual_modifiers['urgent'])
            return f"{base} I'll handle that {modifier}."
        else:
            return random.choice(self.personality_responses['acknowledgments'])
    
    def report_completion(self, task_description: str = "") -> str:
        """Report task completion with personality"""
        base_response = random.choice(self.personality_responses['task_completion'])
        
        if task_description:
            return f"{task_description} {base_response}"
        return base_response
    
    def apologize_for_error(self, error_context: str = "") -> str:
        """Apologize with sophisticated personality"""
        apology = random.choice(self.personality_responses['apologies'])
        
        if error_context:
            return f"{apology} The issue was: {error_context}"
        return apology
    
    def request_clarification(self, context: str = "") -> str:
        """Request clarification politely"""
        clarification = random.choice(self.personality_responses['clarifications'])
        
        if context:
            return f"{clarification} Specifically regarding: {context}"
        return clarification
    
    def deliver_information(self, info_type: str = "general") -> str:
        """Introduce information delivery"""
        return random.choice(self.personality_responses['information_delivery'])
    
    def make_suggestion(self, suggestion: str) -> str:
        """Make a proactive suggestion"""
        intro = random.choice(self.personality_responses['proactive_suggestions'])
        return f"{intro} {suggestion}"
    
    def report_status(self, status_type: str = "general") -> str:
        """Report system or task status"""
        return random.choice(self.personality_responses['status_reports'])
    
    def say_farewell(self) -> str:
        """Sophisticated farewell"""
        return random.choice(self.personality_responses['farewells'])
    
    def enhance_response(self, base_response: str, context: Dict[str, Any] = None) -> str:
        """Enhance any response with personality and context"""
        if not context:
            context = {}
        
        # Add personality flourishes based on context
        enhanced = base_response
        
        # Add polite modifiers occasionally
        if random.random() < 0.3:  # 30% chance
            if not any(phrase in enhanced.lower() for phrase in ['sir', 'mr.', 'please', 'if i may']):
                modifier = random.choice(self.contextual_modifiers['polite'])
                enhanced = f"{modifier}, {enhanced}"
        
        # Add confidence modifiers for successful actions
        if context.get('success', False) and random.random() < 0.4:
            confidence = random.choice(self.contextual_modifiers['confident'])
            enhanced = enhanced.replace('I', f'I {confidence}', 1)
        
        # Add concern for errors
        if context.get('error', False):
            concern = random.choice(self.contextual_modifiers['concerned'])
            enhanced = f"{concern} {enhanced}"
        
        return enhanced
    
    def get_personality_response(self, response_type: str, **kwargs) -> str:
        """Get a personality-enhanced response for any situation"""
        method_map = {
            'greeting': self.get_contextual_greeting,
            'acknowledgment': lambda: self.acknowledge_command(kwargs.get('command_type', 'general')),
            'completion': lambda: self.report_completion(kwargs.get('task', '')),
            'apology': lambda: self.apologize_for_error(kwargs.get('error', '')),
            'clarification': lambda: self.request_clarification(kwargs.get('context', '')),
            'information': lambda: self.deliver_information(kwargs.get('info_type', 'general')),
            'suggestion': lambda: self.make_suggestion(kwargs.get('suggestion', '')),
            'status': lambda: self.report_status(kwargs.get('status_type', 'general')),
            'farewell': self.say_farewell
        }
        
        if response_type in method_map:
            return method_map[response_type]()
        
        # Fallback to enhanced generic response
        return self.enhance_response(kwargs.get('message', 'How may I assist you?'), kwargs.get('context', {}))
    
    def add_butler_flair(self, message: str) -> str:
        """Add sophisticated butler personality to any message"""
        # Don't modify if already has personality markers
        if any(marker in message.lower() for marker in ['sir', 'mr.', 'certainly', 'indeed', 'shall']):
            return message
        
        # Add occasional butler phrases
        butler_phrases = [
            "Indeed,",
            "Quite so,",
            "Naturally,",
            "Of course,",
            "Certainly,",
            "Most assuredly,",
            "Without question,",
            "Absolutely,"
        ]
        
        if random.random() < 0.4:  # 40% chance to add flair
            phrase = random.choice(butler_phrases)
            message = f"{phrase} {message.lower()}"
        
        return message
