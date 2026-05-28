from crewai import LLM
import os

try:
    llm = LLM(
        model="gemini/gemini-2.5-flash",
        api_key=os.getenv("GEMINI_API_KEY")
    )
except Exception as e:
    raise Exception(f"Failed to initialize LLM — {e}")
