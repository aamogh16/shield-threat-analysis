from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean, JSON
from sqlalchemy.sql import func
from app.database import Base

class Threat(Base):
  __tablename__ = "threats"

  # Primary key
  id = Column(Integer, primary_key=True, index=True)

  # Original article information (from news source)
  title = Column(String(500), nullable=False)
  description = Column(Text, nullable=True)
  source = Column(String(100), nullable=False)
  source_url = Column(String(500), unique=True, nullable=False)  # Unique prevents duplicate articles
  published_at = Column(DateTime, nullable=True)

  # AI Analysis Results - REQUIRED fields (nothing gets stored without AI analysis)
  ai_threat_level = Column(Integer, nullable=False)  # 1-10 scale from AI
  ai_category = Column(String(50), nullable=False)   # cyber, environmental, etc.
  ai_summary = Column(Text, nullable=False)          # AI's explanation
  ai_confidence = Column(Float, nullable=False)      # 0.0-1.0 how sure AI is
  ai_keywords = Column(JSON, nullable=False)         # ["keyword1", "keyword2"]
  ai_reason = Column(Text, nullable=False)

  # Human Override Fields - OPTIONAL (only filled if human reviews)
  human_threat_level = Column(Integer, nullable=True)     # NULL unless human overrides
  human_category = Column(String(50), nullable=True)      # NULL unless human overrides
  human_notes = Column(Text, nullable=True)               # Human's explanation for override
  reviewed_by = Column(String(100), nullable=True)        # Username of reviewer
  reviewed_at = Column(DateTime, nullable=True)           # When human reviewed

  # System metadata
  created_at = Column(DateTime(timezone=True), server_default=func.now())
  updated_at = Column(DateTime(timezone=True), onupdate=func.now())

  # Flags
  requires_review = Column(Boolean, default=False)    # Flag if AI confidence is low

  # Computed properties for the API response
  @property
  def threat_level(self):
    """Returns the final threat level - human override takes precedence"""
    if self.human_threat_level is not None:
      return self.human_threat_level
    return self.ai_threat_level

  @property
  def category(self):
    """Returns the final category - human override takes precedence"""
    if self.human_category is not None:
      return self.human_category
    return self.ai_category

  @property
  def summary(self):
    """Always returns AI summary (we don't override summaries)"""
    return self.ai_summary

  @property
  def confidence(self):
    """Returns AI confidence score"""
    return self.ai_confidence

  @property
  def has_human_review(self):
    """Boolean flag indicating if a human has reviewed this threat"""
    return self.reviewed_by is not None

  def __repr__(self):
    """String representation for debugging"""
    return f"<Threat(id={self.id}, title='{self.title[:50]}...', level={self.threat_level})>"