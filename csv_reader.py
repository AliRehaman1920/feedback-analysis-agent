import pandas as pd

def load_feedback():
    feedback = []
    
    try:
        reviews = pd.read_csv("data/app_store_reviews.csv")
        for _, row in reviews.iterrows():
            feedback.append({
                "source_id": row["review_id"],
                "source_type": "app_store_review",
                "text": row["review_text"],
                "metadata": {
                    "platform": row["platform"],
                    "rating": row["rating"],
                    "app_version": row["app_version"]
                }
            })
    except FileNotFoundError:
        raise FileNotFoundError("app_store_reviews.csv not found in data/")
    except Exception as e:
        raise Exception(f"Error reading app_store_reviews.csv — {e}")

    try:
        emails = pd.read_csv("data/support_emails.csv")
        for _, row in emails.iterrows():
            feedback.append({
                "source_id": row["email_id"],
                "source_type": "support_email",
                "text": f"{row['subject']}. {row['body']}",
                "metadata": {
                    "sender": row["sender_email"],
                    "timestamp": row["timestamp"]
                }
            })
    except FileNotFoundError:
        raise FileNotFoundError("support_emails.csv not found in data/")
    except Exception as e:
        raise Exception(f"Error reading support_emails.csv — {e}")

    return feedback