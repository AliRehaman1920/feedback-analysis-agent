from crewai import Agent

from llm import llm
from tools import write_csv_tool, write_log_tool


# Classifier agent
classifier_agent = Agent(
    role = "User Feedback Classifer",
    goal = "Accurately classify user feedback into categories with confidence scores",
    backstory=(
        "You are an expert product analyst,"
        "with years of experience analyzing mobile app feedback."
        "You can instantly identify whether feedback"
        "is a bug report, feature request, praise, complaint, or spam"
        "You always return structured JSON output"
    ),
    allow_delegation=False,
    llm = llm,
    verbose=False
)

# Bug analysis agent
bug_analysis_agent = Agent(
    role="Bug Analysis Specialist",
    goal="Extract structured technical details from feedback items classified as bugs",
    backstory=(
        "You are a senior mobile QA engineer with deep experience analyzing "
        "Android and iOS application failures. You transform raw user complaints "
        "into structured engineering-ready bug reports."
        "You always return structured JSON output."
    ),
    allow_delegation=False,
    llm=llm,
    verbose=False
)

# Feature extractor agent

feature_extractor_agent = Agent(
    role="Feature Request Analyst",
    goal="Extract structured details from feedback items classified as Feature Request",
    backstory=(
        "You are a senior product manager with experience analyzing user feature requests. "
        "You identify the core feature being requested, estimate user impact and demand. "
        "You always return structured JSON output."
    ),
    allow_delegation=False,
    llm=llm,
    verbose=False
)

# Ticket creator agent and task

ticket_creator_agent = Agent(
    role="Ticket Creator",
    goal="Generate clean structured tickets from enriched feedback and save to CSV using write_csv_tool",
    backstory=(
        "You are a project management expert who creates clear actionable "
        "engineering tickets from user feedback and saves them to CSV. "
        "You always use the write_csv_tool to save tickets. "
        "You always return structured JSON output."
    ),
    allow_delegation=False,
    llm=llm,
    verbose=False,
    tools=[write_csv_tool]
)

# Quality critic agent
quality_critic_agent = Agent(
    role="Quality Critic",
    goal="Review generated tickets for completeness and accuracy and save review to CSV",
    backstory=(
        "You are a senior QA lead who reviews engineering tickets before they "
        "reach the development team. You check for missing information, incorrect "
        "priority assignments, and unclear titles. "
        "You always use write_log_tool to save your review. "
        "You always return structured JSON output."
    ),
    allow_delegation=False,
    llm=llm,
    verbose=False,
    tools=[write_log_tool]
)


agents = [
    classifier_agent,
    bug_analysis_agent,
    feature_extractor_agent,
    ticket_creator_agent,
    quality_critic_agent
]