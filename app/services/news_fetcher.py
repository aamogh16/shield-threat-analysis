import json
import os

from dotenv import load_dotenv
from datetime import datetime
import requests

from app.models.threat import Threat
from app.schemas.threat import ArticleData, ListArticleData


class NewsFetcher:

  def fetch_article_data(self, key):
    """
    Performs a request to get the real article data via NewsAPI. Returns a json of the top headlines
    in the United States right now.
    :param key: The API key that is required to call the API.
    :return: A json of all the articles that are top headlines right now.
    """

    return requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={key}").json()

  def convert_data(self, article_data, db):
    """
    Takes the json of all articles, then transforms this data into ArticleData objects. Returns
    this data in the form of ListArticleData so that the AI Analyzer can provide its analysis.
    :param article_data: json information of all articles
    :param db: The database instance that the information will be stored in. Need it here to
                check for duplicates
    :return: a ListArticleData object.
    """
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

      if not self.check_if_duplicate(db, res):
        res_articles.append(res)

    list_articles = ListArticleData(articles=res_articles)
    return list_articles

  def check_if_duplicate(self, db, article: ArticleData):
    """
    Checks if the given article is a duplicate by verifying its URL against existing
    records in the database.

    This method queries the database for a `Threat` entity with a source URL matching
    the provided article's URL. If a match is found, it returns True, indicating that
    the article is a duplicate. Otherwise, it returns False.

    :param db: Database session used to query for existing threats.
    :type db: sqlalchemy.orm.Session
    :param article: The article data object containing details about the article,
        including its URL.
    :return: True if the article URL already exists in the database, indicating a
        duplicate; otherwise False.
    :rtype: bool
    """
    existing = db.query(Threat).filter(Threat.source_url == article.url).first()
    return existing is not None

  def fetch_and_convert(self, db):
    """
    Calls both helper functions in a clean manner so that main pipeline can easily
    fetch news effectively.
    :param db: The database instance that the information will be stored in. Need it here to
                check for duplicates
    :return: a ListArticleData object.
    """
    load_dotenv()
    apikey = os.getenv("NEWS_API_KEY")

    article_data = self.fetch_article_data(apikey)
    return self.convert_data(article_data, db)