import streamlit as st
import requests
from bs4 import BeautifulSoup
import spacy
from textblob import TextBlob


# Apply a dark theme
st.set_page_config(page_title="Equities Focus Market Overview", layout="wide")

nlp = spacy.load("en_core_web_sm")

# Function to scrape news from Yahoo Finance
def fetch_yahoo_finance_news():
    url = "https://finance.yahoo.com/topic/stock-market-news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = {}

    for item in soup.find_all('h3', {'class': lambda x: x and 'Mb(5px)' in x}):
        text = item.get_text()
        link = item.a['href']

        if text and link:
            headlines[text] = {
                'link': f"https://finance.yahoo.com{link}"
            }
    return headlines

# Web App Title with Enhanced Typography
st.markdown("<h1 style='text-align: center; color: white;'>Equities Focus Market Overview</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: white;'>By Jamal Lawal</h3>", unsafe_allow_html=True)

headlines = fetch_yahoo_finance_news()
headline_list = list(headlines.keys())

def summarize_text(text):
    doc = nlp(text)
    sentences = [sentence.orth_ for sentence in doc.sents]
    return ' '.join(sentences[:3])  # Return the first 3 sentences as a summary

def fetch_article_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    article_text = ' '.join([para.text for para in paragraphs])
    return article_text

def get_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    if sentiment_score > 0.00:
        return '😊 Positive', '#00cc66'  # green
    elif sentiment_score < 0.00:
        return '😞 Negative', '#ff6666'  # red
    else:
        return '😐 Neutral', '#ffffff'  # white

st.markdown("<h2 style='color: white;'>Select a headline for summary</h2>", unsafe_allow_html=True)
st.write("Source: Top 10 equities news headlines from Yahoo Finance")
for headline in headline_list:
    with st.expander(headline):
        summary_url = headlines[headline]['link']
        full_article_text = fetch_article_text(summary_url)
        summary = summarize_text(full_article_text)
        sentiment, color = get_sentiment(full_article_text)
        st.markdown(f"Summary: {summary}")
        st.markdown(f"Sentiment: <span style='background-color:{color};'>{sentiment}</span>", unsafe_allow_html=True)
        st.markdown(f"For more details, [click here]({summary_url})", unsafe_allow_html=True)
        
 

st.subheader("News")

iframe_code = '''
<!-- TradingView Widget BEGIN -->
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank"><span class="blue-text">Track all markets on TradingView</span></a></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-timeline.js" async>
  {
  "feedMode": "all_symbols",
  "isTransparent": false,
  "displayMode": "regular",
  "width": "100%",
  "height": "1200",
  "colorTheme": "dark",
  "locale": "en"
}
  </script>
</div>
<!-- TradingView Widget END -->
'''
st.components.v1.html(iframe_code, height=1200)






        
st.subheader("Economic Calendar")

iframe_code = '''
<iframe src="https://sslecal2.investing.com?columns=exc_flags,exc_currency,exc_importance,exc_actual,exc_forecast,exc_previous&category=_centralBanks&importance=3&features=datepicker,timezone,timeselector,filters&countries=72,35,4,5&calType=week&timeZone=15&lang=51" width="900" height="900" frameborder="0" allowtransparency="true" marginwidth="0" marginheight="0"></iframe><div class="poweredBy" style="font-family: Arial, Helvetica, sans-serif;"><span style="font-size: 11px;color: #333333;text-decoration: none;">Real Time Economic Calendar provided by <a href="https://uk.Investing.com/" rel="nofollow" target="_blank" style="font-size: 11px;color: #06529D; font-weight: bold;" class="underline_link">Investing.com UK</a>.</span></div>
'''
st.components.v1.html(iframe_code, height=800)

# Exchange Rates Section
st.subheader("Exchange Rates")

iframe_code = '''<!-- TradingView Widget BEGIN -->
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank"><span class="blue-text">Track all markets on TradingView</span></a></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-forex-cross-rates.js" async>
  {
  "width": "100%",
  "height": "900",
  "currencies": [
    "EUR",
    "USD",
    "JPY",
    "GBP",
    "CHF",
    "AUD",
    "CAD",
    "NZD"
  ],
  "isTransparent": true,
  "colorTheme": "dark",
  "locale": "en"
}
  </script>
</div>
<!-- TradingView Widget END -->'''
st.components.v1.html(iframe_code, height= 900)

st.subheader("Equities Market Overview")

iframe_code = '''
<!-- TradingView Widget BEGIN -->
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank"><span class="blue-text">Track all markets on TradingView</span></a></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-market-quotes.js" async>
  {
  "width": "100%",
  "height": "900",
  "symbolsGroups": [
    {
      "name": "Indices",
      "originalName": "Indices",
      "symbols": [
        {
          "name": "FOREXCOM:SPXUSD",
          "displayName": "S&P 500"
        },
        {
          "name": "FOREXCOM:NSXUSD",
          "displayName": "US 100"
        },
        {
          "name": "FOREXCOM:DJI",
          "displayName": "Dow 30"
        },
        {
          "name": "INDEX:NKY",
          "displayName": "Nikkei 225"
        },
        {
          "name": "INDEX:DEU40",
          "displayName": "DAX Index"
        },
        {
          "name": "FOREXCOM:UKXGBP",
          "displayName": "UK 100"
        }
      ]
    },
    {
      "name": "Futures",
      "originalName": "Futures",
      "symbols": [
        {
          "name": "CME_MINI:ES1!",
          "displayName": "S&P 500"
        },
        {
          "name": "CME:6E1!",
          "displayName": "Euro"
        },
        {
          "name": "COMEX:GC1!",
          "displayName": "Gold"
        },
        {
          "name": "NYMEX:CL1!",
          "displayName": "WTI Crude Oil"
        },
        {
          "name": "NYMEX:NG1!",
          "displayName": "Gas"
        },
        {
          "name": "CBOT:ZC1!",
          "displayName": "Corn"
        }
      ]
    },
    {
      "name": "Bonds",
      "originalName": "Bonds",
      "symbols": [
        {
          "name": "CBOT:ZB1!",
          "displayName": "T-Bond"
        },
        {
          "name": "CBOT:UB1!",
          "displayName": "Ultra T-Bond"
        },
        {
          "name": "EUREX:FGBL1!",
          "displayName": "Euro Bund"
        },
        {
          "name": "EUREX:FBTP1!",
          "displayName": "Euro BTP"
        },
        {
          "name": "EUREX:FGBM1!",
          "displayName": "Euro BOBL"
        }
      ]
    },
    {
      "name": "Stocks",
      "symbols": [
        {
          "name": "NASDAQ:TSLA",
          "displayName": "TESLA"
        },
        {
          "name": "NASDAQ:AAPL",
          "displayName": "APPLE INC."
        },
        {
          "name": "NASDAQ:NVDA",
          "displayName": "NVIDIA "
        },
        {
          "name": "NASDAQ:MSFT",
          "displayName": "MICROSOFT CORPORATION"
        },
        {
          "name": "NASDAQ:AMZN",
          "displayName": "AMAZON"
        },
        {
          "name": "NASDAQ:META",
          "displayName": "META"
        },
        {
          "name": "NASDAQ:GOOGL",
          "displayName": "GOOG"
        }
      ]
    }
  ],
  "showSymbolLogo": true,
  "isTransparent": false,
  "colorTheme": "dark",
  "locale": "en"
}
  </script>
</div>
<!-- TradingView Widget END -->
'''
st.components.v1.html(iframe_code, height=900)


   
