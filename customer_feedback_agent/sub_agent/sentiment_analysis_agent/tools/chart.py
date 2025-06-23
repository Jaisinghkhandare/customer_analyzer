from typing import List, Literal
import matplotlib.pyplot as plt
import os
from datetime import datetime
from collections import defaultdict




def plot_sentiment_line_chart(sentiments: List[Literal["positive", "neutral", "negative"]], dates: List[str]) -> str:
    """
    sentiments: List of sentiment labels
    dates: List of dates corresponding to the sentiments (format: 'YYYY-MM-DD')
    """
    sentiment_by_date = {
        "positive": defaultdict(int),
        "neutral": defaultdict(int),
        "negative": defaultdict(int)
    }

    for sentiment, date in zip(sentiments, dates):
        if sentiment in sentiment_by_date:
            sentiment_by_date[sentiment][date] += 1

    # Sort dates
    sorted_dates = sorted(set(dates))
    
    fig, ax = plt.subplots()
    for sentiment, color in zip(["positive", "neutral", "negative"], ["green", "gray", "red"]):
        counts = [sentiment_by_date[sentiment].get(date, 0) for date in sorted_dates]
        ax.plot(sorted_dates, counts, label=sentiment, color=color, marker='o')

    ax.set_title("Sentiment Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Reviews")
    ax.legend()
    plt.xticks(rotation=45)

    filename = f"sentiment_line_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    output_dir = os.path.abspath("static")
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, filename)

    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()

    return f"/static/{filename}"

def plot_sentiment_pie_chart(sentiments: List[str]) -> str:
    from collections import Counter

    counts = Counter(sentiments)
    labels = list(counts.keys())
    sizes = list(counts.values())
    colors = ["green", "gray", "red"]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors[:len(labels)], autopct='%1.1f%%')
    ax.set_title("Sentiment Distribution - Pie Chart")
    filename = f"sentiment_pie_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    output_dir = os.path.abspath("static")
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, filename)

    plt.savefig(file_path)
    plt.close()

    return f"/static/{filename}"

def plot_sentiment_bar_chart(sentiments: List[str]) -> str:
    """
    Generates a bar chart showing counts of each sentiment type and returns the relative file path."""
    counts = {"positive": 0, "neutral": 0, "negative": 0}
    for sentiment in sentiments:
        if sentiment in counts:
            counts[sentiment] += 1

    fig, ax = plt.subplots()
    ax.bar(counts.keys(), counts.values(), color=["green", "gray", "red"])
    ax.set_title("Sentiment Distribution")
    ax.set_ylabel("Number of Reviews")

    filename = f"sentiment_chart_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    output_dir = os.path.abspath("static")
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, filename)

    plt.savefig(file_path)
    plt.close()

    return f"/static/{filename}"  # path that browser can use
  # returns absolute path for file handling or downloading

  
