import json
import asyncio
import nest_asyncio
import requests
from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler, CacheMode, CrawlerRunConfig
from crawl4ai.extraction_strategy import JsonXPathExtractionStrategy

# Define the XPath schema for crawl4ai
schema = {
        "name": "News Content via XPath",
        "baseSelector": "//main[@id='main']",
        "fields": [
            {
                "name": "title",
                "selector": ".//h1[contains(@class, 'main-title')]",
                "type": "text"
            },
            {
                "name": "subtitle",
                "selector": ".//h2[contains(@class, 'sub-title')]",
                "type": "text"
            },
            {
                "name": "publish_date",
                "selector": ".//li[contains(@class, 'publish-date')]/time",
                "type": "text"
            },
            {
                "name": "publish_time",
                "selector": ".//li[contains(@class, 'publish-time')]/time",
                "type": "text"
            },
            {
                "name": "publisher",
                "selector": ".//li[contains(@class, 'publish-author')]//span[contains(@class, 'organization')]",
                "type": "text"
            },
            {
                "name": "author",
                "selector": ".//li[contains(@class, 'publish-author')]//span[contains(@class, 'name')]",
                "type": "text"
            },
            {
                "name": "tags",
                "selector": ".//div[contains(@class, 'taglist')]//li/a",
                "type": "list",
                "subtype": "text"
            },
            {
                "name": "main_image",
                "selector": ".//figure[contains(@class, 'picture--article')][1]//img",
                "type": "attribute",
                "attribute": "src"
            },
            {
                "name": "content",
                "selector": ".//div[contains(@class, 'article-wrap')]/article",
                "type": "text"
            }
        ]
    }

async def crawl4ai_crawl(url: str):
    async with AsyncWebCrawler() as crawler:
        try:
            extraction_strategy = JsonXPathExtractionStrategy(schema, verbose=True)
            config = CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                extraction_strategy=extraction_strategy,
            )
            result = await crawler.arun(url=url, config=config)
            title = result.metadata.get("title") if result.metadata else None
            
            if title:
                print(f"Succeeded: crawl4ai found: {title}")
                return {"url": url, "title": title}
            else:
                # If title is not found, indicate the failure
                print(f"WARN: crawl4ai did not find a title for {url}")
                return None  # Return None to trigger fallback crawling
        except Exception as e:
            # Handle exceptions and indicate error
            print(f"Error: crawl4ai encountered an error: {e}")
            return None  # Return None to trigger fallback crawling

# Fallback crawling method using BeautifulSoup
async def bs_crawl(url: str):
    try:
        web = requests.get(url)
        web.raise_for_status()        
        soup = BeautifulSoup(web.text, "html.parser")
        title = soup.title.get_text() if soup.title else "No title found"
        print(f"Succeeded: BeautifulSoup found: {title}")
        return {"url": url, "title": title}
    except requests.RequestException as e:
        print(f"Error: BeautifulSoup could not retrieve {url}: {e}")
        return {"url": url, "title": "Error"}

async def crawl_title(url: str):
    result = await crawl4ai_crawl(url)
    if result is None:
        result = bs_crawl(url)
    return result

async def crawl_titles(urls: list):
    tasks = [crawl_title(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results