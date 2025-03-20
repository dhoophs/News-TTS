import streamlit as st
import requests

# Base API URL
API_URL = "http://127.0.0.1:8000"

st.title("News Summarization and Sentiment Analysis Tool")

# Input company name
company_name = st.text_input("Enter Company Name:", "")

if st.button("Fetch and Analyze News"):
    if company_name:
        with st.spinner("Fetching news and performing analysis..."):
            try:
                response = requests.post(f"{API_URL}/analyze", json={"company": company_name})
                response.raise_for_status()
                data = response.json()
                st.success("Analysis complete!")

                if not data["articles"]:
                    st.warning("No articles found for the given company.")
                else:
                    # Display structured report
                    st.subheader(f"Sentiment Analysis for {company_name}")
                    for article in data["articles"]:
                        st.write(f"**Title**: {article['title']}")
                        st.write(f"**Summary**: {article['summary']}")
                        st.write(f"**Sentiment**: {article['sentiment']}")
                        st.write(f"**Topics**: {', '.join(article['topics'])}")
                        st.write("---")
                    
                    # Comparative sentiment analysis
                    st.subheader("Comparative Analysis")
                    st.json(data["comparative_analysis"])

                    # Hindi TTS output
                    st.subheader("Hindi Text-to-Speech Output")
                    if data["audio_url"]:
                        st.audio(data["audio_url"])
                    else:
                        st.warning("Audio generation failed.")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to fetch news or perform analysis: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
    else:
        st.error("Please enter a company name.")
