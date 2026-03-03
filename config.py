# =============================================================================
# AI Digest - Configuration
# Set your secrets in GitHub Actions Secrets, not here.
# =============================================================================

import os
from dotenv import load_dotenv

load_dotenv()

# --- Your Details ---
RECIPIENT_EMAIL = os.environ.get("RECIPIENT_EMAIL", "you@gmail.com")
SENDER_EMAIL    = os.environ.get("SENDER_EMAIL", "you@gmail.com")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")  # Gmail App Password

# --- API Keys ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")  # https://aistudio.google.com (free)
NEWS_API_KEY   = os.environ.get("NEWS_API_KEY", "")    # https://newsapi.org (free)

# --- Digest Settings ---
MAX_ARTICLES_PER_SOURCE = 10   # How many raw articles to pull per source
MAX_ITEMS_PER_CATEGORY  = 5    # Max items shown per category in email

# --- News Sources ---
RSS_FEEDS = {
    "HuggingFace Blog": "https://huggingface.co/blog/feed.xml",
    "Papers with Code": "https://paperswithcode.com/latest.xml",
    "arXiv CS.AI":      "http://arxiv.org/rss/cs.AI",
    "arXiv CS.LG":      "http://arxiv.org/rss/cs.LG",
    "arXiv CS.CL":      "http://arxiv.org/rss/cs.CL",
    "MIT News AI":      "https://news.mit.edu/topic/artificial-intelligence2/feed",
    "DeepMind Blog":    "https://deepmind.google/blog/rss.xml",
    "OpenAI News":      "https://openai.com/blog/rss.xml",
}

REDDIT_SUBREDDITS = [
    "MachineLearning",
    "artificial",
    "LocalLLaMA",      # developer-focused, cutting edge open source
    "singularity",     # innovation breakthroughs
]

NEWSAPI_QUERIES = [
    "artificial intelligence",
    "large language model",
    "AI startup funding",
    "machine learning framework",
    "Generative AI",
    "Generative AI news",
    "Generative adversarial networks",
    "neural networks",
    "computer vision",
    "natural language processing",
    "reinforcement learning",
    "genetic algorithms",
    "swarm intelligence",
    "fuzzy logic",
    "evolutionary computation",
    "AI developer tools",
]

# --- Email Categories ---
CATEGORIES = {
    "🔧 For Developers":         "New tools, SDKs, APIs, libraries, frameworks, open-source releases developers can use right now.",
    "📄 Research Breakthroughs": "New papers, model architectures, benchmark results, and academic findings with real-world impact.",
    "🚀 Startups & Funding":     "New AI companies, funding rounds, acquisitions, and emerging players.",
    "💡 Product Innovations":    "New AI-powered products, features, demos, and launches for end users.",
    "🌍 Industry & Big Moves":   "Policy changes, major company announcements, open-source drops from big labs, ecosystem shifts.",
}
