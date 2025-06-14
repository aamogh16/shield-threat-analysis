import sys
import os
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

  news_fetcher.fetch_article_data(key)


if __name__ == "__main__":
  test()