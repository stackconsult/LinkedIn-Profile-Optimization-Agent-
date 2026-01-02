"""
Dynamic checklist generation based on profile analysis
"""

import re
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum

class TaskPriority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class ChecklistTask:
    """Individual checklist task"""
    id: str
    title: str
    description: str
    priority: TaskPriority
    estimated_time: str
    impact_level: str
    section: str
    dependencies: List[str] = None
    completed: bool = False

class DynamicChecklistGenerator:
    """Generate personalized checklist based on profile analysis"""
    
    def __init__(self):
        self.task_templates = {
            'headline_issues': [
                {
                    'title': '📝 Optimize Headline Length',
                    'description': 'Adjust headline to 60-120 characters for maximum impact',
                    'priority': TaskPriority.HIGH,
                    'time': '5 min',
                    'impact': 'High'
                },
                {
                    'title': '🎯 Add Value Proposition',
                    'description': 'Include clear value proposition showing what you bring to employers',
                    'priority': TaskPriority.HIGH,
                    'time': '10 min',
                    'impact': 'High'
                },
                {
                    'title': '🔍 Include Target Role Keywords',
                    'description': 'Add specific keywords related to your target role',
                    'priority': TaskPriority.HIGH,
                    'time': '5 min',
                    'impact': 'High'
                }
            ],
            'about_issues': [
                {
                    'title': '📄 Expand About Section',
                    'description': 'Increase word count to 300-500 words for comprehensive coverage',
                    'priority': TaskPriority.HIGH,
                    'time': '15 min',
                    'impact': 'High'
                },
                {
                    'title': '📖 Add Storytelling Elements',
                    'description': 'Include career journey, passion, and professional narrative',
                    'priority': TaskPriority.MEDIUM,
                    'time': '20 min',
                    'impact': 'Medium'
                },
                {
                    'title': '📊 Add Quantifiable Achievements',
                    'description': 'Include specific numbers, percentages, and measurable outcomes',
                    'priority': TaskPriority.HIGH,
                    'time': '10 min',
                    'impact': 'High'
                },
                {
                    'title': '🎯 Add Industry Keywords',
                    'description': 'Include more industry-specific terminology',
                    'priority': TaskPriority.MEDIUM,
                    'time': '10 min',
                    'impact': 'Medium'
                },
                {
                    'title': '📞 Add Call to Action',
                    'description': 'Include clear call to action for recruiters and connections',
                    'priority': TaskPriority.MEDIUM,
                    'time': '5 min',
                    'impact': 'Medium'
                }
            ],
            'experience_issues': [
                {
                    'title': '💼 Add Action Verbs',
                    'description': 'Start bullet points with strong action verbs',
                    'priority': TaskPriority.HIGH,
                    'time': '15 min',
                    'impact': 'High'
                },
                {
                    'title': '📈 Add Metrics and Results',
                    'description': 'Include specific numbers, percentages, and quantifiable outcomes',
                    'priority': TaskPriority.HIGH,
                    'time': '20 min',
                    'impact': 'High'
                },
                {
                    'title': '🎯 Add Impact Statements',
                    'description': 'Show the impact and results of your work',
                    'priority': TaskPriority.HIGH,
                    'time': '15 min',
                    'impact': 'High'
                },
                {
                    'title': '📝 Enhance Descriptions',
                    'description': 'Improve job descriptions with more detail and achievements',
                    'priority': TaskPriority.MEDIUM,
                    'time': '25 min',
                    'impact': 'Medium'
                }
            ],
            'skills_issues': [
                {
                    'title': '🎯 Add Industry-Specific Skills',
                    'description': 'Include more skills relevant to your target industry',
                    'priority': TaskPriority.HIGH,
                    'time': '10 min',
                    'impact': 'High'
                },
                {
                    'title': '⚖️ Balance Technical and Soft Skills',
                    'description': 'Ensure good mix of technical and interpersonal skills',
                    'priority': TaskPriority.MEDIUM,
                    'time': '10 min',
                    'impact': 'Medium'
                },
                {
                    'title': '📊 Add Missing Key Skills',
                    'description': 'Include essential skills for your target role',
                    'priority': TaskPriority.HIGH,
                    'time': '15 min',
                    'impact': 'High'
                }
            ],
            'general_optimization': [
                {
                    'title': '📱 Get Recommendations',
                    'description': 'Request recommendations from managers and colleagues',
                    'priority': TaskPriority.MEDIUM,
                    'time': '20 min',
                    'impact': 'Medium'
                },
                {
                    'title': '📅 Plan Content Strategy',
                    'description': 'Create 30-day content and engagement plan',
                    'priority': TaskPriority.LOW,
                    'time': '30 min',
                    'impact': 'Low'
                },
                {
                    'title': '🔍 Optimize Keywords',
                    'description': 'Ensure consistent keyword usage throughout profile',
                    'priority': TaskPriority.MEDIUM,
                    'time': '15 min',
                    'impact': 'Medium'
                },
                {
                    'title': '📊 Add Measurable Outcomes',
                    'description': 'Add specific metrics and achievements throughout',
                    'priority': TaskPriority.HIGH,
                    'time': '25 min',
                    'impact': 'High'
                }
            ]
        }
    
    def generate_dynamic_checklist(self, profile_data: Dict[str, Any], quality_scores: Dict[str, Any], 
                                 optimization_report: str, target_industry: str, target_role: str) -> List[ChecklistTask]:
        """Generate personalized checklist based on analysis"""
        
        checklist_tasks = []
        
        # Analyze headline
        headline_tasks = self._analyze_headline(profile_data.get('headline', ''), quality_scores.get('headline'))
        checklist_tasks.extend(headline_tasks)
        
        # Analyze about section
        about_tasks = self._analyze_about_section(profile_data.get('about', ''), quality_scores.get('about'))
        checklist_tasks.extend(about_tasks)
        
        # Analyze experience
        experience_data = profile_data.get('experience', [])
        # Handle both list of ExperienceItem objects and list of dicts
        if experience_data and hasattr(experience_data[0], 'description'):
            # ExperienceItem objects - convert to list format expected by analysis
            experience_tasks = self._analyze_experience_section(experience_data, quality_scores.get('experience'))
        else:
            # Dict objects or empty list
            experience_tasks = self._analyze_experience_section(experience_data, quality_scores.get('experience'))
        checklist_tasks.extend(experience_tasks)
        
        # Analyze skills
        skills_tasks = self._analyze_skills_section(profile_data.get('skills', []), quality_scores.get('skills'), target_industry)
        checklist_tasks.extend(skills_tasks)
        
        # Add general optimization tasks
        general_tasks = self._get_general_optimization_tasks(optimization_report)
        checklist_tasks.extend(general_tasks)
        
        # Sort by priority and impact
        checklist_tasks.sort(key=lambda x: (x.priority.value, x.impact_level), reverse=True)
        
        # Assign IDs
        for i, task in enumerate(checklist_tasks):
            task.id = f"task_{i+1}"
        
        return checklist_tasks
    
    def _analyze_headline(self, headline: str, headline_score) -> List[ChecklistTask]:
        """Analyze headline and generate tasks"""
        tasks = []
        
        if not headline or len(headline) < 60:
            tasks.append(ChecklistTask(
                id="", title="📝 Create Compelling Headline",
                description="Write a headline that's 60-120 characters and includes your value proposition",
                priority=TaskPriority.HIGH,
                estimated_time="10 min",
                impact_level="High",
                section="Headline"
            ))
        
        if headline_score and headline_score.score < 80:
            # Add specific tasks based on score feedback
            if "value proposition" in str(headline_score.feedback):
                tasks.append(ChecklistTask(
                    id="", title="🎯 Add Value Proposition",
                    description="Include what value you bring to potential employers",
                    priority=TaskPriority.HIGH,
                    estimated_time="5 min",
                    impact_level="High",
                    section="Headline"
                ))
        
        return tasks
    
    def _analyze_about_section(self, about: str, about_score) -> List[ChecklistTask]:
        """Analyze about section and generate tasks"""
        tasks = []
        
        word_count = len(about.split()) if about else 0
        
        if word_count < 300:
            tasks.append(ChecklistTask(
                id="", title="📄 Expand About Section",
                description=f"Expand from {word_count} to 300-500 words with more detail",
                priority=TaskPriority.HIGH,
                estimated_time="20 min",
                impact_level="High",
                section="About"
            ))
        
        if about_score and about_score.score < 70:
            if "storytelling" in str(about_score.feedback):
                tasks.append(ChecklistTask(
                    id="", title="📖 Add Career Story",
                    description="Add your professional journey and passion narrative",
                    priority=TaskPriority.MEDIUM,
                    estimated_time="15 min",
                    impact_level="Medium",
                    section="About"
                ))
            
            if "quantifiable" in str(about_score.feedback):
                tasks.append(ChecklistTask(
                    id="", title="📊 Add Measurable Achievements",
                    description="Include specific numbers and achievements in your story",
                    priority=TaskPriority.HIGH,
                    estimated_time="10 min",
                    impact_level="High",
                    section="About"
                ))
        
        return tasks
    
    def _analyze_experience_section(self, experiences: List, experience_score) -> List[ChecklistTask]:
        """Analyze experience section and generate tasks"""
        tasks = []
        
        if not experiences:
            tasks.append(ChecklistTask(
                id="", title="💼 Add Experience Entries",
                description="Add your work experience with detailed descriptions",
                priority=TaskPriority.HIGH,
                estimated_time="30 min",
                impact_level="High",
                section="Experience"
            ))
            return tasks
        
        # Check for missing metrics in experience descriptions
        for i, exp in enumerate(experiences):
            # Handle both dict and ExperienceItem objects
            if hasattr(exp, 'description'):
                description = exp.description
                title = exp.title
            else:
                description = exp.get('description', '')
                title = exp.get('title', 'Experience')
            
            if not any(indicator in description.lower() for indicator in ['%', '$', 'number', 'increased', 'decreased']):
                tasks.append(ChecklistTask(
                    id="", title=f"📈 Add Metrics to {title}",
                    description="Add specific numbers and results to this experience",
                    priority=TaskPriority.HIGH,
                    estimated_time="10 min",
                    impact_level="High",
                    section="Experience"
                ))
        
        if experience_score and experience_score.score < 70:
            if "action verbs" in str(experience_score.feedback):
                tasks.append(ChecklistTask(
                    id="", title="⚡ Add Action Verbs",
                    description="Start bullet points with strong action verbs",
                    priority=TaskPriority.HIGH,
                    estimated_time="15 min",
                    impact_level="High",
                    section="Experience"
                ))
        
        return tasks
    
    def _analyze_skills_section(self, skills: List[str], skills_score, target_industry: str) -> List[ChecklistTask]:
        """Analyze skills section and generate tasks"""
        tasks = []
        
        if len(skills) < 10:
            tasks.append(ChecklistTask(
                id="", title="🎯 Add More Skills",
                description=f"Add {10 - len(skills)} more relevant skills to reach optimal count",
                priority=TaskPriority.HIGH,
                estimated_time="10 min",
                impact_level="High",
                section="Skills"
            ))
        
        if skills_score and skills_score.score < 70:
            if "industry-relevant" in str(skills_score.feedback):
                tasks.append(ChecklistTask(
                    id="", title="🔍 Add Industry-Specific Skills",
                    description=f"Add more {target_industry} specific skills",
                    priority=TaskPriority.HIGH,
                    estimated_time="15 min",
                    impact_level="High",
                    section="Skills"
                ))
        
        return tasks
    
    def _get_general_optimization_tasks(self, optimization_report: str) -> List[ChecklistTask]:
        """Extract general optimization tasks from report"""
        tasks = []
        
        # Always include these general tasks
        tasks.extend([
            ChecklistTask(
                id="", title="📱 Get Recommendations",
                description="Request recommendations from managers and colleagues",
                priority=TaskPriority.MEDIUM,
                estimated_time="20 min",
                impact_level="Medium",
                section="General"
            ),
            ChecklistTask(
                id="", title="📅 Plan Content Strategy",
                description="Create 30-day content and engagement plan",
                priority=TaskPriority.LOW,
                estimated_time="30 min",
                impact_level="Low",
                section="General"
            )
        ])
        
        return tasks
    
    def estimate_completion_time(self, tasks: List[ChecklistTask]) -> Dict[str, Any]:
        """Estimate total completion time and breakdown"""
        total_minutes = 0
        priority_breakdown = {
            TaskPriority.HIGH: 0,
            TaskPriority.MEDIUM: 0,
            TaskPriority.LOW: 0
        }
        
        for task in tasks:
            # Parse time estimate (e.g., "15 min" -> 15)
            time_match = re.search(r'(\d+)', task.estimated_time)
            if time_match:
                minutes = int(time_match.group(1))
                total_minutes += minutes
                priority_breakdown[task.priority] += minutes
        
        return {
            'total_minutes': total_minutes,
            'total_hours': round(total_minutes / 60, 1),
            'priority_breakdown': {
                'high': priority_breakdown[TaskPriority.HIGH],
                'medium': priority_breakdown[TaskPriority.MEDIUM],
                'low': priority_breakdown[TaskPriority.LOW]
            },
            'formatted_time': self._format_time(total_minutes)
        }
    
    def _format_time(self, minutes: int) -> str:
        """Format time in human readable format"""
        if minutes < 60:
            return f"{minutes} minutes"
        elif minutes < 120:
            return f"1 hour {minutes - 60} minutes"
        else:
            hours = minutes // 60
            remaining_minutes = minutes % 60
            return f"{hours} hours {remaining_minutes} minutes"
