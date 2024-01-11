import streamlit as st
import requests
from bs4 import BeautifulSoup
import spacy
from textblob import TextBlob
import streamlit as st


# Apply a dark theme
st.set_page_config(page_title="Rates Focus Market Overview", layout="wide")

nlp = spacy.load("en_core_web_sm")

# Function to scrape news from Yahoo Finance
def fetch_yahoo_finance_news():
    url = "https://finance.yahoo.com/topic/economic-news"
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
st.markdown("<h1 style='text-align: center; color: white;'>Rates Focus Market Overview</h1>", unsafe_allow_html=True)
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

st.subheader("Rates")

iframe_code = '''
<iframe frameborder="0" scrolling="no" height=50 width="474" allowtransparency="true" marginwidth="0" marginheight="0" src="https://sslirates.investing.com/index.php?rows=4&bg1=281f4a&bg2=000000&text_color=ffffff&enable_border=hide&border_color=000000&header_bg=0452A1&header_text=FFFFFF&force_lang=51" align="center"></iframe><br /><table width="200"><tbody><tr><td style="text-align:left"><a href="https://uk.investing.com" rel="nofollow" target="_blank"><img style="vertical-align:middle;" title="Investing.com UK" alt="Investing.com UK" border="0" src="https://92f8049275b46d631f32-c598b43a8fdedd4f0b9230706bd7ad18.ssl.cf1.rackcdn.com/forexpros_en_logo.png"></a></td></tr><tr><td><span style="font-size: 11px;color: #333333;text-decoration: none;">Interest Rates powered by <a href="https://uk.investing.com/" rel="nofollow" target="_blank" style="font-size: 11px;color: #06529D; font-weight: bold;" class="underline_link">Investing.com UK</a>.</span></td></tr></tbody></table>
'''
st.components.v1.html(iframe_code, height=50)
    
    
st.markdown("<h2 style='color: white;'>Select a headline for summary</h2>", unsafe_allow_html=True)
st.write("Source: Top 10 economics news headlines from Yahoo Finance")
for headline in headline_list:
    with st.expander(headline):
        summary_url = headlines[headline]['link']
        full_article_text = fetch_article_text(summary_url)
        summary = summarize_text(full_article_text)
        sentiment, color = get_sentiment(full_article_text)
        st.markdown(f"Summary: {summary}")
        st.markdown(f"Sentiment: <span style='background-color:{color};'>{sentiment}</span>", unsafe_allow_html=True)
        st.markdown(f"For more details, [click here]({summary_url})", unsafe_allow_html=True)
        
        

        
st.subheader("Economic Calendar")

iframe_code = '''
<iframe src="https://sslecal2.investing.com?columns=exc_flags,exc_currency,exc_importance,exc_actual,exc_forecast,exc_previous&category=_centralBanks&importance=3&features=datepicker,timezone,timeselector,filters&countries=72,35,4,5&calType=week&timeZone=15&lang=51" width="900" height="900" frameborder="0" allowtransparency="true" marginwidth="0" marginheight="0"></iframe><div class="poweredBy" style="font-family: Arial, Helvetica, sans-serif;"><span style="font-size: 11px;color: #333333;text-decoration: none;">Real Time Economic Calendar provided by <a href="https://uk.Investing.com/" rel="nofollow" target="_blank" style="font-size: 11px;color: #06529D; font-weight: bold;" class="underline_link">Investing.com UK</a>.</span></div>
'''
st.components.v1.html(iframe_code, height=500)

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
