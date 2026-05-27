from crewai.tools import tool
import json
import os
import pandas as pd
import re


@tool("write_csv_tool")
def write_csv_tool(data: str) -> str:
    """Writes a JSON string of tickets to generated_tickets.csv"""
    try:
        cleaned = re.sub(r'```json|```', '', data).strip()
        match = re.search(r'\[.*\]', cleaned, re.DOTALL)
        if match:
            cleaned = match.group(0)
        tickets = json.loads(cleaned)
        filepath = "output/generated_tickets.csv"
        df_new = pd.DataFrame(tickets)
        if os.path.exists(filepath):
            df_existing = pd.read_csv(filepath)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df_combined = df_new
        df_combined.to_csv(filepath, index=False)
        return f"Successfully written {len(tickets)} tickets to {filepath}"
    except json.JSONDecodeError as e:
        return f"Error: Could not parse JSON — {e}"
    except Exception as e:
        return f"Error writing tickets — {e}"


# log writer tool
@tool("write_log_tool")
def write_log_tool(data: str) -> str:
    """Writes reviewed tickets to processing_log.csv"""
    try:
        cleaned = re.sub(r'```json|```', '', data).strip()
        match = re.search(r'\[.*\]', cleaned, re.DOTALL)
        if match:
            cleaned = match.group(0)
        reviewed_tickets = json.loads(cleaned)
        filepath = "output/processing_log.csv"
        df_new = pd.DataFrame(reviewed_tickets)
        if os.path.exists(filepath):
            df_existing = pd.read_csv(filepath)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df_combined = df_new
        df_combined.to_csv(filepath, index=False)
        return f"Successfully written {len(reviewed_tickets)} tickets to {filepath}"
    except json.JSONDecodeError as e:
        return f"Error: Could not parse JSON — {e}"
    except Exception as e:
        return f"Error writing processing log — {e}"