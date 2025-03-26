import json

class PRParser:
    """
    Parses pull request data and provides structured information for generating PR descriptions.
    """

    def __init__(self, pr_data):
        """
        Initializes the PRParser with the pull request data.

        Args:
            pr_data (dict): Dictionary containing PR data (e.g., ID, title, body, changed files).
        """
        self.pr_id = pr_data.get("id")
        self.title = pr_data.get("title", "")
        self.body = pr_data.get("body", "")
        self.changed_files = pr_data.get("changed_files", [])
        self.author = pr_data.get("author", "")
        self.created_at = pr_data.get("created_at", "")
        self.language=pr_data.get("language")

    def get_summary(self):
        """
        Creates a summary of the PR details.

        Returns:
            str: A formatted summary of the PR.
        """
        summary = f"PR ID: {self.pr_id}\n"
        summary += f"Title: {self.title}\n"
        summary += f"Author: {self.author}\n"
        summary += f"Created At: {self.created_at}\n"
        summary += f"Changed Files: {len(self.changed_files)}\n"
        summary += f"language: {self.language}\n"
        return summary

    def get_changed_files(self):
        """
        Returns a list of file names that were changed in the PR.

        Returns:
            list: List of changed file names.
        """
        return [file['filename'] for file in self.changed_files]

    def parse_body(self):
        """
        Parses the PR body to extract relevant information if formatted data exists.

        Returns:
            str: The cleaned or structured PR body.
        """
        # Example: Extracting key sections if PR body follows a specific template
        if "## Description" in self.body:
            description = self.body.split("## Description")[1].split("##")[0].strip()
            return f"Description:\n{description}"
        return self.body.strip()

    def to_json(self):
        """
        Converts the parsed PR data into JSON format.

        Returns:
            str: JSON representation of the parsed PR data.
        """
        parsed_data = {
            "pr_id": self.pr_id,
            "title": self.title,
            "author": self.author,
            "created_at": self.created_at,
            "language":self.language,
            "changed_files": self.get_changed_files(),
            "summary": self.get_summary(),
            "body": self.parse_body(),
        }
        return json.dumps(parsed_data, indent=2)
