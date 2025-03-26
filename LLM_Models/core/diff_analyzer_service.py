class DiffAnalyzerService:
    def __init__(self, diff_content):
        """
        Initializes the diff analyzer with diff content.

        Args:
            diff_content (str): The string content of the diff.
        """
        self.diff_content = diff_content

    def analyse_diff(self):
        """
        Analyzes the diff content and returns a structured summary.

        Returns:
            list: A list of dictionaries containing analyzed diff data for each file.
        """
        analysis = []
        current_file = None

        for line in self.diff_content.splitlines():
            if line.startswith('diff --git'):
                if current_file:
                    analysis.append(current_file)
                file_path = line.split()[-1]  # Get the file path (e.g., b/test_file.py)
                current_file = {"file": file_path, "changes": []}
            elif line.startswith('+') and not line.startswith('+++'):
                current_file["changes"].append({"type": "addition", "content": line[1:].strip()})
            elif line.startswith('-') and not line.startswith('---'):
                current_file["changes"].append({"type": "deletion", "content": line[1:].strip()})

        if current_file:
            analysis.append(current_file)

        return analysis
