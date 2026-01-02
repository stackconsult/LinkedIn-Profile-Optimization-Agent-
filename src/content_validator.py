"""
Content quality validation system for LinkedIn optimization outputs
"""

import re
from typing import Dict, List, Tuple, Any
from .prompt_templates import INDUSTRY_DATA

class ContentQualityValidator:
    """Validates and scores LinkedIn optimization content quality"""
    
    def __init__(self):
        self.min_requirements = {
            "about_min_length": 300,
            "about_max_length": 500,
            "headline_max_length": 220,
            "min_keywords": 5,
            "min_achievements_per_experience": 3,
            "min_quantifiable_metrics": 8
        }
    
    def validate_content_quality(self, content: Dict[str, Any], target_industry: str, target_role: str) -> Tuple[int, List[str]]:
        """
        Validate content quality and return score with feedback
        
        Args:
            content: Dictionary with optimized content sections
            target_industry: Target industry for keyword validation
            target_role: Target role for relevance validation
            
        Returns:
            Tuple of (score_out_of_100, feedback_list)
        """
        score = 0
        feedback = []
        
        # Get industry data for validation
        industry_info = INDUSTRY_DATA.get(target_industry, INDUSTRY_DATA["Technology"])
        industry_keywords = set(industry_info["keywords"])
        role_skills = set(industry_info["role_specific"].get(target_role, {}).get("skills", []))
        
        # 1. Validate Headline
        headline_score, headline_feedback = self._validate_headline(content.get("headline", ""), industry_keywords)
        score += headline_score
        feedback.extend(headline_feedback)
        
        # 2. Validate About Section
        about_score, about_feedback = self._validate_about_section(content.get("about", ""), industry_keywords, role_skills)
        score += about_score
        feedback.extend(about_feedback)
        
        # 3. Validate Experience Section
        experience_score, experience_feedback = self._validate_experience_section(
            content.get("experience", []), industry_keywords
        )
        score += experience_score
        feedback.extend(experience_feedback)
        
        # 4. Validate Skills Section
        skills_score, skills_feedback = self._validate_skills_section(
            content.get("skills", []), role_skills
        )
        score += skills_score
        feedback.extend(skills_feedback)
        
        # 5. Overall Content Quality
        overall_score, overall_feedback = self._validate_overall_quality(content)
        score += overall_score
        feedback.extend(overall_feedback)
        
        return min(score, 100), feedback
    
    def _validate_headline(self, headline: str, industry_keywords: set) -> Tuple[int, List[str]]:
        """Validate headline quality"""
        score = 0
        feedback = []
        
        # Length check
        if len(headline) <= self.min_requirements["headline_max_length"]:
            score += 10
        else:
            feedback.append(f"❌ Headline too long ({len(headline)} chars). Max: {self.min_requirements['headline_max_length']}")
        
        # Industry keywords check
        keyword_count = len([kw for kw in industry_keywords if kw.lower() in headline.lower()])
        if keyword_count >= 1:
            score += 10
        else:
            feedback.append("❌ Headline should include at least 1 industry keyword")
        
        # Quantifiable metrics check
        if re.search(r'\d+%|\$\d+|\d+ years?', headline):
            score += 10
        else:
            feedback.append("❌ Headline should include a quantifiable achievement (%, $, or numbers)")
        
        return score, feedback
    
    def _validate_about_section(self, about: str, industry_keywords: set, role_skills: set) -> Tuple[int, List[str]]:
        """Validate about section quality"""
        score = 0
        feedback = []
        
        # Length check
        if self.min_requirements["about_min_length"] <= len(about) <= self.min_requirements["about_max_length"]:
            score += 15
        elif len(about) < self.min_requirements["about_min_length"]:
            feedback.append(f"❌ About section too short ({len(about)} chars). Min: {self.min_requirements['about_min_length']}")
        else:
            feedback.append(f"❌ About section too long ({len(about)} chars). Max: {self.min_requirements['about_max_length']}")
        
        # Industry keywords check
        keyword_count = len([kw for kw in industry_keywords if kw.lower() in about.lower()])
        if keyword_count >= 3:
            score += 10
        else:
            feedback.append(f"❌ About section should include at least 3 industry keywords (found: {keyword_count})")
        
        # Role skills check
        skill_count = len([skill for skill in role_skills if skill.lower() in about.lower()])
        if skill_count >= 2:
            score += 10
        else:
            feedback.append(f"❌ About section should include at least 2 role-specific skills (found: {skill_count})")
        
        # Quantifiable achievements check
        metric_count = len(re.findall(r'\d+%|\$\d+|\d+ (?:years?|months?|people|projects|teams)', about))
        if metric_count >= 3:
            score += 15
        else:
            feedback.append(f"❌ About section should include at least 3 quantifiable achievements (found: {metric_count})")
        
        return score, feedback
    
    def _validate_experience_section(self, experiences: List[Dict], industry_keywords: set) -> Tuple[int, List[str]]:
        """Validate experience section quality"""
        score = 0
        feedback = []
        total_achievements = 0
        total_metrics = 0
        
        for i, exp in enumerate(experiences):
            achievements = 0
            metrics = 0
            
            description = exp.get("description", "")
            
            # Check for bullet points (achievements)
            bullet_points = re.split(r'[-•*]\s*', description)
            bullet_points = [bp.strip() for bp in bullet_points if bp.strip()]
            achievements = len(bullet_points)
            total_achievements += achievements
            
            # Check for quantifiable metrics
            metrics = len(re.findall(r'\d+%|\$\d+|\d+ (?:years?|months?|people|projects|teams)', description))
            total_metrics += metrics
            
            # Industry keywords in experience
            keyword_count = len([kw for kw in industry_keywords if kw.lower() in description.lower()])
            
            if achievements >= 3:
                score += 5
            else:
                feedback.append(f"❌ Experience {i+1} should have at least 3 bullet points (found: {achievements})")
            
            if metrics >= 2:
                score += 5
            else:
                feedback.append(f"❌ Experience {i+1} should include at least 2 metrics (found: {metrics})")
        
        # Overall experience validation
        if total_achievements >= len(experiences) * 3:
            score += 10
        else:
            feedback.append(f"❌ Each experience should have at least 3 bullet points")
        
        if total_metrics >= self.min_requirements["min_quantifiable_metrics"]:
            score += 10
        else:
            feedback.append(f"❌ Total quantifiable metrics should be at least {self.min_requirements['min_quantifiable_metrics']} (found: {total_metrics})")
        
        return score, feedback
    
    def _validate_skills_section(self, skills: List[str], role_skills: set) -> Tuple[int, List[str]]:
        """Validate skills section quality"""
        score = 0
        feedback = []
        
        # Check for role-specific skills
        found_role_skills = [skill for skill in role_skills if skill in skills]
        if len(found_role_skills) >= 3:
            score += 15
        else:
            feedback.append(f"❌ Skills section should include at least 3 role-specific skills (found: {len(found_role_skills)})")
        
        # Total skills count
        if len(skills) >= 10:
            score += 10
        else:
            feedback.append(f"❌ Skills section should include at least 10 skills (found: {len(skills)})")
        
        # Skills categorization (technical, business, leadership)
        technical_skills = [s for s in skills if any(tech in s.lower() for tech in ['python', 'java', 'javascript', 'aws', 'azure', 'sql', 'react'])]
        if len(technical_skills) >= 3:
            score += 5
        else:
            feedback.append("❌ Include more technical skills")
        
        return score, feedback
    
    def _validate_overall_quality(self, content: Dict[str, Any]) -> Tuple[int, List[str]]:
        """Validate overall content quality"""
        score = 0
        feedback = []
        
        # Check for completeness
        required_sections = ["headline", "about", "experience", "skills"]
        missing_sections = [section for section in required_sections if not content.get(section)]
        
        if not missing_sections:
            score += 10
        else:
            feedback.append(f"❌ Missing required sections: {', '.join(missing_sections)}")
        
        # Check for action-oriented language
        all_text = " ".join([
            content.get("headline", ""),
            content.get("about", ""),
            " ".join([exp.get("description", "") for exp in content.get("experience", [])])
        ])
        
        action_verbs = len(re.findall(r'\b(led|managed|developed|created|implemented|optimized|achieved|increased|reduced|improved)\b', all_text, re.IGNORECASE))
        if action_verbs >= 5:
            score += 10
        else:
            feedback.append(f"❌ Include more action verbs (found: {action_verbs})")
        
        # Check for professional tone
        unprofessional_words = ['awesome', 'cool', 'stuff', 'things', 'etc', 'blah', 'lol']
        found_unprofessional = [word for word in unprofessional_words if word in all_text.lower()]
        
        if not found_unprofessional:
            score += 10
        else:
            feedback.append(f"❌ Remove unprofessional language: {', '.join(found_unprofessional)}")
        
        return score, feedback
    
    def generate_improvement_suggestions(self, content: Dict[str, Any], target_industry: str, target_role: str) -> List[str]:
        """Generate specific improvement suggestions"""
        score, feedback = self.validate_content_quality(content, target_industry, target_role)
        
        if score >= 80:
            return ["✅ Content quality is excellent! Ready for implementation."]
        
        suggestions = []
        industry_info = INDUSTRY_DATA.get(target_industry, INDUSTRY_DATA["Technology"])
        
        # Headline suggestions
        if "❌ Headline" in " ".join(feedback):
            suggestions.append(f"🎯 Headline: Add a quantifiable achievement and 1+ industry keywords like {industry_info['keywords'][:3]}")
        
        # About section suggestions
        if "❌ About section" in " ".join(feedback):
            suggestions.append(f"📝 About: Add 3+ specific achievements with metrics (%, $, numbers) and industry keywords")
        
        # Experience suggestions
        if "❌ Experience" in " ".join(feedback):
            suggestions.append("💼 Experience: Rewrite bullet points with 'Achieved X% improvement' format")
        
        # Skills suggestions
        if "❌ Skills section" in " ".join(feedback):
            role_skills = industry_info["role_specific"].get(target_role, {}).get("skills", [])
            suggestions.append(f"🔧 Skills: Add role-specific skills like {role_skills[:5]}")
        
        return suggestions


# Global validator instance
content_validator = ContentQualityValidator()
