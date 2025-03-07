from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

# Initialize FastAPI
app = FastAPI()

# Request model
class PromptRequest(BaseModel):
    model: str
    prompt: str

# Ensure API Server URL is set
FAST_API_SERVER_URL = os.getenv("FAST_API_SERVER_URL", "http://localhost:11434/api/generate")

@app.get("/")
def home():
    return {"message": "LLM API is running via FastAPI & ngrok!"}

@app.post("/generate")
def generate_text(request: PromptRequest):
    """
    Sends a prompt to the appropriate LLM API and returns the response.
    """
    try:
        model = request.model.lower()

        if model not in ["deepseek-r1", "llama3.3", "mistral"]:
            raise HTTPException(status_code=400, detail=f"Unsupported model: {model}")

        payload = {
            "model": model,
            "prompt": request.prompt,
            "stream": False
        }
        print(f"Debug: Forwarding request to {model} API at {FAST_API_SERVER_URL}")

        response = requests.post(FAST_API_SERVER_URL, json=payload)
        response_json = response.json()

        print(f"Debug: Received response from {model} API: {response_json}")

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Error calling {model} API")

        # Ensure response contains expected key
        generated_text = response_json.get("response", "").strip()

        if not generated_text:
            generated_text = f"Warning: {model} returned an empty response."

        return {"response": generated_text}

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
