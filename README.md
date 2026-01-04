# Home Plant Catalogue

A personal, AI-assisted catalogue of plants in my home. This project automates plant identification, metadata extraction, and provides both a static site and a dynamic backend for community uploads.

---

## 🌟 Features

- **AI-Powered Plant Identification** using OpenAI Vision API
- **Beautiful Botanical Journal UI** with glassmorphic design
- **Detailed Plant Cards** with care instructions, symbolism, and personality traits
- **Interactive Detail Modals** for comprehensive plant information
- **Public Plants Upload** (Backend feature) - Community members can upload and identify their plants
- **Performance Optimized** - Bundled data loading, thumbnail-only images
- **Responsive Design** - Works beautifully on all devices

---

## Project Structure

```
plant-catalogue/
├── backend/              # FastAPI backend for public uploads
│   ├── main.py           # API routes (POST /upload, GET /public-plants)
│   ├── database.py       # SQLAlchemy models and DB setup
│   ├── services/
│   │   └── identifier.py # Shared AI identification logic
│   └── public_plants.db  # SQLite database (local development)
├── data/                 # Plant metadata JSON files
│   ├── all_plants.json   # Bundled data (performance optimization)
│   └── index.json        # File index for fallback loading
├── photos/               # Original images (local only, not in repo)
├── thumbnails/           # Web-optimized images (synced to GitHub)
├── uploads/              # User-uploaded images (backend feature)
├── scripts/              # Automation scripts
│   ├── batch_identify_plants.py  # Batch processing with AI
│   ├── bundle_data.py            # Create all_plants.json
│   ├── make_thumbnails.py        # Generate thumbnails
│   └── plant_schema.json         # Data schema definition
├── index.html            # Main web interface
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Deadhood97/plant-catalogue.git
   cd plant-catalogue
   ```

2. **Set up virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install openai python-dotenv Pillow fastapi uvicorn python-multipart sqlalchemy
   ```

4. **Configure API key:**
   Create a `.env` file:
   ```
   OPENAI_API_KEY=sk-...
   ```

---

## 📖 Usage

### View the Catalogue (Static)

1. **Start the frontend server:**
   ```bash
   python3 -m http.server 8000
   ```

2. **Open in browser:**
   ```
   http://localhost:8000
   ```

### Enable Public Uploads (Backend)

1. **Start the backend server:**
   ```bash
   ./venv/bin/python3 -m backend.main
   ```
   Backend runs on `http://localhost:8001`

2. **Start the frontend server** (in another terminal):
   ```bash
   python3 -m http.server 8000
   ```

3. **Upload plants:**
   - Navigate to `http://localhost:8000`
   - Scroll to "Public Collection"
   - Click "📸 Add Your Plant"
   - Upload an image → AI identifies it automatically!

---

## 🛠️ Workflow

### Adding Your Own Plants

1. **Add photos** to the `photos/` directory

2. **Run identification:**
   ```bash
   ./venv/bin/python scripts/batch_identify_plants.py
   ```
   - Processes all new images
   - Generates detailed JSON metadata in `data/`

3. **Generate thumbnails:**
   ```bash
   ./venv/bin/python scripts/make_thumbnails.py
   ```

4. **Bundle data for web:**
   ```bash
   ./venv/bin/python scripts/bundle_data.py
   ```

5. **Refresh the site** - Your plants now appear in the catalogue!

### Single Plant Identification

```bash
./venv/bin/python scripts/identify_one_plant.py path/to/image.jpg
```

---

## 🌐 Deployment

### GitHub Pages (Frontend Only)

The static catalogue is hosted at: **[Your GitHub Pages URL]**

This displays your personal plant collection with:
- ✅ Full botanical details
- ✅ Beautiful UI
- ✅ Fast loading (bundled data + thumbnails)

### Backend Deployment (Optional)

To enable the **Public Plants** upload feature on the live site:

1. **Deploy to Render** (free tier):
   - See `deployment_plan.md` for detailed steps
   - Requires: `requirements.txt` and `render.yaml`
   - Set `OPENAI_API_KEY` in Render dashboard

