from crewai import LLM
import os

try:
    llm = LLM(
        model="gemini/gemini-1.5-flash-002",
        api_key=os.getenv("GEMINI_API_KEY2")
    )
except Exception as e:
    raise Exception(f"Failed to initialize LLM — {e}")
