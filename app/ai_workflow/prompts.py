from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from .schemas import MotivationalContent

parser = PydanticOutputParser(pydantic_object=MotivationalContent)

# List of motivational themes
THEMES = [
    "discipline", "courage", "self-belief", "focus", "learning from failure",
    "patience", "gratitude", "growth mindset", "taking action", "overcoming fear",
    "resilience", "success", "mindfulness", "determination", "creativity",
    "teamwork", "leadership", "passion", "positivity", "self-discipline"
]

PROMPT_TEMPLATE = ChatPromptTemplate.from_template("""
Generate SEO-optimized motivational content for YouTube Shorts.
Theme: "{theme}"

Instructions:
1. Motivational Sentences (4 total):
   - Step 1: Awakening
   - Step 2: Commitment
   - Step 3: Action
   - Step 4: Achievement
   - 4–6 words each, emotionally powerful, logical progression

2. Video Title:
   - Use these primary keywords only:
     "motivation", "motivational mindset", "growth mindset",
     "luxury lifestyle", "inspiration"
   - Short, catchy, SEO-friendly, emotionally engaging

3. YouTube Description:
   - Include 300–500 words, integrating keywords naturally
   - Opening hook: repeat title + value proposition
   - Main content: benefits, outcomes, urgency, retention hook
   - Keyword-rich section: motivational terms, lifestyle, long-tail phrases
   - Call-to-Action: encourage likes, comments, subscriptions, shares

4. Video Tags:
   - 15–20 highly relevant tags including primary keywords
   - Short, authentic, trending motivational terms

{format_instructions}
""")
