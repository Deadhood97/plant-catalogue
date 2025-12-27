import os
import sys
import base64
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY not found in environment")

client = OpenAI(api_key=api_key)

if len(sys.argv) < 2:
    raise RuntimeError("Usage: python identify_one_plant.py <image_path>")

image_path = sys.argv[1]

with open(image_path, "rb") as f:
    image_bytes = f.read()

image_base64 = base64.b64encode(image_bytes).decode("utf-8")

image_data_url = f"data:image/jpeg;base64,{image_base64}"

prompt = """
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
- If overall confidence < 0.6, set identified_name to "unknown" and leave candidate_identifications empty
- Local names should correspond ONLY to the primary identification
- Include multiple local names only if they are commonly used
- Each local name must include a confidence score
- Local name should be an Indian local name if available
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

response = client.responses.create(
    model="gpt-4.1-mini",
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": prompt},
                {"type": "input_image", "image_url": image_data_url}
            ]
        }
    ]
)

raw_text = response.output_text

data = json.loads(raw_text)
data["reference_image"]["url"] = image_path
data["reference_image"]["source"] = "local"
data["date_added"] = datetime.utcnow().isoformat() + "Z"

print(json.dumps(data, indent=2))
