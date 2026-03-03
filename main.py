"""
main.py — Entry point. Run this directly or via GitHub Actions.

Usage:
    python main.py
"""

import sys
from fetcher    import fetch_all
from summarizer import build_digest
from renderer   import render_html, render_plain_text
from sender     import send_digest


def run():
    print("=" * 50)
    print("🤖 AI/ML Daily Digest — Starting")
    print("=" * 50)

    # Step 1: Fetch all articles from all sources
    print("\n[1/4] Fetching articles from all sources...")
    articles = fetch_all()
    if not articles:
        print("❌ No articles fetched. Check your network / API keys.")
        sys.exit(1)
    print(f"      Found {len(articles)} unique articles.")

    # Step 2: Send to Claude for categorization + summarization
    print("\n[2/4] Sending to Claude for analysis...")
    digest = build_digest(articles)

    # Step 3: Render HTML + plain text email
    print("\n[3/4] Rendering email...")
    html_body  = render_html(digest)
    plain_body = render_plain_text(digest)

    # Step 4: Send via Gmail
    print("\n[4/4] Sending email...")
    send_digest(html_body, plain_body)

    print("\n✅ Done! Digest sent successfully.")


if __name__ == "__main__":
    run()
