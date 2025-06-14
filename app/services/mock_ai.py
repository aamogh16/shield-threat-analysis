from app.schemas.threat import ArticleData, AIAnalysisResult


class MockAI:
  """
  Simple "AI" Service to test pipeline functionality. Will take in sample article data and provide 
  output data that will be simulate the real AI's output data. 
  """

  def analyze_article(self, article: ArticleData):
    title = article.title.lower()
    description = ""
    if article.description:
      description = article.description.lower()

    # set of good words - if article contains these words, it is not a threat.
    safe_words = {
      "support", "help", "community", "guide", "safe", "protect", "wellness",
      "education", "success", "innovation", "clean", "peaceful", "relief",
      "improve", "solution", "health", "care", "growth", "inspire",
      "collaboration", "discovery", "progress", "celebration", "joy",
      "resilience", "unity", "trust", "transparency", "empowerment", "kindness"
    }

    # set of bad words - results in a high level threat.
    threat_words = {
      "attack", "bomb", "threat", "murder", "war", "gun", "kill", "shoot",
      "assault", "crisis", "panic", "danger", "virus", "hack", "breach", "scam",
      "fraud", "explosion", "terror", "hostage", "toxic", "disaster", "arrest",
      "criminal", "abuse", "violence", "hate", "ransomware", "stalk", "exploit",
      "extremist"
    }

    # if threat word is found, break and set to true
    threat_found = False
    for tword in threat_words:
      if tword in title or tword in description:
        threat_found = True
        break

    # if safe word is found, break and set to true
    safe_found = False
    for sword in safe_words:
      if sword in title or sword in description:
        safe_found = True
        break

    print(f"Article: {title} - {description}. Here is threat_found: {threat_found}, and here is safe_found: {safe_found}")

    if threat_found:
      return AIAnalysisResult(
          is_threat=True, threat_level=10, category="Any threat", summary="this is a threat", keywords=[], confidence=1.0)

    if safe_found:
      return AIAnalysisResult(
          is_threat=False, threat_level=1, category="", summary="", keywords=[], confidence=1.0)

    return AIAnalysisResult(
        is_threat=True, threat_level=6, category="Mild threat", summary="don't know for sure, but letting it be a threat for more data.", keywords=[], confidence=0.5)

