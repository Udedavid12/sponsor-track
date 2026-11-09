import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_id = Column(String, index=True) # Adzuna's job ID
    source = Column(String, default="adzuna")
    
    title = Column(String, nullable=False)
    company_name = Column(String)
    location = Column(String)
    description = Column(Text)
    apply_url = Column(String)
    
    # Sponsorship fields (we'll fill these in Phase 3)
    sponsorship_score = Column(Integer, default=0)
    sponsorship_category = Column(String, default="UNKNOWN")
    
    ingested_at = Column(DateTime, default=datetime.utcnow)