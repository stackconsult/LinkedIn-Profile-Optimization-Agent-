"""
PDF Profile Analysis System with OCR and Deep Research
"""

import re
import io
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import json

# PDF processing libraries (optional)
try:
    import PyPDF2
    PDF_PYPDF2_AVAILABLE = True
except ImportError:
    PDF_PYPDF2_AVAILABLE = False

try:
    import pdfplumber
    PDF_PLUMBER_AVAILABLE = True
except ImportError:
    PDF_PLUMBER_AVAILABLE = False

# OCR libraries (optional)
try:
    import pytesseract
    from PIL import Image
    OCR_PYTESSERACT_AVAILABLE = True
except ImportError:
    OCR_PYTESSERACT_AVAILABLE = False

try:
    import fitz  # PyMuPDF
    OCR_FITZ_AVAILABLE = True
except ImportError:
    OCR_FITZ_AVAILABLE = False

PDF_AVAILABLE = PDF_PYPDF2_AVAILABLE or PDF_PLUMBER_AVAILABLE
OCR_AVAILABLE = OCR_PYTESSERACT_AVAILABLE and OCR_FITZ_AVAILABLE

@dataclass
class PDFProfileData:
    """Complete profile data extracted from PDF"""
    raw_text: str
    sections: Dict[str, str]
    experiences: List[Dict[str, str]]
    skills: List[str]
    education: List[Dict[str, str]]
    contact_info: Dict[str, str]
    metadata: Dict[str, Any]

