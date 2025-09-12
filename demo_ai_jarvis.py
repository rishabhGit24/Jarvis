#!/usr/bin/env python3
"""
Demo script to showcase AI-enhanced Jarvis capabilities
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from jarvis_brain import JarvisBrain
from colorama import init, Fore, Style

init(autoreset=True)

def demo_ai_jarvis():
    print(f"{Fore.BLUE}🤖 AI-Enhanced JARVIS Demo{Style.RESET_ALL}")
    print("=" * 50)
    
    brain = JarvisBrain()
    
    # Demo commands showing AI understanding
    demo_commands = [
        "Hello Jarvis, how are you doing today?",
        "I need you to help me find a document called report.pdf",
        "Can you tell me what the weather is like outside?",
        "Please remember that I prefer working in the morning",
        "What do you know about machine learning?",
        "Show me my system performance",
        "I'm feeling a bit tired, what do you suggest?",
        "Find any Python files in my project",
        "Thank you for all your help today"
    ]
    
    print(f"{Fore.GREEN}Demonstrating natural language conversations:{Style.RESET_ALL}\\n")
    
    for i, command in enumerate(demo_commands, 1):
        print(f"{Fore.CYAN}[{i}] You:{Style.RESET_ALL} {command}")
        
        try:
            response = brain.process_command(command)
            print(f"{Fore.YELLOW}Jarvis:{Style.RESET_ALL} {response}\\n")
        except Exception as e:
            print(f"{Fore.RED}Error:{Style.RESET_ALL} {e}\\n")
    
    print("=" * 50)
    print(f"{Fore.GREEN}🎉 Demo Complete! Your AI-enhanced Jarvis is ready to serve!{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Start with: python3 jarvis.py{Style.RESET_ALL}")

if __name__ == "__main__":
    demo_ai_jarvis()
