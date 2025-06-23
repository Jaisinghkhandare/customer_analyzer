from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from typing import List


# Input Schema
class ReviewItem(BaseModel):
    source: str
    text: str
    score: int
    date: str


class AppIssueBatchInput(BaseModel):
    reviews: List[ReviewItem]


# Updated Output Schema
class ExtractedIssue(BaseModel):
    issue: str = Field(description="The reported issue in one sentence")
    tag: str = Field(description="Issue category: bug, crash, ui, performance, feature_request, other")
    priority: str = Field(description="Priority level: high, medium, low")


class AppIssueBatchOutput(BaseModel):
    results: List[ExtractedIssue]


# Agent Definition
extract_issues_agent = LlmAgent(
    name="extract_issues_agent",
    model="gemini-2.0-flash",
    description="Extracts user-reported app issues from reviews",
    instruction="""
You are an AI assistant that identifies problems in software applications based on user reviews.

Instructions:
- Read each review and extract only specific issues mentioned (e.g., bugs, crashes, UI glitches, performance lags, or missing features).
- Do not include the original review text in the output.
- For each issue:
  - Write a short one-line description.
  - Assign a tag: "bug", "crash", "ui", "performance", "feature_request", or "other".
  - Assign a priority: "high", "medium", or "low" based on user urgency or impact.

Return ONLY a flat list of issues in valid JSON format using the schema.
""",
    input_schema=AppIssueBatchInput,
    output_schema=AppIssueBatchOutput,
    output_key="results"
)