class PDFProfileAnalyzer:
    """Advanced PDF profile analysis with OCR and deep research"""
    
    def __init__(self):
        self.section_patterns = {
            'experience': [
                r'experience|work experience|professional experience|employment|work history',
                r'career|professional background|job history'
            ],
            'education': [
                r'education|academic|university|college|degree',
                r'qualification|certification|training'
            ],
            'skills': [
                r'skills|competencies|expertise|technical skills',
                r'proficiencies|capabilities|toolkit|technologies'
            ],
            'about': [
                r'about|summary|profile|objective|introduction',
                r'professional summary|personal statement'
            ],
            'contact': [
                r'contact|email|phone|address|linkedin',
                r'reach out|get in touch|connect'
            ]
        }
        
        self.experience_indicators = [
            r'(\d{1,2}/\d{4}|\d{4}\s*-\s*(\d{4}|present))',  # Date ranges
            r'(company|corporation|inc\.|ltd\.|llc)',  # Company indicators
            r'(manager|director|senior|junior|lead|chief)',  # Position indicators
        ]
    
    def analyze_pdf(self, pdf_file) -> PDFProfileData:
        """Complete PDF analysis with OCR and structure extraction"""
        
        if not PDF_AVAILABLE:
            raise ImportError("PDF processing libraries not available. Install PyPDF2 or pdfplumber: pip install PyPDF2 pdfplumber")
        
        # Extract text using multiple methods
        raw_text = self._extract_text_from_pdf(pdf_file)
        
        # If text extraction is poor, use OCR
        if len(raw_text.strip()) < 500:  # Threshold for OCR
            if OCR_AVAILABLE:
                raw_text = self._ocr_pdf(pdf_file)
            else:
                # OCR not available, work with what we have
                print("Warning: OCR libraries not available. Working with extracted text only.")
        
        # Structure the extracted text
        sections = self._extract_sections(raw_text)
        experiences = self._extract_experiences(raw_text, sections.get('experience', ''))
        skills = self._extract_skills(raw_text, sections.get('skills', ''))
        education = self._extract_education(raw_text, sections.get('education', ''))
        contact_info = self._extract_contact_info(raw_text)
        
        # Generate metadata
        metadata = {
            'total_characters': len(raw_text),
            'word_count': len(raw_text.split()),
            'sections_found': list(sections.keys()),
            'experiences_count': len(experiences),
            'skills_count': len(skills),
            'processing_method': 'ocr' if len(raw_text.strip()) < 500 else 'direct',
            'pdf_libraries': {
                'pypdf2': PDF_PYPDF2_AVAILABLE,
                'pdfplumber': PDF_PLUMBER_AVAILABLE,
                'ocr_available': OCR_AVAILABLE
            }
        }
        
        return PDFProfileData(
            raw_text=raw_text,
            sections=sections,
            experiences=experiences,
            skills=skills,
            education=education,
            contact_info=contact_info,
            metadata=metadata
        )
    
    def _extract_text_from_pdf(self, pdf_file) -> str:
        """Extract text directly from PDF"""
        text = ""
        
        try:
            # Method 1: PyPDF2
            if PDF_PYPDF2_AVAILABLE:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"PyPDF2 extraction failed: {e}")
        
        try:
            # Method 2: pdfplumber (more accurate)
            if PDF_PLUMBER_AVAILABLE:
                pdf_file.seek(0)  # Reset file pointer
                with pdfplumber.open(pdf_file) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text() + "\n"
        except Exception as e:
            print(f"pdfplumber extraction failed: {e}")
        
        return text
    
    def _ocr_pdf(self, pdf_file) -> str:
        """OCR PDF when direct extraction fails"""
        text = ""
        
        if not OCR_AVAILABLE:
            raise ImportError("OCR libraries not available. Install pytesseract, PyMuPDF, and Pillow: pip install pytesseract PyMuPDF Pillow")
        
        try:
            # Use PyMuPDF to convert PDF pages to images
            pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
            
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                
                # Convert page to image
                pix = page.get_pixmap()
                img_data = pix.tobytes("png")
                image = Image.open(io.BytesIO(img_data))
                
                # OCR the image
                page_text = pytesseract.image_to_string(image)
                text += page_text + "\n"
                
        except Exception as e:
            raise ImportError(f"OCR processing failed: {e}")
        
        return text
    
    def _extract_sections(self, text: str) -> Dict[str, str]:
        """Extract different sections from the text"""
        sections = {}
        
        # Normalize text
        normalized_text = text.lower()
        
        for section_name, patterns in self.section_patterns.items():
            section_content = ""
            
            for pattern in patterns:
                # Find section start
                matches = list(re.finditer(pattern, normalized_text, re.IGNORECASE))
                
                for match in matches:
                    start_pos = match.start()
                    
                    # Find next section (look for any section header)
                    end_pos = len(text)
                    for other_section, other_patterns in self.section_patterns.items():
                        if other_section != section_name:
                            for other_pattern in other_patterns:
                                other_match = re.search(other_pattern, normalized_text[start_pos+100:], re.IGNORECASE)
                                if other_match:
                                    end_pos = min(end_pos, start_pos + 100 + other_match.start())
                                    break
                    
                    # Extract section content
                    section_text = text[start_pos:end_pos].strip()
                    if len(section_text) > len(section_content):
                        section_content = section_text
            
            if section_content:
                sections[section_name] = section_content
        
        return sections
    
    def _extract_experiences(self, text: str, experience_section: str) -> List[Dict[str, str]]:
        """Extract work experiences from text"""
        experiences = []
        
        # Focus on experience section if available, otherwise use full text
        search_text = experience_section if experience_section else text
        
        # Look for experience patterns
        experience_patterns = [
            r'(?P<title>[A-Z][a-z]+\s+[A-Z][a-z]+\s*(?:[A-Z][a-z]+)?)\s*[-–]\s*(?P<company>.*?)(?=\n|$)',
            r'(?P<company>[A-Z][a-z]+\s+(?:Inc|Corp|LLC|Ltd)\.?)\s*\n(?P<title>.*?)(?=\n|$)',
            r'(?P<date>\d{1,2}/\d{4}\s*[-–]\s*(?:\d{1,2}/\d{4}|Present))\s*\n(?P<title>.*?)\s*[-–]\s*(?P<company>.*?)(?=\n|$)'
        ]
        
        for pattern in experience_patterns:
            matches = re.finditer(pattern, search_text, re.MULTILINE | re.IGNORECASE)
            
            for match in matches:
                experience = {
                    'title': match.group('title').strip() if 'title' in match.groupdict() else '',
                    'company': match.group('company').strip() if 'company' in match.groupdict() else '',
                    'dates': match.group('date').strip() if 'date' in match.groupdict() else '',
                    'description': self._extract_experience_description(search_text, match.start())
                }
                
                # Only add if we have meaningful content
                if experience['title'] or experience['company']:
                    experiences.append(experience)
        
        return experiences
    
    def _extract_experience_description(self, text: str, start_pos: int) -> str:
        """Extract description for an experience entry"""
        # Look for bullet points or paragraphs after the position
        description_text = text[start_pos:start_pos + 500]  # Next 500 characters
        
        # Extract bullet points
        bullet_points = re.findall(r'[•\-\*]\s*(.*?)(?=[•\-\*]|\n\n|\Z)', description_text, re.MULTILINE | re.DOTALL)
        
        if bullet_points:
            return '\n'.join([point.strip() for point in bullet_points if point.strip()])
        
        # Extract paragraphs
        paragraphs = re.findall(r'(.*?)(?=\n\n|\Z)', description_text, re.MULTILINE | re.DOTALL)
        
        if paragraphs:
            return paragraphs[0].strip() if paragraphs[0].strip() else ''
        
        return ''
    
    def _extract_skills(self, text: str, skills_section: str) -> List[str]:
        """Extract ALL skills from text - enhanced to capture 100+ skills"""
        skills = []
        
        # Focus on skills section if available
        search_text = skills_section if skills_section else text
        
        # Extract skills from bullet points and lists
        bullet_patterns = [
            r'[•·]\s*([A-Za-z][A-Za-z0-9\s\+\#\.\-\/]+)',  # Bullet point skills
            r'^\s*[-*]\s*([A-Za-z][A-Za-z0-9\s\+\#\.\-\/]+)',  # Dash/asterisk lists
            r',\s*([A-Za-z][A-Za-z0-9\s\+\#\.\-\/]+)',  # Comma-separated skills
        ]
        
        for pattern in bullet_patterns:
            matches = re.findall(pattern, search_text, re.MULTILINE)
            for match in matches:
                skill = match.strip()
                if 2 < len(skill) < 50:  # Reasonable skill length
                    skills.append(skill)
        
        # Extract common technology skills
        tech_skills = [
            'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Rust', 'Ruby', 'PHP', 'Swift', 'Kotlin',
            'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch', 'Oracle', 'SQLite',
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Terraform', 'Ansible', 'Jenkins', 'CI/CD',
            'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'Spring', 'Express', 'FastAPI',
            'Machine Learning', 'Deep Learning', 'AI', 'Data Science', 'TensorFlow', 'PyTorch', 'NLP',
            'Agile', 'Scrum', 'Kanban', 'DevOps', 'MLOps', 'SRE', 'Linux', 'Unix', 'Windows Server',
            'Git', 'GitHub', 'GitLab', 'Bitbucket', 'JIRA', 'Confluence', 'Slack', 'Microsoft Office',
            'Excel', 'PowerPoint', 'Word', 'Tableau', 'Power BI', 'Looker', 'Salesforce', 'HubSpot',
            'REST', 'GraphQL', 'API', 'Microservices', 'SOA', 'OAuth', 'JWT', 'Security', 'Cybersecurity'
        ]
        
        for skill in tech_skills:
            if skill.lower() in text.lower():
                skills.append(skill)
        
        # Extract business and soft skills
        business_skills = [
            'Leadership', 'Management', 'Strategy', 'Communication', 'Teamwork', 'Problem Solving',
            'Critical Thinking', 'Negotiation', 'Presentation', 'Public Speaking', 'Project Management',
            'Product Management', 'Business Development', 'Sales', 'Marketing', 'Analytics', 'Finance',
            'Budgeting', 'Forecasting', 'Strategic Planning', 'Operations', 'Supply Chain', 'Logistics',
            'Customer Success', 'Account Management', 'Partnership', 'Stakeholder Management',
            'Change Management', 'Process Improvement', 'Quality Assurance', 'Risk Management',
            'Compliance', 'Governance', 'Automation', 'Digital Transformation', 'Innovation'
        ]
        
        for skill in business_skills:
            if skill.lower() in text.lower():
                skills.append(skill)
        
        # Also look for certifications
        cert_patterns = [
            r'(?:certified|certification|certificate)\s+([A-Za-z\s\+\-]+)',
            r'([A-Za-z\s]+)\s+(?:certified|certification|certificate)',
            r'(AWS|Azure|GCP|PMP|CISSP|CISM|CISA|CPA|CFA|CCNA|CCNP)\s*(?:certified|certification)?'
        ]
        
        for pattern in cert_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                cert = match.strip()
                if 2 < len(cert) < 50:
                    skills.append(f"{cert} (Certified)")
        
        # Remove duplicates and common words
        common_words = {'and', 'the', 'with', 'for', 'of', 'in', 'to', 'a', 'an', 'or', 'but', 'on', 'at', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'shall', 'can'}
        skills = list(set([skill for skill in skills if skill.lower() not in common_words and len(skill) > 2]))
        
        return sorted(skills)
    
    def _extract_education(self, text: str, education_section: str) -> List[Dict[str, str]]:
        """Extract education information"""
        education = []
        
        # Focus on education section if available
        search_text = education_section if education_section else text
        
        # Education patterns
        education_patterns = [
            r'(?P<degree>[A-Z][a-z]+\s+(?:Degree|Certificate|Diploma))\s*[-–]\s*(?P<institution>.*?)(?=\n|$)',
            r'(?P<institution>.*?University|.*?College)\s*\n(?P<degree>.*?)(?=\n|$)',
            r'(?P<date>\d{4})\s*[-–]\s*(?:\d{4}|Present)\s*\n(?P<degree>.*?)\s*[-–]\s*(?P<institution>.*?)(?=\n|$)'
        ]
        
        for pattern in education_patterns:
            matches = re.finditer(pattern, search_text, re.MULTILINE | re.IGNORECASE)
            
            for match in matches:
                edu_entry = {
                    'degree': match.group('degree').strip() if 'degree' in match.groupdict() else '',
                    'institution': match.group('institution').strip() if 'institution' in match.groupdict() else '',
                    'dates': match.group('date').strip() if 'date' in match.groupdict() else ''
                }
                
                if edu_entry['degree'] or edu_entry['institution']:
                    education.append(edu_entry)
        
        return education
    
    def _extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract contact information"""
        contact = {}
        
        # Email patterns
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact['email'] = emails[0]
        
        # Phone patterns
        phone_pattern = r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b'
        phones = re.findall(phone_pattern, text)
        if phones:
            contact['phone'] = '-'.join(phones[0])
        
        # LinkedIn pattern
        linkedin_pattern = r'linkedin\.com/in/([A-Za-z0-9-]+)'
        linkedin_matches = re.findall(linkedin_pattern, text)
        if linkedin_matches:
            contact['linkedin'] = f"linkedin.com/in/{linkedin_matches[0]}"
        
        return contact
    
    def generate_profile_analysis_report(self, profile_data: PDFProfileData, target_industry: str, target_role: str) -> str:
        """Generate comprehensive profile analysis report"""
        
        report = f"""
