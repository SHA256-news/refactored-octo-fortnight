#!/usr/bin/env python3
"""
SHA256-News: Bitcoin Mining News Automation MCP Server
Fetches Bitcoin mining news, generates insights, and publishes to GitHub Pages + Twitter
"""

import asyncio
import hashlib
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest, 
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent
)

from dotenv import load_dotenv
from src.news_processor import BitcoinNewsProcessor
from src.github_publisher import GitHubPublisher  
from src.twitter_publisher import TwitterPublisher

# Load environment variables
load_dotenv()

class SHA256NewsServer:
    """MCP Server for Bitcoin Mining News Automation"""
    
    def __init__(self):
        self.server = Server("sha256-news-server")
        self.news_processor = BitcoinNewsProcessor()
        self.github_publisher = GitHubPublisher()
        self.twitter_publisher = TwitterPublisher()
        
        # In-memory storage for processed articles (use Redis in production)
        self.processed_articles = {}
        self.article_cache = {}
        
        self.setup_tools()
    
    def setup_tools(self):
        """Register MCP tools"""
        
        @self.server.list_tools()
        async def list_tools() -> ListToolsResult:
            return ListToolsResult(
                tools=[
                    Tool(
                        name="fetch_bitcoin_mining_news",
                        description="Fetch latest Bitcoin mining news from EventRegistry API",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "max_articles": {
                                    "type": "integer", 
                                    "description": "Maximum number of articles to fetch",
                                    "default": 10
                                },
                                "days_back": {
                                    "type": "integer",
                                    "description": "Days to look back for news",
                                    "default": 1
                                }
                            }
                        }
                    ),
                    Tool(
                        name="generate_holistic_article", 
                        description="Generate comprehensive article with insights using Gemini AI",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "article_sources": {
                                    "type": "array",
                                    "description": "Array of source articles to analyze",
                                    "items": {"type": "object"}
                                },
                                "focus_angle": {
                                    "type": "string",
                                    "description": "Specific angle or theme to focus on",
                                    "default": "mining industry impact"
                                }
                            },
                            "required": ["article_sources"]
                        }
                    ),
                    Tool(
                        name="publish_to_github",
                        description="Publish generated article to GitHub Pages",
                        inputSchema={
                            "type": "object", 
                            "properties": {
                                "article_content": {
                                    "type": "string",
                                    "description": "Markdown content of the article"
                                },
                                "title": {
                                    "type": "string", 
                                    "description": "Article title"
                                },
                                "tags": {
                                    "type": "array",
                                    "description": "Article tags",
                                    "items": {"type": "string"}
                                }
                            },
                            "required": ["article_content", "title"]
                        }
                    ),
                    Tool(
                        name="create_twitter_thread",
                        description="Create and post Twitter thread about published article", 
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "article_url": {
                                    "type": "string",
                                    "description": "Published article URL"
                                },
                                "article_summary": {
                                    "type": "string", 
                                    "description": "Brief summary for thread"
                                },
                                "key_insights": {
                                    "type": "array",
                                    "description": "Key insights to highlight",
                                    "items": {"type": "string"}
                                }
                            },
                            "required": ["article_url", "article_summary"]
                        }
                    ),
                    Tool(
                        name="run_full_pipeline",
                        description="Execute complete news automation pipeline",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "auto_publish": {
                                    "type": "boolean",
                                    "description": "Whether to auto-publish or create draft",
                                    "default": False
                                }
                            }
                        }
                    )
                ]
            )
        
        @self.server.call_tool()
        async def call_tool(request: CallToolRequest) -> CallToolResult:
            """Handle tool calls"""
            try:
                if request.params.name == "fetch_bitcoin_mining_news":
                    return await self._fetch_bitcoin_mining_news(request.params.arguments)
                elif request.params.name == "generate_holistic_article":
                    return await self._generate_holistic_article(request.params.arguments) 
                elif request.params.name == "publish_to_github":
                    return await self._publish_to_github(request.params.arguments)
                elif request.params.name == "create_twitter_thread":
                    return await self._create_twitter_thread(request.params.arguments)
                elif request.params.name == "run_full_pipeline": 
                    return await self._run_full_pipeline(request.params.arguments)
                else:
                    raise ValueError(f"Unknown tool: {request.params.name}")
                    
            except Exception as e:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error: {str(e)}")],
                    isError=True
                )
    
    async def _fetch_bitcoin_mining_news(self, args: Dict) -> CallToolResult:
        """Fetch Bitcoin mining news using EventRegistry"""
        max_articles = args.get("max_articles", 10)
        days_back = args.get("days_back", 1)
        
        try:
            articles = await self.news_processor.fetch_mining_news(
                max_articles=max_articles,
                days_back=days_back
            )
            
            # Generate SHA256 hashes for deduplication
            for article in articles:
                content_hash = hashlib.sha256(
                    (article['title'] + article['body']).encode('utf-8')
                ).hexdigest()
                article['sha256_hash'] = content_hash
                
            return CallToolResult(
                content=[TextContent(
                    type="text", 
                    text=json.dumps({
                        "status": "success",
                        "articles_found": len(articles),
                        "articles": articles
                    }, indent=2)
                )]
            )
            
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Failed to fetch news: {str(e)}")],
                isError=True
            )
    
    async def _generate_holistic_article(self, args: Dict) -> CallToolResult:
        """Generate comprehensive article using Gemini AI"""
        article_sources = args.get("article_sources", [])
        focus_angle = args.get("focus_angle", "mining industry impact")
        
        try:
            generated_article = await self.news_processor.generate_comprehensive_article(
                source_articles=article_sources,
                focus_angle=focus_angle
            )
            
            # Generate article ID
            article_id = hashlib.sha256(
                generated_article['title'].encode('utf-8')
            ).hexdigest()[:12]
            
            generated_article['article_id'] = article_id
            generated_article['generated_at'] = datetime.utcnow().isoformat()
            
            # Cache the article
            self.article_cache[article_id] = generated_article
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(generated_article, indent=2)
                )]
            )
            
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Failed to generate article: {str(e)}")],
                isError=True
            )
    
    async def _publish_to_github(self, args: Dict) -> CallToolResult:
        """Publish article to GitHub Pages"""
        article_content = args.get("article_content")
        title = args.get("title") 
        tags = args.get("tags", [])
        
        try:
            result = await self.github_publisher.publish_article(
                content=article_content,
                title=title, 
                tags=tags
            )
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps({
                        "status": "published",
                        "article_url": result['url'],
                        "github_commit": result['commit_sha']
                    }, indent=2)
                )]
            )
            
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Failed to publish: {str(e)}")], 
                isError=True
            )
    
    async def _create_twitter_thread(self, args: Dict) -> CallToolResult:
        """Create Twitter thread about published article"""
        article_url = args.get("article_url")
        article_summary = args.get("article_summary")
        key_insights = args.get("key_insights", [])
        
        try:
            thread_result = await self.twitter_publisher.create_thread(
                article_url=article_url,
                summary=article_summary,
                insights=key_insights
            )
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps({
                        "status": "posted",
                        "thread_tweets": len(thread_result['tweet_ids']),
                        "thread_url": thread_result['thread_url']
                    }, indent=2)
                )]
            )
            
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Failed to create thread: {str(e)}")],
                isError=True
            )
    
    async def _run_full_pipeline(self, args: Dict) -> CallToolResult:
        """Execute the complete automation pipeline"""
        auto_publish = args.get("auto_publish", False)
        
        try:
            # Step 1: Fetch news
            fetch_result = await self._fetch_bitcoin_mining_news({"max_articles": 5, "days_back": 1})
            articles_data = json.loads(fetch_result.content[0].text)
            
            if not articles_data.get("articles"):
                return CallToolResult(
                    content=[TextContent(type="text", text="No new articles found")]
                )
            
            # Step 2: Generate comprehensive article
            generate_result = await self._generate_holistic_article({
                "article_sources": articles_data["articles"],
                "focus_angle": "Bitcoin mining industry developments"
            })
            generated_content = json.loads(generate_result.content[0].text)
            
            # Step 3: Publish to GitHub (if auto_publish is True)
            if auto_publish:
                publish_result = await self._publish_to_github({
                    "article_content": generated_content["content"],
                    "title": generated_content["title"],
                    "tags": ["bitcoin", "mining", "cryptocurrency"]
                })
                publish_data = json.loads(publish_result.content[0].text)
                
                # Step 4: Create Twitter thread
                thread_result = await self._create_twitter_thread({
                    "article_url": publish_data["article_url"],
                    "article_summary": generated_content["summary"],
                    "key_insights": generated_content.get("key_insights", [])
                })
                
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=json.dumps({
                            "pipeline_status": "completed",
                            "article_published": True,
                            "twitter_thread_posted": True,
                            "article_url": publish_data["article_url"]
                        }, indent=2)
                    )]
                )
            else:
                return CallToolResult(
                    content=[TextContent(
                        type="text", 
                        text=json.dumps({
                            "pipeline_status": "draft_ready",
                            "article_generated": True,
                            "title": generated_content["title"],
                            "word_count": len(generated_content["content"].split())
                        }, indent=2)
                    )]
                )
                
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Pipeline failed: {str(e)}")],
                isError=True
            )

async def main():
    """Main entry point"""
    server = SHA256NewsServer()
    async with stdio_server() as streams:
        await server.server.run(streams[0], streams[1])

if __name__ == "__main__":
    asyncio.run(main())
