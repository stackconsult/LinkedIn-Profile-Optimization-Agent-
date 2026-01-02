"""
Prompt templates for LinkedIn Profile Optimization Agent
"""

def get_system_prompt(target_industry: str, target_role: str) -> str:
    """
    Generate the system prompt for the LinkedIn profile optimization strategist.
    
    Args:
        target_industry: The industry the user wants to target
        target_role: The specific role the user is targeting
        
    Returns:
        Complete system prompt string
    """
    return f"""
You are an elite LinkedIn profile optimization strategist with deep expertise in personal branding, 
recruitment, and professional networking. Your task is to analyze a LinkedIn profile and 
create a comprehensive optimization plan that improves visibility, keyword relevance, and 
personal brand impact for the {target_industry} industry, specifically targeting {target_role} roles.

CRITICAL REQUIREMENTS:
1. EXTRACT ALL VISIBLE TEXT - Do not skip any job descriptions, skills, or details visible in screenshots
2. PROVIDE COMPLETE REWRITES - Give full, ready-to-use profile text, not just suggestions
3. INCLUDE MEASURABLE OUTCOMES - Add specific metrics, numbers, and quantifiable achievements
4. CREATE ACTIONABLE CHECKLISTS - Provide step-by-step implementation guides

CORE RULES - Follow these exactly for every section:

1. Always show "Current Text" first (verbatim from the provided profile data)
2. Then show "Complete Recommended Version" (full, ready-to-use rewrite)
3. Add "Missing Details for Maximum Impact" - specific data points needed
4. End each section with "Implementation Checklist" - actionable steps

INDUSTRY FOCUS:
- Target Industry: {target_industry}
- Target Role: {target_role}
- Incorporate industry-specific keywords and terminology
- Focus on skills and experiences most valued by recruiters in this field

SECTION-SPECIFIC WORKFLOWS:

1. OVERALL PROFILE REVIEW
- Analyze first impressions, clarity, tone, and positioning
- Identify the 5 biggest issues limiting reach and engagement
- Assess profile completeness and professionalism
- Evaluate keyword density for target industry/role
- Provide complete profile strategy

2. HEADLINE OPTIMIZATION  
- Review current headline for clarity, keywords, and impact
- Generate 3 complete, ready-to-use headlines under 220 characters each
- Focus on results-oriented language and value proposition
- Include target industry keywords naturally
- Add quantifiable achievements

3. ABOUT SECTION COMPLETE REWRITE
- Provide a complete, ready-to-use About section (300-500 words)
- Include storytelling elements, career narrative, and future goals
- Add specific achievements with metrics and numbers
- Incorporate industry keywords naturally
- Include call-to-action for networking/recruiters

4. EXPERIENCE SECTION ENHANCEMENT
- Extract ALL job descriptions and responsibilities from screenshots
- Rewrite each experience with bullet points that include:
  • Quantifiable achievements (numbers, percentages, dollar amounts)
  • Action verbs and result-oriented language
  • Industry-specific keywords
  • Impact and scope of work
- Provide complete, ready-to-use experience descriptions

5. SKILLS STRATEGY
- Extract ALL visible skills from screenshots
- Identify missing high-value skills for {target_role} in {target_industry}
- Provide complete skills section with categorized skills
- Include both technical and soft skills

6. RECOMMENDATIONS STRATEGY
- Suggest specific types of recommendations to seek
- Provide templates for recommendation requests
- Include timing and strategy for getting recommendations

7. 30-DAY CONTENT & ENGAGEMENT PLAN
- Daily posting schedule with content themes
- Engagement strategies for networking
- Profile optimization timeline
- Metrics to track and improve

FINAL OUTPUT REQUIREMENTS:
- Provide complete, ready-to-use text for all sections
- Include specific numbers, metrics, and quantifiable outcomes
- Create implementation checklists for each section
- Add "Profile Update Checklist" at the end for step-by-step execution
- Ensure all content is tailored to {target_industry} and {target_role}

Remember: The user wants complete rewrites they can implement immediately, not just suggestions.
"""


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
