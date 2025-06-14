import json
import os

from dotenv import load_dotenv
from datetime import datetime
import requests
from sqlalchemy import String

from app.schemas.threat import ArticleData


class NewsFetcher:

  def fetch_article_data(self, key):
    return requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={key}").json()

  def convert_data(self, article_data):
    res_articles = []
    for article in article_data["articles"]:
      date_time = article.get("publishedAt")

      res = ArticleData (
          title=article.get("title"),
          description=article.get("description"),
          url=article.get("url"),
          source=article.get("source").get("name"),
          published_at=datetime.fromisoformat(date_time[:19])
      )

      res_articles.append(res)

    return res_articles

  def fetch_and_convert(self):
    load_dotenv()
    apikey = os.getenv("NEWS_API_KEY")

    article_data = self.fetch_article_data(apikey)
    return self.convert_data(article_data)