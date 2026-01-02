"""
Perfect Profile Template Generator and Gap Analyzer

This module generates tailored "perfect profile" templates based on industry/role
and analyzes gaps between the user's current profile and the ideal profile.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import json


@dataclass
class ProfileGap:
    """Represents a gap between current and ideal profile"""
    category: str  # headline, about, experience, skills, certifications, etc.
    gap_type: str  # missing, incomplete, weak, outdated
    description: str
    priority: str  # critical, high, medium, low
    action_required: str
    effort_level: str  # quick_win, moderate, significant
    impact_score: int  # 1-10


@dataclass
class PerfectProfileSection:
    """A section of the perfect profile template"""
    section_name: str
    ideal_content: str
    benchmarks: List[str]
    must_haves: List[str]
    nice_to_haves: List[str]
    examples: List[str]


@dataclass
class PerfectProfileTemplate:
    """Complete perfect profile template for a specific industry/role"""
    industry: str
    role: str
    headline: PerfectProfileSection
    about: PerfectProfileSection
    experience: PerfectProfileSection
    skills: PerfectProfileSection
    certifications: PerfectProfileSection
    recommendations: PerfectProfileSection
    overall_score_target: int = 95


# Industry-specific perfect profile benchmarks
PERFECT_PROFILE_BENCHMARKS = {
    "Technology": {
        "Software Engineer": {
            "headline_patterns": [
                "{Role} | {Specialty} | {Tech Stack}",
                "Senior {Role} at {Company} | {Impact Statement}",
                "{Role} | Building {Product Type} | {Key Tech}"
            ],
            "headline_must_haves": ["Current role", "Key specialty", "1-2 technologies"],
            "about_structure": ["Hook statement", "Years of experience", "Key achievements (quantified)", "Technical expertise", "Passion/mission", "Call to action"],
            "about_length": "200-300 words",
            "experience_benchmarks": {
                "bullet_count": "3-5 per role",
                "quantification": "80% of bullets should have metrics",
                "action_verbs": True,
                "technologies_mentioned": True
            },
            "must_have_skills": [
                "Python", "JavaScript", "SQL", "Git", "AWS/Azure/GCP",
                "REST APIs", "Agile/Scrum", "CI/CD", "Docker"
            ],
            "recommended_certifications": [
                "AWS Solutions Architect", "Google Cloud Professional",
                "Kubernetes Administrator", "Scrum Master"
            ],
            "experience_indicators": [
                "Led/managed projects", "Reduced costs by X%", "Improved performance by X%",
                "Built systems serving X users", "Mentored X developers"
            ]
        },
        "Product Manager": {
            "headline_patterns": [
                "Product Manager | {Industry} | {Impact}",
                "Senior PM at {Company} | {Product Area}",
                "Product Leader | {Methodology} | {Outcome}"
            ],
            "headline_must_haves": ["Product Manager title", "Industry/domain", "Key achievement or focus"],
            "about_structure": ["Vision statement", "Experience summary", "Product wins", "Cross-functional leadership", "User-centric approach", "Call to action"],
            "about_length": "250-350 words",
            "experience_benchmarks": {
                "bullet_count": "4-6 per role",
                "quantification": "90% should have metrics",
                "action_verbs": True,
                "business_impact": True
            },
            "must_have_skills": [
                "Product Strategy", "Roadmap Planning", "User Research", "A/B Testing",
                "Agile/Scrum", "Data Analysis", "Stakeholder Management", "SQL"
            ],
            "recommended_certifications": [
                "Product Management Certificate", "Scrum Product Owner",
                "Google Analytics", "Design Thinking"
            ],
            "experience_indicators": [
                "Launched X products", "Grew revenue by X%", "Increased user engagement by X%",
                "Managed $X budget", "Led cross-functional team of X"
            ]
        },
        "Data Scientist": {
            "headline_patterns": [
                "Data Scientist | {Specialty} | {Industry}",
                "Senior Data Scientist | ML/AI | {Impact}",
                "Data Science Lead | {Company} | {Focus Area}"
            ],
            "headline_must_haves": ["Data Scientist title", "ML/AI specialty", "Industry or impact"],
            "about_structure": ["Impact statement", "Technical expertise", "Business value delivered", "Research/publications", "Tools mastery", "Call to action"],
            "about_length": "200-300 words",
            "experience_benchmarks": {
                "bullet_count": "3-5 per role",
                "quantification": "85% should have metrics",
                "action_verbs": True,
                "model_performance": True
            },
            "must_have_skills": [
                "Python", "Machine Learning", "Deep Learning", "SQL", "TensorFlow/PyTorch",
                "Statistics", "Data Visualization", "NLP", "Computer Vision"
            ],
            "recommended_certifications": [
                "AWS Machine Learning Specialty", "Google Professional ML Engineer",
                "TensorFlow Developer Certificate", "IBM Data Science Professional"
            ],
            "experience_indicators": [
                "Built models with X% accuracy", "Processed X TB of data",
                "Reduced prediction error by X%", "Saved $X through automation"
            ]
        },
        "Engineering Manager": {
            "headline_patterns": [
                "Engineering Manager | {Team Size} Engineers | {Company}",
                "VP Engineering | {Specialty} | {Impact}",
                "Director of Engineering | Building {Product} at {Company}"
            ],
            "headline_must_haves": ["Leadership title", "Team scope", "Company or impact"],
            "about_structure": ["Leadership philosophy", "Team achievements", "Technical background", "Scaling experience", "Culture building", "Call to action"],
            "about_length": "250-350 words",
            "experience_benchmarks": {
                "bullet_count": "4-6 per role",
                "quantification": "90% should have metrics",
                "leadership_focus": True,
                "team_growth": True
            },
            "must_have_skills": [
                "Team Leadership", "Technical Architecture", "Agile/Scrum", "Hiring",
                "Performance Management", "Strategic Planning", "Budget Management"
            ],
            "recommended_certifications": [
                "Engineering Management Certificate", "Leadership Development",
                "AWS Solutions Architect", "Scrum Master"
            ],
            "experience_indicators": [
                "Grew team from X to Y", "Delivered X projects on time",
                "Reduced attrition by X%", "Hired X engineers", "Managed $X budget"
            ]
        },
        "DevOps Engineer": {
            "headline_patterns": [
                "DevOps Engineer | {Cloud Platform} | {Specialty}",
                "Senior DevOps | CI/CD | {Impact}",
                "Site Reliability Engineer | {Company} | {Scale}"
            ],
            "headline_must_haves": ["DevOps/SRE title", "Cloud platform", "Key specialty"],
            "about_structure": ["Automation philosophy", "Infrastructure scale", "Reliability achievements", "Tool expertise", "Security focus", "Call to action"],
            "about_length": "200-300 words",
            "experience_benchmarks": {
                "bullet_count": "3-5 per role",
                "quantification": "85% should have metrics",
                "automation_focus": True,
                "uptime_metrics": True
            },
            "must_have_skills": [
                "AWS/Azure/GCP", "Kubernetes", "Docker", "Terraform", "CI/CD",
                "Linux", "Python/Bash", "Monitoring", "Security"
            ],
            "recommended_certifications": [
                "AWS DevOps Professional", "Kubernetes Administrator",
                "HashiCorp Terraform Associate", "Google Cloud DevOps Engineer"
            ],
            "experience_indicators": [
                "Achieved X% uptime", "Reduced deployment time by X%",
                "Automated X% of infrastructure", "Managed X servers/containers"
            ]
        },
        "CTO": {
            "headline_patterns": [
                "CTO | {Company} | {Industry Focus}",
                "Chief Technology Officer | Scaling {Product Type}",
                "CTO & Co-Founder | {Mission Statement}"
            ],
            "headline_must_haves": ["CTO title", "Company or scope", "Strategic focus"],
            "about_structure": ["Vision statement", "Track record", "Technical leadership", "Business impact", "Innovation focus", "Board/advisory roles"],
            "about_length": "300-400 words",
            "experience_benchmarks": {
                "bullet_count": "4-6 per role",
                "quantification": "95% should have metrics",
                "strategic_focus": True,
                "business_outcomes": True
            },
            "must_have_skills": [
                "Technical Strategy", "Team Building", "Architecture", "Fundraising",
                "Board Presentations", "Vendor Management", "Security", "Compliance"
            ],
            "recommended_certifications": [
                "Executive Leadership Program", "AWS Solutions Architect Professional",
                "CISSP", "Board Governance"
            ],
            "experience_indicators": [
                "Scaled engineering from X to Y", "Raised $X funding",
                "Launched X products", "Achieved $X ARR", "Led M&A technical due diligence"
            ]
        },
        "CSO": {
            "headline_patterns": [
                "CSO | {Company} | {Strategic Focus}",
                "Chief Strategy Officer | {Industry} | {Transformation Focus}",
                "CSO & Technology Innovator | {Impact Statement}"
            ],
            "headline_must_haves": ["CSO/Strategy title", "Industry or company", "Strategic impact"],
            "about_structure": ["Strategic vision", "Transformation track record", "Cross-functional leadership", "Market capture achievements", "Innovation philosophy", "Advisory/board roles"],
            "about_length": "300-400 words",
            "experience_benchmarks": {
                "bullet_count": "4-6 per role",
                "quantification": "95% should have metrics",
                "strategic_outcomes": True,
                "market_impact": True
            },
            "must_have_skills": [
                "Strategic Planning", "Market Analysis", "Business Development", "M&A",
                "Digital Transformation", "Automation", "Sales Strategy", "Operations"
            ],
            "recommended_certifications": [
                "Executive Strategy Program", "Digital Transformation Certificate",
                "Six Sigma Black Belt", "Change Management"
            ],
            "experience_indicators": [
                "Drove X% revenue growth", "Captured X market share",
                "Led $X digital transformation", "Optimized operations saving $X"
            ]
        }
    },
    "Finance": {
        "Financial Analyst": {
            "headline_patterns": [
                "Financial Analyst | {Specialty} | {Company}",
                "Senior Financial Analyst | FP&A | {Industry}",
                "Finance Professional | {Certification} | {Focus}"
            ],
            "headline_must_haves": ["Analyst title", "Specialty area", "Certification if applicable"],
            "about_structure": ["Financial expertise", "Analytical achievements", "Tool proficiency", "Industry knowledge", "Value delivered", "Call to action"],
            "about_length": "200-300 words",
            "experience_benchmarks": {
                "bullet_count": "3-5 per role",
                "quantification": "90% should have metrics",
                "financial_impact": True
            },
            "must_have_skills": [
                "Financial Modeling", "Excel", "SQL", "Tableau/Power BI", "FP&A",
                "Budgeting", "Forecasting", "Variance Analysis", "ERP Systems"
            ],
            "recommended_certifications": [
                "CFA", "CPA", "Financial Modeling Certification",
                "Excel Expert", "Tableau Certification"
            ],
            "experience_indicators": [
                "Managed $X budget", "Improved forecast accuracy by X%",
                "Identified $X in cost savings", "Built models used by X stakeholders"
            ]
        },
        "Investment Banker": {
            "headline_patterns": [
                "Investment Banker | {Coverage Area} | {Bank}",
                "VP Investment Banking | M&A | {Industry}",
                "Investment Banking Associate | {Specialty}"
            ],
            "headline_must_haves": ["IB title", "Coverage/product area", "Bank or deal experience"],
            "about_structure": ["Deal experience", "Industry expertise", "Analytical skills", "Client relationships", "Transaction highlights", "Call to action"],
            "about_length": "250-350 words",
            "experience_benchmarks": {
                "bullet_count": "4-6 per role",
                "quantification": "95% should have deal values",
                "transaction_focus": True
            },
            "must_have_skills": [
                "Financial Modeling", "Valuation", "M&A", "DCF Analysis", "LBO Modeling",
                "Pitch Books", "Due Diligence", "Client Management", "Capital Markets"
            ],
            "recommended_certifications": [
                "CFA", "Series 79", "Financial Modeling Certificate",
                "M&A Certificate"
            ],
            "experience_indicators": [
                "Executed $X in transactions", "Advised on X deals",
                "Built models for $X deals", "Managed X client relationships"
            ]
        }
    },
    "Healthcare": {
        "Healthcare Administrator": {
            "headline_patterns": [
                "Healthcare Administrator | {Facility Type} | {Focus}",
                "Hospital Administrator | {Specialty} | {Impact}",
                "Healthcare Executive | {Organization} | {Achievements}"
            ],
            "headline_must_haves": ["Administrator title", "Healthcare setting", "Key focus area"],
            "about_structure": ["Healthcare mission", "Operational achievements", "Patient outcomes", "Team leadership", "Regulatory expertise", "Call to action"],
            "about_length": "250-350 words",
            "experience_benchmarks": {
                "bullet_count": "4-6 per role",
                "quantification": "85% should have metrics",
                "patient_focus": True,
                "operational_excellence": True
            },
            "must_have_skills": [
                "Healthcare Operations", "Budget Management", "Regulatory Compliance",
                "Quality Improvement", "Staff Management", "EHR Systems", "Patient Safety"
            ],
            "recommended_certifications": [
                "FACHE", "Lean Six Sigma Healthcare", "Healthcare Compliance",
                "Project Management Professional"
            ],
            "experience_indicators": [
                "Managed X-bed facility", "Improved patient satisfaction by X%",
                "Reduced costs by $X", "Led team of X healthcare professionals"
            ]
        }
    },
    "Marketing": {
        "Marketing Manager": {
            "headline_patterns": [
                "Marketing Manager | {Specialty} | {Industry}",
                "Digital Marketing Manager | {Channel} | {Impact}",
                "Senior Marketing Manager | {Brand} | {Achievements}"
            ],
            "headline_must_haves": ["Marketing title", "Specialty area", "Results or industry"],
            "about_structure": ["Marketing philosophy", "Campaign highlights", "Channel expertise", "Data-driven approach", "Brand building", "Call to action"],
            "about_length": "200-300 words",
            "experience_benchmarks": {
                "bullet_count": "4-5 per role",
                "quantification": "90% should have metrics",
                "campaign_focus": True,
                "roi_metrics": True
            },
            "must_have_skills": [
                "Digital Marketing", "SEO/SEM", "Content Marketing", "Social Media",
                "Marketing Analytics", "Campaign Management", "Brand Strategy", "CRM"
            ],
            "recommended_certifications": [
                "Google Analytics", "HubSpot Marketing", "Facebook Blueprint",
                "Content Marketing Institute"
            ],
            "experience_indicators": [
                "Generated X leads", "Achieved X% conversion rate",
                "Grew social following by X%", "Managed $X marketing budget"
            ]
        }
    },
    "Sales": {
        "Sales Manager": {
            "headline_patterns": [
                "Sales Manager | {Industry} | {Quota Achievement}",
                "Regional Sales Director | {Territory} | {Revenue}",
                "VP Sales | {Company} | {Growth Metrics}"
            ],
            "headline_must_haves": ["Sales title", "Industry or territory", "Revenue/quota metrics"],
            "about_structure": ["Sales philosophy", "Revenue achievements", "Team leadership", "Client relationships", "Sales methodology", "Call to action"],
            "about_length": "200-300 words",
            "experience_benchmarks": {
                "bullet_count": "4-5 per role",
                "quantification": "95% should have revenue metrics",
                "quota_achievement": True,
                "team_performance": True
            },
            "must_have_skills": [
                "Sales Strategy", "Account Management", "Negotiation", "CRM (Salesforce)",
                "Pipeline Management", "Forecasting", "Team Leadership", "Enterprise Sales"
            ],
            "recommended_certifications": [
                "Salesforce Administrator", "Sandler Sales Training",
                "Miller Heiman Strategic Selling", "SPIN Selling"
            ],
            "experience_indicators": [
                "Exceeded quota by X%", "Generated $X in revenue",
                "Grew territory by X%", "Led team achieving $X"
            ]
        }
    },
    "Operations": {
        "Operations Manager": {
            "headline_patterns": [
                "Operations Manager | {Industry} | {Efficiency Gains}",
                "Director of Operations | {Company} | {Scale}",
                "VP Operations | {Focus Area} | {Impact}"
            ],
            "headline_must_haves": ["Operations title", "Industry", "Key achievement"],
            "about_structure": ["Operations philosophy", "Efficiency achievements", "Process improvement", "Team leadership", "Technology adoption", "Call to action"],
            "about_length": "200-300 words",
            "experience_benchmarks": {
                "bullet_count": "4-5 per role",
                "quantification": "90% should have metrics",
                "efficiency_focus": True,
                "cost_savings": True
            },
            "must_have_skills": [
                "Process Improvement", "Lean/Six Sigma", "Supply Chain", "Budget Management",
                "Team Leadership", "Vendor Management", "ERP Systems", "Quality Control"
            ],
            "recommended_certifications": [
                "Six Sigma Black Belt", "PMP", "Lean Certification",
                "Supply Chain Management"
            ],
            "experience_indicators": [
                "Reduced costs by X%", "Improved efficiency by X%",
                "Managed operations with $X budget", "Led team of X"
            ]
        }
    }
}


class ProfileGapAnalyzer:
    """Analyzes gaps between current profile and perfect profile template"""
    
    def __init__(self):
        self.benchmarks = PERFECT_PROFILE_BENCHMARKS
    
    def get_perfect_profile_template(
        self, 
        industry: str, 
        role: str,
        current_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate a perfect profile template tailored to the user's industry and role.
        """
        # Get industry benchmarks or default to Technology
        industry_benchmarks = self.benchmarks.get(industry, self.benchmarks.get("Technology", {}))
        
        # Find the closest matching role or use a default
        role_benchmarks = self._find_best_role_match(role, industry_benchmarks)
        
        if not role_benchmarks:
            # Create generic benchmarks based on the role
            role_benchmarks = self._create_generic_benchmarks(role, industry)
        
        # Generate the perfect profile template
        perfect_template = self._generate_perfect_template(
            industry, role, role_benchmarks, current_profile
        )
        
        return perfect_template
    
    def analyze_gaps(
        self, 
        current_profile: Dict[str, Any],
        industry: str,
        role: str
    ) -> Dict[str, Any]:
        """
        Analyze gaps between current profile and perfect profile.
        Returns detailed gap analysis with prioritized recommendations.
        """
        perfect_template = self.get_perfect_profile_template(industry, role, current_profile)
        
        gaps = []
        
        # Analyze headline gaps
        headline_gaps = self._analyze_headline_gaps(
            current_profile.get('headline', ''),
            perfect_template.get('headline', {}),
            role
        )
        gaps.extend(headline_gaps)
        
        # Analyze about section gaps
        about_gaps = self._analyze_about_gaps(
            current_profile.get('about', ''),
            perfect_template.get('about', {})
        )
        gaps.extend(about_gaps)
        
        # Analyze experience gaps
        experience_gaps = self._analyze_experience_gaps(
            current_profile.get('experience', []),
            perfect_template.get('experience', {})
        )
        gaps.extend(experience_gaps)
        
        # Analyze skills gaps
        skills_gaps = self._analyze_skills_gaps(
            current_profile.get('skills', []),
            perfect_template.get('skills', {})
        )
        gaps.extend(skills_gaps)
        
        # Analyze certification gaps
        cert_gaps = self._analyze_certification_gaps(
            current_profile.get('skills', []),  # Certs often listed in skills
            current_profile.get('about', ''),
            perfect_template.get('certifications', {})
        )
        gaps.extend(cert_gaps)
        
        # Sort gaps by priority and impact
        sorted_gaps = self._prioritize_gaps(gaps)
        
        # Calculate profile completeness score
        completeness_score = self._calculate_completeness_score(gaps)
        
        return {
            'perfect_template': perfect_template,
            'gaps': sorted_gaps,
            'completeness_score': completeness_score,
            'quick_wins': [g for g in sorted_gaps if g['effort_level'] == 'quick_win'][:5],
            'high_impact': [g for g in sorted_gaps if g['priority'] in ['critical', 'high']][:5],
            'missing_to_perfect': self._get_missing_to_perfect(sorted_gaps),
            'roadmap': self._generate_improvement_roadmap(sorted_gaps)
        }
    
    def _find_best_role_match(self, role: str, industry_benchmarks: Dict) -> Optional[Dict]:
        """Find the best matching role in benchmarks"""
        role_lower = role.lower()
        
        # Direct match
        for benchmark_role, benchmarks in industry_benchmarks.items():
            if benchmark_role.lower() == role_lower:
                return benchmarks
        
        # Partial match
        for benchmark_role, benchmarks in industry_benchmarks.items():
            if any(word in role_lower for word in benchmark_role.lower().split()):
                return benchmarks
        
        # Keywords match
        role_keywords = {
            'engineer': 'Software Engineer',
            'developer': 'Software Engineer',
            'product': 'Product Manager',
            'data': 'Data Scientist',
            'devops': 'DevOps Engineer',
            'sre': 'DevOps Engineer',
            'manager': 'Engineering Manager',
            'director': 'Engineering Manager',
            'vp': 'Engineering Manager',
            'cto': 'CTO',
            'cso': 'CSO',
            'chief': 'CTO'
        }
        
        for keyword, mapped_role in role_keywords.items():
            if keyword in role_lower:
                return industry_benchmarks.get(mapped_role)
        
        return None
    
    def _create_generic_benchmarks(self, role: str, industry: str) -> Dict:
        """Create generic benchmarks for roles not in our database"""
        return {
            "headline_patterns": [
                f"{role} | {{Specialty}} | {{Company}}",
                f"Senior {role} | {{Industry}} | {{Impact}}",
                f"{role} | {{Key Achievement}}"
            ],
            "headline_must_haves": ["Current title", "Industry/specialty", "Key differentiator"],
            "about_structure": ["Hook statement", "Experience summary", "Key achievements", "Expertise areas", "Call to action"],
            "about_length": "200-300 words",
            "experience_benchmarks": {
                "bullet_count": "3-5 per role",
                "quantification": "80% should have metrics",
                "action_verbs": True
            },
            "must_have_skills": [],
            "recommended_certifications": [],
            "experience_indicators": [
                "Led/managed X", "Improved X by Y%", "Delivered X projects", "Generated $X"
            ]
        }
    
    def _generate_perfect_template(
        self, 
        industry: str, 
        role: str, 
        benchmarks: Dict,
        current_profile: Dict
    ) -> Dict[str, Any]:
        """Generate the perfect profile template"""
        
        # Get user's name for personalization
        current_headline = current_profile.get('headline', '')
        user_name = current_profile.get('name', 'Professional')
        
        return {
            'headline': {
                'ideal_template': benchmarks.get('headline_patterns', [])[0] if benchmarks.get('headline_patterns') else f"{role} | [Specialty] | [Impact]",
                'patterns': benchmarks.get('headline_patterns', []),
                'must_haves': benchmarks.get('headline_must_haves', []),
                'example': f"{role} | {industry} Expert | Driving Innovation & Growth",
                'max_length': 220
            },
            'about': {
                'structure': benchmarks.get('about_structure', []),
                'ideal_length': benchmarks.get('about_length', '200-300 words'),
                'must_include': [
                    "Quantified achievements",
                    "Years of experience",
                    "Key expertise areas",
                    "Call to action"
                ],
                'example_hooks': [
                    f"Passionate {role} with X+ years driving {industry.lower()} innovation.",
                    f"Results-driven {role} transforming businesses through strategic execution.",
                    f"{industry} leader specializing in [specialty] with proven track record."
                ]
            },
            'experience': {
                'benchmarks': benchmarks.get('experience_benchmarks', {}),
                'ideal_indicators': benchmarks.get('experience_indicators', []),
                'must_haves': [
                    "3-5 bullet points per role",
                    "80%+ bullets with quantified metrics",
                    "Strong action verbs",
                    "Clear impact statements"
                ],
                'action_verbs': [
                    "Led", "Delivered", "Transformed", "Optimized", "Launched",
                    "Grew", "Reduced", "Improved", "Built", "Managed",
                    "Spearheaded", "Architected", "Pioneered", "Streamlined"
                ]
            },
            'skills': {
                'must_have': benchmarks.get('must_have_skills', []),
                'recommended_count': '50-100 skills',
                'categories': [
                    "Technical/Hard Skills",
                    "Leadership/Soft Skills", 
                    "Tools & Technologies",
                    "Industry-Specific Skills"
                ]
            },
            'certifications': {
                'recommended': benchmarks.get('recommended_certifications', []),
                'ideal_count': '3-5 relevant certifications',
                'priority_order': [
                    "Industry-recognized certifications",
                    "Technology-specific certifications",
                    "Leadership/management certifications"
                ]
            },
            'recommendations': {
                'ideal_count': '5-10 recommendations',
                'should_include': [
                    "From direct managers",
                    "From cross-functional partners",
                    "From direct reports (if applicable)",
                    "From clients/customers"
                ]
            },
            'overall': {
                'target_score': 95,
                'key_differentiators': [
                    f"Clear positioning as {role} in {industry}",
                    "Quantified achievements throughout",
                    "Complete skills inventory",
                    "Relevant certifications",
                    "Strong recommendations"
                ]
            }
        }
    
    def _analyze_headline_gaps(self, current: str, ideal: Dict, role: str) -> List[Dict]:
        """Analyze gaps in headline"""
        gaps = []
        
        if not current:
            gaps.append({
                'category': 'headline',
                'gap_type': 'missing',
                'description': 'No headline found',
                'priority': 'critical',
                'action_required': f'Add a compelling headline like: "{role} | [Specialty] | [Key Achievement]"',
                'effort_level': 'quick_win',
                'impact_score': 10
            })
            return gaps
        
        # Check for key components
        must_haves = ideal.get('must_haves', [])
        
        if '|' not in current:
            gaps.append({
                'category': 'headline',
                'gap_type': 'incomplete',
                'description': 'Headline lacks structure (use | to separate key elements)',
                'priority': 'high',
                'action_required': 'Restructure headline with format: "Role | Specialty | Achievement"',
                'effort_level': 'quick_win',
                'impact_score': 8
            })
        
        if len(current) < 50:
            gaps.append({
                'category': 'headline',
                'gap_type': 'weak',
                'description': f'Headline is too short ({len(current)} chars). Ideal: 100-200 characters',
                'priority': 'medium',
                'action_required': 'Expand headline with more specific details about your expertise and impact',
                'effort_level': 'quick_win',
                'impact_score': 6
            })
        
        # Check for quantification
        if not any(char.isdigit() for char in current):
            gaps.append({
                'category': 'headline',
                'gap_type': 'incomplete',
                'description': 'Headline lacks quantification (e.g., years of experience, team size)',
                'priority': 'medium',
                'action_required': 'Add a metric to your headline (e.g., "10+ Years Experience" or "Leading Team of 20+")',
                'effort_level': 'quick_win',
                'impact_score': 5
            })
        
        return gaps
    
    def _analyze_about_gaps(self, current: str, ideal: Dict) -> List[Dict]:
        """Analyze gaps in about section"""
        gaps = []
        
        if not current:
            gaps.append({
                'category': 'about',
                'gap_type': 'missing',
                'description': 'No about section found',
                'priority': 'critical',
                'action_required': 'Write a compelling 200-300 word about section highlighting your expertise and achievements',
                'effort_level': 'moderate',
                'impact_score': 10
            })
            return gaps
        
        word_count = len(current.split())
        
        if word_count < 100:
            gaps.append({
                'category': 'about',
                'gap_type': 'weak',
                'description': f'About section too short ({word_count} words). Ideal: 200-300 words',
                'priority': 'high',
                'action_required': 'Expand your about section with more details about achievements, expertise, and value proposition',
                'effort_level': 'moderate',
                'impact_score': 8
            })
        
        # Check for quantification
        if not any(char.isdigit() for char in current):
            gaps.append({
                'category': 'about',
                'gap_type': 'incomplete',
                'description': 'About section lacks quantified achievements',
                'priority': 'high',
                'action_required': 'Add specific metrics (e.g., "increased revenue by 40%", "led team of 15")',
                'effort_level': 'moderate',
                'impact_score': 9
            })
        
        # Check for call to action
        cta_keywords = ['connect', 'reach out', 'contact', 'discuss', 'collaborate', 'email', 'message']
        if not any(keyword in current.lower() for keyword in cta_keywords):
            gaps.append({
                'category': 'about',
                'gap_type': 'incomplete',
                'description': 'About section lacks call to action',
                'priority': 'medium',
                'action_required': 'Add a call to action at the end (e.g., "Let\'s connect to discuss...")',
                'effort_level': 'quick_win',
                'impact_score': 5
            })
        
        return gaps
    
    def _analyze_experience_gaps(self, experiences: List, ideal: Dict) -> List[Dict]:
        """Analyze gaps in experience section"""
        gaps = []
        
        if not experiences:
            gaps.append({
                'category': 'experience',
                'gap_type': 'missing',
                'description': 'No experience entries found',
                'priority': 'critical',
                'action_required': 'Add your work experience with detailed descriptions and achievements',
                'effort_level': 'significant',
                'impact_score': 10
            })
            return gaps
        
        # Check each experience entry
        for i, exp in enumerate(experiences):
            if hasattr(exp, 'description'):
                description = exp.description
                title = exp.title
            else:
                description = exp.get('description', '')
                title = exp.get('title', f'Position {i+1}')
            
            if not description or len(description) < 50:
                gaps.append({
                    'category': 'experience',
                    'gap_type': 'incomplete',
                    'description': f'Experience "{title}" lacks detailed description',
                    'priority': 'high',
                    'action_required': f'Add 3-5 bullet points with achievements for "{title}"',
                    'effort_level': 'moderate',
                    'impact_score': 8
                })
            elif not any(char.isdigit() for char in description):
                gaps.append({
                    'category': 'experience',
                    'gap_type': 'weak',
                    'description': f'Experience "{title}" lacks quantified achievements',
                    'priority': 'high',
                    'action_required': f'Add metrics to "{title}" (e.g., percentages, dollar amounts, team sizes)',
                    'effort_level': 'moderate',
                    'impact_score': 7
                })
        
        return gaps
    
    def _analyze_skills_gaps(self, current_skills: List, ideal: Dict) -> List[Dict]:
        """Analyze gaps in skills"""
        gaps = []
        
        skills_count = len(current_skills)
        
        if skills_count < 20:
            gaps.append({
                'category': 'skills',
                'gap_type': 'incomplete',
                'description': f'Only {skills_count} skills listed. Ideal: 50-100 skills',
                'priority': 'high',
                'action_required': 'Add more skills including technical, soft skills, and tools',
                'effort_level': 'quick_win',
                'impact_score': 7
            })
        elif skills_count < 50:
            gaps.append({
                'category': 'skills',
                'gap_type': 'weak',
                'description': f'{skills_count} skills listed. Consider adding more for better visibility',
                'priority': 'medium',
                'action_required': 'Add industry-specific and emerging technology skills',
                'effort_level': 'quick_win',
                'impact_score': 5
            })
        
        # Check for must-have skills
        must_have = ideal.get('must_have', [])
        current_skills_lower = [s.lower() for s in current_skills]
        
        missing_critical = []
        for skill in must_have:
            if skill.lower() not in current_skills_lower:
                missing_critical.append(skill)
        
        if missing_critical:
            gaps.append({
                'category': 'skills',
                'gap_type': 'missing',
                'description': f'Missing critical skills: {", ".join(missing_critical[:5])}',
                'priority': 'high',
                'action_required': f'Add these must-have skills: {", ".join(missing_critical)}',
                'effort_level': 'quick_win',
                'impact_score': 8
            })
        
        return gaps
    
    def _analyze_certification_gaps(self, skills: List, about: str, ideal: Dict) -> List[Dict]:
        """Analyze gaps in certifications"""
        gaps = []
        
        # Check for certifications in skills or about
        combined_text = ' '.join(skills) + ' ' + about
        combined_lower = combined_text.lower()
        
        cert_keywords = ['certified', 'certification', 'certificate', 'cfa', 'cpa', 'pmp', 'aws', 'azure', 'gcp']
        has_certs = any(keyword in combined_lower for keyword in cert_keywords)
        
        if not has_certs:
            recommended = ideal.get('recommended', [])
            gaps.append({
                'category': 'certifications',
                'gap_type': 'missing',
                'description': 'No certifications detected in profile',
                'priority': 'medium',
                'action_required': f'Consider obtaining: {", ".join(recommended[:3])}' if recommended else 'Add relevant industry certifications',
                'effort_level': 'significant',
                'impact_score': 6
            })
        
        return gaps
    
    def _prioritize_gaps(self, gaps: List[Dict]) -> List[Dict]:
        """Sort gaps by priority and impact"""
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        
        return sorted(gaps, key=lambda x: (
            priority_order.get(x['priority'], 4),
            -x['impact_score']
        ))
    
    def _calculate_completeness_score(self, gaps: List[Dict]) -> int:
        """Calculate profile completeness score (0-100)"""
        if not gaps:
            return 95
        
        total_impact = sum(g['impact_score'] for g in gaps)
        max_impact = len(gaps) * 10
        
        if max_impact == 0:
            return 95
        
        deduction = min(50, int((total_impact / max_impact) * 50))
        return max(30, 95 - deduction)
    
    def _get_missing_to_perfect(self, gaps: List[Dict]) -> Dict[str, List[str]]:
        """Get categorized list of what's missing for a perfect profile"""
        missing = {
            'headline': [],
            'about': [],
            'experience': [],
            'skills': [],
            'certifications': []
        }
        
        for gap in gaps:
            category = gap['category']
            if category in missing:
                missing[category].append(gap['action_required'])
        
        return missing
    
    def _generate_improvement_roadmap(self, gaps: List[Dict]) -> List[Dict]:
        """Generate a prioritized improvement roadmap"""
        roadmap = []
        
        # Phase 1: Quick Wins (1-2 hours)
        quick_wins = [g for g in gaps if g['effort_level'] == 'quick_win']
        if quick_wins:
            roadmap.append({
                'phase': 'Phase 1: Quick Wins',
                'timeframe': '1-2 hours',
                'actions': [g['action_required'] for g in quick_wins[:5]],
                'expected_impact': 'Immediate visibility improvement'
            })
        
        # Phase 2: Moderate Effort (1-2 days)
        moderate = [g for g in gaps if g['effort_level'] == 'moderate']
        if moderate:
            roadmap.append({
                'phase': 'Phase 2: Content Enhancement',
                'timeframe': '1-2 days',
                'actions': [g['action_required'] for g in moderate[:5]],
                'expected_impact': 'Significant profile strength increase'
            })
        
        # Phase 3: Significant Effort (1-4 weeks)
        significant = [g for g in gaps if g['effort_level'] == 'significant']
        if significant:
            roadmap.append({
                'phase': 'Phase 3: Long-term Development',
                'timeframe': '1-4 weeks',
                'actions': [g['action_required'] for g in significant[:5]],
                'expected_impact': 'Complete profile transformation'
            })
        
        return roadmap


