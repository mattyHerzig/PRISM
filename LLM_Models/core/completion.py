import os
import requests
import logging
import json

class Completion:
    def __init__(self, prompt):
        self.api_url = os.getenv("FAST_API_URL")  # API URL from env
        self.prompt = prompt
        self.result = ""
        self.model = self._load_model_name()

        if not self.api_url:
            raise ValueError("FAST_API_URL environment variable is not set")

    def _load_model_name(self) -> str:
        """Load selected model from model_config.json."""
        try:
            with open("model_config.json", "r") as f:
                config = json.load(f)
                return config.get("model", "")
        except Exception as e:
            logging.error(f"Failed to load model_config.json: {e}")
            raise

    def _complete_prompt(self) -> str:
        logging.info(f"Sending prompt to API: {self.prompt}")
        headers = {
            "Content-Type": "application/json",
        }
        data = {
            "prompt": self.prompt,
            "model": self.model
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            generated_text = response.json().get("generated_text") or response.json().get("response", "")
            logging.info(f"Received generated text: {generated_text}")
            return generated_text.strip()
        except requests.RequestException as e:
            logging.error(f"Error while generating text: {str(e)}")
            raise

    def complete(self):
        logging.info("Generating completion for prompt...")
        self.result = self._complete_prompt()
        logging.info(f"Completion result: {self.result}")

    def get_result(self) -> str:
        return self.result

    def __repr__(self):
        return f"Completion(prompt='{self.prompt}', result='{self.result}')"
