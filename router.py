import os
import json
import logging
from typing import Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.7"))

def load_prompts() -> Dict[str, str]:
    with open("prompts.json", "r") as f:
        return json.load(f)

PROMPTS = load_prompts()

CLASSIFIER_PROMPT = """Your task is to classify the user's intent. Based on the user message below, choose one of the following labels: code, data, writing, career, unclear. Respond with a single JSON object containing two keys: 'intent' (the label you chose) and 'confidence' (a float from 0.0 to 1.0, representing your certainty). Do not provide any other text or explanation."""

def classify_intent(message: str) -> Dict[str, Any]:
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": CLASSIFIER_PROMPT},
                {"role": "user", "content": message}
            ],
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        intent_data = json.loads(content)
        
        # Validate structure
        if "intent" not in intent_data or "confidence" not in intent_data:
            raise ValueError("Invalid JSON structure from LLM")
            
        return intent_data
    except Exception as e:
        logger.error(f"Error classifying intent: {e}")
        return {"intent": "unclear", "confidence": 0.0}

def route_and_respond(message: str, intent_data: Dict[str, Any]) -> str:
    intent = intent_data.get("intent", "unclear")
    confidence = intent_data.get("confidence", 0.0)

    # Apply confidence threshold
    if confidence < CONFIDENCE_THRESHOLD:
        intent = "unclear"

    system_prompt = PROMPTS.get(intent, PROMPTS["unclear"])

    if intent == "unclear":
        # For unclear intent, we don't necessarily need another LLM call if we have a static clarification,
        # but the requirements say "generate a response that asks for clarification".
        # Let's use the LLM to make it more natural if needed, or just use the static one.
        # Requirement: "The clarification question should guide the user toward a supported intent"
        return system_prompt

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return "I encountered an error while processing your request. Please try again later."

def log_request(intent: str, confidence: float, message: str, response: str):
    log_entry = {
        "intent": intent,
        "confidence": confidence,
        "user_message": message,
        "final_response": response
    }
    with open("route_log.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
