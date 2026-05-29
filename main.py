import os
import re
import json
import pandas as pd
from crew import feedback_analysis_crew
from csv_reader import load_feedback

def main():
    # Clear previous output
    try:
        for f in ["output/generated_tickets.csv", "output/processing_log.csv"]:
            if os.path.exists(f):
                os.remove(f)
        os.makedirs("output", exist_ok=True)
    except Exception as e:
        print(f"Warning: Could not clear output files — {e}")

    # Load feedback
    try:
        feedback = load_feedback()
        print(f"Loaded {len(feedback)} feedback items")
    except FileNotFoundError as e:
        print(f"Error: Could not find input CSV files — {e}")
        exit(1)
    except Exception as e:
        print(f"Error loading feedback — {e}")
        exit(1)

    # Run pipeline
    try:
        print("Starting multi-agent pipeline...")
        BATCH_SIZE = 10
        for i in range(0, len(feedback), BATCH_SIZE):
            batch = feedback[i:i + BATCH_SIZE]
            print(f"Processing batch {i//BATCH_SIZE + 1} of {-(-len(feedback)//BATCH_SIZE)}...")
            feedback_analysis_crew.kickoff(inputs={"feedback": str(batch)})
    except Exception as e:
        print(f"Pipeline failed — {e}")
        exit(1)

    # Summary
    try:
        if os.path.exists("output/generated_tickets.csv"):
            df = pd.read_csv("output/generated_tickets.csv")
            print(f"\nPipeline complete — {len(df)} tickets generated")
            print(df["category"].value_counts().to_string())
        else:
            print("Pipeline complete — no tickets file found")
    except Exception as e:
        print(f"Error reading output — {e}")

    # Generate metrics
    try:
        if os.path.exists("output/generated_tickets.csv"):
            df = pd.read_csv("output/generated_tickets.csv")
            
            metrics = {
                "total_processed": len(feedback),
                "total_tickets": len(df),
                "bugs": len(df[df["category"] == "Bug"]),
                "feature_requests": len(df[df["category"] == "Feature Request"]),
                "praise": len(df[df["category"] == "Praise"]),
                "complaints": len(df[df["category"] == "Complaint"]),
                "spam": len(df[df["category"] == "Spam"]),
                "critical": len(df[df["priority"] == "Critical"]),
                "high": len(df[df["priority"] == "High"]),
                "medium": len(df[df["priority"] == "Medium"]),
                "low": len(df[df["priority"] == "Low"]),
            }

            # accuracy vs expected classifications
            try:
                expected = pd.read_csv("data/expected_classifications.csv")
                merged = df.merge(expected, on="source_id", suffixes=("_generated", "_expected"))
                correct = (merged["category_generated"] == merged["category_expected"]).sum()
                metrics["accuracy"] = round(correct / len(merged) * 100, 2) if len(merged) > 0 else 0
                metrics["total_compared"] = len(merged)
            except Exception:
                metrics["accuracy"] = "N/A"
                metrics["total_compared"] = 0

            pd.DataFrame([metrics]).to_csv("output/metrics.csv", index=False)
            print(f"\nMetrics saved — accuracy: {metrics['accuracy']}%")

    except Exception as e:
        print(f"Error generating metrics — {e}")

if __name__ == "__main__":
    main()
