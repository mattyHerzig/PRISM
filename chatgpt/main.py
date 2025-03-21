import os
import sys
import json
import openai

# Set OpenAI API key securely from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY is not set.")
    sys.exit(1)

openai.api_key = OPENAI_API_KEY

def query_chatgpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0.3
    )
    return response.choices[0].message['content'].strip()

def generate_pr_description(diff_content, pr_number):
    prompt=f"These are the code changes: \n\nPR Summary: \nPR #{pr_number}\n\nCode Changes:\n{diff_content}."
    
    # Load scoring instructions (same structure as before)
    with open('scoring_prompt.txt', 'r') as f:
        scoring_prompt = f.read()
    
    full_prompt = prompt + scoring_prompt

    try:
        generated_text = query_chatgpt(full_prompt)
        if not generated_text.strip():
            return "Model returned empty response."
        return generated_text

    except Exception as e:
        print(f"Error: Failed contacting ChatGPT API - {e}")
        return "Error: Unable to contact ChatGPT API."

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main.py <diff_file_path> <pr_number>")
        sys.exit(1)

    diff_file_path = sys.argv[1]
    pr_number = sys.argv[2]

    try:
        with open(diff_file_path, "r") as f:
            diff_content = f.read().strip()
        
        if not diff_content:
            print("Warning: Diff file empty.")
            pr_body = "No changes detected."
        else:
            pr_body = generate_pr_description(diff_content, pr_number)

        with open("pr_description.txt", "w") as f:
            f.write(pr_body)

        print("PR description saved successfully.")

    except FileNotFoundError:
        print(f"Error: Diff file '{diff_file_path}' not found.")
        sys.exit(1)

    except Exception as e:
        print(f"Unexpected Error: {e}")
        sys.exit(1)
