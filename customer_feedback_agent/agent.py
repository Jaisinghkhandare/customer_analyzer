import re
import json
from typing import Dict, List
from google.adk.agents import Agent
from google_play_scraper import reviews, Sort
# agents/root_agent.py


from customer_feedback_agent.sub_agent.sentiment_analysis_agent import sentiment_analysis_agent
from customer_feedback_agent.sub_agent.extract_issues_agent import extract_issues_agent
# Now you can call it like this:



import os

def fetch_playstore_reviews(app_url: str, count: int = 50) -> List[Dict]:
    """Fetches reviews from a Play Store app URL.
    Args:
        app_url: Play Store URL (e.g., https://play.google.com/store/apps/details?id=com.example).
        count: Number of reviews to fetch.
    Returns:
        List of review dictionaries with text, score, and date.
    """
    try:
        app_id = re.search(r"id=([\w\.]+)", app_url).group(1)
        result, _ = reviews(
            app_id,
            lang="en",
            country="us",
            sort=Sort.NEWEST,
            count=count,
        )
        return [
            {
                "source": "playstore",
                "text": r["content"],
                "score": r["score"],
                "date": r["at"].strftime("%Y-%m-%d"),
            }
            for r in result
        ]
    except Exception as e:
        return [{"status": "error", "message": f"Failed to fetch reviews: {str(e)}"}]

root_agent = Agent(
    name="customer_feedback_agent",
    description=(
        "The central orchestrator agent in a multi-agent system designed to help app developers understand their users better. "
        "This AI agent gathers, organizes, and updates customer reviews from the Google Play Store and coordinates with sub-agents "
        "like the topic extractor and sentiment analyzer to generate actionable insights. It maintains a central review store (JSON format) "
        "and intelligently routes developer queries to the appropriate analysis agents. Ideal for identifying app issues, understanding "
        "public perception, and improving overall app quality."
        "Once reviews are fetched, ask the user: - Type 1 to extract issues → delegate to `extract_issues_agent`- Type 2 for sentiment analysis → delegate to `sentiment_analysis_agent`Send the fetched reviews to the appropriate subagent using its input schema" 
        
    ),
    model="gemini-2.0-flash",
    instruction=(
       "You are the entry-point agent of a multi-agent system for analyzing customer feedback from Play Store reviews.\n\n"
        "Your primary responsibilities are:\n"
        "1. Prompt the developer to input the app’s Play Store URL or package name.\n"
        "2. Use internal tools to fetch up to 50 recent Play Store reviews (due to API limitations).\n"
        "3. Store and maintain these reviews in a centralized JSON file.\n"
        "4. On developer request:\n"
        "   - For identifying app issues, refresh the review set if needed, then invoke the `topic_extractor` agent to extract recurring complaints or bugs.\n"
        "   - For understanding the app’s public image or perception, fetch additional reviews if possible and invoke the `sentiment_analyzer` agent to categorize user sentiment (positive, neutral, negative).\n"
        "\nYour job is NOT to interpret or analyze the reviews directly, but to ensure accurate data flow between the input, review storage, and sub-agent analysis pipelines. "
        "Always ensure the output shown to the developer is based on real user reviews, and delegate intelligent processing to the appropriate agent."
        "Once reviews are fetched, ask the user: - Type 1 to extract issues → delegate to `topic_extr`- Type 2 for sentiment analysis → delegate to `multi_tool_agent`Send the fetched reviews to the appropriate subagent using its input schema"
    ),
    sub_agents=[sentiment_analysis_agent,extract_issues_agent ],
    tools=[fetch_playstore_reviews],
)







