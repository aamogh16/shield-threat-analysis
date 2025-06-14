import os

from dotenv import load_dotenv
from google import genai

from app.schemas.threat import ArticleData, ListArticleData, AIAnalysisResult


class AIAnalyzer:
  """
  Leverages Gemini's API to perform an analysis on article data received via
  NewsAPI. Will be able to assess an article and provide a threat level, category,
  summary, list of keywrods, and how confident it is.
  """

  # noinspection PyTypeChecker
  def analyze_articles(self, article: ListArticleData):
    load_dotenv()
    apikey = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=apikey)
    input_dict = article.model_dump()
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Read through these articles. Provide the following for EACH article: a boolean if it represents a threat or not, a threat-level from 1-10, a 1-2 word category representing the article, a brief summary of the article, a list of keywords, a float from 0.0-1.0 of how confident you are in your assessment, and the original title of the article. Here are the articles: {str(input_dict)}",
        config={
          "response_mime_type": "application/json",
          "response_schema": list[AIAnalysisResult]
        },
    )
    return response.text