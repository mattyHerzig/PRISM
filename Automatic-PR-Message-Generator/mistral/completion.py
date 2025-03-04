import os
import requests
import logging

class Completion:
    """
    This class interacts with a text generation API to generate a PR description based on a given prompt.
    """

    def __init__(self, prompt):
        """
        Initializes the Completion object with a prompt.

        Args:
            prompt (str): The prompt text used to generate a response.
        """
        self.api_url = os.getenv("LLAMA_API_URL")  # API URL should be provided as an environment variable
        self.prompt = prompt
        self.result = ""

        if not self.api_url:
            raise ValueError("LLAMA_API_URL environment variable is not set")

    def _complete_prompt(self) -> str:
        """
        Sends the prompt to the text generation API and retrieves the generated text.

        Returns:
            str: The generated text from the API response.

        Raises:
            requests.RequestException: If there's an error in the API request.
        """
        logging.info(f"Sending prompt to API: {self.prompt}")
        headers = {
            "Content-Type": "application/json",
        }
        data = {
            "prompt": self.prompt,
            "model": "deepseek-r1"
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()  # Raise an error for bad responses
            generated_text = response.json()["generated_text"]
            logging.info(f"Received generated text: {generated_text}")
            return generated_text
        except requests.RequestException as e:
            logging.error(f"Error while generating text: {str(e)}")
            raise

    def complete(self):
        """
        Generates the completion text based on the prompt and updates the result attribute.
        """
        logging.info("Generating completion for prompt...")
        self.result = self._complete_prompt()
        logging.info(f"Completion result: {self.result}")

    def get_result(self) -> str:
        """
        Returns the result of the completion.

        Returns:
            str: The generated completion result.
        """
        return self.result

    def __repr__(self):
        """
        Provides a string representation of the Completion object.

        Returns:
            str: String representation of the object.
        """
        return f"Completion(prompt='{self.prompt}', result='{self.result}')"
