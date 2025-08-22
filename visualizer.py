import pandas as pd
import json
import matplotlib.pyplot as plt
from datetime import datetime

def plot_pie_chart(csv_file='llama2_13b_sentiment.csv'):
    df = pd.read_csv(csv_file, encoding='utf-8-sig')
    sentiment_counts = df['sentiment scores'].value_counts()

    plt.figure(figsize=(6, 6))
    plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Sentiment Distribution')
    plt.tight_layout()
    plt.savefig('llama2_13b_sentiment_distribution_pie_chart.png')
    plt.close()

def plot_sentiment_trend(csv_file='llama2_13b_sentiment.csv', json_file='dataset_facebook.json'):
    df = pd.read_csv(csv_file, encoding='utf-8-sig')

    df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date
    df = df.dropna(subset=['date'])

    trend_data = df.groupby(['date', 'sentiment scores']).size().unstack(fill_value=0)

    plt.figure(figsize=(10, 6))
    trend_data.plot(marker='o')
    plt.title('Daily Sentiment Trend')
    plt.xlabel('Date')
    plt.ylabel('Number of Comments')
    plt.legend(title='Sentiment')
    plt.tight_layout()
    plt.savefig('llama2_13b_daily_sentiment_trend.png')
    plt.close()
