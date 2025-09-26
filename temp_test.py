from eventregistry import EventRegistry, QueryArticles, RequestArticlesInfo, ReturnInfo
import os
from dotenv import load_dotenv

load_dotenv()

# Test basic EventRegistry connection
er = EventRegistry(apiKey=os.getenv('EVENT_REGISTRY_API_KEY'))

# Simple test query
q = QueryArticles(keywords="bitcoin mining")
q.setRequestedResult(RequestArticlesInfo(count=2))

print("Testing EventRegistry query...")
try:
    result = er.execQuery(q)
    print(f"✅ Query successful! Found {len(result.get('articles', {}).get('results', []))} articles")
except Exception as e:
    print(f"❌ Query failed: {e}")
