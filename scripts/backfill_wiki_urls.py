import os
import urllib.parse
from sqlalchemy.orm import Session
from backend.database import SessionLocal, PublicPlant

def backfill():
    db: Session = SessionLocal()
    try:
        plants = db.query(PublicPlant).all()
        updated_count = 0
        
        for plant in plants:
            data = dict(plant.data or {})
            if "wiki_url" not in data:
                wiki_name = data.get("scientific_name") or data.get("identified_name")
                if wiki_name:
                    encoded_name = urllib.parse.quote(wiki_name.replace(" ", "_"))
                    data["wiki_url"] = f"https://en.wikipedia.org/wiki/{encoded_name}"
                    plant.data = data
                    updated_count += 1
        
        db.commit()
        print(f"Successfully backfilled {updated_count} plants with Wikipedia URLs.")
    except Exception as e:
        print(f"Error during backfill: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    backfill()
