"""
Enhanced prompt templates for LinkedIn Profile Optimization Agent
"""

# Industry-specific data and templates
INDUSTRY_DATA = {
    "Technology": {
        "keywords": [
            "Agile", "Scrum", "DevOps", "CI/CD", "Cloud Computing", 
            "Microservices", "Kubernetes", "Docker", "AWS", "Azure",
            "Machine Learning", "AI", "Data Science", "Python", "JavaScript",
            "React", "Node.js", "Full-Stack", "Backend", "Frontend"
        ],
        "achievement_patterns": [
            "Reduced {metric} by {percentage}% through {technology} implementation",
            "Increased {metric} by {percentage}% using {approach}",
            "Led team of {number} engineers to deliver {project} {timeframe}",
            "Improved {process} efficiency by {percentage}%",
            "Managed budget of ${amount} for {project} initiative",
            "Scaled {system} to handle {number} concurrent users",
            "Decreased infrastructure costs by ${amount} via {optimization}",
            "Accelerated development timeline by {percentage}% with {methodology}"
        ],
        "role_specific": {
            "Software Engineer": {
                "skills": ["Python", "JavaScript", "React", "Node.js", "AWS", "Docker", "Kubernetes"],
                "metrics": ["performance", "reliability", "scalability", "user experience", "code quality"]
            },
            "Data Scientist": {
                "skills": ["Python", "R", "Machine Learning", "Statistics", "SQL", "TensorFlow", "PyTorch"],
                "metrics": ["accuracy", "insights", "predictions", "data quality", "model performance"]
            },
            "Product Manager": {
                "skills": ["Product Strategy", "Agile", "User Research", "Analytics", "Roadmapping", "Stakeholder Management"],
                "metrics": ["user engagement", "revenue", "market share", "customer satisfaction", "time to market"]
            }
        }
    },
    "Finance": {
        "keywords": [
            "Financial Analysis", "Risk Management", "Investment Banking", 
            "Portfolio Management", "M&A", "Valuation", "Financial Modeling",
            "Compliance", "Audit", "Treasury", "Capital Markets"
        ],
        "achievement_patterns": [
            "Managed portfolio of ${amount} with {return}% annual return",
            "Reduced risk exposure by {percentage}% through {strategy}",
            "Identified ${amount} in cost savings via {analysis}",
            "Led ${amount} merger/acquisition deal",
            "Improved financial reporting efficiency by {percentage}%",
            "Compliance rate of {percentage}% maintained through {system}"
        ],
        "role_specific": {
            "Financial Analyst": {
                "skills": ["Financial Modeling", "Excel", "Valuation", "Risk Analysis", "Due Diligence"],
                "metrics": ["ROI", "risk reduction", "cost savings", "accuracy", "efficiency"]
            }
        }
    },
    "Healthcare": {
        "keywords": [
            "Healthcare Management", "Clinical Operations", "Patient Care",
            "Medical Technology", "Healthcare IT", "Regulatory Compliance",
            "Quality Improvement", "Patient Safety", "Healthcare Analytics"
        ],
        "achievement_patterns": [
            "Improved patient satisfaction by {percentage}%",
            "Reduced readmission rates by {percentage}%",
            "Managed budget of ${amount} for {department}",
            "Implemented {system} serving {number} patients",
            "Achieved {percentage}% compliance rate"
        ],
        "role_specific": {
            "Healthcare Administrator": {
                "skills": ["Healthcare Management", "Budget Management", "Regulatory Compliance", "Quality Improvement"],
                "metrics": ["patient satisfaction", "cost reduction", "compliance", "efficiency", "quality scores"]
            }
        }
    }
}

# Achievement quantification templates
ACHIEVEMENT_TEMPLATES = {
    "leadership": [
        "Led team of {number} {professionals} to achieve {outcome}",
        "Managed cross-functional team of {number} across {departments}",
        "Mentored {number} team members, resulting in {result}",
        "Directed {project} initiative with budget of ${amount}"
    ],
    "technical": [
        "Developed {solution} that improved {metric} by {percentage}%",
        "Implemented {technology} reducing {issue} by {percentage}%",
        "Architected {system} serving {number} users daily",
        "Optimized {process} achieving {performance} improvement"
    ],
    "business": [
        "Generated ${amount} in revenue through {strategy}",
        "Reduced costs by ${amount} via {initiative}",
        "Increased market share by {percentage}% in {timeframe}",
        "Acquired {number} new clients worth ${amount}"
    ],
    "efficiency": [
        "Streamlined {process} reducing time by {percentage}%",
        "Automated {task} saving {hours} hours weekly",
        "Improved {metric} from {baseline} to {target}",
        "Reduced errors by {percentage}% through {method}"
    ]
}

