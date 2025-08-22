import csv
import requests
import re
from datetime import datetime
from data_loader import load_json
from sentiment_analyzer import quick_sentiment
from sentiment import analy
from bs4 import BeautifulSoup
from visualizer import plot_pie_chart, plot_sentiment_trend

if __name__ == "__main__":
    url = "https://weirdkaya.com/say-goodbye-to-freedom-withdrawals-after-55yo-epf-looking-into-monthly-payouts-in-5-years/?fbclid=IwZXh0bgNhZW0CMTAAYnJpZBExbTFUUTc4SHllZzRyc2c1awEeCBIq4dGlPOx03h_M4RPSn1rIfPFBZnx374Pzw6I30S2jIJGuV3-wrD1uja8_aem_7XDmUYbkShj0cs-umQOV2w"  # 替换为目标网页

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        article_body = soup.find("div", itemprop="articleBody")
        
        if article_body:
            elements = article_body.find_all(["p", "h2"])
            with open('content.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        
                writer = csv.writer(csvfile)
                for elem in elements:
                    writer.writerow([elem.get_text(strip=True)])
        else:
            print("Could not find <div> with itemprop='articleBody'")
    else:
        print(f"Request failed, status code: {response.status_code}")

    with open('content.csv', 'r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        all_text = ' '.join([' '.join(row) for row in reader]) 

    print("=== QUICK SENTIMENT ANALYSIS ===\n")
    
    data = load_json()
    
    with open('report.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['index', 'comment', 'sentiment scores','date'])

        for idx, item in enumerate(data):
            try:
                sentiment = quick_sentiment(item['text'],item['postTitle'],all_text)
                print(f'{idx+1} {sentiment}')
                #sentiment = re.sub(r'<think>.*?</think>', '', sentiment, flags=re.DOTALL).strip()
                date = datetime.fromisoformat(item['date'].replace('Z', '+00:00'))
                writer.writerow([idx + 1, item['text'], sentiment,date])
            except Exception as e:
                print(f"Error on index {idx}: {e}")
                continue

    with open('report.csv', 'r', newline='', encoding='utf-8-sig') as csvfile:        
        reader = csv.reader(csvfile)
        all_text = ' '.join([' '.join(row) for row in reader])
        analysis = analy(all_text)
        print(analysis)

    #plot_pie_chart()
    #plot_sentiment_trend()
