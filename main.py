from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import uuid

from database import get_db
from models import Job

app = FastAPI(title="SponsorTrack API")

# Pydantic schema for returning data
class JobResponse(BaseModel):
    id: uuid.UUID
    title: str
    company_name: Optional[str]
    location: Optional[str]
    apply_url: Optional[str]
    sponsorship_category: str
    sponsorship_score: int
    ingested_at: datetime

    class Config:
        from_attributes = True

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/jobs", response_model=List[JobResponse])
def get_jobs(
    sponsorship: Optional[str] = Query(None, description="Filter by LIKELY, UNKNOWN, or UNLIKELY"),
    location: Optional[str] = Query(None, description="Filter by city/province"),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db)
):
    """
    Search and filter jobs by sponsorship likelihood and location.
    """
    query = db.query(Job)

    # Apply filters if the user provided them
    if sponsorship:
        query = query.filter(Job.sponsorship_category == sponsorship.upper())
    
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))

    # Order by most recently ingested
    jobs = query.order_by(Job.ingested_at.desc()).limit(limit).all()
    return jobs