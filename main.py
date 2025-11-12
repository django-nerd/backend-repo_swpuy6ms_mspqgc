import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents

app = FastAPI(title="AWS Student Community Day 2025 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "AWS Student Community Day 2025 API running"}

# Public content endpoints
@app.get("/api/event")
def get_event():
    try:
        docs = get_documents("event", limit=1)
        if not docs:
            # Seed a default event if none exists
            seed = {
                "title": "AWS Student Community Day 2025",
                "tagline": "Learn. Build. Network.",
                "description": "A full-day community-led conference celebrating AWS technologies, hands-on learning, and networking.",
                "date": "2025-02-15",
                "start_time": "09:00 AM",
                "end_time": "05:30 PM",
                "venue": "Silver Oak University, Ahmedabad",
                "city": "Ahmedabad",
                "registration_open": True,
            }
            create_document("event", seed)
            docs = [seed]
        doc = docs[0]
        doc["_id"] = str(doc.get("_id", ""))
        return doc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/speakers")
def get_speakers():
    try:
        docs = get_documents("speaker")
        for d in docs:
            d["_id"] = str(d.get("_id", ""))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/schedule")
def get_schedule():
    try:
        docs = get_documents("session")
        for d in docs:
            d["_id"] = str(d.get("_id", ""))
        # Optional: sort by start time if available
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sponsors")
def get_sponsors():
    try:
        docs = get_documents("sponsor")
        for d in docs:
            d["_id"] = str(d.get("_id", ""))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Registration endpoint
class RegistrationPayload(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    institute: Optional[str] = None
    year: Optional[str] = None
    interests: Optional[List[str]] = None
    referral: Optional[str] = None
    consent: bool = True

@app.post("/api/register")
def register_user(payload: RegistrationPayload):
    try:
        reg = payload.model_dump()
        reg_id = create_document("registration", reg)
        return {"status": "ok", "id": reg_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
