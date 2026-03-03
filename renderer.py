"""
renderer.py — Renders the digest dict into a beautiful HTML email.
"""

from datetime import datetime, timezone


# Category accent colors
CATEGORY_COLORS = {
    "🔧 For Developers":         "#6366f1",  # indigo
    "📄 Research Breakthroughs": "#10b981",  # emerald
    "🚀 Startups & Funding":     "#f59e0b",  # amber
    "💡 Product Innovations":    "#3b82f6",  # blue
    "🌍 Industry & Big Moves":   "#ef4444",  # red
}
DEFAULT_COLOR = "#8b5cf6"


def render_html(digest: dict) -> str:
    today = datetime.now(timezone.utc).strftime("%A, %B %d, %Y")
    tldr = digest.get("tldr", "")
    categories = digest.get("categories", {})

    # Build category HTML blocks
    category_blocks = ""
    for cat_name, items in categories.items():
        if not items:
            continue
        color = CATEGORY_COLORS.get(cat_name, DEFAULT_COLOR)

        items_html = ""
        for item in items:
            title   = item.get("title", "")
            summary = item.get("summary", "")
            url     = item.get("url", "#")
            why     = item.get("why_it_matters", "")
            items_html += f"""
            <div style="margin-bottom:20px; padding:16px; background:#f8fafc; border-left:4px solid {color}; border-radius:0 8px 8px 0;">
              <a href="{url}" style="font-size:15px; font-weight:600; color:#1e293b; text-decoration:none; line-height:1.4; display:block; margin-bottom:6px;">{title}</a>
              <p style="margin:0 0 8px 0; color:#475569; font-size:13.5px; line-height:1.6;">{summary}</p>
              <div style="display:inline-block; background:{color}18; border:1px solid {color}44; border-radius:4px; padding:4px 10px;">
                <span style="font-size:12px; color:{color}; font-weight:600;">💬 Why it matters: </span>
                <span style="font-size:12px; color:#334155;">{why}</span>
              </div>
            </div>"""

        category_blocks += f"""
        <div style="margin-bottom:36px;">
          <div style="display:flex; align-items:center; margin-bottom:16px; padding-bottom:10px; border-bottom:2px solid {color}22;">
            <div style="width:4px; height:24px; background:{color}; border-radius:2px; margin-right:12px;"></div>
            <h2 style="margin:0; font-size:17px; font-weight:700; color:#1e293b;">{cat_name}</h2>
            <span style="margin-left:8px; background:{color}18; color:{color}; font-size:11px; font-weight:600; padding:2px 8px; border-radius:99px;">{len(items)} items</span>
          </div>
          {items_html}
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Digest — {today}</title>
</head>
<body style="margin:0; padding:0; background:#f1f5f9; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">

  <div style="max-width:640px; margin:32px auto; background:#ffffff; border-radius:16px; overflow:hidden; box-shadow:0 4px 24px rgba(0,0,0,0.08);">

    <!-- Header -->
    <div style="background:linear-gradient(135deg, #1e293b 0%, #334155 50%, #1e3a5f 100%); padding:36px 40px;">
      <div style="display:flex; align-items:center; margin-bottom:8px;">
        <span style="font-size:28px; margin-right:12px;">🤖</span>
        <span style="font-size:13px; font-weight:600; color:#94a3b8; letter-spacing:2px; text-transform:uppercase;">AI/ML Daily Digest</span>
      </div>
      <h1 style="margin:0 0 8px 0; font-size:26px; font-weight:800; color:#ffffff; line-height:1.2;">{today}</h1>
      <p style="margin:0; color:#64748b; font-size:13px;">Last 24 hours · Curated by Claude</p>
    </div>

    <!-- TL;DR Section -->
    <div style="padding:28px 40px; background:#f8fafc; border-bottom:1px solid #e2e8f0;">
      <div style="display:flex; align-items:flex-start; gap:12px;">
        <div style="flex-shrink:0; background:#6366f1; color:white; font-size:11px; font-weight:700; padding:4px 8px; border-radius:4px; margin-top:2px; letter-spacing:0.5px;">TL;DR</div>
        <p style="margin:0; color:#334155; font-size:14.5px; line-height:1.7; font-style:italic;">{tldr}</p>
      </div>
    </div>

    <!-- Categories -->
    <div style="padding:32px 40px;">
      {category_blocks}
    </div>

    <!-- Footer -->
    <div style="padding:24px 40px; background:#f8fafc; border-top:1px solid #e2e8f0; text-align:center;">
      <p style="margin:0 0 4px 0; font-size:12px; color:#94a3b8;">Powered by Claude · Sources: HuggingFace, arXiv, Reddit, NewsAPI, OpenAI, DeepMind</p>
      <p style="margin:0; font-size:11px; color:#cbd5e1;">Your daily AI digest. Stay sharp. 🚀</p>
    </div>

  </div>

</body>
</html>"""
    return html


def render_plain_text(digest: dict) -> str:
    """Fallback plain text version."""
    today = datetime.now(timezone.utc).strftime("%A, %B %d, %Y")
    lines = [f"AI/ML Daily Digest — {today}", "=" * 50, "", f"TL;DR:\n{digest.get('tldr', '')}", ""]

    for cat_name, items in digest.get("categories", {}).items():
        if not items:
            continue
        lines.append(f"\n{cat_name}")
        lines.append("-" * 40)
        for item in items:
            lines.append(f"• {item['title']}")
            lines.append(f"  {item['summary']}")
            lines.append(f"  ↳ {item['why_it_matters']}")
            lines.append(f"  🔗 {item['url']}")
            lines.append("")

    return "\n".join(lines)
