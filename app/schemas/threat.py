from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# What comes from news sources, this is the raw data we have to process through AI
class ArticleData(BaseModel):
  title: str
  description: Optional[str] = None
  url: str
  source: str
  published_at: Optional[datetime]

# What AI returns after analysis
class AIAnalysisResult(BaseModel):
  is_threat: bool
  threat_level: int  # 1-10, AI-determined
  category: str  # AI-determined
  summary: str  # AI-generated
  keywords: List[str]
  confidence: float  # 0-1, how sure AI is

# What gets stored in database (combination of article and AI analysis)
class ThreatCreate(BaseModel):
  # Original article info
  title: str
  description: Optional[str] = None
  source: str
  source_url: str
  published_at: Optional[datetime] = None

  # AI-determined fields (required because AI must analyze first)
  ai_threat_level: int
  ai_category: str
  ai_summary: str
  ai_confidence: float
  ai_keywords: List[str]

  # Location if detected
  location: Optional[str] = None

# Human override (for later)
class ThreatOverride(BaseModel):
  threat_level: Optional[int] = None
  category: Optional[str] = None
  notes: Optional[str] = None

# What API returns - clean and simple
class ThreatResponse(BaseModel):
  id: int
  title: str
  description: Optional[str]
  source: str
  source_url: str

  # Only show final values (not the AI/human breakdown)
  threat_level: int  # This will be the final value
  category: str      # This will be the final value
  summary: str       # AI summary is always shown

  # Metadata
  location: Optional[str]
  created_at: datetime

  # Useful flags
  confidence: float  # So users know how sure AI was
  has_human_review: bool  # Just a boolean, not the details

  class Config:
    from_attributes = True