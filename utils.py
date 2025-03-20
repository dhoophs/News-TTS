import requests
from transformers import pipeline
from gtts import gTTS
from googletrans import Translator
import spacy
import os
import logging

if not os.path.exists("static"):
    os.makedirs("static")

# Fetch news articles
def fetch_news(company_name):
    try:
        print(f"Fetching news for company: {company_name}")
        response = requests.get(f"https://newsapi.org/v2/everything?q={company_name}&apiKey=d0a80ac8114a486faf28e300690b23a7")
        response.raise_for_status()
        data = response.json()
        articles = [{"title": article["title"], "content": article["content"]} for article in data.get("articles", [])]
        return articles
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []



nlp = spacy.load("en_core_web_sm")
def extract_topics(text):
    doc = nlp(text)
    topics = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]
    return list(set(topics)) or ["No specific topics"]

# Analyze sentiment of articles
def analyze_sentiment(articles):
    try:
        sentiment_pipeline = pipeline("sentiment-analysis")
        analyzed_articles = []
        for article in articles:
            content = article["content"] or ""
            sentiment = sentiment_pipeline(content[:512])[0]  # Limit to 512 chars
            topics = extract_topics(content)
            analyzed_articles.append({
                "title": article["title"],
                "summary": content[:150],  # Example: Use first 150 chars as summary
                "sentiment": sentiment["label"],
                "topics": topics
            })
        return analyzed_articles
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return []
    

def chunk_text(text, max_length=500):
    words = text.split()
    chunks, chunk = [], []
    for word in words:
        if len(" ".join(chunk + [word])) <= max_length:
            chunk.append(word)
        else:
            chunks.append(" ".join(chunk))
            chunk = [word]
    if chunk:
        chunks.append(" ".join(chunk))
    return chunks    


# Handles large text translation by chunking and error handling
def translate_large_text(text):
    chunks = chunk_text(text)
    logging.debug(f"[DEBUG] Splitting text into {len(chunks)} chunks.")
    translated_chunks = []
    
    for i, chunk in enumerate(chunks, 1):
        try:
            translated_chunk = translate_to_hindi(chunk)
            if translated_chunk is None:
                raise ValueError(f"Chunk {i} returned None.")
            translated_chunks.append(translated_chunk)
        except Exception as e:
            logging.error(f"Error in translating chunk {i}: {str(e)}. Skipping this chunk.")
            translated_chunks.append("")  
    return " ".join(translated_chunks)


# Translate text to Hindi
def translate_to_hindi(text):
    if not text.strip():
        raise ValueError("No text to translate.")
    try:
        translator = Translator()
        result = translator.translate(text, src="en", dest="hi")
        
        # Debugging: Check the result object
        if not result:
            raise ValueError("Translation response is None.")
        if not hasattr(result, 'text'):
            raise ValueError("Invalid translation response format.")
        return result.text
    except Exception as e:
        print(f"Error in translation: {e}")
        raise ValueError(f"Translation failed: {e}")


# Generate TTS audio in Hindi
def generate_audio(text, filename="output.mp3"):
    if not text.strip():
        raise ValueError("No text to generate audio.")
    
    try:
        file_path = os.path.join("static", filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        tts = gTTS(text=text, lang="hi")
        tts.save(file_path)
        return f"/static/{filename}"
    except Exception as e:
        raise ValueError(f"Audio generation failed: {e}")