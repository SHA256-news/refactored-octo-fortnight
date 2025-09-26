"""
Test that all modules import correctly
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

def test_imports():
    """Test that all main modules can be imported"""
    try:
        from src.news_processor import BitcoinNewsProcessor
        print("✅ BitcoinNewsProcessor imports successfully")
        
        from src.github_publisher import GitHubPublisher
        print("✅ GitHubPublisher imports successfully")
        
        from src.twitter_publisher import TwitterPublisher
        print("✅ TwitterPublisher imports successfully")
        
        from src.bitcoin_news_server import SHA256NewsServer
        print("✅ SHA256NewsServer imports successfully")
        
        print("🎉 All modules import successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

if __name__ == "__main__":
    test_imports()
