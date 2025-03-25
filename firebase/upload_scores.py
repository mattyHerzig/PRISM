import sys
import re
import requests
import json
import os

def extract_scores(text):
    scores = {
        "readability_score": None,
        "robustness_score": None,
        "security_score": None,
        "performance_score": None
    }

    for key in scores:
        # Match: "readability_score": 1  or  "readability_score": "1"
        match = re.search(rf'"{key}"\s*:\s*["“]?(\d)["”]?', text)
        if match:
            scores[key] = int(match.group(1))

    return scores

def update_firebase(user, new_scores, firebase_url):
    url = f"{firebase_url}/users/{user}.json"

    try:
        response = requests.get(url)
        if not response.ok:
            print("Failed to fetch user data from Firebase.")
            return

        existing = response.json() or {}
        current_count = existing.get("pr_count", 0)

        updated = {}
        for key in new_scores:
            if new_scores[key] is not None:
                prev_val = existing.get(key, 0)
                updated[key] = (prev_val * current_count + new_scores[key]) / (current_count + 1)
            else:
                updated[key] = existing.get(key, 0)

        updated["pr_count"] = current_count + 1

        put_response = requests.put(url, json=updated)
        if put_response.ok:
            print(f"Uploaded scores for {user}")
        else:
            print(f"Failed to update scores: {put_response.text}")
    
    except Exception as e:
        print(f"Error updating Firebase: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python upload_scores.py <pr_message_file> <github_user>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        pr_text = f.read()

    user = sys.argv[2]
    firebase_url = os.getenv("FIREBASE_URL")

    if not firebase_url:
        print("FIREBASE_URL is not set.")
        sys.exit(1)

    scores = extract_scores(pr_text)
    print(f"Extracted Scores: {scores}")
    update_firebase(user, scores, firebase_url)
