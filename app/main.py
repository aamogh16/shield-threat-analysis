from datetime import datetime, timedelta
from fastapi import FastAPI
from dotenv import load_dotenv
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from starlette.responses import PlainTextResponse

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


@app.get("/api/threats/recent", response_model=List[ThreatResponse])
def get_recent_threats(days: int = 3, db: Session = Depends(get_db)):
  """Gets all 'recent' threats (default last 3 days)"""
  cutoff_date = datetime.now() - timedelta(days=days)
  threats = db.query(Threat).filter(Threat.created_at >= cutoff_date).all()
  return threats


@app.get("/api/threats/search")
def search_threats(q: str, db: Session = Depends(get_db)):
  """Search threats by keywords in title or summary"""
  threats = db.query(Threat).filter(
      (Threat.title.contains(q)) | (Threat.ai_summary.contains(q))
  ).all()
  return threats


@app.get("/api/threats/fury-overview", response_class=PlainTextResponse)
def fury_overview(db: Session = Depends(get_db)):
  """Overview for Director Fury, to get a general idea of all threats"""
  cutoff_date = datetime.now() - timedelta(days=3)
  threat_count = db.query(Threat).count()
  high_threat_count = db.query(Threat).filter(Threat.ai_threat_level >= 7).count()
  recent_threats = db.query(Threat).filter(Threat.created_at >= cutoff_date).all()
  recent_categories = db.query(Threat.ai_category).filter(
      Threat.created_at >= cutoff_date
  ).distinct().all()
  threat_titles = [threat.title for threat in recent_threats]
  category_names = [cat[0] for cat in recent_categories]
  shield_logo = """
                       AAAAAAAAA                       
                 AAAAAAAAAAAAAAAAAAAAA                 
             AAAAAAAAAAAGQWYXQHAAAAAAAAAAA             
          AAAAAAAA                   AAAAAAA           
        AAAAAAM                         OAAAAAA        
      AAAAAA                               AAAAAA      
     AAAAB  B             FAAAAAO            BAAAA     
   AAAAA  BAAAA          AAAAAZ         XAAAC  AAAAA   
  AAAAA  AAAAAAAAV      AAAAAAA       FAAAAAAA  AAAAA  
  AAAA W  GAAAAAAAAK   EAAAAAAAA   SAAAAAAAAAA   AAAA  
 AAAA SAAM  AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAZ  A  AAAA 
 AAAZ AAAAA  KAAAAAAAAAAAAAAAAAAAAAAAAAAAAF  AAAA YAAAA
AAAA BAAAB BA  AAAAAAAAAAAAAAAAAAAAAAAAAF  NAAAAAF AAAA
AAAN AAG LAAAA   AAAAAAAAAAAAAAAAAAAAAA  SAA GAAAA MAAA
AAAX Q JAAAAAAAU  EAAAAAAAAAAAAAAAAAA   AAAAADVFAA YAAA
AAAX FAAAAAAAATXA   AAAAAAAAAAAAAAA    NAAAAAAABSL YAAA
AAAN AAAAAAAG BAAAA  XAAAAAAAAAAAP  LAAM AAAAAAAAB MAAA
AAAA BAAAAA EAAAAAAA   AAAAAAAAA   AAAAAA MAAAAAAD AAAA
 AAAY AAA SAAAAAAAA      AAAAA     RAAAAAAA AAAAA XAAAA
 AAAA MG AAAAAAAA     AA  IA   AA    AAAAAAANZAA  AAAA 
  AAAA XAAAAAAAB    LAAAAD   AAAAA    AAAAAAAAY  AAAA  
  AAAAA WAAAAAT    AAAAAAAAAAAAAAAA    AAAAAAA  AAAAA  
    AAAAX AAA     AAAAAAAAAAAAAAAAAAG   JAAAB  AAAA    
     AAAAB      QAAAAAAAAAAAAAAAAAAAAB   RA  BAAAA     
      AAAAAB   EAAAAAAAAAAAAAAAAAAAAAAA    BAAAAA      
        AAAAAAJ  AAAAAAAAAAAAAAAAAAAAA  MAAAAAA        
           AAAAAAA   VAAAAAAAAAAAY   AAAAAAA           
             AAAAAAAAAAAAJQSQJAAAAAAAAAAAA             
                 AAAAAAAAAAAAAAAAAAAAA                 
                        AAAAAAA                        
  
  """

  return (f"{shield_logo} \nHello Director Fury, welcome to the S.H.I.E.L.D. Threat Modeling System.\n"
          f"There are currently {threat_count} threats that S.H.I.E.L.D. is monitoring in our database.\n"
          f"S.H.I.E.L.D. analysis has determined that {high_threat_count} of these are HIGH level threats.\n"
          f"This is a list of recent threats that S.H.I.E.L.D. has been monitoring for the last three days: {threat_titles}\n"
          f"This is a list of the recent categories of threats: {category_names}\n"
          f"Have a good day Director Fury.")


@app.get("/api/threats/pending_review", response_model=List[ThreatResponse])
def get_threats_to_review(db: Session = Depends(get_db)):
  """Get all threats that a human should review if AI analysis presents low confidence."""
  review_threats = db.query(Threat).filter(Threat.requires_review).all()
  return review_threats


@app.put("/api/threats/{threat_id}/review")
def review_threat(threat_id: int, review_data: ThreatOverride, db: Session = Depends(get_db)):
  """Human review/override of a threat"""
  threat = db.query(Threat).filter(Threat.id == threat_id).first()
  if not threat:
    raise HTTPException(status_code=404, detail="Threat not found")

  # update with human review
  threat.human_threat_level = review_data.human_threat_level
  threat.human_category = review_data.human_category
  threat.human_notes = review_data.human_notes
  threat.reviewed_by = review_data.reviewed_by
  threat.reviewed_at = datetime.now()

  db.commit()
  return {"message": "Threat reviewed successfully"}


@app.get("/api/threats/level/{min_level}", response_model=List[ThreatResponse])
def get_threats_by_level(min_level: int, db: Session = Depends(get_db)):
  """Get threats at or above a certain threat level"""
  threats = db.query(Threat).filter(Threat.ai_threat_level >= min_level).all()
  return threats


@app.get("/api/threats/{threat_id}", response_model=ThreatResponse)
def get_one_threat(threat_id: int, db: Session = Depends(get_db)):
  """Get a specific threat by its ID"""
  threat = db.query(Threat).filter(Threat.id == threat_id).first()
  if not threat:
    raise HTTPException(status_code=404, detail="Threat not found")
  return threat