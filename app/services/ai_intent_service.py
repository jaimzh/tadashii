# app/services/ai_intent_service.py

import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def analyze_prompt(user_prompt: str):

    prompt = f"""
You are an anime intent parser for a recommendation system.

Analyze the user request and return ONLY valid JSON.

User prompt:
"{user_prompt}"

Return:

{{
  "search_keywords": [],
  "semantic_tags": [],
  "themes": [],
  "mood": "",
  "genres": [],
  "character_arc": ""
}}

Rules:

- search_keywords:
  Short searchable anime terms only.
  Must work well with anime databases.
  Examples:
  ["underdog", "training", "revenge", "friendship"]

- semantic_tags:
  Broader concepts and meanings.
  Examples:
  ["zero to hero", "self growth"]

- genres:
  Use real anime genres only

- maximum 5 keywords

Return JSON only.
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite", contents=prompt
    )

    return json.loads(response.text)
