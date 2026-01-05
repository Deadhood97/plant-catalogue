# Home Plant Catalogue

A personal, AI-assisted catalogue of plants in my home. This project automates plant identification, metadata extraction, and provides both a static site and a dynamic serverless backend for community uploads.

---

## 🌟 Features

- **AI-Powered Plant Identification** using OpenAI Vision API
- **The Uncertainty Model (Visual Honesty)** - UI visually communicates AI confidence using grayscale and blur effects for lower-confidence specimens.
- **Wikipedia Integration** - Automatic external reading links for every plant, with smart reliability warnings.
- **Botanical Journal UI** - Professional glassmorphic design inspired by vintage herbariums.
- **Serverless Cloud Backend** - Robust AWS-native architecture (Lambda, S3, API Gateway).
- **Interactive Detail Modals** - Comprehensive care instructions, symbolism, and personality traits.
- **Performance Optimized** - Bundled data loading and web-optimized thumbnails.

---

## ☁️ Architecture (AWS Serverless)

This project is fully cloud-native, ensuring scalability and cost-efficiency:
- **Compute**: **AWS Lambda** (Python 3.10) running via Mangum.
- **Database**: **PostgreSQL** (Managed via Neon.tech).
- **File Storage**: **AWS S3** for persistent specimen image hosting.
- **API Gateway**: Secure RESTful interface for the frontend.
- **Infrastructure**: Defined via **AWS SAM** (Serverless Application Model).

---

## Project Structure

```
plant-catalogue/
├── backend/              # serverless backend code
│   ├── main.py           # Lambda handler & API routes
│   └── database.py       # SQLAlchemy models (Postgres/SQLite)
├── template.yaml         # AWS SAM Infrastructure definition
├── scripts/              # Automation tools
│   ├── backfill_wiki_urls.py # Update records with Wikipedia links
│   ├── batch_identify_plants.py # Batch processing CLI
│   └── bundle_data.py        # Optimized JSON bundling
├── data/                 # Personal collection metadata (JSON)
├── assets/               # CSS and Shared JS
│   └── js/
│       ├── common.js     # Config & API endpoints
│       └── catalogue.js  # Core rendering & Uncertainty logic
├── index.html            # Main Entry Point
└── README.md
```

---

## 🚀 Deployment

### Cloud Backend (AWS)

1. **Build the Stack**:
   ```bash
   sam build
   ```
2. **Deploy**:
   ```bash
   sam deploy --parameter-overrides "DatabaseUrl='...' OpenAiApiKey='...'"
   ```

### Static Frontend (GitHub Pages)

The catalogue is hosted on GitHub Pages and connects to the AWS API automatically.
- **Personal Plants**: Synced via the `data/` folder.
- **Public Plants**: Fetched live from the AWS Lambda API.

---

## 🧪 Visual Honesty & Integrity

The conservatory uses a unique **Uncertainty Model** to build trust:
*   **🌟 Very Confident (90%+)**: Displayed in full, vivid color.
*   **🔍 Uncertain (60-74%)**: Applied with a 60% grayscale filter.
*   **⚠️ Guessing (<60%)**: Applied with heavy grayscale and a 3px blur.
*   **Interactive Reveal**: Hovering over an uncertain plant restores its color and clarity temporarily.

---

## 📜 Metadata Schema

Each plant specimen contains:
- `identified_name`, `scientific_name`, `confidence`
- `wiki_url`: Direct link to Wikipedia
- `care`: Watering frequency, sunlight, soil type, and growth rate
- `plant_personality`: Fun "vibe" description (e.g., "Drama Queen")
- `symbolism`, `fun_fact`, `is_flowering`, `is_toxic_to_pets`

---

## 🤝 Tech Stack

- **Frontend**: HTML5, Vanilla JS, Tailwind CSS
- **Backend**: AWS Lambda, API Gateway
- **Database**: PostgreSQL (Neon)
- **AI**: OpenAI GPT-4o-mini
- **Storage**: AWS S3

---

_Last updated: January 2026_
