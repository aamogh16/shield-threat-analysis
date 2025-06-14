import sys
import os

from app.schemas.threat import ListArticleData
from app.services.ai_analyzer import AIAnalyzer

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

from app.services.news_fetcher import NewsFetcher

load_dotenv()
key = os.getenv("NEWS_API_KEY")

def test():
  """
  random testing purposes
  """

  print("🛡️ Testing S.H.I.E.L.D. Threat API")
  print("-" * 50)

  news_fetcher = NewsFetcher()
  ai = AIAnalyzer()

  article_list = news_fetcher.fetch_and_convert()

  listarticledata = ListArticleData(
      articles=article_list
  )

  ai.analyze_articles(listarticledata)


if __name__ == "__main__":
  test()