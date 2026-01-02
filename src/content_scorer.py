"""
Content quality scoring and validation system for LinkedIn profiles
"""

import re
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass

@dataclass
class QualityMetrics:
    """Data class for quality metrics"""
    score: int
    max_score: int
    feedback: List[str]
    suggestions: List[str]

class ContentQualityScorer:
    """Advanced content quality scoring system"""
    
    def __init__(self):
        self.industry_keywords = {
            "Technology": ["software", "development", "programming", "coding", "tech", "digital", "data", "ai", "ml"],
            "Finance": ["financial", "investment", "banking", "trading", "risk", "compliance", "fintech"],
            "Healthcare": ["healthcare", "medical", "clinical", "patient", "health", "wellness", "pharmaceutical"],
            "Marketing": ["marketing", "brand", "digital", "social", "content", "campaign", "analytics"],
            "Sales": ["sales", "revenue", "growth", "client", "business", "account", "relationship"]
        }
        
        self.action_verbs = [
            "led", "managed", "developed", "created", "implemented", "launched", 
            "grew", "increased", "reduced", "improved", "optimized", "achieved"
        ]
        
        self.quantifiable_indicators = [
            "%", "$", "number", "count", "increase", "decrease", "growth", "reduction",
            "million", "billion", "thousand", "hundred", "times", "fold"
        ]
    
    def calculate_overall_score(self, profile_data: Dict[str, Any], target_industry: str, target_role: str) -> Dict[str, QualityMetrics]:
        """Calculate comprehensive quality scores for all profile sections"""
        
        scores = {}
        
        # Headline Quality Score
        scores['headline'] = self._score_headline(profile_data.get('headline', ''), target_role)
        
        # About Section Quality Score
        scores['about'] = self._score_about_section(profile_data.get('about', ''), target_industry)
        
        # Experience Quality Score
        scores['experience'] = self._score_experience_section(profile_data.get('experience', []))
        
        # Skills Quality Score
        scores['skills'] = self._score_skills_section(profile_data.get('skills', []), target_industry)
        
        # Overall Profile Score
        scores['overall'] = self._calculate_overall_profile_score(scores)
        
        return scores
    
    def _score_headline(self, headline: str, target_role: str) -> QualityMetrics:
        """Score headline quality"""
        score = 0
        max_score = 100
        feedback = []
        suggestions = []
        
        # Length check (ideal: 60-120 characters)
        if 60 <= len(headline) <= 120:
            score += 25
        else:
            feedback.append("Headline length is not optimal")
            suggestions.append("Aim for 60-120 characters for maximum impact")
        
        # Value proposition check
        value_words = ["helping", "driving", "delivering", "creating", "solving"]
        if any(word in headline.lower() for word in value_words):
            score += 25
        else:
            feedback.append("Missing clear value proposition")
            suggestions.append("Include what value you provide to employers")
        
        # Target role keywords
        if target_role.lower() in headline.lower():
            score += 25
        else:
            feedback.append("Target role not mentioned")
            suggestions.append(f"Include '{target_role}' in your headline")
        
        # Professional tone
        if not any(word in headline.lower() for word in ["looking", "seeking", "unemployed"]):
            score += 25
        else:
            feedback.append("Avoid passive language")
            suggestions.append("Use active, confident language")
        
        return QualityMetrics(score, max_score, feedback, suggestions)
    
    def _score_about_section(self, about: str, target_industry: str) -> QualityMetrics:
        """Score about section quality"""
        score = 0
        max_score = 100
        feedback = []
        suggestions = []
        
        # Length check (ideal: 300-500 words)
        word_count = len(about.split())
        if 300 <= word_count <= 500:
            score += 20
        else:
            feedback.append(f"About section is {word_count} words (ideal: 300-500)")
            suggestions.append("Expand your about section to 300-500 words")
        
        # Storytelling elements
        story_indicators = ["journey", "passion", "mission", "vision", "story"]
        if any(word in about.lower() for word in story_indicators):
            score += 20
        else:
            feedback.append("Missing storytelling elements")
            suggestions.append("Add your career story and passion")
        
        # Industry keywords
        industry_keywords = self.industry_keywords.get(target_industry, [])
        keyword_count = sum(1 for keyword in industry_keywords if keyword.lower() in about.lower())
        if keyword_count >= 3:
            score += 20
        else:
            feedback.append(f"Only {keyword_count} industry keywords found")
            suggestions.append(f"Include more {target_industry} industry keywords")
        
        # Quantifiable achievements
        quant_count = sum(1 for indicator in self.quantifiable_indicators if indicator in about.lower())
        if quant_count >= 2:
            score += 20
        else:
            feedback.append("Missing quantifiable achievements")
            suggestions.append("Add specific numbers and metrics")
        
        # Call to action
        cta_indicators = ["connect", "reach out", "contact", "opportunity", "collaborate"]
        if any(word in about.lower() for word in cta_indicators):
            score += 20
        else:
            feedback.append("Missing call to action")
            suggestions.append("Add a clear call to action for recruiters")
        
        return QualityMetrics(score, max_score, feedback, suggestions)
    
    def _score_experience_section(self, experiences: List[Dict]) -> QualityMetrics:
        """Score experience section quality"""
        score = 0
        max_score = 100
        feedback = []
        suggestions = []
        
        if not experiences:
            return QualityMetrics(0, max_score, ["No experience entries found"], ["Add your work experience"])
        
        total_possible_score = len(experiences) * 25
        actual_score = 0
        
        for exp in experiences:
            exp_score = 0
            description = exp.get('description', '')
            
            # Action verbs
            action_count = sum(1 for verb in self.action_verbs if verb in description.lower())
            if action_count >= 2:
                exp_score += 8
            else:
                feedback.append(f"Experience '{exp.get('title', 'Unknown')}' lacks action verbs")
                suggestions.append("Start bullet points with action verbs")
            
            # Quantifiable results
            quant_count = sum(1 for indicator in self.quantifiable_indicators if indicator in description.lower())
            if quant_count >= 1:
                exp_score += 9
            else:
                feedback.append(f"Experience '{exp.get('title', 'Unknown')}' lacks metrics")
                suggestions.append("Add specific numbers and results")
            
            # Impact statements
            impact_indicators = ["resulted in", "led to", "achieved", "improved", "increased"]
            if any(indicator in description.lower() for indicator in impact_indicators):
                exp_score += 8
            else:
                feedback.append(f"Experience '{exp.get('title', 'Unknown')}' lacks impact statements")
                suggestions.append("Show the impact of your work")
            
            actual_score += exp_score
        
        # Normalize score
        if total_possible_score > 0:
            score = int((actual_score / total_possible_score) * 100)
        
        return QualityMetrics(score, max_score, feedback, suggestions)
    
    def _score_skills_section(self, skills: List[str], target_industry: str) -> QualityMetrics:
        """Score skills section quality"""
        score = 0
        max_score = 100
        feedback = []
        suggestions = []
        
        if not skills:
            return QualityMetrics(0, max_score, ["No skills listed"], ["Add your relevant skills"])
        
        # Skill count (ideal: 10-15)
        if 10 <= len(skills) <= 15:
            score += 30
        else:
            feedback.append(f"Skills count: {len(skills)} (ideal: 10-15)")
            suggestions.append("Aim for 10-15 relevant skills")
        
        # Industry relevance
        industry_keywords = self.industry_keywords.get(target_industry, [])
        relevant_skills = [skill for skill in skills if any(keyword in skill.lower() for keyword in industry_keywords)]
        
        if len(relevant_skills) >= 5:
            score += 40
        else:
            feedback.append(f"Only {len(relevant_skills)} industry-relevant skills")
            suggestions.append(f"Add more {target_industry} specific skills")
        
        # Skill diversity (technical vs soft)
        technical_indicators = ["python", "java", "javascript", "sql", "aws", "docker", "kubernetes"]
        soft_indicators = ["leadership", "communication", "teamwork", "management", "strategy"]
        
        technical_skills = [skill for skill in skills if any(indicator in skill.lower() for indicator in technical_indicators)]
        soft_skills = [skill for skill in skills if any(indicator in skill.lower() for indicator in soft_indicators)]
        
        if technical_skills and soft_skills:
            score += 30
        else:
            feedback.append("Balance technical and soft skills")
            suggestions.append("Include both technical and soft skills")
        
        return QualityMetrics(score, max_score, feedback, suggestions)
    
    def _calculate_overall_profile_score(self, section_scores: Dict[str, QualityMetrics]) -> QualityMetrics:
        """Calculate overall profile quality score"""
        weights = {
            'headline': 0.2,
            'about': 0.3,
            'experience': 0.35,
            'skills': 0.15
        }
        
        total_score = 0
        all_feedback = []
        all_suggestions = []
        
        for section, score_obj in section_scores.items():
            if section in weights:
                weight = weights[section]
                total_score += (score_obj.score / 100) * weight * 100
                all_feedback.extend(score_obj.feedback)
                all_suggestions.extend(score_obj.suggestions)
        
        return QualityMetrics(
            int(total_score),
            100,
            all_feedback,
            all_suggestions
        )
    
    def score_profile_content(self, profile_data, target_industry: str = "Technology", target_role: str = "Software Engineer") -> Dict[str, Any]:
        """Score profile content - wrapper for calculate_overall_score"""
        # Convert LinkedInProfile to dict if needed
        if hasattr(profile_data, 'headline'):
            # Handle Pydantic models - convert to dict format
            experience_list = []
            if hasattr(profile_data, 'experience') and profile_data.experience:
                for exp in profile_data.experience:
                    if hasattr(exp, 'dict'):
                        # Pydantic model
                        exp_dict = exp.dict()
                    elif hasattr(exp, '__dict__'):
                        # Object with __dict__
                        exp_dict = exp.__dict__
                    elif isinstance(exp, dict):
                        # Already a dict
                        exp_dict = exp
                    else:
                        # Unknown format, create basic dict
                        exp_dict = {
                            'title': getattr(exp, 'title', 'Unknown'),
                            'company': getattr(exp, 'company', 'Unknown'),
                            'dates': getattr(exp, 'dates', ''),
                            'description': getattr(exp, 'description', '')
                        }
                    experience_list.append(exp_dict)
            
            profile_dict = {
                'headline': profile_data.headline,
                'about': profile_data.about,
                'experience': experience_list,
                'skills': profile_data.skills if hasattr(profile_data, 'skills') else []
            }
        else:
            profile_dict = profile_data
        
        # Calculate scores using existing method
        scores = self.calculate_overall_score(profile_dict, target_industry, target_role)
        
        # Convert to simple dict format for UI
        result = {}
        for section, metrics in scores.items():
            result[f'{section}_score'] = metrics.score
            result[f'{section}_max_score'] = metrics.max_score
            result[f'{section}_feedback'] = metrics.feedback
            result[f'{section}_suggestions'] = metrics.suggestions
        
        return result
    
    def get_quality_recommendations(self, quality_scores: Dict[str, Any]) -> List[str]:
        """Get quality recommendations based on scores"""
        recommendations = []
        
        # Extract scores from the quality_scores dict
        for key, value in quality_scores.items():
            if key.endswith('_score') and isinstance(value, int):
                section = key.replace('_score', '')
                score = value
                max_score_key = f'{section}_max_score'
                max_score = quality_scores.get(max_score_key, 100)
                
                if score < max_score * 0.7:  # Less than 70% of max score
                    feedback_key = f'{section}_feedback'
                    feedback = quality_scores.get(feedback_key, [])
                    recommendations.extend(feedback)
        
        return list(set(recommendations))  # Remove duplicates
    
    def validate_content(self, content: str, content_type: str) -> Dict[str, Any]:
        """Real-time content validation"""
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'suggestions': []
        }
        
        # Character limits
        limits = {
            'headline': {'min': 60, 'max': 120},
            'about': {'min': 300, 'max': 500},
            'experience': {'min': 50, 'max': 300}
        }
        
        if content_type in limits:
            limit = limits[content_type]
            length = len(content)
            
            if length < limit['min']:
                validation_result['errors'].append(f"Too short - minimum {limit['min']} characters")
                validation_result['is_valid'] = False
            elif length > limit['max']:
                validation_result['warnings'].append(f"Quite long - consider reducing to {limit['max']} characters")
        
        # Common issues
        if "looking for" in content.lower():
            validation_result['warnings'].append("Avoid passive language like 'looking for'")
        
        if content.count('!') > 2:
            validation_result['warnings'].append("Too many exclamation marks")
        
        # Suggestions
        if not any(verb in content.lower() for verb in self.action_verbs):
            validation_result['suggestions'].append("Add more action verbs")
        
        return validation_result
