"""
Twitter Publisher Module  
Handles creating and posting Twitter threads about published articles
"""

import os
import re
from typing import Dict, Any, List
from datetime import datetime

import tweepy
from dotenv import load_dotenv

load_dotenv()

class TwitterPublisher:
    """Creates and posts Twitter threads about Bitcoin mining articles"""
    
    def __init__(self):
        # Twitter API credentials
        self.api_key = os.getenv('TWITTER_API_KEY')
        self.api_secret = os.getenv('TWITTER_API_SECRET')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        
        if not all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
            raise ValueError("Twitter API credentials are required")
        
        # Initialize Tweepy client (v2 API)
        self.client = tweepy.Client(
            bearer_token=self.bearer_token,
            consumer_key=self.api_key,
            consumer_secret=self.api_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
            wait_on_rate_limit=True
        )
        
        self.max_tweets = int(os.getenv('TWITTER_THREAD_MAX_TWEETS', '10'))
    
    async def create_thread(
        self, 
        article_url: str, 
        summary: str, 
        insights: List[str] = None
    ) -> Dict[str, Any]:
        """Create and post Twitter thread about article"""
        
        try:
            # Generate thread content
            thread_tweets = self._generate_thread_content(article_url, summary, insights or [])
            
            # Post thread
            tweet_ids = []
            previous_tweet_id = None
            
            for i, tweet_text in enumerate(thread_tweets):
                if i == 0:
                    # First tweet
                    response = self.client.create_tweet(text=tweet_text)
                else:
                    # Reply to previous tweet
                    response = self.client.create_tweet(
                        text=tweet_text,
                        in_reply_to_tweet_id=previous_tweet_id
                    )
                
                tweet_ids.append(response.data['id'])
                previous_tweet_id = response.data['id']
            
            # Generate thread URL (first tweet URL)
            thread_url = f"https://twitter.com/i/web/status/{tweet_ids[0]}"
            
            return {
                'status': 'posted',
                'tweet_ids': tweet_ids,
                'thread_url': thread_url,
                'total_tweets': len(tweet_ids)
            }
            
        except Exception as e:
            raise Exception(f"Failed to create Twitter thread: {str(e)}")
    
    def _generate_thread_content(
        self, 
        article_url: str, 
        summary: str, 
        insights: List[str]
    ) -> List[str]:
        """Generate content for Twitter thread"""
        
        tweets = []
        
        # Tweet 1: Introduction with summary
        intro_text = f"🚀 New Bitcoin Mining Analysis!\n\n{summary[:200]}...\n\n🧵 Thread 👇"
        tweets.append(self._ensure_tweet_length(intro_text))
        
        # Tweet 2: Key insights
        if insights:
            insights_text = "📊 Key Insights:\n\n" + "\n".join([f"• {insight}" for insight in insights[:3]])
            tweets.append(self._ensure_tweet_length(insights_text))
        
        # Tweet 3: Industry impact
        impact_text = "⛏️ What this means for Bitcoin mining:\n\n• Network security implications\n• Miner profitability factors\n• Hash rate distribution effects"
        tweets.append(self._ensure_tweet_length(impact_text))
        
        # Tweet 4: Technical details
        tech_text = "🔧 Technical Highlights:\n\n• Mining difficulty adjustments\n• Hardware efficiency trends\n• Energy consumption patterns"
        tweets.append(self._ensure_tweet_length(tech_text))
        
        # Final tweet: Call to action with link
        final_text = f"📖 Read the full analysis:\n{article_url}\n\n💡 What are your thoughts on these developments?\n\n#Bitcoin #Mining #Cryptocurrency #SHA256News"
        tweets.append(self._ensure_tweet_length(final_text))
        
        # Ensure we don't exceed max tweets
        return tweets[:self.max_tweets]
    
    def _ensure_tweet_length(self, text: str, max_length: int = 280) -> str:
        """Ensure tweet doesn't exceed character limit"""
        
        if len(text) <= max_length:
            return text
        
        # Truncate and add ellipsis
        return text[:max_length-3] + "..."
    
    def test_connection(self) -> Dict[str, Any]:
        """Test Twitter API connection"""
        
        try:
            me = self.client.get_me()
            return {
                'status': 'connected',
                'username': me.data.username,
                'user_id': me.data.id
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
