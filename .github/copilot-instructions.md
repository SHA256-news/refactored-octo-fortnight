# GitHub Copilot Instructions for SHA256-News

## Project Overview

SHA256-News is an automated Bitcoin mining news system that:
- Fetches Bitcoin mining news from EventRegistry API
- Generates comprehensive analysis using Google Gemini AI
- Publishes to GitHub Pages with Jekyll
- Creates Twitter threads for distribution
- Uses MCP (Model Context Protocol) for VS Code integration
- Focuses EXCLUSIVELY on Bitcoin mining (no other cryptocurrencies)

## Coding Guidelines

### Language & Framework
- **Primary Language**: Python 3.8+
- **Framework**: MCP Server with asyncio
- **APIs**: EventRegistry, Google Gemini, GitHub API, Twitter API v2
- **Dependencies**: See requirements.txt

### Bitcoin Mining Focus
- ONLY cover Bitcoin mining industry
- Focus on: hash rate, mining difficulty, ASIC miners, mining pools
- Keywords: "bitcoin mining", "miners", "hash rate", "mining difficulty"
- NO other cryptocurrencies (Ethereum, Litecoin, etc.)
- Use SHA256 hashing for content deduplication (thematic relevance)

### Code Style
- Follow PEP 8 standards
- Use type hints for all functions
- Async/await for I/O operations
- Comprehensive error handling with try/catch
- Docstrings for all classes and methods
- Use descriptive variable names
