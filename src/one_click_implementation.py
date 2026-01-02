"""
One-click implementation system with smart formatting
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from io import BytesIO

@dataclass
class ContentSection:
    """Content section for implementation"""
    title: str
    content: str
    formatted_content: str
    character_count: int
    word_count: int

class OneClickImplementation:
    """Smart implementation system with formatting and validation"""
    
    def __init__(self):
        self.linkedin_limits = {
            'headline': {'min': 60, 'max': 120},
            'about': {'min': 300, 'max': 500},
            'experience': {'min': 50, 'max': 300}
        }
        
        self.formatting_rules = {
            'remove_extra_whitespace': True,
            'fix_punctuation': True,
            'ensure_proper_capitalization': True,
            'escape_special_characters': True
        }
    
    def extract_content_from_report(self, optimization_report: str) -> Dict[str, ContentSection]:
        """Extract and format content sections from optimization report"""
        
        sections = {}
        
        # Extract headline options
        headline_content = self._extract_headline_content(optimization_report)
        if headline_content:
            sections['headline'] = ContentSection(
                title="Headline Options",
                content=headline_content,
                formatted_content=self._format_headline_content(headline_content),
                character_count=len(headline_content),
                word_count=len(headline_content.split())
            )
        
        # Extract about section
        about_content = self._extract_about_content(optimization_report)
        if about_content:
            sections['about'] = ContentSection(
                title="About Section",
                content=about_content,
                formatted_content=self._format_about_content(about_content),
                character_count=len(about_content),
                word_count=len(about_content.split())
            )
        
        # Extract experience content
        experience_content = self._extract_experience_content(optimization_report)
        if experience_content:
            sections['experience'] = ContentSection(
                title="Experience Section",
                content=experience_content,
                formatted_content=self._format_experience_content(experience_content),
                character_count=len(experience_content),
                word_count=len(experience_content.split())
            )
        
        # Extract skills content
        skills_content = self._extract_skills_content(optimization_report)
        if skills_content:
            sections['skills'] = ContentSection(
                title="Skills Section",
                content=skills_content,
                formatted_content=self._format_skills_content(skills_content),
                character_count=len(skills_content),
                word_count=len(skills_content.split())
            )
        
        return sections
    
    def _extract_headline_content(self, report: str) -> str:
        """Extract headline options from report"""
        headline_section = self._find_section(report, "HEADLINE OPTIMIZATION")
        if not headline_section:
            return ""
        
        # Look for recommended headlines
        headlines = []
        lines = headline_section.split('\n')
        
        for line in lines:
            # Look for numbered or bulleted headlines
            if re.match(r'^\d+\.', line.strip()) or line.strip().startswith('•'):
                clean_line = re.sub(r'^\d+\.\s*|•\s*', '', line.strip())
                if clean_line and len(clean_line) > 20:  # Reasonable headline length
                    headlines.append(clean_line)
        
        return '\n'.join(headlines) if headlines else ""
    
    def _extract_about_content(self, report: str) -> str:
        """Extract complete about section rewrite"""
        about_section = self._find_section(report, "ABOUT SECTION COMPLETE REWRITE")
        if not about_section:
            return ""
        
        # Look for "Recommended Version" or similar
        if "Recommended Version" in about_section:
            parts = about_section.split("Recommended Version")
            if len(parts) > 1:
                content = parts[1].strip()
                # Remove any section headers that follow
                content = re.split(r'\n[A-Z]+ [A-Z]+', content)[0].strip()
                return content
        
        return about_section.strip()
    
    def _extract_experience_content(self, report: str) -> str:
        """Extract enhanced experience content"""
        experience_section = self._find_section(report, "EXPERIENCE SECTION ENHANCEMENT")
        if not experience_section:
            return ""
        
        # Extract all experience entries
        content = experience_section.strip()
        
        # Remove section headers and keep only content
        lines = content.split('\n')
        content_lines = []
        
        for line in lines:
            line = line.strip()
            # Skip headers and empty lines
            if not line or line.isupper() or line.startswith('CURRENT') or line.startswith('RECOMMENDED'):
                continue
            content_lines.append(line)
        
        return '\n'.join(content_lines)
    
    def _extract_skills_content(self, report: str) -> str:
        """Extract skills strategy content"""
        skills_section = self._find_section(report, "SKILLS STRATEGY")
        if not skills_section:
            return ""
        
        # Extract skills list
        skills = []
        lines = skills_section.split('\n')
        
        for line in lines:
            # Look for skills in list format
            if re.match(r'^\d+\.', line.strip()) or line.strip().startswith('•') or line.strip().startswith('-'):
                clean_line = re.sub(r'^\d+\.\s*|•\s*|-\s*', '', line.strip())
                if clean_line and len(clean_line) > 2:
                    skills.append(clean_line)
        
        return '\n'.join(skills) if skills else ""
    
    def _find_section(self, report: str, section_name: str) -> str:
        """Find and extract a specific section from the report"""
        start_pos = report.find(section_name)
        if start_pos == -1:
            return ""
        
        # Find next major section
        section_headers = [
            "OVERALL PROFILE REVIEW", "HEADLINE OPTIMIZATION", "ABOUT SECTION COMPLETE REWRITE",
            "EXPERIENCE SECTION ENHANCEMENT", "SKILLS STRATEGY", "RECOMMENDATIONS STRATEGY",
            "CONTENT & ENGAGEMENT PLAN"
        ]
        
        end_pos = len(report)
        current_index = section_headers.index(section_name)
        
        for next_section in section_headers[current_index + 1:]:
            next_pos = report.find(next_section)
            if next_pos != -1 and next_pos > start_pos:
                end_pos = next_pos
                break
        
        return report[start_pos:end_pos]
    
    def _format_headline_content(self, content: str) -> str:
        """Format headline content for LinkedIn"""
        # Clean up and format headlines
        headlines = content.split('\n')
        formatted_headlines = []
        
        for headline in headlines:
            headline = headline.strip()
            if headline:
                # Ensure proper capitalization
                headline = self._ensure_proper_capitalization(headline)
                # Remove extra whitespace
                headline = re.sub(r'\s+', ' ', headline)
                formatted_headlines.append(headline)
        
        return '\n\n'.join(formatted_headlines)
    
    def _format_about_content(self, content: str) -> str:
        """Format about section for LinkedIn"""
        # Clean up paragraphs
        paragraphs = content.split('\n\n')
        formatted_paragraphs = []
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if paragraph:
                # Remove bullet points that might be in the middle
                paragraph = re.sub(r'^\s*[•\-\*]\s*', '', paragraph)
                # Ensure proper spacing
                paragraph = re.sub(r'\s+', ' ', paragraph)
                # Proper capitalization
                paragraph = self._ensure_proper_capitalization(paragraph)
                formatted_paragraphs.append(paragraph)
        
        return '\n\n'.join(formatted_paragraphs)
    
    def _format_experience_content(self, content: str) -> str:
        """Format experience content for LinkedIn"""
        # Clean up bullet points and formatting
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Format bullet points
            if re.match(r'^\d+\.', line) or line.startswith('•') or line.startswith('-'):
                # Ensure consistent bullet format
                clean_line = re.sub(r'^\d+\.\s*|•\s*|-\s*', '• ', line)
                # Ensure proper capitalization
                clean_line = self._ensure_proper_capitalization(clean_line[2:])
                formatted_lines.append('• ' + clean_line)
            else:
                # Regular text line
                clean_line = self._ensure_proper_capitalization(line)
                formatted_lines.append(clean_line)
        
        return '\n'.join(formatted_lines)
    
    def _format_skills_content(self, content: str) -> str:
        """Format skills content for LinkedIn"""
        # Clean up skills list
        skills = content.split('\n')
        formatted_skills = []
        
        for skill in skills:
            skill = skill.strip()
            if skill:
                # Remove any numbering or bullets
                clean_skill = re.sub(r'^\d+\.\s*|•\s*|-\s*', '', skill)
                clean_skill = clean_skill.strip()
                if clean_skill:
                    formatted_skills.append(clean_skill)
        
        return ', '.join(formatted_skills)
    
    def _ensure_proper_capitalization(self, text: str) -> str:
        """Ensure proper capitalization"""
        if not text:
            return text
        
        # Capitalize first letter of sentences
        text = re.sub(r'([.!?]\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper(), text)
        
        # Capitalize first letter if it's lowercase
        if text and text[0].islower():
            text = text[0].upper() + text[1:]
        
        return text
    
    def validate_content_length(self, section: str, content: str) -> Dict[str, Any]:
        """Validate content against LinkedIn limits"""
        limits = self.linkedin_limits.get(section, {})
        
        if not limits:
            return {'valid': True, 'message': 'No limits defined for this section'}
        
        char_count = len(content)
        
        if char_count < limits['min']:
            return {
                'valid': False,
                'message': f'Too short - minimum {limits["min"]} characters (currently {char_count})',
                'type': 'too_short'
            }
        elif char_count > limits['max']:
            return {
                'valid': False,
                'message': f'Too long - maximum {limits["max"]} characters (currently {char_count})',
                'type': 'too_long'
            }
        else:
            return {
                'valid': True,
                'message': f'Good length - {char_count} characters',
                'type': 'good'
            }
    
    def create_implementation_package(self, sections: Dict[str, ContentSection]) -> Dict[str, Any]:
        """Create complete implementation package"""
        
        package = {
            'sections': sections,
            'validation_results': {},
            'implementation_order': ['headline', 'about', 'experience', 'skills'],
            'total_content': '',
            'word_count': 0,
            'character_count': 0
        }
        
        # Validate each section
        for section_name, section_data in sections.items():
            package['validation_results'][section_name] = self.validate_content_length(
                section_name, section_data.formatted_content
            )
        
        # Calculate totals
        for section_data in sections.values():
            package['total_content'] += section_data.formatted_content + '\n\n'
            package['word_count'] += section_data.word_count
            package['character_count'] += section_data.character_count
        
        return package
    
    def generate_copy_text(self, sections: Dict[str, ContentSection], section_name: str) -> str:
        """Generate copy-ready text for a specific section"""
        if section_name not in sections:
            return ""
        
        section = sections[section_name]
        
        # Add section header for context
        header = f"=== {section.title.upper()} ===\n\n"
        
        return header + section.formatted_content
    
    def create_batch_copy_text(self, sections: Dict[str, ContentSection]) -> str:
        """Create batch copy text for all sections"""
        batch_text = "LINKEDIN PROFILE OPTIMIZATION - READY TO IMPLEMENT\n"
        batch_text += "=" * 60 + "\n\n"
        
        order = ['headline', 'about', 'experience', 'skills']
        
        for section_name in order:
            if section_name in sections:
                section = sections[section_name]
                batch_text += f"=== {section.title.upper()} ===\n\n"
                batch_text += section.formatted_content + "\n\n"
                batch_text += "-" * 40 + "\n\n"
        
        return batch_text
