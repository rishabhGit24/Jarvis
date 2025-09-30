"""
Personal Bio Analysis System for Jarvis
Analyzes personal information to understand user identity and preferences
"""
import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
import config

class PersonalBioAnalyzer:
    """Analyzes personal bio to extract key information about the user"""
    
    def __init__(self, bio_file_path: str = "personal_info.txt"):
        self.bio_file_path = bio_file_path
        self.bio_data = {}
        self.analysis_results = {}
        self.sentiment_analysis = {}
        self.personality_traits = {}
        self.load_bio_data()
        self.analyze_bio()
    
    def load_bio_data(self):
        """Load personal bio data from file"""
        try:
            with open(self.bio_file_path, 'r', encoding='utf-8') as file:
                self.bio_data['raw_text'] = file.read().strip()
                self.bio_data['word_count'] = len(self.bio_data['raw_text'].split())
                self.bio_data['character_count'] = len(self.bio_data['raw_text'])
        except FileNotFoundError:
            print(f"Warning: Personal bio file {self.bio_file_path} not found")
            self.bio_data['raw_text'] = ""
        except Exception as e:
            print(f"Error loading bio data: {e}")
            self.bio_data['raw_text'] = ""
    
    def analyze_bio(self):
        """Perform comprehensive analysis of the personal bio"""
        if not self.bio_data.get('raw_text'):
            return
        
        # Extract key personal information
        self._extract_personal_info()
        
        # Perform sentiment analysis
        self._perform_sentiment_analysis()
        
        # Extract personality traits
        self._extract_personality_traits()
        
        # Extract interests and motivations
        self._extract_interests_motivations()
        
        # Extract relationships and family
        self._extract_relationships()
        
        # Extract career and education
        self._extract_career_education()
        
        # Extract goals and aspirations
        self._extract_goals_aspirations()
    
    def _extract_personal_info(self):
        """Extract basic personal information"""
        text = self.bio_data['raw_text'].lower()
        
        # Name extraction
        name_patterns = [
            r'my name is ([a-zA-Z\s]+)',
            r'i am ([a-zA-Z\s]+)',
            r'name is ([a-zA-Z\s]+)'
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, text)
            if match:
                self.analysis_results['name'] = match.group(1).strip().title()
                break
        
        # Birth date extraction
        birth_patterns = [
            r'born on (\d{1,2}(?:st|nd|rd|th)?\s+\w+\s+\d{4})',
            r'birthday is (\d{1,2}(?:st|nd|rd|th)?\s+\w+\s+\d{4})',
            r'born (\d{1,2}(?:st|nd|rd|th)?\s+\w+\s+\d{4})'
        ]
        
        for pattern in birth_patterns:
            match = re.search(pattern, text)
            if match:
                self.analysis_results['birth_date'] = match.group(1).strip()
                break
        
        # Location extraction
        location_patterns = [
            r'born in ([a-zA-Z\s]+)',
            r'from ([a-zA-Z\s]+)',
            r'living in ([a-zA-Z\s]+)',
            r'based in ([a-zA-Z\s]+)'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text)
            if match:
                self.analysis_results['location'] = match.group(1).strip().title()
                break
    
    def _perform_sentiment_analysis(self):
        """Perform sentiment analysis on the bio text"""
        text = self.bio_data['raw_text'].lower()
        
        # Positive sentiment indicators
        positive_words = [
            'love', 'amazing', 'great', 'excellent', 'wonderful', 'fantastic',
            'brilliant', 'motivated', 'inspired', 'passionate', 'dedicated',
            'successful', 'achieved', 'accomplished', 'proud', 'happy',
            'excited', 'thrilled', 'grateful', 'blessed', 'fortunate'
        ]
        
        # Negative sentiment indicators
        negative_words = [
            'difficult', 'challenging', 'struggled', 'failed', 'disappointed',
            'sad', 'depressed', 'anxious', 'worried', 'stressed', 'frustrated',
            'angry', 'upset', 'hurt', 'broken', 'devastated', 'terrible',
            'awful', 'horrible', 'nightmare', 'crisis', 'problem'
        ]
        
        # Count sentiment words
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        
        # Calculate sentiment score
        total_sentiment_words = positive_count + negative_count
        if total_sentiment_words > 0:
            sentiment_score = (positive_count - negative_count) / total_sentiment_words
        else:
            sentiment_score = 0
        
        # Determine sentiment category
        if sentiment_score > 0.3:
            sentiment_category = "positive"
        elif sentiment_score < -0.3:
            sentiment_category = "negative"
        else:
            sentiment_category = "neutral"
        
        self.sentiment_analysis = {
            'score': sentiment_score,
            'category': sentiment_category,
            'positive_words_count': positive_count,
            'negative_words_count': negative_count,
            'total_sentiment_words': total_sentiment_words
        }
    
    def _extract_personality_traits(self):
        """Extract personality traits from the bio"""
        text = self.bio_data['raw_text'].lower()
        
        # Define personality trait patterns
        trait_patterns = {
            'motivated': ['motivated', 'driven', 'ambitious', 'determined', 'focused'],
            'intelligent': ['brilliant', 'smart', 'intelligent', 'quick', 'clever', 'genius'],
            'hardworking': ['hardworking', 'dedicated', 'committed', 'persistent', 'diligent'],
            'family_oriented': ['family', 'love my family', 'close to family', 'family first'],
            'tech_savvy': ['coding', 'programming', 'technology', 'software', 'tech', 'ai'],
            'goal_oriented': ['goals', 'aspirations', 'dreams', 'success', 'achieve'],
            'resilient': ['overcome', 'persevere', 'bounce back', 'recover', 'resilient'],
            'curious': ['learn', 'explore', 'discover', 'curious', 'interested', 'fascinated'],
            'empathetic': ['help', 'support', 'care', 'understand', 'compassionate'],
            'creative': ['create', 'build', 'design', 'innovate', 'creative', 'artistic']
        }
        
        traits = {}
        for trait, keywords in trait_patterns.items():
            count = sum(1 for keyword in keywords if keyword in text)
            if count > 0:
                traits[trait] = {
                    'strength': count,
                    'keywords_found': [kw for kw in keywords if kw in text]
                }
        
        self.personality_traits = traits
    
    def _extract_interests_motivations(self):
        """Extract interests and motivations"""
        text = self.bio_data['raw_text'].lower()
        
        interests = {
            'technology': ['coding', 'programming', 'software', 'ai', 'tech', 'computer'],
            'science': ['science', 'physics', 'astrophysics', 'quantum', 'research'],
            'sports': ['cricket', 'sports', 'fitness', 'workout', 'exercise'],
            'movies': ['movies', 'marvel', 'iron man', 'jarvis', 'cinema'],
            'education': ['learning', 'study', 'university', 'college', 'knowledge'],
            'career': ['career', 'job', 'work', 'professional', 'success'],
            'family': ['family', 'parents', 'brother', 'relationships'],
            'spirituality': ['spirituality', 'meditation', 'mindfulness', 'inner peace']
        }
        
        extracted_interests = {}
        for interest, keywords in interests.items():
            count = sum(1 for keyword in keywords if keyword in text)
            if count > 0:
                extracted_interests[interest] = count
        
        # Extract role models and inspirations
        role_models = []
        role_model_patterns = [
            r'inspired by ([a-zA-Z\s]+)',
            r'motivated by ([a-zA-Z\s]+)',
            r'look up to ([a-zA-Z\s]+)',
            r'admire ([a-zA-Z\s]+)'
        ]
        
        for pattern in role_model_patterns:
            matches = re.findall(pattern, text)
            role_models.extend(matches)
        
        # Extract specific mentioned role models
        mentioned_models = ['elon musk', 'steve jobs', 'einstein', 'ratan tata', 'brian green', 'ramanujan', 'max plank']
        for model in mentioned_models:
            if model in text:
                role_models.append(model.title())
        
        self.analysis_results['interests'] = extracted_interests
        self.analysis_results['role_models'] = list(set(role_models))
    
    def _extract_relationships(self):
        """Extract information about relationships and family"""
        text = self.bio_data['raw_text'].lower()
        
        # Family members
        family_members = {}
        
        # Extract family information
        family_patterns = {
            'father': ['dad', 'father', 'papa'],
            'mother': ['mom', 'mother', 'mama'],
            'brother': ['brother', 'elder brother', 'sibling'],
            'friends': ['friends', 'best friends', 'close friends']
        }
        
        for relation, keywords in family_patterns.items():
            for keyword in keywords:
                if keyword in text:
                    # Try to extract names
                    name_patterns = [
                        rf'{keyword}\s+([a-zA-Z\s]+)',
                        rf'([a-zA-Z\s]+)\s+{keyword}'
                    ]
                    for pattern in name_patterns:
                        match = re.search(pattern, text)
                        if match:
                            family_members[relation] = match.group(1).strip().title()
                            break
        
        # Extract friend names
        friend_names = []
        friend_patterns = [
            r'friends?\s+([a-zA-Z\s,]+)',
            r'best friends?\s+([a-zA-Z\s,]+)',
            r'close friends?\s+([a-zA-Z\s,]+)'
        ]
        
        for pattern in friend_patterns:
            match = re.search(pattern, text)
            if match:
                friends_text = match.group(1)
                # Split by common separators
                friends = re.split(r'[,;]\s*', friends_text)
                friend_names.extend([f.strip().title() for f in friends if f.strip()])
        
        self.analysis_results['family'] = family_members
        self.analysis_results['friends'] = friend_names
    
    def _extract_career_education(self):
        """Extract career and education information"""
        text = self.bio_data['raw_text'].lower()
        
        # Education
        education = {}
        
        # School information
        school_patterns = [
            r'studied in ([a-zA-Z\s]+)',
            r'school name was ([a-zA-Z\s]+)',
            r'attended ([a-zA-Z\s]+)'
        ]
        
        for pattern in school_patterns:
            match = re.search(pattern, text)
            if match:
                education['school'] = match.group(1).strip().title()
                break
        
        # College information
        college_patterns = [
            r'joined ([a-zA-Z\s]+)',
            r'studying at ([a-zA-Z\s]+)',
            r'university ([a-zA-Z\s]+)',
            r'college ([a-zA-Z\s]+)'
        ]
        
        for pattern in college_patterns:
            match = re.search(pattern, text)
            if match:
                education['college'] = match.group(1).strip().title()
                break
        
        # Career information
        career = {}
        
        # Current job
        job_patterns = [
            r'working at ([a-zA-Z\s]+)',
            r'employed at ([a-zA-Z\s]+)',
            r'work for ([a-zA-Z\s]+)',
            r'company called ([a-zA-Z\s]+)'
        ]
        
        for pattern in job_patterns:
            match = re.search(pattern, text)
            if match:
                career['current_company'] = match.group(1).strip().title()
                break
        
        # Job offers
        offer_patterns = [
            r'offers? from ([a-zA-Z\s]+)',
            r'received offers? from ([a-zA-Z\s]+)',
            r'approached by ([a-zA-Z\s]+)'
        ]
        
        offers = []
        for pattern in offer_patterns:
            matches = re.findall(pattern, text)
            offers.extend(matches)
        
        career['job_offers'] = [offer.strip().title() for offer in offers]
        
        self.analysis_results['education'] = education
        self.analysis_results['career'] = career
    
    def _extract_goals_aspirations(self):
        """Extract goals and aspirations"""
        text = self.bio_data['raw_text'].lower()
        
        goals = []
        
        # Goal patterns
        goal_patterns = [
            r'want to ([a-zA-Z\s]+)',
            r'goal is to ([a-zA-Z\s]+)',
            r'aspire to ([a-zA-Z\s]+)',
            r'dream of ([a-zA-Z\s]+)',
            r'plan to ([a-zA-Z\s]+)',
            r'aim to ([a-zA-Z\s]+)'
        ]
        
        for pattern in goal_patterns:
            matches = re.findall(pattern, text)
            goals.extend(matches)
        
        # Extract specific goals mentioned
        specific_goals = []
        if 'success' in text:
            specific_goals.append('Achieve success in career')
        if 'mercedes' in text:
            specific_goals.append('Buy Mercedes cars')
        if 'epitome' in text:
            specific_goals.append('Reach epitome of success')
        if 'bachelor' in text:
            specific_goals.append('Remain bachelor and focus on career')
        
        self.analysis_results['goals'] = goals
        self.analysis_results['specific_goals'] = specific_goals
    
    def get_personal_summary(self) -> str:
        """Get a comprehensive personal summary"""
        if not self.analysis_results:
            return "Personal information not available."
        
        summary_parts = []
        
        # Basic info
        if 'name' in self.analysis_results:
            summary_parts.append(f"Name: {self.analysis_results['name']}")
        
        if 'location' in self.analysis_results:
            summary_parts.append(f"Location: {self.analysis_results['location']}")
        
        if 'birth_date' in self.analysis_results:
            summary_parts.append(f"Born: {self.analysis_results['birth_date']}")
        
        # Personality traits
        if self.personality_traits:
            top_traits = sorted(self.personality_traits.items(), 
                              key=lambda x: x[1]['strength'], reverse=True)[:3]
            trait_names = [trait.replace('_', ' ').title() for trait, _ in top_traits]
            summary_parts.append(f"Key traits: {', '.join(trait_names)}")
        
        # Interests
        if 'interests' in self.analysis_results:
            top_interests = sorted(self.analysis_results['interests'].items(), 
                                 key=lambda x: x[1], reverse=True)[:3]
            interest_names = [interest.title() for interest, _ in top_interests]
            summary_parts.append(f"Main interests: {', '.join(interest_names)}")
        
        # Career
        if 'career' in self.analysis_results and 'current_company' in self.analysis_results['career']:
            summary_parts.append(f"Current company: {self.analysis_results['career']['current_company']}")
        
        # Goals
        if 'specific_goals' in self.analysis_results:
            summary_parts.append(f"Key goals: {', '.join(self.analysis_results['specific_goals'])}")
        
        return " | ".join(summary_parts)
    
    def get_sentiment_summary(self) -> str:
        """Get sentiment analysis summary"""
        if not self.sentiment_analysis:
            return "Sentiment analysis not available."
        
        sentiment = self.sentiment_analysis
        return f"Sentiment: {sentiment['category'].title()} (Score: {sentiment['score']:.2f})"
    
    def get_personality_profile(self) -> Dict[str, Any]:
        """Get comprehensive personality profile"""
        return {
            'basic_info': self.analysis_results,
            'sentiment_analysis': self.sentiment_analysis,
            'personality_traits': self.personality_traits,
            'summary': self.get_personal_summary(),
            'sentiment_summary': self.get_sentiment_summary()
        }
    
    def save_analysis(self, file_path: str = "personal_bio_analysis.json"):
        """Save analysis results to file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(self.get_personality_profile(), file, indent=2, ensure_ascii=False)
            print(f"Personal bio analysis saved to {file_path}")
        except Exception as e:
            print(f"Error saving analysis: {e}")

# Initialize the analyzer
personal_bio_analyzer = PersonalBioAnalyzer()
