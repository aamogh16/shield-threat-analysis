from datetime import datetime, timedelta

from apscheduler.schedulers.blocking import BlockingScheduler

from app.database import get_db
from app.models.threat import Threat
from app.services.news_fetcher import NewsFetcher
from app.services.threat_processor import ThreatProcessor

def main():
  scheduler = BlockingScheduler()

  # runs the pipeline every hour
  scheduler.add_job(pipeline, 'interval', hours=1)

  # runs first time
  pipeline()

  try:
    scheduler.start()  # This runs forever
  except KeyboardInterrupt:
    print("\nS.H.I.E.L.D. System shutting down...")


def pipeline():
  """
  Performs the full S.H.I.E.L.D. threat analysis system.
  1. Fetches news from NewsAPI
  2. Checks for duplicate articles to avoid extra processing
  3. Analyzes articles with GeminiAPI
  4. Sends potential threats to database
  5. Ready to perform get requests to get threats, or ready for potential human override
  """
  print("🛡️ S.H.I.E.L.D. Threat Analysis Pipeline Starting... \n")
  # ASCII art displays every time the pipeline runs
  print("""
                       AAAAAAAAA                       
                 AAAAAAAAAAAAAAAAAAAAA                 
             AAAAAAAAAAAGQWYXQHAAAAAAAAAAA             
          AAAAAAAA                   AAAAAAA           
        AAAAAAM                         OAAAAAA        
      AAAAAA                               AAAAAA      
     AAAAB  B             FAAAAAO            BAAAA     
   AAAAA  BAAAA          AAAAAZ         XAAAC  AAAAA   
  AAAAA  AAAAAAAAV      AAAAAAA       FAAAAAAA  AAAAA  
  AAAA W  GAAAAAAAAK   EAAAAAAAA   SAAAAAAAAAA   AAAA  
 AAAA SAAM  AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAZ  A  AAAA 
 AAAZ AAAAA  KAAAAAAAAAAAAAAAAAAAAAAAAAAAAF  AAAA YAAAA
AAAA BAAAB BA  AAAAAAAAAAAAAAAAAAAAAAAAAF  NAAAAAF AAAA
AAAN AAG LAAAA   AAAAAAAAAAAAAAAAAAAAAA  SAA GAAAA MAAA
AAAX Q JAAAAAAAU  EAAAAAAAAAAAAAAAAAA   AAAAADVFAA YAAA
AAAX FAAAAAAAATXA   AAAAAAAAAAAAAAA    NAAAAAAABSL YAAA
AAAN AAAAAAAG BAAAA  XAAAAAAAAAAAP  LAAM AAAAAAAAB MAAA
AAAA BAAAAA EAAAAAAA   AAAAAAAAA   AAAAAA MAAAAAAD AAAA
 AAAY AAA SAAAAAAAA      AAAAA     RAAAAAAA AAAAA XAAAA
 AAAA MG AAAAAAAA     AA  IA   AA    AAAAAAANZAA  AAAA 
  AAAA XAAAAAAAB    LAAAAD   AAAAA    AAAAAAAAY  AAAA  
  AAAAA WAAAAAT    AAAAAAAAAAAAAAAA    AAAAAAA  AAAAA  
    AAAAX AAA     AAAAAAAAAAAAAAAAAAG   JAAAB  AAAA    
     AAAAB      QAAAAAAAAAAAAAAAAAAAAB   RA  BAAAA     
      AAAAAB   EAAAAAAAAAAAAAAAAAAAAAAA    BAAAAA      
        AAAAAAJ  AAAAAAAAAAAAAAAAAAAAA  MAAAAAA        
           AAAAAAA   VAAAAAAAAAAAY   AAAAAAA           
             AAAAAAAAAAAAJQSQJAAAAAAAAAAAA             
                 AAAAAAAAAAAAAAAAAAAAA                 
                        AAAAAAA                        
  
  """)

  try:
    # initializing the database, news fetcher, and threat processor (all services for the pipeline)
    db = next(get_db())

    cleanup_old_threats(db)

    fetcher = NewsFetcher()
    processor = ThreatProcessor()

    articles = fetcher.fetch_and_convert(db)

    # prevent extra processing by returning early if there is no new data
    if not articles.articles:
      print("No new articles found, no threats as of now.")
      return

    print(
      f"Found {len(articles.articles)} articles to process for threats.")

    saved_threats = processor.process_articles(articles, db)

    print(
      f"{len(saved_threats)} articles show situations that post a threat. Information has been sent to the database.")

    print(
      f"🛡️ S.H.I.E.L.D. Pipeline completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


  except Exception as e:
    print(f"❌ Pipeline error: {e}")
  finally:
    db.close()


def cleanup_old_threats(db):
  """
  Removes threats from the database that are more than 5 days old.
  """

  cutoff_date = datetime.now() - timedelta(days=5)

  deleted_count = db.query(Threat).filter(Threat.created_at < cutoff_date).delete()
  db.commit()

  if deleted_count > 0:
    print(f"Deleted {deleted_count} old threats from the database, more than 5 days have passed.")

if __name__ == "__main__":
  main()
