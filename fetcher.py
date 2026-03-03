"""
fetcher.py — Pulls raw articles from all configured sources (last 24 hours).
Returns a unified list of dicts: {title, url, summary, source, published}
"""

import feedparser
import requests
import json
import time
from datetime import datetime, timezone, timedelta
from config import (
    RSS_FEEDS, REDDIT_SUBREDDITS, NEWSAPI_QUERIES,
    NEWS_API_KEY, MAX_ARTICLES_PER_SOURCE
)


def _is_recent(dt: datetime, hours: int = 24) -> bool:
    if dt is None:
        return True  # include if we can't determine age
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt >= cutoff


def _parse_rss_date(entry) -> datetime | None:
    for field in ("published_parsed", "updated_parsed"):
        t = getattr(entry, field, None)
        if t:
            try:
                return datetime(*t[:6], tzinfo=timezone.utc)
            except Exception:
                pass
    return None


# ---------------------------------------------------------------------------
# RSS / Atom Feeds
# ---------------------------------------------------------------------------
def fetch_rss() -> list[dict]:
    articles = []
    for source_name, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)
            count = 0
            for entry in feed.entries:
                if count >= MAX_ARTICLES_PER_SOURCE:
                    break
                pub = _parse_rss_date(entry)
                if not _is_recent(pub):
                    continue
                summary = getattr(entry, "summary", "") or getattr(entry, "description", "") or ""
                # Strip HTML tags simply
                import re
                summary = re.sub(r"<[^>]+>", " ", summary).strip()[:500]
                articles.append({
                    "title":     entry.get("title", "No title").strip(),
                    "url":       entry.get("link", ""),
                    "summary":   summary,
                    "source":    source_name,
                    "published": pub.isoformat() if pub else "unknown",
                })
                count += 1
        except Exception as e:
            print(f"[RSS] Failed {source_name}: {e}")
    print(f"[RSS] Fetched {len(articles)} articles")
    return articles


# ---------------------------------------------------------------------------
# Reddit (JSON API — no auth needed for public posts)
# ---------------------------------------------------------------------------
def fetch_reddit() -> list[dict]:
    articles = []
    headers = {"User-Agent": "ai-digest-bot/1.0"}
    for sub in REDDIT_SUBREDDITS:
        try:
            url = f"https://www.reddit.com/r/{sub}/hot.json?limit={MAX_ARTICLES_PER_SOURCE}"
            resp = requests.get(url, headers=headers, timeout=10)
            data = resp.json()
            for post in data["data"]["children"]:
                p = post["data"]
                if p.get("stickied"):
                    continue
                created = datetime.fromtimestamp(p.get("created_utc", 0), tz=timezone.utc)
                if not _is_recent(created):
                    continue
                articles.append({
                    "title":     p.get("title", "").strip(),
                    "url":       p.get("url", ""),
                    "summary":   (p.get("selftext", "") or p.get("url", ""))[:400],
                    "source":    f"r/{sub}",
                    "published": created.isoformat(),
                })
            time.sleep(1)  # be polite to Reddit
        except Exception as e:
            print(f"[Reddit] Failed r/{sub}: {e}")
    print(f"[Reddit] Fetched {len(articles)} posts")
    return articles


# ---------------------------------------------------------------------------
# NewsAPI
# ---------------------------------------------------------------------------
def fetch_newsapi() -> list[dict]:
    if not NEWS_API_KEY:
        print("[NewsAPI] No API key, skipping.")
        return []
    articles = []
    from_time = (datetime.now(timezone.utc) - timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")
    for query in NEWSAPI_QUERIES:
        try:
            resp = requests.get(
                "https://newsapi.org/v2/everything",
                params={
                    "q":        query,
                    "from":     from_time,
                    "sortBy":   "publishedAt",
                    "pageSize": MAX_ARTICLES_PER_SOURCE,
                    "language": "en",
                },
                headers={"X-Api-Key": NEWS_API_KEY},
                timeout=10,
            )
            data = resp.json()
            for a in data.get("articles", []):
                if not a.get("title") or a["title"] == "[Removed]":
                    continue
                articles.append({
                    "title":     a["title"].strip(),
                    "url":       a.get("url", ""),
                    "summary":   (a.get("description") or a.get("content") or "")[:500],
                    "source":    a.get("source", {}).get("name", "NewsAPI"),
                    "published": a.get("publishedAt", "unknown"),
                })
        except Exception as e:
            print(f"[NewsAPI] Failed query '{query}': {e}")
    print(f"[NewsAPI] Fetched {len(articles)} articles")
    return articles


# ---------------------------------------------------------------------------
# Master fetch
# ---------------------------------------------------------------------------
def fetch_all() -> list[dict]:
    all_articles = []
    all_articles.extend(fetch_rss())
    all_articles.extend(fetch_reddit())
    all_articles.extend(fetch_newsapi())

    # Deduplicate by URL
    seen_urls = set()
    unique = []
    for a in all_articles:
        url = a.get("url", "").split("?")[0]  # strip query params
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique.append(a)

    print(f"[Fetcher] Total unique articles: {len(unique)}")
    return unique
