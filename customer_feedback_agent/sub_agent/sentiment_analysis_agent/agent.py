from typing import List
from pydantic import BaseModel
from pydantic import Field
from google.adk.agents import Agent
class ReviewInput(BaseModel):
    source: str
    text: str
    score: int
    date: str

class ReviewBatchInput(BaseModel):
    reviews: List[ReviewInput]


class AnalyzedReview(BaseModel):
    source: str
    text: str
    score: int
    date: str
    sentiment: str = Field(description="positive, neutral, or negative")
    confidence: float = Field(description="Sentiment confidence, 0 to 1")
    frustrated: bool
    sarcastic: bool

class ReviewBatchOutput(BaseModel):
    results: List[AnalyzedReview]



sentiment_analysis_agent = Agent(
    name="sentiment_analysis_agent",
    model="gemini-2.0-flash",
    description="Analyzes a batch of app reviews for sentiment, frustration, sarcasm",
    instruction="""
You are a review analysis expert.
you are a subagent your parent agent is customer_feedback when he provide data do your task and print the output in the secheme given
Given a list of user reviews (with rating, source, and date), analyze each one and return:
- sentiment: "positive", "neutral", or "negative"
- confidence: float (0 to 1)
- frustrated: true if the user is upset
- sarcastic: true if sarcastic tone is detected

Each review in the response should retain the original fields: source, text, score, and date.
Respond ONLY with valid JSON using the output schema.
""",
    input_schema=ReviewBatchInput,
    output_schema=ReviewBatchOutput,
    output_key="review_result"
)
