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

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS (since frontend is on :8000 and backend on :8001)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev, allow all. In prod, strict source.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Uploads directory
UPLOAD_DIR = "uploads"
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
        
        # 3. Content Moderation - Reject if not a plant
        MIN_CONFIDENCE = 0.6  # Minimum confidence to accept
        
        if plant_data.get("confidence", 0) < MIN_CONFIDENCE:
            # Delete the uploaded file
            os.remove(file_path)
            raise HTTPException(
                status_code=400, 
                detail=f"Unable to identify a plant in this image (confidence: {plant_data.get('confidence', 0):.0%}). Please upload a clear photo of a plant."
            )
        
        if plant_data.get("identified_name", "").lower() == "unknown":
            os.remove(file_path)
            raise HTTPException(
                status_code=400,
                detail="Could not identify a plant in this image. Please upload a clear photo of a plant."
            )
        
        # 4. Augment Data (set reference image to the public URL)
        # Use BASE_URL env var for prod, fallback to localhost for dev
        base_url = os.getenv('BASE_URL', 'http://localhost:8001')
        plant_data["reference_image"] = {
            "url": f"{base_url}/uploads/{unique_filename}",
            "source": "public_upload",
            "license": "public"
        }
        
        # 5. Save to Database
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
    Returns list of all public plants.
    """
    plants = db.query(PublicPlant).order_by(PublicPlant.uploaded_at.desc()).all()
    # Return just the JSON data blobs
    return [p.data for p in plants]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