def get_system_prompt(target_industry: str, target_role: str) -> str:
    """
    Generate the enhanced system prompt for the LinkedIn profile optimization strategist.
    
    Args:
        target_industry: The industry the user wants to target
        target_role: The specific role the user is targeting
        
    Returns:
        Complete system prompt string with industry-specific data
    """
    # Get industry-specific data
    industry_info = INDUSTRY_DATA.get(target_industry, INDUSTRY_DATA["Technology"])
    keywords = ", ".join(industry_info["keywords"][:10])  # Top 10 keywords
    role_data = industry_info["role_specific"].get(target_role, industry_info["role_specific"]["Software Engineer"])
    role_skills = ", ".join(role_data["skills"])
    role_metrics = ", ".join(role_data["metrics"])
    
    # Get achievement patterns
    patterns = industry_info["achievement_patterns"][:5]  # Top 5 patterns
    pattern_examples = "\n        ".join([f"- {pattern}" for pattern in patterns])
    
    return f"""
You are an elite LinkedIn profile optimization strategist with deep expertise in personal branding, 
recruitment, and professional networking. Your task is to analyze a LinkedIn profile and 
create a comprehensive optimization plan that improves visibility, keyword relevance, and 
personal brand impact for the {target_industry} industry, specifically targeting {target_role} roles.

🎯 INDUSTRY-SPECIFIC EXPERTISE:
Target Industry: {target_industry}
Target Role: {target_role}
Key Industry Keywords: {keywords}
Essential Skills: {role_skills}
Critical Metrics: {role_metrics}

📈 ACHIEVEMENT PATTERNS FOR {target_industry}:
Use these specific patterns for quantifying achievements:
{pattern_examples}

🚨 CRITICAL REQUIREMENTS - NON-NEGOTIABLE:
1. ANALYZE USER'S ACTUAL PROFILE DATA - Use only the real headline, about, experience, skills provided
2. ENHANCE REAL ACHIEVEMENTS - Quantify the user's actual experience with specific metrics
3. PROVIDE COMPLETE REWRITES - Give full, ready-to-use text based on their real background
4. INCLUDE SPECIFIC METRICS - Add concrete numbers to the user's actual accomplishments
5. USE INDUSTRY KEYWORDS - Naturally incorporate keywords relevant to their real experience
6. CREATE ACTIONABLE CHECKLISTS - Provide step-by-step implementation guides

🎨 CONTENT QUALITY STANDARDS:
- Every bullet point must enhance the user's REAL achievements with quantifiable results
- Use the achievement patterns provided above but apply to USER'S ACTUAL EXPERIENCE
- Include specific numbers (%, $, count, timeframe) based on their real work
- Make content sound authentic to the user's actual background, not generic
- Ensure all content is LinkedIn-optimized and professional

📋 SECTION-SPECIFIC WORKFLOWS:

1. OVERALL PROFILE REVIEW
- Analyze the user's ACTUAL current headline, about, experience, skills
- Identify the 5 biggest issues in THEIR REAL profile limiting reach and engagement
- Assess gaps in THEIR ACTUAL profile completeness and professionalism
- Evaluate keyword density in THEIR CURRENT content for {target_industry}/{target_role}
- Provide complete strategy based on THEIR REAL BACKGROUND

2. HEADLINE OPTIMIZATION  
- Analyze the user's ACTUAL current headline
- Generate 3 complete, ready-to-use headlines based on THEIR REAL experience
- Each headline must include: their actual role + their key achievement + industry keyword
- Use quantifiable results from THEIR REAL work (%, $, numbers)
- Focus on results-oriented language from THEIR ACTUAL accomplishments

3. ABOUT SECTION COMPLETE REWRITE
- Provide a complete, ready-to-use About section (300-500 words) based on THEIR REAL career
- Include storytelling elements from THEIR ACTUAL professional journey
- Add 3-5 quantified milestones from THEIR REAL experience with metrics
- Incorporate {keywords} naturally throughout THEIR ACTUAL background
- Include strong call-to-action relevant to THEIR REAL career goals
- Structure: Hook → THEIR Story → THEIR Achievements → THEIR Future Goals → CTA

4. EXPERIENCE SECTION ENHANCEMENT
- Extract ALL job descriptions from the user's ACTUAL experience
- Rewrite each of THEIR REAL experiences with 3-5 bullet points that include:
  • Specific achievement from THEIR ACTUAL work using the patterns above
  • Quantifiable results from THEIR REAL accomplishments (%, $, numbers, timeframe)
  • Industry keywords relevant to THEIR ACTUAL experience
  • Action verbs and impact-oriented language based on THEIR REAL impact
- Make each bullet point impressive but authentic to THEIR REAL background

5. SKILLS STRATEGY
- Extract ALL skills from the user's ACTUAL profile
- Add missing high-value skills for {target_role} that complement THEIR REAL experience
- Categorize THEIR ACTUAL skills: Technical, Business, Leadership
- Prioritize skills most valued by {target_industry} recruiters that match THEIR BACKGROUND

📊 FINAL OUTPUT REQUIREMENTS:
- Provide complete, ready-to-use text based on USER'S ACTUAL PROFILE
- Include at least 5 industry keywords relevant to THEIR REAL experience
- Add 3+ quantified achievements per experience based on THEIR ACTUAL work
- Create implementation checklists for each section
- Ensure all content is authentic to THEIR REAL background and personalized
- Add "Profile Update Checklist" at the end for step-by-step execution

🎯 SUCCESS METRICS:
Your output should be so impressive that:
- Recruiters immediately understand the user's ACTUAL value from THEIR REAL experience
- Profile ranks in top results for {target_role} searches based on THEIR REAL qualifications
- Content feels authentic and personal to THEIR ACTUAL background, not generic
- Every section has specific, quantified achievements from THEIR REAL work

🚨 REMEMBER: You are optimizing THE USER'S ACTUAL LINKEDIN PROFILE, not creating a generic template. 
Every recommendation must be based on and enhance THEIR REAL EXPERIENCE, SKILLS, AND BACKGROUND!"""


