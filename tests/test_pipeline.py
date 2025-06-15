import sys
import os
from datetime import datetime

from app.services.news_fetcher import NewsFetcher

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.schemas.threat import ArticleData
from app.services.threat_processor import ThreatProcessor
from app.database import get_db
from app.models.threat import Threat

def test_pipeline():
  """
  should test full api functionality from using fake articles to process through a fake AI,
  determing if articles are threats, then passing to database with information ready for
  a request of the data.
  """

  print("🛡️ Testing Full S.H.I.E.L.D. Threat API")
  print("-" * 50)

  # # creating fake article data: 2 with threat words, 1 with safe word,
  # # and 1 with a word thats not in either
  # threat_article1 = ArticleData(
  #     title="Attack at XYZ",
  #     description="Major security attack reported at downtown location",
  #     url="1",  # Fixed: added proper URL
  #     source="Amogh",
  #     published_at=datetime.now()
  # )
  # threat_article2 = ArticleData(
  #     title="Bomb at XYZ",
  #     description="Explosive device found at local facility",
  #     url="2",  # Fixed: added proper URL
  #     source="Abhi",
  #     published_at=datetime.now()
  # )
  # threat_article3 = ArticleData(
  #     title="Help at XYZ",
  #     description="Community",
  #     url="3",  # Fixed: added proper URL
  #     source="Rohit",
  #     published_at=datetime.now()
  # )
  # threat_article4 = ArticleData(
  #     title="Bottle at XYZ",
  #     description="New water bottle recycling program launched in the city",
  #     url="4",  # Fixed: added proper URL
  #     source="Saket",
  #     published_at=datetime.now()
  # )
  #
  # threats = [threat_article1, threat_article2, threat_article3, threat_article4]

  # fetching real news articles with newsfetcher object
  fetcher = NewsFetcher()
  db = next(get_db())
  threats = fetcher.fetch_and_convert(db)
  print(f"Processing {len(threats.articles)} test articles...\n")

  # establishing database connection

  db.query(Threat).delete()

  # creating a threat processor object
  processor = ThreatProcessor()

  # process all articles
  saved_threats = processor.process_articles(threats, db)

  print("\n" + "-" * 50)
  print("RESULTS:")
  print(f"Articles processed: {len(threats.articles)}")
  print(f"Threats detected and saved: {len(saved_threats)}")

  # checking if data is actually in the database
  threats_in_db = db.query(Threat).all()  # Fixed: Use Threat model, not threat schema
  print(f"Total threats in database: {len(threats_in_db)}")
  db.close()

if __name__ == "__main__":
  test_pipeline()