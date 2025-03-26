class PrBodyGenerator:
    def __init__(self, prompt):
        """
        Initializes the PR body generator with a prompt.
        """
        self.prompt = prompt
        self.body = ""

    def generate_body(self):
        """
        Generates the PR body by setting the prompt text as the body.
        """
        self.body = self.prompt.text
