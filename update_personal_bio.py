#!/usr/bin/env python3
"""
Update Personal Bio Analysis
"""
import sys
import os
from datetime import datetime

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from jarvis_personal_bio import PersonalBioAnalyzer
    from jarvis_layer3_gemini import layer3_gemini_model
    from jarvis_layered_ai_router import layered_ai_router
    import config
    
    print("🔄 Updating Personal Bio Analysis...")
    print("=" * 50)
    
    # Create new analyzer with updated personal info
    new_analyzer = PersonalBioAnalyzer("personal_info.txt")
    
    # Get analysis results
    profile = new_analyzer.get_personality_profile()
    
    # Display key results
    print("📋 Updated Analysis Results:")
    print("-" * 30)
    
    # Basic info
    if 'basic_info' in profile:
        basic_info = profile['basic_info']
        print(f"👤 Name: {basic_info.get('name', 'Not found')}")
        print(f"📍 Location: {basic_info.get('location', 'Not found')}")
        print(f"🎂 Birth Date: {basic_info.get('birth_date', 'Not found')}")
    
    # Personality traits
    if 'personality_traits' in profile:
        traits = profile['personality_traits']
        print(f"\n🧠 Personality Traits ({len(traits)} found):")
        for trait, data in sorted(traits.items(), key=lambda x: x[1]['strength'], reverse=True):
            print(f"  • {trait.replace('_', ' ').title()}: {data['strength']} indicators")
    
    # Interests
    if 'basic_info' in profile and 'interests' in profile['basic_info']:
        interests = profile['basic_info']['interests']
        print(f"\n🎯 Interests ({len(interests)} found):")
        for interest, count in sorted(interests.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {interest.title()}: {count} mentions")
    
    # Role models
    if 'basic_info' in profile and 'role_models' in profile['basic_info']:
        role_models = profile['basic_info']['role_models']
        if role_models:
            print(f"\n🌟 Role Models ({len(role_models)} found):")
            for model in role_models:
                print(f"  • {model}")
    
    # Career info
    if 'basic_info' in profile and 'career' in profile['basic_info']:
        career = profile['basic_info']['career']
        if 'current_company' in career:
            print(f"\n💼 Current Company: {career['current_company']}")
        if 'job_offers' in career and career['job_offers']:
            print(f"📋 Job Offers: {', '.join(career['job_offers'])}")
    
    # Goals
    if 'basic_info' in profile and 'specific_goals' in profile['basic_info']:
        goals = profile['basic_info']['specific_goals']
        if goals:
            print(f"\n🎯 Goals ({len(goals)} found):")
            for goal in goals:
                print(f"  • {goal}")
    
    # Sentiment
    if 'sentiment_analysis' in profile:
        sentiment = profile['sentiment_analysis']
        print(f"\n😊 Sentiment Analysis:")
        print(f"  • Category: {sentiment['category'].title()}")
        print(f"  • Score: {sentiment['score']:.2f}")
    
    # Save analysis
    new_analyzer.save_analysis("personal_bio_analysis.json")
    
    # Update global analyzer
    import jarvis_personal_bio
    jarvis_personal_bio.personal_bio_analyzer = new_analyzer
    
    # Update AI models
    if layer3_gemini_model:
        layer3_gemini_model.update_personal_context()
        print("✅ Gemini model updated")
    
    layered_ai_router.update_personal_context()
    print("✅ AI router updated")
    
    print("\n🎉 Personal bio analysis updated successfully!")
    
    # Show summary
    summary = new_analyzer.get_personal_summary()
    print(f"📝 Personal Summary: {summary}")
    
except Exception as e:
    print(f"❌ Error: {e}")