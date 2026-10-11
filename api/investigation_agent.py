from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

def investigate_transaction(explanations):

    feature_list = []

    for item in explanations:
        feature_list.append(
            f"{item['feature']} (impact: {item['impact']:.3f})"
        )

    feature_text = ", ".join(feature_list)

    prompt = f"""
You are a fraud investigation assistant.

The fraud detection model flagged a transaction.

Important features influencing the decision were:
{feature_text}

Write a short investigation summary explaining why this transaction may be suspicious.
"""

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction="You are a fraud investigation analyst.",
            temperature=0.2,
        ),
    )

    return response.text