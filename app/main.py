from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.database import get_db
from app.models.threat import Threat
from app.schemas.threat import ThreatResponse, ThreatOverride, ArticleData, AIAnalysisResult

# loading environment variables
load_dotenv()

# creating a FastAPI app
app = FastAPI(
    title="S.H.I.E.L.D. Threat Analysis Platform",
    description="AI-powered threat monitoring system",
    version="0.1.0"
)

@app.get("/")
def read_root():
  return {
    "message": "S.H.I.E.L.D. Threat Analysis Platform ACTIVE",
    "status": "operational",
    "clearance_level": "public"
  }

@app.get("/api/threats", response_model=List[ThreatResponse])
def get_all_threats(db: Session = Depends(get_db)):
  """Get all threats that AI has identified"""
  threats = db.query(Threat).all()
  return threats

@app.get("/api/threats/count")  # MOVED THIS BEFORE {threat_id}
def count_threats(db: Session = Depends(get_db)):
  """How many threats do we have?"""
  total = db.query(Threat).count()
  return {"total_threats": total}

@app.get("/api/threats/{threat_id}", response_model=ThreatResponse)  # NOW THIS IS LAST
def get_one_threat(threat_id: int, db: Session = Depends(get_db)):
  """Get a specific threat by its ID"""
  threat = db.query(Threat).filter(Threat.id == threat_id).first()
  if not threat:
    raise HTTPException(status_code=404, detail="Threat not found")
  return threat