COMPREHENSIVE PDF PROFILE ANALYSIS REPORT
=========================================

TARGET PROFILE:
• Industry: {target_industry}
• Role: {target_role}
• Processing Method: {profile_data.metadata['processing_method'].upper()}

PROFILE EXTRACTION SUMMARY:
• Total Characters: {profile_data.metadata['total_characters']}
• Word Count: {profile_data.metadata['word_count']}
• Sections Found: {', '.join(profile_data.metadata['sections_found'])}
• Experiences Identified: {profile_data.metadata['experiences_count']}
• Skills Extracted: {profile_data.metadata['skills_count']}

"""
        
        # Add detailed sections
        if profile_data.experiences:
            report += "\nEXPERIENCE SECTION ANALYSIS:\n"
            report += "-" * 40 + "\n"
            
            for i, exp in enumerate(profile_data.experiences, 1):
                report += f"\n{i}. {exp.get('title', 'Unknown Position')}\n"
                report += f"   Company: {exp.get('company', 'Unknown')}\n"
                report += f"   Dates: {exp.get('dates', 'Unknown')}\n"
                if exp.get('description'):
                    report += f"   Description: {exp['description'][:200]}{'...' if len(exp['description']) > 200 else ''}\n"
        
        if profile_data.skills:
            report += f"\n\nSKILLS ANALYSIS:\n"
            report += "-" * 20 + "\n"
            report += f"Total Skills Found: {len(profile_data.skills)}\n"
            report += f"Skills: {', '.join(profile_data.skills[:10])}{'...' if len(profile_data.skills) > 10 else ''}\n"
        
        if profile_data.education:
            report += f"\n\nEDUCATION ANALYSIS:\n"
            report += "-" * 25 + "\n"
            
            for i, edu in enumerate(profile_data.education, 1):
                report += f"\n{i}. {edu.get('degree', 'Unknown Degree')}\n"
                report += f"   Institution: {edu.get('institution', 'Unknown')}\n"
                report += f"   Dates: {edu.get('dates', 'Unknown')}\n"
        
        # Add recommendations
        report += f"\n\nOPTIMIZATION RECOMMENDATIONS:\n"
        report += "=" * 35 + "\n"
        
        if len(profile_data.experiences) < 3:
            report += "• Consider adding more detailed experience descriptions\n"
        
        if len(profile_data.skills) < 10:
            report += f"• Add more {target_industry.lower()}-specific skills (currently {len(profile_data.skills)})\n"
        
        if not profile_data.sections.get('about'):
            report += "• Add a professional summary/about section\n"
        
        report += "\n• Use this analysis to create your optimized LinkedIn profile\n"
        report += "• Focus on quantifiable achievements and impact statements\n"
        report += "• Ensure consistent formatting and professional presentation\n"
        
        return report
    
    def create_ultimate_profile_template(self, profile_data: PDFProfileData, target_industry: str, target_role: str) -> str:
        """Create the ultimate optimized profile template"""
        
        template = f"""