2. **Update frontend:**
   ```javascript
   // In index.html, change:
   const API_URL = 'https://your-app.onrender.com';
   ```

3. **Migrate to PostgreSQL** (recommended for production):
   - Render's free PostgreSQL prevents data loss on redeploys

---

## 🏠 Self-Hosting

Run your own instance of the Plant Catalogue with systemd and Nginx. This setup ensures the backend restarts automatically and serves the frontend on your local network.

### Prerequisites

- Linux (tested on Ubuntu/Debian)
- Python 3.8+
- Nginx

### Setup Guide

1.  **Helper Script**:
    Use the included setup script to configure everything automatically:
    ```bash
    sudo ./scripts/setup_service.sh
    ```
    *(Note: Ensure you have `setup_service.sh` if you made one, otherwise manual steps below)*
    
    **Manual Setup:**

    **Backend Service:**
    Copy `plant-backend.service` to `/etc/systemd/system/` and start it:
    ```bash
    sudo cp plant-backend.service /etc/systemd/system/
    sudo systemctl enable --now plant-backend
    ```

    **Monitoring Service:**
    (Optional) Start the Glances monitor:
    ```bash
    sudo cp plant-monitor.service /etc/systemd/system/
    sudo systemctl enable --now plant-monitor
    ```

    **Nginx Configuration:**
    Configure Nginx to serve the static site and proxy API requests:
    ```bash
    sudo cp nginx.conf /etc/nginx/sites-available/plant-catalogue
    sudo ln -s /etc/nginx/sites-available/plant-catalogue /etc/nginx/sites-enabled/
    sudo systemctl restart nginx
    ```

2.  **Access:**
    - Catalogue: `http://localhost` (or your server IP)
    - Backend API: `http://localhost/api`
    - Monitor: `http://localhost:61208`

---

## 📋 Scripts Reference

| Script | Purpose |
|--------|---------|
| `batch_identify_plants.py` | Batch process images in `photos/` |
| `identify_one_plant.py` | Identify a single plant |
| `make_thumbnails.py` | Generate web-optimized thumbnails |
| `bundle_data.py` | Create `all_plants.json` for performance |
| `generate_json_index.py` | Update `data/index.json` |

---

## 🎨 Design Philosophy

- **Botanical Journal Aesthetic** - Inspired by vintage plant catalogues
- **Glassmorphism** - Modern, elegant UI with frosted glass effects
- **Personality-Driven** - Each plant has a unique "vibe" (e.g., "Drama Queen", "Chill Roommate")
- **Mobile-First** - Responsive design that works beautifully on all devices
- **Performance-Focused** - Thumbnails, bundled data, lazy loading

---

## 🔒 Privacy & Data

- **Personal Collection** (`data/`): Your private plant data, synced to GitHub
- **Public Uploads** (`uploads/`, database): Community contributions (backend feature)
- **API Keys**: Never commit `.env` to git (already in `.gitignore`)
- **Photos**: Original `photos/` folder is gitignored to save repo space

---

## 🛡️ Schema

All plant metadata follows a strict JSON schema defined in `scripts/plant_schema.json`.

**Key Fields:**
- `identified_name`, `scientific_name`, `confidence`
- `care` (watering, sunlight, soil, growth rate)
- `plant_personality` (e.g., "Low Maintenance Buddy")
- `symbolism`, `fragrance`, `lifespan`
- `is_flowering`, `is_medicinal`, `is_edible`, `is_toxic_to_pets`

---

## 🤝 Contributing

This is a personal project, but feel free to:
- Fork it for your own plant collection
- Suggest improvements via Issues
- Share your deployed version!

---

## 📜 License

MIT License - Feel free to use this for your own plant catalogue!

---

## 🌱 Tech Stack

- **Frontend**: HTML, Tailwind CSS, Vanilla JavaScript, Nginx
- **Backend**: FastAPI, SQLAlchemy, SQLite/PostgreSQL, Systemd
- **AI**: OpenAI GPT-4 Vision API
- **Hosting**: GitHub Pages (frontend), Render (backend), Self-Hosted (Home Server)

---

_Last updated: 2025-12-28_
