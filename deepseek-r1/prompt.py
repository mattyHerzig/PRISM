class Prompt:
    def __init__(self, diff_analysis, pr_summary):
        """
        Initializes the prompt with diff analysis and PR summary.
        """
        self.diff_analysis = diff_analysis  # Expecting this to be a list of dictionaries
        self.pr_summary = pr_summary
        self.text = self._create_prompt_text()

    def _create_prompt_text(self):
        """
        Create the prompt text based on the diff analysis.
        """
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
"""s


        for file_change in self.diff_analysis:
            file_name = file_change.get("file", "Unknown file")
            prompt_text += f"  - {file_name}:\n"
            for change in file_change.get("changes", []):
                change_type = change.get("type", "Unknown")
                content = change.get("content", "")
                prompt_text += f"    {change_type.capitalize()}: {content}\n"

        return prompt_text
