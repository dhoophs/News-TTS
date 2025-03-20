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
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

4. Install Dependencies:
   ```bash
   pip install -r requirements.txt

6. Download the en_core_web_sm model for topic extraction:
   ```bash
   python -m spacy download en_core_web_sm

---

## Usage

1. Run the FastAPI application:
   ```bash
   uvicorn api:app --reload

2. Run Streamlit application
   ```bash
   streamlit run app.py

---

## File Structure

   ```php
   News-TTS/
   ├── api.py                # Main FastAPI application
   ├── utils.py              # Helper functions for API
   ├── static/               # Directory for storing generated audio files
   ├── requirements.txt      # List of dependencies
   ├── README.md             # Project documentation
   └── .gitignore            # Files to ignore in version control
```
---
## Dependencies
1. Python 3.7+
2. FastAPI
3. spaCy
4. Hugging Face Transformers
5. Requests
6. Googletrans


