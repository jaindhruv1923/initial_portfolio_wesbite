"""
Candidate Defense Playbook & Recruiter Screening Interview Generator
====================================================================
Generates surgical screening interview questions and candidate outreach
templates to expose phantom requisitions before wasting application effort.
"""

from typing import Dict, Any, List

class CandidateDefensePlaybook:
    def generate_recruiter_screening_questions(
        self,
        job_title: str,
        company_name: str,
        days_live: float = 30.0,
        is_ghost_suspect: bool = True
    ) -> List[Dict[str, str]]:
        """
        Generates tactical questions for the candidate to ask during the HR screen
        to verify active hiring budget and unfreeze hidden ghost signals.
        """
        questions = [
            {
                "question": f"Is this {job_title} role backfilling an engineer who recently moved, or is it newly approved expansion headcount for this quarter?",
                "objective": "Verify active headcount budget.",
                "green_flag_answer": "Explicitly names a team expansion project or explains the previous person's internal promotion.",
                "red_flag_answer": "'We are always looking for great talent to build our pipeline for upcoming needs.'"
            },
            {
                "question": "What specific team milestone or deliverables will this hire own within their first 60 days?",
                "objective": "Test day-to-day team ownership.",
                "green_flag_answer": "Identifies an immediate pending sprint, architecture overhaul, or product feature.",
                "red_flag_answer": "'It depends on what projects come up later this year.'"
            },
            {
                "question": f"I noticed this opening has been listed on portals ({days_live:.0f} days live). What is the targeted hiring timeline and start date?",
                "objective": "Detect stale requisition lingering.",
                "green_flag_answer": "'We aim to make an offer within 2-3 weeks for a start date by next month.'",
                "red_flag_answer": "'There is no rush; we're taking our time exploring different candidate profiles.'"
            },
            {
                "question": "How many candidates are currently in the final interview rounds for this requisition?",
                "objective": "Check interview pipeline velocity.",
                "green_flag_answer": "Clear, specific count (e.g. '2 candidates at final stage, you will be in the next cohort').",
                "red_flag_answer": "Vague evasion or admitting they haven't reviewed applications in weeks."
            },
            {
                "question": "Who will be the direct reporting manager for this role, and will I be speaking with them in round two?",
                "objective": "Confirm hiring manager engagement.",
                "green_flag_answer": "Directly names the Engineering Manager / Director and outlines their technical round.",
                "red_flag_answer": "Refuses to disclose the manager or mentions external client interview uncertainty."
            }
        ]
        return questions

    def generate_hiring_manager_outreach(
        self,
        job_title: str,
        company_name: str,
        key_skills: str = "Python, SQL, Distributed Systems"
    ) -> str:
        """
        Generates an executive outreach message for candidates to message
        engineering leaders on LinkedIn, bypassing dormant portal ATS queues.
        """
        return f"""Hi [Hiring Manager Name],

I noticed the {job_title} requisition at {company_name} and wanted to reach out directly rather than getting lost in portal ATS queues.

I specialize in {key_skills} and have recently delivered scalable solutions in this exact domain. Given {company_name}'s recent work, I would love to learn if your team is actively interviewing for this role this month and whether a brief conversation would make sense.

I have attached my portfolio / GitHub and would welcome 5 minutes to see if my background aligns with your current roadmap.

Best regards,
[Your Name] | [LinkedIn / Portfolio Link]
"""

# Singleton instance
defense_playbook = CandidateDefensePlaybook()