def generate_perfect_profile_report(
    current_profile: Dict[str, Any],
    industry: str,
    role: str
) -> str:
    """Generate a comprehensive perfect profile report"""
    analyzer = ProfileGapAnalyzer()
    analysis = analyzer.analyze_gaps(current_profile, industry, role)
    
    report = []
    report.append("# 🎯 PERFECT PROFILE ANALYSIS REPORT")
    report.append("=" * 60)
    report.append("")
    
    # Completeness Score
    score = analysis['completeness_score']
    report.append(f"## 📊 Profile Completeness Score: {score}/100")
    if score >= 90:
        report.append("🌟 Excellent! Your profile is nearly perfect.")
    elif score >= 70:
        report.append("✅ Good foundation. Some improvements needed.")
    elif score >= 50:
        report.append("⚠️ Needs work. Several gaps to address.")
    else:
        report.append("🚨 Significant improvements required.")
    report.append("")
    
    # Perfect Profile Template
    template = analysis['perfect_template']
    report.append("## 🏆 YOUR PERFECT PROFILE TEMPLATE")
    report.append("-" * 40)
    report.append("")
    
    report.append("### 📝 Ideal Headline")
    report.append(f"**Template:** {template['headline']['ideal_template']}")
    report.append(f"**Example:** {template['headline']['example']}")
    report.append("**Must Include:**")
    for item in template['headline']['must_haves']:
        report.append(f"  • {item}")
    report.append("")
    
    report.append("### 📄 Ideal About Section")
    report.append(f"**Ideal Length:** {template['about']['ideal_length']}")
    report.append("**Structure:**")
    for i, item in enumerate(template['about']['structure'], 1):
        report.append(f"  {i}. {item}")
    report.append("")
    
    report.append("### 💼 Ideal Experience")
    for item in template['experience']['must_haves']:
        report.append(f"  • {item}")
    report.append("**Power Action Verbs:**")
    report.append(f"  {', '.join(template['experience']['action_verbs'][:10])}")
    report.append("")
    
    report.append("### 🎯 Must-Have Skills")
    if template['skills']['must_have']:
        report.append(f"  {', '.join(template['skills']['must_have'])}")
    report.append("")
    
    report.append("### 📜 Recommended Certifications")
    if template['certifications']['recommended']:
        for cert in template['certifications']['recommended']:
            report.append(f"  • {cert}")
    report.append("")
    
    # Gap Analysis
    report.append("## 🔍 GAP ANALYSIS: What's Missing")
    report.append("-" * 40)
    
    missing = analysis['missing_to_perfect']
    for category, items in missing.items():
        if items:
            report.append(f"\n### {category.upper()}")
            for item in items:
                report.append(f"  ❌ {item}")
    report.append("")
    
    # Quick Wins
    if analysis['quick_wins']:
        report.append("## ⚡ QUICK WINS (Do These First!)")
        report.append("-" * 40)
        for i, gap in enumerate(analysis['quick_wins'], 1):
            report.append(f"{i}. {gap['action_required']}")
        report.append("")
    
    # Improvement Roadmap
    report.append("## 🗺️ IMPROVEMENT ROADMAP")
    report.append("-" * 40)
    for phase in analysis['roadmap']:
        report.append(f"\n### {phase['phase']} ({phase['timeframe']})")
        report.append(f"**Expected Impact:** {phase['expected_impact']}")
        for action in phase['actions']:
            report.append(f"  • {action}")
    report.append("")
    
    return "\n".join(report)