def get_user_content_template() -> str:
    """
    Enhanced template for formatting user content (profile data) for the strategist.
    
    Returns:
        String template for user content
    """
    return """
🎯 USER'S ACTUAL LINKEDIN PROFILE DATA - ANALYZE THIS EXACT CONTENT:

CURRENT HEADLINE:
{headline}

CURRENT ABOUT SECTION:
{about}

CURRENT EXPERIENCE:
{experience}

CURRENT SKILLS:
{skills}

TARGET INDUSTRY: {target_industry}
TARGET ROLE: {target_role}

🚨 CRITICAL INSTRUCTIONS:
1. ANALYZE THE USER'S ACTUAL CURRENT PROFILE DATA ABOVE
2. DO NOT USE TEMPLATE CONTENT - USE ONLY THE USER'S REAL DATA
3. IDENTIFY SPECIFIC GAPS IN THE USER'S CURRENT PROFILE
4. PROVIDE COMPLETE REWRITES BASED ON THEIR ACTUAL EXPERIENCE
5. ENHANCE THEIR REAL ACHIEVEMENTS WITH QUANTIFIABLE METRICS

The user wants optimization of THEIR ACTUAL PROFILE, not generic templates. 
Base all recommendations on their real experience, skills, and background.
"""


def format_profile_for_prompt(profile_data: dict, target_industry: str, target_role: str) -> str:
    """
    Format profile data into the enhanced user content template with emphasis on real data.
    
    Args:
        profile_data: Dictionary containing profile information
        target_industry: Target industry
        target_role: Target role
        
    Returns:
        Formatted string for user content
    """
    # Format experience section with emphasis on real data
    experience_text = ""
    if profile_data.get("experience"):
        for i, exp in enumerate(profile_data["experience"], 1):
            experience_text += f"EXPERIENCE {i}:\n"
            experience_text += f"  Title: {exp.get('title', 'No Title')}\n"
            experience_text += f"  Company: {exp.get('company', 'No Company')}\n"
            experience_text += f"  Dates: {exp.get('dates', 'No dates')}\n"
            experience_text += f"  Current Description: {exp.get('description', 'No description')}\n\n"
    else:
        experience_text = "NO EXPERIENCE DATA FOUND - User has not provided any experience information"
    
    # Format skills with emphasis on real data
    skills_text = ""
    if profile_data.get("skills"):
        skills_text = f"USER'S CURRENT SKILLS: {', '.join(profile_data['skills'])}"
    else:
        skills_text = "NO SKILLS DATA FOUND - User has not provided any skills information"
    
    # Format headline and about with clear labeling
    headline_text = profile_data.get("headline", "NO HEADLINE FOUND - User has not provided a headline")
    about_text = profile_data.get("about", "NO ABOUT SECTION FOUND - User has not provided an about section")
    
    return get_user_content_template().format(
        headline=headline_text,
        about=about_text,
        experience=experience_text.strip(),
        skills=skills_text,
        target_industry=target_industry,
        target_role=target_role
    )


def get_followup_prompt_template() -> str:
    """
    Template for follow-up questions and additional context.
    
    Returns:
        String template for follow-up content
    """
    return """
ADDITIONAL CONTEXT/CLARIFICATIONS:
{additional_context}

Please update your optimization recommendations based on this additional information, maintaining the same Current → Recommended → Missing → Quick Fixes format for any sections that need updates.
"""


def format_followup_content(additional_context: str) -> str:
    """
    Format follow-up content for additional questions.
    
    Args:
        additional_context: Additional context from user
        
    Returns:
        Formatted string for follow-up
    """
    return get_followup_prompt_template().format(
        additional_context=additional_context
    )
