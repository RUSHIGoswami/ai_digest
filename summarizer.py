"""
summarizer.py — Sends raw articles to Gemini, gets back a structured digest
                with categorization, summaries, and a TL;DR for each item.
"""

import json
import requests
from config import GEMINI_API_KEY, CATEGORIES, MAX_ITEMS_PER_CATEGORY

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"
)


def build_digest(articles: list[dict]) -> dict:
    """
    Returns a dict shaped like:
    {
        "tldr": "One-paragraph overview of today's AI landscape",
        "categories": {
            "🔧 For Developers": [
                {"title": "...", "summary": "...", "url": "...", "why_it_matters": "..."},
                ...
            ],
            ...
        }
    }
    """

    # Prepare a compact article list for the prompt (keep tokens reasonable)
    articles_text = ""
    for i, a in enumerate(articles[:120]):  # cap at 120 articles
        articles_text += f"\n---\nID: {i}\nSource: {a['source']}\nTitle: {a['title']}\nURL: {a['url']}\nSummary: {a['summary'][:300]}\n"

    categories_desc = "\n".join([f"- **{k}**: {v}" for k, v in CATEGORIES.items()])

    prompt = f"""You are an expert AI/ML analyst. I will give you a list of raw articles and posts from the last 24 hours.

Your job:
1. Read through all items and pick the MOST important and interesting ones.
2. Categorize each selected item into EXACTLY one of these categories:
{categories_desc}

3. For each selected item, write:
   - A crisp 2-sentence summary (jargon-free but technically accurate)
   - A "why_it_matters" line (1 sentence, direct developer/builder value)

4. Select at most {MAX_ITEMS_PER_CATEGORY} items per category. Quality over quantity.
5. Write a short "tldr" paragraph (3-4 sentences) summarizing the overall AI landscape today.

Respond ONLY with a valid JSON object, no markdown fences, in this exact structure:
{{
  "tldr": "...",
  "categories": {{
    "🔧 For Developers": [
      {{"title": "...", "summary": "...", "url": "...", "why_it_matters": "..."}}
    ],
    "📄 Research Breakthroughs": [...],
    "🚀 Startups & Funding": [...],
    "💡 Product Innovations": [...],
    "🌍 Industry & Big Moves": [...]
  }}
}}

Here are today's articles:
{articles_text}
"""

    print("[Summarizer] Sending to Gemini API...")
    resp = requests.post(
        GEMINI_URL,
        headers={"x-goog-api-key": GEMINI_API_KEY},
        json={
            "contents": [{"parts": [{"text": prompt}]}],
        },
        timeout=60,
    )
    resp.raise_for_status()
    raw = resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()

    # Strip accidental markdown fences
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    digest = json.loads(raw)
    print("[Summarizer] Done. Categories returned:", list(digest.get("categories", {}).keys()))
    return digest
