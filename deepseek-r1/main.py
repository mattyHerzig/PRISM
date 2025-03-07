
import os
import requests
import sys
import json

FAST_API_URL = os.getenv("FAST_API_URL")

def generate_pr_description(diff_content, pr_number):
    if not FAST_API_URL:
        print("Error: FAST_API_URL is not set.")
        return "Error: FAST_API_URL is not configured."


    prompt=f"These are the code changes: \n\nPR Summary: \nPR #{pr_number}\n\nCode Changes:\n{diff_content}."
    
    prompt += """

And give an overall score based on Readability, Maintainability, and Clarity. 

The return format should be in the below json format:
{
    "readability_score": “<score within 1-3>”,
    "output": "<text explanation of the reason for the scoring and suggested improvements>”
} 

Be careful while analyzing the code. Make sure to identify all the code changes and double-check the answer. Use the checkboxes and scoring criteria below while assigning the score.

—

These are the code changes:
PR Summary: \nPR #{pr_number}\n\nCode Changes:\n{diff_content}.

Checkboxes: 
1. Clear Naming Conventions (Function and variable names are meaningful, self-explanatory and easy to understand.)
2. Documentation (Code includes meaningful inline comments explaining logic and purpose.)
3. Formatting & Styling (Code follows consistent indentation and spacing.)
4. Maintainability (Code is easy to extend or modify.)
5. Code Length (Logic is broken down into simpler parts.)

Scoring Criteria:
- 3 (Excellent): Code meets all readability, maintainability, and clarity standards. Naming is clear, documentation is informative, formatting is consistent, code structure is easy to modify, and functions are not excessively long.  
- 2 (Moderate): Code is largely readable and maintainable but has a scope for improvement.  
- 1 (Poor): Code is highly unreadable.

"""
    prompt += """
    
2. And give an overall score based on Robustness and Error handling. 

The return format should be in the below json format:
{
    "robustness_score": “<score within 1-3>”,
    "output": "<text explanation of the reason for the scoring and suggested improvements>”
} 

Be careful while analyzing the code. Make sure to identify all the code changes and double-check the answer. Use the checkboxes and scoring criteria below while assigning the score.

—

These are the code changes:
PR Summary: \nPR #{pr_number}\n\nCode Changes:\n{diff_content}.

Checkboxes:
1. Error Finding (No syntax, runtime and logical errors in the code.)
2. Error Handling (Code uses `try-except` for handling exceptions properly if applicable)
3. Edge Cases (Correctly handles edge cases like extreme, unusual, or unexpected inputs)
4. Input Validation (Code checks for invalid inputs)
5. No Infinite Loops (Code ensures that loops have a proper termination condition to avoid endless execution if found)

Scoring Criteria:
	⁃ 3 (Excellent): No errors found and follows all the checkboxes.
	⁃ 2 (Moderate): A few errors found and mostly follows the checkboxes. 
	- 1 (Poor): A lot of errors found and does not follow the checkboxes.

"""
    prompt += """

3. And give an overall score based on Security and Vulnerability. 
The return format should be in the below json format:
{
    "security_score": “<score within 1-3>”,
    "output": "<text explanation of the reason for the scoring and suggested improvements>”
} 

Be careful while analyzing the code. Make sure to identify all the code changes and double-check the answer. Use the checkboxes and scoring criteria below while assigning the score.

—

These are the code changes:
PR Summary: \nPR #{pr_number}\n\nCode Changes:\n{diff_content}.

Checkboxes:
1. No Security Threats Code does not have injection flaws like SQL injection, Code injection, Command injection, XSS and other injections, buffer overflows, insecure data storage, improper input validation, race conditions, logic flaws, authorization issues, information leakage, denial-of-service (DoS) vulnerabilities, unpatched software, misconfigurations, and hardcoded credentials)
2. No Authentication & Authorization issues
3. No Hard Coded Secrets (There isn’t any hardcoded credentials, API keys, or sensitive information)
4. No Secure Dependencies (There isn’t outdated and insecure third-party libraries)
5. Proper Session Management (Session expiration is perfect and handle token handling securely)

Scoring Criteria:
	⁃ 3 (Excellent): No security or vulnerability issues and follows all the checkboxes.
	⁃ 2 (Moderate): A few security or vulnerability issues and mostly follows checkboxes.
	⁃ 1 (Poor): A lot of security and vulnerability issues and does not follows all checkboxes.


"""
      prompt += """
4. And give an overall score based on Performance and Efficiency. 

The return format should be in the below json format:
{
    "performance_score": “<score within 1-3>”,
    "output": "<text explanation of the reason for the scoring and suggested improvements>”
} 

Be careful while analyzing the code. Make sure to identify all the code changes and double-check the answer. Use the checkboxes and scoring criteria below while assigning the score.

—

These are the code changes:
PR Summary: \nPR #{pr_number}\n\nCode Changes:\n{diff_content}.

Checkboxes: 
1. Improved Time Complexity (Code runs more efficiently than before.)
2. Improved Space Complexity (Code uses less memory than before.)
3. No Redundant Computation (No unnecessary and unused loops, recalculations, or duplicate operations, methods, and variables)


Scoring Criteria:
- 3 (Excellent): The code has improved either time complexity or space complexity and there are no unnecessary computations. 
- 2 (Moderate): The code has not improved time or space complexity and slightly follows checkboxes.
- 1 (Poor): The code reduces the time or space complexity and does not follow any of the checkboxes.
"""
    try:
        print(f" Sending request to FAST_API_URL: {FAST_API_URL}")
        
        response = requests.post(FAST_API_URL, json={"model": "deepseek-r1", "prompt": prompt})
        
        if response.status_code != 200:
            print(f" Error: Received status code {response.status_code} from FAST API")
            return "Error generating PR description."

        response_json = response.json()
        print(" Debug: Full response from FastAPI:", json.dumps(response_json, indent=2))

        # Extract response text safely
        generated_text = response_json.get("response", "No content from deepseek.")
        
        if not generated_text.strip():
            print("Warning: FASTAPI API returned an empty response.")
            return "No content from deepseek."

        return generated_text

    except requests.exceptions.RequestException as e:
        print(f" Error: Failed to reach FAST API - {e}")
        return "Error: Unable to contact FAST API."

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
