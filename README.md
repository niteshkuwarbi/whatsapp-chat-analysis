# WhatsApp Chat Analyzer

A Streamlit web app that analyzes exported WhatsApp chats and generates insights through timelines, activity patterns, user statistics, word usage, and emoji analysis.

## Features

- Timelines – Monthly and daily trends of messages.
- Activity Maps – Most active days, months, and weekly heatmaps.
- Participants – Identify the most active contributors.
- Word Analysis – Word cloud and most frequent words (with stopword filtering). 
- Emoji Analysis – Frequency and share of emojis used.
- Data Privacy – Uploaded files are processed only in-memory during the session. No data is stored or transmitted externally.

## Project Structure
- app.py               Main Streamlit app
- helper.py            Helper functions for analysis
- preprocessor.py      Chat preprocessing logic
- stop_hinglish.txt    Stopword list for filtering Hinglish/English
- requirements.txt     Dependencies
- README.md            Documentation

## How to Export WhatsApp Chat

* Open the chat in WhatsApp.
* Select More → Export chat → Without media.
* Save the .txt file.
* Upload it to the app sidebar.

## Disclaimer

This project is for educational and analytical purposes.
- Files are parsed locally within the session.
- No permanent storage, database writes, or external transmissions occur.
