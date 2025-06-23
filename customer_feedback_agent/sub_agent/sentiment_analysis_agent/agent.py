from typing import List
from pydantic import BaseModel
from pydantic import Field
from google.adk.agents import Agent
from customer_feedback_agent.sub_agent.sentiment_analysis_agent.tools.chart import (
    plot_sentiment_bar_chart,
    plot_sentiment_pie_chart,
    plot_sentiment_line_chart,
)

class ReviewInput(BaseModel):
    source: str
    text: str
    score: int
    date: str

class ReviewBatchInput(BaseModel):
    reviews: List[ReviewInput]

sentiment_analysis_agent = Agent(
    name="sentiment_analysis_agent",
    model="gemini-2.0-flash",
    description="Computes an average sentiment score (0–10 scale) and counts of positive/neutral/negative reviews.",
    instruction="""
You are a review analysis expert working under the customer_feedback root agent.

Given a list of user reviews, analyze all reviews and return:
1. sentiment_scale: a float from 0 to 10, where
   - positive = 10,
   - neutral = 5,
   - negative = 0
   - average it across all reviews.
2. sentiment_count: a list of counts in the order [positive, neutral, negative].

Return output as **one valid JSON object** containing only:
- "sentiment_scale": float
- "sentiment_count": list of 3 integers

Also, you must generate all sentiment charts using:
- plot_sentiment_bar_chart
- plot_sentiment_pie_chart
- plot_sentiment_line_chart

Each chart tool returns a static image path (e.g., /static/chart.png). Display those URLs clearly in the final response.

After this, return control to the root agent.
""",
    input_schema=ReviewBatchInput,
    output_key="review_result",
    tools=[plot_sentiment_bar_chart, plot_sentiment_pie_chart, plot_sentiment_line_chart],
)
