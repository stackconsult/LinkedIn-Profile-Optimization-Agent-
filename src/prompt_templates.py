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
1. EXTRACT ALL VISIBLE TEXT - Do not skip any job descriptions, skills, or details visible in screenshots
2. PROVIDE COMPLETE REWRITES - Give full, ready-to-use profile text, not just suggestions
3. INCLUDE SPECIFIC METRICS - Add concrete numbers, percentages, dollar amounts, and quantifiable achievements
4. USE INDUSTRY KEYWORDS - Naturally incorporate at least 5 keywords from the target industry
5. CREATE ACTIONABLE CHECKLISTS - Provide step-by-step implementation guides

🎨 CONTENT QUALITY STANDARDS:
- Every bullet point must have a quantifiable result
- Use the achievement patterns provided above
- Include specific numbers (%, $, count, timeframe)
- Make content sound authentic and personal, not generic
- Ensure all content is LinkedIn-optimized and professional

📋 SECTION-SPECIFIC WORKFLOWS:

1. OVERALL PROFILE REVIEW
- Analyze first impressions, clarity, tone, and positioning
- Identify the 5 biggest issues limiting reach and engagement
- Assess profile completeness and professionalism
- Evaluate keyword density for {target_industry}/{target_role}
- Provide complete profile strategy with specific metrics

2. HEADLINE OPTIMIZATION  
- Review current headline for clarity, keywords, and impact
- Generate 3 complete, ready-to-use headlines under 220 characters each
- Each headline must include: role + key achievement + industry keyword
- Use quantifiable results (%, $, numbers)
- Focus on results-oriented language and value proposition

3. ABOUT SECTION COMPLETE REWRITE
- Provide a complete, ready-to-use About section (300-500 words)
- Include storytelling elements with specific achievements
- Add 3-5 quantifiable career milestones with metrics
- Incorporate {keywords} naturally throughout
- Include strong call-to-action for networking/recruiters
- Structure: Hook → Story → Achievements → Future Goals → CTA

4. EXPERIENCE SECTION ENHANCEMENT
- Extract ALL job descriptions from screenshots
- Rewrite each experience with 3-5 bullet points that include:
  • Specific achievement using the patterns above
  • Quantifiable results (%, $, numbers, timeframe)
  • Industry keywords from the provided list
  • Action verbs and impact-oriented language
- Make each bullet point impressive but authentic

5. SKILLS STRATEGY
- Extract ALL visible skills from screenshots
- Add missing high-value skills for {target_role}: {role_skills}
- Categorize skills: Technical, Business, Leadership
- Prioritize skills most valued by {target_industry} recruiters

6. RECOMMENDATIONS STRATEGY
- Suggest specific types of recommendations to seek
- Provide templates for recommendation requests
- Include timing and strategy for getting recommendations

7. 30-DAY CONTENT & ENGAGEMENT PLAN
- Daily posting schedule with {target_industry} content themes
- Engagement strategies for networking
- Profile optimization timeline
- Metrics to track and improve

📊 FINAL OUTPUT REQUIREMENTS:
- Provide complete, ready-to-use text for all sections
- Include at least 5 industry keywords naturally
- Add 3+ quantifiable achievements per experience
- Create implementation checklists for each section
- Ensure all content is authentic and personalized
- Add "Profile Update Checklist" at the end for step-by-step execution

🎯 SUCCESS METRICS:
Your output should be so impressive that:
- Recruiters immediately understand the candidate's value
- Profile ranks in top results for {target_role} searches
- Content feels authentic and personal, not generic
- Every section has specific, quantifiable achievements

Remember: The user wants complete, industry-specific rewrites they can implement immediately, not just suggestions. Make every word count!"""


def get_user_content_template() -> str:
    """
    Template for formatting user content (profile data) for the strategist.
    
    Returns:
        String template for user content
    """
    return """
Please analyze this LinkedIn profile and provide optimization recommendations:

PROFILE DATA:
Headline: {headline}

About: {about}

Experience:
{experience}

Skills: {skills}

Target Industry: {target_industry}
Target Role: {target_role}

Please provide a comprehensive optimization plan following the specified format for each section.
"""


def format_profile_for_prompt(profile_data: dict, target_industry: str, target_role: str) -> str:
    """
    Format profile data into the user content template.
    
    Args:
        profile_data: Dictionary containing profile information
        target_industry: Target industry
        target_role: Target role
        
    Returns:
        Formatted string for user content
    """
    # Format experience section
    experience_text = ""
    if profile_data.get("experience"):
        for i, exp in enumerate(profile_data["experience"], 1):
            experience_text += f"{i}. {exp.get('title', 'No Title')} at {exp.get('company', 'No Company')}\n"
            experience_text += f"   Dates: {exp.get('dates', 'No dates')}\n"
            experience_text += f"   Description: {exp.get('description', 'No description')}\n\n"
    else:
        experience_text = "No experience data available"
    
    # Format skills
    skills_text = ", ".join(profile_data.get("skills", []))
    if not skills_text:
        skills_text = "No skills data available"
    
    return get_user_content_template().format(
        headline=profile_data.get("headline", "No headline"),
        about=profile_data.get("about", "No about section"),
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
