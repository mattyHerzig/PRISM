class PullRequest:
    """
    A class to represent and manage pull request data, including updating the PR body.
    """

    def __init__(self, pr_id, body):
        """
        Initializes the PullRequest object with an ID and existing body content.

        Args:
            pr_id (int): The ID of the pull request.
            body (str): The current body content of the pull request.
        """
        self.pr_id = pr_id
        self.body = body

    def update_auto_body(self, new_body):
        """
        Updates the body of the pull request with a new generated description.

        Args:
            new_body (str): The new description to set as the PR body.
        """
        self.body = new_body

    def get_pr_data(self):
        """
        Returns a dictionary representation of the PR data.

        Returns:
            dict: A dictionary containing the PR ID and body.
        """
        return {
            "pr_id": self.pr_id,
            "body": self.body
        }

    def __str__(self):
        """
        Returns a string representation of the PR data.

        Returns:
            str: A string with the PR ID and body content.
        """
        return f"PR ID: {self.pr_id}\nBody:\n{self.body}"
