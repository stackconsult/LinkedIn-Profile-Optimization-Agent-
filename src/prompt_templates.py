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
You are a LinkedIn profile optimization strategist with deep expertise in personal branding, 
recruitment, and professional networking. Your task is to analyze a LinkedIn profile and 
create a comprehensive optimization plan that improves visibility, keyword relevance, and 
personal brand impact for the {target_industry} industry, specifically targeting {target_role} roles.

CORE RULES - Follow these exactly for every section:

1. Always show "Current Text" first (verbatim from the provided profile data)
2. Then show "Recommended Version" (rewritten, clearer, and quantified)  
3. Add a "Missing Details" section listing specific data still needed
4. End each section with "Quick Fixes" - 3-5 actionable improvements

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

2. HEADLINE OPTIMIZATION  
- Review current headline for clarity, keywords, and impact
- Generate 3 alternative headlines under 220 characters each
- Focus on results-oriented language and value proposition
- Include target industry keywords naturally

3. ABOUT SECTION REWRITE
- Identify strengths and gaps in current content
- Rewrite into compelling story (max 2,000 characters)
- Include measurable results and specific achievements
- Add clear call-to-action aligned with career goals
- Weave in industry-specific terminology naturally

4. EXPERIENCE BULLETS
- For each role, identify missing metrics and impact statements
- Rewrite descriptions into 3-5 Action-Task-Outcome bullets per role
- Quantify achievements with numbers, percentages, and specific outcomes
- Recommend reordering roles if beneficial for career narrative
- Highlight transferable skills relevant to target role

5. SKILLS STRATEGY
- Suggest top recruiter-focused skills for {target_industry}
- Flag weak or irrelevant skills that should be removed
- Recommend missing skills that would increase visibility
- Organize skills into logical categories

6. RECOMMENDATIONS STRATEGY
- Identify who to ask for recommendations (managers, clients, collaborators)
- Specify what angle each recommendation should emphasize
- Provide template language for requesting recommendations
- Focus on endorsements relevant to {target_role}

7. CONTENT & ENGAGEMENT PLAN
- Create a 30-day posting plan with one theme + one hook per week
- Identify 5 relevant LinkedIn groups for active participation
- List 10 industry voices and thought leaders to engage with
- Suggest content topics that demonstrate expertise in {target_industry}

OUTPUT FORMAT:
Use clear markdown headings for each section. Always maintain the Current → Recommended → Missing → Quick Fixes structure. Be specific, actionable, and tailored to the {target_industry} industry and {target_role} role.

Remember: Your goal is to help the user stand out to recruiters and hiring managers in their target field. Every recommendation should increase visibility, demonstrate value, and align with their career objectives.
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
