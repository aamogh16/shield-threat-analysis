import json

from app.models.threat import Threat
from app.schemas.threat import ArticleData, ListArticleData
from app.schemas.threat import ThreatCreate
from app.services.ai_analyzer import AIAnalyzer
from app.services.mock_ai import MockAI
from app.database import get_db


class ThreatProcessor:
    """
    Takes in the news data from API/test articles, as well as AI Analysis to output data
    into the database.
    """

    def __init__(self):
      # creating AI analyzer to analyze articles.
      self.mock_ai = MockAI()
      self.ai_analyzer = AIAnalyzer()


    def find_matching_dictionary(self, title, ai_results):
      """
      Searches for a dictionary within a list of dictionaries that matches the specified
      title. The `ai_results` parameter must be an iterable of dictionaries, each containing
      a "title" key. This function iterates through the list looking for a dictionary whose
      "title" key matches the value of the `title` parameter. If such a dictionary is found,
      it is returned; otherwise, the function returns None.

      :param title: The title to be matched against the "title" key in the dictionaries
                    from the list.
      :type title: str
      :param ai_results: A list of dictionaries, where each dictionary must include a
                         "title" key.
      :type ai_results: list[dict]
      :return: The first dictionary from the list where the value of the "title" key
               matches the provided `title`, or None if no match is found.
      :rtype: dict | None
      """
      for result in ai_results:
        if result["title"] == title:
          return result
      return None

    def process_articles(self, listArticleData: ListArticleData, db):
      """
      Processes a list of ArticleData: receiving it from the NewsAPI, then sending it to
      GeminiAI for analysis, then sending all viable threats to the S.H.I.E.L.D database.
      :param listArticleData:
      :param articles: ListArticleData that will be processed
      :param db: The database instance used for accessing or modifying data as
          part of the article processing.
      :return: The result of the processing operation, which depends on the specific
          implementation and may be data, a status, or some transformation outcome.
      """

      res = []
      ai_result_json = self.ai_analyzer.analyze_articles(listArticleData)
      ai_result_dict = json.loads(ai_result_json)

      for article in listArticleData.articles:
        match_dict = self.find_matching_dictionary(article.title, ai_result_dict)
        if match_dict.get("is_threat"):
          threat = Threat(
              title=article.title,
              description=article.description,
              source=article.source,
              source_url=article.url,
              published_at=article.published_at,

              ai_threat_level=match_dict.get("threat_level"),
              ai_category=match_dict.get("category"),
              ai_summary=match_dict.get("summary"),
              ai_confidence=match_dict.get("confidence"),
              ai_keywords=match_dict.get("keywords"),
              ai_reason=match_dict.get("reason")
          )
          res.append(threat)
          db.add(threat)
          db.commit()

      return res

    # def process_article(self, article: ArticleData, database):
    #   """
    #   Processes an article and performs operations based on provided data and database.
    #
    #   :param article: The article data object containing the necessary information for
    #       processing.
    #   :type article: ArticleData
    #   :param database: The database instance used for accessing or modifying data as
    #       part of the article processing.
    #   :return: The result of the processing operation, which depends on the specific
    #       implementation and may be data, a status, or some transformation outcome.
    #   """
    #
    #   ai_result = self.ai.analyze_article(article)
    #   print(f"AI Threat Analysis - Is it a threat: {ai_result.is_threat} \n What Threat Level: {ai_result.threat_level}")
    #
    #   if ai_result.is_threat:
    #     threat = Threat(
    #         title=article.title,
    #         description=article.description,
    #         source=article.source,
    #         source_url=article.url,
    #         published_at=article.published_at,
    #
    #         ai_threat_level=ai_result.threat_level,
    #         ai_category=ai_result.category,
    #         ai_summary=ai_result.summary,
    #         ai_confidence=ai_result.confidence,
    #         ai_keywords=ai_result.keywords
    #     )
    #     database.add(threat)
    #     database.commit()
    #     print("Threat added to Database.")
    #     return threat
    #
    #   else:
    #     print("Article did not post a threat, information ignored.")
    #     return None

