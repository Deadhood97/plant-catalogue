from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import shutil
import os
import uuid
from datetime import datetime

from backend.database import engine, Base, SessionLocal, PublicPlant
from backend.services.identifier import identify_plant_from_file

# Lambda & Cloud imports
try:
    from mangum import Mangum
except ImportError:
    Mangum = None
import boto3

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

if Mangum:
    handler = Mangum(app)

# Enable CORS (since frontend is on :8000 and backend on :8001)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev, allow all. In prod, strict source.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Uploads directory
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Mount uploads dir to serve images
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/upload")
async def upload_plant(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Receives an image, saves it, runs AI ID, saves to DB, returns JSON.
    """
    try:
        # 1. Save File
        file_ext = file.filename.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 2. Run AI Identification
        plant_data = identify_plant_from_file(file_path)
        
        # 3. Augment Data (set reference image to the public URL)
        bucket_name = os.getenv("BUCKET_NAME")
        
        if bucket_name:
            # S3 Upload
            s3 = boto3.client('s3')
            s3.upload_file(file_path, bucket_name, unique_filename)
            file_url = f"https://{bucket_name}.s3.amazonaws.com/{unique_filename}"
            # Clean up local temp file
            os.remove(file_path)
        else:
            # Local Upload
            base_url = os.getenv('BASE_URL', 'http://localhost:8001')
            file_url = f"{base_url}/uploads/{unique_filename}"

        plant_data["reference_image"] = {
            "url": file_url,
            "source": "public_upload",
            "license": "public"
        }

        # 4. Generate Wikipedia URL
        import urllib.parse
        wiki_name = plant_data.get("scientific_name") or plant_data.get("identified_name")
        if wiki_name:
            encoded_name = urllib.parse.quote(wiki_name.replace(" ", "_"))
            plant_data["wiki_url"] = f"https://en.wikipedia.org/wiki/{encoded_name}"
        
        # 5. Save to Database (ONLY if not unknown)
        if plant_data.get("identified_name", "").lower() != "unknown":
            db_plant = PublicPlant(
                filename=unique_filename,
                data=plant_data
            )
            db.add(db_plant)
            db.commit()
            db.refresh(db_plant)
        
        return plant_data

    except Exception as e:
        print(f"Error during upload: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/public-plants")
def get_public_plants(db: Session = Depends(get_db)):
    """
    Returns list of all public plants, excluding "unknown" identifications.
    """
    plants = db.query(PublicPlant).order_by(PublicPlant.uploaded_at.desc()).all()
    # Filter out any existing unknown entries in Python for simplicity
    return [p.data for p in plants if p.data.get("identified_name", "").lower() != "unknown"]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
