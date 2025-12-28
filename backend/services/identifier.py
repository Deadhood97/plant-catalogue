import os
import json
import base64
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# Load env vars from project root
load_dotenv()

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROMPT = """\
You are a careful plant identification assistant.

From the provided image:
- Identify up to 3 likely plant species, ordered by confidence
- These are candidate identifications
- Then choose the highest-confidence candidate as the primary identification

Return ONLY valid JSON matching the schema below.

Schema:
{
  "candidate_identifications": [
    {
      "identified_name": "",
      "scientific_name": "",
      "confidence": 0.0
    }
  ],
  "identified_name": "",
  "scientific_name": "",
  "local_names": [
    {
      "name": "",
      "language": "",
      "region": "",
      "confidence": 0.0
    }
  ],
  "confidence": 0.0,
  "fun_fact": {
    "text": "",
    "confidence": 0.0,
    "category": ""
  },
  "is_flowering": null,
  "is_medicinal": null,
  "is_edible": null,
  "is_toxic_to_pets": null,
  "plant_type": "",
  "environment": "",
  "difficulty": "",
  "care": {
    "watering_frequency": "",
    "sunlight_requirement": "",
    "soil_type": "",
    "growth_rate": "",
    "hardiness_zone": ""
  },
  "origin_region": "",
  "plant_personality": "",
  "fragrance": "",
  "symbolism": "",
  "lifespan": "",
  "reference_image": {
    "url": "",
    "source": "",
    "license": ""
  },
  "date_added": ""
}

Rules:
- candidate_identifications must contain 1 to 3 entries
- Order candidate_identifications by descending confidence
- Use the FIRST candidate as the primary identification
- identified_name and scientific_name must match the first candidate
- confidence must equal the first candidate’s confidence
- Attributes (flowering, edible, medicinal, toxic, plant_type, environment, difficulty) must be based ONLY on the first candidate
- NEW: Fill in the "care" object with specific advice for the primary identification
- NEW: "plant_personality" should be a fun, short "vibe" description (e.g., "Drama Queen", "Low Maintenance Buddy")
- NEW: "symbolism" should include cultural or historical meanings
- NEW: "fragrance" should describe the scent or "None"
- If overall confidence < 0.6, set identified_name to "unknown" and leave candidate_identifications empty
- Local names should correspond ONLY to the primary identification
- Local name should be an Indian local name if available
- Include multiple local names only if they are commonly used
- Each local name must include a confidence score
- Prefer empty lists over guessing for local_names
- Include at most ONE fun_fact
- The fun_fact should be cultural, historical, gardening-related, or aesthetic
- Examples include symbolism, use in famous gardens, architecture, folklore, or popular culture
- Do NOT include medical advice, instructions, or safety claims in fun_fact
- fun_fact must relate ONLY to the primary identification
- If unsure, omit the fun_fact or set its confidence below 0.6
- Do not invent medicinal, edible, or toxic claims
- Prefer nulls or empty fields over guessing
"""

def identify_plant_from_file(file_path: str) -> dict:
    """
    Reads an image file, sends it to OpenAI for identification, and returns the parsed JSON.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Read and encode image
    with open(file_path, "rb") as f:
        image_bytes = f.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    image_data_url = f"data:image/jpeg;base64,{image_base64}"

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": PROMPT},
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": "Identify the plant from this image."},
                        {"type": "input_image", "image_url": image_data_url}
                    ]
                }
            ]
        )

        # Parse JSON output
        text_output = response.output_text.strip()
        data = json.loads(text_output)
        
        # Add timestamps if not present (though prompt usually doesn't, we add it here)
        if not data.get("date_added"):
             data["date_added"] = datetime.utcnow().isoformat() + "Z"

        return data

    except json.JSONDecodeError:
        # Fallback query or simple error handling could go here
        raise ValueError("Failed to parse JSON response from AI")
    except Exception as e:
        raise e
