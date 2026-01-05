from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import PublicPlant
import json

engine = create_engine("sqlite:///backend/public_plants.db")
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

plants = db.query(PublicPlant).all()
print(f"Found {len(plants)} plants.")
for p in plants:
    print(f"ID: {p.id}")
    print(f"Filename: {p.filename}")
    print(f"Ref URL: {p.data.get('reference_image', {}).get('url')}")
    print("-" * 20)
