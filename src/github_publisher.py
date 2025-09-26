"""
GitHub Publisher Module
Handles publishing articles to GitHub Pages and creating GitHub issues
"""

import os
import base64
from datetime import datetime
from typing import Dict, Any, Optional, List
import json
import re

from github import Github
from dotenv import load_dotenv

load_dotenv()

class GitHubPublisher:
    """Publishes articles to GitHub Pages and manages GitHub issues"""
    
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        if not self.github_token:
            raise ValueError("GITHUB_TOKEN environment variable is required")
        
        self.repo_owner = os.getenv('GITHUB_REPO_OWNER', 'SHA256-news')
        self.repo_name = os.getenv('GITHUB_REPO_NAME', 'refactored-octo-fortnight')
        self.pages_branch = os.getenv('GITHUB_PAGES_BRANCH', 'main')
        self.pages_path = os.getenv('GITHUB_PAGES_PATH', 'docs')
        
        self.github = Github(self.github_token)
        self.repo = self.github.get_repo(f"{self.repo_owner}/{self.repo_name}")
    
    async def publish_article(
        self, 
        content: str, 
        title: str, 
        tags: List[str] = None,
        create_issue: bool = True
    ) -> Dict[str, Any]:
        """Publish article to GitHub Pages"""
        
        try:
            # Generate filename from title
            filename = self._generate_filename(title)
            file_path = f"{self.pages_path}/articles/{filename}"
            
            # Create Jekyll front matter
            front_matter = self._create_front_matter(title, tags or [])
            
            # Combine front matter with content
            full_content = f"{front_matter}\n{content}"
            
            # Check if file already exists
            try:
                existing_file = self.repo.get_contents(file_path, ref=self.pages_branch)
                # Update existing file
                commit_result = self.repo.update_file(
                    path=file_path,
                    message=f"Update article: {title}",
                    content=full_content,
                    sha=existing_file.sha,
                    branch=self.pages_branch
                )
            except:
                # Create new file
                commit_result = self.repo.create_file(
                    path=file_path,
                    message=f"Publish article: {title}",
                    content=full_content,
                    branch=self.pages_branch
                )
            
            # Generate article URL
            article_url = f"https://{self.repo_owner}.github.io/{self.repo_name}/articles/{filename.replace('.md', '.html')}"
            
            # Create GitHub issue for review/discussion
            if create_issue:
                issue_result = await self._create_article_issue(title, article_url, tags or [])
            
            return {
                'status': 'published',
                'url': article_url,
                'file_path': file_path,
                'commit_sha': commit_result['commit'].sha,
                'issue_url': issue_result.get('html_url') if create_issue else None
            }
            
        except Exception as e:
            raise Exception(f"Failed to publish article to GitHub: {str(e)}")
    
    async def _create_article_issue(
        self, 
        title: str, 
        article_url: str, 
        tags: List[str]
    ) -> Dict[str, Any]:
        """Create GitHub issue for article discussion"""
        
        try:
            issue_title = f"📰 New Article: {title}"
            
            issue_body = f"""
## 🚀 New Bitcoin Mining Article Published

**Article Title:** {title}
**Published URL:** {article_url}
**Tags:** {', '.join(tags)}
**Published Date:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC

### 📋 Post-Publication Checklist
- [ ] Review article content and formatting
- [ ] Verify all links work correctly
- [ ] Check social media sharing
- [ ] Monitor for community feedback
- [ ] Update article index if needed

### 🐦 Twitter Thread
This issue will be updated with the Twitter thread URL once posted.

### 💬 Discussion
Use this issue to discuss the article, suggest improvements, or report any issues.

---
*This issue was automatically created by SHA256-News automation system.*
"""
            
            # Create issue
            issue = self.repo.create_issue(
                title=issue_title,
                body=issue_body,
                labels=['article', 'automated', 'bitcoin-mining'] + [f"tag:{tag}" for tag in tags[:3]]
            )
            
            return {
                'number': issue.number,
                'html_url': issue.html_url,
                'title': issue.title
            }
            
        except Exception as e:
            print(f"Warning: Failed to create GitHub issue: {str(e)}")
            return {}
    
    def _generate_filename(self, title: str) -> str:
        """Generate filename from article title"""
        # Remove special characters and convert to lowercase
        filename = re.sub(r'[^\w\s-]', '', title.lower())
        filename = re.sub(r'[-\s]+', '-', filename)
        
        # Add date prefix
        date_prefix = datetime.utcnow().strftime('%Y-%m-%d')
        
        # Limit filename length
        if len(filename) > 50:
            filename = filename[:50].rstrip('-')
        
        return f"{date_prefix}-{filename}.md"
    
    def _create_front_matter(self, title: str, tags: List[str]) -> str:
        """Create Jekyll front matter for the article"""
        
        front_matter = f"""---
layout: post
title: "{title}"
date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} +0000
categories: [bitcoin, mining]
tags: {json.dumps(tags)}
author: SHA256-News
description: "Automated Bitcoin mining industry analysis and insights"
image: /assets/images/bitcoin-mining-default.jpg
---"""
        
        return front_matter
