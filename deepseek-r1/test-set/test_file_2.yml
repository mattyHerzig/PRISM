import requests
import base64
import json
import os

# GitHub API Token (Ensure it is valid and has the required permissions)
GITHUB_TOKEN = 'Hidden_Token'
HEADERS = {'Authorization': f'token {GITHUB_TOKEN}'}

def get_pull_request_details(owner, repo, pr_id):
    """Fetches details of a specific pull request."""
    pr_url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_id}'
    print(pr_id)
    response = requests.get(pr_url, headers=HEADERS)
    
    if response.status_code == 200:
        pr_data = response.json()
        return {
            "Title": pr_data.get('title', 'N/A'),
            "Mergeable": pr_data.get('mergeable', False)
        }
    else:
        print(f"Failed to fetch PR details. Status Code: {response.status_code}")
        return None

def get_pull_request_files(owner, repo, pr_id):
    """Fetches all files changed in the pull request."""
    files_url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_id}/files'
    response = requests.get(files_url, headers=HEADERS)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch PR files. Status Code: {response.status_code}")
        return None
