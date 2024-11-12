# app.py
from flask import Flask, render_template
import feedparser
from datetime import datetime

app = Flask(__name__)

def clean_text(text):
    # Remove HTML tags and clean up the text
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text).strip()

def fetch_news():
    # Using Times of India RSS feed
    urls = [
        "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
        "https://feeds.feedburner.com/ndtvnews-top-stories"
    ]
    
    news_items = []
    
    for url in urls:
        try:
            feed = feedparser.parse(url)
            
            for entry in feed.entries[:5]:  # Get top 5 from each source
                # Get publication date
                pub_date = entry.get('published', '')
                try:
                    date_obj = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %z')
                    formatted_date = date_obj.strftime('%B %d, %Y %I:%M %p')
                except:
                    formatted_date = pub_date

                # Get description and clean it
                description = clean_text(entry.get('description', ''))
                
                news_items.append({
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'description': description,
                    'date': formatted_date,
                    'source': 'Times of India' if 'timesofindia' in url else 'NDTV'
                })
                
        except Exception as e:
            print(f"Error fetching news from {url}: {e}")
            continue
    
    return sorted(news_items, key=lambda x: x['date'], reverse=True)[:10]  # Return top 10 most recent

@app.route('/')
def home():
    news_items = fetch_news()
    return render_template('index.html', news_items=news_items)

if __name__ == '__main__':
    app.run(debug=True)