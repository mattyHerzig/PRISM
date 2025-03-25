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

def store_scores_by_pr(user, pr_id, new_scores, firebase_url):
    url = f"{firebase_url}/users/{user}/pr_{pr_id}.json"
    print(f"Uploading scores to: {url}")

    response = requests.put(url, json=new_scores)
    if response.ok:
        print(f"Scores for PR #{pr_id} uploaded successfully under {user}")
    else:
        print(f"Failed to upload scores: {response.text}")

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
    print(f" Extracted Scores: {scores}")

    if all(v is not None for v in scores.values()):
        store_scores_by_pr(user, pr_id, scores, firebase_url)
    else:
        print(" Not all scores found. Skipping Firebase upload.")
