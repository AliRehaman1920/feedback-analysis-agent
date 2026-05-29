from crewai import Task
import os

from agents import (
    classifier_agent,
    bug_analysis_agent,
    feature_extractor_agent,
    ticket_creator_agent,
    quality_critic_agent
)

# Classifying Task
classifying_task = Task(
    description=(
        "You will receive a list of feedback items"
        "For each item, ADD the following fields without removing anything"
        "-category: Bug / Feature Request / Praise /Complaint / Spam"
        "-confidence: float between 0 and 1"
        "-reasoning: one line explanation"
        "Feedback items: {feedback}"
        "Return ONLY the JSON list with new fields added, no extra text"
    ),
    expected_output=(
        "A JSON List with all original fields plus category, confidence and reasoning"
    ),
    agent = classifier_agent
)

# Bug analysis task
bug_analysis_task = Task(
    description=(
        "You will receive a list of classified feedback items."
        "Add these fields to the json given to you: 'priority' and 'technical_details'"

        "For items where category is exactly 'Bug': "
        "-ADD to priority: Critical/High/Medium/Low based on impact"
        "-ADD to technical_details: extract from the text field and format exactly as:"
        '"Device: X | OS : X | Version: X | Steps : X"'

        "Use 'Unknown' for any missing values"

        "For items where category is NOT 'Bug':"
        "-ADD to priority: Null"
        "-ADD to technical_details: Null"
        "Do not remove any existing fields."
        "Return ONLY the complete JSON list of all items, no extra text."
    ),
    expected_output="Valid JSON only",
    agent=bug_analysis_agent,
    context=[classifying_task]
)

# Feature Extracting Task
feature_extraction_task = Task(
    description=(
        "You will receive a list of feedback items. "
        "For items where category is exactly 'Feature Request': "
        "-ADD to priority: Critical/High/Medium/Low based on user impact "
        "-ADD to technical_details: format exactly as: "
        "'Device: X | Version: X |Feature: X | Impact: X | Demand: X' "
        "For items where category is NOT 'Feature Request': "
        "-Keep priority and technical_details exactly as they already are, do not overwrite them. "
        "Do not remove any existing fields. "
        "Return ONLY the complete JSON list of all items, no extra text."
    ),
    expected_output="Valid JSON only",
    agent=feature_extractor_agent,
    context=[bug_analysis_task]
)

# Ticket Generating Task
ticket_creation_task = Task(
    description=(
        "You will receive a list of enriched feedback items. "
        "For each item create a clean ticket by: "
        "KEEP: source_id, source_type, category, priority, technical_details "
        "ADD suggested_title: in format '[CATEGORY] description' "
        "Set null/Unknown technical_details to 'No technical details required' "
        "Set null priority to 'Low' "
        "REMOVE: text, metadata, confidence, reasoning "
        "You MUST use write_csv_tool to save the final tickets to CSV. "
        "Return ONLY a valid JSON list of clean tickets, no extra text."
    ),
    expected_output="Valid JSON list of clean tickets saved to CSV",
    agent=ticket_creator_agent,
    context=[feature_extraction_task]
)

# Quality Critic Task
quality_critic_task = Task(
    description=(
        "You will receive a list of generated tickets. "
        "Review each ticket and add these fields: "
        "-ADD quality_score: integer from 1 to 10 "
        "-ADD quality_notes: one line explaining the score "
        "-ADD quality_status: 'Pass' if score >= 7, 'Review' if below 7 "
        "Do not remove any existing fields. "
        "You MUST use write_log_tool to save the reviewed tickets. "
        "Return ONLY a valid JSON list, no extra text."
    ),
    expected_output="Valid JSON list of reviewed tickets saved to processing_log.csv",
    agent=quality_critic_agent,
    context=[ticket_creation_task]
)



tasks = [
    classifying_task,
    bug_analysis_task,
    feature_extraction_task,
    ticket_creation_task,
    quality_critic_task
]
