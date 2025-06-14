from app.models.threat import Threat
from app.schemas.threat import ArticleData
from app.schemas.threat import ThreatCreate
from app.services.mock_ai import MockAI
from app.database import get_db


class ThreatProcessor:
  """
  Takes in the news data from API/test articles, as well as AI Analysis to output data
  into the database.
  """

  def __init__(self):
    # creating Mock AI to perform analysis, only need for testing purposes.
    self.ai = MockAI()


  def process_article(self, article: ArticleData, database):
    """
    Processes an article and performs operations based on provided data and database.

    :param article: The article data object containing the necessary information for
        processing.
    :type article: ArticleData
    :param database: The database instance used for accessing or modifying data as
        part of the article processing.
    :return: The result of the processing operation, which depends on the specific
        implementation and may be data, a status, or some transformation outcome.
    """

    ai_result = self.ai.analyze_article(article)
    print(f"AI Threat Analysis - Is it a threat: {ai_result.is_threat} \n What Threat Level: {ai_result.threat_level}")

    if ai_result.is_threat:
      threat = Threat(
          title=article.title,
          description=article.description,
          source=article.source,
          source_url=article.url,
          published_at=article.published_at,

          ai_threat_level=ai_result.threat_level,
          ai_category=ai_result.category,
          ai_summary=ai_result.summary,
          ai_confidence=ai_result.confidence,
          ai_keywords=ai_result.keywords
      )
      database.add(threat)
      database.commit()
      print("Threat added to Database.")
      return threat

    else:
      print("Article did not post a threat, information ignored.")
      return None