ULTIMATE LINKEDIN PROFILE TEMPLATE
==================================

Generated for: {target_role} in {target_industry}
Based on: PDF Profile Analysis

"""
        
        # Headline template
        template += f"""
HEADLINE TEMPLATES:
==================
1. {target_role} | {target_industry} | Driving Innovation & Growth
2. Senior {target_role} | {target_industry} Expert | 5+ Years Experience
3. {target_role} Specializing in {target_industry} Solutions | Results-Driven Professional

"""
        
        # About section template
        template += f"""
ABOUT SECTION TEMPLATE:
=======================
As a passionate {target_role} with deep expertise in the {target_industry} sector, I bring a proven track record of delivering exceptional results through innovative solutions and strategic thinking. With over [X] years of experience, I've developed comprehensive skills in [key skills from profile] and have consistently demonstrated the ability to [key achievement areas].

My professional journey has equipped me with unique insights into [industry-specific challenges], allowing me to develop effective strategies that drive measurable outcomes. I specialize in [2-3 core competencies] and have successfully [major accomplishment].

I'm particularly passionate about [industry trend or technology] and am committed to staying at the forefront of [relevant field]. My approach combines technical expertise with strong business acumen, enabling me to bridge the gap between [technical/business aspects].

I thrive in collaborative environments where I can leverage my skills in [key areas] to contribute to organizational success. I'm always open to connecting with fellow professionals who are passionate about [shared interests] and exploring opportunities where I can make a meaningful impact.

