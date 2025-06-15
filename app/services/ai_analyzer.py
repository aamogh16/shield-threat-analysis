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
  def analyze_articles(self, articles: ListArticleData):
    """
    Leverages GeminiAPI to acquire analysis on the current headlines. Gemini is prompted to output data
    in a list of AIAnalysisResult objects, as structured json output.
    :param articles: ListArticleData object that Gemini can read once it is converted to a dictionary
    :return: structured json data with analysis of each article.
    """
    load_dotenv()
    apikey = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=apikey)
    input_dict = articles.model_dump()
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Read through these articles. Provide the following for EACH article: a boolean if it represents a threat or not, a threat-level from 1-10, a 1-2 word category representing the article, a brief summary of the article, a list of keywords, a float from 0.0-1.0 of how confident you are in your assessment, the original title of the article, and provide a brief statement explaining why or why not this article is a threat. Here are the articles: {str(input_dict)}",
        config={
          "response_mime_type": "application/json",
          "response_schema": list[AIAnalysisResult]
        },
    )
    return response.text