# 🛰️ AlphaSweep

**The Institutional-Grade Job Intelligence Engine**

**AlphaSweep** is a specialized reconnaissance tool designed to eliminate the "information lag" in the 2026 job market. By programmatically auditing Applicant Tracking Systems (ATS) and surfacing sub-indexed roles, AlphaSweep ensures you are in the first 0.1% of applicants for high-stakes Quant, SWE, and Investment roles.

## 🛠️ Core Capabilities

* **ATS Subdomain Infiltration:** Targets the "hidden" backends of Lever, Greenhouse, Ashby, Workday, and more.
* **Multi-Bucket Dorking:** Implements a 39-token logic split to bypass Google's 32-word limit, ensuring zero-loss keyword indexing.
* **Sub-Hourly Precision:** Powered by `APScheduler` for zero-drift monitoring at the top of every even hour.
* **Rich Discord Intelligence:** Streams formatted "Alpha Alerts" directly to your mobile device via Discord Webhooks.
* **Persistent Memory:** Uses a `Peewee` ORM-backed SQLite database to deduplicate listings across multiple aggregators.

---

## 🏗️ Repository Architecture

The "Beast" is built on a modular, monolithic architecture designed for 100% uptime and horizontal scaling.

```text
AlphaSweep/
├── engines/           # Specialized Discovery Spiders (Serper.dev)
├── models/            # Persistence Layer (Peewee ORM + SQLite)
├── utils/             # Notification Wrappers & Token Budgeting
├── core/              # Scheduling & Orchestration Logic
├── main.py            # The AlphaSweep Heartbeat
└── Dockerfile         # Containerized Deployment Configuration

```

---

## 🚀 Quick Start

### 1. Environment Configuration

Create a `.env` file in the root directory:

```bash
SERPER_KEY=
DB_NAME=jobs.db
DISCORD_WEBHOOK=
DISCORD_WEBHOOK_NAME=
DISCORD_WEBHOOK_AVATAR_URL=

```

### 2. Native Deployment

```bash
pip install -r requirements.txt
python main.py

```

### 3. Docker Deployment (Recommended)

```bash
docker build -t alphasweep .
docker run -d \
--name alphasweep_instance \
-v $(pwd)/data:/app/data \
--env-file .env \
alphasweep:latest
```

---

## 📊 Logic Engine: The "Ultimate Net"

AlphaSweep executes a rotating 3-bucket search strategy to maximize Serper.dev API credits:

| Bucket | Focus | Target Platforms |
| --- | --- | --- |
| **Alpha-Tier** | HFTs & Elite Startups | Lever, Greenhouse, Ashby, Resolu |
| **Institutional** | Global Banks | Workday, iCIMS, SmartRecruiters |
| **Emerging** | Boutique Finance | Pinpoint, Breezy, Gem |

---

## 🛡️ Anti-Detection & Stealth

To ensure longevity in 2026 scraping environments:

* **Human Jitter:** Randomized second-offsets for all scheduled tasks.
* **CDP Protocol:** Built-in hooks for SeleniumBase (optional) to bypass Cloudflare and PerimeterX shields.
* **Token Budgeting:** Automatic query auditing to prevent silent truncation.

---

## 📜 Disclaimer

*This tool is for educational and personal career advancement purposes only. Ensure your monitoring frequency complies with the Terms of Service of the respective platforms.*

---

**Developed by Stephen Sulimani | 2026 Quantitative Finance & SWE Discovery**

---
