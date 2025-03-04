
import os
import requests
import sys
import json

LLAMA_API_URL = os.getenv("LLAMA_API_URL")

def generate_pr_description(diff_content, pr_number):
    if not LLAMA_API_URL:
        print("❌ Error: LLAMA_API_URL is not set.")
        return "Error: LLAMA_API_URL is not configured."

    
    prompt = """

Analyze the given code changes and generate a detailed pull request description as a summary.

And give an overall single score based on Readability, Maintainability and Clarity. 



The return format should be in the below json format:
{
    "readability_score": “<score within 1-3>”,
    "output": "<text explanation of the reason for the scoring and improvements that can apply>”
} 

Be careful while analyzing the new code. Make sure to identify all the code changes before and after modifications and double-check the answer. Use the checkboxes and scoring criteria below while assigning the score.

—
"""
    prompt+=f"These are the code changes: \n\nPR Summary: \nPR #{pr_number}\n\nCode Changes:\n{diff_content}."

    prompt+="""
Checkboxes: 
1. Clear Naming Conventions (Function and variable names are meaningful, self-explanatory and easy to understand.)
2. Documentation (Code includes meaningful inline comments explaining logic and purpose.)
3. Formatting & Styling (Code follows consistent indentation and spacing.)
4. Maintainability (Code is easy to extend or modify.)
5. Code Length (Functions are not excessively long; logic is broken down into smaller parts.)

Scoring Criteria:
- 3 (Excellent): After modifications, Code meets all readability, maintainability, and clarity standards. Naming is clear, proper documentation, formatting is consistent, and code structure is easy to modify.  
- 2 (moderate): After modifications, Code is readable and maintainable but has a scope for improvement.  
- 1 (Poor): After modifications, Code is highly unreadable, with little no documentation, inconsistent naming.
---
"""

    try:
        print(f"🔹 Sending request to LLAMA_API_URL: {LLAMA_API_URL}")
        
        response = requests.post(LLAMA_API_URL, json={"model": "deepseek-r1", "prompt": prompt})
        
        if response.status_code != 200:
            print(f" Error: Received status code {response.status_code} from Llama API")
            return "Error generating PR description."

        response_json = response.json()
        print(" Debug: Full response from FastAPI:", json.dumps(response_json, indent=2))

        # Extract response text safely
        generated_text = response_json.get("response", "No content from Llama.")
        
        if not generated_text.strip():
            print("Warning: Llama API returned an empty response.")
            return "No content from Llama."

        return generated_text

    except requests.exceptions.RequestException as e:
        print(f" Error: Failed to reach Llama API - {e}")
        return "Error: Unable to contact Llama API."

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(" Error: Missing required arguments. Usage: python main.py <diff_file_path> <pr_number>")
        sys.exit(1)

    diff_file_path = sys.argv[1]
    pr_number = sys.argv[2]

    try:
        with open(diff_file_path, "r") as f:
            diff_content = f.read().strip()
        
        if not diff_content:
            print(" Warning: The diff file is empty. No content to process.")
            pr_body = "No changes detected in this PR."
        else:
            pr_body = generate_pr_description(diff_content, pr_number)

        # Write the generated PR description to a file
        with open("pr_description.txt", "w") as f:
            f.write(pr_body)

        print("PR description saved successfully.")

    except FileNotFoundError:
        print(f" Error: Diff file '{diff_file_path}' not found.")
        sys.exit(1)

    except Exception as e:
        print(f" Unexpected Error: {e}")
        sys.exit(1)
