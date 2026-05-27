from crewai import Crew, Process
from agents import agents
from tasks import tasks

try:
    feedback_analysis_crew = Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential
    )
except Exception as e:
    raise Exception(f"Failed to initialize crew — {e}")
