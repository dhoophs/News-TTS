# News-TTS

**News-TTS** is a Python-based application that fetches news articles about a specific company, analyzes their sentiment, extracts topics, translates summaries to Hindi, and generates a Text-to-Speech (TTS) audio file in Hindi.

---

## Features

- Fetch news articles for a given company using a news API.
- Perform sentiment analysis (Positive, Negative, Neutral) on the articles.
- Extract topics from article content.
- Translate article summaries to Hindi.
- Generate TTS audio for the translated summaries.

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/dhoophs/News-TTS.git
   cd News-TTS

2. Create and activate a virtual environment:
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install Dependencies:
   pip install -r requirements.txt

4. Download the en_core_web_sm model for topic extraction:
   python -m spacy download en_core_web_sm
   
