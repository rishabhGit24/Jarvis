#!/usr/bin/env python3
"""
Fix syntax error in jarvis_nlp.py
"""

def fix_nlp_syntax():
    """Fix the syntax error in jarvis_nlp.py"""
    try:
        with open('jarvis_nlp.py', 'r') as f:
            content = f.read()
        
        # Fix the syntax error on line 44
        content = content.replace(
            "self._initialize_speed_cache()\\n                self.system_context = f\"\"\"",
            "self._initialize_speed_cache()\n        \n        # System context for Jarvis personality\n        self.system_context = f\"\"\""
        )
        
        # Write fixed content back
        with open('jarvis_nlp.py', 'w') as f:
            f.write(content)
        
        print("✅ Fixed syntax error in jarvis_nlp.py")
        
    except Exception as e:
        print(f"❌ Error fixing syntax: {e}")

if __name__ == "__main__":
    fix_nlp_syntax()
