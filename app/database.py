from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# getting database URL from env, or just using sqlite as a default backup
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./shield.db")

# Neon (and some other Postgres hosts) gives a plain postgresql:// URL; SQLAlchemy
# needs the explicit psycopg2 driver prefix to avoid deprecation warnings on 2.x.
if SQLALCHEMY_DATABASE_URL.startswith("postgresql://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

# creating a database engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

# creating session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create base class for all models
Base = declarative_base()

# Dependency to get database session going
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()