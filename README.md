# 🛡️ S.H.I.E.L.D. Threat Analysis Platform

An AI-powered threat monitoring system that automatically processes real-world news articles to identify, categorize, and track security threats. Built with Python, FastAPI, and Google's Gemini AI.

## 🌟 Features

- **Automated Threat Detection**: Processes news articles hourly using Google's Gemini AI to identify potential threats
- **Smart Filtering**: AI analyzes threat level (1-10), category, confidence scores, and provides detailed summaries
- **Duplicate Prevention**: Automatically filters out previously analyzed articles to optimize API usage
- **REST API**: 8+ endpoints for threat retrieval, filtering, and human review
- **Human-in-the-Loop**: Review system with override capabilities for AI assessments
- **Rolling Database**: Automatically maintains a 5-day window of current threats
- **Scheduled Monitoring**: Runs every hour to keep threat intelligence up-to-date

## 🏗️ Architecture

```
NewsAPI → Data Pipeline → Gemini AI Analysis → SQLite Database → FastAPI Endpoints
                ↓                                      ↓
         Duplicate Check                    Human Review System
```

## 🛠️ Tech Stack

- **Backend**: Python 3.13, FastAPI
- **Database**: SQLite, SQLAlchemy ORM
- **AI**: Google Gemini 2.0 Flash
- **News Source**: NewsAPI
- **Validation**: Pydantic
- **Scheduling**: APScheduler
- **Server**: Uvicorn

## 📋 Prerequisites

- Python 3.13+
- NewsAPI API Key ([Get one here](https://newsapi.org))
- Google Gemini API Key ([Get one here](https://ai.google.dev/))

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/aamogh16/shield-threat-analysis.git
cd shield-threat-analysis
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory:
```env
NEWS_API_KEY=your_newsapi_key_here
GEMINI_API_KEY=your_gemini_key_here
```

5. **Initialize the database**
```bash
python scripts/create_tables.py
```

## 💻 Usage

### Run the API Server

```bash
uvicorn app.main:app --reload
```

Access the interactive API documentation at `http://127.0.0.1:8000/docs`

### Run the Automated Threat Pipeline

**One-time execution:**
```bash
python scripts/full_threat_pipeline.py
```

**Scheduled hourly monitoring:**
```bash
python scripts/full_threat_pipeline.py
# The scheduler runs continuously, processing threats every hour
```

### Test the Pipeline

```bash
python -m tests.test_pipeline
```

## 📡 API Endpoints

### Core Endpoints
- `GET /` - Health check and system status
- `GET /api/threats` - Get all threats
- `GET /api/threats/count` - Get total threat count
- `GET /api/threats/{threat_id}` - Get specific threat by ID

### Filtering Endpoints
- `GET /api/threats/recent?days=3` - Get threats from last N days
- `GET /api/threats/level/{min_level}` - Get threats at or above threat level
- `GET /api/threats/search?q=keyword` - Search threats by keywords

### Special Endpoints
- `GET /api/threats/fury-overview` - Director Fury's executive overview
- `GET /api/threats/pending_review` - Get threats needing human review
- `PUT /api/threats/{threat_id}/review` - Submit human review/override

## 🎯 How It Works

### 1. **News Fetching**
- Retrieves top headlines from NewsAPI (US focus)
- Can be configured for multiple countries/categories

### 2. **Duplicate Detection**
- Checks article URLs against database
- Prevents redundant API calls and processing

### 3. **AI Analysis**
- Sends articles to Gemini AI for threat assessment
- Batch processes up to 20 articles per request for efficiency
- AI evaluates: threat level, category, confidence, summary, keywords

### 4. **Database Storage**
- Only stores articles identified as threats (level 3+)
- Maintains both AI assessments and optional human overrides
- Auto-cleans threats older than 5 days

### 5. **Human Review**
- Low-confidence threats flagged for review
- Humans can override AI assessments
- Full audit trail maintained

## 📊 Database Schema

### Threat Table
- **Article Info**: title, description, source, URL, published date
- **AI Analysis**: threat_level, category, summary, confidence, keywords, reason
- **Human Override**: human_threat_level, category, notes, reviewer, review date
- **Metadata**: created_at, updated_at, is_active, requires_review

## 🎨 Project Structure

```
shield-threat-analysis/
├── app/
│   ├── main.py              # FastAPI application & endpoints
│   ├── database.py          # Database configuration
│   ├── models/
│   │   └── threat.py        # SQLAlchemy Threat model
│   ├── schemas/
│   │   └── threat.py        # Pydantic validation schemas
│   └── services/
│       ├── news_fetcher.py  # NewsAPI integration
│       ├── ai_analyzer.py   # Gemini AI integration
│       └── threat_processor.py  # Core processing logic
├── scripts/
│   ├── create_tables.py     # Database initialization
│   └── full_threat_pipeline.py  # Automated monitoring
├── tests/
│   └── test_pipeline.py     # Pipeline testing
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
└── README.md
```

## 🔐 Security Considerations

- API keys stored in environment variables
- Database includes soft-delete functionality
- Human review system for oversight
- Rate limiting on external APIs

## 📈 Future Enhancements

- [ ] Deploy to cloud platform (Railway/Render)
- [ ] Add WebSocket for real-time threat notifications
- [ ] Implement user authentication
- [ ] Add data visualization dashboard
- [ ] Expand to multiple news sources
- [ ] Add threat trending analysis
- [ ] Email notifications for high-priority threats

## 🤝 Contributing

This is a personal project, but feedback and suggestions are welcome! Feel free to open an issue or submit a pull request.

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

**Amogh Athimamula**
- GitHub: [@aamogh16](https://github.com/aamogh16)
- LinkedIn: [Amogh Athimamula](https://linkedin.com/in/amoghathimamula)
- Email: athimamula.a@northeastern.edu

## 🙏 Acknowledgments

- NewsAPI for providing real-time news data
- Google Gemini AI for advanced threat analysis
- Northeastern University for academic support
- Marvel's S.H.I.E.L.D. for the inspiration 🦅

---

**Built with ❤️ by Amogh Athimamula | Northeastern University CS '28**
