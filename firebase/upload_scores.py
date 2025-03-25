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
        match = re.search(rf'"{key}"\s*:\s*["“]?(\d)["”]?', text)
        if match:
            scores[key] = int(match.group(1))

    return scores

def update_firebase(user, pr_id, new_scores, firebase_url):
    base_url = f"{firebase_url}/users/{user}"
    pr_url = f"{base_url}/pr_{pr_id}.json"
    cumulative_url = f"{base_url}/cumulative_score.json"

    # Upload per-PR scores
    print(f"Uploading scores to: {pr_url}")
    pr_response = requests.put(pr_url, json=new_scores)
    if pr_response.ok:
        print(f"Scores for PR #{pr_id} uploaded.")
    else:
        print(f"Failed to upload PR scores: {pr_response.text}")
        return

    # Fetch existing cumulative scores
    existing = requests.get(cumulative_url).json() or {}
    pr_count = existing.get("pr_count", 0)

    updated = {}
    for key in new_scores:
        prev_val = existing.get(key, 0)
        updated[key] = (prev_val * pr_count + new_scores[key]) / (pr_count + 1)

    updated["pr_count"] = pr_count + 1

    # Upload updated cumulative score
    print(f"📡 Updating cumulative score at: {cumulative_url}")
    cum_response = requests.put(cumulative_url, json=updated)
    if cum_response.ok:
        print("Cumulative score updated.")
    else:
        print(f"Failed to update cumulative score: {cum_response.text}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python upload_scores.py <pr_message_file> <github_user> <pr_id>")
        sys.exit(1)

    pr_file = sys.argv[1]
    user = sys.argv[2]
    pr_id = sys.argv[3]
    firebase_url = os.getenv("FIREBASE_URL")

    if not firebase_url:
        print("FIREBASE_URL is not set.")
        sys.exit(1)

    with open(pr_file, 'r') as f:
        pr_text = f.read()

    print("PR body snippet:")
    print(pr_text[:300])

    scores = extract_scores(pr_text)
    print(f"Extracted Scores: {scores}")

    if all(v is not None for v in scores.values()):
        update_firebase(user, pr_id, scores, firebase_url)
    else:
        print("Not all scores found. Skipping Firebase upload.")
