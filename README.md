# 🤖 AI/ML Daily Digest

> A self-hosted, zero-cost daily email service that sends you a curated, categorized AI/ML digest every morning — powered by Gemini.

---

## What You Get

A beautiful HTML email every morning with last 24h highlights, organized into:

| Category | What's inside |
|---|---|
| 🔧 For Developers | New tools, SDKs, frameworks, open-source releases |
| 📄 Research Breakthroughs | Papers, model releases, benchmark results |
| 🚀 Startups & Funding | New companies, funding rounds, acquisitions |
| 💡 Product Innovations | AI-powered products, demos, launches |
| 🌍 Industry & Big Moves | Policy, big lab announcements, ecosystem shifts |

**Sources:** HuggingFace Blog, arXiv (AI/LG/CL), Papers with Code, OpenAI, DeepMind, MIT News, Reddit (r/MachineLearning, r/artificial, r/LocalLLaMA, r/singularity), NewsAPI

---

## Setup (5 minutes)

### 1. Fork / Clone this repo
```bash
git clone https://github.com/YOUR_USERNAME/ai-digest.git
cd ai-digest
```

### 2. Get your API Keys

| Key | Where to get it | Free? |
|---|---|---|
| `GEMINI_API_KEY` | [aistudio.google.com](https://aistudio.google.com) | ✅ Free (1,500 req/day) |
| `NEWS_API_KEY` | [newsapi.org](https://newsapi.org/register) | ✅ Free (100 req/day) |
| `GMAIL_APP_PASSWORD` | See below | ✅ Free |

**Gmail App Password setup:**
1. Enable 2FA on your Google account: [myaccount.google.com/security](https://myaccount.google.com/security)
2. Go to: [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Create a new app password (name it "AI Digest")
4. Copy the 16-character password

### 3. Add GitHub Secrets

In your GitHub repo → **Settings → Secrets and variables → Actions → New repository secret**

Add these 5 secrets:

| Secret | Value |
|---|---|
| `GEMINI_API_KEY` | Your Gemini key |
| `NEWS_API_KEY` | Your NewsAPI key |
| `SENDER_EMAIL` | your.gmail@gmail.com |
| `RECIPIENT_EMAIL` | your.gmail@gmail.com (can be same) |
| `GMAIL_APP_PASSWORD` | The 16-char app password |

### 4. Customize Delivery Time

Edit `.github/workflows/daily_digest.yml`:

```yaml
- cron: "30 1 * * *"   # 7:00 AM IST (UTC+5:30)
```

Use [crontab.guru](https://crontab.guru) to generate your preferred time in UTC.

Common IST times:
- 7:00 AM IST → `30 1 * * *`
- 8:00 AM IST → `30 2 * * *`
- 9:00 AM IST → `30 3 * * *`

### 5. Enable & Test

- Push to GitHub → Actions tab → the workflow will appear
- Click **"Run workflow"** to test it manually right now
- Check your inbox in ~60 seconds

---

## Running Locally

```bash
pip install -r requirements.txt

export GEMINI_API_KEY="sk-ant-..."
export NEWS_API_KEY="your-newsapi-key"
export SENDER_EMAIL="you@gmail.com"
export RECIPIENT_EMAIL="you@gmail.com"
export GMAIL_APP_PASSWORD="xxxx xxxx xxxx xxxx"

python main.py
```

---

## Cost Estimate

| Item | Cost |
|---|---|
| GitHub Actions | **Free** (2,000 min/month) |
| NewsAPI | **Free** (100 req/day) |
| Gmail SMTP | **Free** |
| Gemini 2.0 Flash | **Free** (1,500 req/day) |

**Total: ~$0.30–0.90/month**

---

## Customization

**Add/remove news sources:** Edit `RSS_FEEDS` and `REDDIT_SUBREDDITS` in `config.py`

**Change categories:** Edit `CATEGORIES` dict in `config.py` — Claude will automatically use your new categories

**More items per category:** Increase `MAX_ITEMS_PER_CATEGORY` in `config.py`

---

## Project Structure

```
ai-digest/
├── main.py                          # Entry point
├── config.py                        # All settings
├── fetcher.py                       # News source aggregator
├── summarizer.py                    # Claude API integration
├── renderer.py                      # HTML email template
├── sender.py                        # Gmail SMTP delivery
├── requirements.txt
└── .github/workflows/
    └── daily_digest.yml             # GitHub Actions cron
```
