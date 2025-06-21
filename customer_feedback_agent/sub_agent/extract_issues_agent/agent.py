from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from typing import List

# Define schema for each review input
class ReviewItem(BaseModel):
    source: str
    text: str
    score: int
    date: str

# Define schema for each review output
class SingleReviewIssueOutput(BaseModel):
    text: str
    issues: List[str] = Field(description="List of application or product issues mentioned in the review")
    issue_count: int = Field(description="Number of distinct issues found")

# Full input schema for batch
class AppIssueBatchInput(BaseModel):
    reviews: List[ReviewItem]

# Full output schema for batch
class AppIssueBatchOutput(BaseModel):
    results: List[SingleReviewIssueOutput]

# Define the agent
extract_issues_agent = LlmAgent(
    name="extract_issues_agent",
    model="gemini-2.0-flash",
    description="Extracts app issues from a list of user reviews",
    instruction="""
You are an AI assistant that identifies problems in software applications or products based on user reviews.

Instructions:
- For each review, extract all user-reported issues such as bugs, crashes, UI problems, missing features, or poor performance.
- List each issue as a short bullet point (max 1 sentence).
- Count and return the number of distinct issues.
- Include the original 'text' field in your response.
- Return ONLY valid JSON using the defined output schema.
""",
    input_schema=AppIssueBatchInput,
    output_schema=AppIssueBatchOutput,
    output_key="issue_analysis"
)
