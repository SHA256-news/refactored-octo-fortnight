# 🔗 SHA256-News: Automated Bitcoin Mining News System

> **Automated Bitcoin Mining Industry Analysis & Insights**

An AI-powered news automation system that fetches Bitcoin mining news, generates comprehensive analysis, and publishes content to GitHub Pages with Twitter thread distribution.

## 🚀 Features

- **📰 News Aggregation**: Fetches Bitcoin mining news from EventRegistry API
- **🤖 AI Analysis**: Generates comprehensive articles using Google Gemini AI
- **📊 Industry Focus**: Exclusively covers Bitcoin mining (no other cryptocurrencies)
- **🔗 SHA256 Hashing**: Uses SHA256 for content deduplication and article IDs
- **📝 GitHub Pages**: Automated publishing to GitHub Pages with Jekyll
- **🐦 Twitter Integration**: Automatic Twitter thread creation and posting
- **⚡ MCP Protocol**: Built as Model Context Protocol server for VS Code integration

## 🏗️ Architecture

    MCP Client (VS Code) → Python MCP Server →
    ├── EventRegistry API (Bitcoin mining news)
    ├── Google Gemini API (article generation + insights) 
    ├── GitHub API (create issues + GitHub Pages publishing)
    └── Twitter API via Tweepy (thread publishing)

## 🛠️ Setup

### Prerequisites

- Python 3.8+
- VS Code with MCP support
- API Keys for:
  - EventRegistry
  - Google Gemini
  - GitHub (Personal Access Token)
  - Twitter API v2

### Installation

1. **Clone the repository**:
   git clone https://github.com/SHA256-news/refactored-octo-fortnight.git
   cd refactored-octo-fortnight

2. **Install dependencies**:
   pip install -r requirements.txt

3. **Configure environment**:
   cp .env.example .env
   # Edit .env with your API keys

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| EVENT_REGISTRY_API_KEY | EventRegistry API key | ✅ |
| GEMINI_API_KEY | Google Gemini API key | ✅ |
| GITHUB_TOKEN | GitHub Personal Access Token | ✅ |
| TWITTER_API_KEY | Twitter API key | ✅ |
| TWITTER_API_SECRET | Twitter API secret | ✅ |
| TWITTER_ACCESS_TOKEN | Twitter access token | ✅ |
| TWITTER_ACCESS_TOKEN_SECRET | Twitter access token secret | ✅ |
| TWITTER_BEARER_TOKEN | Twitter bearer token | ✅ |

## 🎯 Usage

### MCP Server Integration

1. **Start the MCP server**:
   python src/bitcoin_news_server.py

2. **Available MCP Tools**:
   - fetch_bitcoin_mining_news - Fetch latest mining news
   - generate_holistic_article - Generate comprehensive analysis
   - publish_to_github - Publish to GitHub Pages
   - create_twitter_thread - Post Twitter thread
   - run_full_pipeline - Execute complete automation

### Manual Usage Example

You can also use individual components programmatically.

## 📊 Pipeline Flow

1. **🔍 News Fetching**: EventRegistry API searches for Bitcoin mining news
2. **🔧 Content Processing**: SHA256 hashing for deduplication
3. **🤖 AI Analysis**: Gemini generates comprehensive articles with insights
4. **📝 GitHub Publishing**: Articles published to GitHub Pages with Jekyll front matter
5. **📋 Issue Creation**: GitHub issues created for article review/discussion
6. **🐦 Twitter Distribution**: Automatic Twitter thread creation and posting

## 🔧 Development

### Project Structure

    SHA256-News/
    ├── src/
    │   ├── bitcoin_news_server.py    # Main MCP server
    │   ├── news_processor.py         # EventRegistry + Gemini integration
    │   ├── github_publisher.py       # GitHub Pages publishing
    │   └── twitter_publisher.py      # Twitter thread creation
    ├── tests/
    │   └── test_server.py            # Unit tests
    ├── docs/                         # GitHub Pages content
    ├── .github/
    │   ├── workflows/                # GitHub Actions
    │   └── copilot-instructions.md   # AI coding instructions
    ├── requirements.txt              # Python dependencies
    ├── .env.example                  # Environment variables template
    └── README.md                     # This file

### Running Tests

    pytest tests/

### Code Formatting

    black src/ tests/

## 🌟 Key Features

### Bitcoin-Only Focus
- Exclusively covers Bitcoin mining industry
- No other cryptocurrencies or blockchain projects
- SHA256 algorithm focus (hence the name)

### Advanced AI Analysis
- Google Gemini AI for comprehensive article generation
- Industry-specific insights and analysis
- Technical implications assessment
- Market impact evaluation

### Automated Publishing
- Jekyll-compatible GitHub Pages publishing
- SEO-optimized content with proper front matter
- Automatic article indexing and organization

### Social Media Integration
- Twitter thread generation with engaging content
- Proper hashtag usage and community engagement
- Thread metrics tracking and analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This is an automated news analysis system. All generated content should be reviewed before publication. The system is designed for informational purposes and does not provide financial advice.

## 🔗 Links

- **Website**: https://sha256-news.github.io/refactored-octo-fortnight
- **Twitter**: @SHA256_News (when created)
- **Repository**: https://github.com/SHA256-news/refactored-octo-fortnight

---

*Built with ❤️ for the Bitcoin mining community*
