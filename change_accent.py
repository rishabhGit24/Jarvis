#!/usr/bin/env python3
"""
JARVIS Accent Changer
Easily change the voice accent for your JARVIS assistant
"""

import os
import sys

def get_available_accents():
    """Get list of available accents"""
    return {
        '1': ('british', 'British English (Daniel, Oliver, Serena, Kate)'),
        '2': ('american', 'American English (Alex, Fred, Victoria, Allison, Tom, Bruce, Ralph)'),
        '3': ('australian', 'Australian English (Karen, Lee, Catherine)'),
        '4': ('indian', 'Indian English (Rishi, Veena, Lekha)'),
        '5': ('irish', 'Irish English (Moira, Fiona)'),
        '6': ('scottish', 'Scottish English (Fiona, Moira)'),
        '7': ('french', 'French English (Thomas, Aurelie)'),
        '8': ('german', 'German English (Anna, Yannick)'),
        '9': ('spanish', 'Spanish English (Monica, Jorge)'),
        '10': ('italian', 'Italian English (Luca, Alice)')
    }

def get_current_accent():
    """Get the current accent from config.py"""
    try:
        with open('config.py', 'r') as f:
            content = f.read()
            
        # Find the VOICE_ACCENT line
        for line in content.split('\n'):
            if line.strip().startswith('VOICE_ACCENT'):
                # Extract the accent value
                if '=' in line:
                    accent = line.split('=')[1].strip().strip("'\"")
                    return accent
        return 'british'  # default
    except Exception as e:
        print(f"Error reading config: {e}")
        return 'british'

def set_accent(new_accent):
    """Update the accent in config.py"""
    try:
        with open('config.py', 'r') as f:
            content = f.read()
        
        # Replace the VOICE_ACCENT line
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.strip().startswith('VOICE_ACCENT'):
                lines[i] = f"VOICE_ACCENT = '{new_accent}'  # Change this to your preferred accent"
                break
        
        # Write back to file
        with open('config.py', 'w') as f:
            f.write('\n'.join(lines))
        
        return True
    except Exception as e:
        print(f"Error updating config: {e}")
        return False

def main():
    print("🎭 JARVIS ACCENT CHANGER")
    print("=" * 50)
    
    # Show current accent
    current = get_current_accent()
    print(f"Current accent: {current.upper()}")
    print()
    
    # Show available options
    accents = get_available_accents()
    print("Available accents:")
    print("-" * 30)
    
    for key, (accent, description) in accents.items():
        marker = " ← CURRENT" if accent == current else ""
        print(f"{key}. {description}{marker}")
    
    print()
    print("0. Exit without changing")
    print()
    
    # Get user choice
    try:
        choice = input("Select accent (1-10, 0 to exit): ").strip()
        
        if choice == '0':
            print("No changes made. Goodbye!")
            return
        
        if choice not in accents:
            print("Invalid choice. Please run the script again.")
            return
        
        new_accent, description = accents[choice]
        
        # Confirm change
        print(f"\nChanging accent to: {description}")
        confirm = input("Confirm? (y/N): ").strip().lower()
        
        if confirm in ['y', 'yes']:
            if set_accent(new_accent):
                print(f"\n✅ SUCCESS! Accent changed to {new_accent.upper()}")
                print("\n🎯 Next steps:")
                print("1. Restart JARVIS to apply the new accent")
                print("2. Run: source jarvis_env/bin/activate && python3 jarvis.py")
                print("\nYour JARVIS will now speak with the new accent! 🎉")
            else:
                print("\n❌ Failed to update accent. Please check file permissions.")
        else:
            print("No changes made.")
    
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()

