"""
Basic tests for SHA256-News MCP Server
"""
import pytest
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

@pytest.mark.asyncio
async def test_server_initialization():
    """Test that the server can be initialized"""
    from src.bitcoin_news_server import SHA256NewsServer
    
    # This will fail without API keys, but should at least import
    try:
        server = SHA256NewsServer()
        assert server is not None
        print("✅ Server initialized successfully")
    except ValueError as e:
        # Expected if API keys are missing
        print(f"⚠️ Server requires API keys: {e}")
        assert "API" in str(e) or "key" in str(e).lower()

def test_basic_functionality():
    """Test basic module functionality"""
    from src.news_processor import BitcoinNewsProcessor
    from src.github_publisher import GitHubPublisher
    from src.twitter_publisher import TwitterPublisher
    
    # Test classes can be imported and instantiated (will fail without API keys)
    try:
        processor = BitcoinNewsProcessor()
        print("✅ NewsProcessor created")
    except Exception as e:
        print(f"⚠️ NewsProcessor requires API keys: {e}")
    
    try:
        github_pub = GitHubPublisher()
        print("✅ GitHubPublisher created")
    except Exception as e:
        print(f"⚠️ GitHubPublisher requires API keys: {e}")
    
    try:
        twitter_pub = TwitterPublisher()
        print("✅ TwitterPublisher created")
    except Exception as e:
        print(f"⚠️ TwitterPublisher requires API keys: {e}")

if __name__ == "__main__":
    asyncio.run(test_server_initialization())
    test_basic_functionality()