Key Strengths:
• [Strength 1 from profile]
• [Strength 2 from profile] 
• [Strength 3 from profile]
• [Industry-specific strength]

Let's connect to discuss how my expertise in {target_industry} can benefit your organization.

"""
        
        # Experience section template
        if profile_data.experiences:
            template += "\nEXPERIENCE SECTION TEMPLATES:\n"
            template += "=============================\n"
            
            for i, exp in enumerate(profile_data.experiences[:3], 1):
                template += f"""
{i}. {exp.get('title', 'Senior {target_role}')}
{exp.get('company', 'Leading {target_industry} Company')}
{exp.get('dates', '2020 - Present')}

• Spearaked [key initiative] resulting in [quantifiable outcome]
• Led team of [X] professionals to achieve [specific result]
• Implemented [strategy/technology] improving [metric] by [percentage]
• Developed [solution/process] that increased [business value] by [amount]
• Managed [budget/project] worth [amount] delivering [outcome]
• Collaborated with cross-functional teams to [achievement]
• Reduced [cost/time] by [percentage] through [optimization]
• Enhanced [process/system] leading to [improvement]

"""
        
        # Skills section template
        template += f"""
SKILLS SECTION TEMPLATE:
=======================
Technical Skills:
{', '.join(profile_data.skills[:8] if len(profile_data.skills) >= 8 else profile_data.skills)}

Industry Knowledge:
{target_industry} Trends, Market Analysis, Strategic Planning, Business Development

Soft Skills:
Leadership, Communication, Project Management, Problem Solving, Team Collaboration

Certifications:
[Relevant certifications for {target_role} in {target_industry}]

"""
        
        template += f"""
IMPLEMENTATION INSTRUCTIONS:
===========================
1. Replace bracketed [text] with your specific details
2. Quantify achievements with numbers, percentages, and dollar amounts
3. Tailor content to highlight your unique strengths and experiences
4. Ensure all sections align with {target_industry} standards
5. Review and optimize for LinkedIn's character limits and best practices

This template is designed to maximize your visibility and appeal to recruiters in the {target_industry} sector.
"""
        
        return template
