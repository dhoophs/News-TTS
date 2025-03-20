from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from utils import fetch_news, analyze_sentiment, translate_large_text, generate_audio
import logging

app = FastAPI()

# Mount static directory for audio files
app.mount("/static", StaticFiles(directory="static"), name="static")

class CompanyRequest(BaseModel):
    company: str

class ArticleResponse(BaseModel):
    title: str
    summary: str
    sentiment: str
    topics: List[str]

class AnalysisResponse(BaseModel):
    articles: List[ArticleResponse]
    comparative_analysis: dict
    audio_url: str

@app.post("/analyze", response_model=AnalysisResponse)
def analyze(company_request: CompanyRequest):
    try:
        company = company_request.company
        logging.info(f"Fetching news articles for company: {company}")
        
        # Step 1: Fetch news articles
        articles = fetch_news(company)
        if not articles:
            logging.warning(f"No articles found for company: {company}")
            raise HTTPException(status_code=404, detail="No articles found for the given company.")
        
        
        # Step 2: Perform sentiment analysis
        logging.info(f"Performing sentiment analysis for company: {company}")
        analyzed_articles = analyze_sentiment(articles)
        if not analyzed_articles:
            logging.error(f"Sentiment analysis failed for company: {company}")
            raise HTTPException(status_code=500, detail="Sentiment analysis failed.")
        
        # Convert analyzed articles to ArticleResponse objects
        article_responses = [
            ArticleResponse(
                title=article["title"],
                summary=article["summary"],
                sentiment=article["sentiment"],
                topics=article["topics"]
            ) for article in analyzed_articles
        ]
        

        # Step 3: Perform comparative analysis
        logging.info(f"Performing comparative analysis for company: {company}")
        all_topics = [topic for article in analyzed_articles for topic in article["topics"]]
        common_topics = list(set(topic for topic in all_topics if all_topics.count(topic) > 1))
        unique_topics = {article["title"]: article["topics"] for article in analyzed_articles}
        
        comparative_analysis = {
            "sentiment_distribution": {
                "Positive": sum(1 for a in analyzed_articles if a["sentiment"] == "POSITIVE"),
                "Negative": sum(1 for a in analyzed_articles if a["sentiment"] == "NEGATIVE"),
                "Neutral": sum(1 for a in analyzed_articles if a["sentiment"] == "NEUTRAL"),
            },
            "topic_overlap": {
                "common_topics": common_topics,
                "unique_topics": unique_topics,
            },
        }

        # Combine summaries for TTS
        combined_summaries = " ".join([article["summary"] for article in analyzed_articles])
        if not combined_summaries.strip():
            raise ValueError("No summaries available for translation.")
        logging.info(f"Combined summaries for translation: {combined_summaries}")

        
        
        # Translate to Hindi
        logging.info(f"Translating summaries to Hindi for company: {company}")
        hindi_text = translate_large_text(combined_summaries)
        logging.info(f"Translated Hindi Text: {hindi_text}")
        
        
        # Generate Hindi TTS audio
        logging.info(f"Generating Hindi TTS audio for company: {company}")
        audio_url = generate_audio(hindi_text)
        if not audio_url:
            logging.error(f"Audio generation failed for company: {company}")
            raise HTTPException(status_code=500, detail="Audio generation failed.")
        
        
        # Step 5: Prepare the final response
        return AnalysisResponse(
            articles=article_responses,
            comparative_analysis=comparative_analysis,
            audio_url=audio_url
        )

    except HTTPException as e:
        logging.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error. Check logs for details.")
